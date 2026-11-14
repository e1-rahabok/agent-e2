"""Answer modes: baseline (no knowledge base), classic RAG, agentic (the agent loop, agent.py).

Classic and agentic replies pass the answer verifier (verify.py); a hard issue gets one repair turn.
Classic context carries catalog facts for the files it holds; agentic mode adds the catalog, calculate and flow tools.
Two answer kinds: choice (multiple-choice letters, verified) and open (free-text conversation answer, not verified:
the verifier checks letter format only). The retrieval and tools are the same for both.
"""
import json
import re

import catalog
import clarify
import terms
import verify
import web
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
    '- For a troubleshooting question, call flow on the matching troubleshooting file and follow its steps in order.\n'
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


TROUBLESHOOT = re.compile(r'\b(slow|troubleshoot\w*|what (do|should|would) (you|i|we) check|root cause|cause[sd]?|why (is|are|does|do)|'
                          r'complain\w*|drops?|dropped|fail\w*|spike\w*|high|degrad\w*)\b', re.I)


def classic_context(retriever, question, cfg, budget=None):
    """One fixed retrieval pass: search, expand same_name and related, fit to budget (default cfg context_tokens).
    Also the agent's first lookup when it starts primed (agent.py, cfg agent_seed_tokens)."""
    matched = terms.match(question) if cfg.get('term_map') else []
    hits = retriever.search(terms.query(question, matched), k=cfg['classic_k'])
    ids = [h['id'] for h in hits]
    if cfg.get('route_troubleshooting') and TROUBLESHOOT.search(question):
        flows = [h for h in retriever.search(question, filters={'retriever_guide': 'troubleshooting'}, k=2, min_hits=1)
                 if retriever.docs.get(h['id']) and retriever.docs[h['id']].meta.get('retriever_guide') == 'troubleshooting']
        for h in reversed(flows[:1]):
            if h['id'] in ids:
                ids.remove(h['id'])
            ids.insert(0, h['id'])
    pos = cfg.get('term_map_position', 1)
    for f in reversed(terms.files(matched, retriever.docs, cfg.get('term_map_files', 2))):
        if f in ids:
            ids.remove(f)
        ids.insert(min(pos, len(ids)), f)
    for h in hits[:2]:
        links = retriever.links(h['id'], 'same_name') + retriever.links(h['id'], 'related')[:2]
        if cfg.get('expand_derive'):
            links += retriever.links(h['id'], 'internal_derive')[:cfg.get('expand_derive_n', 3)]
        for link in links:
            if link['id'] in retriever.docs and link['id'] not in ids:
                ids.append(link['id'])
    budget, parts, used = budget or cfg['context_tokens'], [], []
    notes = terms.block(matched)
    if notes:
        parts.append(notes)
        budget -= _tok(notes)
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
    pages = web.gather(question, cfg['web']) if (cfg.get('web') or {}).get('enabled') else []
    if pages:
        _step(trace, 'web', [p['url'] for p in pages], [p.get('error') or f"{_tok(p['text'])} tokens" for p in pages])
    pages_text = ('\n\n' + web.block(pages)) if pages else ''
    msgs = [{'role': 'system', 'content': PROMPTS[kind]['kb']},
            _user(f'Knowledge base:\n{context}{pages_text}\n\nQuestion:\n{question}', images)]
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


CONSENSUS_MODES = ('classic', 'agentic')  # the shipped modes; baseline and web stay one sample: they measure the model alone


def answer(mode, client, model, question, images, cfg, retriever, kind='choice'):
    """Run one question in one mode. kind: choice (letters) or open (free text).
    With cfg consensus_samples n > 1 (choice questions, classic and agentic mode): n samples; the letters stand only
    when every sample gives the same set, otherwise the answer is Unsure (harness/README.md, section Consensus).
    Returns (result, ids used, trace, fallback flag)."""
    n = cfg.get('consensus_samples') or 1
    if n > 1 and kind == 'choice' and mode in CONSENSUS_MODES:
        return _consensus(n, mode, client, model, question, images, cfg, retriever)
    return _answer_once(mode, client, model, question, images, cfg, retriever, kind)


def _consensus(n, mode, client, model, question, images, cfg, retriever):
    """Up to n samples, stopped at the first disagreement or Unsure: unanimous letters stand, anything else is Unsure.

    Why: on the 2026-11-13 round, 55-75% of the confident-wrong multiple-choice answers in knowledge base modes were
    partly right, and the same question got different letters in different runs. Disagreement between samples marks
    the questions the model does not know; the Unsure rule in the prompt alone did not (Unsure 1-6% of answers).
    """
    _, unsure, _ = verify.options(question)
    trace, used, fallback, first, first_letters = [], [], False, None, None
    for i in range(n):
        res, ids, tr, fb = _answer_once(mode, client, model, question, images, cfg, retriever, 'choice')
        for s in tr:
            s['sample'] = i + 1
        trace += tr
        used += [x for x in ids if x not in used]
        fallback = fallback or fb
        letters = sorted(set(verify.answer_letters(res.get('content') or '') or []))
        if first is None:
            first, first_letters = res, letters
        if not letters or letters != first_letters or (unsure and letters == [unsure]):
            break
    else:
        _step(trace, 'consensus', n, f'agreed: {",".join(first_letters)}')
        return first, used, trace, fallback
    if not unsure:  # no Unsure option to fall back to: keep the first answer, flag it
        _step(trace, 'consensus', n, 'disagreed; no Unsure option, first answer kept')
        return first, used, trace, fallback
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
    return out, used, trace, fallback


def _answer_once(mode, client, model, question, images, cfg, retriever, kind='choice'):
    trace = []
    if mode == 'baseline':
        res, used = baseline(client, model, question, images, cfg, trace, kind)
        return res, used, trace, False
    if mode == 'classic':
        res, used = classic(client, model, question, images, cfg, trace, retriever, kind)
        return res, used, trace, False
    if mode == 'web':
        res, used = agent.web_only(client, model, question, images, cfg, trace, retriever, kind)
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


# The agent loop lives in agent.py, which imports the prompts and helpers above; so it is imported last.
import agent  # noqa: E402
from agent import TOOLS, TOOL_NAMES, FallbackNeeded  # noqa: E402,F401  (re-exported for the runner)
