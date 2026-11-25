"""Draw images/knowledge-structure.svg: what the knowledge is (KNOWLEDGE-ENGINEERING.md, section 2).

Hand-laid SVG for human readers, in the style of product_diagram.py. The file counts are typed in below:
update them when `python3 project/tools/knowledge_stats.py` and the folder counts move.
Run from the repository root:
    python3 project/tools/knowledge_diagram.py
"""
import os
from xml.sax.saxutils import escape

W, H = 1800, 1532
LH = 15
out = []

C = {
    'method': ('#e4edfa', '#1f5fae', '#0d2a4d'),
    'prod': ('#e6f4e4', '#2e7d32', '#173a16'),
    'guest': ('#fdebd3', '#c25e00', '#4a2400'),
    'shared': ('#efe9f8', '#5e35b1', '#2a1650'),
    'data': ('#f2f2f2', '#666666', '#222222'),
    'white': ('#ffffff', '#888888', '#333333'),
}


def t(x, y, s, size=12, weight='normal', fill='#222', anchor='start', mono=False):
    f = ' font-family="ui-monospace,Menlo,Consolas,monospace"' if mono else ''
    out.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
               f'text-anchor="{anchor}"{f}>{escape(s)}</text>')


def box(x, y, w, title, lines, kind, h=None, dash=False, mono=False):
    fill, stroke, ink = C[kind]
    h = h or (28 + LH * len(lines) + 8)
    d = ' stroke-dasharray="6 4"' if dash else ''
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.4"{d}/>')
    t(x + 10, y + 19, title, 13, 'bold', ink, mono=mono)
    for n, ln in enumerate(lines):
        t(x + 10, y + 38 + n * LH, ln, 11.5, 'normal', ink)
    return (x, y, w, h)


def band(y, h, num, label, sub):
    out.append(f'<rect x="10" y="{y}" width="{W - 20}" height="{h}" rx="10" fill="#fafafa" stroke="#c9c9c9"/>')
    out.append(f'<circle cx="38" cy="{y + 28}" r="14" fill="#333"/>')
    t(38, y + 33, str(num), 14, 'bold', '#fff', 'middle')
    t(62, y + 33, label, 16, 'bold', '#222')
    t(62, y + 52, sub, 12, 'normal', '#555')


def arrow(pts, label=None, lx=None, ly=None, color='#555555', dash=False):
    d = 'M ' + ' L '.join(f'{x} {y}' for x, y in pts)
    ds = ' stroke-dasharray="5 4"' if dash else ''
    out.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.5"{ds} marker-end="url(#ah)"/>')
    if label:
        wpx = len(label) * 6.1 + 8
        out.append(f'<rect x="{lx - wpx / 2:.0f}" y="{ly - 11}" width="{wpx:.0f}" height="15" fill="#fafafa"/>')
        t(lx, ly, label, 10.5, 'normal', color, 'middle')


out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif">')
out.append('<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
           'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#555555"/></marker></defs>')
out.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
t(24, 34, 'Agent E2, Knowledge: what "Private Cloud Operations Management with VMware Cloud Foundation" knowledge is made of', 20, 'bold', '#111')
t(24, 54, '288 files, about 327K tokens. Two bodies of knowledge, one layered product, three ways to find a fact, '
          'one anatomy for every file. Read top to bottom.', 12.5, 'normal', '#444')

# ------------------------------------------------------------------ 1. two bodies
y1 = 70
band(y1, 345, 1, 'Two bodies of knowledge, in every answer',
     'The method says how to operate VCF. The product says what VCF is and does. Shared vocabulary and exact values serve both.')
by = y1 + 68
# Method
box(30, by, 520, 'Method: the SP5 Framework', [], 'method', h=262)
t(40, by + 38, 'How to operate VCF, in VCF terms and examples.', 11.5, 'normal', '#0d2a4d')
t(40, by + 53, 'knowledge/sp5-framework/   57 files', 11.5, 'bold', '#0d2a4d', mono=True)
subs = [('concepts/  14', 'the framework across pillars: health check,', 'SLAs, class of service, modelling'),
        ('observability/  13', 'how to read telemetry: input types, interval,', 'units, Triple See Method'),
        ('outputs/  13', 'how insight reaches people: alerts,', 'dashboards, reports, NOC screen'),
        ('capacity/  12', 'supply, demand, overcommit, forecasting,', 'planning, sizing, reclamation'),
        ('performance/  5', 'KPI design, KPI vs SLA, noisy neighbour', '')]
for n, (a, b, c) in enumerate(subs):
    yy = by + 66 + n * 38
    out.append(f'<rect x="42" y="{yy}" width="496" height="34" rx="4" fill="#ffffff" stroke="#1f5fae" stroke-width="1"/>')
    t(50, yy + 14, a, 11.5, 'bold', '#0d2a4d', mono=True)
    t(190, yy + 14, b, 11, 'normal', '#0d2a4d')
    if c:
        t(190, yy + 28, c, 11, 'normal', '#0d2a4d')
# Product
box(580, by, 760, 'Product: VCF 9.x', [], 'prod', h=262)
t(590, by + 38, 'What each component is and does, down to the counter.', 11.5, 'normal', '#173a16')
# vsphere
out.append(f'<rect x="592" y="{by + 50}" width="736" height="124" rx="4" fill="#ffffff" stroke="#2e7d32" stroke-width="1"/>')
t(602, by + 68, 'vsphere/   204 files', 12, 'bold', '#173a16', mono=True)
vs = [('architecture/  7', 'what every metric depends on:', 'provider/consumer, overhead'),
      ('technology/  150', 'raw metrics by technology:', 'cpu gpu memory storage net'),
      ('object-types/  39', 'content by object type:', 'vm, esxi, cluster ...'),
      ('tools/  8', 'how tools show counters:', 'esxtop, vSphere Client')]
for n, (a, b, c) in enumerate(vs):
    xx = 602 + n * 181
    out.append(f'<rect x="{xx}" y="{by + 78}" width="172" height="86" rx="4" fill="#e6f4e4" stroke="#2e7d32" stroke-width="1"/>')
    t(xx + 6, by + 96, a, 11, 'bold', '#173a16', mono=True)
    t(xx + 6, by + 113, b, 10.5, 'normal', '#173a16')
    t(xx + 6, by + 127, c, 10.5, 'normal', '#173a16')
# vcf-operations
out.append(f'<rect x="592" y="{by + 184}" width="360" height="68" rx="4" fill="#ffffff" stroke="#2e7d32" stroke-width="1"/>')
t(602, by + 202, 'vcf-operations/   10 files', 12, 'bold', '#173a16', mono=True)
t(602, by + 219, 'The product VCF Operations: its role, alert definitions,', 10.5, 'normal', '#173a16')
t(602, by + 233, 'report suite, dashboards and features as built.', 10.5, 'normal', '#173a16')
# guest-os
out.append(f'<rect x="968" y="{by + 184}" width="360" height="68" rx="4" fill="#fdebd3" stroke="#c25e00" stroke-width="1.4"/>')
t(978, by + 202, 'guest-os/   16 files', 12, 'bold', '#4a2400', mono=True)
t(978, by + 219, 'Windows and Linux: a separate layer, not Broadcom', 10.5, 'normal', '#4a2400')
t(978, by + 233, 'products, not part of the VM. cpu, memory, storage, system.', 10.5, 'normal', '#4a2400')
# shared
box(1370, by, 400, 'Shared by both', [], 'shared', h=262)
out.append(f'<rect x="1382" y="{by + 36}" width="376" height="100" rx="4" fill="#ffffff" stroke="#5e35b1" stroke-width="1"/>')
t(1392, by + 54, 'glossary.md   1 file', 12, 'bold', '#2a1650', mono=True)
t(1392, by + 72, 'The agent\'s vocabulary: one English word per', 11, 'normal', '#2a1650')
t(1392, by + 86, 'concept, other names users say, confusable', 11, 'normal', '#2a1650')
t(1392, by + 100, 'pairs (Usage vs Utilization, KPI vs SLA).', 11, 'normal', '#2a1650')
t(1392, by + 122, 'Wrong words produce wrong reasoning.', 11, 'bold', '#2a1650')
out.append(f'<rect x="1382" y="{by + 146}" width="376" height="104" rx="4" fill="#ffffff" stroke="#5e35b1" stroke-width="1"/>')
t(1392, by + 164, 'catalog/   9 YAML files', 12, 'bold', '#2a1650', mono=True)
t(1392, by + 182, 'Exact values, loaded into SQLite, not chunked:', 11, 'normal', '#2a1650')
t(1392, by + 196, 'vCenter counters, esxtop fields, thresholds,', 11, 'normal', '#2a1650')
t(1392, by + 210, 'object model, user terms.', 11, 'normal', '#2a1650')
t(1392, by + 232, 'A number must not depend on retrieval luck.', 11, 'bold', '#2a1650')

# ------------------------------------------------------------------ 2. layers
y2 = y1 + 345 + 15
band(y2, 225, 2, 'The product is a stack: a metric lives in the layer that produces it',
     'Not in the object that stores it. A VM is a virtual motherboard; the Guest OS above it is a separate layer. Tag: layer.')
ly = y2 + 68
layers = [
    ('guest', 'guest-os', 'Windows or Linux inside the VM', 'Not a Broadcom product, not part of the VM.', 'Folder: knowledge/guest-os/'),
    ('prod', 'virtual-motherboard', 'The VM as the hypervisor presents it', 'Example: vCPU Ready, the consumer view.', 'Folder: technology/*/metrics/virtual-motherboard/'),
    ('prod', 'hypervisor', 'ESXi: kernel worlds, schedulers, overhead', 'The provider view of the same resource.', 'Folder: vsphere/architecture/ and metrics/host/'),
    ('data', 'physical', 'Cores, memory, NICs, disks', 'The hardware under the hypervisor.', 'Tag only: no folder of its own.'),
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
t(30, ly + 124, 'Consumer and provider show up as two vantage points on one resource: a consumer VM seen from the virtual motherboard, '
                'the provider ESXi seen from the hypervisor. Same word, different layer, different meaning.', 11.5, 'normal', '#333')
t(30, ly + 142, 'Why it matters: "ESXi CPU Ready is high, so the host waits for CPU" is a wrong reading, because Ready is a consumer metric. '
                'The layer tag keeps the two apart in search.', 11.5, 'normal', '#333')

# ------------------------------------------------------------------ 3. slices
y3 = y2 + 225 + 15
band(y3, 312, 3, 'One fact, three ways to find it',
     'The folder tree holds one slice. Tags and links hold the others. Retrieval filters on any tag; the model follows any link.')
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
    box(xx, sy + 100, 560, f'{a}   ({b})', [], 'data', h=100)
    t(xx + 10, sy + 142, c, 13, 'bold', '#222', mono=True)
    t(xx + 10, sy + 162, d, 11.5, 'normal', '#222')
    t(xx + 10, sy + 177, e, 11.5, 'normal', '#222')
    arrow([(900 if n == 1 else (660 if n == 0 else 1140), sy + 64), (xx + 280, sy + 99)])
t(30, sy + 232, 'Tags: scope, technology, pillar, product, object, layer, instance, metric_class. '
                'Links: internal_derive, same_name, same_meaning, related. Together they are the expert\'s map of what is read together.', 11.5, 'normal', '#333')

# ------------------------------------------------------------------ 4. file anatomy
y4 = y3 + 312 + 15
band(y4, 340, 4, 'One file: the same anatomy for every fact',
     'One fact per bullet, so a mistake stays on one line. Templates keep section names the same, so a question finds the same kind of section everywhere.')
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
    t(190, yy + 12, c, 11.5, 'bold', '#1f5fae', 'end')
    t(200, yy + 12, d, 10.5, 'normal', '#222')
t(40, ay + 246, 'The harness reads the kind, not the folder.', 11, 'bold', '#222')
# anatomy
box(490, ay, 400, 'Inside a file', [], 'prod', h=256)
parts = [('# Title', 'A name a question uses.'),
         ('## Sections', 'Meaning, Formula, Includes / excludes, Reason.'),
         ('## Misconceptions', 'A wrong reading in the user\'s words, and its fix.'),
         ('Mermaid chart', 'Master of a flow; steps follow it.'),
         ('## Metadata (yaml)', 'Last. Tags, links, provenance.')]
for n, (a, d) in enumerate(parts):
    yy = ay + 40 + n * 36
    out.append(f'<rect x="500" y="{yy - 4}" width="380" height="32" rx="4" fill="#ffffff" stroke="#2e7d32" stroke-width="1"/>')
    t(508, yy + 11, a, 11.5, 'bold', '#173a16', mono=True)
    t(508, yy + 24, d, 10.5, 'normal', '#173a16')
t(500, ay + 244, 'A ## section is the unit of retrieval.', 11, 'bold', '#173a16')
# metadata
box(920, ay, 850, 'What the metadata block holds', [], 'shared', h=256)
groups = [('Find it', ['scope  technology  pillar  product', 'object  layer  instance  metric_class'], 'Tags filter retrieval.'),
          ('Link it', ['internal_derive  same_name', 'same_meaning  related'], 'Links choose what is read together.'),
          ('Trust it', ['source.document  source.path  status', 'corrections  review_notes'], 'Vendor version, draft or reviewed, what to check.'),
          ('Deliver it', ['up_front  images'], 'The marked misconception goes with every question.')]
for n, (a, ls, d) in enumerate(groups):
    xx = 932 + (n % 2) * 420
    yy = ay + 38 + (n // 2) * 108
    out.append(f'<rect x="{xx}" y="{yy}" width="404" height="96" rx="4" fill="#ffffff" stroke="#5e35b1" stroke-width="1"/>')
    t(xx + 10, yy + 18, a, 12.5, 'bold', '#2a1650')
    for m, l in enumerate(ls):
        t(xx + 10, yy + 38 + m * 15, l, 11, 'normal', '#2a1650', mono=True)
    t(xx + 10, yy + 82, d, 11, 'normal', '#2a1650')

# ------------------------------------------------------------------ 5. five paths
y5 = y4 + 340 + 15
band(y5, 150, 5, 'The home of a fact follows its path to the model',
     'Five paths, each for a failure the others cannot prevent. One home per fact; the next diagram, in the next subsection, shows them in detail.')
py = y5 + 68
paths = [('Retrieved', 'Mechanisms, metrics, flows', 'knowledge/**/*.md'),
         ('Looked up exactly', 'Units, rollups, thresholds', 'knowledge/catalog/*.yaml'),
         ('Given up front', 'Widest misconceptions, pairs', 'up_front lines + glossary'),
         ('Executed as code', 'Arithmetic, answer checks', 'harness/*.py'),
         ('Instructed', 'Conduct for every answer', 'answer_modes.py, expert_agent.py')]
for n, (a, b, c) in enumerate(paths):
    xx = 30 + n * 350
    box(xx, py, 335, f'{n + 1}  {a}', [b, c], 'data', h=64)
    if n < 4:
        pass

out.append('</svg>')

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.dirname(here))
path = os.path.join(root, 'images', 'knowledge-structure.svg')
with open(path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(out) + '\n')
print('wrote', path)
