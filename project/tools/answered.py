"""List open author questions that have an answer, including answers written on the lines below `- Answer:`.

Usage: python3 project/tools/answered.py
"""
import re

texts = [open(f, encoding='utf-8').read() for f in ['project/author-questions-release-1.0.md', 'project/author-questions-future-release.md']]  # open questions only
for block in [b for text in texts for b in re.split(r'(?=^### Q)', text, flags=re.M)[1:]]:
    m = re.search(r'^- Answer:(.*)\Z', block, re.M | re.S)
    answer = m.group(1).strip() if m else ''
    if answer:
        print(block.splitlines()[0])
        print('  ' + answer.replace('\n', '\n  ') + '\n')
