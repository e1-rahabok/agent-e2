"""Questions: load, shuffle options, render, parse and score answers.

Only `## Prompt` and attachments are ever shown to the model under test. The answer key
(metadata `answer`, `misconception`; sections `## Expected key points`, `## Likely wrong answer`) is read here
for scoring only: letters by the runner, key points by the judge (judge.py).

Sub-scores (benchmark/design.md, section 3): answer type (deterministic: letters; judged: free text),
input type (text, table, screenshot: from the attachments), level (100, 200, 300, 400).
"""
import base64
import glob
import mimetypes
import os
import re

import yaml

from kb import ROOT
from verify import answer_letters

META = '\n## Metadata\n```yaml\n'
UNSURE = 'Unsure: the information available does not settle this question.'
TABLE_EXT = ('.csv', '.xlsx', '.xls')
IMAGE_EXT = ('.png', '.jpg', '.jpeg', '.webp')
# A prompt links each attachment by its path, e.g. [the attached chart](0004/chart.png), so a reviewer can open it on GitHub.
# The model reads only the link text: the target is stripped, as kb.FILE_LINK does for knowledge links (no token cost).
ATTACH_LINK = re.compile(r'\[([^\]\n]+)\]\((\d{4}/[^)\s]+)\)')
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # 25 written options at most: Unsure takes the next letter (Q199, 2026-11-14: no fixed option count)
OPTION = re.compile(r'^(?:[-*]\s+)?([A-Y])\.\s+(.*)$')  # 'A. text' or '- A. text' (a bullet renders as a list on GitHub)


class Question:
    def __init__(self, path):
        text = open(path).read()
        i = text.rfind(META)
        if i < 0:
            raise ValueError(f'{path}: no ## Metadata section at the end')
        body, fm = text[:i], text[i + len(META):].rstrip().removesuffix('```')
        self.path = path
        self.meta = yaml.safe_load(fm)
        self.id = self.meta['id']
        self.technology = list(self.meta.get('technology') or [])
        self.task = self.meta.get('task', '')
        self.level = self.meta.get('level', '')
        self.answer_type = self.meta.get('answer_type', 'judged')
        self.answer = [str(a) for a in (self.meta.get('answer') or [])]
        self.misconception = [str(a) for a in (self.meta.get('misconception') or [])]
        self.knowledge = list(self.meta.get('knowledge') or [])
        self.knowledge_main = str(self.meta.get('knowledge_main') or '')  # the file that holds the answer or the misconception (Q130)
        self.attachments = [os.path.join(ROOT, 'benchmark', 'questions', a) for a in (self.meta.get('attachments') or [])]
        m = re.search(r'## Prompt\n(.*?)(?=\n## )', body, re.S)
        self.prompt = ATTACH_LINK.sub(r'\1', m.group(1).strip()) if m else ''
        self.tables = self._tables()
        self.stem, self.options, self.footer = self._split_prompt(self.prompt)
        self.key_points = _section(body, 'Expected key points')
        self.likely_wrong = _section(body, 'Likely wrong answer')

    @staticmethod
    def _split_prompt(prompt):
        """Stem, options, footer. Options may be bullets and may be separated by blank lines.
        A line right after an option continues it; after a blank line, a line that is not an option starts the footer."""
        stem, options, footer, state, blank = [], [], [], 'stem', False
        for line in prompt.split('\n'):
            m = OPTION.match(line.strip())
            if m and state in ('stem', 'opts'):
                options.append([m.group(1), m.group(2)])
                state, blank = 'opts', False
            elif state == 'opts' and not line.strip():
                blank = True
            elif (state == 'opts' and not blank and not line.strip().endswith(':')
                  and not line.strip().lower().startswith('hint')):
                options[-1][1] += ' ' + line.strip()
            elif state == 'stem':
                stem.append(line)
            else:
                state = 'footer'
                footer.append(line)
        return '\n'.join(stem).strip(), options, '\n'.join(footer).strip()

    @property
    def choice(self):
        """Scored by letters (deterministic) or by the judge (judged)."""
        return self.answer_type == 'deterministic'

    @property
    def scorable(self):
        if self.meta.get('status') in ('awaiting-input', 'retired', 'deferred'):
            return False  # input not supplied yet, retired, or deferred to a later release (screenshot set after 1.0)
        if self.choice:
            return bool(self.options) and bool(self.answer)
        return bool(self.prompt) and bool(self.key_points)

    @property
    def input_types(self):
        """Input types from the attachments: screenshot (images), table (spreadsheet or CSV), or text alone."""
        types = []
        if self.has_tables:
            types.append('table')
        if self.has_images:
            types.append('screenshot')
        return types or ['text']

    @property
    def has_tables(self):
        return any(a.lower().endswith(TABLE_EXT) for a in self.attachments)

    @property
    def has_images(self):
        return any(a.lower().endswith(IMAGE_EXT) for a in self.attachments)

    def _tables(self):
        """CSV attachments as text, appended to the prompt: '<file name>:' then the CSV in a fence.
        1.0 tables are small (benchmark/design.md, section 13.1), so they are read in the context; a table tool is after 1.0."""
        out = []
        for a in self.attachments:
            if a.lower().endswith('.csv') and os.path.exists(a):
                out.append(f'Attachment {os.path.basename(a)}:\n```csv\n{open(a, encoding="utf-8-sig").read().strip()}\n```')
        return '\n\n'.join(out)

    def open_text(self):
        """The prompt as written, then its tables."""
        return self.prompt + ('\n\n' + self.tables if self.tables else '')

    def stem_text(self):
        """The question without its options, then its tables: what an operator would type (retrieval check, --no-options)."""
        return self.stem + ('\n\n' + self.tables if self.tables else '')

    def render(self, rng):
        """Shuffle options, append Unsure, return (text, map shown_letter -> original).

        No "Not covered" option (author, Q038, 2026-11-05): the system answers from the knowledge base first
        and from the model's own knowledge where the knowledge base is silent."""
        opts = self.options[:]
        rng.shuffle(opts)
        letters = LETTERS
        mapping, lines = {}, []
        for i, (orig, text) in enumerate(opts):
            mapping[letters[i]] = orig
            lines.append(f'{letters[i]}. {text}')
        un = letters[len(opts)]
        mapping[un] = 'UN'
        lines.append(f'{un}. {UNSURE}')
        parts = [self.stem] + (['', self.tables] if self.tables else []) + ['', '\n'.join(lines)]
        if self.footer:
            parts += ['', self.footer]
        # Same instruction for every question: the number of correct options is never revealed.
        parts += ['', 'Choose all the correct options. There can be more than one.']
        return '\n'.join(parts), mapping

    def image_parts(self):
        out = []
        for a in self.attachments:
            if not a.lower().endswith(IMAGE_EXT):
                continue  # tables go in the text (self.tables)
            mime = mimetypes.guess_type(a)[0] or 'image/png'
            data = base64.b64encode(open(a, 'rb').read()).decode()
            out.append({'type': 'image_url', 'image_url': {'url': f'data:{mime};base64,{data}'}})
        return out


def _section(body, name):
    m = re.search(rf'^## {re.escape(name)}\n(.*?)(?=^## |\Z)', body, re.S | re.M)
    return m.group(1).strip() if m else ''


def load(pattern=None):
    files = sorted(glob.glob(os.path.join(ROOT, 'benchmark', 'questions', '**', '*.md'), recursive=True))
    questions = [Question(f) for f in files]
    if pattern:
        keep = [p.strip() for p in pattern.split(',')]
        questions = [c for c in questions if any(k == c.id or k in os.path.basename(c.path) for k in keep)]
    return questions


def parse(text, mapping):
    """Return the original letters chosen, or None when the answer cannot be parsed."""
    letters = answer_letters(text)
    if not letters:
        return None
    shown = set(letters)
    if not shown or not shown <= set(mapping):
        return None
    return sorted(mapping[s] for s in shown)


def score(question, picked):
    """Exact match, partial credit, misconception picked, Unsure (benchmark/design.md, section 7).

    Unsure counts only when chosen alone; Unsure mixed with other letters is a hedge and scores as wrong.
    An unparseable answer scores as wrong: the user would get no usable answer.
    """
    if picked is None:
        return {'exact': 0, 'partial': 0.0, 'misconception': 0, 'unsure': 0, 'parse_ok': 0}
    correct, chosen = set(question.answer), set(picked)
    unsure = int(chosen == {'UN'})
    exact = int(chosen == correct)
    hits, wrong = len(correct & chosen), len(chosen - correct)
    return {
        'exact': exact,
        'partial': round(max(0, hits - wrong) / len(correct), 3),
        'misconception': int(bool(chosen & set(question.misconception))),
        'unsure': unsure,
        'parse_ok': 1,
    }
