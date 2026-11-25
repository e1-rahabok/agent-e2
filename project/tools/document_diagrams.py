"""Draw the diagrams of the root documents as hand-laid SVG, for human readers.

KNOWLEDGE-ENGINEERING.md: knowledge-workflow, knowledge-paths, file-as-model-sees, source-to-reviewed.
ARCHITECTURE.md: agent-e2-in-pcm, repository-groups.
Knowledge files keep Mermaid (lint checks a chart against its numbered steps); these documents are not indexed.
Colours in these diagrams: green is knowledge, blue is agent and harness code, purple is a check or proof,
orange is the model, grey is a source or another system. Each diagram carries its own key.
Run from the repository root:
    python3 project/tools/document_diagrams.py
"""
import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import diagram_kit as k  # noqa: E402
from diagram_kit import t, box, frame, arrow, legend, begin, finish  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KEY = [('Knowledge', 'prod'), ('Agent and harness', 'method'), ('Model', 'guest'), ('Check or proof', 'shared'), ('Source or other system', 'data')]


def wrap(s, n):
    return textwrap.wrap(s, n)


def head(w, title, sub, key=KEY):
    begin(w, k.canvas['h'])
    t(24, 34, title, 20, 'bold', '#111')
    t(24, 54, sub, 12.5, 'normal', '#444')
    x = w - 24 - sum(20 + len(label) * 6.3 + 22 for label, _ in key) + 22
    legend(x, 74 - 8, key)


def start(w, h):
    k.canvas['h'] = h


def out_path(name):
    return os.path.join(ROOT, 'images', name)


# ------------------------------------------------------------------ 1. knowledge workflow
def knowledge_workflow():
    W, H = 1800, 600
    start(W, H)
    head(W, 'From expertise to knowledge the model reads',
         'Five stages. A wrong answer is traced to its cause and fixed at the source.',
         [('Source or other system', 'data'), ('Knowledge', 'prod'), ('Check or proof', 'shared'), ('Agent and harness', 'method'), ('Model', 'guest')])
    top, fh = 100, 420
    cols = [(30, 280), (350, 260), (650, 320), (1010, 310), (1360, 410)]
    heads = [('1  Sources', None), ('2  Source note', 'project/sources/'), ('3  Codify', 'One form per kind, one home per fact'),
             ('4  Check', None), ('5  Used by the AI', None)]
    for (x, w), (a, b) in zip(cols, heads):
        frame(x, top, w, fh, a, b)
    x, w = cols[0]
    for n, (a, ls) in enumerate([("Books, spreadsheets, diagrams", ["The author's own material."]),
                                 ('Documentation', ['Manuals, white papers, expert answers.']),
                                 ('Environment', ['Screenshots, API, GUI, lab tests.'])]):
        box(x + 12, top + 56 + n * 118, w - 24, a, ls, 'data', h=100)
    x, w = cols[1]
    box(x + 12, top + 56, w - 24, 'One note per topic', wrap('A few pages. Each claim about vendor behaviour, and each measured number, is tied to its evidence.', 34), 'data', h=150)
    x, w = cols[2]
    for n, (a, ls) in enumerate([('Markdown', ['Mechanisms, misconceptions, flows.']),
                                 ('Catalog YAML', ['Counters, thresholds, object model.']),
                                 ('Tags and links', ["The expert's map: which files are", 'read together.'])]):
        box(x + 12, top + 56 + n * 118, w - 24, a, ls, 'prod', h=100)
    x, w = cols[3]
    for n, (a, ls) in enumerate([('Lint', ['On every merge.']),
                                 ('Retrieval check and benchmark', wrap('Are the right files found, and does the whole system answer correctly?', 34)),
                                 ('Author review', ['Status reviewed: the gate of release 1.0.'])]):
        box(x + 12, top + 56 + n * 118, w - 24, a, ls, 'shared', h=100)
    x, w = cols[4]
    box(x + 12, top + 56, w - 24, 'Agent and harness', ['Five paths to the model.'], 'method', h=100)
    box(x + 12, top + 56 + 140, w - 24, 'Model', ['Reads, applies and answers with citations.'], 'guest', h=100)
    arrow([(x + w // 2, top + 56 + 100), (x + w // 2, top + 56 + 140)])
    for (x1, w1), (x2, _) in zip(cols, cols[1:]):
        arrow([(x1 + w1 + 2, top + 215), (x2 - 2, top + 215)])
    for n, line in enumerate(['Drafts are served with their status.', 'Release 1.0 ships only reviewed files.']):
        t(cols[4][0] + 14, top + fh - 50 + n * 15, line, 11.5, 'normal', '#444')
    ex = cols[4][0] + cols[4][1] // 2
    arrow([(ex, top + fh), (ex, top + fh + 60), (cols[1][0] + cols[1][1] // 2, top + fh + 60), (cols[1][0] + cols[1][1] // 2, top + fh + 2)],
          'a wrong answer is traced to a missing fact, a retrieval miss or a model error', 1000, top + fh + 56, '#1f5fae', dash=True)
    finish(out_path('knowledge-workflow.svg'))


# ------------------------------------------------------------------ 2. knowledge paths
def knowledge_paths():
    W, H = 1760, 720
    start(W, H)
    head(W, 'How a fact reaches the model',
         'Five paths. Each blocks a failure the others cannot. Each fact has one home.',
         [('Knowledge', 'prod'), ('Agent and harness code', 'method'), ('Model', 'guest'), ('Route and result', 'data')])
    xs = dict(path=30, home=400, route=770, result=1060)
    for key, label in (('path', 'Path and reason'), ('home', 'Home'), ('route', 'Route'), ('result', 'Reaches the model as')):
        t(xs[key], 112, label, 13, 'bold', '#222')
    rows = [
        ('1  Retrieved when a question needs it', 'Too large to send with every question: about 327K tokens.',
         ('prod', 'knowledge/**/*.md', ['Mechanisms, metrics, misconceptions, flows']), 'Search and links', 'The agent plans the reading set', 'Reading set'),
        ('2  Looked up exactly', "An exact value must not depend on ranking or on the model's memory.",
         ('prod', 'knowledge/catalog/*.yaml', ['Units, rollups, thresholds, user terms']), 'Lookup by key in SQLite', 'Loaded at start-up, not chunked', 'Exact values'),
        ('3  Given up front, every question', 'A confident wrong belief is never looked up, so the correction must be in place first.',
         ('prod', 'up_front lines and glossary.md', ['Widest misconceptions, confusable pairs']), 'upfront_knowledge.py', 'Builds the up-front block', 'Up-front block'),
        ('4  Executed as code', 'Small models slip on arithmetic and skip steps. Code does not.',
         ('method', 'harness/*.py', ['arithmetic_calculator, answer_check,', 'user_terms']), 'Code runs on the case', "Uses the case's values", 'Exact values'),
        ('5  Agent instructions', 'Conduct for every answer, not a fact about one metric.',
         ('method', 'answer_modes.py, expert_agent.py', ['Knowledge base first, threshold only', 'with its source, Unsure']), 'Prompt rules', 'Added to every question', 'Every answer'),
    ]
    ry, rh, gap = 126, 100, 14
    for n, (name, why, (hk, ht, hl), r1, r2, res) in enumerate(rows):
        y = ry + n * (rh + gap)
        box(xs['path'], y, 340, name, wrap(why, 50), 'data', h=rh)
        box(xs['home'], y, 340, ht, hl, hk, h=rh, mono=True)
        box(xs['route'], y, 260, r1, wrap(r2, 34), 'data', h=rh)
        box(xs['result'], y, 220, res, [], 'data', h=rh)
        arrow([(xs['path'] + 342, y + rh // 2), (xs['home'] - 2, y + rh // 2)])
        arrow([(xs['home'] + 342, y + rh // 2), (xs['route'] - 2, y + rh // 2)])
        arrow([(xs['route'] + 262, y + rh // 2), (xs['result'] - 2, y + rh // 2)])
        arrow([(xs['result'] + 222, y + rh // 2), (1352, y + rh // 2)])
    box(1354, ry, 180, 'Model', ['Reads the reading set,', 'the exact values, the', 'up-front block and', 'the rules.'], 'guest', h=5 * rh + 4 * gap)
    box(1570, ry + 2 * (rh + gap), 170, 'Answer', ['With file citations.'], 'method', h=rh)
    arrow([(1536, ry + 2 * (rh + gap) + rh // 2), (1568, ry + 2 * (rh + gap) + rh // 2)])
    finish(out_path('knowledge-paths.svg'))


# ------------------------------------------------------------------ 3. what the model sees of a file
def file_as_model_sees():
    W, H = 1500, 580
    start(W, H)
    head(W, 'What the model sees of a file',
         'A ## section is the unit of retrieval. Metadata is read by code and never embedded.',
         [('Part of a knowledge file', 'prod'), ('Harness', 'method'), ('Not used by the model', 'data')])
    frame(30, 100, 340, 440, 'One knowledge file')
    parts = [('# Title', 'prod'), ('## Sections', 'prod'), ('## Misconceptions', 'prod'), ('Mermaid chart', 'prod')]
    for n, (a, kind) in enumerate(parts):
        box(42, 134 + n * 54, 316, a, [], kind, h=44, mono=True)
    box(42, 354, 316, '## Metadata (yaml, last)', [], 'prod', h=174, mono=True)
    meta_y = [404, 432, 460, 488]
    for y, s in zip(meta_y, ['tags', 'links', 'up_front', 'status, source, review_notes, corrections']):
        t(56, y, s, 11.5, 'normal', '#173a16', mono=True)
    box(520, 134, 400, 'Chunks', ['One chunk per ## section. Each chunk starts', 'with Title (id) > Heading.'], 'method', h=152)
    arrow([(360, 156), (518, 156)]); arrow([(360, 210), (518, 210)]); arrow([(360, 264), (518, 264)])
    box(520, 312, 400, 'Not indexed', ['Removed: the numbered steps carry the flow.'], 'data', h=60, dash=True)
    arrow([(360, 318 + 10), (518, 318 + 10)])
    box(1040, 134, 300, 'Search', ['Chunks, and filters from the tags.'], 'method', h=70)
    arrow([(920, 170), (1038, 170)])
    box(1040, 262, 300, 'Reading plan', ['Follows the links.'], 'method', h=60)
    box(1040, 352, 300, 'Up-front block', ['Sent with every question.'], 'method', h=60)
    box(1040, 442, 300, 'Review only', ['Never embedded.'], 'data', h=60, dash=True)
    # metadata arrows: tags, links, up_front, the review fields
    arrow([(360, 404), (940, 404), (940, 190), (1038, 190)], 'filters', 650, 400, '#1f5fae')
    arrow([(360, 432), (980, 432), (980, 292), (1038, 292)], 'links', 650, 428, '#1f5fae')
    arrow([(360, 460), (1020, 460), (1020, 382), (1038, 382)], 'marked misconceptions', 650, 456, '#1f5fae')
    arrow([(360, 488), (1038, 488)], 'audit fields', 650, 484, '#888888', dash=True)
    finish(out_path('file-as-model-sees.svg'))


# ------------------------------------------------------------------ 4. source to reviewed file
def source_to_reviewed():
    W, H = 1800, 520
    start(W, H)
    head(W, 'From source to reviewed file',
         'Each fact gets one home file. Other files link to it and hold no copy.',
         [('Source or evidence', 'data'), ('Work step', 'method'), ('Knowledge files', 'prod'), ('Check', 'shared')])
    box(30, 110, 270, "Books, spreadsheets, diagrams", ["The author's own material."], 'data', h=90)
    box(30, 230, 270, 'Documentation', ['Manuals, white papers, expert answers.'], 'data', h=90)
    box(30, 350, 270, 'Environment', ['Screenshots, API, GUI, lab tests.'], 'data', h=90)
    box(340, 350, 230, 'evidence/ files', ['Screenshots, API output,', 'lab results.'], 'data', h=90)
    arrow([(302, 395), (338, 395)])
    box(620, 130, 290, 'Source note', ['One topic, a few pages.', 'Vendor and measured claims are', 'tagged E1, E2.', 'Lives in project/sources/.'], 'data', h=290)
    arrow([(302, 155), (618, 155)]); arrow([(302, 275), (618, 275)]); arrow([(572, 395), (596, 395), (596, 360), (618, 360)])
    box(960, 200, 240, 'Digest', ['Each fact gets one', 'home file.'], 'method', h=150)
    arrow([(912, 275), (958, 275)])
    box(1250, 140, 230, 'Home file', ['The fact. source.path names', 'the note.'], 'prod', h=100)
    box(1250, 290, 230, 'Other files', ['A link to the home,', 'no copy.'], 'prod', h=100)
    arrow([(1202, 250), (1226, 250), (1226, 190), (1248, 190)]); arrow([(1202, 300), (1226, 300), (1226, 340), (1248, 340)])
    box(1530, 200, 240, 'Check', ['Lint, retrieval check,', 'author review.'], 'shared', h=150)
    arrow([(1482, 190), (1506, 190), (1506, 250), (1528, 250)]); arrow([(1482, 340), (1506, 340), (1506, 300), (1528, 300)])
    finish(out_path('source-to-reviewed.svg'))


# ------------------------------------------------------------------ 5. Agent E2 in PCM
def agent_e2_in_pcm():
    W, H = 1640, 540
    start(W, H)
    head(W, 'Agent E2 in PCM',
         'Two repositories, two processes. PCM calls Agent E2 over HTTP; Agent E2 calls no PCM code, database or endpoint.',
         [('PCM', 'data'), ('Agent and harness', 'method'), ('Knowledge', 'prod'), ('Model', 'guest')])
    frame(30, 100, 480, 390, 'PCM', 'Separate repository and process')
    box(46, 150, 448, 'Screens and the Agent E2 panel', [], 'data', h=60)
    box(46, 236, 448, 'Data', ['VCF Operations, synthetic ACME.'], 'data', h=70)
    box(46, 332, 448, 'Identity, roles, conversation and topics', ['The caller keeps the conversation.'], 'data', h=80)
    frame(760, 100, 480, 390, 'Agent E2', 'This repository')
    box(776, 150, 448, 'harness/answer_service.py', ['POST /v1/answer, /v1/suggest, /v1/topic', 'GET /v1/health'], 'method', h=80, mono=True)
    box(776, 270, 448, 'Agent and harness', ['Case, reading plan, tools, verifier.'], 'method', h=70)
    box(776, 390, 448, 'knowledge/', ['Read by the agent through the harness.'], 'prod', h=70, mono=True)
    arrow([(1000, 232), (1000, 268)]); arrow([(1000, 342), (1000, 388)])
    box(1380, 270, 230, 'Model server', ['Local GPU. Lab: gateway.'], 'guest', h=70)
    arrow([(1226, 305), (1378, 305)], 'OpenAI-compatible API', 1302, 296)
    for n, s in enumerate(['question, facts (screen and', 'KPI series), role, history,', 'topic_choice']):
        t(635, 160 + n * 14, s, 10.5, 'normal', '#1f5fae', 'middle')
    arrow([(512, 205), (758, 205)], color='#1f5fae')
    for n, s in enumerate(['lead, answer, files read,', 'computed, topic, shape,', 'knowledge commit']):
        t(635, 262 + n * 14, s, 10.5, 'normal', '#2e7d32', 'middle')
    arrow([(758, 250), (512, 250)], color='#2e7d32')
    finish(out_path('agent-e2-in-pcm.svg'))


# ------------------------------------------------------------------ 6. repository groups
def repository_groups():
    W, H = 1500, 780
    start(W, H)
    head(W, 'Repository: product, proof and project',
         'One repository, three groups. Only the product is deployed to the site.',
         [('Knowledge', 'prod'), ('Agent and harness', 'method'), ('Model', 'guest'), ('Check or proof', 'shared'), ('Other', 'data')])
    frame(30, 100, 960, 560, 'Product', 'Deployed to the site')
    box(60, 160, 270, 'knowledge/', ['Codified expertise.', 'The only indexed folder.'], 'prod', h=90, mono=True)
    box(420, 160, 270, 'harness/', ['Retrieval, tools,', 'verifier, rules.'], 'method', h=90, mono=True)
    box(240, 400, 310, 'Agent', ["The expert's procedure as code:", 'case, reading plan, checks.'], 'method', h=90)
    box(700, 400, 260, 'Open-weight model', ['On a local GPU.'], 'guest', h=90)
    arrow([(418, 205), (332, 205)], 'retrieves', 375, 196)
    arrow([(290, 398), (290, 252)], 'plans from the map of', 290, 330)
    arrow([(500, 398), (500, 252)], 'runs the tools of', 500, 330)
    arrow([(552, 445), (698, 445)], 'calls to read and write', 625, 436)
    frame(1030, 100, 440, 190, 'Proof', 'Not deployed')
    box(1050, 160, 400, 'benchmark/', ['Questions, models, runner, results.'], 'shared', h=90, mono=True)
    frame(1030, 320, 440, 340, 'Project', 'Not deployed')
    box(1050, 370, 400, 'project/tools/', ['rules_check.py,', 'rules_check_values.yaml.'], 'shared', h=100, mono=True)
    box(1050, 520, 400, 'project/', ['Plan, decisions, author questions,', 'reviews.'], 'data', h=100, mono=True)
    arrow([(1050, 200), (692, 200)], 'runs questions through', 870, 190)
    arrow([(1250, 368), (1250, 252)], 'checks', 1280, 310)
    arrow([(1050, 420), (1010, 420), (1010, 128), (195, 128), (195, 158)], 'checks', 600, 122)
    box(240, 700, 310, 'PCM', ['Separate repository.'], 'data', h=60)
    arrow([(395, 698), (395, 492)], 'HTTP: answer_service.py', 520, 600)
    finish(out_path('repository-groups.svg'))


# ------------------------------------------------------------------ 7. benchmark folders (benchmark/README.md)
def benchmark_folders():
    W, H = 1100, 890
    start(W, H)
    head(W, 'benchmark/: questions, runner, models, results',
         'Each folder and its role in the proof.',
         [('Benchmark code', 'method'), ('Question, result or proof', 'shared'), ('Document for people', 'data')])
    frame(20, 100, 1060, 780, 'Proof, not deployed', 'Only the product is deployed to the site.')
    box(50, 400, 200, 'benchmark/', ['The proof of Agent E2.'], 'white', mono=True)
    kids = [  # (x, y, w, title, lines, kind, mono)
        (330, 110, 380, 'questions/', ['L<level>-<nnn>-<slug>.md: one question', 'per file, one flat folder.'], 'shared', True),
        (330, 190, 380, 'questions/<id>/', ["The question's attachments: screenshots,", 'logs, diagrams (only when it has any).'], 'shared', True),
        (330, 270, 380, 'runner/', ['Benchmark runner: run_executor.py,', 'round_executor.py, round_sample_check.py,',
                                    'bad_answer_guard.py, round_alive_check.py,', 'run_folders_backup.py, inference_providers.py,',
                                    'round_resume.py, round_summary.py,', 'score_report.py, adaptive_concurrency.py,',
                                    'runner_config.yaml'], 'method', True),
        (330, 425, 380, 'models.md', ['Candidate models and the frontier reference.'], 'data', True),
        (330, 505, 380, 'RUN.md', ['How to run a round: prompt, approvals,', 'time, cost.'], 'data', True),
        (330, 585, 380, 'live-test.md', ['The system on an offline model:', 'plan and pass criteria.'], 'data', True),
        (330, 665, 380, '_templates/question.md', ['Template for a new question.'], 'data', True),
        (330, 730, 380, 'results/README.md', ['One analysis of all runs of a round,', 'written when the last run finishes.'], 'shared', True),
    ]
    for x, y, w, title, lines, kind, mono in kids:
        _, _, _, h = box(x, y, w, title, lines, kind, mono=mono)
        arrow([(250, 435), (x - 2, y + h // 2)])
    box(760, 730, 300, 'results/<date>-<model>/', ['Per run: answers.csv, report.md,', 'config.json (traces.jsonl not in git)'], 'shared', mono=True)
    arrow([(710, 763), (758, 763)])
    finish(out_path('benchmark-folders.svg'))


# ------------------------------------------------------------------ 8. six stages of the agent (harness/AGENT.md)
def agent_six_stages():
    W, H = 1000, 880
    start(W, H)
    head(W, 'Agent E2: one question through six stages',
         'Code decides the route. The model reads in stages 1 and 5 and may run once more in stage 6.',
         [('Agent code', 'method'), ('Model call', 'guest'), ('Input or output', 'data')])
    box(260, 100, 460, 'Question and images', ['Input: the question text and its screenshots.'], 'data', h=52)
    box(260, 190, 460, '1 Understand', ['Model (1 call): reads the question into a', 'fixed schema. The agent resolves names.'], 'guest', h=70)
    box(260, 290, 460, '2 Plan', ['Agent: builds the reading set from the', "knowledge base's map. No model call."], 'method', h=70)
    box(260, 390, 460, '3 Compute', ['Agent: catalog, calculator, flow executor,', 'planning calculator on the case.'], 'method', h=70)
    box(260, 490, 460, '4 Ask?', ['Agent rule: does a missing fact', 'change the answer?'], 'method', h=70)
    box(740, 475, 240, 'One clarifying round', ['A missing fact changes', 'the answer. One round,', 'then back to stage 1.'], 'method', h=86)
    box(260, 590, 460, '5 Answer', ['Model (1 call, n with consensus): reads', 'and writes the draft answer.'], 'guest', h=70)
    box(260, 690, 460, '6 Check', ['Agent: verifier, consensus, coverage.', 'A gap follow-up or repair may call the model.'], 'method', h=70)
    box(260, 790, 460, 'Answer with citations', ['Computed facts and citations to the files.'], 'data', h=52)
    arrow([(490, 152), (490, 188)])
    arrow([(490, 260), (490, 288)])
    arrow([(490, 360), (490, 388)])
    arrow([(490, 460), (490, 488)])
    arrow([(720, 525), (738, 525)])
    arrow([(860, 475), (860, 225), (722, 225)])
    arrow([(490, 560), (490, 588)], 'no', 506, 578)
    arrow([(490, 660), (490, 688)])
    arrow([(490, 760), (490, 788)])
    arrow([(260, 725), (200, 725), (200, 325), (258, 325)], 'gap: a named metric not read', 118, 520)
    finish(out_path('agent-six-stages.svg'))


if __name__ == '__main__':
    for fn in (knowledge_workflow, knowledge_paths, file_as_model_sees, source_to_reviewed, agent_e2_in_pcm, repository_groups,
               benchmark_folders, agent_six_stages):
        fn()
