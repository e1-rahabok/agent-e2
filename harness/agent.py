"""Agent E2's agent: the neuro-symbolic expert system. Design: harness/AGENT.md.

Code leads; the model reads and writes. One pipeline for every question, six stages:
  1. understand: the model reads the question (and its images) into a case, a fixed JSON shape; code keeps only what
     resolves, and the code-only reading of planner.py always runs, so a failed extraction leaves a usable case;
  2. plan: code builds the reading set from the knowledge base's map (planner.py);
  3. compute: code runs the exact tools on the case's values (catalog facts, summation conversions);
  4. ask: in a conversation, code decides whether the model may ask the user once;
  5. answer: the model reads the reading set and writes; consensus samples share the one reading set (modes.py);
  6. check: verifier with one repair turn; one gap follow-up when the draft names a metric whose file was not read;
     a coverage flag when nothing the question names is in the knowledge base.
The model makes no tool calls, so no tool-call format can break and no fallback mode exists.
"""
import json
import re

import calc
import catalog
import planner
import primer
import terms
import verify
import web

KINDS = ('how-it-works', 'metric-meaning', 'term-meaning', 'what-to-set', 'health-check', 'troubleshooting', 'decision-tree')

UNDERSTAND = (
    'Read the question below into a JSON object. Do not answer it. Copy names exactly as the question writes them.\n'
    'Fields:\n'
    f'- "kind": one of {", ".join(KINDS)}.\n'
    '- "objects": object types named or implied: VM, ESXi host, cluster, datastore, resource pool, Guest OS.\n'
    '- "metrics": a list of {"name", "object", "value", "unit", "interval", "tool"}: every metric, counter, chart label or '
    'esxtop field in the question or the images. value as a number or null; interval as written ("real-time", "20 seconds", '
    '"past day") or null; tool: vCenter, esxtop, VCF Operations, Windows, Linux or null.\n'
    '- "vcpus": the VM\'s vCPU count as a number, or null.\n'
    '- "symptom": what the user observes, or null.\n'
    '- "premise": a belief the question takes for granted that may be wrong, or null.\n'
    '- "claims": the separate things the question asks to decide, one short line each.\n'
    '- "missing": facts the question does not give that the answer depends on (object, interval, vCPU count, version).\n'
    '- "images": per image, {"tool", "object", "shows"}: what the screen is and the values it shows.\n'
    'Reply with the JSON object only.')

ANSWER_RULES = (
    '\nHow to use what you are given:\n'
    '- The case is how the question was read; check it against the question.\n'
    '- Computed facts are exact: use them, do not compute again.\n'
    '- Base each claim on a knowledge base file and name its id. The knowledge base wins over what you believe.\n')
OPEN_SHAPE = ('- If a claim rests on no file, put it under a last line "Not settled by the knowledge base:" '
              'instead of stating it as fact.\n')
GAP = ('Your draft relies on these metrics, and their files were not in what you read: {names}. '
       'Their text is below. Check your answer against it and answer again, in the same format.\n\n{text}\n\n')

COUNTER_MS = re.compile(r'\b([a-z]+\.[a-zA-Z]+(?:\.[a-z]+)?)\s*(?:=|:|of|at|is)?\s*([\d][\d,]*(?:\.\d+)?)\s*ms\b')
VCPUS = re.compile(r'\b(\d+)[- ]?vCPU', re.I)
INTERVAL_SECONDS = (  # the vSphere Client chart intervals: vsphere/tools/vsphere-client/vcenter-statistics
    (re.compile(r'real[- ]?time|20[- ]?s(ec(ond)?s?)?\b', re.I), 20),
    (re.compile(r'past day|1 day|one day|5[- ]?min(ute)?s?\b|300 ?s', re.I), 300),
    (re.compile(r'past week|1 week|30[- ]?min(ute)?s?\b', re.I), 1800),
    (re.compile(r'past month|1 month|2[- ]?hours?\b', re.I), 7200),
    (re.compile(r'past year|1 year', re.I), 86400),
)


def _step(trace, action, inp, out, res=None):
    s = {'step': len(trace) + 1, 'action': action, 'input': inp, 'output': out}
    if res:
        s.update({k: res.get(k) for k in ('prompt_tokens', 'completion_tokens', 'latency', 'provider')})
    trace.append(s)


def _tok(text):
    return len(text) // 4


def _user(text, images):
    if not images:
        return {'role': 'user', 'content': text}
    return {'role': 'user', 'content': [{'type': 'text', 'text': text}] + images}


# ---------- stage 1: understand ----------
def parse_case(text):
    """The first JSON object in a reply, as a dict with the expected fields; {} when there is none."""
    m = re.search(r'\{.*\}', text or '', re.S)
    if not m:
        return {}
    try:
        raw = json.loads(m.group(0))
    except json.JSONDecodeError:
        return {}
    if not isinstance(raw, dict):
        return {}
    case = {k: raw.get(k) for k in ('kind', 'objects', 'metrics', 'vcpus', 'symptom', 'premise', 'claims', 'missing', 'images')}
    if case['kind'] not in KINDS:
        case['kind'] = None
    for k in ('objects', 'metrics', 'claims', 'missing', 'images'):
        v = case[k]
        case[k] = [x for x in v if x] if isinstance(v, list) else []
    case['metrics'] = [m for m in case['metrics'] if isinstance(m, dict) and m.get('name')]
    case['vcpus'] = case['vcpus'] if isinstance(case['vcpus'], (int, float)) and case['vcpus'] > 0 else None
    return case


def understand(client, model, question, images, cfg, trace, kw):
    """Stage 1: the model's case. A reply that is not JSON leaves an empty case: the code-only reading of planner.py
    runs in every case, so the plan never depends on this call. Asked at temperature 0 (deterministic), so the same
    question is read the same way every time."""
    case = {}
    if cfg.get('case_model', True):
        res = client.chat(model, [{'role': 'system', 'content': UNDERSTAND}, _user(f'Question:\n{question}', images)],
                          max_tokens=cfg.get('case_max_tokens', 1200), deterministic=True, provider_order=kw['provider_order'])
        case = parse_case(res.get('content'))
        _step(trace, 'understand', '', {k: v for k, v in case.items() if v} or 'unreadable: code-only case', res)
    case = case or {k: [] for k in ('objects', 'metrics', 'claims', 'missing', 'images')}
    case['code_objects'] = sorted(planner.objects_in(question))
    return case


# ---------- stage 3: compute ----------
def _interval(text):
    for pat, sec in INTERVAL_SECONDS:
        if pat.search(str(text or '')):
            return sec
    return None


def compute(case, question, retriever, used):
    """Stage 3: exact values the model reads instead of computing. Catalog facts of the files read come with the
    reading set (catalog.facts_for); here: summation counters given in ms, turned into % by calc.py."""
    lines, cat = [], catalog.get(retriever.docs)
    found = list(case.get('metrics') or [])
    for key, num in COUNTER_MS.findall(question):  # the code-only reading: 'cpu.ready.summation = 8,000 ms'
        found.append({'name': key, 'value': float(num.replace(',', '')), 'unit': 'ms'})
    if not case.get('vcpus'):
        v = VCPUS.search(question)
        case = dict(case, vcpus=int(v.group(1)) if v else None)
    for m in found:
        unit = str(m.get('unit') or '').lower()
        value = m.get('value')
        if not isinstance(value, (int, float)) or unit not in ('ms', 'millisecond', 'milliseconds'):
            continue
        rows = cat.lookup(str(m['name']), catalog.norm_object(m.get('object')) if m.get('object') else None).get('counters', [])
        if not any(r.get('rollup') == 'summation' for r in rows[:2]) and 'summation' not in str(m['name']).lower():
            continue
        sec = _interval(m.get('interval')) or _interval(question)
        if not sec:
            continue
        one = calc.evaluate(f'summation_to_percent({value}, {sec}, 1)')
        line = f"- {m['name']} = {value:g} ms in a {sec}-second sample: {one.get('result'):g}% of one vCPU"
        if case.get('vcpus'):
            per = calc.evaluate(f"summation_to_percent({value}, {sec}, {case['vcpus']})")
            line += f"; {per.get('result'):g}% per vCPU of {case['vcpus']:g} vCPUs (the counter sums every vCPU)"
        lines.append(line + '. [calc.py: ' + '; '.join(one.get('notes') or []) + ']')
    return ('Computed (exact):\n' + '\n'.join(dict.fromkeys(lines))) if lines else ''


# ---------- stage 6: check ----------
def gaps(docs, case, draft, used, limit=2):
    """Metric files the draft names that are not in the reading set, for the objects of the case."""
    objs = planner.objects_in(' '.join(map(str, case.get('objects') or [])) + ' ' + ' '.join(case.get('code_objects') or []))
    return [i for i in planner.anchors(docs, draft, objs or None, strict=True) if i not in used][:limit]


def coverage(tiers):
    """Weak when the question names nothing the knowledge base holds and gets no flow: only search hits."""
    return 'weak' if not any(t in ('flow', 'named') for t in tiers.values()) else 'named'


# ---------- the pipeline ----------
def prepare(client, model, question, images, cfg, trace, retriever, kind, prompts):
    """Stages 1-4: everything before the model writes. The result is shared by every consensus sample, so the
    samples differ only in the model's reasoning, never in what it read. prompts: modes.PROMPTS."""
    kw = {'provider_order': cfg.get('provider_order', {}).get(model)}
    case = understand(client, model, question, images, cfg, trace, kw)                                   # 1
    reading, used, hits, tiers = planner.reading_set(retriever, question, cfg, case=case)                 # 2
    _step(trace, 'plan', question[:200], {t: [i for i in used if tiers[i] == t] for t in planner.ORDER if t in tiers.values()})
    computed = compute(case, question, retriever, used)                                                  # 3
    if computed:
        _step(trace, 'compute', '', computed.split('\n')[1:])
    cover = coverage(tiers)
    _step(trace, 'coverage', '', cover)
    p = prompts[kind]
    if kind == 'chat':                                                                                   # 4
        reasons = [r for r, on in (('missing fact', case.get('missing')), ('premise', case.get('premise')),
                                   ('premise term', any(h.get('premise') for h in terms.match(question)))) if on]
        if not reasons:
            p = prompts['chat_final']
        _step(trace, 'ask', '', ('allowed: ' + ', '.join(reasons)) if reasons else 'no: nothing missing, no premise')
    system = p['kb'] + ANSWER_RULES + (OPEN_SHAPE if kind != 'choice' else '')
    up_front = primer.build(retriever.docs, cfg.get('primer') or {})
    if up_front:
        system += '\n\n' + up_front
    pages = web.gather(question, cfg['web']) if (cfg.get('web') or {}).get('enabled') else []
    if pages:
        _step(trace, 'web', [p_['url'] for p_ in pages], [p_.get('error') or f"{_tok(p_['text'])} tokens" for p_ in pages])
    shown = {k: v for k, v in case.items() if v}
    text = (f'Case (how the question was read):\n{json.dumps(shown, ensure_ascii=False)}\n\n'
            + (f'{computed}\n\n' if computed else '')
            + ('Coverage: the question names nothing the knowledge base holds; if the text below does not settle it, '
               'say the question is outside the knowledge base.\n\n' if cover == 'weak' else '')
            + f'Knowledge base:\n{reading}'
            + ('\n\n' + web.block(pages) if pages else '')
            + f'\n\nQuestion:\n{question}')
    return {'case': case, 'used': used, 'seen': reading + '\n' + computed, 'format': p['format'],
            'msgs': [{'role': 'system', 'content': system}, _user(text, images)], 'kw': kw}


def write(client, model, question, cfg, trace, retriever, kind, prep, verified):
    """Stages 5-6: the model answers from the prepared messages; code checks. Returns (result, ids read)."""
    kw, msgs, used, seen = prep['kw'], prep['msgs'], list(prep['used']), prep['seen']
    import modes  # the window estimate lives with the prompts; imported here because modes imports this module
    if modes.over_window(msgs, cfg):
        _step(trace, 'context_over', cfg.get('context_window'), 'prompt larger than the deployed window')
    res = client.chat(model, msgs, temperature=cfg.get('temperature'), max_tokens=cfg['max_tokens'], **kw)   # 5
    _step(trace, 'answer', '', (res.get('content') or '')[:400], res)
    if cfg.get('gap_followup', True) and res.get('content'):                                             # 6
        missing = gaps(retriever.docs, prep['case'], res['content'], used)
        if missing:
            extra = '\n\n'.join(planner.sections_of(retriever, i, question, cfg.get('plan_section_tokens', 400)) for i in missing)
            names = ', '.join(retriever.docs[i].title for i in missing)
            msgs = msgs + [{'role': 'assistant', 'content': res['content']},
                           {'role': 'user', 'content': GAP.format(names=names, text=extra) + prep['format']}]
            res = client.chat(model, msgs, temperature=cfg.get('temperature'), max_tokens=cfg['max_tokens'], **kw)
            _step(trace, 'gap', missing, (res.get('content') or '')[:400], res)
            used += missing
            seen += '\n' + extra
    if kind == 'choice':
        res = verified(client, model, msgs, res, question, seen, set(retriever.docs), cfg, trace, kw['provider_order'])
    return res, used
