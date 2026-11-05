"""Renumber benchmark question files: L<level>-<nn>-<slug>.md, nn from 01 per level, in id order.

Run after a question changes level (edit its `level:` first):
    python3 project/tools/renumber_questions.py
The id (4 digits, metadata only) never changes; attachments stay in benchmark/questions/<id>/.
File names and every reference to them in the documents listed in DOCS are updated.
"""
import os
import re
import subprocess
import sys

Q = 'benchmark/questions'
DOCS = ['benchmark/design.md', 'project/author-questions.md', 'project/todo.md']
NAME = re.compile(r'^L\d-\d{2,3}-(.+)\.md$')


def meta(path):
    t = open(path).read().split('\n## Metadata\n')[-1]
    qid = re.search(r'^id: "?(\d+)"?', t, re.M).group(1)
    level = int(re.search(r'^level: (\d+)', t, re.M).group(1))
    title = re.search(r'^title: "?(.*?)"?$', t, re.M).group(1)
    return qid, level, title


def plan():
    rows = []
    for f in sorted(os.listdir(Q)):
        if f.endswith('.md'):
            qid, level, title = meta(os.path.join(Q, f))
            m = NAME.match(f)
            rows.append((level, int(qid), f, m.group(1) if m else f[:-3], title))
    rows.sort()
    out, count = {}, {}
    for level, qid, f, slug, title in rows:
        count[level] = count.get(level, 0) + 1
        out[f] = f'L{level // 100}-{count[level]:02d}-{slug}.md'
    return out


def main():
    m = {a: b for a, b in plan().items() if a != b}
    if not m:
        print('nothing to rename'); return 0
    for a in m:  # two steps, so names can swap
        subprocess.run(['git', 'mv', f'{Q}/{a}', f'{Q}/{a}.tmp'], check=True)
    for a, b in m.items():
        subprocess.run(['git', 'mv', f'{Q}/{a}.tmp', f'{Q}/{b}'], check=True)
    pre = {re.match(r'L\d-\d+', a).group(0): re.match(r'L\d-\d+', b).group(0) for a, b in m.items() if NAME.match(a)}
    pat = re.compile('|'.join(sorted(map(re.escape, list(m) + list(pre)), key=len, reverse=True)) + r'(?![\w-])' if pre else
                     '|'.join(sorted(map(re.escape, m), key=len, reverse=True)))
    for d in DOCS:
        t = open(d).read()
        u = re.sub(r'(?<![\w-])(?:' + pat.pattern + ')', lambda x: m.get(x.group(0), pre.get(x.group(0), x.group(0))), t)
        if u != t:
            open(d, 'w').write(u); print('updated', d)
    print(f'renamed {len(m)} files')
    return 0


if __name__ == '__main__':
    sys.exit(main())
