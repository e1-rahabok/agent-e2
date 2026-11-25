"""Draw images/knowledge-structure.svg: what the knowledge is (KNOWLEDGE-ENGINEERING.md, section 2).

Hand-laid SVG for human readers, in the style of product_diagram.py. The file counts are typed in below:
update them when `python3 project/tools/knowledge_stats.py` and the folder counts move. A colour is added only with an entry
in the colour key: a colour with no entry reads as random.
Run from the repository root:
    python3 project/tools/knowledge_diagram.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from diagram_kit import out, C, t, box, band, arrow, begin, finish  # noqa: E402

W, H = 1800, 1572
begin(W, H)
t(24, 34, 'Agent E2 knowledge structure', 20, 'bold', '#111')
t(24, 54, 'Knowledge of private cloud operations management with VMware Cloud Foundation: 288 files, about 327K tokens. '
          'Bands: method and product, layers, slices of one fact, anatomy of a file, paths to the model.', 12.5, 'normal', '#444')

# colour key: one meaning per colour, in every band
lx = 1130
for label, kind in (('Method (SP5 Framework)', 'method'), ('Product (VMware, hardware)', 'prod'), ('Guest OS', 'guest'), ('Applies to all', 'data')):
    fill, stroke, ink = C[kind]
    out.append(f'<rect x="{lx}" y="22" width="14" height="14" rx="3" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>')
    t(lx + 20, 34, label, 11.5, 'normal', '#333')
    lx += 20 + len(label) * 6.3 + 22

# ------------------------------------------------------------------ 1. method and product
y1 = 70
B1 = 384
band(y1, B1, 1, 'Method | Product',
     'Method explains how private cloud is managed. Product is the knowledge of the IT products involved. Each has supporting files, drawn with a dashed outline.')
by = y1 + 68
BH = 304
# Method
box(30, by, 540, 'Method: IT Operations Framework', [], 'method', h=BH)
t(40, by + 38, 'The SP5 Framework: how private cloud is managed, with VCF terms and examples.', 11.5, 'normal', '#0d2a4d')
t(40, by + 53, 'knowledge/sp5-framework/   57 files', 11.5, 'bold', '#0d2a4d', mono=True)
subs = [('concepts/  14', 'the framework across pillars: health check,', 'SLAs, class of service, modelling'),
        ('observability/  13', 'how to read telemetry: input types, interval,', 'units, Triple See Method'),
        ('outputs/  13', 'how insight reaches people: alerts,', 'dashboards, reports, NOC screen'),
        ('capacity/  12', 'supply, demand, overcommit, forecasting,', 'planning, sizing, reclamation'),
        ('performance/  5', 'KPI design, KPI vs SLA, noisy neighbour', '')]
for n, (a_, b_, c_) in enumerate(subs):
    yy = by + 66 + n * 38
    out.append(f'<rect x="42" y="{yy}" width="516" height="34" rx="4" fill="#ffffff" stroke="#1f5fae" stroke-width="1"/>')
    t(50, yy + 14, a_, 11.5, 'bold', '#0d2a4d', mono=True)
    t(190, yy + 14, b_, 11, 'normal', '#0d2a4d')
    if c_:
        t(190, yy + 28, c_, 11, 'normal', '#0d2a4d')
yy = by + 66 + 5 * 38
out.append(f'<rect x="42" y="{yy}" width="516" height="34" rx="4" fill="#f5f8fd" stroke="#1f5fae" stroke-width="1" stroke-dasharray="5 3"/>')
t(50, yy + 14, 'glossary.md  1', 11.5, 'bold', '#0d2a4d', mono=True)
t(190, yy + 14, 'supporting file: one English word per concept, other names', 11, 'normal', '#0d2a4d')
t(190, yy + 28, 'users say, confusable pairs such as Usage vs Utilization', 11, 'normal', '#0d2a4d')
# Product
box(590, by, 1180, 'Product: IT products', [], 'prod', h=BH)
t(600, by + 38, 'VMware Cloud Foundation, Windows and Linux. Hardware appears as the physical layer under ESXi.', 11.5, 'normal', '#173a16')
out.append(f'<rect x="602" y="{by + 50}" width="1156" height="124" rx="4" fill="#ffffff" stroke="#2e7d32" stroke-width="1"/>')
t(612, by + 68, 'vsphere/   204 files', 12, 'bold', '#173a16', mono=True)
vs = [('architecture/  7', 'what every metric depends on:', 'provider/consumer, overhead'),
      ('technology/  150', 'raw metrics by technology:', 'cpu gpu memory storage network'),
      ('object-types/  39', 'content by object type:', 'vm, esxi, cluster ...'),
      ('tools/  8', 'how tools show counters:', 'esxtop, vSphere Client')]
for n, (a_, b_, c_) in enumerate(vs):
    xx = 612 + n * 287
    out.append(f'<rect x="{xx}" y="{by + 78}" width="276" height="86" rx="4" fill="#e6f4e4" stroke="#2e7d32" stroke-width="1"/>')
    t(xx + 6, by + 96, a_, 11, 'bold', '#173a16', mono=True)
    t(xx + 6, by + 113, b_, 10.5, 'normal', '#173a16')
    t(xx + 6, by + 127, c_, 10.5, 'normal', '#173a16')
out.append(f'<rect x="602" y="{by + 184}" width="571" height="68" rx="4" fill="#ffffff" stroke="#2e7d32" stroke-width="1"/>')
t(612, by + 202, 'vcf-operations/   10 files', 12, 'bold', '#173a16', mono=True)
t(612, by + 219, 'The product VCF Operations: its role, alert definitions,', 10.5, 'normal', '#173a16')
t(612, by + 233, 'report suite, dashboards and features as built.', 10.5, 'normal', '#173a16')
out.append(f'<rect x="1187" y="{by + 184}" width="571" height="68" rx="4" fill="#fdebd3" stroke="#c25e00" stroke-width="1.4"/>')
t(1197, by + 202, 'guest-os/   16 files', 12, 'bold', '#4a2400', mono=True)
t(1197, by + 219, 'Windows and Linux above the VM: a separate layer, not VMware', 10.5, 'normal', '#4a2400')
t(1197, by + 233, 'products. cpu, memory, storage, system.', 10.5, 'normal', '#4a2400')
out.append(f'<rect x="602" y="{by + 262}" width="1156" height="34" rx="4" fill="#f6fbf5" stroke="#2e7d32" stroke-width="1" stroke-dasharray="5 3"/>')
t(612, by + 276, 'catalog/   9 YAML files', 11.5, 'bold', '#173a16', mono=True)
t(790, by + 276, 'supporting files: exact values loaded into SQLite and looked up by key: vCenter counters, esxtop fields,', 11, 'normal', '#173a16')
t(790, by + 290, 'thresholds, object model, user terms.', 11, 'normal', '#173a16')

# ------------------------------------------------------------------ 2. layers
y2 = y1 + B1 + 15
band(y2, 225, 2, 'Layers of the product',
     'Tag: layer. A VM is a virtual motherboard and the Guest OS above it is a separate layer, so the layer that produces a metric decides its home.')
ly = y2 + 68
layers = [
    ('guest', 'guest-os', 'Windows or Linux inside the VM', 'Not a Broadcom product, not part of the VM.', 'Folder: knowledge/guest-os/'),
    ('prod', 'virtual-motherboard', 'The VM as the hypervisor presents it', 'Example: vCPU Ready, the consumer view.', 'Folder: technology/*/metrics/virtual-motherboard/'),
    ('prod', 'hypervisor', 'ESXi: kernel worlds, schedulers, overhead', 'The provider view of the same resource.', 'Folder: vsphere/architecture/ and metrics/host/'),
    ('prod', 'physical', 'Cores, memory, NICs, disks', 'The hardware under the hypervisor.', 'Tag only: no folder of its own.'),
]
for n, (k, a, b, c, d) in enumerate(layers):
    xx = 30 + n * 435
    fill, stroke, ink = C[k]
    out.append(f'<rect x="{xx}" y="{ly}" width="420" height="104" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>')
    t(xx + 10, ly + 20, a, 13, 'bold', ink, mono=True)
    t(xx + 10, ly + 38, b, 11.5, 'bold', ink)
    t(xx + 10, ly + 58, c, 11, 'normal', ink)
    t(xx + 10, ly + 72, d, 11, 'normal', ink)
    if n < 3:
        arrow([(xx + 422, ly + 52), (xx + 433, ly + 52)])
t(30, ly + 124, 'Vantage points: a consumer VM is seen from the virtual motherboard, and the provider ESXi from the hypervisor. '
                'The same word can mean different things in two layers.', 11.5, 'normal', '#333')
t(30, ly + 142, 'Example: reading ESXi CPU Ready as the host waiting for CPU is wrong, because Ready is a consumer metric. '
                'The layer tag keeps the two apart in search.', 11.5, 'normal', '#333')

# ------------------------------------------------------------------ 3. slices
y3 = y2 + 225 + 15
band(y3, 312, 3, 'Slices of one fact',
     'The folder tree holds one slice. Tags and links hold the others. Retrieval filters on any tag, and the model follows any link.')
sy = y3 + 68
box(560, sy, 680, 'VM CPU Ready', [
    'knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/ready.md',
    'One metric, one object type, one file. Kind: metric-meaning. Class: contention.'], 'prod', h=64, mono=True)
slices = [
    ('Technology', 'Folder and tag', 'cpu', 'Read contention first,', 'then consumption. Folder: vsphere/technology/cpu/'),
    ('Object', 'Tag and link', 'VirtualMachine', 'Listed in vm-health-check, part of the', 'VM Performance KPI (vm-performance).'),
    ('Pillar', 'Tag and link', 'performance', 'Used by performance-kpi-design and by', 'the cluster KPI in the SP5 Framework.'),
]
for n, (a, b, c, d, e) in enumerate(slices):
    xx = 30 + n * 590
    kind = 'method' if a == 'Pillar' else 'prod'  # the pillars belong to the SP5 Framework
    ink = C[kind][2]
    box(xx, sy + 100, 560, f'{a}   ({b})', [], kind, h=100)
    t(xx + 10, sy + 142, c, 13, 'bold', ink, mono=True)
    t(xx + 10, sy + 162, d, 11.5, 'normal', ink)
    t(xx + 10, sy + 177, e, 11.5, 'normal', ink)
    arrow([(900 if n == 1 else (660 if n == 0 else 1140), sy + 64), (xx + 280, sy + 99)])
t(30, sy + 232, 'Tags: scope, technology, pillar, product, object, layer, instance, metric_class. '
                'Links: internal_derive, same_name, same_meaning, related. Together they list which files are read together.', 11.5, 'normal', '#333')

# ------------------------------------------------------------------ 4. file anatomy
y4 = y3 + 312 + 15
band(y4, 340, 4, 'Anatomy of a file',
     'One fact per bullet, so a mistake sits on one line. Templates fix the section names, so one question finds the same section in every file.')
ay = y4 + 68
# kinds
box(30, ay, 430, 'Seven kinds of file (retriever_guide)', [], 'data', h=256)
kinds = [('metric-meaning', '107', 'What does this number mean on this object?'),
         ('how-it-works', '129', 'How does it work? Why does the metric behave so?'),
         ('what-to-set', '29', 'What to configure, which alerts, and why.'),
         ('troubleshooting', '12', 'It is slow or down. Why? Order of checks.'),
         ('decision-tree', '7', 'Can it, should it, how much?'),
         ('health-check', '3', 'Is it healthy? What to check, in what order.'),
         ('term-meaning', '1', 'The glossary.')]
for n, (a, c, d) in enumerate(kinds):
    yy = ay + 34 + n * 29
    t(40, yy + 12, a, 11.5, 'bold', '#222', mono=True)
    t(190, yy + 12, c, 11.5, 'bold', '#222', 'end')
    t(200, yy + 12, d, 10.5, 'normal', '#222')
t(40, ay + 246, 'The harness reads the kind from the metadata.', 11, 'bold', '#222')
# anatomy
box(490, ay, 400, 'Inside a file', [], 'data', h=256)
parts = [('# Title', 'A name a question uses.'),
         ('## Sections', 'Meaning, Formula, Includes / excludes, Reason.'),
         ('## Misconceptions', 'A wrong reading in the user\'s words, and its fix.'),
         ('Mermaid chart', 'Master of a flow; steps follow it.'),
         ('## Metadata (yaml)', 'Last. Tags, links, provenance.')]
for n, (a, d) in enumerate(parts):
    yy = ay + 40 + n * 36
    out.append(f'<rect x="500" y="{yy - 4}" width="380" height="32" rx="4" fill="#ffffff" stroke="#666666" stroke-width="1"/>')
    t(508, yy + 11, a, 11.5, 'bold', '#222', mono=True)
    t(508, yy + 24, d, 10.5, 'normal', '#222')
t(500, ay + 244, 'A ## section is the unit of retrieval.', 11, 'bold', '#222')
# metadata
box(920, ay, 850, 'Metadata block', [], 'data', h=256)
groups = [('Search tags', ['scope  technology  pillar  product', 'object  layer  instance  metric_class'], 'Tags filter retrieval.'),
          ('Links', ['internal_derive  same_name', 'same_meaning  related'], 'Links choose what is read together.'),
          ('Provenance', ['source.document  source.path  status', 'corrections  review_notes'], 'Vendor version, draft or reviewed, what to check.'),
          ('Delivery', ['up_front  images'], 'The marked misconception goes with every question.')]
for n, (a, ls, d) in enumerate(groups):
    xx = 932 + (n % 2) * 420
    yy = ay + 38 + (n // 2) * 108
    out.append(f'<rect x="{xx}" y="{yy}" width="404" height="96" rx="4" fill="#ffffff" stroke="#666666" stroke-width="1"/>')
    t(xx + 10, yy + 18, a, 12.5, 'bold', '#222')
    for m, l in enumerate(ls):
        t(xx + 10, yy + 38 + m * 15, l, 11, 'normal', '#222', mono=True)
    t(xx + 10, yy + 82, d, 11, 'normal', '#222')

# ------------------------------------------------------------------ 5. five paths
y5 = y4 + 340 + 15
band(y5, 150, 5, 'Paths to the model',
     'Five ways knowledge reaches the model: retrieved, looked up, given up front, run as code, set as agent instructions. Each fact has one home.')
py = y5 + 68
paths = [('Retrieved', 'Mechanisms, metrics, flows', 'knowledge/**/*.md'),
         ('Looked up exactly', 'Units, rollups, thresholds', 'knowledge/catalog/*.yaml'),
         ('Given up front', 'Widest misconceptions, pairs', 'up_front lines + glossary'),
         ('Executed as code', 'Arithmetic, answer checks', 'harness/*.py'),
         ('Agent instructions', 'Conduct for every answer', 'answer_modes.py, expert_agent.py')]
for n, (a, b, c) in enumerate(paths):
    xx = 30 + n * 350
    box(xx, py, 335, f'{n + 1}  {a}', [b, c], 'data', h=64)
    if n < 4:
        pass

here = os.path.dirname(os.path.abspath(__file__))
finish(os.path.join(os.path.dirname(os.path.dirname(here)), 'images', 'knowledge-structure.svg'))
