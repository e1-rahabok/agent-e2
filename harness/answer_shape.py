"""The shape of an open answer, chosen by what the question asks (plan, 2026-11-24).

One fixed shape (conclusion, mechanism, what to check next) made every answer long: a question on what a metric measures
got the page's figures and a drill-down it did not ask for. The shape now follows the question:
  - explain: what it is, what it measures or how it works, at mechanism depth. No page figures, no next steps.
  - advise: the setting or value first, then the reason and the trade-off.
  - diagnose: a verdict, a cause or a next step was asked: conclusion, evidence and mechanism, then what to check next.
  - general: none of the above is clear: only what is asked; next steps only when a verdict, cause or next step is asked.
Code reads the user's own words first (the caller's bare question, never the facts or rules added to it, whose words such
as "cause" or "next" would match); when code cannot tell, the case's kind from stage 1 decides; else general.
"""
import re

CLOSE = ' If the information available does not settle the question, say so instead of guessing.'
# The open-answer format of answer_modes.py, which each shape replaces; the chat prompts add their rules after it.
OPEN_FORMAT = ('Answer in plain text, at most 250 words. Give the conclusion first, then the mechanism and the reason, '
               'then what to check next.' + CLOSE)
FORMATS = {
    'explain': ('Answer in plain text, at most 250 words, and only what is asked: what it is, what it measures or how it '
                'works, at mechanism depth, with what it leaves out when that changes how it is read. Stop there: no '
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
# The question asks for a verdict, a cause or a next step.
DIAGNOSE = re.compile(
    r'\b(?:check next|what next|next step|should I|do I need|need (?:more|to add)|is (?:it|this|that|there) (?:a )?(?:problem|'
    r'ok|okay|normal|bad|healthy|fine|enough)|a problem|healthy|performing|suffer\w*|how many more|can (?:it|this \w+|the \w+) '
    r'take|root cause|the cause|caus\w+|wrong|worst|why (?:did|is|was|are|were|does|do) .{0,60}?\b(?:drop\w*|ris\w+|spik\w+|'
    r'high|low|slow\w*|fall\w*|fell|worse|declin\w*|dip\w*|degrad\w*|chang\w*|improv\w*|mov\w*|red|orange|yellow|clos\w+|'
    r'open\w*|full)\b)', re.I)
# The question asks what something is, means or how it works.
EXPLAIN = re.compile(r'^\s*(?:what (?:does|do|is|are)|what\'s|how (?:does|do|is|are)|why (?:does|do|is|are)|explain|define|'
                     r'(?:the )?meaning of|(?:the )?difference between)\b', re.I)
ADVISE = re.compile(r'^\s*(?:what (?:value|setting|size)|how (?:should|do) I (?:set|size|configure))\b', re.I)
BY_KIND = {'how-it-works': 'explain', 'metric-meaning': 'explain', 'term-meaning': 'explain', 'what-to-set': 'advise',
           'health-check': 'diagnose', 'troubleshooting': 'diagnose', 'decision-tree': 'diagnose'}


def by_code(question):
    """The shape the user's own words ask for, or None when they do not say."""
    q = str(question or '').strip()
    if ADVISE.search(q):  # "How should I size ..." before the verdict words ("should I")
        return 'advise'
    if DIAGNOSE.search(q):
        return 'diagnose'
    if EXPLAIN.search(q):
        return 'explain'
    return None


def choose(shape, case):
    """The code's shape when it has one, else the case's kind, else general."""
    return shape or BY_KIND.get((case or {}).get('kind')) or 'general'
