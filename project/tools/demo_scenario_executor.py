"""Run the steps of one demo scenario through Agent E2, as the shipped assistant answers them (answer_modes.converse, chat mode).

A scenario folder in project/demo-site/ holds steps/step-1.txt, step-2.txt, ...: at each step the L2 specialist's
question, a blank line, then the readings Agent E2 reads from VCF Operations and vCenter. The VCF Operations connector is
not built yet: the readings stand for what it would fetch, and the pipeline gets them as text. Each step is a question of its own: Agent E2 does not
carry an earlier answer into the next one. The answers, with the exact facts computed by code (stage 3), the files read,
the trace and the knowledge base commit, go to <folder>/results/<model>.json; a rerun of some steps keeps the others.

Usage: python3 project/tools/demo_scenario_executor.py <folder> <model> [--params '{"reasoning": {"effort": "low"}}'] [--steps 1,3] [--label run2]
--label writes results/<model>__<label>.json instead, so the gate runs of a quick-answer demo do not overwrite each other.
--params replaces the model's request settings (runner_config model_params), as a benchmark run passes --params.
Needs AI_GATEWAY_API_KEY (the benchmark gateway). Not a benchmark run: a demo is not scored.
"""
import argparse
import glob
import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'harness'))
import answer_modes  # noqa: E402
import knowledge_loader  # noqa: E402
from knowledge_search import Retriever  # noqa: E402
from model_client import GatewayClient, LLMError, ParamClient  # noqa: E402

TRACE_KEYS = ('step', 'action', 'output', 'prompt_tokens', 'completion_tokens', 'latency', 'provider')


def _trace(steps):
    return [{k: s.get(k) for k in TRACE_KEYS} for s in steps]


def step_files(folder):
    files = glob.glob(os.path.join(folder, 'steps', 'step-*.txt'))
    return sorted(files, key=lambda p: int(re.search(r'step-(\d+)\.txt$', p).group(1)))


def main(folder, model, params_json=None, only=None, label=None):
    cfg = yaml.safe_load(open(os.path.join(ROOT, 'benchmark', 'runner', 'runner_config.yaml')))
    params = {model: json.loads(params_json) if params_json else (((cfg.get('model_params') or {}).get(model) or [{}])[0] or {})}
    sampling = {model: (cfg.get('sampling') or {}).get(model, {'temperature': cfg.get('temperature')})}
    client = ParamClient(GatewayClient(cfg['gateway'], retry_seconds=cfg.get('gateway_retry_minutes', 1) * 60), params, sampling)
    docs, chunks = knowledge_loader.load()
    try:
        retriever = Retriever(docs, chunks, client, cfg.get('embedding_model'), expand=cfg.get('query_expansion', False))
    except LLMError as e:
        print(f'Embeddings unavailable ({e}); BM25 only.')
        retriever = Retriever(docs, chunks, expand=cfg.get('query_expansion', False))
    out_path = os.path.join(folder, 'results', model.replace('/', '_') + (f'__{label}' if label else '') + '.json')
    rec = json.load(open(out_path)) if os.path.exists(out_path) else {}
    rec.update({'model': model, 'model_params': params[model], 'knowledge_commit': knowledge_loader.git_sha()})
    rec.setdefault('steps', {})
    for path in step_files(folder):
        n = re.search(r'step-(\d+)\.txt$', path).group(1)
        if only and n not in only:
            continue
        text = open(path).read()
        out = answer_modes.converse('agent-e2', client, model, [text], [], cfg, retriever)
        trace = _trace(out['trace'])
        computed = [line for s in trace if s['action'] == 'compute' for line in (s.get('output') or [])]
        rec['steps'][n] = {'type': out['type'], 'content': out['result'].get('content'), 'computed': computed,
                           'files_read': out['used'], 'knowledge_commit': rec['knowledge_commit'], 'trace': trace}
        print(f'step {n}: {out["type"]}, {len(out["result"].get("content") or "")} characters, computed {len(computed)}')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    json.dump(rec, open(out_path, 'w'), indent=1, ensure_ascii=False, default=str)
    print(out_path)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('folder')
    ap.add_argument('model')
    ap.add_argument('--params')
    ap.add_argument('--steps', help='comma-separated step numbers; default every step')
    ap.add_argument('--label', help='a run label: results/<model>__<label>.json')
    a = ap.parse_args()
    main(a.folder, a.model, a.params, a.steps.split(',') if a.steps else None, a.label)
