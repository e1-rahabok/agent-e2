"""Questions: load, shuffle options, render, parse and score answers.

Only `## Prompt` and attachments are ever shown to the model under test. The answer key
(metadata `answer`, `trap`; sections `## Expected key points`, `## Likely wrong answer`) is read here
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

META = '\n## Metadata\n```yaml\n'
UNSURE = 'Unsure: the information available does not settle this question.'
# Scoring that removes the reward for guessing: a wrong answer costs as much as a right one earns.
POINTS = {'exact': 1, 'unsure': 0, 'wrong': -1}
TABLE_EXT = ('.csv', '.xlsx', '.xls')
OPTION = re.compile(r'^(?:[-*]\s+)?([A-H])\.\s+(.*)$')  # 'A. text' or '- A. text' (a bullet renders as a list on GitHub)
ANSWER = re.compile(r'ANSWER:\s*\**\s*([A-J](?:\s*(?:,|and|&)?\s*[A-J])*)\b', re.I)


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
        self.trap = [str(a) for a in (self.meta.get('trap') or [])]
        self.knowledge = list(self.meta.get('knowledge') or [])
        self.attachments = [os.path.join(ROOT, 'benchmark', 'questions', a) for a in (self.meta.get('attachments') or [])]
        m = re.search(r'## Prompt\n(.*?)(?=\n## )', body, re.S)
        self.prompt = m.group(1).strip() if m else ''
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
        if self.meta.get('status') in ('awaiting-input', 'retired'):
            return False  # the author has not supplied the screenshot or table yet, or the question is retired
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
        return any(a.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')) for a in self.attachments)

    def render(self, rng):
        """Shuffle options, append Unsure, return (text, map shown_letter -> original).

        No "Not covered" option (author, Q038, 2026-11-05): the system answers from the knowledge base first
        and from the model's own knowledge where the knowledge base is silent."""
        opts = self.options[:]
        rng.shuffle(opts)
        letters = 'ABCDEFGHIJ'
        mapping, lines = {}, []
        for i, (orig, text) in enumerate(opts):
            mapping[letters[i]] = orig
            lines.append(f'{letters[i]}. {text}')
        un = letters[len(opts)]
        mapping[un] = 'UN'
        lines.append(f'{un}. {UNSURE}')
        parts = [self.stem, '', '\n'.join(lines)]
        if self.footer:
            parts += ['', self.footer]
        # Same instruction for every question: the number of correct options is never revealed.
        parts += ['', 'Choose all the correct options. There can be more than one.']
        return '\n'.join(parts), mapping

    def image_parts(self):
        out = []
        for a in self.attachments:
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
        questions = [c for c in questions if any(k in c.id for k in keep)]
    return questions


def parse(text, mapping):
    """Return the original letters chosen, or None when the answer cannot be parsed."""
    m = None
    for m in ANSWER.finditer(text or ''):
        pass  # last ANSWER line wins (models sometimes draft first)
    if not m:
        return None
    shown = set(re.findall(r'[A-J]', m.group(1).upper()))
    if not shown or not shown <= set(mapping):
        return None
    return sorted(mapping[s] for s in shown)


def score(question, picked):
    """Exact match, partial credit, trap hit, and points: +1 exact, 0 Unsure, -1 anything else.

    Unsure counts only when chosen alone; Unsure mixed with other letters is a hedge and scores as wrong.
    An unparseable answer scores as wrong: the user would get no usable answer.
    """
    if picked is None:
        return {'exact': 0, 'partial': 0.0, 'trap': 0, 'not_covered': 0, 'unsure': 0, 'points': POINTS['wrong'], 'parse_ok': 0}
    correct, chosen = set(question.answer), set(picked)
    unsure = int(chosen == {'UN'})
    exact = int(chosen == correct)
    hits, wrong = len(correct & chosen), len(chosen - correct)
    return {
        'exact': exact,
        'partial': round(max(0, hits - wrong) / len(correct), 3),
        'trap': int(bool(chosen & set(question.trap))),
        'not_covered': int('NC' in chosen),
        'unsure': unsure,
        'points': POINTS['exact'] if exact else POINTS['unsure'] if unsure else POINTS['wrong'],
        'parse_ok': 1,
    }
