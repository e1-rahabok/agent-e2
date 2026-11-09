"""Hybrid retrieval: BM25 keyword search plus optional embeddings, fused by reciprocal rank."""
import hashlib
import json
import math
import os
import re
from collections import Counter, defaultdict

from kb import FILTER_FIELDS, ROOT

TOKEN = re.compile(r'[a-z0-9]+(?:[.\-][a-z0-9]+)*')
STOP = set('a an and are as at be by for from has in is it its of on or that the this to was were with which what when how why does do not no'.split())


def tokens(text):
    return [t for t in TOKEN.findall(text.lower()) if t not in STOP]


class BM25:
    def __init__(self, texts, k1=1.4, b=0.75):
        self.k1, self.b = k1, b
        self.docs = [Counter(tokens(t)) for t in texts]
        self.lens = [sum(c.values()) for c in self.docs]
        self.avg = sum(self.lens) / max(1, len(self.lens))
        df = defaultdict(int)
        for c in self.docs:
            for t in c:
                df[t] += 1
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - v + 0.5) / (v + 0.5)) for t, v in df.items()}

    def scores(self, query):
        q = tokens(query)
        out = []
        for i, c in enumerate(self.docs):
            s = 0.0
            for t in q:
                f = c.get(t)
                if f:
                    s += self.idf[t] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * self.lens[i] / self.avg))
            out.append(s)
        return out


def glossary_terms(docs):
    """(term found in a question, words to add) from the glossary tables Synonyms and Words to avoid."""
    g = docs.get('glossary')
    out = []
    if not g:
        return out
    for head, text in g.sections:
        if head.startswith('Defined terms'):
            for line in text.split('\n'):
                cells = [c.strip() for c in line.strip().strip('|').split('|')]
                if len(cells) < 3 or set(cells[0]) <= set('-: ') or cells[0] == 'Term':
                    continue
                preferred = re.sub(r'\(.*?\)', '', cells[0]).strip()
                for a in cells[2].split(','):
                    a = re.sub(r'\(.*?\)', '', a).strip()
                    if len(a) > 2 and a != '-':
                        out.append((a, preferred))
        if head.startswith('Synonyms') or head.startswith('Words to avoid'):
            for line in text.split('\n'):
                cells = [c.strip() for c in line.strip().strip('|').split('|')]
                if len(cells) < 2 or set(cells[0]) <= set('-: ') or cells[0] in ('Preferred term', 'Avoid'):
                    continue
                if head.startswith('Synonyms'):
                    preferred, aliases = cells[0], cells[1].split(',')
                else:
                    preferred, aliases = cells[1], [cells[0]]
                preferred = re.sub(r'\(.*?\)', '', preferred).strip()
                for a in aliases:
                    a = re.sub(r'\(.*?\)', '', a).strip()
                    if len(a) > 2:
                        out.append((a, preferred))
    return out


def expand_query(query, terms):
    """Add the glossary's preferred words when the question uses another name for the same thing."""
    extra = [pref for alias, pref in terms
             if re.search(r'(?<![\w-])' + re.escape(alias) + r'(?![\w-])', query, re.I) and pref.lower() not in query.lower()]
    return query + ('\n' + ' '.join(dict.fromkeys(extra)) if extra else '')


class Retriever:
    def __init__(self, docs, chunks, client=None, embed_model=None, cache_dir=None, expand=False,
                 reranker=None, rerank_n=30, rerank_mode='replace', rerank_stem=False):
        self.docs, self.chunks = docs, chunks
        self.reranker, self.rerank_n, self.rerank_mode, self.rerank_stem = reranker, rerank_n, rerank_mode, rerank_stem  # optional cross-encoder (harness/rerank.py)
        self.expand = expand
        self.synonyms = glossary_terms(docs)
        self.bm25 = BM25([c.text for c in chunks])
        self.vectors = None
        self.client, self.embed_model = client, embed_model
        if client and embed_model:
            self.vectors = self._embed_chunks(cache_dir or os.path.join(ROOT, 'harness', '.cache'))

    # ---- embeddings -------------------------------------------------------
    def _embed_chunks(self, cache_dir):
        os.makedirs(cache_dir, exist_ok=True)
        path = os.path.join(cache_dir, 'embeddings-' + self.embed_model.replace('/', '_') + '.json')
        cache = json.load(open(path)) if os.path.exists(path) else {}
        keys = [hashlib.sha1(c.text.encode()).hexdigest() for c in self.chunks]
        missing = [(k, c.text) for k, c in zip(keys, self.chunks) if k not in cache]
        for i in range(0, len(missing), 64):
            batch = missing[i:i + 64]
            vecs = self.client.embed(self.embed_model, [t[:8000] for _, t in batch])
            for (k, _), v in zip(batch, vecs):
                cache[k] = v
        if missing:
            json.dump(cache, open(path, 'w'))
        return [self._norm(cache[k]) for k in keys]

    @staticmethod
    def _norm(v):
        n = math.sqrt(sum(x * x for x in v)) or 1.0
        return [x / n for x in v]

    def _vector_scores(self, query):
        q = self._norm(self.client.embed(self.embed_model, [query])[0])
        return [sum(a * b for a, b in zip(q, v)) for v in self.vectors]

    # ---- search -------------------------------------------------------------
    def _allowed(self, doc, filters):
        for f in FILTER_FIELDS:
            want = filters.get(f) if filters else None
            if not want:
                continue
            want = want if isinstance(want, list) else [want]
            if not set(want) & set(doc.tags(f)):
                return False
        return True

    def search(self, query, filters=None, k=8, min_hits=3):
        """Return the top k documents (best chunk per document)."""
        if self.expand:
            query = expand_query(query, self.synonyms)
        ranked = self._rank(query, filters)
        if filters and len(ranked) < min_hits:
            ranked = self._rank(query, None)
        return ranked[:k]

    def _rank(self, query, filters):
        lists = [self.bm25.scores(query)]
        if self.vectors is not None:
            lists.append(self._vector_scores(query))
        fused = defaultdict(float)
        for scores in lists:
            order = sorted(range(len(scores)), key=lambda i: -scores[i])
            for r, i in enumerate(order[:200]):
                if scores[i] > 0:
                    fused[i] += 1.0 / (60 + r)
        order = [(i, s) for i, s in sorted(fused.items(), key=lambda x: -x[1]) if self._allowed(self.chunks[i].doc, filters)]
        if self.reranker and order:
            head = order[:self.rerank_n]
            q = re.sub(r'(?m)^\s*-\s*[A-H]\.\s.*$', '', query).strip() if self.rerank_stem else query  # options out
            rs = self.reranker.scores(q, [self.chunks[i].text for i, _ in head])
            if self.rerank_mode == 'fuse':  # add the re-ranker's rank as a third list in the fusion
                pos = {h[0]: p for h, p in zip([x[0] for x in sorted(zip(head, rs), key=lambda x: -x[1])], range(len(head)))}
                head = sorted(((i, s + 1.0 / (60 + pos[i])) for i, s in head), key=lambda x: -x[1])
            else:  # replace: the re-ranker's order alone
                head = [(i, r) for (i, _), r in sorted(zip(head, rs), key=lambda x: -x[1])]
            order = head + order[self.rerank_n:]
        best = {}
        for i, s in order:
            c = self.chunks[i]
            if c.doc.id not in best:
                best[c.doc.id] = (s, c)
        return [{'id': d, 'score': round(s, 4), 'title': c.doc.title, 'heading': c.heading,
                 'snippet': ' '.join(c.text.split('\n')[1:3])[:240], 'status': c.doc.status}
                for d, (s, c) in best.items()]

    def links(self, doc_id, link_type='all'):
        d = self.docs.get(doc_id)
        if not d:
            return []
        types = list(d.links) if link_type == 'all' else [link_type]
        out = []
        for t in types:
            for lid in d.links.get(t, []):
                ld = self.docs.get(lid)
                out.append({'id': lid, 'type': t, 'title': ld.title if ld else '(missing)',
                            'status': ld.status if ld else 'missing'})
        return out
