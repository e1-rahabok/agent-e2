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

ANSWER = re.compile(r'ANSWER:\s*\**\s*([A-J](?:\s*(?:,|and|&)?\s*[A-J])*)\b', re.I)
OPTION = re.compile(r'^([A-J])\.\s+(.*)$', re.M)
KB_ID = re.compile(r'\b(?:vsphere|guest-os|foundations)/[a-z0-9][a-z0-9/\-]*[a-z0-9]')
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
    m = None
    for m in ANSWER.finditer(reply or ''):
        pass
    if not m:
        return [{'type': 'format', 'hard': True, 'detail': 'No line starting with "ANSWER:".'}]
    letters = sorted(set(re.findall(r'[A-J]', m.group(1).upper())))
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
