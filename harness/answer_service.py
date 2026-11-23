"""Agent E2 as a service: one HTTP endpoint that answers a question with the live facts a caller sends.

The caller is PCM (Private Cloud Management): PCM owns the data, the actions, the user's identity and every screen;
Agent E2 owns the knowledge base, the reading plan, the flow executor and the model call (project/plan.md, decision of
2026-11-20). The answer is the shipped pipeline, `answer_modes.converse('agent-e2', ...)`, unchanged.

    POST /v1/answer
      {"question": "...", "facts": {...} (optional, JSON from the caller), "turns": [...] (optional, for the clarifying
       round: [question, Agent E2's questions, the user's reply]), "role": "l1" | "l2" | "capacity" | "executive" (optional)}
    -> 200 {"type": "answer" | "clarify", "content": "...", "questions": [...], "files_read": [...],
            "lead": "...", "computed": [...], "model": "...", "knowledge_commit": "..."}
    lead: the opening the person reads first, written by code from the calculator's numbers in plain words (empty when no
    KPI series was sent); the model's text continues from it. computed: the calculator's lines, exact, for review; the
    screen shows the lead, not these.
    POST /v1/suggest
      {"facts": {"object": {"kind": "cluster" | "host" | "vm"}, "pillar": "Performance" | "Capacity", "window": "...",
                 "kpis": [{"label": "...", "better": "higher" | "lower", "points": [[time, value], ...]}, ...]}}
    -> 200 {"situation": {"pillar", "kind", "level": "good" | "medium" | "bad", "movement": null | "declining" | "dip" | "rising"},
            "questions": [3 at most], "basis": [...]}
    The questions a whole page suggests, chosen by its situation, read by code with no model call (user_suggestions.py).
    GET /v1/health -> 200 {"ok": true, "model": "...", "files": n}

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
import catalog_database  # noqa: E402
import expert_agent  # noqa: E402
import knowledge_loader  # noqa: E402
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
    'How to answer a person on a PCM screen:\n'
    '- They typed only the question. They see the PCM page named under "screen", not the data below. Speak of what they '
    'see: the chart, the tab, the page, an object by its name. Never mention JSON, the facts, a payload or the data '
    'provided.\n'
    '- When an opening is given below, the person reads it first, as the start of your answer, in the same voice. Continue '
    'from it: never repeat a figure, the time or the verdict it gives (the computed line on how the KPI moved across the '
    'window holds the same figures), and never say a number is "computed".\n'
    '- Answer the question asked, in the first sentence. When it asks why a score moved, what is wrong or what to check, do not '
    'open with the drop or the level: open with the cause, which part pulled the score down, then where to look next. When it '
    'asks how a metric works, what it measures or why it is designed so, explain the mechanism from the knowledge base first; '
    'the page\'s figures come after, as a short example, or not at all.\n'
    '- If the opening says the KPI stayed within its normal movement, do not restate the range: say what the KPI measures and '
    'why this movement is normal.\n'
    '- Other computed lines are exact: give their figures as written when the answer needs them (for example a sub-metric\'s '
    'own value). For a question on why a score moved or what is wrong: if a computed line names the sub-metric that moved a '
    'score most, lead with that sub-metric and its band, then the next step for that resource. Give every sub-metric the band '
    'the computed line gives it: an orange or red one is never low.\n'
    '- With no opening, answer directly first, with the figures.\n'
    '- If "screen" names where to look next (drill_down), point there first, by page and tab, before any knowledge-base flow.\n'
    '- If a value the answer needs is not in the data, name the PCM page that shows it, or say PCM does not show it yet.\n'
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
                   'worst point and any sentence that only restates the verdict. Open with the cause: which part pulled the '
                   'KPI down, then where to look next. Keep every other fact, name and number. Do not say computed, '
                   'calculator, the box above or the model. Reply with the answer only.\n\n{text}')
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
    return ' '.join(out)


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

    def lead(self, facts):
        if not facts:
            return ''
        rows = expert_agent.kpi_trend_rows(facts, self.cat)
        if isinstance(facts, dict) and facts.get('asked_about_kpi'):
            rows = rows[:1]  # a question on one KPI card: the opening is about that KPI; the others are context
        return (lead_text(rows, facts) + step_text(expert_agent.kpi_step_row(facts, self.cat))).strip()

    def suggest(self, body):
        return user_suggestions.suggest(body.get('facts'), self.cat, self.suggestions, screen_time)

    def answer(self, body):
        # A metric question of the page (user_suggestions.yaml, metric) asks how a KPI works: it is answered from the knowledge
        # base, with the page named but not its numbers. With the numbers, the model opened with what pulled the score down.
        if user_suggestions.is_metric(body.get('question'), self.suggestions) and isinstance(body.get('facts'), dict):
            body = {**body, 'facts': {k: v for k, v in body['facts'].items() if k in METRIC_FACTS}}
            lead = ''
        else:
            lead = self.lead(body.get('facts'))
        turns = body.get('turns')
        if turns:
            turns = [question_text({**body, 'question': turns[0]}, lead)] + list(turns[1:])
        else:
            turns = [question_text(body, lead)]
        out = answer_modes.converse('agent-e2', self.client, self.model, turns, [], self.cfg, self.retriever)
        computed = [line for s in out['trace'] if s.get('action') == 'compute' for line in (s.get('output') or [])]
        content = no_file_refs(out['result'].get('content'), self.docs)
        if body.get('facts') and out['type'] == 'answer':
            content = self.screen_wording(content)
            # The figures the person reads in the opening, and the same figures, exact, in the trend line.
            content = self.no_repeat(content, [lead] + [_shown(c) for c in computed if TREND_LINE.search(c)])
            content = no_file_refs(content, self.docs)  # a rewrite may bring a path back
        return {'type': out['type'], 'content': content, 'questions': out.get('questions', []),
                'files_read': out['used'], 'lead': lead if out['type'] == 'answer' else '',
                'computed': [_shown(c) for c in computed], 'model': self.model,
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
                return self.send(200, {'ok': True, 'model': service.model, 'files': len(service.docs)})
            return self.send(404, {'error': 'not found'})

        def do_POST(self):
            if self.path not in ('/v1/answer', '/v1/suggest'):
                return self.send(404, {'error': 'not found'})
            try:
                body = json.loads(self.rfile.read(int(self.headers.get('Content-Length') or 0)) or b'{}')
                return self.send(200, service.suggest(body) if self.path == '/v1/suggest' else service.answer(body))
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
