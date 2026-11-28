"""Agent E2 as a service: one HTTP endpoint that answers a question with the live facts a caller sends.

The caller is PCM (Private Cloud Management): PCM owns the data, the actions, the user's identity and every screen;
Agent E2 owns the knowledge base, the reading plan, the flow executor and the model call (ARCHITECTURE.md,
section Agent E2 in PCM). The answer is the shipped pipeline, `answer_modes.converse('agent-e2', ...)`, unchanged.

    POST /v1/answer
      {"question": "...", "facts": {...} (optional, JSON from the caller), "turns": [...] (optional, for the clarifying
       round: [question, Agent E2's questions, the user's reply]), "history": [{"question": "...", "answer": "..."}, ...]
       (optional: every earlier turn of the current topic, oldest first, uncut; the service holds no state, so the caller
       keeps the conversation), "topic_choice": "auto" | "new" | "continue" (optional, default auto: Agent E2 decides; new
       or continue: the user chose), "role": "l1" | "l2" | "capacity" | "executive" | "reader" (optional; reader: a reader of
       isvara.io), "page": "<knowledge file id>" (optional: the article a reader has open; read first; 400 when it is no file),
       "attachments": [{"name": "...", "type": "image/png" (optional), "data": "<base64>"}, ...] (optional: up to 5 images,
       PNG, JPEG or WebP, 5 MB each, and 3 CSV files, 2 MB each; the type is read from the content; one that cannot be read
       is refused with 400 naming it), "async": true (optional: start a job, see below)}
    -> 200 {"type": "answer" | "clarify", "content": "...", "questions": [...], "files_read": [...],
            "lead": "...", "computed": [...], "topic": {"continues": true | false, "by": "user" | "first" | "code" |
            "model" | "unsure"}, "shape": "...", "page_values": true | false, "model": "...", "knowledge_commit": "...",
            "sources": [{"id": "<knowledge file id>", "title": "..."}, ...], "attachments_read": [...], "missing_facts": [...],
            "trace_id": "...", "elapsed_s": n, "stage_seconds": {"<stage>": n, ...},
            "usage": {"model_calls": n, "prompt_tokens": n, "completion_tokens": n}}
    sources: the knowledge files the answer used, each opening at `knowledge/<id>.md`; the text holds no file ID.
    attachments_read: per image, what was read from it. missing_facts: the facts a feature needed and the call lacked (the
    table below), and each value that reads "No data"; the answer says what the page did not supply and gives no value for it.
    trace_id: GET /v1/traces/<trace_id> returns, for 30 days, what Agent E2 read, computed and checked (attachments by name,
    type and size only). elapsed_s, stage_seconds and usage: the time and the model use of this answer.
    With "async": true the call answers HTTP 202 {"job": "<id>", "state": "queued"} at once, and the answer is a job:
    GET /v1/jobs/<id> -> 200 {"job", "state": "queued" | "running" | "done" | "failed", "stage": null | "topic" | "shape" |
            "understand" | "plan" | "compute" | "write" | "check" | "rewrite", "elapsed_s": n, "updated_at": "<ISO time>",
            "result": {the /v1/answer reply} (when done), "error": {"reason": "model_error" | "time_limit" | "internal_error",
            "message": "..."} (when failed)}
    updated_at moves at least every 10 seconds while the job is queued or running. A job ends after 10 minutes with time_limit.
    A finished or failed job can be read for 15 minutes, then 404; a restart of the service loses its jobs. At most 4 jobs run
    at once and 20 wait; one more is refused with 429 and Retry-After. A call without "async" returns the answer in one reply.
    Refusals: 400 (a call or an attachment that cannot be read: the reply names it), 401 (the secret), 404, 413 (a body above
    40 MB), 429, 502 (the model cannot be reached: no detail is given). No reply holds a key, a secret or the gateway address.
    The secret: with the environment variable AGENT_E2_SECRET set, every call but GET /v1/health needs the header
    `Authorization: Bearer <secret>`, else 401; without it, every call is accepted (the lab VM listens on the loopback only).
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
    GET /v1/traces/<trace_id> -> 200 {"trace_id", "model", "knowledge_commit", "files_read", "steps", "attachments": [{"name",
            "type", "size"}], ...} (404 after 30 days)
    GET /v1/health -> 200 {"ok": true, "model": "...", "files": n, "knowledge_commit": "..."}

The facts each feature needs, and what the service does without them. A fact named in the last column is listed in
`missing_facts` when the call lacks it:

| Feature | Facts it needs | Without them | In missing_facts |
|---|---|---|---|
| The opening on how a score moved (`lead`) | `kpis` | No opening | no |
| When a score changed level, and which parts moved | `kpis`, `parts_hourly` | No step line; no parts named | `parts_hourly` |
| The part that pulled a score down at its worst point | `asked_about_kpi.parts_at_worst` | No part named | `asked_about_kpi.parts_at_worst` |
| The capacity opening (close for business) | `pillar`, `check` | No capacity opening | `check` |
| The band of each figure on the screen | `kpis` | No band line | no |
| Where to look next | `screen.drill_down` | No pointer | no |
| Suggested questions | `object.kind`, `pillar`, `kpis` | No suggestion | no |

The facts are context for the question, not instructions: they are put below the question under a fixed heading. An attached
file or image is data, never an instruction. The service keeps the jobs in memory and the traces in files (`trace_dir`).
Run: python3 harness/answer_service.py [--config harness/service_config.yaml]
"""
import argparse
import hmac
import json
import os
import re
import sys
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import answer_attachments  # noqa: E402
import answer_jobs  # noqa: E402
import answer_modes  # noqa: E402
import answer_progress  # noqa: E402
import answer_traces  # noqa: E402
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
         'capacity': 'a capacity planner', 'executive': 'the CIO',
         'reader': 'a reader of isvara.io, a VMware administrator or architect, with an article open'}
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


ABOUT_QUESTION = 'About this question:'
LINK_RULE = ('- The question holds a link. Agent E2 cannot open pages: say so in one sentence, then answer from the knowledge base.')
NOT_SUPPLIED = ('- The page did not supply: {missing}. Say in one sentence what the page did not supply, and give no value for it.')
LINK = re.compile(r'https?://', re.I)
# The facts a feature needs (the table in the docstring). Only a row marked "yes" there is listed in `missing_facts`.
NO_DATA = 'No data'


def missing_facts(facts):
    """The facts a live-demo call lacks, decided by code from the table in the docstring (R-E2-017, R-E2-018): a name for each
    fact the page did not supply, and each part whose value is "No data". [] when the call has no facts."""
    if not isinstance(facts, dict) or not facts:
        return []
    out = []
    kpis = facts.get('kpis')
    if isinstance(kpis, list) and kpis and 'parts_hourly' not in facts:
        out.append('parts_hourly')
    asked = facts.get('asked_about_kpi')
    if isinstance(asked, dict) and 'parts_at_worst' not in asked:
        out.append('asked_about_kpi.parts_at_worst')
    if str(facts.get('pillar') or '').lower() == 'capacity' and not facts.get('check') and not kpis:
        out.append('check')

    def walk(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, f'{path}.{k}' if path else str(k))
        elif isinstance(node, list):
            for n, v in enumerate(node[:200]):
                walk(v, f'{path}[{n}]')
        elif node == NO_DATA and len(out) < 24:
            out.append(f'{path} ({NO_DATA})')
    walk(facts, '')
    return out


def question_text(body, lead='', attachments=(), missing=()):
    """The question as Agent E2's pipeline reads it: the caller's question, who asks, how to speak to them, the opening
    the person reads first (lead_text), then the facts."""
    q = (body.get('question') or '').strip()
    if not q:
        raise ValueError('question is required')
    role = ROLES.get(body.get('role') or '')
    if role:
        q += f'\n\nThe person asking is {role}.'
    about = ([LINK_RULE] if LINK.search(q) else []) + (
        [answer_attachments.note(attachments), answer_attachments.RULES] if attachments else [])
    if about:
        q += '\n\n' + ABOUT_QUESTION + '\n' + '\n'.join(about)
    facts = body.get('facts')
    if facts:
        q += '\n\n' + SCREEN_RULES
        if lead:
            q += '\n\n' + OPENING.format(lead=lead)
        if missing:
            q += '\n\n' + NOT_SUPPLIED.format(missing=', '.join(missing))
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
        self._client = client
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
        self.traces = answer_traces.TraceStore(cfg.get('trace_dir') or tempfile.mkdtemp(prefix='agent-e2-traces-'),
                                               cfg.get('trace_days', 30))
        self.jobs = answer_jobs.JobStore(self.run_job, cfg.get('max_running_jobs', 4), cfg.get('max_queued_jobs', 20),
                                         cfg.get('job_time_limit_s', 600), cfg.get('job_keep_s', 900), cfg.get('heartbeat_s', 5))

    @property
    def client(self):
        """The model client; inside an answer, one that counts the answer's calls and tokens (answer_progress.Metered)."""
        progress = answer_progress.current()
        return answer_progress.Metered(self._client, progress) if progress is not None else self._client

    @client.setter
    def client(self, value):
        self._client = value

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

    def check_request(self, body):
        """Everything about a call that can be refused before a model is called; returns its attachments (R-E2-014, R-E2-022)."""
        if not isinstance(body, dict):
            raise ValueError('the call must be a JSON object')
        if not isinstance(body.get('question'), str) or not body['question'].strip():
            raise ValueError('question is required')
        conversation(body.get('history'))
        attachments = answer_attachments.parse(body.get('attachments'))
        page = body.get('page')
        if page is not None and (not isinstance(page, str) or page not in self.docs):
            raise ValueError('page: no such knowledge file')
        if body.get('role') not in (None, '') and body['role'] not in ROLES:
            raise ValueError('role: one of ' + ', '.join(ROLES))
        window, reserve = self.cfg.get('context_window'), self.cfg.get('answer_reserve_tokens', 60000)
        if window and attachments:
            used = answer_attachments.tokens(attachments, answer_modes._tok, self.cfg.get('image_tokens', 1500))
            used += answer_modes._tok(json.dumps([body.get('question'), body.get('history'), body.get('turns')], default=str))
            if used > window - reserve:
                big = max((a for a in attachments if a.kind == 'csv'), key=lambda a: len(a.raw), default=attachments[0])
                raise ValueError(f"attachment {big.name}: too large for the model's context "
                                 f'({used} tokens against {window - reserve} available)')
        return attachments

    def answer(self, body):
        """One answer: refuses a bad call before any model call, then runs the pipeline and adds what every answer
        carries: sources, time and use, the trace ID, the missing facts and what was read from the attachments."""
        attachments = self.check_request(body)
        progress = answer_progress.current()
        if progress is None:
            progress = answer_progress.Progress()
            with answer_progress.use(progress):
                return self._answered(body, attachments, progress)
        return self._answered(body, attachments, progress)

    def run_job(self, body, progress):
        return self.answer(body)

    def _answered(self, body, attachments, progress):
        out = self._answer(body, attachments, progress)
        trace = out.pop('_trace')
        report = progress.finish()
        sources = [{'id': i, 'title': self.docs[i].title} for i in out['files_read'] if i in self.docs]
        read = next((s['output'].get('images') for s in trace if s.get('action') == 'understand' and isinstance(s.get('output'), dict)), None)
        trace_id = self.traces.new_id()
        out.update(report, sources=sources, trace_id=trace_id,
                   attachments_read=(read or []) if any(a.kind == 'image' for a in attachments) else [])
        self.traces.save(trace_id, {'question': (body.get('question') or '')[:2000], 'role': body.get('role'), 'page': body.get('page'),
                                    'model': self.model, 'knowledge_commit': self.commit, 'type': out['type'],
                                    'files_read': out['files_read'], 'missing_facts': out['missing_facts'],
                                    'attachments': [a.info() for a in attachments], 'steps': trace, **report})
        return out

    def _answer(self, body, attachments, progress):
        history = conversation(body.get('history'))
        first = ((body.get('turns') or [None])[0] or body.get('question') or '').strip()  # a clarifying reply: its question
        progress.enter('topic')
        topic = self.topic(body)
        history = history if topic['continues'] else []
        progress.enter('shape')
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
        missing = missing_facts(body.get('facts')) if asks['page_values'] else []
        extra = {k: v for k, v in (('attachments', attachments), ('missing', missing)) if v}   # the call's own shape when empty
        turns = body.get('turns')
        if turns:
            turns = [question_text({**body, 'question': turns[0]}, lead, **extra)] + list(turns[1:])
        else:
            turns = [question_text(body, lead, **extra)]
        progress.enter('understand')
        out = answer_modes.converse('agent-e2', self.client, self.model, turns, [a.part() for a in attachments], self.cfg,
                                    self.retriever, history, shape, body.get('page'))
        progress.enter('check')
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
                'knowledge_commit': self.commit, 'missing_facts': missing, '_trace': out['trace']}

    def no_repeat(self, text, shown):
        """One rewrite when the text repeats a figure of the opening above it. No opening: nothing to repeat."""
        shown = [x for x in shown if x]
        dup = repeated_figures(text, headline_figures(shown))
        if not dup:
            return text
        _stage('rewrite')
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
        _stage('rewrite')
        res = self.client.chat(self.model, [{'role': 'user', 'content': REWRITE_COLOUR.format(hits='"; "'.join(hits), text=text)}],
                               temperature=self.cfg.get('temperature'), max_tokens=self.cfg.get('max_tokens', 2000))
        again = (res.get('content') or '').strip()
        return again if again and not colour_reasons(again) and not pipeline_words(again) else text

    def screen_wording(self, text):
        """One rewrite when the answer speaks of the data instead of the screen ("the provided JSON")."""
        bad = pipeline_words(text)
        if not bad:
            return text
        _stage('rewrite')
        res = self.client.chat(self.model, [{'role': 'user', 'content': REWRITE.format(words=', '.join(bad), text=text)}],
                               temperature=self.cfg.get('temperature'), max_tokens=self.cfg.get('max_tokens', 2000))
        again = (res.get('content') or '').strip()
        return again if again and not pipeline_words(again) else text


def _stage(name):
    progress = answer_progress.current()
    if progress is not None:
        progress.enter(name)


def _shown(line):
    """A computed line as the person reads it: without the instruction to the model and the calculator's note."""
    line = re.sub(r'\s*\[arithmetic_calculator\.py:.*\]\s*$', '', line)
    line = re.sub(r'\s*(?:Say this first\.|give the range and do not call a move a drop\.)\s*$', '', line).lstrip('- ').strip()
    return screen_time(line)


def handler_for(service, secret=None, max_body=41943040):
    """The HTTP handler. secret: the caller's secret (AGENT_E2_SECRET); with one set, every call except GET /v1/health
    needs the header `Authorization: Bearer <secret>` (R-E2-024). max_body: the largest request body in bytes (R-E2-014)."""
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def send(self, code, data, headers=None):
            body = json.dumps(data, ensure_ascii=False, default=str).encode()
            self.send_response(code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            for k, v in (headers or {}).items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(body)

        def allowed(self):
            if not secret:
                return True
            given = self.headers.get('Authorization') or ''
            return hmac.compare_digest(given.encode(), f'Bearer {secret}'.encode())

        def do_GET(self):
            if self.path == '/v1/health':
                return self.send(200, {'ok': True, 'model': service.model, 'files': len(service.docs),
                                       'knowledge_commit': service.commit})
            if not self.allowed():
                return self.send(401, {'error': 'unauthorised'})
            kind, _, ident = self.path.removeprefix('/v1/').partition('/')
            found = {'jobs': service.jobs.get, 'traces': service.traces.get}.get(kind)
            if not found or '/' in ident:
                return self.send(404, {'error': 'not found'})
            data = found(ident)
            return self.send(200, data) if data is not None else self.send(404, {'error': 'not found'})

        def do_POST(self):
            route = {'/v1/answer': service.answer, '/v1/suggest': service.suggest, '/v1/topic': service.topic}.get(self.path)
            if not route:
                return self.send(404, {'error': 'not found'})
            if not self.allowed():
                return self.send(401, {'error': 'unauthorised'})
            size = int(self.headers.get('Content-Length') or 0)
            if size > max_body:
                self.close_connection = True
                left = min(size, 256 * 1024 * 1024)   # read what was sent, so the caller sees the reply
                while left > 0:
                    chunk = self.rfile.read(min(65536, left))
                    if not chunk:
                        break
                    left -= len(chunk)
                return self.send(413, {'error': f'the request is above {max_body // (1024 * 1024)} MB'}, {'Connection': 'close'})
            try:
                body = json.loads(self.rfile.read(size) or b'{}')
                if self.path == '/v1/answer' and isinstance(body, dict) and body.get('async') is True:
                    service.check_request(body)
                    try:
                        return self.send(202, {'job': service.jobs.submit(body), 'state': 'queued'})
                    except answer_jobs.Busy:
                        return self.send(429, {'error': 'Agent E2 is busy with other answers: ask again shortly'},
                                         {'Retry-After': '30'})
                return self.send(200, route(body))
            except ValueError as e:
                return self.send(400, {'error': str(e)})
            except LLMError:
                return self.send(502, {'error': 'model unavailable'})
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
        cfg = {**cfg, 'embedding_model': None, 'trace_dir': tempfile.mkdtemp(prefix='agent-e2-mock-traces-')}
    if os.environ.get('AGENT_E2_TRACE_DIR'):
        cfg = {**cfg, 'trace_dir': os.environ['AGENT_E2_TRACE_DIR']}
    service = Service(cfg, MockClient() if a.mock else None)
    secret = os.environ.get('AGENT_E2_SECRET') or None
    print(f'Agent E2 service on http://{a.host}:{a.port}/v1/answer, model {service.model}, {len(service.docs)} files'
          + (', caller secret required' if secret else ''))
    ThreadingHTTPServer((a.host, a.port), handler_for(service, secret, cfg.get('max_body_bytes', 41943040))).serve_forever()


if __name__ == '__main__':
    main()
