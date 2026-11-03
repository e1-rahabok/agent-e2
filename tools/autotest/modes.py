"""Answer modes: baseline (no knowledge base), classic RAG, agentic retrieval (tool loop)."""
import json

from llm import LLMError

FORMAT = ('Reply with exactly two lines and nothing else:\n'
          'ANSWER: <letter or letters, comma separated>\n'
          'REASON: <one sentence>')

SYSTEM_BASE = ('You are an expert on VMware vSphere and VCF metrics. Answer the multiple-choice question.\n' + FORMAT)

SYSTEM_KB = (
    'You answer questions about VMware vSphere and VCF metrics using ONLY the knowledge base text provided to you.\n'
    'Rules:\n'
    '- Treat the knowledge base as the source of truth, even when it contradicts what you believe about IT in general.\n'
    '- Prefer mechanism and reason over definitions. Watch for metrics with the same name on different objects.\n'
    '- Quote a threshold only when the knowledge base states it.\n'
    '- If the knowledge base does not cover the question, choose the option "Not covered by the knowledge base."\n'
    + FORMAT)

SYSTEM_AGENT = SYSTEM_KB.replace(
    'using ONLY the knowledge base text provided to you',
    'using ONLY knowledge base text you retrieve with the tools. You know nothing about vSphere metrics beyond what the tools return') + (
    '\nTool rules:\n'
    '- Your first action must be search.\n'
    '- Answer only from text returned by read_file.\n'
    '- Before answering about a metric, call follow_links with link_type "same_name" on its file.\n'
    '- For a troubleshooting question, read the matching diagnosis file first and follow its numbered steps.\n'
    '- You have at most {max_calls} tool calls. Then answer.')

TOOLS = [
    {'type': 'function', 'function': {
        'name': 'search', 'description': 'Search the knowledge base. Returns file ids, titles, snippets.',
        'parameters': {'type': 'object', 'properties': {
            'query': {'type': 'string'},
            'product': {'type': 'string', 'description': 'vsphere, vsan, nsx, vcf-operations, windows, linux'},
            'object': {'type': 'string', 'description': 'VirtualMachine, HostSystem, ClusterComputeResource, Datastore, ...'},
            'technology': {'type': 'string', 'description': 'cpu, memory, storage, network, system'},
            'retriever_guide': {'type': 'string', 'description': 'how-it-works, metric-meaning, term-meaning, what-to-set, what-to-check'}},
            'required': ['query']}}},
    {'type': 'function', 'function': {
        'name': 'read_file', 'description': 'Read one knowledge file, or one section of it.',
        'parameters': {'type': 'object', 'properties': {
            'id': {'type': 'string'}, 'heading': {'type': 'string'}}, 'required': ['id']}}},
    {'type': 'function', 'function': {
        'name': 'follow_links', 'description': 'List files linked from a file. Titles only.',
        'parameters': {'type': 'object', 'properties': {
            'id': {'type': 'string'},
            'link_type': {'type': 'string', 'enum': ['related', 'internal_derive', 'same_name', 'same_meaning', 'all']}},
            'required': ['id']}}},
    {'type': 'function', 'function': {
        'name': 'get_images', 'description': 'List image records (diagrams, charts) of a file.',
        'parameters': {'type': 'object', 'properties': {'id': {'type': 'string'}}, 'required': ['id']}}},
]


def _user(text, images):
    if not images:
        return {'role': 'user', 'content': text}
    return {'role': 'user', 'content': [{'type': 'text', 'text': text}] + images}


def _tok(text):
    return len(text) // 4


def _step(trace, action, inp, out, res=None):
    s = {'step': len(trace) + 1, 'action': action, 'input': inp, 'output': out}
    if res:
        s.update({k: res.get(k) for k in ('prompt_tokens', 'completion_tokens', 'latency', 'provider')})
    trace.append(s)


def baseline(client, model, question, images, cfg, trace):
    res = client.chat(model, [{'role': 'system', 'content': SYSTEM_BASE}, _user(question, images)],
                      temperature=cfg['temperature'], max_tokens=cfg['max_tokens'], provider_order=cfg.get('provider_order', {}).get(model))
    _step(trace, 'answer', '', res['content'][:400], res)
    return res, []


def classic_context(retriever, question, cfg):
    """One fixed retrieval pass: search, expand same_name and related, fit to budget."""
    hits = retriever.search(question, k=cfg['classic_k'])
    ids = [h['id'] for h in hits]
    for h in hits[:2]:
        for link in retriever.links(h['id'], 'same_name') + retriever.links(h['id'], 'related')[:2]:
            if link['id'] in retriever.docs and link['id'] not in ids:
                ids.append(link['id'])
    budget, parts, used = cfg['context_tokens'], [], []
    for i in ids:
        d = retriever.docs[i]
        block = f'### {d.title}\nid: {d.id} | status: {d.status}\n{d.body}'
        if _tok(block) > budget:
            block = block[:budget * 4]
        parts.append(block)
        used.append(i)
        budget -= _tok(block)
        if budget <= 200:
            break
    return '\n\n'.join(parts), used, hits


def classic(client, model, question, images, cfg, trace, retriever):
    context, used, hits = classic_context(retriever, question, cfg)
    _step(trace, 'search', question[:200], [h['id'] for h in hits])
    _step(trace, 'context', '', used)
    msgs = [{'role': 'system', 'content': SYSTEM_KB},
            _user(f'Knowledge base:\n{context}\n\nQuestion:\n{question}', images)]
    res = client.chat(model, msgs, temperature=cfg['temperature'], max_tokens=cfg['max_tokens'],
                      provider_order=cfg.get('provider_order', {}).get(model))
    _step(trace, 'answer', '', res['content'][:400], res)
    return res, used


def _run_tool(retriever, name, args, state):
    if name == 'search':
        filters = {k: args[k] for k in ('product', 'object', 'technology', 'retriever_guide') if args.get(k)}
        out = retriever.search(args.get('query', ''), filters=filters, k=8)
        state['searched'] = True
        return json.dumps(out, indent=0)
    if name == 'read_file':
        d = retriever.docs.get(args.get('id', ''))
        if not d:
            return json.dumps({'error': f'unknown id {args.get("id")}'})
        state['read'].append(d.id)
        text = d.body
        if args.get('heading'):
            text = next((t for h, t in d.sections if h.lower() == args['heading'].lower()), text)
        return f'id: {d.id} | status: {d.status}\n{text}'
    if name == 'follow_links':
        lt = args.get('link_type', 'all')
        if lt in ('same_name', 'all'):
            state['same_name_checked'].add(args.get('id'))
        return json.dumps(retriever.links(args.get('id', ''), lt), indent=0)
    if name == 'get_images':
        d = retriever.docs.get(args.get('id', ''))
        return json.dumps(d.images if d else [], indent=0)
    return json.dumps({'error': f'unknown tool {name}'})


def agentic(client, model, question, images, cfg, trace, retriever):
    """Tool loop. Returns (final result, ids read). Raises FallbackNeeded on repeated format errors."""
    max_calls, budget = cfg['agent_max_calls'], cfg['agent_tool_tokens']
    msgs = [{'role': 'system', 'content': SYSTEM_AGENT.format(max_calls=max_calls)}, _user(question, images)]
    state = {'read': [], 'same_name_checked': set(), 'searched': False}
    seen, calls, errors, reminded, tokens_used = set(), 0, 0, False, 0
    po = cfg.get('provider_order', {}).get(model)
    while True:
        tools = TOOLS if calls < max_calls and tokens_used < budget else None
        if tools is None:
            msgs.append({'role': 'user', 'content': 'Tool budget used. Answer now from what you have read.\n' + FORMAT})
        res = client.chat(model, msgs, tools=tools, temperature=cfg['temperature'], max_tokens=cfg['max_tokens'], provider_order=po)
        tcs = res['tool_calls'] if tools else []
        if not tcs:
            metric_reads = [r for r in state['read'] if '/metrics/' in r and '/comparisons/' not in r]
            unchecked = [r for r in metric_reads if r not in state['same_name_checked']]
            if unchecked and not reminded and tools:
                reminded = True
                msgs.append({'role': 'assistant', 'content': res['content'] or ''})
                msgs.append({'role': 'user', 'content': f'Before answering, call follow_links with link_type "same_name" on: {", ".join(unchecked[:3])}.'})
                _step(trace, 'reminder', '', unchecked[:3], res)
                continue
            _step(trace, 'answer', '', (res['content'] or '')[:400], res)
            return res, state['read']
        msgs.append({'role': 'assistant', 'content': res['content'] or None, 'tool_calls': tcs})
        for n, tc in enumerate(tcs):
            r = res if n == 0 else None
            calls += 1
            name = tc.get('function', {}).get('name', '')
            raw = tc.get('function', {}).get('arguments') or '{}'
            try:
                args = json.loads(raw) if isinstance(raw, str) else raw
            except json.JSONDecodeError:
                errors += 1
                out = json.dumps({'error': 'arguments are not valid JSON'})
                _step(trace, 'tool_error', raw[:200], 'bad json', r)
                if errors >= 2:
                    raise FallbackNeeded('tool call format errors')
            else:
                key = name + json.dumps(args, sort_keys=True)
                if not state['searched'] and name != 'search':
                    out = json.dumps({'error': 'Your first action must be search.'})
                    _step(trace, 'refused', {name: args}, 'search first', r)
                elif key in seen:
                    out = json.dumps({'error': 'Identical call already made. Use the earlier result.'})
                    _step(trace, 'refused', {name: args}, 'repeat', r)
                else:
                    seen.add(key)
                    out = _run_tool(retriever, name, args, state)
                    _step(trace, name, args, _summary(name, out), r)
            tokens_used += _tok(out)
            msgs.append({'role': 'tool', 'tool_call_id': tc.get('id', ''), 'content': out})


def _summary(name, out):
    if name in ('search', 'follow_links'):
        try:
            return [x['id'] for x in json.loads(out)]
        except Exception:
            return out[:120]
    return f'{_tok(out)} tokens'


class FallbackNeeded(Exception):
    pass


def answer(mode, client, model, question, images, cfg, retriever):
    """Run one question in one mode. Returns (result, ids used, trace, fallback flag)."""
    trace = []
    if mode == 'baseline':
        res, used = baseline(client, model, question, images, cfg, trace)
        return res, used, trace, False
    if mode == 'classic':
        res, used = classic(client, model, question, images, cfg, trace, retriever)
        return res, used, trace, False
    try:
        res, used = agentic(client, model, question, images, cfg, trace, retriever)
        return res, used, trace, False
    except (FallbackNeeded, LLMError) as e:
        if isinstance(e, LLMError) and 'tool' not in str(e).lower():
            raise
        _step(trace, 'fallback', str(e)[:200], 'classic')
        res, used = classic(client, model, question, images, cfg, trace, retriever)
        return res, used, trace, True
