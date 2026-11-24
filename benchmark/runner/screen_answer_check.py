#!/usr/bin/env python3
"""Does Agent E2 answer a question typed on a PCM screen the way it asks (harness/answer_service.py)?

Runs every question of screen_answer_check.yaml through the service, in process, with the page's facts as PCM sends them
(screen_answer_check_pages.json), on the real model, and checks each answer by code:
  - page values: the opening is shown (the answer reads the page's values) exactly when the question needs them; an
    answer that should not read them names none of the opening's figures;
  - shape: the answer shape is one the question accepts;
  - must, must_some, must_not: what the answer has to say, or must not say.
No judge: every check is a pattern. Read the answers too (--out): a pattern proves a word is there, not that it is right.
A development check of the service, not the benchmark; run it before and after a change to how the service reads a
question or shapes an answer, and add the wordings of every wrong answer seen in the live test.

Examples:
  AI_GATEWAY_API_KEY=... python3 benchmark/runner/screen_answer_check.py --out /tmp/answers.json
  AI_GATEWAY_API_KEY=... python3 benchmark/runner/screen_answer_check.py --only S01,P04
"""
import argparse
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'harness'))
import answer_service  # noqa: E402

FIGURE = re.compile(r'(?<![\d.])\d+(?:\.\d+)?%')


def check(ask, out, page_lead):
    """The failed checks of one answer, as short labels; [] when it passes."""
    text, fails = out.get('content') or '', []
    shown = bool(out.get('lead'))
    if shown != ask['page_values']:
        fails.append('page values ' + ('shown' if shown else 'missing'))
    if not ask['page_values']:
        figs = sorted({f for f in FIGURE.findall(page_lead) if re.search(r'(?<![\d.])' + re.escape(f), text)})
        if figs:
            fails.append('page figures ' + ' '.join(figs))
    if out.get('shape') not in ask['shape']:
        fails.append(f'shape {out.get("shape")}')
    for p in ask.get('must') or []:
        if not re.search(p, text, re.I):
            fails.append(f'missing /{p}/')
    some = ask.get('must_some')
    if some:
        got = sum(bool(re.search(p, text, re.I)) for p in some['of'])
        if got < some['n']:
            fails.append(f'lists {got} of {some["n"]}')
    for p in ask.get('must_not') or []:
        if re.search(p, text, re.I):
            fails.append(f'has /{p}/')
    return fails


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--config', default=os.path.join(HERE, '..', '..', 'harness', 'service_config.yaml'))
    ap.add_argument('--asks', default=os.path.join(HERE, 'screen_answer_check.yaml'))
    ap.add_argument('--pages', default=os.path.join(HERE, 'screen_answer_check_pages.json'))
    ap.add_argument('--only', help='comma-separated ids')
    ap.add_argument('--workers', type=int, default=6)
    ap.add_argument('--out', help='write every answer, its checks and timing to this JSON file')
    a = ap.parse_args()
    cfg = yaml.safe_load(open(a.config))
    asks = yaml.safe_load(open(a.asks))['asks']
    if a.only:
        keep = set(a.only.split(','))
        asks = [x for x in asks if x['id'] in keep]
    pages = json.load(open(a.pages))
    service = answer_service.Service(cfg)
    leads = {p: service.lead(f) for p, f in pages.items()}  # the opening each page shows: its figures

    def one(ask):
        t = time.time()
        try:
            out = service.answer({'question': ask['question'], 'facts': pages[ask['page']], 'role': 'l2'})
        except Exception as e:  # a failed call is a failed check, not a stopped run
            out = {'content': '', 'error': str(e)}
        fails = check(ask, out, leads[ask['page']]) if not out.get('error') else [f'error {out["error"]}']
        return {'id': ask['id'], 'question': ask['question'], 'page': ask['page'], 'fails': fails,
                'seconds': round(time.time() - t, 1), 'shape': out.get('shape'), 'page_values': out.get('page_values'),
                'lead': out.get('lead'), 'content': out.get('content'), 'files_read': len(out.get('files_read') or [])}

    with ThreadPoolExecutor(a.workers) as pool:
        rows = list(pool.map(one, asks))
    for r in rows:
        words = len((r['content'] or '').split())
        print(f"{r['id']} {'ok  ' if not r['fails'] else 'FAIL'} {r['shape'] or '-':8} {words:4}w {r['seconds']:5}s "
              f"{r['files_read']:3}f  {'; '.join(r['fails'])}")
    ok = sum(not r['fails'] for r in rows)
    concept = [r for r, x in zip(rows, asks) if not x['page_values']]
    page = [r for r, x in zip(rows, asks) if x['page_values']]
    print(f'{ok}/{len(rows)} pass; general questions {sum(not r["fails"] for r in concept)}/{len(concept)}, '
          f'page questions {sum(not r["fails"] for r in page)}/{len(page)}; '
          f'median {sorted(r["seconds"] for r in rows)[len(rows) // 2]} s')
    if a.out:
        json.dump(rows, open(a.out, 'w'), indent=1, ensure_ascii=False)


if __name__ == '__main__':
    main()
