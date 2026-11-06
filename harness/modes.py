"""Answer modes: baseline (no knowledge base), classic RAG, agentic (the agent loop, agent.py).

Classic and agentic replies pass the answer verifier (verify.py); a hard issue gets one repair turn.
Classic context carries catalog facts for the files it holds; agentic mode adds the catalog, calculate and flow tools.
Two answer kinds: choice (multiple-choice letters, verified) and open (free-text conversation answer, not verified:
the verifier checks letter format only). The retrieval and tools are the same for both.
"""
import json

import catalog
import verify
from llm import LLMError

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

SYSTEM_AGENT = SYSTEM_KB.replace(
    'Use the knowledge base text provided to you first.',
    'Look up the knowledge base with the tools first, before you answer from your own knowledge.') + (
    '\nTool rules:\n'
    '- Your first action must be search or catalog.\n'
    '- Base the knowledge base part of the answer on text returned by read_file, catalog, flow and calculate. Search snippets are not enough.\n'
    '- Before answering about a metric, call follow_links with link_type "same_name" on its file.\n'
    '- For a unit, rollup, statistics level, esxtop field, threshold or object relationship, call catalog. Its values are exact.\n'
    '- For any arithmetic or unit conversion, call calculate. Do not compute in your head.\n'
    '- For a troubleshooting question, call flow on the matching diagnosis file and follow its steps in order.\n'
    '- You have at most {max_calls} tool calls. Then answer.')

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
    'choice': {'base': SYSTEM_BASE, 'kb': SYSTEM_KB, 'agent': SYSTEM_AGENT, 'format': FORMAT},
    'open': {'base': _open(SYSTEM_BASE), 'kb': _open(SYSTEM_KB), 'agent': _open(SYSTEM_AGENT), 'format': OPEN_FORMAT},
}



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


def classic_context(retriever, question, cfg):
    """One fixed retrieval pass: search, expand same_name and related, fit to budget."""
    hits = retriever.search(question, k=cfg['classic_k'])
    ids = [h['id'] for h in hits]
    for h in hits[:2]:
        for link in retriever.links(h['id'], 'same_name') + retriever.links(h['id'], 'related')[:2]:
            if link['id'] in retriever.docs and link['id'] not in ids:
                ids.append(link['id'])
    budget, parts, used = cfg['context_tokens'], [], []
    facts = catalog.get(retriever.docs).facts_for(ids) if cfg.get('catalog_facts', True) else ''
    if facts:
        parts.append(facts)
        budget -= _tok(facts)
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


def classic(client, model, question, images, cfg, trace, retriever, kind='choice'):
    context, used, hits = classic_context(retriever, question, cfg)
    _step(trace, 'search', question[:200], [h['id'] for h in hits])
    _step(trace, 'context', '', used)
    msgs = [{'role': 'system', 'content': PROMPTS[kind]['kb']},
            _user(f'Knowledge base:\n{context}\n\nQuestion:\n{question}', images)]
    if over_window(msgs, cfg):
        _step(trace, 'context_over', cfg.get('context_window'), 'prompt larger than the deployed window')
    po = cfg.get('provider_order', {}).get(model)
    res = client.chat(model, msgs, temperature=cfg['temperature'], max_tokens=cfg['max_tokens'], provider_order=po)
    _step(trace, 'answer', '', res['content'][:400], res)
    if kind == 'choice':
        res = _verified(client, model, msgs, res, question, context, set(retriever.docs), cfg, trace, po)
    return res, used


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


def answer(mode, client, model, question, images, cfg, retriever, kind='choice'):
    """Run one question in one mode. kind: choice (letters) or open (free text).
    Returns (result, ids used, trace, fallback flag)."""
    trace = []
    if mode == 'baseline':
        res, used = baseline(client, model, question, images, cfg, trace, kind)
        return res, used, trace, False
    if mode == 'classic':
        res, used = classic(client, model, question, images, cfg, trace, retriever, kind)
        return res, used, trace, False
    try:
        res, used = agent.agentic(client, model, question, images, cfg, trace, retriever, kind)
        return res, used, trace, False
    except (agent.FallbackNeeded, LLMError) as e:
        if isinstance(e, LLMError) and 'tool' not in str(e).lower():
            raise
        _step(trace, 'fallback', str(e)[:200], 'classic')
        res, used = classic(client, model, question, images, cfg, trace, retriever, kind)
        return res, used, trace, True


# The agent loop lives in agent.py, which imports the prompts and helpers above; so it is imported last.
import agent  # noqa: E402
from agent import TOOLS, TOOL_NAMES, FallbackNeeded  # noqa: E402,F401  (re-exported for the runner)
