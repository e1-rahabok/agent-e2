"""Reading plan: which knowledge files the model reads for one question, chosen by code from the knowledge base's map.

Stage 2 of Agent E2's agent, the neuro-symbolic expert system (harness/AGENT.md, section 4.2). The model does not choose
what to read: it does not know what the knowledge base holds, and its worst errors are beliefs it never looks up.
The plan is built from what the knowledge base already records about itself:
  - exact names: metric file titles, vCenter counter keys and chart labels in the question resolve to their files
    (catalog), filtered by the objects the question names;
  - the term map (user words to files, harness/terms.py);
  - the kind of question (a troubleshooting question gets its flow first);
  - one search per claim: each option of a multiple-choice question, or each question sentence, is searched on its own,
    because the claims of a Level 400 question test different mechanisms;
  - the mechanism links of what was found: same_name (the other object's meaning of the label) and internal_derive
    (the mechanism files a metric is derived from), which a question's words do not name.
Files are packed by tier into the context budget; the same question always gets the same reading set.
The code-only reading of the question is always used; the case the model reads (stage 1, harness/agent.py) adds its
metric names, kind and claims when given. The retrieval check runs the code-only reading (no model call).
"""
import re

import catalog
import terms
import verify

OBJECT_WORDS = (
    ('VirtualMachine', r'\b(vms?|virtual machines?|vcpus?|vmdks?|vnics?)\b'),
    ('HostSystem', r'\b(esxi?|hosts?|hypervisor|vmkernel|pcpus?|physical (core|cpu|thread)s?)\b'),
    ('ClusterComputeResource', r'\b(clusters?|drs|ha admission)\b'),
    ('Datastore', r'\bdatastores?\b'),
    ('ResourcePool', r'\bresource pools?\b'),
    ('guest', r'\b(guest( os)?|windows|linux|perfmon|task manager|iostat|vmstat|/proc)\b'),
)
OBJECT_PREFIX = re.compile(r'^(VM|ESXi|Guest OS|Cluster|Datastore|Resource pool|Host)\s+', re.I)
COUNTER_KEY = re.compile(r'\b([a-z]+\.[a-zA-Z]+(?:\.[a-zA-Z]+)?)\b')
TROUBLESHOOT = re.compile(r'\b(slow|troubleshoot\w*|what (do|should|would) (you|i|we) check|root cause|cause[sd]?|why (is|are|does|do)|'
                          r'complain\w*|drops?|dropped|fail\w*|spike\w*|high|degrad\w*)\b', re.I)  # the troubleshooting words: flow tier without a case


def _tok(text):
    return len(text) // 4


def objects_in(question):
    """Object types the question names (guest = the Guest OS layer)."""
    return {o for o, p in OBJECT_WORDS if re.search(p, question, re.I)}


def _labels(docs):
    """Phrases that name a metric file: the title without its object word and parenthesis, the parenthesis itself,
    and the label without its technology word when that word names at most two files (Ready, Co-stop; not Usage)."""
    rows = []
    for d in docs.values():
        if d.meta.get('retriever_guide') != 'metric-meaning':
            continue
        title = d.title
        paren = re.findall(r'\(([^)]*)\)', title)
        core = OBJECT_PREFIX.sub('', re.sub(r'\s*\([^)]*\)', '', title)).strip()
        phrases = [core] + [p for p in paren if len(p.split()) >= 2 and not re.search(r'legacy|avoid|vcf operations|%', p, re.I)]
        rows.append((d.id, phrases, core))
    short = {}
    for i, _, core in rows:
        w = re.sub(r'^(CPU|Memory|Disk|Network|Storage)\s+', '', core, flags=re.I)
        if w != core:
            short.setdefault(w.lower(), []).append(i)
    out = []
    for i, phrases, core in rows:
        w = re.sub(r'^(CPU|Memory|Disk|Network|Storage)\s+', '', core, flags=re.I)
        extra = [w] if w != core and len(short.get(w.lower(), [])) <= 2 and len(w) > 3 else []
        out.append((i, [p for p in phrases + extra if len(p) > 3]))
    return out


_LABELS = {}


def anchors(docs, question, objs=None, strict=False):
    """Metric files the question names exactly: by title phrase or vCenter counter key, kept when the file's object
    is one the question names (or the question names none). strict: only phrases of two or more words or a hyphenated
    word (CPU Ready, Co-stop), for free text such as a draft answer, where one plain word (Throughput, System,
    Performance) is ordinary English."""
    key = (id(docs), strict)
    if key not in _LABELS:
        _LABELS[key] = [(i, [re.compile(r'(?<![\w-])' + re.escape(p) + r'(?![\w-])', re.I) for p in ps
                             if not strict or len(p.split()) >= 2 or '-' in p]) for i, ps in _labels(docs)]
    objs = objects_in(question) if objs is None else objs
    found = []
    for i, pats in _LABELS[key]:
        if any(p.search(question) for p in pats):
            fo = set(docs[i].meta.get('object') or []) or ({'guest'} if i.startswith('guest-os/') else set())
            if not objs or not fo or fo & objs:
                found.append(i)
    cat = catalog.get(docs)
    for k in dict.fromkeys(COUNTER_KEY.findall(question)):
        if k.split('.')[0].lower() in ('cpu', 'mem', 'disk', 'net', 'datastore', 'virtualdisk', 'sys', 'power', 'rescpu', 'storageadapter', 'storagepath', 'gpu'):
            for r in cat.lookup(k).get('counters', [])[:2]:
                if r.get('kb') and r['kb'] in docs and r['kb'] not in found:
                    found.append(r['kb'])
    return found


PART = re.compile(r'^\s*([^:\n]{2,40}):\s*$')                       # 'ESXi 01:' heads a list of options
OPTION_LINE = re.compile(r'^\s*(?:[-*]\s+)?([A-J])\.\s+(.*\S)\s*$')    # 'A. text' or '- A. text'
NOT_A_CLAIM = re.compile(r'^(unsure|not covered|it depends)\b', re.I)


def claims(question):
    """The parts a question asks to decide: each option of a multiple-choice question (Unsure left out), prefixed by
    its part when the question has several option lists ('ESXi 01: E. 40 threads'); otherwise the sentences that
    end in a question mark."""
    out, part = [], ''
    for line in question.split('\n'):
        m = OPTION_LINE.match(line)
        if m:
            if not NOT_A_CLAIM.match(m.group(2)):
                out.append(f'{part}: {m.group(2)}' if part else m.group(2))
            continue
        pm = PART.match(line)
        if pm:
            part = pm.group(1).strip()
    if out:
        return list(dict.fromkeys(out))
    return [s.strip() for s in re.findall(r'[^.?!\n]*\?', question) if len(s.split()) >= 4]


def _stem(question):
    """The question without its options: the last sentence that asks, for context of short claims."""
    body = '\n'.join(l for l in question.split('\n') if not OPTION_LINE.match(l))
    asks = [s.strip() for s in re.findall(r'[^.?!\n]*\?', body)]
    return asks[-1] if asks else ''


FLOW_KINDS = ('troubleshooting', 'health-check', 'decision-tree')


def case_files(docs, case):
    """Files the model's case names: each metric through the catalog (the best metric file for its name and object)
    and through the title phrases; a name that does not resolve plans nothing."""
    if not case:
        return []
    cat, out = catalog.get(docs), []
    for m in case.get('metrics') or []:
        name = str(m.get('name') or '').strip()
        if not name:
            continue
        obj = catalog.norm_object(m.get('object')) if m.get('object') else None
        hit = cat.lookup(name, obj if obj in catalog.OBJECT_ALIASES.values() else None)
        out += [r['id'] for r in hit.get('metric_files', [])[:1]] + [r['kb'] for r in hit.get('counters', [])[:1] if r.get('kb')]
    text = ' '.join(str(m.get('name') or '') for m in case.get('metrics') or [])
    out += anchors(docs, text, objects_in(' '.join(map(str, case.get('objects') or []))) or None) if text else []
    return [i for i in dict.fromkeys(out) if i in docs]


def plan(retriever, question, cfg, case=None):
    """Ordered tiers of file ids for one question. case: the model's reading (agent.py, stage 1) or None.
    Returns (tiers, matched term rows, search hits)."""
    docs = retriever.docs
    matched = terms.match(question) if cfg.get('term_map', True) else []
    hits = retriever.search(terms.query(question, matched), k=cfg.get('search_k', 6))
    top = [h['id'] for h in hits]
    tiers = {'flow': [], 'named': [], 'search': top[:3], 'mechanism': [], 'claims': [], 'search_rest': top[3:], 'more': []}
    kind = (case or {}).get('kind')
    flow_kind = kind if kind in FLOW_KINDS else ('troubleshooting' if TROUBLESHOOT.search(question) and kind in (None, '') else None)
    if flow_kind:
        tiers['flow'] = [h['id'] for h in retriever.search(question, filters={'retriever_guide': flow_kind}, k=2, min_hits=1)
                         if docs.get(h['id']) and docs[h['id']].meta.get('retriever_guide') == flow_kind][:1]
    tiers['named'] = terms.files(matched, docs, cfg.get('term_map_files', 2)) + anchors(docs, question) + case_files(docs, case)
    stem = _stem(question)
    second = []
    found = claims(question)
    for c in (case or {}).get('claims') or []:
        if isinstance(c, str) and c.strip() and not verify.options(question)[0] and c not in found:
            found.append(c.strip())   # an open question: the parts the model read; options are taken from the text
    for c in found[:cfg.get('plan_claims_max', 10)]:
        q = c if len(c.split()) >= 8 or not stem else f'{stem} {c}'
        ids = [h['id'] for h in retriever.search(q, k=2)]
        tiers['claims'] += ids[:1]
        second += ids[1:2]
    base = tiers['named'] + top[:2]
    for i in base:
        tiers['mechanism'] += [x['id'] for x in retriever.links(i, 'same_name')]
        tiers['mechanism'] += [x['id'] for x in retriever.links(i, 'internal_derive')][:cfg.get('plan_derive_n', 3)]
    for h in top[:2]:
        tiers['more'] += [x['id'] for x in retriever.links(h, 'related')][:2]
    tiers['more'] = second + tiers['more']
    return tiers, matched, hits


ORDER = ('flow', 'named', 'search', 'mechanism', 'claims', 'search_rest', 'more')
WHOLE = ('flow', 'named', 'search')  # read in full; the other tiers give their best sections (cfg plan_section_tokens)


def sections_of(retriever, doc_id, query, cap):
    """The best sections of one file for a query, within cap tokens (the gap follow-up of agent.py, stage 6)."""
    return _sections(retriever, doc_id, retriever.bm25.scores(query), cap)


def _sections(retriever, doc_id, scores, cap):
    """The best sections of one file for the question, in file order, within cap tokens (at least the best one)."""
    idx = [n for n, c in enumerate(retriever.chunks) if c.doc.id == doc_id]
    best = sorted(idx, key=lambda n: -scores[n])
    keep, used = [], 0
    for n in best:
        t = _tok(retriever.chunks[n].text)
        if keep and used + t > cap:
            continue
        keep.append(n)
        used += t
    d = retriever.docs[doc_id]
    body = '\n\n'.join(d.sections[idx.index(n)][1] for n in sorted(keep))
    return f'### {d.title} (sections)\nid: {d.id} | status: {d.status}\n{body}'


def reading_set(retriever, question, cfg, budget=None, case=None):
    """The reading set: (text, ids used in order, search hits, tier of each id)."""
    tiers, matched, hits = plan(retriever, question, cfg, case)
    ids, whole = [], set()
    for t in ORDER:
        for i in tiers[t]:
            if i in retriever.docs and i not in ids:
                ids.append(i)
                if t in WHOLE:
                    whole.add(i)
    budget, parts, used = budget or cfg['context_tokens'], [], []
    notes = terms.block(matched)
    if notes:
        parts.append(notes)
        budget -= _tok(notes)
    facts = catalog.get(retriever.docs).facts_for(ids) if cfg.get('catalog_facts', True) else ''
    if facts:
        parts.append(facts)
        budget -= _tok(facts)
    cap = cfg.get('plan_section_tokens', 0)
    scores = retriever.bm25.scores(question) if cap else None
    for i in ids:
        d = retriever.docs[i]
        block = f'### {d.title}\nid: {d.id} | status: {d.status}\n{d.body}'
        if cap and (i not in whole or _tok(block) > budget):
            block = _sections(retriever, i, scores, min(cap, budget) if i not in whole else budget)
        if _tok(block) > budget:
            block = block[:budget * 4]
        parts.append(block)
        used.append(i)
        budget -= _tok(block)
        if budget <= 200:
            break
    tier_of = {}
    for t in ORDER:
        for i in tiers[t]:
            tier_of.setdefault(i, t)
    return '\n\n'.join(parts), used, hits, {i: tier_of.get(i) for i in used}
