#!/usr/bin/env python3
"""Does Agent E2 tell a question that continues the topic from one that starts a new topic (harness/topic_decision.py)?

Scores the labelled pairs of topic_check_pairs.yaml three ways:
  - always: every question continues (what shipped before topics, 2026-11-24);
  - code: the code rule alone; a question it cannot settle continues;
  - model: the full decision, code then one model call (needs AI_GATEWAY_API_KEY; one call per pair the code cannot settle).
Two errors are counted apart: lost context (the label continues, the decision says new: the answer misses what the user
refers to, the worse error) and extra context (the label is new, the decision continues: earlier turns are sent for nothing).

Examples:
  python3 benchmark/runner/topic_check.py --no-model
  AI_GATEWAY_API_KEY=... python3 benchmark/runner/topic_check.py
"""
import argparse
import os
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'harness'))
import knowledge_loader  # noqa: E402
import topic_decision  # noqa: E402
from model_client import GatewayClient, ParamClient  # noqa: E402


def score(pairs, decided):
    lost = [p['id'] for p, d in zip(pairs, decided) if p['continues'] and not d]
    extra = [p['id'] for p, d in zip(pairs, decided) if not p['continues'] and d]
    return {'right': len(pairs) - len(lost) - len(extra), 'lost': lost, 'extra': extra}


def line(name, s, n):
    return (f'{name:7} {s["right"]}/{n} right; lost context {len(s["lost"])} {s["lost"] or ""}; '
            f'extra context {len(s["extra"])} {s["extra"] or ""}')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--config', default=os.path.join(HERE, '..', '..', 'harness', 'service_config.yaml'))
    ap.add_argument('--pairs', default=os.path.join(HERE, 'topic_check_pairs.yaml'))
    ap.add_argument('--model', help='model to ask (default: the service config model)')
    ap.add_argument('--no-model', action='store_true', help='code rule only, offline')
    a = ap.parse_args()
    cfg = yaml.safe_load(open(a.config))
    pairs = yaml.safe_load(open(a.pairs))['pairs']
    docs, _ = knowledge_loader.load()
    n = len(pairs)
    print(line('always', score(pairs, [True] * n), n))
    code = [True if topic_decision.points_back(docs, p['question']) else None for p in pairs]
    print(line('code', score(pairs, [c if c is not None else True for c in code]), n),
          f'(settled {sum(c is not None for c in code)} of {n}; the rest continue)')
    if a.no_model:
        return
    model = a.model or cfg['model']
    client = ParamClient(GatewayClient(cfg['gateway'], retry_seconds=cfg.get('gateway_retry_minutes', 1) * 60),
                         {model: (cfg.get('model_params') or {}).get(model, {})},
                         {model: (cfg.get('sampling') or {}).get(model, {'temperature': cfg.get('temperature')})})
    out = [topic_decision.decide(client, model, p['question'], p['history'], 'auto', docs, cfg) for p in pairs]
    s = score(pairs, [o['continues'] for o in out])
    print(line('model', s, n), f'({model}; by: ' + ', '.join(f'{b} {sum(o["by"] == b for o in out)}' for b in ('code', 'model', 'unsure')) + ')')


if __name__ == '__main__':
    main()
