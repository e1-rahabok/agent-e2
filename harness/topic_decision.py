"""Whether the user's question continues the current topic or starts a new one.

A model call holds no memory: the caller (PCM) keeps the conversation and sends the current topic's earlier turns
(`history`). A context (an object, tab and window) holds topics; a topic holds turns. This module decides whether the new
question belongs to the topic those turns hold. When it does, the turns go to the model and the earlier questions join the
search; when it does not, the question is read alone and the page's opening is shown again.

Order of the decision, first match wins:
  1. user: the user chose (PCM's undo, its New topic button, a suggested question): `topic_choice` new or continue.
  2. first: no earlier turn, so a new topic.
  3. code: the question names nothing the knowledge base holds (no metric file, no term-map row) and points back: a
     word that refers to the earlier turns ("it", "that", "again", "instead", "also"), an opening such as "And", "So",
     "What about", or five words or fewer ("Why?", "Simpler please."). It cannot stand alone, so it continues.
     "This cluster" and "this VM" are not a pointer: they name the page the user is on.
  4. model: anything else may be a new subject or a narrower question on the same one ("Is Co-stop also high on that
     VM?"). One model call at temperature 0 reads the earlier turns and the question.
When unsure (an unreadable reply), it continues: losing the context is the worse mistake, since an answer without it
answers the wrong question; extra context costs only tokens, and the model answers the latest question.
Measured on benchmark/runner/topic_check_pairs.yaml with benchmark/runner/topic_check.py.
"""
import re

import reading_plan
import user_terms

CHOICES = ('auto', 'new', 'continue')

RULE = ('Decide whether the new question continues the earlier conversation or starts a new topic.\n'
        'Test: could a VMware expert answer the new question correctly if they saw it alone, without the earlier '
        'conversation?\n'
        '- No, it needs the earlier turns: it refers to them (it, that, the VM, the host, the drop), or asks about their '
        'answer. It continues.\n'
        '- Yes, but it asks about the same subject: a narrower, wider or related question on the same metric, object or '
        'event. It continues.\n'
        '- Yes, and it asks about a different subject: another metric, another object or another task. New topic.\n'
        '"This cluster", "this VM" or "this page" name the page the user is on, not the earlier conversation.\n'
        'Reply with JSON only, nothing else: {"continues": true} or {"continues": false}')
POINTS_BACK = re.compile(r"\b(?:it|its|that|those|them|they|again|instead|also|too|then|earlier|previous|above|same|"
                         r"simpler|example|explain|elaborate|sure|next)\b|^\s*(?:and|but|so|or|what about|how about|what if)\b", re.I)
SHORT = 5   # words: a question this short cannot carry a subject of its own
JSON = re.compile(r'\{[^{}]*"continues"\s*:\s*(true|false)[^{}]*\}', re.I)


def names_nothing(docs, question):
    """The question names no metric file and no user term."""
    return not reading_plan.anchors(docs, question) and not user_terms.match(question)


def points_back(docs, question):
    """Code's rule: names nothing, and refers back or is too short to stand alone."""
    return names_nothing(docs, question) and (bool(POINTS_BACK.search(question)) or len(question.split()) <= SHORT)


def prompt(history, question):
    turns = '\n\n'.join(f'Question {i}: {t["question"]}\nAnswer {i}: {t["answer"]}' for i, t in enumerate(history, 1))
    return f'Earlier conversation, oldest first:\n\n{turns}\n\nNew question: {question}'


def parse(text):
    m = JSON.search(text or '')
    return None if not m else m.group(1).lower() == 'true'


def decide(client, model, question, history, choice, docs, cfg, provider_order=None):
    """Returns {'continues': bool, 'by': 'user' | 'first' | 'code' | 'model' | 'unsure'}."""
    choice = choice or 'auto'
    if choice not in CHOICES:
        raise ValueError(f'topic_choice must be one of {", ".join(CHOICES)}')
    if choice != 'auto':
        return {'continues': choice == 'continue' and bool(history), 'by': 'user'}
    if not history:
        return {'continues': False, 'by': 'first'}
    if points_back(docs, question):
        return {'continues': True, 'by': 'code'}
    res = client.chat(model, [{'role': 'system', 'content': RULE}, {'role': 'user', 'content': prompt(history, question)}],
                      max_tokens=cfg.get('case_max_tokens', 1200), deterministic=True, provider_order=provider_order)
    got = parse(res.get('content'))
    return {'continues': True, 'by': 'unsure'} if got is None else {'continues': got, 'by': 'model'}
