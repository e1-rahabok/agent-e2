"""Answer verifier: checks a model reply before it is returned.

Hard issues trigger one repair turn (the model is told what is wrong and answers again):
  - no ANSWER line, or letters that are not options;
  - Unsure or "Not covered" mixed with other letters (a hedge, scored as wrong).
Soft issues are recorded in the trace only, so reports can measure whether they predict wrong answers
before they are allowed to change an answer:
  - no REASON line;
  - a knowledge-file id in REASON that does not exist;
  - a number with a unit in REASON that appears neither in the question nor in the text the model was given
    (a possible invented threshold).
"""
import re

ANSWER = re.compile(r'ANSWER:[ \t]*([^\n]*)', re.I)
# One letter of a letter list: optional bold or italics around it, then a separator (comma, &, the word and, or a space).
LETTER = re.compile(r'\s*[*_]*([A-J])[*_]*(?![A-Za-z])\s*(?:,|&|\band\b)?', re.I)


def answer_letters(text):
    """Letters of the last ANSWER line, in order of appearance, or None when there is none.

    Reads a list of single letters from the start of the line and stops at the first other word, so 'C and E' is C, E
    (not the letters of 'and'), '**B**, **D**' is B, D, and 'B. Because ...' is B.
    """
    m = None
    for m in ANSWER.finditer(text or ''):
        pass  # last ANSWER line wins (models sometimes draft first)
    if not m:
        return None
    line, pos, out = m.group(1), 0, []
    while True:
        t = LETTER.match(line, pos)
        if not t or t.end() == pos:
            break
        out.append(t.group(1).upper())
        pos = t.end()
    return out or None
OPTION = re.compile(r'^([A-J])\.\s+(.*)$', re.M)
KB_ID = re.compile(r'\b(?:vsphere|guest-os|observability|sp5-framework|vcf-operations)/[a-z0-9][a-z0-9/\-]*[a-z0-9]')
NUMBER = re.compile(r'(?<![\w.,])(\d+(?:\.\d+)?)\s?(%|ms|µs|us|ns|MB/s|MBps|KBps|Mbps|GB|MB|KB|GHz|MHz|seconds|minutes)(?![\w/])')


def options(question):
    """Letters shown in the question, and which letters are Unsure and Not covered."""
    opts = {m.group(1): m.group(2) for m in OPTION.finditer(question or '')}
    unsure = next((k for k, v in opts.items() if v.lower().startswith('unsure')), None)
    nc = next((k for k, v in opts.items() if v.lower().startswith('not covered')), None)
    return opts, unsure, nc


def check(reply, question, context='', kb_ids=None):
    """Return a list of issues: {'type', 'hard', 'detail'}."""
    issues = []
    opts, unsure, nc = options(question)
    found = answer_letters(reply)
    if not found:
        return [{'type': 'format', 'hard': True, 'detail': 'No line starting with "ANSWER:".'}]
    letters = sorted(set(found))
    bad = [x for x in letters if opts and x not in opts]
    if bad:
        issues.append({'type': 'format', 'hard': True, 'detail': f'{", ".join(bad)} is not an option.'})
    for special, name in ((unsure, 'Unsure'), (nc, 'Not covered')):
        if special and special in letters and len(letters) > 1:
            issues.append({'type': 'hedge', 'hard': True,
                           'detail': f'{name} ({special}) must be chosen alone. Choose only {special}, or only the options you are certain of.'})
    reason = next((ln.split(':', 1)[1].strip() for ln in (reply or '').split('\n') if ln.strip().upper().startswith('REASON:')), '')
    if not reason:
        issues.append({'type': 'format', 'hard': False, 'detail': 'No REASON line.'})
    if kb_ids is not None:
        for cited in sorted(set(KB_ID.findall(reason))):
            if cited not in kb_ids:
                issues.append({'type': 'citation', 'hard': False, 'detail': f'{cited} is not a knowledge file.'})
    if context:
        seen = re.sub(r'(?<=\d),(?=\d{3})', '', f'{question}\n{context}')
        for num, unit in NUMBER.findall(re.sub(r'(?<=\d),(?=\d{3})', '', reason)):
            if not re.search(r'(?<![\d.])' + re.escape(num) + r'(?![\d])', seen):
                issues.append({'type': 'ungrounded', 'hard': False, 'detail': f'{num} {unit} is not in the question or the knowledge base text.'})
    return issues


def repair_prompt(issues, fmt):
    lines = [f'- {i["detail"]}' for i in issues if i['hard']]
    return 'Your answer cannot be scored:\n' + '\n'.join(lines) + '\nAnswer again.\n' + fmt
