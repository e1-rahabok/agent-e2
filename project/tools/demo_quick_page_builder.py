"""Build the page of one quick-answer demo: project/demo-site/quick-N-<name>/index.html, one self-contained file.

A quick-answer demo is one question an L2 specialist asks and one recorded Agent E2 answer: no incident, no steps.
The page uses the look of the scenario pages (project/tools/demo_page_builder.py): what the specialist sees on the
left, Agent E2 on the right. Reads from the demo folder:
  demo.yaml              the title, the readings shown as tiles, the claim the question carries, the knowledge files the
                         answer rests on, the benchmark twin, the run shown and the gate result;
  steps/step-1.txt       the question as the specialist typed it, sent to Agent E2 as is;
  results/<model>__<run>.json   Agent E2's answers, one file per gate run, written by project/tools/demo_scenario_executor.py --label.
The answer is shown as recorded; nothing in it is edited.

Usage: python3 project/tools/demo_quick_page_builder.py project/demo-site/quick-2-esxi-cpu-demand
"""
import json
import os
import sys

import yaml

from demo_page_builder import CSS, NAV_CSS, REPO, nav, computed_box, esc, inline, knowledge_ids, markdown, sources, tile

QUICK_CSS = """
.inc.q{border-color:#155e75;background:#0c2a3d}.inc.q .id{color:#7dd3fc;border-color:#155e75}
.claims{margin:0;padding:0 0 0 18px}.claims li{margin:4px 0}
.kb{display:flex;flex-direction:column;gap:6px}.kb a{font:12px var(--mono);text-decoration:none;color:#93c5fd}.kb span{color:var(--muted);font-size:12px}
.twin td.n{font:600 14px var(--mono)}.twin td.n.g{color:#86efac}
.foot{margin:0 16px 16px;font:11px var(--mono);color:var(--muted);text-align:right}
.wrap{padding-bottom:16px}aside{height:calc(100vh - 150px)}
"""


def build(folder):
    sc = yaml.safe_load(open(os.path.join(folder, 'demo.yaml')))
    run = sc['run']
    res = os.path.join(folder, 'results', run['model'].replace('/', '_') + f"__{run['shown']}.json")
    rec = json.load(open(res)) if os.path.exists(res) else {'steps': {}}
    r = (rec.get('steps') or {}).get('1')
    ask = open(os.path.join(folder, 'steps', 'step-1.txt')).read().strip()
    o = sc['object']
    see = (f'<div class="panel"><div class="h">What the specialist sees</div><p class="obj">{esc(o["kind"])} · {esc(o["name"])}</p>'
           f'<p class="objm">{esc(o["meta"])}</p><div class="tiles">' + ''.join(tile(t, False) for t in sc['tiles']) + '</div></div>')
    claims = ('<div class="panel"><div class="h">The claims on the table</div><ul class="claims">'
              + ''.join(f'<li>{inline(c)}</li>' for c in sc['claims']) + '</ul></div>')
    kb = ('<div class="panel"><div class="h">Where the answer comes from</div><div class="kb">'
          + ''.join(f'<a href="{esc(REPO + k["id"] + ".md")}" target="_blank" rel="noopener">{esc(k["id"])}</a><span>{inline(k["what"])}</span>'
                    for k in sc['knowledge']) + '</div></div>')
    tw = sc['twin']
    twin = ('<div class="panel"><div class="h">The same question in the benchmark</div>'
            f'<p class="note">Its multiple-choice twin, <a href="{esc(tw["url"])}" target="_blank" rel="noopener">{esc(tw["title"])}</a>, '
            'in the round of 2026-11-16: runs fully right out of 5, on three local models.</p>'
            '<div class="scroll twin"><table><thead><tr><th>Local model</th><th>With Agent E2</th><th>Model alone</th></tr></thead><tbody>'
            + ''.join(f'<tr><td>{esc(m)}</td><td class="n g">{a} of 5</td><td class="n">{b} of 5</td></tr>'
                      for m, a, b in zip(tw['models'], tw['e2'], tw['alone']))
            + '</tbody></table></div></div>')
    chat = f'<div class="msg you">{esc(ask)}</div>'
    if r:
        calls = [t for t in r.get('trace', []) if t.get('prompt_tokens')]
        sec = sum(t.get('latency') or 0 for t in calls)
        src = sources(r.get('content') or '', knowledge_ids())
        chat += (f'<div class="msg e2"><div class="who2">{"Agent E2 asks back" if r.get("type") == "clarify" else "Agent E2"}</div>'
                 f'{computed_box(r.get("computed"))}{markdown(r.get("content"))}'
                 + ('<div class="src">' + ''.join(f'<a href="{esc(u)}" target="_blank" rel="noopener">{esc(t)}</a>' for t, u in src) + '</div>' if src else '')
                 + f'<div class="meta">read {len(r.get("files_read") or [])} knowledge files · {len(calls)} model calls · {sec:.0f} s</div></div>')
    else:
        chat += '<div class="msg e2"><div class="who2">Agent E2</div><p class="note">Not run yet.</p></div>'
    about = '<details class="about"><summary>About this demo</summary>' + markdown(sc['about']) + '</details>'
    rec_line = (f'Recorded run · {esc(run["label"])} ({esc(run["params"])}) · {esc(run["shown"])} of the gate · '
                f'knowledge {esc((rec.get("knowledge_commit") or "")[:7])}')
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(sc['short_title'])}</title><style>{CSS}{QUICK_CSS}{NAV_CSS}</style></head><body>
<header><span class="brand">VCF Operations</span>{nav(sc['page'])}
<span class="pill" style="margin-left:auto">Ask Agent E2</span><span class="who">{esc(sc['user'])}</span></header>
<div class="inc q"><span class="id">Question</span><b>{esc(sc['title'])}</b><span class="m">one question · one recorded answer</span></div>
{about}
<div class="wrap"><main>{see}{claims}{kb}{twin}</main>
<aside><div class="ah"><b>Agent E2</b> <span class="pill">knowledge base · local model</span><div class="m">{esc(sc['context'])}</div></div>
<div class="chat" id="chat">{chat}</div></aside></div>
<div class="foot">{rec_line}</div></body></html>"""
    out = os.path.join(folder, 'index.html')
    open(out, 'w').write(page)
    return out


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    print(build(sys.argv[1]))
