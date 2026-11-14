"""What the question set covers (benchmark/design.md, section 3).
Run: python3 project/tools/coverage.py      Prints the count of each tag value; a line marked << has no question.
Counts the questions that run (status draft or reviewed). There are no targets: the set changes as questions are added,
rewritten or retired. A value with no question is a gap to look at. Lint checks each file; this describes the set.
"""
import collections
import glob
import os
import re
import sys

import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'harness'))
from kb import split  # noqa: E402

RUNS = ('draft', 'reviewed')
TASKS = ('troubleshoot', 'read-metric', 'decide-capacity', 'explain-mechanism', 'judge-setting')   # lint.py checks the same five
TECHNOLOGY = ('cpu', 'memory', 'storage', 'network', 'system')


def load():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'benchmark', 'questions', '*.md'))):
        fm, _ = split(f)
        out.append((os.path.basename(f), fm or {}))
    return out


def line(name, n, width=34):
    return f'  {name:<{width}} {n:>4}' + ('' if n else '  <<')


def counts(title, c, values):
    print(title)
    for v in values:
        print(line(str(v), c[v]))


def main():
    qs = load()
    tags = yaml.safe_load(open(os.path.join(ROOT, 'project', 'tools', 'tags.yaml')))
    status = collections.Counter(fm.get('status') for _, fm in qs)
    run = [(f, fm) for f, fm in qs if fm.get('status') in RUNS]
    print(f'Questions that run: {len(run)}   (status: {dict(status)})')
    counts('Level:', collections.Counter(fm.get('level') for _, fm in run), (100, 200, 300, 400))
    counts('Answer type:', collections.Counter(fm.get('answer_type') for _, fm in run), ('deterministic', 'judged'))
    c = collections.Counter((fm.get('level'), fm.get('answer_type')) for _, fm in run)
    print('Level x answer type:')
    for lv in (100, 200, 300, 400):
        print(f'  {lv}  deterministic {c[(lv, "deterministic")]:>4}   judged {c[(lv, "judged")]:>4}')
    c = collections.Counter(x for _, fm in run for x in (fm.get('input') or []))
    print('Input (questions that include it):')
    print(line('text only', sum(1 for _, fm in run if (fm.get('input') or ['text']) == ['text'])))
    print(line('table', c['table'])); print(line('screenshot', c['screenshot']))
    counts('Task:', collections.Counter(fm.get('task') for _, fm in run), TASKS)
    counts('Technology touched:', collections.Counter(x for _, fm in run for x in (fm.get('technology') or [])), TECHNOLOGY)
    print(line('Guest OS layer (windows, linux)', sum(1 for _, fm in run if {'windows', 'linux'} & set(fm.get('product') or []))))
    counts('Misconception type:', collections.Counter(x for _, fm in run for x in (fm.get('misconception_type') or [])), tags['misconception_type'])
    counts('Object:', collections.Counter(x for _, fm in run for x in (fm.get('object') or [])), tags['question_object'])
    counts('Tool:', collections.Counter(x for _, fm in run for x in (fm.get('tool') or [])), [x for x in tags['question_tool'] if x != 'none'])
    n = sum(1 for _, fm in run if any('/troubleshooting/' in k for k in fm.get('knowledge') or []))
    print('Other:'); print(line('follows a troubleshooting flow', n))
    c = collections.Counter(fm.get('origin') for _, fm in run)
    print(f'Origin: {dict(c)}')
    missing = [f for f, fm in run if not all(fm.get(k) for k in ('object', 'tool', 'knowledge_main'))
               or ('misconception_type' not in fm and fm.get('level', 0) >= 300)]
    print(f'Missing coverage tags (object, tool, knowledge_main; misconception_type at Level 300-400): {len(missing)}')
    for f in missing:
        print('  ' + f)


if __name__ == '__main__':
    main()
