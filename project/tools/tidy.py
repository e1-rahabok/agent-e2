"""Undo what a Markdown formatter does to knowledge files, without changing content.

- Table cells padded to equal width → one space each side (padding costs context tokens on every retrieval).
- Separator rows of many dashes → |---|.
- Runs of 3 or more blank lines → one blank line.
- HTML line breaks (<br />) inside table cells → '; '.
- Non-breaking spaces → plain spaces (search splits words on plain spaces only).
    python3 project/tools/tidy.py            # rewrite knowledge/**/*.md in place
    python3 project/tools/tidy.py --check    # list files that would change; exit 1 if any (used by lint)
"""
import glob
import re
import sys


def tidy(text):
    out, fence = [], False
    for line in text.split('\n'):
        if line.startswith('```'):
            fence = not fence
        if not fence and line.startswith('|') and '<br' in line:  # HTML line breaks in a table cell: a formatter's, not Markdown
            line = re.sub(r'(\s*<br\s*/?>\s*)+', '; ', line)
        padded = re.search(r' {2,}\|', line) or re.search(r'\| *-{4,}', line)
        if not fence and line.startswith('|') and line.rstrip().endswith('|') and padded and '\\|' not in line:
            cells = [c.strip() for c in line.strip()[1:-1].split('|')]
            if all(re.fullmatch(r':?-{3,}:?', c) for c in cells):
                line = '|' + '|'.join(':---' if c.startswith(':') else '---' for c in cells) + '|'
            else:
                line = '| ' + ' | '.join(cells) + ' |'
        out.append(line)
    return re.sub(r'\n{4,}', '\n\n', '\n'.join(out)).replace('\u00a0', ' ')


def main():
    check = '--check' in sys.argv
    changed = []
    for f in sorted(glob.glob('knowledge/**/*.md', recursive=True)):
        s = open(f).read()
        t = tidy(s)
        if t != s:
            changed.append(f)
            if not check:
                open(f, 'w').write(t)
    for f in changed:
        print(f)
    return 1 if (check and changed) else 0


if __name__ == '__main__':
    sys.exit(main())
