"""Agent E2 as a service: one HTTP endpoint that answers a question with the live facts a caller sends.

The caller is PCM (Private Cloud Management): PCM owns the data, the actions, the user's identity and every screen;
Agent E2 owns the knowledge base, the reading plan, the flow executor and the model call (project/plan.md, decision of
2026-11-20). The answer is the shipped pipeline, `answer_modes.converse('agent-e2', ...)`, unchanged.

    POST /v1/answer
      {"question": "...", "facts": {...} (optional, JSON from the caller), "turns": [...] (optional, for the clarifying
       round: [question, Agent E2's questions, the user's reply]), "role": "l1" | "l2" | "capacity" | "executive" (optional)}
    -> 200 {"type": "answer" | "clarify", "content": "...", "questions": [...], "files_read": [...],
            "computed": [...], "model": "...", "knowledge_commit": "..."}
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
import expert_agent  # noqa: E402
import knowledge_loader  # noqa: E402
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
    '- Computed lines, when given, are shown to the person above your text, so they already read every figure and the verdict. '
    'Never repeat a figure, a time or the verdict of a computed line, and never say a number is "computed". Do not open with '
    'the drop or the level. Open with the cause: which part pulled the score down, then where to look next. You may give a '
    'figure only if no computed line holds it (for example a sub-metric\'s own value).\n'
    '- If a computed line says a KPI is steady, do not restate the range: open with what the KPI measures and why this movement '
    'is normal.\n'
    '- If a computed line names the sub-metric that moved a score most, lead with that sub-metric and its band, then '
    'the next step for that resource. Give every sub-metric the band the computed line gives it: an orange or red one is never low.\n'
    '- With no computed line, answer directly first, with the figures.\n'
    '- If "screen" names where to look next (drill_down), point there first, by page and tab, before any knowledge-base flow.\n'
    '- If a value the answer needs is not in the data, name the PCM page that shows it, or say PCM does not show it yet.')
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
# A computed line that lists the sub-metrics holds figures the answer may use (a part's own value).
PART_LINE = re.compile(r'sub-metrics', re.I)
MONTHS = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
ISO_TIME = re.compile(r'\b(\d{4})-(\d\d)-(\d\d)[T ](\d\d):(\d\d)(?::\d\d(?:\.\d+)?)?(?:Z|[+-]\d\d:?\d\d)?')
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
    return sorted(f for f in figures if re.search(r'(?<![\d.])' + re.escape(f) + r'(?![\d]|\.\d)', text or ''))


def question_text(body):
    """The question as Agent E2's pipeline reads it: the caller's question, who asks, how to speak to them, then the facts."""
    q = (body.get('question') or '').strip()
    if not q:
        raise ValueError('question is required')
    role = ROLES.get(body.get('role') or '')
    if role:
        q += f'\n\nThe person asking is {role}.'
    facts = body.get('facts')
    if facts:
        q += '\n\n' + SCREEN_RULES
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

    def answer(self, body):
        turns = body.get('turns')
        if turns:
            turns = [question_text({**body, 'question': turns[0]})] + list(turns[1:])
        else:
            turns = [question_text(body)]
        out = answer_modes.converse('agent-e2', self.client, self.model, turns, [], self.cfg, self.retriever)
        computed = [line for s in out['trace'] if s.get('action') == 'compute' for line in (s.get('output') or [])]
        content = out['result'].get('content')
        if body.get('facts') and out['type'] == 'answer':
            content = self.screen_wording(content)
            content = self.no_repeat(content, [_shown(c) for c in computed])
        return {'type': out['type'], 'content': content, 'questions': out.get('questions', []),
                'files_read': out['used'], 'computed': [_shown(c) for c in computed], 'model': self.model,
                'knowledge_commit': self.commit}

    def no_repeat(self, text, shown):
        """One rewrite when the text repeats a figure of the computed lines above it. No computed line: nothing to repeat."""
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
            if self.path != '/v1/answer':
                return self.send(404, {'error': 'not found'})
            try:
                body = json.loads(self.rfile.read(int(self.headers.get('Content-Length') or 0)) or b'{}')
                return self.send(200, service.answer(body))
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
