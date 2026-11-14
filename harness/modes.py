"""Answer modes: Agent E2 (the neuro-symbolic expert system, agent.py), and the two benchmark references:
baseline (the model alone, no knowledge base) and web (the frontier reference: the model alone with web search, as a
user meets it). Agent E2 replies pass the answer verifier (verify.py); a hard issue gets one repair turn.
Two answer kinds: choice (multiple-choice letters, verified) and open (free text); chat and chat_final are the
conversation kinds of the shipped assistant (clarify.py).
"""
import json
import re

import clarify
import verify
import web

FORMAT = ('Reply with exactly two lines and nothing else:\n'
          'ANSWER: <letter or letters, comma separated>\n'
          'REASON: <one sentence>')

UNSURE_RULE = ('A wrong answer is worse than Unsure: an operator would act on it. Do not guess. '
               'If you cannot decide every option with certainty, choose only the Unsure option.\n')

SYSTEM_BASE = ('You are an expert on VMware vSphere and VCF metrics. Answer the multiple-choice question.\n'
               + UNSURE_RULE + FORMAT)

SYSTEM_KB = (
    'You answer questions about VMware vSphere and VCF metrics. Use the knowledge base text provided to you first.\n'
    'Rules:\n'
    '- Treat the knowledge base as the source of truth, even when it contradicts what you believe about IT in general.\n'
    '- Where the knowledge base and your own knowledge differ, the knowledge base wins.\n'
    '- Where the knowledge base is silent, use your own knowledge, and say in the reason which part comes from it.\n'
    '- Prefer mechanism and reason over definitions. Watch for metrics with the same name on different objects.\n'
    '- Quote a threshold only when the knowledge base states it.\n'
    '- If neither the knowledge base nor your own knowledge settles every option, choose only the Unsure option.\n'
    + UNSURE_RULE + FORMAT)

OPEN_FORMAT = ('Answer in plain text, at most 250 words. Give the conclusion first, then the mechanism and the reason, '
               'then what to check next. If the information available does not settle the question, say so instead of guessing.')

OPEN_RULE = 'A wrong answer is worse than saying the question is not settled: an operator would act on it. Do not guess.\n'


def _open(system):
    """Turn a multiple-choice system prompt into the open-answer one: same rules, no options."""
    return (system.replace('Answer the multiple-choice question.\n', 'Answer the question.\n')
            .replace('settles every option, choose only the Unsure option.', 'settles the question, say so.')
            .replace('say in the reason which part', 'say which part')
            .replace(UNSURE_RULE, OPEN_RULE).replace(FORMAT, OPEN_FORMAT))


PROMPTS = {
    'choice': {'base': SYSTEM_BASE, 'kb': SYSTEM_KB, 'format': FORMAT},
    'open': {'base': _open(SYSTEM_BASE), 'kb': _open(SYSTEM_KB), 'format': OPEN_FORMAT},
}
# Conversation kinds (the shipped assistant, harness/clarify.py): 'chat' may ask once; 'chat_final' must answer.
PROMPTS['chat'] = {k: v + clarify.ASK_RULE for k, v in PROMPTS['open'].items()}
PROMPTS['chat_final'] = {k: v + clarify.FINAL_RULE for k, v in PROMPTS['open'].items()}



def _user(text, images):
    if not images:
        return {'role': 'user', 'content': text}
    return {'role': 'user', 'content': [{'type': 'text', 'text': text}] + images}


def _tok(text):
    return len(text) // 4


def msgs_tokens(msgs, cfg):
    """Estimated prompt size of a conversation: text at 4 characters per token, each image at cfg image_tokens."""
    n = 0
    for m in msgs:
        c = m.get('content')
        if isinstance(c, str):
            n += _tok(c)
        elif isinstance(c, list):
            for part in c:
                n += _tok(part.get('text', '')) if part.get('type') == 'text' else cfg.get('image_tokens', 1500)
        for tc in m.get('tool_calls') or []:
            n += _tok(json.dumps(tc))
    return n


def over_window(msgs, cfg):
    """True when the prompt plus the answer budget would not fit the deployed context window (cfg context_window)."""
    window = cfg.get('context_window')
    return bool(window) and msgs_tokens(msgs, cfg) + cfg['max_tokens'] > window


def _step(trace, action, inp, out, res=None):
    s = {'step': len(trace) + 1, 'action': action, 'input': inp, 'output': out}
    if res:
        s.update({k: res.get(k) for k in ('prompt_tokens', 'completion_tokens', 'latency', 'provider')})
    trace.append(s)


def baseline(client, model, question, images, cfg, trace, kind='choice'):
    res = client.chat(model, [{'role': 'system', 'content': PROMPTS[kind]['base']}, _user(question, images)],
                      temperature=cfg['temperature'], max_tokens=cfg['max_tokens'], provider_order=cfg.get('provider_order', {}).get(model))
    _step(trace, 'answer', '', res['content'][:400], res)
    return res, []


def _verified(client, model, msgs, res, question, context, kb_ids, cfg, trace, po):
    """Run the answer verifier. Hard issues get one repair turn; soft issues are only recorded."""
    if not cfg.get('verify', True):
        return res
    issues = verify.check(res.get('content') or '', question, context, kb_ids)
    if not issues:
        return res
    _step(trace, 'verify', '', [f"{i['type']}: {i['detail']}" for i in issues])
    if not any(i['hard'] for i in issues):
        return res
    msgs = msgs + [{'role': 'assistant', 'content': res.get('content') or ''},
                   {'role': 'user', 'content': verify.repair_prompt(issues, FORMAT)}]
    res2 = client.chat(model, msgs, temperature=cfg['temperature'], max_tokens=cfg['max_tokens'], provider_order=po)
    _step(trace, 'repair', '', (res2.get('content') or '')[:400], res2)
    return res2


AGENT = 'agent-e2'                # the shipped system
MODES = ('baseline', AGENT, 'web')  # baseline and web are benchmark references: the model alone, without and with web search
CONSENSUS_MODES = (AGENT,)        # baseline and web stay one sample: they measure the model alone


def answer(mode, client, model, question, images, cfg, retriever, kind='choice'):
    """Run one question in one mode. kind: choice (letters), open (free text), chat or chat_final (conversation).
    With cfg consensus_samples n > 1 (choice questions, Agent E2): n samples of the answer on one reading set; the letters
    stand only when every sample gives the same set, otherwise the answer is Unsure (harness/README.md, section Consensus).
    Returns (result, ids used, trace, fallback flag). The flag stays for the run log's column: Agent E2 has no fallback."""
    if mode not in MODES:
        raise ValueError(f'unknown mode {mode!r}: {", ".join(MODES)}')
    trace = []
    if mode == 'baseline':
        res, used = baseline(client, model, question, images, cfg, trace, kind)
        return res, used, trace, False
    if mode == 'web':
        res, used = web_only(client, model, question, images, cfg, trace, kind)
        return res, used, trace, False
    prep = agent.prepare(client, model, question, images, cfg, trace, retriever, kind, PROMPTS)
    n = cfg.get('consensus_samples') or 1
    if n > 1 and kind == 'choice':
        res, used = _consensus(n, client, model, question, cfg, trace, retriever, prep)
    else:
        res, used = agent.write(client, model, question, cfg, trace, retriever, kind, prep, _verified)
    return res, used, trace, False


def _consensus(n, client, model, question, cfg, trace, retriever, prep):
    """Up to n samples of the answer on the one prepared reading set, stopped at the first disagreement or Unsure:
    unanimous letters stand, anything else is Unsure.

    Why: on the 2026-11-13 round, 55-75% of the confident-wrong multiple-choice answers were partly right, and the same
    question got different letters in different runs. Disagreement between samples marks the questions the model does not
    know; the Unsure rule in the prompt alone did not (Unsure 1-6% of answers). The reading set is shared, so a
    disagreement is doubt in the reasoning, not a different search.
    """
    _, unsure, _ = verify.options(question)
    used, first, first_letters, letters = [], None, None, None
    for i in range(n):
        tr = []
        res, ids = agent.write(client, model, question, cfg, tr, retriever, 'choice', prep, _verified)
        for s in tr:
            s['sample'] = i + 1
        trace += tr
        used += [x for x in ids if x not in used]
        letters = sorted(set(verify.answer_letters(res.get('content') or '') or []))
        if first is None:
            first, first_letters = res, letters
        if not letters or letters != first_letters or (unsure and letters == [unsure]):
            break
    else:
        _step(trace, 'consensus', n, f'agreed: {",".join(first_letters)}')
        return first, used
    if not unsure:  # no Unsure option to fall back to: keep the first answer, flag it
        _step(trace, 'consensus', n, 'disagreed; no Unsure option, first answer kept')
        return first, used
    seen = f'{",".join(first_letters) or "none"} then {",".join(letters) or "none"}'
    if not letters:
        why = 'a sample gave no readable letters'
    elif letters == [unsure] or first_letters == [unsure]:
        why = 'a sample chose Unsure'
    else:
        why = f'the samples disagreed ({seen})'
    _step(trace, 'consensus', n, f'Unsure: {why}')
    first_reason = next((ln.split(':', 1)[1].strip() for ln in (first.get('content') or '').split('\n')
                         if ln.strip().upper().startswith('REASON:')), '')
    out = dict(first)
    # One ANSWER line only: the parser reads the last one, so the first sample's own ANSWER line is not repeated.
    out['content'] = (f'ANSWER: {unsure}\nREASON: Not settled: {why}, so the knowledge read does not decide every option.'
                      + (f' First sample\'s reason: {first_reason[:400]}' if first_reason else ''))
    return out, used


def converse(mode, client, model, turns, images, cfg, retriever):
    """The shipped assistant: one question, or the question, Agent E2's clarifying questions and the user's reply.

    turns: [question] or [question, clarifying reply, user's reply].
    Returns a dict: type 'clarify' (questions) or 'answer' (result), plus ids used, trace and fallback flag.
    """
    if len(turns) >= 3:
        question, kind = clarify.joined(turns[0], turns[1], turns[2]), 'chat_final'
    else:
        question, kind = turns[0], 'chat'
    res, used, trace, fb = answer(mode, client, model, question, images, cfg, retriever, kind)
    asked = clarify.parse(res.get('content') or '')
    if asked and kind == 'chat':
        _step(trace, 'clarify', '', asked)
        return {'type': 'clarify', 'questions': asked, 'result': res, 'used': used, 'trace': trace, 'fallback': fb}
    if asked:  # asked a second time: the rule allows one round; one repair turn to answer
        _step(trace, 'clarify_again', '', asked)
        res, used, trace2, fb = answer(mode, client, model, question + '\n\nAnswer now. Do not ask the user again.',
                                       images, cfg, retriever, 'chat_final')
        trace += trace2
    return {'type': 'answer', 'result': res, 'used': used, 'trace': trace, 'fallback': fb}


# Reference mode `web` (benchmark): what a chat product gives a frontier model when web search is on. The descriptions say
# nothing about when to search: the model decides, as it does for an administrator who types a question.
REF_WEB_TOOLS = [
    {'type': 'function', 'function': {
        'name': 'web_search', 'description': 'Search the web.',
        'parameters': {'type': 'object', 'properties': {'query': {'type': 'string'}}, 'required': ['query']}}},
    {'type': 'function', 'function': {
        'name': 'fetch_url', 'description': 'Fetch a web page.',
        'parameters': {'type': 'object', 'properties': {'url': {'type': 'string'}}, 'required': ['url']}}},
]
TOOL_NAMES = [t['function']['name'] for t in REF_WEB_TOOLS]   # the only tool calls left: the web reference's


def web_only(client, model, question, images, cfg, trace, kind='choice'):
    """Reference mode: the baseline prompt plus web search and page fetch that the model may use or ignore.
    No knowledge base, no instruction to search, the open web (no host list), no answer verifier. Returns (result, [])."""
    wcfg = dict(cfg.get('web') or {})
    wcfg.update({'enabled': True, 'search_hosts': [], 'allow_hosts': []})
    if not web.search_configured(wcfg):
        raise ValueError('mode web needs web.search_backend or web.search_url in the config')
    max_calls = cfg.get('web_max_calls', 5)
    msgs = [{'role': 'system', 'content': PROMPTS[kind]['base']}, _user(question, images)]
    po = cfg.get('provider_order', {}).get(model)
    calls = 0
    while True:
        tools = REF_WEB_TOOLS if calls < max_calls else None
        if tools is None:
            msgs.append({'role': 'user', 'content': 'Answer now.\n' + PROMPTS[kind]['format']})
        res = client.chat(model, msgs, tools=tools, temperature=cfg['temperature'], max_tokens=cfg['max_tokens'], provider_order=po)
        tcs = res['tool_calls'] if tools else []
        if not tcs:
            _step(trace, 'answer', '', (res['content'] or '')[:400], res)
            return res, []
        msgs.append({'role': 'assistant', 'content': res['content'] or None, 'tool_calls': tcs})
        for n, tc in enumerate(tcs):
            calls += 1
            name = tc.get('function', {}).get('name', '')
            raw = tc.get('function', {}).get('arguments') or '{}'
            try:
                args = json.loads(raw) if isinstance(raw, str) else raw
            except json.JSONDecodeError:
                args = {}
            if name == 'web_search':
                out = json.dumps(web.search(str(args.get('query', '')), wcfg), ensure_ascii=False, indent=0)
            elif name == 'fetch_url':
                out = web.block([web.fetch(str(args.get('url', '')), question, wcfg)])
            else:
                out = json.dumps({'error': f'unknown tool {name}'})
            _step(trace, name, args, f'{_tok(out)} tokens', res if n == 0 else None)
            msgs.append({'role': 'tool', 'tool_call_id': tc.get('id', ''), 'content': out})


import agent  # noqa: E402  (agent.py reads PROMPTS and _verified from here at call time)
