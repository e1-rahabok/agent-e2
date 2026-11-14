"""List open author questions that have an answer, including answers written on the lines below `- Answer:`.

Usage: python3 project/tools/answered.py
"""
import re

texts = [open('project/author-questions.md', encoding='utf-8').read()]  # open questions only; answered ones are in author-questions-resolved.md
for block in [b for text in texts for b in re.split(r'(?=^### Q)', text, flags=re.M)[1:]]:
    m = re.search(r'^- Answer:(.*)\Z', block, re.M | re.S)
    answer = re.split(r'^## ', m.group(1), flags=re.M)[0].strip() if m else ''   # a section heading ends the last entry of a section
    if answer:
        print(block.splitlines()[0])
        print('  ' + answer.replace('\n', '\n  ') + '\n')
