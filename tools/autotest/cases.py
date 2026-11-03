"""Golden cases: load, shuffle options, render, parse and score answers.

Only `## Prompt` and attachments are ever shown to the model. The answer key
(front matter `answer`, `trap`) is read here for scoring only.
"""
import base64
import glob
import mimetypes
import os
import re

import yaml

from kb import ROOT

NOT_COVERED = 'Not covered by the knowledge base.'
OPTION = re.compile(r'^([A-H])\.\s+(.*)$')
ANSWER = re.compile(r'ANSWER:\s*\**\s*([A-H](?:\s*(?:,|and|&)?\s*[A-H])*)\b', re.I)


class Case:
    def __init__(self, path):
        text = open(path).read()
        _, fm, body = text.split('---\n', 2)
        self.path = path
        self.meta = yaml.safe_load(fm)
        self.id = self.meta['id']
        self.area = self.meta.get('area', '')
        self.level = self.meta.get('level', '')
        self.format = self.meta.get('format', 'free-text')
        self.answer = [str(a) for a in (self.meta.get('answer') or [])]
        self.trap = [str(a) for a in (self.meta.get('trap') or [])]
        self.knowledge = list(self.meta.get('knowledge') or [])
        self.attachments = [os.path.join(ROOT, 'evaluation', 'attachments', a) for a in (self.meta.get('attachments') or [])]
        m = re.search(r'## Prompt\n(.*?)(?=\n## )', body, re.S)
        self.prompt = m.group(1).strip() if m else ''
        self.stem, self.options, self.footer = self._split_prompt(self.prompt)

    @staticmethod
    def _split_prompt(prompt):
        stem, options, footer, state = [], [], [], 'stem'
        for line in prompt.split('\n'):
            m = OPTION.match(line.strip())
            if m and state in ('stem', 'opts'):
                options.append([m.group(1), m.group(2)])
                state = 'opts'
            elif state == 'opts' and line.strip() and not line.strip().endswith(':') and not line.lower().startswith('hint'):
                options[-1][1] += ' ' + line.strip()
            elif state == 'stem':
                stem.append(line)
            else:
                state = 'footer'
                footer.append(line)
        return '\n'.join(stem).strip(), options, '\n'.join(footer).strip()

    @property
    def scorable(self):
        return self.format == 'multiple-choice' and bool(self.options) and bool(self.answer)

    @property
    def has_images(self):
        return any(a.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')) for a in self.attachments)

    def render(self, rng):
        """Shuffle options, append Not covered, return (text, map shown_letter -> original)."""
        opts = self.options[:]
        rng.shuffle(opts)
        letters = 'ABCDEFGH'
        mapping, lines = {}, []
        for i, (orig, text) in enumerate(opts):
            mapping[letters[i]] = orig
            lines.append(f'{letters[i]}. {text}')
        nc = letters[len(opts)]
        mapping[nc] = 'NC'
        lines.append(f'{nc}. {NOT_COVERED}')
        parts = [self.stem, '', '\n'.join(lines)]
        if self.footer:
            parts += ['', self.footer]
        multi = len(self.answer) > 1
        parts += ['', 'Choose all correct options.' if multi else 'Choose the single best option.']
        return '\n'.join(parts), mapping

    def image_parts(self):
        out = []
        for a in self.attachments:
            mime = mimetypes.guess_type(a)[0] or 'image/png'
            data = base64.b64encode(open(a, 'rb').read()).decode()
            out.append({'type': 'image_url', 'image_url': {'url': f'data:{mime};base64,{data}'}})
        return out


def load(pattern=None):
    files = sorted(glob.glob(os.path.join(ROOT, 'evaluation', 'cases', '**', '*.md'), recursive=True))
    cases = [Case(f) for f in files]
    if pattern:
        keep = [p.strip() for p in pattern.split(',')]
        cases = [c for c in cases if any(k in c.id for k in keep)]
    return cases


def parse(text, mapping):
    """Return the original letters chosen, or None when the answer cannot be parsed."""
    m = None
    for m in ANSWER.finditer(text or ''):
        pass  # last ANSWER line wins (models sometimes draft first)
    if not m:
        return None
    shown = set(re.findall(r'[A-H]', m.group(1).upper()))
    if not shown or not shown <= set(mapping):
        return None
    return sorted(mapping[s] for s in shown)


def score(case, picked):
    if picked is None:
        return {'exact': 0, 'partial': 0.0, 'trap': 0, 'not_covered': 0, 'parse_ok': 0}
    correct, chosen = set(case.answer), set(picked)
    hits, wrong = len(correct & chosen), len(chosen - correct)
    return {
        'exact': int(chosen == correct),
        'partial': round(max(0, hits - wrong) / len(correct), 3),
        'trap': int(bool(chosen & set(case.trap))),
        'not_covered': int('NC' in chosen),
        'parse_ok': 1,
    }
