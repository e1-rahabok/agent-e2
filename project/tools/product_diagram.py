"""Draw images/product-architecture.svg: the Product diagram of ARCHITECTURE.md (agent, harness, knowledge, model).

Hand-laid SVG, so the layers stay in place; Mermaid's automatic layout tangles at this size.
Run from the repository root after a change to harness/ that the diagram shows:
    python3 project/tools/product_diagram.py
"""
import os
import sys
from xml.sax.saxutils import escape

W, H = 1960, 1420
LH = 15  # line height
out = []

C = {
    'know': ('#e6f4e4', '#2e7d32', '#173a16'),
    'tool': ('#efe9f8', '#5e35b1', '#2a1650'),
    'stage': ('#e4edfa', '#1f5fae', '#0d2a4d'),
    'model': ('#fdebd3', '#c25e00', '#4a2400'),
    'data': ('#f2f2f2', '#666666', '#222222'),
    'notyet': ('#f8f8f8', '#9a9a9a', '#666666'),
    'out': ('#ffffff', '#888888', '#444444'),
}


def t(x, y, s, size=12, weight='normal', fill='#222', anchor='start', style=''):
    out.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
               f'text-anchor="{anchor}"{style}>{escape(s)}</text>')


def box(x, y, w, title, lines, kind, h=None, dash=False, rx=6, mono_title=False, title_size=13):
    fill, stroke, ink = C[kind]
    h = h or (26 + LH * len(lines) + 8)
    d = ' stroke-dasharray="6 4"' if dash or kind == 'notyet' else ''
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1.4"{d}/>')
    t(x + 9, y + 18, title, title_size, 'bold', ink, style=' font-family="ui-monospace,Menlo,Consolas,monospace"' if mono_title else '')
    for n, ln in enumerate(lines):
        t(x + 9, y + 36 + n * LH, ln, 11.5, 'normal', ink)
    return (x, y, w, h)


def band(y, h, label, sub, fill):
    out.append(f'<rect x="10" y="{y}" width="{W - 20}" height="{h}" rx="10" fill="{fill}" stroke="#c9c9c9"/>')
    t(24, y + 24, label, 15, 'bold', '#333')
    if sub:
        for n, s in enumerate(sub):
            t(24, y + 42 + n * 14, s, 11, 'normal', '#555')


def arrow(pts, kind='flow', label=None, lx=None, ly=None, anchor='middle'):
    style = {
        'flow': ('#1f5fae', '1.6', '', 'a-flow'),
        'tool': ('#5e35b1', '1.3', ' stroke-dasharray="5 4"', 'a-tool'),
        'call': ('#c25e00', '3', '', 'a-call'),
        'data': ('#555555', '1.4', '', 'a-data'),
        'grey': ('#8a8a8a', '1.3', ' stroke-dasharray="5 4"', 'a-data'),
        'back': ('#1f5fae', '1.4', ' stroke-dasharray="7 4"', 'a-flow'),
    }[kind]
    d = 'M ' + ' L '.join(f'{x} {y}' for x, y in pts)
    out.append(f'<path d="{d}" fill="none" stroke="{style[0]}" stroke-width="{style[1]}"{style[2]} marker-end="url(#{style[3]})"/>')
    if label:
        lines = label.split('\n')
        for n, s in enumerate(lines):
            wpx = len(s) * 6.0 + 6
            yy = ly + n * 13
            xx = lx - wpx / 2 if anchor == 'middle' else lx - 3 if anchor == 'start' else lx - wpx + 3
            out.append(f'<rect x="{xx:.0f}" y="{yy - 10}" width="{wpx:.0f}" height="13" fill="#ffffff" opacity="0.9"/>')
            t(lx, yy, s, 10.5, 'normal', style[0], anchor)


# ---------------------------------------------------------------- canvas
out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif">')
out.append('<defs>')
for mid, col in (('a-flow', '#1f5fae'), ('a-tool', '#5e35b1'), ('a-call', '#c25e00'), ('a-data', '#555555')):
    out.append(f'<marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
               f'<path d="M0,0 L10,5 L0,10 z" fill="{col}"/></marker>')
out.append('</defs>')
out.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')

t(24, 34, 'Agent E2, Product: how the agent and the harness drive the model and use the knowledge', 20, 'bold', '#111')
t(24, 54, 'Code leads, the model reads. Code decides what to read, compute and ask; the model is called 2 times in the common case, '
          '4 at most, plus consensus samples. One pipeline for every question.', 12.5, 'normal', '#444')

# column x positions
X0, X1, X2, X3, X4, X5, X6, X7 = 30, 245, 470, 755, 980, 1185, 1430, 1645
W0, W1, W2, W3, W4, W5, W6, W7 = 190, 200, 260, 200, 180, 220, 190, 285

# ---------------------------------------------------------------- knowledge band
band(70, 165, 'knowledge/', ['The only folder the harness', 'reads at run time.', 'Indexed; Level 400.',
                             'Text the model reads and', 'the map the code plans with.'], '#f5fbf4')
yk = 92
box(X1, yk, W1, 'Knowledge files *.md', ['metric, concept, mechanism, flow', 'body split by ## heading',
                                         '## Misconceptions:', 'lines marked up_front', 'KPI files: colour bands'], 'know')
box(X2, yk, W2, '## Metadata (yaml): the map', ['same_name, internal_derive, related', 'retriever_guide: health-check,',
                                                 'troubleshooting, decision-tree', 'flows: ## Checks, in order', 'object, status, images'], 'know')
box(X3, yk, W3 + 30, 'catalog/*.yaml', ['vcenter-counters, vcenter-api-counters', 'esxtop-fields, objects',
                                       'thresholds-performance,', 'thresholds-capacity (planning-*),', 'thresholds-alerts'], 'know')
box(X4 + 15, yk, W4 + 25, 'catalog/user-terms.yaml', ['user words to KB terms', 'and files', 'misconception note',
                                                      'premise flag, product label'], 'know')
box(X5 + 40, yk, W5 - 10, 'glossary.md', ['preferred word per concept', 'Also called, Not to confuse with',
                                          'Product label, Invites,', 'Better name'], 'know')
# legend
lx, ly = 1500, 88
t(lx, ly + 4, 'Legend', 12.5, 'bold', '#333')
items = [('know', 'knowledge (data the harness reads)'), ('tool', 'harness tool (code, exact)'), ('stage', 'agent stage (code decides)'),
         ('model', 'model endpoint'), ('data', 'data passed between stages'), ('notyet', 'built, not yet called')]
for n, (k, s) in enumerate(items):
    f, st, _ = C[k]
    yy = ly + 14 + n * 19
    d = ' stroke-dasharray="4 3"' if k == 'notyet' else ''
    out.append(f'<rect x="{lx}" y="{yy}" width="22" height="13" rx="3" fill="{f}" stroke="{st}"{d}/>')
    t(lx + 30, yy + 11, s, 11, 'normal', '#333')
lx2 = 1730
for n, (k, s) in enumerate([('flow', 'pipeline order'), ('call', 'model call (numbered)'), ('tool', 'code calls a tool'),
                            ('data', 'data flow'), ('back', 'loop back (bounded)')]):
    yy = ly + 20 + n * 19
    arrow([(lx2, yy), (lx2 + 34, yy)], k)
    t(lx2 + 42, yy + 4, s, 11, 'normal', '#333')

# ---------------------------------------------------------------- tools band
band(250, 265, 'harness/: tools', ['Built at start-up; called', 'only by code, never the model.'], '#faf8fd')
arrow([(1000, 237), (1000, 252)], 'data')
t(1008, 248, 'loaded once at start-up: files to chunks and links; YAML and KPI bands to SQLite; term rows; up-front block', 10.5, 'normal', '#555')

yb1, yb2 = 268, 392
box(X1, yb1, W1, 'knowledge_loader.py', ['load knowledge/**/*.md', 'split at ## Metadata', 'chunk by ##, prefix title + id',
                           'drop Mermaid and link paths', 'glossary entries'], 'tool', mono_title=True)
box(X2, yb1, W2, 'knowledge_search.py', ['Retriever: BM25 + embeddings,', 'reciprocal rank fusion', 'search(query, filters, k)',
                                  'links / backlinks by type', 'vectors cached in .cache/'], 'tool', mono_title=True)
box(X3, yb1, W3, 'catalog_database.py', ['SQLite in memory', 'lookup: counter, label, esxtop', 'facts_for(ids): unit, rollup,',
                                'stats level, thresholds, bands', 'object relations and paths'], 'tool', mono_title=True)
box(X4, yb1, W4 + 10, 'user_clarification.py', ['ASK_RULE (kind chat)', 'FINAL_RULE (chat_final)', 'parse CLARIFY:',
                                     'at most 3 questions'], 'tool', mono_title=True)
box(X5, yb1, W5, 'upfront_knowledge.py', ['up-front block, 3K tokens max', 'misconceptions marked up_front',
                               'confusable pairs (glossary)'], 'tool', mono_title=True)
box(X6, yb1, W6, 'model_client.py', ['the model client', '(see the model band)'], 'tool', mono_title=True, dash=False)
box(X7, yb1, W7, 'answer_check.py', ['hard: no ANSWER line, letter not an', 'option, Unsure mixed: one repair',
                               'soft: no REASON, unknown file id,', 'ungrounded number: recorded only'], 'tool', mono_title=True)

box(X2, yb2, W2 - 50, 'user_terms.py', ['match: rows ranked by hits', 'case_labels: from screenshots', 'query words, files, notes'],
    'tool', mono_title=True)
box(X3 - 43, yb2, W3 + 8, 'arithmetic_calculator.py', ['safe arithmetic (ast)', 'summation_to_percent,', 'units, cpu_states',
                                  'result names its source'], 'tool', mono_title=True)
box(X4, yb2, 170, 'flow_executor.py', ['steps of a flow file', 'executable steps: Q166'], 'notyet', h=64, mono_title=True, title_size=12)
box(X4, yb2 + 70, 170, 'capacity_calculator.py', ['planning calculator'], 'notyet', h=48, mono_title=True, title_size=12)
box(X5, yb2, W5, 'public_web_lookup.py', ['URLs in the question: fetch', 'current-fact words: vendor search', 'system names dropped,',
                            'private IPs refused, trim 2K'], 'tool', mono_title=True)

# operator / runner in col 0 of tools band
box(X0, 330, W0, 'Operator', ['question, screenshots, links', 'benchmark runner (Proof):', 'same path, kind choice,', 'same budgets'], 'out', rx=14)

# ---------------------------------------------------------------- agent band
band(530, 470, 'Agent', ['harness/expert_agent.py,', 'reading_plan.py, answer_modes.py', '', 'prepare: stages 1-4,', 'once per question',
                         'write: stages 5-6,', 'once per sample'], '#f6f9fe')
ys = 562
box(X0, 680, W0, 'answer_modes.converse', ['turn 1: kind chat', 'turn 3: question + asked', '+ reply, kind chat_final',
                                    'answer_modes.answer(', 'agent-e2), kind: choice,', 'open, chat, chat_final'], 'stage', mono_title=True)
s1 = box(X1, ys, W1, '1 Understand', ['expert_agent.understand', 'model reads question + images', 'into the case: JSON schema',
                                      'UNDERSTAND, temperature 0', 'parse_case: known fields only;', 'not JSON: code-only case',
                                      'reading_plan.objects_in: code', 'reads object words, always'], 'stage')
s2 = box(X2, ys, W2, '2 Plan: reading_plan.reading_set', ['code only; same question, same set',
                                                    'T1 Flow: best file of the case kind,', '    filter retriever_guide; whole',
                                                    'T2 Named: term rows, titles, counter', '    keys, case metrics; first 3 whole',
                                                    'T3 Search: hits 1-3, whole (k 10)', 'T4 Mechanism: same_name and',
                                                    '    internal_derive (8) of named,', '    top 2 hits and the flow',
                                                    'T5 Claims: one search per option,', '    at most 20',
                                                    'T6 Rest: hits 4-10, 2nd claim hit,', '    related: 4 out + 4 back',
                                                    'Pack 32K in tier order: term notes,', 'catalog facts, then files whole',
                                                    'or best sections, 400 tokens each'], 'stage')
s3 = box(X3, ys, W3, '3 Compute (exact)', ['expert_agent.compute, before', 'the model reads: counter in ms',
                                           '+ chart interval (20 s, 300 s,', '1,800 s, 7,200 s, 1 day)',
                                           '+ vCPUs: % of one vCPU and', '% per vCPU, with source',
                                           'expert_agent.coverage: weak', 'when no flow and no named file',
                                           'to build: flow path, band', 'verdict, capacity plan'], 'stage')
s4 = box(X4, ys, W4, '4 Ask? (kind chat)', ['allowed when the case has', 'a missing fact or a premise,',
                                            'or a premise term row hits', 'yes: prompt chat, model', 'may reply CLARIFY:',
                                            'no: prompt chat_final', 'choice, open: never ask'], 'stage')
s5p = box(X5, ys, W5, 'Prompt', ['system: rules by kind', '+ ANSWER_RULES', '+ OPEN_SHAPE (open kinds)',
                                 '+ LABEL_ORDER (label hit)', '+ up-front block', 'user: case JSON, Computed',
                                 '(exact), coverage note,', 'Knowledge base: reading set,', 'web block (untrusted),',
                                 'question + images', 'over_window: flag > 128K'], 'stage')
s5 = box(X6, ys, W6, '5 Answer', ['expert_agent.write', 'card sampling, 4,000', 'tokens max', 'ANSWER + REASON,',
                                  'a file id per claim;', 'knowledge base first,', 'it wins on conflict'], 'stage')
s6 = box(X7, ys, W7, '6 Check', ['expert_agent.gaps: the draft names a', 'metric file not in the reading set:',
                                 'add its best sections', '(reading_plan.sections_of, at most', '2 files), answer again',
                                 'answer_check.check (kind choice): a hard', 'issue gets one repair turn',
                                 'grounding: numbers and file ids'], 'stage')

# consensus diamond
cx, cy = X7 + W7 / 2, 830
out.append(f'<polygon points="{cx},{cy - 52} {cx + 140},{cy} {cx},{cy + 52} {cx - 140},{cy}" fill="#e4edfa" stroke="#1f5fae" stroke-width="1.4"/>')
t(cx, cy - 18, 'Consensus, kind choice', 12.5, 'bold', '#0d2a4d', 'middle')
t(cx, cy - 2, 'answer_modes._consensus: n samples', 11.5, 'normal', '#0d2a4d', 'middle')
t(cx, cy + 13, 'on one reading set', 11.5, 'normal', '#0d2a4d', 'middle')
t(cx, cy + 28, 'same letters?', 11.5, 'normal', '#0d2a4d', 'middle')

# data artefacts
yd = 865
case = box(X1 + 30, yd, W1 - 30, 'Case', ['kind, objects, metrics', '(value, unit, interval,', 'tool), vcpus, symptom,',
                                          'premise, claims, missing'], 'data')
rs = box(X2, yd, W2, 'Reading set', ['text within 32K tokens', 'ids used, tier of each id'], 'data')
cf = box(X3, yd, W3, 'Computed (exact)', ['lines with source file', 'coverage: weak or named'], 'data')

# ---------------------------------------------------------------- model band
band(1030, 200, 'Model', ['harness/model_client.py:', 'the only place the', 'endpoint differs between', 'benchmark and site'], '#fffaf3')
cl = box(X1, 1062, 470, 'model_client.py client', ['GatewayClient: benchmark, Vercel AI Gateway',
                                          'local OpenAI-compatible server at the site', 'ParamClient: the model card sampling',
                                          'deterministic=True: temperature 0 (the case)', 'MockClient: unit tests, offline'], 'model', mono_title=True)
box(X3 - 15, 1062, 225, 'Open-weight vision LLM', ['enterprise GPU, up to 4', 'vLLM, llama.cpp or Ollama',
                                                    'context window 128K', 'reads screenshot pixels'], 'model', rx=16)
box(X4 + 30, 1062, 175, 'Embedding model', ['qwen3-embedding-0.6b', 'on CPU, for hybrid', 'search (knowledge_search.py)'], 'model', rx=16)

# ---------------------------------------------------------------- outputs
yo = 1048
box(X5 + 30, yo, 190, 'Trace, per answer', ['understand, plan by tier,', 'compute, coverage, ask, web,', 'answer, gap, verify, repair,',
                                             'consensus, context_over;', 'written by every step'], 'data', rx=14)
box(X6 + 10, yo + 92, 200, 'Clarifying questions', ['answer starts CLARIFY: (chat)', 'one round, at most 3', 'reply: turn 3 via converse'], 'out')
box(X7 + 20, yo + 100, 125, 'Answer', ['file ids, computed', 'facts, ids read'], 'out')
box(X7 + 155, yo + 100, 125, 'Unsure', ['not settled:', 'samples disagree'], 'out')

# ---------------------------------------------------------------- arrows: pipeline order
yp = 600
arrow([(X0 + W0 / 2, 330 + 94), (X0 + W0 / 2, 680)], 'flow')          # runner -> entry (passes operator? no: runner below operator)
arrow([(X0 + W0 + 0, 720), (X1 - 2, 720)], 'flow')                     # entry -> S1
arrow([(X1 + W1, yp), (X2 - 2, yp)], 'flow')
arrow([(X2 + W2, yp), (X3 - 2, yp)], 'flow')
arrow([(X3 + W3, yp), (X4 - 2, yp)], 'flow')
arrow([(X4 + W4, yp), (X5 - 2, yp)], 'flow')
arrow([(X5 + W5, yp), (X6 - 2, yp)], 'flow')
arrow([(X6 + W6, yp), (X7 - 2, yp)], 'flow')
arrow([(cx, s6[1] + s6[3]), (cx, cy - 53)], 'flow')
# consensus loop to S5
arrow([(cx - 140, cy), (X6 + W6 / 2, cy), (X6 + W6 / 2, s5[1] + s5[3] + 2)], 'back', 'next sample:\nstages 5-6 again',
      X6 + W6 / 2 + 6, cy + 18, 'start')
# consensus -> outputs
arrow([(cx - 40, cy + 40), (X7 + 82, yo + 98)], 'flow', 'agreed, or n = 1', X7 + 22, 935, 'start')
arrow([(cx + 40, cy + 40), (X7 + 217, yo + 98)], 'flow', 'disagree or Unsure', X7 + 200, 935, 'start')
# answer -> clarifying
arrow([(X7 + 20, yo + 135), (X6 + 212, yo + 135)], 'flow')
# clarifying -> back to operator (bottom left loop)
arrow([(X6 + 110, yo + 166), (X6 + 110, 1255), (18, 1255), (18, 360), (X0 - 2, 360)], 'back',
      'user replies: turn 3, kind chat_final', 700, 1251, 'middle')
# answer -> operator
# operator -> entry

# S1 -> case, case -> plan, plan -> RS, RS/CF/case -> prompt bus
arrow([(X1 + 115, s1[1] + s1[3]), (X1 + 115, yd - 2)], 'data')
arrow([(X1 + W1, yd + 20), (X2 - 2, s2[1] + s2[3] - 30)], 'data')
arrow([(X2 + 130, s2[1] + s2[3]), (X2 + 130, yd - 2)], 'data')
arrow([(X2 + W2, yd + 30), (X3 - 2, yd + 30)], 'data')
ybus = 985
for bx, bot in ((X1 + 110, yd + case[3]), (X2 + 130, yd + rs[3]), (X3 + 100, yd + cf[3])):
    out.append(f'<path d="M {bx} {bot} L {bx} {ybus}" fill="none" stroke="#555" stroke-width="1.4"/>')
arrow([(X1 + 110, ybus), (X5 + 110, ybus), (X5 + 110, s5p[1] + s5p[3] + 2)], 'data',
      'case, reading set, computed facts into the prompt', 830, ybus - 5)
arrow([(X3 + 100, s3[1] + s3[3]), (X3 + 100, yd - 2)], 'data')

# ---------------------------------------------------------------- arrows: tools used by code
arrow([(X1 + W1, yb1 + 40), (X2 - 2, yb1 + 40)], 'tool')  # kb -> retrieval
arrow([(X2 + W2 - 30, yb1 + 104), (X2 + W2 - 30, ys - 2)], 'tool', 'search, links', X2 + W2 - 34, 545, 'end')
arrow([(X2 + 100, yb2 + 79), (X2 + 100, ys - 2)], 'tool', 'words, labels', X2 + 106, 515, 'start')
arrow([(X3 + W3 - 25, yb1 + 104), (X3 + W3 - 25, 500), (X2 + W2 - 8, 500), (X2 + W2 - 8, ys - 2)], 'tool', 'counter keys, facts_for', X3 + 60, 496, 'middle')
arrow([(X3 + W3 - 25, 500), (X3 + W3 - 25, ys - 2)], 'tool', 'lookup', X3 + W3 - 29, 545, 'end')
arrow([(X3 + 90, yb2 + 94), (X3 + 90, ys - 2)], 'tool', 'summation_to_percent', X3 + 84, 522, 'end')
arrow([(X4 + 40, yb2 + 118), (X3 + W3 - 6, ys - 2)], 'grey', 'to build', X4 + 30, 545, 'start')
arrow([(X4 + W4 - 3, yb1 + 92), (X4 + W4 - 3, ys - 2)], 'tool', 'ask rule', X4 + W4 - 8, 545, 'end')
arrow([(X5 + W5 - 10, yb1 + 77), (X5 + W5 - 10, ys - 2)], 'tool')
t(X5 + W5 - 14, 545, 'up-front', 10.5, 'normal', '#5e35b1', 'end')
arrow([(X5 + 100, yb2 + 94), (X5 + 100, ys - 2)], 'tool', 'pages', X5 + 106, 515, 'start')
arrow([(X7 + 140, yb1 + 92), (X7 + 140, ys - 2)], 'tool', 'issues, repair prompt', X7 + 146, 515, 'start')
# retrieval -> check (sections_of): route along tools band bottom


# ---------------------------------------------------------------- arrows: model calls
xc1 = X1 + 14
arrow([(xc1, s1[1] + s1[3]), (xc1, 1060)], 'call', '1 the case', xc1 + 5, 1015, 'start')
ycall = 1005
arrow([(X6 + 30, s5[1] + s5[3]), (X6 + 30, ycall), (X1 + 420, ycall), (X1 + 420, 1060)], 'call')
t(X6 + 36, ycall - 50, '2 the draft', 10.5, 'bold', '#c25e00')
out.append(f'<path d="M {X7 + 12} {s6[1] + s6[3]} L {X7 + 12} {ycall} L {X6 + 30} {ycall}" fill="none" stroke="#c25e00" stroke-width="3"/>')
t(X7 + 18, s6[1] + s6[3] + 16, '3 gap, once', 10.5, 'bold', '#c25e00')
t(X7 + 18, s6[1] + s6[3] + 29, '4 repair, once', 10.5, 'bold', '#c25e00')
arrow([(X1 + 470, 1110), (X3 - 17, 1110)], 'call')
arrow([(X1 + 470, 1150), (X1 + 470 + 30, 1150), (X1 + 470 + 30, 1200), (X4 + 30 + 80, 1200), (X4 + 30 + 80, 1062 + 104)], 'data',
      'embed', X3 + 100, 1196, 'middle')

# footer
t(24, 1290, 'Notes', 13, 'bold', '#333')
notes = [
    'Stages 1-4 run once per question (expert_agent.prepare), so every consensus sample reads the same reading set: a disagreement is doubt in the reasoning, not a different search.',
    'The model never chooses a file or a tool. It reads the question into the case (call 1) and the reading set into the answer (call 2). Calls 3 and 4 fire only on a gap or a hard verifier issue.',
    'Tiers T1-T3 are read whole (named: the first 3), the rest as their best sections; the order is the priority when the 32K budget runs out. Settings: search_k, context_tokens, plan_* in the runner config.',
    'Dashed grey: flow_executor.py (executable flow steps, Q166) and capacity_calculator.py (planning calculator) are built and unit-tested; wiring them into stage 3 is open work (harness/AGENT.md, section 7).',
    'Same code for benchmark and site: only the endpoint in model_client.py differs. public_web_lookup.py sends only public requests; customer data stays on site.',
]
for n, s in enumerate(notes):
    t(24, 1310 + n * 17, '- ' + s, 11.5, 'normal', '#444')

out.append('</svg>')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'images', 'product-architecture.svg')
with open(path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(out) + '\n')
