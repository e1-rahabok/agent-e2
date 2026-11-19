"""Build the page of one demo scenario: project/demo-site/<scenario>/index.html, one self-contained file.

The page looks like the L2 specialist's workspace: the incident on top, the evidence of the current object on the left,
Agent E2 on the right, a stepper at the bottom. Each step replays one narrow question, the readings Agent E2 fetched, and its recorded answer.
Reads from the scenario folder:
  scenario.yaml          the incident, the evidence shown at each step, the specialist's pinned findings, the end screen;
  steps/step-N.txt       the specialist's question, a blank line, the readings Agent E2 reads from VCF Operations;
  results/<model>.json   Agent E2's answers, written by project/tools/demo_scenario_executor.py.
The answers and the computed facts are shown as recorded; nothing in them is edited.

Usage: python3 project/tools/demo_page_builder.py project/demo-site/scenario-1-memory-tiering
"""
import glob
import html
import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPO = 'https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/'
KB_URL = 'https://knowledge.broadcom.com/external/article/'
BAND = {'green': '#22c55e', 'yellow': '#eab308', 'orange': '#f97316', 'red': '#ef4444', 'grey': '#64748b'}

CSS = """
:root{--bg:#0b1220;--panel:#111a2e;--panel2:#16213a;--ink:#e2e8f0;--muted:#94a3b8;--line:#26324a;--accent:#38bdf8;
--g:#22c55e;--y:#eab308;--o:#f97316;--r:#ef4444;--grey:#64748b;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
*{box-sizing:border-box}html,body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
a{color:var(--accent)}button{font:inherit;color:inherit}
header{position:sticky;top:0;z-index:5;background:rgba(11,18,32,.96);border-bottom:1px solid var(--line);display:flex;gap:12px;align-items:center;
padding:10px 16px;flex-wrap:wrap}.brand{font-weight:700;font-size:16px}.pill{font:12px var(--mono);color:var(--accent);border:1px solid var(--line);
border-radius:6px;padding:2px 8px}.tabs{display:flex;gap:4px;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:3px;margin-left:auto}
.tabs button{border:0;background:none;padding:5px 12px;border-radius:6px;cursor:pointer;color:var(--muted)}.tabs button[aria-selected=true]{background:var(--accent);color:#06263a;font-weight:600}
.who{font-size:12px;color:var(--muted);border:1px solid var(--line);border-radius:8px;padding:4px 10px}
.inc{margin:14px 16px 0;padding:10px 14px;border:1px solid #7f1d1d;background:#1d0f14;border-radius:10px;display:flex;gap:10px 16px;flex-wrap:wrap;align-items:baseline}
.inc .id{font:12px var(--mono);color:#fca5a5;border:1px solid #7f1d1d;border-radius:6px;padding:1px 8px}.inc b{font-size:15px}.inc .m{color:var(--muted);font-size:13px}
.wrap{display:grid;grid-template-columns:minmax(0,2fr) minmax(0,1fr);gap:14px;padding:14px 16px 90px;max-width:1500px;margin:0 auto}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px;margin-bottom:14px}
.h{font:600 12px var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin:0 0 10px;display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.crumb{display:flex;gap:6px;flex-wrap:wrap;align-items:center;font:12px var(--mono);margin-bottom:12px}.crumb span{border:1px solid var(--line);border-radius:6px;padding:3px 8px;color:var(--muted)}
.crumb span.on{border-color:var(--accent);color:var(--accent)}.crumb i{color:var(--muted);font-style:normal}
.obj{font-size:18px;font-weight:700;margin:0}.objm{color:var(--muted);font-size:13px;margin:2px 0 12px}
.tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:10px}
.tile{background:var(--panel2);border:1px solid var(--line);border-left:4px solid var(--grey);border-radius:8px;padding:9px 11px;position:relative}
.tile.sel{outline:2px solid var(--accent);outline-offset:1px}.tile.sel:after{content:'✓';position:absolute;top:6px;right:9px;color:var(--accent);font-weight:700}
.tile .l{font-size:12px;color:var(--muted);padding-right:14px}.tile .v{font:600 20px var(--mono);margin-top:2px}.tile .u{font-size:12px;color:var(--muted);margin-left:4px}
.tile .n{font-size:11px;color:var(--muted)}
.b-green{border-left-color:var(--g)}.b-yellow{border-left-color:var(--y)}.b-orange{border-left-color:var(--o)}.b-red{border-left-color:var(--r)}
table{border-collapse:collapse;width:100%;font-size:13px}th,td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
th{color:var(--muted);font-weight:600}.scroll{overflow-x:auto}td.c{font-family:var(--mono);text-align:center;font-weight:600}
td.c-green{background:rgba(34,197,94,.16);color:#86efac}td.c-yellow{background:rgba(234,179,8,.16);color:#fde047}td.c-orange{background:rgba(249,115,22,.18);color:#fdba74}
td.c-red{background:rgba(239,68,68,.2);color:#fca5a5}td.c-grey{color:var(--muted)}
code{font:12px var(--mono);background:#0b1426;border:1px solid var(--line);border-radius:4px;padding:0 4px}
svg text{fill:var(--muted);font:12px var(--mono)}.chart{overflow-x:auto}.chart svg{min-width:560px;display:block}.note{color:var(--muted);font-size:12px}
.find li{margin:6px 0}.find li b{color:var(--accent);font-family:var(--mono);margin-right:6px}
aside{position:sticky;top:64px;align-self:start;height:calc(100vh - 160px);min-height:520px;display:flex;flex-direction:column;background:var(--panel);
border:1px solid var(--line);border-radius:10px}
.ah{padding:12px 14px;border-bottom:1px solid var(--line)}.ah b{font-size:15px}.ah .m{font:11px var(--mono);color:var(--accent)}
.chat{flex:1;overflow-y:auto;padding:12px 14px;display:flex;flex-direction:column;gap:12px}
.msg{border-radius:10px;padding:10px 12px;font-size:13px}.you{background:#0c2a3d;border:1px solid #155e75;align-self:flex-end;max-width:92%}
.e2{background:var(--panel2);border:1px solid var(--line)}.e2 .who2{font:600 11px var(--mono);color:var(--accent);margin-bottom:4px}
.e2 p{margin:5px 0}.l1 p{margin:6px 0}.rc{border-color:#0e7490}.rc p{margin:6px 0}.rc ul{margin:4px 0 8px 18px;padding:0}.rc h4{margin:10px 0 4px;font-size:13px;color:#cbd5e1}.l1 ul{margin:4px 0 8px 18px;padding:0}.l1 h4{margin:12px 0 4px;font-size:13px;color:#cbd5e1}.e2 ul,.e2 ol{margin:5px 0 5px 18px;padding:0}.e2 h4{margin:10px 0 4px;font-size:13px;color:#cbd5e1}
.att summary{cursor:pointer;color:#7dd3fc;font-size:12px;margin-top:6px}.att pre{white-space:pre-wrap;font:11px var(--mono);color:var(--muted);margin:6px 0 0}
.calc{border:1px solid #0e7490;background:#071d2a;border-radius:8px;padding:8px 10px;margin:6px 0 8px}.calc .t{font:600 11px var(--mono);color:#67e8f9}
.calc .x{font:12px var(--mono);color:#e0f2fe;margin-top:3px}.calc .w{font-size:11px;color:var(--muted);margin-top:3px}
.src{display:flex;flex-wrap:wrap;gap:5px;margin-top:8px}.src a{font:11px var(--mono);border:1px solid var(--line);border-radius:999px;padding:1px 8px;text-decoration:none;color:#93c5fd}
.meta{font:11px var(--mono);color:var(--muted);margin-top:6px}.sys{font-size:12px;color:var(--muted);text-align:center}
.ask{border-top:1px solid var(--line);padding:10px;display:flex;gap:8px}.ask .in{flex:1;min-width:0;background:var(--bg);border:1px solid var(--line);border-radius:8px;
padding:8px 10px;color:var(--muted);font-size:13px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.ask button{background:var(--accent);color:#06263a;border:0;border-radius:8px;padding:8px 12px;font-weight:700;cursor:pointer;white-space:nowrap}
.ask button:disabled{opacity:.4;cursor:default}
.step{position:fixed;left:0;right:0;bottom:0;z-index:6;background:rgba(11,18,32,.97);border-top:1px solid var(--line);display:flex;gap:10px;align-items:center;
padding:8px 16px;flex-wrap:wrap}.step button{background:var(--panel2);border:1px solid var(--line);border-radius:8px;padding:5px 12px;cursor:pointer}
.step .lab{font:600 12px var(--mono)}.step .rec{margin-left:auto;font:11px var(--mono);color:var(--muted)}
details.about{margin:10px 16px 0;color:var(--muted);font-size:13px}details.about summary{cursor:pointer;color:var(--accent)}details.about ul{margin:6px 0 0 18px;padding:0}
@media (max-width:900px){.wrap{grid-template-columns:minmax(0,1fr)}aside{position:static;height:auto;min-height:0}.chat{max-height:none}.tabs{margin-left:0}}
"""

JS = """
var views=document.querySelectorAll('[data-view]'),ups=document.querySelectorAll('[data-upto]'),last=%LAST%,cur=0;
var asks=%ASKS%;
function show(i){cur=Math.max(0,Math.min(last,i));
views.forEach(function(e){e.hidden=(+e.dataset.view!==cur);});
ups.forEach(function(e){e.hidden=(+e.dataset.upto>cur);});
document.querySelectorAll('.crumb span').forEach(function(s){s.className=(+s.dataset.at===+(document.querySelector('[data-view="'+cur+'"]').dataset.at||-1))?'on':'';});
document.getElementById('lab').textContent=cur===0?'Start':(cur===last?'End':'Step '+cur+' of '+(last-1));
document.getElementById('prev').disabled=cur===0;document.getElementById('next').disabled=cur===last;
var a=asks[cur]||'';document.getElementById('in').textContent=a||'Replay ended';document.getElementById('send').disabled=!a;
var c=document.getElementById('chat');c.scrollTop=c.scrollHeight;
var m=document.querySelectorAll('.chat [data-upto="'+cur+'"]');if(m.length&&window.innerWidth>900){c.scrollTop=m[0].offsetTop-c.offsetTop-8;}
document.getElementById('send').textContent=(cur===last-1)?'Open':'Ask';}
document.getElementById('prev').onclick=function(){show(cur-1);};document.getElementById('next').onclick=function(){show(cur+1);};
document.getElementById('send').onclick=function(){show(cur+1);};
document.addEventListener('keydown',function(e){if(e.key==='ArrowRight')show(cur+1);if(e.key==='ArrowLeft')show(cur-1);});
document.querySelectorAll('.tabs button').forEach(function(b){b.onclick=function(){document.querySelectorAll('.tabs button').forEach(function(x){
x.setAttribute('aria-selected',x===b);document.getElementById(x.dataset.for).hidden=(x!==b);});};});
show(0);
"""


def esc(s):
    return html.escape(str(s))


def inline(s):
    s = esc(s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'(?<![*\w])\*([^*\n]+)\*(?!\*)', r'<i>\1</i>', s)
    s = re.sub(r'\$([^$]+)\$', lambda m: m.group(1).replace('\\text{', '').replace('}', '').replace('{', '').replace('\\times', '×')
               .replace('\\div', '÷').replace('\\rightarrow', '→').replace('\\approx', '≈').replace('\\', ''), s)
    return s


def markdown(text):
    """A small subset for Agent E2's answers: headings, paragraphs, lists, tables, code blocks, bold, code."""
    out, kind, rows, code = [], None, [], None
    lines = (text or '').split('\n') + ['']

    def close():
        nonlocal kind, rows
        if kind:
            out.append(f'</{kind}>')
            kind = None
        if rows:
            body = ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in rows[1:])
            out.append('<div class="scroll"><table><thead><tr>' + ''.join(f'<th>{inline(c)}</th>' for c in rows[0]) +
                       f'</tr></thead><tbody>{body}</tbody></table></div>')
            rows = []
    for line in lines:
        if line.strip().startswith('```'):
            if code is None:
                close()
                code = []
            else:
                out.append('<pre>' + esc('\n'.join(code)) + '</pre>')
                code = None
            continue
        if code is not None:
            code.append(line)
            continue
        if line.strip().startswith('|'):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if all(re.fullmatch(r':?-{2,}:?', c) for c in cells if c):
                continue
            if kind:
                close()
            rows.append(cells)
            continue
        if rows:
            close()
        m = re.match(r'^\s*(?:[-*•]|\d+\.)\s+(.*)$', line)
        if m:
            k = 'ol' if re.match(r'^\s*\d+\.', line) else 'ul'
            if kind != k:
                close()
                out.append(f'<{k}>')
                kind = k
            out.append(f'<li>{inline(m.group(1))}</li>')
            continue
        close()
        if re.fullmatch(r'\s*(-{3,}|\*{3,})\s*', line):
            continue
        h = re.match(r'^#+\s*(.*)$', line)
        if h:
            out.append(f'<h4>{inline(h.group(1))}</h4>')
        elif line.strip():
            out.append(f'<p>{inline(line)}</p>')
    return '\n'.join(out)


def knowledge_ids():
    base = os.path.join(ROOT, 'knowledge')
    return sorted((os.path.relpath(p, base)[:-3] for p in glob.glob(os.path.join(base, '**', '*.md'), recursive=True)),
                  key=len, reverse=True)


def sources(text, ids):
    found, seen = [], set()
    leaf = {}
    for i in ids:
        leaf.setdefault(i.split('/')[-1], []).append(i)
    for i in ids:
        if i in text and not any(i in s for s in seen):
            seen.add(i)
            found.append(('/'.join(i.split('/')[-2:]), REPO + i + '.md'))
    for name, full in leaf.items():
        if len(full) == 1 and full[0] not in seen and re.search(r'(?<![\w/-])' + re.escape(name) + r'(?![\w-])', text) and '-' in name:
            seen.add(full[0])
            found.append(('/'.join(full[0].split('/')[-2:]), REPO + full[0] + '.md'))
    for kb in dict.fromkeys(re.findall(r'\bKB\s*(\d{6})\b', text)):
        found.append((f'KB {kb}', KB_URL + kb))
    return found


def tile(t, sel):
    return (f'<div class="tile b-{esc(t.get("band", "grey"))}{" sel" if sel else ""}"><div class="l">{esc(t["label"])}</div>'
            f'<div class="v">{esc(t["value"])}<span class="u">{esc(t.get("unit", ""))}</span></div>'
            f'<div class="n">{esc(t.get("note", ""))}</div></div>')


def line_chart(c):
    w, h, l, r, t, b = 900, 230, 44, 40, 16, 30
    xs, ymax = c['x'], c.get('ymax') or max(max(s['values']) for s in c['series'])
    px = lambda i: l + (w - l - r) * (i / max(1, len(xs) - 1))  # noqa: E731
    py = lambda v: t + (h - t - b) * (1 - v / ymax)  # noqa: E731
    g = [f'<line x1="{l}" y1="{py(0)}" x2="{w - r}" y2="{py(0)}" stroke="#26324a"/>']
    for k in range(0, 5):
        v = ymax * k / 4
        g.append(f'<text x="{l - 6}" y="{py(v) + 4}" text-anchor="end">{v:g}</text>'
                 f'<line x1="{l}" y1="{py(v)}" x2="{w - r}" y2="{py(v)}" stroke="#1b2740"/>')
    for i, x in enumerate(xs):
        g.append(f'<text x="{px(i)}" y="{h - 8}" text-anchor="middle">{esc(x)}</text>')
    th = c.get('threshold')
    if th:
        g.append(f'<line x1="{l}" y1="{py(th["value"])}" x2="{w - r}" y2="{py(th["value"])}" stroke="#eab308" stroke-dasharray="5 4"/>'
                 f'<text x="{w - r}" y="{py(th["value"]) - 5}" text-anchor="end" style="fill:#eab308">{esc(th["label"])}</text>')
    for s in c['series']:
        pts = ' '.join(f'{px(i):.1f},{py(v):.1f}' for i, v in enumerate(s['values']))
        g.append(f'<polyline points="{pts}" fill="none" stroke="#38bdf8" stroke-width="2"/>')
        for i, v in enumerate(s['values']):
            ring = i in (c.get('ring') or [])
            g.append(f'<circle cx="{px(i):.1f}" cy="{py(v):.1f}" r="{6 if ring else 2.5}" fill="{"none" if ring else "#38bdf8"}" '
                     f'stroke="{"#f97316" if ring else "none"}" stroke-width="2"/>')
            if ring:
                g.append(f'<text x="{px(i):.1f}" y="{py(v) - 10:.1f}" text-anchor="middle" style="fill:#fdba74">{v:g}</text>')
    svg = f'<div class="chart"><svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{esc(c["title"])}">{"".join(g)}</svg></div>'
    return f'<div class="h">{esc(c["title"])}</div>{svg}' + (f'<div class="note">{esc(c["note"])}</div>' if c.get('note') else '')


def bar_chart(c):
    w, lw, rh = 900, 100, 62
    h = rh * len(c['bars']) + 6
    sx = lambda v: lw + (w - lw - 10) * v / c['max']  # noqa: E731
    g = []
    for k, bar in enumerate(c['bars']):
        y = 18 + k * rh
        g.append(f'<text x="0" y="{y + 15}">{esc(bar["name"])}</text>')
        x0, legend = 0, []
        for s in bar['segments']:
            col = BAND[s.get('band', 'grey')]
            g.append(f'<rect x="{sx(x0):.1f}" y="{y}" width="{sx(x0 + s["value"]) - sx(x0):.1f}" height="20" rx="3" '
                     f'fill="{col}" fill-opacity=".45" stroke="#0b1220"/>')
            legend.append(f'<tspan style="fill:{col}">■</tspan> {esc(s["label"])}: {s["value"]:g} GB')
            x0 += s['value']
        g.append(f'<text x="{lw}" y="{y + 36}">{"   ".join(legend)}</text>')
        mk = bar.get('marker')
        if mk:
            g.append(f'<line x1="{sx(mk["value"]):.1f}" y1="{y - 3}" x2="{sx(mk["value"]):.1f}" y2="{y + 23}" stroke="#f97316" stroke-width="2"/>'
                     f'<text x="{sx(mk["value"]) - 4:.1f}" y="{y - 6}" text-anchor="end" style="fill:#fdba74">{esc(mk["label"])}</text>')
    svg = f'<div class="chart"><svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{esc(c["title"])}">{"".join(g)}</svg></div>'
    return f'<div class="h">{esc(c["title"])}</div>{svg}'


def table(head, rows):
    th = ''.join(f'<th>{esc(x)}</th>' for x in head)
    body = ''
    for r in rows:
        cells = ''
        for c in r:
            if isinstance(c, list):
                cells += f'<td class="c c-{esc(c[1])}">{c[0]:g}</td>' if isinstance(c[0], (int, float)) else f'<td class="c c-{esc(c[1])}">{esc(c[0])}</td>'
            else:
                cells += f'<td>{inline(c)}</td>'
        body += f'<tr>{cells}</tr>'
    return f'<div class="scroll"><table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'


def computed_box(lines):
    if not lines:
        return ''
    items = ''
    for ln in lines:
        m = re.match(r'^-?\s*(.*?)\s*\[(.*)\]\s*$', ln)
        main, why = (m.group(1), m.group(2)) if m else (ln.lstrip('- '), '')
        items += f'<div class="x">{esc(main)}</div>' + (f'<div class="w">{esc(why)}</div>' if why else '')
    return f'<div class="calc"><div class="t">▣ Computed by Agent E2 code (exact), not by the model</div>{items}</div>'


def build(folder):
    sc = yaml.safe_load(open(os.path.join(folder, 'scenario.yaml')))
    run = sc['run']
    res_path = os.path.join(folder, 'results', run['model'].replace('/', '_') + '.json')
    rec = json.load(open(res_path)) if os.path.exists(res_path) else {'steps': {}}
    ids = knowledge_ids()
    steps = sc['steps']
    last = len(steps) + 1
    path = [s['object']['name'] for s in steps]
    crumbs = list(dict.fromkeys(path))
    asks, left, chat, finds = {}, [], [], []

    inc = sc['incident']
    left.append(f'<section data-view="0" data-at="-1"><div class="panel l1"><div class="h">Ticket worklog · L1 note</div>'
                f'{markdown(sc["l1_note"])}</div><div class="panel"><p class="note">Cluster {esc(sc["cluster"])}: {esc(sc["cluster_meta"])}</p>'
                f'<p>{esc(sc["start"])}</p></div></section>')
    chat.append(f'<div class="sys" data-upto="0">{esc(sc["incident"]["id"])} loaded. Ask Agent E2: it reads VCF Operations and vCenter for you.</div>')
    for s in steps:
        n = s['n']
        text = open(os.path.join(folder, 'steps', f'step-{n}.txt')).read().strip()
        ask, _, attached = text.partition('\n\n')
        asks[n - 1] = ask
        o = s['object']
        body = (f'<div class="crumb">' + '<i>›</i>'.join(f'<span data-at="{k}">{esc(c)}</span>' for k, c in enumerate(crumbs)) + '</div>'
                f'<p class="obj">{esc(o["kind"])} · {esc(o["name"])}</p><p class="objm">{esc(o["meta"])}</p>')
        if s.get('tiles'):
            body += '<div class="tiles">' + ''.join(tile(t, True) for t in s['tiles']) + '</div>'
        if s.get('table'):
            body += table(s['table']['head'], s['table']['rows'])
        if s.get('risk'):
            body += table(s['risk']['head'], s['risk']['rows']) + f'<p class="note">{esc(s["risk"].get("note", ""))}</p>'
        panel = f'<div class="panel">{body}</div>'
        ch = s.get('chart')
        if ch:
            panel += '<div class="panel">' + (line_chart(ch) if ch['type'] == 'line' else bar_chart(ch)) + '</div>'
        left.append(f'<section data-view="{n}" data-at="{crumbs.index(o["name"])}">{panel}</section>')
        r = (rec.get('steps') or {}).get(str(n))
        nread = sum(1 for x in attached.splitlines()[1:] if x.strip())
        chat.append(f'<div class="msg you" data-upto="{n}">{esc(ask)}<details class="att"><summary>⇣ Agent E2 read {nread} lines from VCF Operations</summary>'
                    f'<pre>{esc(attached)}</pre></details></div>')
        if r:
            calls = [t for t in r.get('trace', []) if t.get('prompt_tokens')]
            sec = sum(t.get('latency') or 0 for t in calls)
            src = sources(r.get('content') or '', ids)
            kind = 'Agent E2 asks back' if r.get('type') == 'clarify' else 'Agent E2'
            chat.append(f'<div class="msg e2" data-upto="{n}"><div class="who2">{kind}</div>{computed_box(r.get("computed"))}'
                        f'{markdown(r.get("content"))}'
                        + ('<div class="src">' + ''.join(f'<a href="{esc(u)}" target="_blank" rel="noopener">{esc(t)}</a>' for t, u in src) + '</div>' if src else '')
                        + f'<div class="meta">read {len(r.get("files_read") or [])} knowledge files · {len(calls)} model calls · {sec:.0f} s</div></div>')
        else:
            chat.append(f'<div class="msg e2" data-upto="{n}"><div class="who2">Agent E2</div><p class="note">Not run yet.</p></div>')
        fol = s.get('follow')
        if fol and r:
            q = fol.get('quote')
            if q and q not in (r.get('content') or ''):
                sys.exit(f'step {n}: the follow quote is not in the recorded answer: {q!r}')
            chat.append(f'<div class="sys" data-upto="{n}">' + (f'Check next, from the answer: “{esc(q)}” → ' if q else '') + f'{esc(fol["note"])}</div>')
        if s.get('finding') and s['finding'] != 'TBD':
            finds.append(f'<li data-upto="{n}"><b>{n}</b>{inline(s["finding"])}</li>')
    e = sc['end']
    asks[len(steps)] = e.get('ask', 'Open the change calendar')
    left.append(f'<section data-view="{last}" data-at="{len(crumbs) - 1}"><div class="panel"><div class="h">{esc(e["title"])}</div>'
                + table(['Change', 'When', 'Team', 'What', 'Matches'], [[c['id'], c['when'], c['team'], c['what'], c['match']] for c in e['rows']])
                + f'<p>{esc(e["note"])}</p></div>'
                + f'<div class="panel rc"><div class="h">Root cause, written by the specialist</div>{markdown(e["root_cause"])}</div>'
                + (f'<div class="panel rc"><div class="h">Fix, proposed by the specialist</div>{markdown(e["remediation"])}</div>' if e.get('remediation') else '')
                + f'<div class="panel"><p><b>{esc(e["next"])}</b></p></div></section>')
    chat.append(f'<div class="sys" data-upto="{last}">{esc(e.get("chat", "Change calendar: the changes fall at the times Agent E2 flagged."))}</div>')
    pro = sc['proactive']
    proactive = (f'<div class="panel"><div class="h">Daily health check · {esc(sc["cluster"])}</div><p class="note">{esc(pro["intro"])}</p>'
                 + table(['Object', 'Symptom', 'Started', 'Status'], [[x['object'], x['symptom'], x['started'], x['status']] for x in pro['rows']]) + '</div>')
    about = '<details class="about"><summary>About this demo</summary>' + markdown(sc['about']) + '</details>'
    shas = list(dict.fromkeys((st.get('knowledge_commit') or rec.get('knowledge_commit') or '')[:7] for st in (rec.get('steps') or {}).values()))
    rec_line = (f'Recorded run · {esc(run["label"])} ({esc(run["params"])}) · knowledge {esc(", ".join(shas) or (rec.get("knowledge_commit") or "")[:7])}')
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(sc['short_title'])}</title><style>{CSS}</style></head><body>
<header><span class="brand">VCF Operations</span><span class="pill">vSphere specialist workspace</span>
<div class="tabs" role="tablist"><button aria-selected="true" data-for="reactive">Reactive: incidents</button><button aria-selected="false" data-for="proactive">Proactive: health</button></div>
<span class="who">{esc(sc['incident']['user'])}</span></header>
<div class="inc"><span class="id">{esc(sc['incident']['id'])} · {esc(sc['incident']['priority'])}</span><b>{esc(sc['incident']['title'])}</b>
<span>{esc(sc['incident']['summary'])}</span><span class="m">{esc(sc['incident']['escalated'])} · {esc(sc['incident']['now'])}</span></div>
{about}
<div class="wrap"><main><div id="reactive">{''.join(left)}<div class="panel find"><div class="h">Findings pinned by the specialist</div><ol style="list-style:none;margin:0;padding:0">{''.join(finds)}</ol></div></div>
<div id="proactive" hidden>{proactive}</div></main>
<aside><div class="ah"><b>Agent E2</b> <span class="pill">knowledge base · local model</span><div class="m">Context: {esc(sc['incident']['id'])} · {esc(sc['cluster'])}</div></div>
<div class="chat" id="chat">{''.join(chat)}</div>
<div class="ask"><div class="in" id="in"></div><button id="send">Ask</button></div></aside></div>
<div class="step"><button id="prev">◀</button><span class="lab" id="lab"></span><button id="next">▶</button><span class="note">← → keys</span><span class="rec">{rec_line}</span></div>
<script>{JS.replace('%LAST%', str(last)).replace('%ASKS%', json.dumps(asks))}</script></body></html>"""
    out = os.path.join(folder, 'index.html')
    open(out, 'w').write(page)
    return out


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    print(build(sys.argv[1]))
