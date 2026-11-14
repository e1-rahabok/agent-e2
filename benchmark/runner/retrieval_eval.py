#!/usr/bin/env python3
"""Harness-only test: does retrieval find the files a question needs? No model is called.

For every question with `knowledge` ids, build Agent E2's reading set (harness/planner.py, the code-only reading of the
question: no model call) on the prompt text (the same `## Prompt` the model sees, options included) and report:
  - recall@k of plain search (top k files),
  - recall of the reading set (named files, search, mechanism links, one search per claim, within the token budget),
  - which needed files were missed,
  - questions whose main file (`knowledge_main`) is missing from the reading set: each one is a defect,
  - complete questions by number of needed files.
A miss here is a harness or knowledge problem, never a model problem.

Examples:
  python3 benchmark/runner/retrieval_eval.py                 # BM25 only, offline
  AI_GATEWAY_API_KEY=... python3 benchmark/runner/retrieval_eval.py --embeddings   # hybrid, as in runs
"""
import argparse
import os
import random
import sys

import yaml

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'harness'))
import questions as C  # noqa: E402
import kb  # noqa: E402
import planner  # noqa: E402
from retrieval import Retriever  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--config', default=os.path.join(os.path.dirname(__file__), 'config.yaml'))
    ap.add_argument('--embeddings', action='store_true', help='hybrid search with the configured embedding model (needs AI_GATEWAY_API_KEY)')
    ap.add_argument('--k', type=int, default=6)
    ap.add_argument('--no-options', action='store_true', help='the stem only, as an operator asks: options left out (the field reading; every benchmark question is multiple choice)')
    ap.add_argument('--questions', help='comma-separated id fragments')
    ap.add_argument('--set', action='append', default=[], metavar='KEY=VALUE',
                    help='override a config value for this check, e.g. --set plan_section_tokens=250 (repeatable)')
    a = ap.parse_args()
    cfg = yaml.safe_load(open(a.config))
    for kv in a.set:
        k, v = kv.split('=', 1)
        cfg[k] = yaml.safe_load(v)
    docs, chunks = kb.load()
    rr = {}
    if cfg.get('rerank'):
        from rerank import Reranker
        rr = {'reranker': Reranker(cfg.get('rerank_model', 'bge-reranker-v2-m3')), 'rerank_n': cfg.get('rerank_n', 30), 'rerank_mode': cfg.get('rerank_mode', 'replace'), 'rerank_stem': cfg.get('rerank_stem', False)}
    if a.embeddings:
        from llm import GatewayClient
        client = GatewayClient(cfg['gateway'], os.environ['AI_GATEWAY_API_KEY'])
        ret = Retriever(docs, chunks, client, cfg['embedding_model'], expand=cfg.get('query_expansion', False), **rr)
    else:
        ret = Retriever(docs, chunks, expand=cfg.get('query_expansion', False), **rr)
    rows = []
    for c in C.load(a.questions):
        need = list(c.knowledge)
        unknown = [i for i in need if i not in docs]
        if unknown:  # never drop a needed file silently: that would raise recall
            sys.exit(f'{c.id}: unknown knowledge ids {unknown} (moved? use the current id: project/tools/moved.yaml maps old ids)')
        if not need:
            continue
        question = c.stem_text() if a.no_options else c.render(random.Random(0))[0] if c.options else c.open_text()
        top = [h['id'] for h in ret.search(question, k=a.k)]
        ctx = planner.reading_set(ret, question, cfg)[1]
        rows.append((c.id, need, top, ctx, c.knowledge_main))
    print(f"| Question | Needed | Search top {a.k} | Reading set | Missed in the reading set |")
    print('|---|---|---|---|---|')
    for cid, need, top, ctx, main_id in rows:
        sh = sum(i in top for i in need)
        ch = sum(i in ctx for i in need)
        miss = ', '.join(f'`{i}`' + (' (main)' if i == main_id else '') for i in need if i not in ctx) or '-'
        print(f'| {cid} | {len(need)} | {sh}/{len(need)} | {ch}/{len(need)} | {miss} |')
    s = summary(rows)
    print(f"\nQuestions: {s['questions']}. Recall@{a.k} search: {s['search']:.0%}. Recall reading set: {s['context']:.0%}. "
          f"Questions with every needed file in context: {s['complete']}/{s['questions']} ({s['complete'] / s['questions']:.0%}). "
          f"Main file missing from the reading set: {len(s['main_missed'])} of {s['main_keyed']} questions with a main file"
          f"{' (' + ', '.join(s['main_missed']) + ')' if s['main_missed'] else ''}. "
          f"Mode: {'hybrid' if a.embeddings else 'BM25 only'}{' + rerank' if cfg.get('rerank') else ''}"
          ".")
    print('Complete by number of needed files: ' + ', '.join(f"{k} file{'s' if k != '1' else ''} {v[0]}/{v[1]} ({v[0] / v[1]:.0%})"
                                                         for k, v in s['by_need'].items()) + '.')
    print('Release levels (benchmark/retrieval-check.md): main file 100%, context recall at least 95%, complete at least 90%.')


def summary(rows):
    """The numbers of the check, from rows (id, needed, search top k, reading set, main id or '')."""
    n = sum(len(need) for _, need, _, _, _ in rows)
    keyed = [(cid, main_id, ctx) for cid, _, _, ctx, main_id in rows if main_id]
    return {'questions': len(rows),
            'search': sum(i in top for _, need, top, _, _ in rows for i in need) / n if n else 0,
            'context': sum(i in ctx for _, need, _, ctx, _ in rows for i in need) / n if n else 0,
            'complete': sum(all(i in ctx for i in need) for _, need, _, ctx, _ in rows),
            'main_keyed': len(keyed),
            'main_missed': [cid for cid, main_id, ctx in keyed if main_id not in ctx],
            'by_need': _by_need(rows)}


def _by_need(rows):
    """Complete questions by number of needed files: {'1': (complete, questions), ..., '5+': ...}."""
    out = {}
    for _, need, _, ctx, _ in sorted(rows, key=lambda r: len(r[1])):
        k = str(len(need)) if len(need) < 5 else '5+'
        done, total = out.get(k, (0, 0))
        out[k] = (done + all(i in ctx for i in need), total + 1)
    return out

if __name__ == '__main__':
    main()
