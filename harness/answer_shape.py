"""What a question asks, read by the model, before anything else: the answer's shape and whether it needs the page.

One fixed shape (conclusion, mechanism, what to check next) made every answer long: a question on what a metric measures
got the page's figures and a drill-down it did not ask for. The shape now follows the question:
  - explain: what it is, what it measures, what it includes or leaves out, or how it works. No page figures, no next steps.
  - advise: the setting or value first, then the reason and the trade-off.
  - diagnose: a verdict, a cause or a next step was asked: conclusion, evidence and mechanism, then what to check next.
  - general: none of the above is clear: only what is asked; next steps only when a verdict, cause or next step is asked.
And a question asked on a PCM page either needs the page's values (what happened to this object, why its score moved) or
is about how a score works in general, the same answer on any object (page_values false: no opening, no figures).

The model decides both, in one call at temperature 0 on the user's bare question (never the facts and rules added to it).
Code used to decide with keyword patterns; each new wording needed a new pattern ("What metrics are omitted from Cluster
Performance?" matched none, so it got the page's drop and next steps), and a pattern cannot tell "What is the worst
sub-metric?" from "What is Cluster Risk?" (plan, 2026-11-24). Measured on benchmark/runner/screen_answer_check.py.
When the reply is unreadable: the page's values are kept (an answer can ignore a figure it has, not use one it lacks) and
the case's kind from stage 1 decides the shape (choose).
"""
import json
import re

CLOSE = ' If the information available does not settle the question, say so instead of guessing.'
# The open-answer format of answer_modes.py, which each shape replaces; the chat prompts add their rules after it.
OPEN_FORMAT = ('Answer in plain text, at most 250 words. Give the conclusion first, then the mechanism and the reason, '
               'then what to check next.' + CLOSE)
FORMATS = {
    'explain': ('Answer in plain text, at most 250 words, and only what is asked. When it asks which items (which metrics '
                'a score uses, omits or leaves out), list them first, one line each with its reason, from the file of the '
                'score asked about. Otherwise say what it is, what it measures or how it works, at mechanism depth, with '
                'what it leaves out when that changes how it is read. Stop there: no '
                'figures from the page unless the question asks for them, no next steps, no drill-down, no closing summary.'
                + CLOSE),
    'advise': ('Answer in plain text, at most 250 words. Give the setting or the value first, then the reason and the '
               'trade-off. No next steps unless the question asks for them.' + CLOSE),
    'diagnose': ('Answer in plain text, at most 250 words. Give the conclusion first, then the evidence, the mechanism and the '
                 'reason, then what to check next.' + CLOSE),
    'general': ('Answer in plain text, at most 250 words, and only what is asked. Give the conclusion first; add the mechanism '
                'and the reason when they change how the answer is read. Say what to check next only when the question asks '
                'for a verdict, a cause or a next step.' + CLOSE),
}
BY_KIND = {'how-it-works': 'explain', 'metric-meaning': 'explain', 'term-meaning': 'explain', 'what-to-set': 'advise',
           'health-check': 'diagnose', 'troubleshooting': 'diagnose', 'decision-tree': 'diagnose'}


def choose(shape, case):
    """The code's shape when it has one, else the case's kind, else general."""
    return shape or BY_KIND.get((case or {}).get('kind')) or 'general'


SHAPES = tuple(FORMATS)
RULE = (
    'A person typed the question below while looking at a monitoring page of one object (a cluster, an ESXi host or a VM): '
    'its scores over a time window. Do not answer it. Decide two things.\n'
    '1. "page_values": does a correct answer need the values on this page?\n'
    '- true: it asks about this object or this window: what happened, why a score moved, what pulls it down, what is worst '
    'or wrong, whether a value is a problem, what to check next, whether the object can take more VMs; or it names a time, '
    'a figure, "now", or this cluster, host or VM.\n'
    '- false: it asks how a score or metric works in general: what it measures, its formula, what it includes or leaves '
    'out and why, its limits or thresholds, why it is designed so. The same answer would be right on any object.\n'
    '2. "shape":\n'
    '- "explain": what something is, measures or includes, what it leaves out, how it works, or why it is designed so.\n'
    '- "advise": which value, setting or size to use.\n'
    '- "diagnose": a verdict, a cause or a next step for this object.\n'
    '- "general": none of these.\n'
    'Reply with JSON only, nothing else: {"page_values": true or false, "shape": "explain", "advise", "diagnose" or "general"}')
JSON = re.compile(r'\{[^{}]*\}')


def prompt(question, earlier=()):
    """The question, after the earlier questions of its topic when it continues one: a follow-up ("Why?", "Simpler.")
    asks about what they asked."""
    if not earlier:
        return f'Question: {question}'
    lines = '\n'.join(f'- {q}' for q in earlier)
    return (f'Earlier questions of this conversation, oldest first; the new question continues them:\n{lines}\n\n'
            f'New question: {question}')


def parse(text):
    """{'page_values': bool, 'shape': str} from the reply, or None when it is not readable."""
    for m in JSON.finditer(text or ''):
        try:
            raw = json.loads(m.group(0))
        except json.JSONDecodeError:
            continue
        if isinstance(raw, dict) and isinstance(raw.get('page_values'), bool) and raw.get('shape') in SHAPES:
            return {'page_values': raw['page_values'], 'shape': raw['shape']}
    return None


def decide(client, model, question, earlier=(), cfg=None, provider_order=None):
    """What the question asks: {'page_values': bool, 'shape': str or None, 'by': 'model' | 'unsure'}. One call at
    temperature 0. Unsure: the page's values are kept and the shape is left to the case's kind (choose)."""
    res = client.chat(model, [{'role': 'system', 'content': RULE}, {'role': 'user', 'content': prompt(question, earlier)}],
                      max_tokens=(cfg or {}).get('case_max_tokens', 1200), deterministic=True, provider_order=provider_order)
    got = parse(res.get('content'))
    return {**got, 'by': 'model'} if got else {'page_values': True, 'shape': None, 'by': 'unsure'}
