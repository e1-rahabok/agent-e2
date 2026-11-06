"""Turn file references in the author-facing documents into clickable GitHub links.

A backticked knowledge id (`vsphere/foundations/resource-controls`) becomes [<its # title>](URL).
A backticked repository path that exists (`benchmark/design.md`) becomes [path](URL).
    python3 project/tools/link_refs.py          # rewrite DOCS
    python3 project/tools/link_refs.py --check  # list unlinked references; exit 1 if any (used by lint)
"""
import glob
import os
import re
import subprocess
import sys

BASE = 'https://github.com/e1-rahabok/isvara-2/blob/main/'
DOCS = ['project/author-questions.md', 'project/plan.md', 'MISSION.md', 'benchmark/design.md', 'benchmark/README.md',
        'benchmark/runner/README.md', 'benchmark/models.md']
TICK = re.compile(r'`([\w./-]+)`')
_TRACKED = None


def tracked(path):
    """True when git tracks the file, or a file under the folder: local caches and untracked files are not linked."""
    global _TRACKED
    if _TRACKED is None:
        out = subprocess.run(['git', 'ls-files'], capture_output=True, text=True).stdout.split('\n')
        _TRACKED = set(out)
        for f in out:
            d = os.path.dirname(f)
            while d:
                _TRACKED.add(d)
                d = os.path.dirname(d)
    return path.rstrip('/') in _TRACKED


def target(ref):
    ref = ref.rstrip('/')
    k = f'knowledge/{ref}.md'
    if '/' in ref and os.path.isfile(k):
        m = re.search(r'^# (.+)$', open(k).read(), re.M)
        return (m.group(1).strip() if m else ref), BASE + k
    if '/' in ref and tracked(ref):
        return ref, BASE + ref
    if '/' not in ref and '-' in ref:  # short knowledge name, e.g. `cluster-risk`, when unique
        hits = [h for h in glob.glob(f'knowledge/**/{ref}.md', recursive=True)]
        if len(hits) == 1:
            return target(hits[0][len('knowledge/'):-3])
    return None


FENCE = re.compile(r'(^```.*?^```)', re.M | re.S)  # code blocks are left as they are


def _prose(text, fn):
    parts = FENCE.split(text)
    return ''.join(p if i % 2 else fn(p) for i, p in enumerate(parts))


def rewrite(text):
    return _prose(text, lambda t: TICK.sub(lambda m: (lambda x: f'[{x[0]}]({x[1]})' if x else m.group(0))(target(m.group(1))), t))


def unlinked(path):
    found = []
    _prose(open(path).read(), lambda t: found.extend(m.group(1) for m in TICK.finditer(t) if target(m.group(1))) or t)
    return found


if __name__ == '__main__':
    if '--check' in sys.argv:
        bad = {d: unlinked(d) for d in DOCS}
        for d, refs in bad.items():
            for r in refs: print(f'{d}: `{r}` should be a link (run project/tools/link_refs.py)')
        sys.exit(1 if any(bad.values()) else 0)
    for d in DOCS:
        t = open(d).read(); u = rewrite(t)
        if u != t: open(d, 'w').write(u); print('updated', d)
