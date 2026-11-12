"""Coverage of the question set against the blueprint (benchmark/design.md, section 3).
Run: python3 project/tools/coverage.py      Prints each count with its target; a line marked << is below target.
Counts the questions that run (status draft or reviewed). Lint checks each file; this checks the set.
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

TOTAL = 150
LEVEL = {100: 5, 200: 15, 300: 40, 400: 90}
LEVEL_ANSWER = {(100, 'deterministic'): 5, (100, 'judged'): 0, (200, 'deterministic'): 11, (200, 'judged'): 4,
                (300, 'deterministic'): 26, (300, 'judged'): 14, (400, 'deterministic'): 48, (400, 'judged'): 42}
ANSWER = {'deterministic': 90, 'judged': 60}
INPUT = {'text': 114, 'table': 35, 'screenshot': 1}
TASK = {'troubleshoot': 45, 'read-metric': 35, 'decide-capacity': 30, 'explain-mechanism': 25, 'judge-setting': 15}
TECHNOLOGY = {'cpu': 40, 'memory': 35, 'storage': 28, 'network': 20, 'system': 30}   # touched, at least
GUEST_OS = 20                                                                         # product windows or linux, at least
MISCONCEPTION_EACH = 5
SAME_NAME = 8
OBJECT = {'vm': 45, 'esxi': 30, 'cluster': 15, 'datastore': 8, 'guest-os': 20, 'resource-pool': 4, 'network': 8}
TOOL = {'vcenter': 30, 'vcf-operations': 25, 'esxtop': 10, 'guest-os-tools': 10}
FLOW = 15
RUNS = ('draft', 'reviewed')


def load():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'benchmark', 'questions', '*.md'))):
        fm, _ = split(f)
        out.append((os.path.basename(f), fm or {}))
    return out


def line(name, n, target, at_least=True, width=34):
    flag = '' if (n >= target if at_least else n == target) else '  <<'
    return f'  {name:<{width}} {n:>4} / {target}{flag}'


def main():
    qs = load()
    tags = yaml.safe_load(open(os.path.join(ROOT, 'project', 'tools', 'tags.yaml')))
    status = collections.Counter(fm.get('status') for _, fm in qs)
    run = [(f, fm) for f, fm in qs if fm.get('status') in RUNS]
    print(f'Questions that run: {len(run)} / {TOTAL}   (status: {dict(status)})')
    c = collections.Counter(fm.get('level') for _, fm in run)
    print('Level (exact):'); [print(line(str(k), c[k], v, False)) for k, v in LEVEL.items()]
    c = collections.Counter((fm.get('level'), fm.get('answer_type')) for _, fm in run)
    print('Level x answer type (within 2):')
    for k, v in LEVEL_ANSWER.items():
        print(f'  {k[0]} {k[1]:<20} {c[k]:>4} / {v}' + ('' if abs(c[k] - v) <= 2 else '  <<'))
    c = collections.Counter(fm.get('answer_type') for _, fm in run)
    print('Answer type:'); [print(line(k, c[k], v, False)) for k, v in ANSWER.items()]
    c = collections.Counter(x for _, fm in run for x in (fm.get('input') or []))
    print('Input (questions that include it):')
    print(line('text only', sum(1 for _, fm in run if (fm.get('input') or ['text']) == ['text']), INPUT['text'], False))
    print(line('table', c['table'], INPUT['table'], False)); print(line('screenshot', c['screenshot'], INPUT['screenshot'], False))
    c = collections.Counter(fm.get('task') for _, fm in run)
    print('Task (within 2):')
    for k, v in TASK.items():
        print(f'  {k:<34} {c[k]:>4} / {v}' + ('' if abs(c[k] - v) <= 2 else '  <<'))
    c = collections.Counter(x for _, fm in run for x in (fm.get('technology') or []))
    print('Technology touched (at least):'); [print(line(k, c[k], v)) for k, v in TECHNOLOGY.items()]
    print(line('Guest OS layer (windows, linux)', sum(1 for _, fm in run if {'windows', 'linux'} & set(fm.get('product') or [])), GUEST_OS))
    c = collections.Counter(x for _, fm in run for x in (fm.get('misconception_type') or []))
    print('Misconception type (at least):')
    for k in tags['misconception_type']:
        print(line(k, c[k], SAME_NAME if k == 'same-name-other-object' else MISCONCEPTION_EACH))
    c = collections.Counter(x for _, fm in run for x in (fm.get('object') or []))
    print('Object (at least):'); [print(line(k, c[k], v)) for k, v in OBJECT.items()]
    c = collections.Counter(x for _, fm in run for x in (fm.get('tool') or []))
    print('Tool (at least):'); [print(line(k, c[k], v)) for k, v in TOOL.items()]
    n = sum(1 for _, fm in run if any('/troubleshooting/' in k for k in fm.get('knowledge') or []))
    print('Other:'); print(line('follows a troubleshooting flow', n, FLOW))
    c = collections.Counter(fm.get('origin') for _, fm in run)
    print(f'Origin: {dict(c)}')
    missing = [f for f, fm in run if not all(fm.get(k) for k in ('object', 'tool', 'knowledge_main'))
               or ('misconception_type' not in fm and fm.get('level', 0) >= 300)]
    print(f'Missing coverage tags (object, tool, knowledge_main; misconception_type at Level 300-400): {len(missing)}')
    for f in missing:
        print('  ' + f)


if __name__ == '__main__':
    main()
