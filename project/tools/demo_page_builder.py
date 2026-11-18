"""Build the page of one demo scenario: project/demo-site/<scenario>/index.html, one self-contained file.

Reads from the scenario folder:
  scenario.yaml   the story, the data tables, the checks an expert answer must pass, and the score of each run;
  turn-1.txt, turn-2.txt   what the user writes;
  results/*.json  Agent E2's answers, written by project/tools/demo_scenario_executor.py.
The answers are shown as Agent E2 wrote them; nothing in them is edited.

Usage: python3 project/tools/demo_page_builder.py project/demo-site/scenario-1-memory-tiering
"""
import html
import json
import os
import re
import sys

import yaml

MARK = {'pass': ('✓', 'pass'), 'partial': ('◐', 'partial'), 'fail': ('✗', 'fail'), 'na': ('–', 'na')}
CSS = """
:root{--bg:#f6f7f9;--panel:#fff;--ink:#16202c;--muted:#5b6776;--line:#d9dee5;--accent:#0b6bcb;--code:#eef1f5;
--g:#d7f0dd;--y:#fbf0c4;--o:#fbd9b5;--r:#f6c6c6;--gi:#1d6b33;--yi:#7a5d00;--oi:#8a4300;--ri:#8f1f1f}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0f141a;--panel:#171e26;--ink:#e6ebf1;--muted:#9aa6b4;
--line:#2a3440;--accent:#5aa9ff;--code:#222b36;--g:#173a22;--y:#3d3412;--o:#43290f;--r:#4a1b1b;--gi:#8fe0a6;--yi:#f1d36b;--oi:#ffb36b;--ri:#ff9b9b}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
main{max-width:1100px;margin:0 auto;padding:24px 16px 64px}h1{font-size:26px;margin:0 0 4px}h2{font-size:19px;margin:36px 0 10px}
h3{font-size:16px;margin:18px 0 8px}.sub{color:var(--muted);margin:0 0 18px}.panel{background:var(--panel);border:1px solid var(--line);
border-radius:10px;padding:14px 16px;margin:10px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px}
table{border-collapse:collapse;width:100%;font-size:14px}th,td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
th{color:var(--muted);font-weight:600}.scroll{overflow-x:auto}code{background:var(--code);padding:1px 4px;border-radius:4px;font-size:13px}
pre{background:var(--code);padding:12px;border-radius:8px;white-space:pre-wrap;font-size:13px;margin:0}
.c-green{background:var(--g);color:var(--gi)}.c-yellow{background:var(--y);color:var(--yi)}.c-orange{background:var(--o);color:var(--oi)}
.c-red{background:var(--r);color:var(--ri)}.c-grey{color:var(--muted)}td.num{font-variant-numeric:tabular-nums;white-space:nowrap}
.pass{color:var(--gi);font-weight:700}.na{color:var(--muted)}.partial{color:var(--yi);font-weight:700}.fail{color:var(--ri);font-weight:700}
.tabs{display:flex;gap:6px;flex-wrap:wrap;margin:8px 0}.tabs button{border:1px solid var(--line);background:var(--panel);color:var(--ink);
border-radius:999px;padding:6px 12px;cursor:pointer;font:inherit;font-size:14px}.tabs button[aria-selected="true"]{border-color:var(--accent);color:var(--accent);font-weight:600}
.answer p{margin:6px 0}.answer ul,.answer ol{margin:6px 0 6px 20px;padding:0}.tag{display:inline-block;font-size:12px;border:1px solid var(--line);
border-radius:999px;padding:1px 8px;color:var(--muted);margin-right:6px}.note{color:var(--muted);font-size:13px}
.timeline li{margin:4px 0}details summary{cursor:pointer;color:var(--accent)}
"""
JS = """
document.querySelectorAll('[data-tabs]').forEach(function(g){var b=g.querySelectorAll('button');b.forEach(function(x){x.addEventListener('click',function(){
b.forEach(function(y){y.setAttribute('aria-selected',y===x);document.getElementById(y.dataset.for).hidden=(y!==x);});});});});
"""


def esc(s):
    return html.escape(str(s))


def inline(s):
    s = esc(s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\$([^$]+)\$', lambda m: m.group(1).replace('\\text{', '').replace('}', '').replace('\\times', '×')
               .replace('\\div', '÷').replace('\\rightarrow', '→'), s)
    return s


def markdown(text):
    """A small subset: paragraphs, bullet and numbered lists, bold, code. Enough for Agent E2's answer shape."""
    out, kind = [], None
    for line in (text or '').split('\n'):
        m = re.match(r'^\s*(?:[-*]|\d+\.)\s+(.*)$', line)
        if m:
            k = 'ol' if re.match(r'^\s*\d+\.', line) else 'ul'
            if kind != k:
                if kind:
                    out.append(f'</{kind}>')
                out.append(f'<{k}>')
                kind = k
            out.append(f'<li>{inline(m.group(1))}</li>')
            continue
        if kind:
            out.append(f'</{kind}>')
            kind = None
        if line.strip():
            h = re.match(r'^#+\s*(.*)$', line)
            out.append(f'<p><strong>{inline(h.group(1))}</strong></p>' if h else f'<p>{inline(line)}</p>')
    if kind:
        out.append(f'</{kind}>')
    return '\n'.join(out)


def table(head, rows, cls=None):
    th = ''.join(f'<th>{esc(h)}</th>' for h in head)
    body = ''
    for r in rows:
        cells = ''
        for i, c in enumerate(r):
            if isinstance(c, dict):
                cells += f'<td class="num c-{esc(c.get("band", "grey"))}">{esc(c["v"])}</td>'
            else:
                cells += f'<td{" class=num" if i and cls == "num" else ""}>{inline(c)}</td>'
        body += f'<tr>{cells}</tr>'
    return f'<div class="scroll"><table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'


def build(folder):
    sc = yaml.safe_load(open(os.path.join(folder, 'scenario.yaml')))
    turns = [open(os.path.join(folder, f)).read() for f in ('turn-1.txt', 'turn-2.txt') if os.path.exists(os.path.join(folder, f))]
    runs = []
    for m in sc['models']:
        p = os.path.join(folder, 'results', m['id'].replace('/', '_') + '.json')
        if os.path.exists(p):
            runs.append((m, json.load(open(p))))
    parts = [f'<h1>{esc(sc["title"])}</h1><p class="sub">{inline(sc["subtitle"])}</p>']
    parts.append('<div class="grid">' + ''.join(f'<div class="panel"><h3>{esc(b["title"])}</h3>{markdown(b["text"])}</div>'
                                                for b in sc['summary']) + '</div>')
    parts.append('<h2>The week</h2><div class="panel"><ol class="timeline">' +
                 ''.join(f'<li><strong>{esc(t["when"])}</strong>: {inline(t["what"])} <span class="note">{inline(t.get("seen", ""))}</span></li>'
                         for t in sc['week']) + '</ol></div>')
    parts.append('<h2>What the L2 specialist sees on Tuesday</h2>')
    for tb in sc['tables']:
        parts.append(f'<div class="panel"><h3>{esc(tb["title"])}</h3>{table(tb["head"], tb["rows"], "num")}'
                     f'<p class="note">{inline(tb.get("note", ""))}</p></div>')
    names = ["The specialist's first message", 'The follow-up, once the change calendar is open']
    for i, t in enumerate(turns, 1):
        parts.append(f'<h2>{names[i - 1] if i <= len(names) else f"Message {i}"}</h2><div class="panel"><pre>{esc(t)}</pre></div>')
        parts.append('<h3>Agent E2 answers</h3><div class="tabs" data-tabs>')
        for j, (m, r) in enumerate(runs):
            parts.append(f'<button data-for="t{i}m{j}" aria-selected="{str(j == 0).lower()}">{esc(m["label"])}</button>')
        parts.append('</div>')
        for j, (m, r) in enumerate(runs):
            tr = r.get(f'turn_{i}') or {}
            calls = [s for s in tr.get('trace', []) if s.get('prompt_tokens')]
            tok = sum((s.get('prompt_tokens') or 0) + (s.get('completion_tokens') or 0) for s in calls)
            sec = sum(s.get('latency') or 0 for s in calls)
            parts.append(f'<div id="t{i}m{j}" class="panel answer"{"" if j == 0 else " hidden"}>'
                         f'<p><span class="tag">{esc(m["id"])}</span><span class="tag">{esc(m["role"])}</span>'
                         f'<span class="tag">{len(calls)} model calls, {tok:,} tokens, {sec:.0f} s</span>'
                         f'<span class="tag">knowledge {esc(r.get("knowledge_commit", "")[:7])}</span></p>'
                         f'{markdown(tr.get("content"))}'
                         f'<details><summary>Files read ({len(tr.get("files_read", []))}), first 15</summary><pre>'
                         f'{esc(chr(10).join(tr.get("files_read", [])[:15]))}</pre></details></div>')
    parts.append('<h2>Checks an expert answer must pass</h2><div class="panel">')
    head = ['Message', 'Check', 'Knowledge'] + [m['label'] for m, _ in runs]
    rows = []
    for c in sc['checks']:
        row = ['first' if c['turn'] == 1 else 'follow-up', c['text'], ' '.join(f'`{k}`' for k in c['kb'])]
        for m, _ in runs:
            v = (sc.get('scores', {}).get(m['id'], {}) or {}).get(c['id'], 'fail')
            sym, cls = MARK[v]
            row.append(f'§{cls}§{sym}')
        rows.append(row)
    t = table(head, rows)
    t = re.sub(r'<td>§(pass|partial|fail|na)§(.)</td>', r'<td class="\1">\2</td>', t)
    totals = []
    for m, _ in runs:
        s = sc.get('scores', {}).get(m['id'], {}) or {}
        apply = [c for c in sc['checks'] if s.get(c['id']) != 'na']
        n = sum(1.0 if s.get(c['id']) == 'pass' else 0.5 if s.get(c['id']) == 'partial' else 0 for c in apply)
        totals.append(f'{esc(m["label"])}: {n:g} of {len(apply)}')
    parts.append(t + f'<p class="note">✓ pass, ◐ partial, ✗ fail, – not applicable. {"; ".join(totals)}. {inline(sc.get("scoring_note", ""))}</p></div>')
    parts.append('<h2>What the run taught us</h2><div class="panel">' + markdown(sc['lessons']) + '</div>')
    parts.append('<h2>How to run it again</h2><div class="panel">' + markdown(sc['rerun']) + '</div>')
    page = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{esc(sc["short_title"])}</title><style>{CSS}</style></head><body><main>{"".join(parts)}</main>'
            f'<script>{JS}</script></body></html>')
    path = os.path.join(folder, 'index.html')
    open(path, 'w').write(page)
    return path


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    print(build(sys.argv[1]))
