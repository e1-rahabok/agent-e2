"""Flow executor: troubleshooting flows from knowledge/**/diagnosis/*.md, served one step at a time.

The markdown file is the single source. Two step formats are read:
  - a '## Checks, in order' section with numbered lines (1. 2. 3. ...), continuation lines kept with their step;
  - '## Step a: <title>' sections (one step per section).
A step that names another step ('step 4', '→ step 2') gets that step number in 'refers_to', so the model can jump.
"""
import re

STEP_LINE = re.compile(r'^(\d+)\.\s+(.*)$')
STEP_HEAD = re.compile(r'^Step\s+([0-9a-z]+)\s*[:.]\s*(.*)$', re.I)
STEP_REF = re.compile(r'\bsteps?\s+(\d+|[a-h])\b', re.I)


def steps_of(doc):
    """Return [(key, text)] for a diagnosis doc, or [] if it has no steps."""
    for head, text in doc.sections:
        if head.lower().startswith('checks'):
            out = []
            for line in text.split('\n')[1:]:
                m = STEP_LINE.match(line.strip())
                if m:
                    out.append([m.group(1), m.group(2).strip()])
                elif out and line.strip() and not line.startswith('## '):
                    out[-1][1] += '\n' + line.rstrip()
            return [tuple(s) for s in out]
    out = []
    for head, text in doc.sections:
        m = STEP_HEAD.match(head)
        if m:
            body = text.split('\n', 1)[1].strip() if '\n' in text else ''
            out.append((m.group(1).lower(), f'{m.group(2).strip()}\n{body}'.strip()))
    return out


def flow_ids(docs):
    return sorted(i for i in docs if '/diagnosis/' in i)


def run(docs, flow_id, step=None):
    """One call of the flow tool. step None: all steps in order. step N: that step and where to go next."""
    d = docs.get(flow_id or '')
    if not d or '/diagnosis/' not in d.id:
        return {'error': f'unknown flow {flow_id!r}', 'flows': {i: docs[i].title for i in flow_ids(docs)}}
    steps = steps_of(d)
    if not steps:
        return {'error': f'{flow_id} has no numbered steps', 'flows': {i: docs[i].title for i in flow_ids(docs)}}
    keys = [k for k, _ in steps]
    if step in (None, '', 'all'):
        return {'flow': d.id, 'title': d.title, 'steps': [f'{k}. {t}' for k, t in steps],
                'rule': 'Work through the steps in order. Do not skip a step whose condition you have not ruled out. '
                        'Read the metric files a step names before deciding it.'}
    k = str(step).strip().lower()
    if k not in keys:
        return {'error': f'no step {step!r} in {flow_id}', 'steps_available': keys}
    i = keys.index(k)
    text = steps[i][1]
    refs = [r.lower() for r in STEP_REF.findall(text) if r.lower() in keys and r.lower() != k]
    return {'flow': d.id, 'title': d.title, 'step': k, 'of': len(steps), 'text': text,
            'next': keys[i + 1] if i + 1 < len(keys) else None, 'refers_to': list(dict.fromkeys(refs)),
            'metrics_to_read': list(d.meta.get('internal_derive') or [])}


def check(docs):
    """Problems for tools/lint.py: diagnosis files without steps, or step references that do not exist."""
    problems = []
    for i in flow_ids(docs):
        steps = steps_of(docs[i])
        if len(steps) < 2:
            problems.append((i, 'diagnosis file needs "## Checks, in order" with numbered steps, or "## Step a:" sections'))
            continue
        keys = {k for k, _ in steps}
        for k, t in steps:
            for r in STEP_REF.findall(t):
                if r.lower() not in keys:
                    problems.append((i, f'step {k} refers to step {r}, which does not exist'))
    return problems
