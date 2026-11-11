#!/usr/bin/env python3
"""Harness-only test: does retrieval find the files a question needs? No model is called.

For every question with `knowledge` ids, run the classic-mode retrieval on the prompt text
(the same `## Prompt` the model sees, options included) and report:
  - recall@k of plain search (top k files),
  - recall of the classic context (search + same_name/related expansion, within the token budget),
  - which needed files were missed.
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
import modes  # noqa: E402
from retrieval import Retriever  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--config', default=os.path.join(os.path.dirname(__file__), 'config.yaml'))
    ap.add_argument('--embeddings', action='store_true', help='hybrid search with the configured embedding model (needs AI_GATEWAY_API_KEY)')
    ap.add_argument('--k', type=int, default=6)
    ap.add_argument('--questions', help='comma-separated id fragments')
    ap.add_argument('--set', action='append', default=[], metavar='KEY=VALUE',
                    help='override a config value for this check, e.g. --set expand_derive=true (repeatable)')
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
        question = c.render(random.Random(0))[0] if c.options else c.prompt
        top = [h['id'] for h in ret.search(question, k=a.k)]
        _, ctx, _ = modes.classic_context(ret, question, cfg)
        rows.append((c.id, need, top, ctx))
    print(f"| Question | Needed | Search top {a.k} | Classic context | Missed in context |")
    print('|---|---|---|---|---|')
    s_hit = c_hit = n = 0
    for cid, need, top, ctx in rows:
        sh = sum(i in top for i in need)
        ch = sum(i in ctx for i in need)
        s_hit += sh
        c_hit += ch
        n += len(need)
        miss = ', '.join(f'`{i}`' for i in need if i not in ctx) or '-'
        print(f'| {cid} | {len(need)} | {sh}/{len(need)} | {ch}/{len(need)} | {miss} |')
    full = sum(all(i in ctx for i in need) for _, need, _, ctx in rows)
    print(f'\nQuestions: {len(rows)}. Recall@{a.k} search: {s_hit / n:.0%}. Recall classic context: {c_hit / n:.0%}. '
          f'Questions with every needed file in context: {full}/{len(rows)}. Mode: {"hybrid" if a.embeddings else "BM25 only"}{" + rerank" if cfg.get("rerank") else ""}.')


if __name__ == '__main__':
    main()
