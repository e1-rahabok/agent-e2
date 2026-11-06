"""Cross-encoder re-ranker: re-scores the top chunks after rank fusion.

A cross-encoder reads the question and one chunk together and returns one relevance score.
It is slower than BM25 or embeddings, so it scores only the top `top_n` fused chunks.
The model runs locally (offline). Default: BAAI/bge-reranker-v2-m3 in harness/.cache/models/.
Scores are cached per (question, chunk) pair in harness/.cache/, so a repeated check is fast.
Switch: `rerank` in benchmark/runner/config.yaml (off by default).
"""
import hashlib
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, 'harness', '.cache')


class Reranker:
    def __init__(self, model='bge-reranker-v2-m3', max_length=1024, cache_dir=CACHE):
        self.name = model
        self.path = model if os.path.isdir(model) else os.path.join(cache_dir, 'models', model)
        self.max_length = max_length
        self.cache_path = os.path.join(cache_dir, f'rerank-{os.path.basename(model)}.json')
        self.cache = json.load(open(self.cache_path)) if os.path.exists(self.cache_path) else {}
        self._model = None

    def _load(self):
        if self._model is None:
            from sentence_transformers import CrossEncoder  # imported only when the switch is on
            self._model = CrossEncoder(self.path, max_length=self.max_length, device='cpu')
        return self._model

    @staticmethod
    def _key(query, text):
        return hashlib.sha1((query + '\x00' + text).encode()).hexdigest()

    def scores(self, query, texts):
        keys = [self._key(query, t) for t in texts]
        todo = [(k, t) for k, t in zip(keys, texts) if k not in self.cache]
        if todo:
            vals = self._load().predict([(query, t) for _, t in todo], batch_size=8)
            for (k, _), v in zip(todo, vals):
                self.cache[k] = float(v)
            os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
            json.dump(self.cache, open(self.cache_path, 'w'))
        return [self.cache[k] for k in keys]
