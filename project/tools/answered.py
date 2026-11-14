"""List open author questions that have an answer, including answers written on the lines below `- Answer:`.

Usage: python3 project/tools/answered.py
"""
import re

text = open('project/author-questions.md').read().split('\n## Resolved index')[0]  # open questions only; resolved ones are in author-questions-resolved.md
for block in re.split(r'(?=^### Q)', text, flags=re.M)[1:]:
    m = re.search(r'^- Answer:(.*)\Z', block, re.M | re.S)
    answer = m.group(1).strip() if m else ''
    if answer:
        print(block.splitlines()[0])
        print('  ' + answer.replace('\n', '\n  ') + '\n')
