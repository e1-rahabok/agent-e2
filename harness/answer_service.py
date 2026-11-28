"""Agent E2 as a service: one HTTP endpoint that answers a question with the live facts a caller sends.

The caller is PCM (Private Cloud Management): PCM owns the data, the actions, the user's identity and every screen;
Agent E2 owns the knowledge base, the reading plan, the flow executor and the model call (ARCHITECTURE.md,
section Agent E2 in PCM). The answer is the shipped pipeline, `answer_modes.converse('agent-e2', ...)`, unchanged.

    POST /v1/answer
      {"question": "...", "facts": {...} (optional, JSON from the caller), "turns": [...] (optional, for the clarifying
       round: [question, Agent E2's questions, the user's reply]), "history": [{"question": "...", "answer": "..."}, ...]
       (optional: every earlier turn of the current topic, oldest first, uncut; the service holds no state, so the caller
       keeps the conversation), "topic_choice": "auto" | "new" | "continue" (optional, default auto: Agent E2 decides; new
       or continue: the user chose), "role": "l1" | "l2" | "capacity" | "executive" (optional)}
    -> 200 {"type": "answer" | "clarify", "content": "...", "questions": [...], "files_read": [...],
            "lead": "...", "computed": [...], "topic": {"continues": true | false, "by": "user" | "first" | "code" |
            "model" | "unsure"}, "shape": "...", "page_values": true | false, "model": "...", "knowledge_commit": "..."}
    shape and page_values: what the question asks, read by the model (answer_shape.decide). page_values false: a question
    on how a score works in general; the page is named, its values and the opening are not used.
    topic: whether the question continued the topic of `history` (topic_decision.py); when it did not, `history` was not
    used and the caller starts a new topic with this turn.
    lead: the opening the person reads first, written by code from the calculator's numbers in plain words (empty when no
    KPI series was sent); the model's text continues from it. computed: the calculator's lines, exact, for review; the
    screen shows the lead, not these.
    POST /v1/suggest
      {"facts": {"object": {"kind": "cluster" | "host" | "vm"}, "pillar": "Performance" | "Capacity", "window": "...",
                 "kpis": [{"label": "...", "better": "higher" | "lower", "points": [[time, value], ...]}, ...]}}
    -> 200 {"situation": {"pillar", "kind", "level": "good" | "medium" | "bad", "movement": null | "declining" | "dip" | "rising"},
            "questions": [3 at most], "basis": [...]}
    The questions a whole page suggests, chosen by its situation, read by code with no model call (user_suggestions.py).
    With "card": {"kind", "name"} and the card's facts: {"question", "card", "condition"}, the card's showcase question.
    POST /v1/topic
      {"question": "...", "history": [...], "topic_choice": "auto" | "new" | "continue", "turns": [...]} (as for /v1/answer)
    -> 200 {"continues": true | false, "by": "user" | "first" | "code" | "model" | "unsure"}
    The topic decision alone (topic_decision.py), the same one /v1/answer makes: the caller shows it before the answer, the
    person can flip it while the answer is written, and the caller then sends /v1/answer with topic_choice new or
    continue, so the decision is made once.
    GET /v1/health -> 200 {"ok": true, "model": "...", "files": n, "knowledge_commit": "..."}

The facts are context for the question, not instructions: they are put below the question under a fixed heading.
The service holds no state and stores nothing. Run: python3 harness/answer_service.py [--config harness/service_config.yaml]
"""
import argparse
import json
import os
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import answer_modes  # noqa: E402
import arithmetic_calculator  # noqa: E402
import answer_shape  # noqa: E402
import catalog_database  # noqa: E402
import expert_agent  # noqa: E402
import knowledge_loader  # noqa: E402
import topic_decision  # noqa: E402
import user_suggestions  # noqa: E402
from knowledge_search import Retriever  # noqa: E402
from model_client import GatewayClient, LLMError, MockClient, ParamClient  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROLES = {'l1': 'a Level 1 NOC operator who follows the SOP', 'l2': 'a Level 2 platform engineer',
         'capacity': 'a capacity planner', 'executive': 'the CIO'}
# The heading lives with stage 3, which reads the series below it (expert_agent.kpi_trends).
FACTS_HEADING = expert_agent.FACTS_HEADING
# The person typed a question on a PCM screen: they see the screen, never the data PCM sent (PCM D-101).
SCREEN_RULES = (
    expert_agent.RULES_HEADING + '\n'
    '- They typed only the question. They see the PCM page named under "screen", not the data below. Speak of what they '
    'see: the chart, the tab, the page, an object by its name. Never mention JSON, the facts, a payload or the data '
    'provided.\n'
    '- When an opening is given below, the person reads it first, as the start of your answer, in the same voice. Continue '
    'from it: never repeat a figure, the time or the verdict it gives (the computed line on how the score moved across the '
    'window holds the same figures), and never say a number is "computed".\n'
    '- Answer the question asked, in the first sentence; when it asks several things, answer them in the order asked. Never '
    'open by restating the opening\'s verdict (that the score fell or that the drop is real): the person has just read it. '
    'When it asks why a score moved, what is wrong or what to check, do not '
    'open with the drop or the level: open with the cause, which part pulled the score down, then where to look next. When it '
    'asks how a metric works, what it measures or why it is designed so, explain the mechanism from the knowledge base first; '
    'the page\'s figures come after, as a short example, or not at all.\n'
    '- If the opening says the score stayed within its normal movement, do not restate the range: say what the score measures and '
    'why this movement is normal.\n'
    '- Other computed lines are exact: give their figures as written when the answer needs them (for example a sub-metric\'s '
    'own value). For a question on why a score moved or what is wrong: if a computed line names the sub-metric that moved a '
    'score most, lead with that sub-metric, its value and what the value means for the VMs (what they waited for and how '
    'much, in the sub-metric\'s own unit), then the next step for that resource. Give every sub-metric the band the computed '
    'line gives it: an orange or red one is never low.\n'
    '- A colour (green, yellow, orange, red) is the label the limits give a value. It explains nothing: never write that a '
    'value is a problem, or fine, because of its colour. The colour may follow a value as its label.\n'
    '- When the question asks whether a value is a problem (bad, fine, normal, acceptable), answer yes or no in the first '
    'sentence, then the reason in this order: against what the object does normally (the window median) and where green '
    'ends; what the VMs waited for, per sub-metric, in its own unit; how broad (the depth and breadth line: not '
    'cluster-wide, under 10% of the VMs, or broad; one host); how long (the time line). Then the next step. The screen names the value 95% of the '
    'window was better than the 5th percentile on a score where higher is better and the 95th where higher is worse: use '
    'its name. The score proves that VMs waited; whether an application suffered is read in its Guest OS and in the '
    'application.\n'
    '- With no opening, answer directly first, with the figures.\n'
    '- If "screen" names where to look next (drill_down), point there first, by page and tab, before any knowledge-base flow.\n'
    '- If a value the answer needs is not in the data, name the PCM page that shows it, or say PCM does not show it yet.\n'
    '- Name a score by its name as the page shows it (Cluster Performance (%), Cluster Risk (%), VM Performance (%)), never '
    '"the KPI": the word is stretched across the industry; the name is exact. Name contention, consumption or risk by the '
    'metric and its limit, never by an adjective such as "high" alone.\n'
    '- Never write a knowledge base file id or path (such as vsphere/technology/...). Name a flow or a metric by its title in words; '
    'PCM lists the files read under Sources.')
METRIC_FACTS = ('screen', 'object', 'pillar', 'window')  # what a metric question keeps of the page
OPENING = ('The opening of your answer, already written; the person reads it first: "{lead}" Write what follows it. Do not '
           'repeat it.')
# Words that show the pipeline instead of the screen; an answer that uses one gets one rewrite.
PIPELINE_WORDS = re.compile(r'\bJSON\b|\bpayload\b|\b(?:provided|given|supplied|attached) (?:data|facts|readings)\b'
                            r'|\b(?:data|facts|readings) (?:provided|given|supplied|sent)\b|\bthe facts\b', re.I)
REWRITE = ('Rewrite this answer for a person who sees the PCM screen and typed only the question. Remove these words: '
           '{words}. Say the chart, this page or PCM instead. Keep every fact, number, name and the order. Reply with the '
           'answer only.\n\n{text}')
REWRITE_FIGURES = ('Rewrite this answer. The person already reads these figures above it: {figures}. Remove them, the time of the '
                   'worst point, and any sentence that only restates the verdict or the rule for a drop (such as "a move of 5 '
                   'points or more counts"). Keep the order of the answer and what it answers first. Keep every other fact, '
                   'name and number. Do not say computed, calculator, the box above or the model. Reply with the answer '
                   'only.\n\n{text}')
# A colour given as the reason a value is a problem or fine ("a problem because it is orange"): circular, since the limits
# set the colour from the value. An answer that does it gets one rewrite (performance-kpi-design, section Is a value a problem).
COLOUR = r'(?:green|yellow|orange|red)'
COLOUR_REASON = re.compile(
    rf'\b(?:because|since)\b[^.;:\n]{{0,60}}?\b(?:is|was|are|were|sits|stays|reads|turned|falls|fell|lies)\s+(?:now\s+|still\s+)?'
    rf'(?:in\s+|into\s+|within\s+)?(?:the\s+)?{COLOUR}\b'
    rf'|\b(?:is|was|are|were)\s+(?:in\s+(?:the\s+)?)?{COLOUR}(?:\s+(?:band|range|zone))?,?\s+(?:so|which means|meaning)\b'
    rf'|\b{COLOUR}\s+(?:band|range|zone)?\s*(?:means|indicates|shows)\s+(?:it\s+is\s+|there\s+is\s+)?(?:a\s+)?'
    rf'(?:problem|issue|concern|fine|healthy|bad|ok)\b', re.I)
REWRITE_COLOUR = ('Rewrite this answer. It gives a colour as the reason a value is a problem or fine: "{hits}". A colour is only '
                  'the label the limits give a value, so it explains nothing. Replace each such reason with what the value '
                  'means for the VMs: what they waited for and how much (in the metric\'s own unit), how many VMs, and for '
                  'how long, using only facts already in the answer. The colour may stay as a label after a value. Keep every '
                  'other fact, number, name and the order. Reply with the answer only.\n\n{text}')
# A figure the question names ("Is 48% a problem?"): the opening first says what that figure is on the card.
ASKED_FIGURE = re.compile(r'(?<![\d.])(\d+(?:\.\d+)?)\s*%')
# The stage 3 line on how a KPI moved across the window (expert_agent.kpi_trends): the opening's figures, exact.
TREND_LINE = re.compile(r'across the window \(\d+ points\)')
# A computed line that lists the sub-metrics holds figures the answer may use (a part's own value).
PART_LINE = re.compile(r'sub-metrics', re.I)
MONTHS = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
ISO_TIME = re.compile(r'\b(\d{4})-(\d\d)-(\d\d)[T ](\d\d):(\d\d)(?::\d\d(?:\.\d+)?)?(?:Z|[+-]\d\d:?\d\d)?')
# A knowledge path: a top folder of knowledge/ and one or more parts, optional knowledge/ prefix and .md suffix; not inside a URL.
KB_PATH = r'(?<![\w/.:-])(?:knowledge/)?(?:{tops})(?:/[\w.-]*\w)+?(?:\.md)?(?![\w/-])'
# Wrappers a model puts around a path: `x`, **x**, [x], [x, y], (x), (see `x`) and harness notes [file.py: ...].
HARNESS_NOTE = re.compile(r'[ \t]*\[[\w-]+\.(?:py|js|ya?ml|json)\b[^\[\]\n]*\]')
# A question on whether the cluster can take more VMs (or is open or closed): the close-for-business opening answers it.
TAKES_VMS = re.compile(r'\b(?:more|new|extra|another|additional|add|fit|room|headroom|upsiz\w*|open|clos\w*)\b.*\bVMs?\b'
                       r'|\bVMs?\b.*\b(?:more|fit|take|accept|add|upsiz\w*|open|clos\w*)\b|close for business', re.I)
PERCENTILE_WORDS = re.compile(r'\b(?:95th|5th) percentile\b|\b95% of the window\b|\bworst 5%', re.I)
FIGURE = re.compile(r'(?<![\d.])\d+(?:\.\d+)?(?![\d.]*\d)')


def screen_time(text):
    """ISO times in the screen's format ("2026-10-19T08:30:00+08:00" -> "19 Oct, 08:30"); the values stay exact."""
    return ISO_TIME.sub(lambda m: f'{int(m.group(3))} {MONTHS[int(m.group(2)) - 1]}, {m.group(4)}:{m.group(5)}', text)


def headline_figures(computed):
    """Figures of the computed lines the person reads: decimals and numbers of 10 or more (a count of 1 to 9 is too common a
    word to flag), outside times and outside the lines that list sub-metrics."""
    out = set()
    for line in computed:
        if PART_LINE.search(line):
            continue
        line = PERCENTILE_WORDS.sub(' ', line)  # "95th percentile", "95% of the window": the name of a figure, not one
        for f in FIGURE.findall(ISO_TIME.sub(' ', re.sub(r'\b\d{1,2} [A-Z][a-z]{2}, \d\d:\d\d', ' ', line))):
            if '.' in f or float(f) >= 10:
                out.add(f)
    return out


def repeated_figures(text, figures):
    """The figures found in the text, also written with trailing zeros ("17" as "17.0")."""
    return sorted(f for f in figures if re.search(r'(?<![\d.])' + re.escape(f) + r'(?:\.0+)?(?![\d]|\.\d)', text or ''))


def _fig(x, level=None):
    """A KPI figure as the person reads it on the chart: whole (PCM D-116). One decimal more only where rounding would put a
    move on the other side of the KPI change level (7.6 is under 8; "8" would not be)."""
    for places in (0, 1, 2):
        v = round(x, places)
        if level is None or (v >= level) == (x >= level):
            break
    return f'{v:g}'


def window_words(facts):
    w = facts.get('window') if isinstance(facts, dict) else None
    if isinstance(w, str) and w.strip():
        w = w.strip()
        return f'in the {w[0].lower() + w[1:]}' if w.lower().startswith('last ') else f'in the window ({w})'
    return 'in the window'


def lead_text(rows, facts=None):
    """The opening the person reads first: how each KPI moved, in plain words, from the calculator's numbers
    (expert_agent.kpi_trend_rows). Code writes it, so every figure is exact; the model's text continues from it.
    Whole figures, the screen's time, no internal words (points count, verdict, change level)."""
    out, when_in = [], window_words(facts)
    for r in rows:
        t, lv, u, n = r['trend'], r['level'], '%' if r['unit'] == '%' else '', r['name']
        up = r['better'] == 'lower'  # higher is worse: the worst point is a rise
        at = f" at {screen_time(str(r['when']))}" if r['when'] else ''
        med, worst = _fig(t['median']), _fig(t['worst'])
        if lv is None:
            out.append(f"{n} {when_in}: median {med}{u}, lowest {_fig(t['low'])}{u}, highest {_fig(t['high'])}{u}. "
                       f"No change level is set for {n}, so no move is called a drop here.")
        elif t['verdict'] == 'worsened':
            out.append(f"{n} {'rose' if up else 'fell'} to {worst}{u}{at}, {_fig(t['worse_move'], lv)} points "
                       f"{'above' if up else 'below'} its median of {med}{u} {when_in}. That is a real "
                       f"{'rise' if up else 'drop'}, not normal movement: a move of {lv:g} points or more counts.")
        elif t['verdict'] == 'improved':
            best = t['low'] if up else t['high']
            out.append(f"{n} improved {when_in}: {'lowest' if up else 'highest'} {_fig(best)}{u}, "
                       f"{_fig(t['better_move'], lv)} points {'below' if up else 'above'} its median of {med}{u}. "
                       f"No {'rise' if up else 'drop'}: its worst point, {worst}{u}, is within its normal movement.")
        else:
            out.append(f"{n} stayed within its normal movement {when_in}: median {med}{u}, "
                       f"{'highest' if up else 'lowest'} {worst}{u}{at}, {_fig(t['worse_move'], lv)} points from the median. "
                       f"No {'rise' if up else 'drop'}: a move counts from {lv:g} points.")
    return out[0] if len(out) == 1 else '\n'.join(f'- {x}' for x in out)  # several KPIs: one bullet each


def figure_text(question, facts, cat):
    """The opening's first sentence when the question names a figure of the KPI card asked about ("Is 48% a problem?"):
    which figure it is and what it means, so the answer starts from the number the person asked about. The screen's 95th
    percentile of a score where higher is better is near the worst end of the window, not the top: say so in words.
    Empty when no number in the question is a figure of the card."""
    k = facts.get('asked_about_kpi') if isinstance(facts, dict) else None
    name = (k.get('label') or k.get('name')) if isinstance(k, dict) else None
    if not name:
        return ''
    w = k.get('worst')
    figures = [('percentile_95', k.get('percentile_95')), ('now', k.get('now')),
               ('worst', w.get('v') if isinstance(w, dict) else w)]
    s = (expert_agent._series(k, [], limit=1) or [None])[0]
    if s:
        try:
            figures.append(('median', arithmetic_calculator.trend(s['values'], s['better'])['median']))
        except arithmetic_calculator.CalcError:
            pass
    sl = cat.score_line(name)
    worse_up = bool(sl and sl['direction'] == 'above') or k.get('better') == 'lower'
    when_in = window_words(facts)
    for q in ASKED_FIGURE.findall(question or ''):
        q = float(q)
        for key, v in figures:
            if not isinstance(v, (int, float)) or isinstance(v, bool) or abs(v - q) >= (0.5 if q.is_integer() else 0.05):
                continue
            f = _fig(v)
            if key == 'percentile_95':
                return (f"{f}% is the {expert_agent.percentile_name(worse_up)} of {name} {when_in}: "
                        f"{expert_agent.percentile_words(float(f), '%', worse_up, k)}.")
            if key == 'now':
                return f"{f}% is the latest value of {name} on the chart."
            if key == 'worst':
                return f"{f}% is the worst point of {name} {when_in}."
            return f"{f}% is the median of {name} {when_in}: its normal level."
    return ''


def colour_reasons(text):
    return [m.group(0) for m in COLOUR_REASON.finditer(text or '')]


def capacity_text(r):
    """The opening on a cluster's Capacity tab, in the order of close for business: Consumption, then contention, which
    overrides, then Risk, which decides only when both are orange. Metrics and limits, no adjective (author, 2026-11-24).
    Markdown, one bullet per check with a bold label, then the decision on its own line: the person scans it, and the
    model's text below it is formatted the same way."""
    if not r:
        return ''
    L, f = r['limits'], _fig
    c = r['consumption']
    if r['c_level'] == 'red':
        t = (f"{f(c)}% (95th percentile, last 24 hours), above the close-for-business limit of "
             f"{f(L['closure-cluster-consumption-red'])}%.")
    elif r['c_level'] == 'orange':
        t = (f"{f(c)}% (95th percentile, last 24 hours), above {f(L['closure-cluster-consumption-orange'])}% "
             f"and not above {f(L['closure-cluster-consumption-red'])}%: orange.")
    else:
        t = (f"{f(c)}% (95th percentile, last 24 hours), not above {f(L['closure-cluster-consumption-orange'])}%: "
             f"the cluster is about {f(c)}% full.")
    bullets = [('Consumption', t)]
    p = r['performance']
    if isinstance(p, (int, float)):
        if r['p_level'] == 'red':
            t = (f"Cluster Performance (%) {f(p)}% (5th percentile), below {f(L['closure-cluster-performance-red'])}%: "
                 'it overrides: closed until the contention is fixed.')
        elif r['p_level'] == 'orange':
            t = (f"Cluster Performance (%) {f(p)}% (5th percentile), below {f(L['closure-cluster-performance-orange'])}% "
                 f"and not below {f(L['closure-cluster-performance-red'])}%: orange, no override.")
        else:
            t = (f"Cluster Performance (%) {f(p)}% (5th percentile), not below "
                 f"{f(L['closure-cluster-performance-orange'])}%: no override.")
        bullets.append(('Contention', t))
    k = r['risk']
    if isinstance(k, (int, float)):
        if r['both_orange']:
            t = (f"Cluster Risk (%) {f(k)}% (95th percentile), {'above' if k > r['risk_limit'] else 'not above'} the "
                 f"production limit of {f(r['risk_limit'])}%: it decides, as Consumption and Cluster Performance (%) are "
                 'both orange. Every cluster gets the production limit, as the environment of a cluster is not known; '
                 f"a non-production cluster's own limit is {f(L['closure-cluster-risk-nonprod'])}%.")
        else:
            t = (f"Cluster Risk (%) {f(k)}% (95th percentile) does not decide: Consumption and Cluster Performance (%) "
                 'are not both orange.')
        bullets.append(('Risk', t))
    verdict = 'Closed for new VMs and VM upsizes.' if r['closed'] else 'Open for new VMs.'
    return '\n'.join(f'- **{label}:** {text}' for label, text in bullets) + f'\n\n**{verdict}**'


def step_text(r):
    """One sentence on when the KPI asked about changed level, and whether the other KPIs followed (expert_agent.kpi_step_row).
    Its worst point can come hours later; a question about a change of colour is about this moment."""
    if not r:
        return ''
    s, st = r['series'], r['step']
    when = screen_time(str(r['when'])) if r['when'] else 'in the window'
    out = (f" {s['name']} changed level at {when}: from {_fig(st['before'])}% the hour before to {_fig(st['after'])}% the hour "
           f"after.")
    for name, mb, ma, moved, lv in r['others']:
        out += (f" {name} moved too, from {_fig(mb)}% to {_fig(ma)}%." if moved else
                f" {name} held: {_fig(mb)}% the hour before, {_fig(ma)}% the hour after.")
    return out


def no_file_refs(text, docs):
    """Knowledge file ids out of the text the person reads; PCM lists the files under Sources. A citation, a path alone in
    brackets or parentheses (a list of paths too), goes; a path the sentence needs ("use `x`") becomes the file's title.
    A path that is no knowledge file goes too. Works on every answer, whatever the model was told (expert_agent asks it
    to name ids, for the benchmark's check)."""
    if not text:
        return text
    tops = sorted({i.split('/')[0] for i in docs if '/' in i}) or ['vsphere']
    path = KB_PATH.format(tops='|'.join(map(re.escape, tops)))
    one = rf'(?:see |source: |sources: )?(?:\*\*)?`?{path}`?(?:\*\*)?'
    many = rf'{one}(?:\s*(?:[,;]|and)\s*{one})*'
    text = HARNESS_NOTE.sub('', text)
    text = re.sub(rf'[ \t]*[(\[]\s*{many}\s*[)\]]', '', text, flags=re.I)

    def title(m):
        key = re.sub(r'^knowledge/|\.md$', '', m.group('p'))
        d = docs.get(key)
        if d is not None and getattr(d, 'title', None):
            return d.title
        return key.rsplit('/', 1)[-1].replace('-', ' ').replace('_', ' ')  # no such file: its last part, in words
    text = re.sub(rf'(?:\*\*)?`?(?P<p>{path})`?(?:\*\*)?', title, text)
    # What a removal leaves: a space before punctuation, a dangling comma, double spaces.
    text = re.sub(r'[ \t]+([.,;:!?])', r'\1', text)
    text = re.sub(r'\s*(?:,\s*)+([.;])', r'\1', text)
    text = re.sub(r'([^\S\n])[^\S\n]+', r'\1', text)
    return text


def question_text(body, lead=''):
    """The question as Agent E2's pipeline reads it: the caller's question, who asks, how to speak to them, the opening
    the person reads first (lead_text), then the facts."""
    q = (body.get('question') or '').strip()
    if not q:
        raise ValueError('question is required')
    role = ROLES.get(body.get('role') or '')
    if role:
        q += f'\n\nThe person asking is {role}.'
    facts = body.get('facts')
    if facts:
        q += '\n\n' + SCREEN_RULES
        if lead:
            q += '\n\n' + OPENING.format(lead=lead)
        q += '\n\n' + FACTS_HEADING + '\n' + json.dumps(facts, indent=1, ensure_ascii=False, default=str)
    return q


def concept_facts(facts):
    """What a question on what a metric is or how it works keeps of the page: the page named, no figures, no drill-down."""
    out = {k: v for k, v in facts.items() if k in METRIC_FACTS}
    if isinstance(out.get('screen'), dict):
        out['screen'] = {k: v for k, v in out['screen'].items() if k != 'drill_down'}
    return out


def conversation(history):
    """The earlier turns the caller sent, checked: a list of {question, answer} strings, oldest first. Every turn is kept."""
    if history is None:
        return []
    if not isinstance(history, list) or not all(isinstance(t, dict) and isinstance(t.get('question'), str)
                                                and isinstance(t.get('answer'), str) for t in history):
        raise ValueError('history must be a list of {"question": "...", "answer": "..."}')
    return [{'question': t['question'].strip(), 'answer': t['answer'].strip()} for t in history if t['question'].strip()]


def pipeline_words(text):
    return sorted({m.group(0).lower() for m in PIPELINE_WORDS.finditer(text or '')})


class Service:
    def __init__(self, cfg, client=None, retriever=None):
        self.cfg = cfg
        self.model = cfg['model']
        if client is None:
            params = {self.model: (cfg.get('model_params') or {}).get(self.model, {})}
            sampling = {self.model: (cfg.get('sampling') or {}).get(self.model, {'temperature': cfg.get('temperature')})}
            client = ParamClient(GatewayClient(cfg['gateway'], retry_seconds=cfg.get('gateway_retry_minutes', 1) * 60),
                                 params, sampling)
        self.client = client
        self.docs, chunks = knowledge_loader.load()
        if retriever is None:
            try:
                retriever = Retriever(self.docs, chunks, client if cfg.get('embedding_model') else None,
                                      cfg.get('embedding_model'), expand=cfg.get('query_expansion', False))
            except LLMError:
                retriever = Retriever(self.docs, chunks, expand=cfg.get('query_expansion', False))
        self.retriever = retriever
        self.commit = knowledge_loader.git_sha()
        self.cat = catalog_database.get(self.docs)
        self.suggestions = user_suggestions.table()

    def lead(self, facts, question=''):
        if not facts:
            return ''
        cap = capacity_text(expert_agent.capacity_check_row(facts, self.cat)) if TAKES_VMS.search(question or '') else ''
        if cap:
            return cap  # a cluster's Capacity page or card: the close-for-business reading, in its order
        rows = expert_agent.kpi_trend_rows(facts, self.cat)
        if isinstance(facts, dict) and facts.get('asked_about_kpi'):
            rows = rows[:1]  # a question on one KPI card: the opening is about that KPI; the others are context
        fig = figure_text(question, facts, self.cat)  # the figure the person asked about comes first
        trend = (lead_text(rows, facts) + step_text(expert_agent.kpi_step_row(facts, self.cat))).strip()
        if not fig:
            return trend
        return f'{fig}\n{trend}' if trend.startswith('- ') else f'{fig} {trend}'.strip()  # several KPIs: their bullets below

    def suggest(self, body):
        if body.get('card'):  # one card's showcase question (user_suggestions.card)
            return user_suggestions.card(body.get('facts'), body['card'], self.cat, self.suggestions)
        return user_suggestions.suggest(body.get('facts'), self.cat, self.suggestions, screen_time)

    def topic(self, body):
        """Whether the question continues the topic of `history`, decided alone, so the caller can show the decision
        before the answer and the person can change it while the answer is written. The caller then sends the answer
        request with topic_choice new or continue."""
        history = conversation(body.get('history'))
        first = ((body.get('turns') or [None])[0] or body.get('question') or '').strip()  # a clarifying reply: its question
        return topic_decision.decide(self.client, self.model, first, history, body.get('topic_choice'), self.docs, self.cfg,
                                     (self.cfg.get('provider_order') or {}).get(self.model))

    def answer(self, body):
        history = conversation(body.get('history'))
        first = ((body.get('turns') or [None])[0] or body.get('question') or '').strip()  # a clarifying reply: its question
        topic = self.topic(body)
        history = history if topic['continues'] else []
        # What the question asks (answer_shape.decide), read by the model on the bare question: the facts and rules added
        # to it below hold words such as "cause" and "next". A reply in a clarifying round takes its question's reading; a
        # turn that continues a topic is read with the topic's earlier questions.
        asks = answer_shape.decide(self.client, self.model, first, [t['question'] for t in history], self.cfg,
                                   (self.cfg.get('provider_order') or {}).get(self.model))
        shape = asks['shape']
        # A question on how a score works in general is answered from the knowledge base, with the page named but not its
        # numbers or where to look next. With the numbers, the model opened with what pulled the score down.
        if not asks['page_values'] and isinstance(body.get('facts'), dict):
            body = {**body, 'facts': concept_facts(body['facts'])}
            lead = ''
        elif history:
            lead = ''  # the opening reads the page once, at the start of a topic; a turn that continues it does not repeat it
        else:
            lead = self.lead(body.get('facts'), body.get('question'))
        turns = body.get('turns')
        if turns:
            turns = [question_text({**body, 'question': turns[0]}, lead)] + list(turns[1:])
        else:
            turns = [question_text(body, lead)]
        out = answer_modes.converse('agent-e2', self.client, self.model, turns, [], self.cfg, self.retriever, history, shape)
        computed = [line for s in out['trace'] if s.get('action') == 'compute' for line in (s.get('output') or [])]
        content = no_file_refs(out['result'].get('content'), self.docs)
        if out['type'] == 'answer':
            content = self.no_colour_reason(content)
        if body.get('facts') and out['type'] == 'answer':
            content = self.screen_wording(content)
            # The figures the person reads in the opening, and the same figures, exact, in the trend line.
            content = self.no_repeat(content, [lead] + [_shown(c) for c in computed if TREND_LINE.search(c)])
            content = no_file_refs(content, self.docs)  # a rewrite may bring a path back
        return {'type': out['type'], 'content': content, 'questions': out.get('questions', []),
                'files_read': out['used'], 'lead': lead if out['type'] == 'answer' else '',
                'computed': [_shown(c) for c in computed], 'topic': topic, 'shape': out['result'].get('shape'),
                'page_values': asks['page_values'],
                'model': self.model,
                'knowledge_commit': self.commit}

    def no_repeat(self, text, shown):
        """One rewrite when the text repeats a figure of the opening above it. No opening: nothing to repeat."""
        shown = [x for x in shown if x]
        dup = repeated_figures(text, headline_figures(shown))
        if not dup:
            return text
        res = self.client.chat(self.model, [{'role': 'user', 'content': REWRITE_FIGURES.format(figures=', '.join(dup), text=text)}],
                               temperature=self.cfg.get('temperature'), max_tokens=self.cfg.get('max_tokens', 2000))
        again = (res.get('content') or '').strip()
        return again if again and not pipeline_words(again) and len(repeated_figures(again, set(dup))) < len(dup) else text

    def no_colour_reason(self, text):
        """One rewrite when the answer gives a colour as the reason a value is a problem or fine. The rewrite is kept only
        when it has no such reason left and no pipeline words."""
        hits = colour_reasons(text)
        if not hits:
            return text
        res = self.client.chat(self.model, [{'role': 'user', 'content': REWRITE_COLOUR.format(hits='"; "'.join(hits), text=text)}],
                               temperature=self.cfg.get('temperature'), max_tokens=self.cfg.get('max_tokens', 2000))
        again = (res.get('content') or '').strip()
        return again if again and not colour_reasons(again) and not pipeline_words(again) else text

    def screen_wording(self, text):
        """One rewrite when the answer speaks of the data instead of the screen ("the provided JSON")."""
        bad = pipeline_words(text)
        if not bad:
            return text
        res = self.client.chat(self.model, [{'role': 'user', 'content': REWRITE.format(words=', '.join(bad), text=text)}],
                               temperature=self.cfg.get('temperature'), max_tokens=self.cfg.get('max_tokens', 2000))
        again = (res.get('content') or '').strip()
        return again if again and not pipeline_words(again) else text


def _shown(line):
    """A computed line as the person reads it: without the instruction to the model and the calculator's note."""
    line = re.sub(r'\s*\[arithmetic_calculator\.py:.*\]\s*$', '', line)
    line = re.sub(r'\s*(?:Say this first\.|give the range and do not call a move a drop\.)\s*$', '', line).lstrip('- ').strip()
    return screen_time(line)


def handler_for(service):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def send(self, code, data):
            body = json.dumps(data, ensure_ascii=False, default=str).encode()
            self.send_response(code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path == '/v1/health':
                return self.send(200, {'ok': True, 'model': service.model, 'files': len(service.docs),
                                       'knowledge_commit': service.commit})
            return self.send(404, {'error': 'not found'})

        def do_POST(self):
            route = {'/v1/answer': service.answer, '/v1/suggest': service.suggest, '/v1/topic': service.topic}.get(self.path)
            if not route:
                return self.send(404, {'error': 'not found'})
            try:
                body = json.loads(self.rfile.read(int(self.headers.get('Content-Length') or 0)) or b'{}')
                return self.send(200, route(body))
            except ValueError as e:
                return self.send(400, {'error': str(e)})
            except LLMError as e:
                return self.send(502, {'error': f'model unavailable: {e}'})
    return Handler


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--config', default=os.path.join(HERE, 'service_config.yaml'))
    ap.add_argument('--host', default='127.0.0.1')
    ap.add_argument('--port', type=int, default=8090)
    ap.add_argument('--mock', action='store_true', help='offline MockClient, BM25 only (tests and demos without a model)')
    a = ap.parse_args()
    cfg = yaml.safe_load(open(a.config))
    if a.mock:
        cfg = {**cfg, 'embedding_model': None}
    service = Service(cfg, MockClient() if a.mock else None)
    print(f'Agent E2 service on http://{a.host}:{a.port}/v1/answer, model {service.model}, {len(service.docs)} files')
    ThreadingHTTPServer((a.host, a.port), handler_for(service)).serve_forever()


if __name__ == '__main__':
    main()
