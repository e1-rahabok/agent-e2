"""Run one demo scenario through Agent E2, as the shipped assistant answers it (answer_modes.converse, chat mode).

A scenario folder in project/demo-site/ holds turn-1.txt (what the user writes first) and, optionally, turn-2.txt
(what the user writes next). Turn 1 runs as is. If Agent E2 asks back (one clarifying round), turn 2 is the user's
reply; otherwise turn 2 is a follow-up that carries the first question and answer. The result, with the files read,
the trace and the knowledge base commit, goes to <folder>/results/<model>.json.

Usage: python3 project/tools/demo_scenario_executor.py project/demo-site/scenario-1-memory-tiering google/gemma-4-31b-it ['{"reasoning": {"effort": "low"}}']
The optional third argument replaces the model's request settings (runner_config model_params), as a benchmark run passes --params.
Needs AI_GATEWAY_API_KEY (the benchmark gateway). Not a benchmark run: demos are not scored into the release.
"""
import json
import os
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


def main(folder, model, params_json=None):
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
    turn1 = open(os.path.join(folder, 'turn-1.txt')).read()
    out1 = answer_modes.converse('agent-e2', client, model, [turn1], [], cfg, retriever)
    rec = {'model': model, 'model_params': params[model], 'knowledge_commit': knowledge_loader.git_sha(),
           'turn_1': {'type': out1['type'], 'content': out1['result'].get('content'), 'files_read': out1['used'],
                      'trace': _trace(out1['trace'])}}
    path2 = os.path.join(folder, 'turn-2.txt')
    if os.path.exists(path2):
        turn2 = open(path2).read()
        if out1['type'] == 'clarify':
            out2 = answer_modes.converse('agent-e2', client, model, [turn1, out1['result'].get('content'), turn2], [], cfg, retriever)
        else:
            follow = f'{turn1}\n\nAgent E2 answered:\n{out1["result"].get("content") or ""}\n\nThe user now writes:\n{turn2}'
            out2 = answer_modes.converse('agent-e2', client, model, [follow], [], cfg, retriever)
        rec['turn_2'] = {'type': out2['type'], 'content': out2['result'].get('content'), 'files_read': out2['used'],
                         'trace': _trace(out2['trace'])}
    os.makedirs(os.path.join(folder, 'results'), exist_ok=True)
    out_path = os.path.join(folder, 'results', model.replace('/', '_') + '.json')
    json.dump(rec, open(out_path, 'w'), indent=1, ensure_ascii=False, default=str)
    print(out_path)


if __name__ == '__main__':
    if len(sys.argv) not in (3, 4):
        sys.exit(__doc__)
    main(*sys.argv[1:])
