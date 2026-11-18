"""One clarifying round (MISSION.md, section 5, Ways to ask; author, 2026-11-09).

A question that makes sense is answered at once. Agent E2 asks first only when:
  - the question is odd or illogical: it names the wrong premise and asks what problem the user saw;
  - the text and an attachment disagree;
  - one missing fact (object, layer, interval, version) changes the answer.
At most one round: after the user replies, it answers, stating any remaining assumption first.
The benchmark runs single-turn kinds (choice, open) and never offers the round.
"""
import re

MAX_QUESTIONS = 3

ASK_RULE = (
    '\nClarifying: you may ask the user once before answering, and only when one of these holds:\n'
    '- the question is odd or illogical: name the wrong premise, then ask what problem the user saw;\n'
    '- the text and an attachment disagree (for example the text says one metric and the screenshot shows another);\n'
    '- one missing fact changes the answer: which object (VM, ESXi, cluster), which layer (Guest OS or VM), which interval, which version;\n'
    '- a term the user wrote has several meanings (a note marked Ambiguous lists them), the meanings lead to different answers, and neither the question nor an attachment tells which: ask "Do you mean A, B or C?".\n'
    'Answering is the default; asking is the exception. A question that makes sense is answered without asking why. Never ask what the knowledge base or an attachment already answers. When one meaning is clearly the most likely, answer it, name it in the first sentence, and add one line for the other meaning.\n'
    'To ask, reply with a first line "CLARIFY:" followed by at most 3 numbered questions, each ending with "because" and the reason. '
    'Write nothing else. Otherwise answer, and state any assumption in the first sentence.\n')

FINAL_RULE = ('\nYou already asked the user once, and their reply is in the question. Do not ask again. '
              'Answer now; state any remaining assumption in the first sentence.\n')

CLARIFY = re.compile(r'^\s*\**CLARIFY:?\**\s*', re.I)
ITEM = re.compile(r'^\s*(?:\d+[.)]|[-*])\s+(.*\S)')


def parse(reply):
    """Questions when the reply asks for clarification, else None. At most MAX_QUESTIONS are kept."""
    if not reply or not CLARIFY.match(reply):
        return None
    body = CLARIFY.sub('', reply, count=1)
    items = [m.group(1) for m in map(ITEM.match, body.split('\n')) if m]
    if not items and body.strip():
        items = [body.strip()]
    return items[:MAX_QUESTIONS] or None


def joined(question, asked, reply):
    """The second round's question: the original, what was asked, what the user replied."""
    return f'{question}\n\nYou asked the user:\n{asked}\n\nThe user replied:\n{reply}'
