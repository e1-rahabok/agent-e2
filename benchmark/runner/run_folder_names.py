"""Names of run folders: `<date>-<model>`, e.g. 20261114-gemma-4-31b-it. The model name is what a reader looks for."""
import datetime as dt
import os
import re


def slug(model):
    """google/gemma-4-31b-it -> gemma-4-31b-it. Keeps letters, digits, dots and hyphens."""
    s = re.sub(r'[^a-z0-9.]+', '-', model.split('/')[-1].lower()).strip('-')
    return s or 'model'


def run_name(models, out_dir, mock=False, today=None):
    """One model: `<date>-<model>`. Several models in one folder: names joined with `+`. A name already taken gets -2, -3."""
    day = (today or dt.date.today()).strftime('%Y%m%d')
    base = f'{day}-' + '+'.join(slug(m) for m in models) + ('-mock' if mock else '')
    name, n = base, 1
    while os.path.exists(os.path.join(out_dir, name)):
        n += 1
        name = f'{base}-{n}'
    return name
