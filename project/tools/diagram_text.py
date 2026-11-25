"""Text form of the SVG diagrams, generated from the SVG itself.

A picture gives a machine reader nothing, and a hand-written twin drifts. This reads an SVG drawn by the diagram
scripts (diagram_kit.py, product_diagram.py) and writes what it shows as Markdown: the title, the colour key, the boxes
nested as they are drawn, and every arrow with its two ends and its label. The text goes under the image in the root
documents, inside a <details> block, so the raw file carries the whole diagram. Never edit that block by hand.

    python3 project/tools/diagram_text.py          # update the blocks in the root documents
    python3 project/tools/diagram_text.py --check  # report blocks that differ (rules_check.py calls this)
"""
import math
import os
import re
import sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS = ['ARCHITECTURE.md', 'KNOWLEDGE-ENGINEERING.md']
NS = '{http://www.w3.org/2000/svg}'
IMAGE = re.compile(r'(!\[[^\]]*\]\((images/[^)]+\.svg)\)\n)(?:\n?<details>\n<summary>Text of the diagram.*?</details>\n)?', re.S)
SUMMARY = 'Text of the diagram, for readers that cannot see it'


def _num(v, default=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def _parse(path):
    tree = ET.parse(path)
    root = tree.getroot()
    cw, ch = _num(root.get('width')), _num(root.get('height'))
    rects, texts, paths = [], [], []
    for el in root.iter():
        tag = el.tag.replace(NS, '')
        if tag == 'rect' and el.get('x') is not None:
            rects.append(dict(x=_num(el.get('x')), y=_num(el.get('y')), w=_num(el.get('width')), h=_num(el.get('height')), fill=(el.get('fill') or '').lower()))
        elif tag == 'text':
            s = ''.join(el.itertext()).strip()
            if s:
                x, y, n = _num(el.get('x')), _num(el.get('y')), len(s)
                anchor = el.get('text-anchor') or 'start'
                cx = x + n * 3 if anchor == 'start' else x - n * 3 if anchor == 'end' else x
                texts.append(dict(x=x, y=y, s=s, size=_num(el.get('font-size'), 12), bold=el.get('font-weight') == 'bold', cx=cx, cy=y - 4, anchor=anchor))
        elif tag == 'path' and (el.get('marker-end') or el.get('marker-start')):
            nums = [float(v) for v in re.findall(r'-?\d+(?:\.\d+)?', el.get('d') or '')]
            pts = list(zip(nums[0::2], nums[1::2]))
            if len(pts) >= 2:
                paths.append(dict(pts=pts, both=bool(el.get('marker-start') and el.get('marker-end')), dashed=bool(el.get('stroke-dasharray'))))
    return cw, ch, rects, texts, paths


def _inside(px, py, r, pad=0.0):
    return r['x'] - pad <= px <= r['x'] + r['w'] + pad and r['y'] - pad <= py <= r['y'] + r['h'] + pad


def _dist(px, py, pts):
    best = 1e9
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        dx, dy = x2 - x1, y2 - y1
        L = dx * dx + dy * dy
        u = 0 if L == 0 else max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / L))
        best = min(best, math.hypot(px - (x1 + u * dx), py - (y1 + u * dy)))
    return best


def _container(px, py, cards, pad=0.0):
    hits = [c for c in cards if _inside(px, py, c, pad)]
    return min(hits, key=lambda c: c['w'] * c['h']) if hits else None


def _hue(fill):
    import colorsys
    m = re.fullmatch(r'#([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})', fill)
    if not m:
        return fill
    h, l, sat = colorsys.rgb_to_hls(*(int(v, 16) / 255 for v in m.groups()))
    if sat < 0.15:
        return 'grey' if l < 0.97 else 'white'
    d = h * 360
    for lo, hi, name in ((0, 15, 'red'), (15, 55, 'orange'), (55, 80, 'yellow'), (80, 170, 'green'), (170, 255, 'blue'), (255, 320, 'purple'), (320, 361, 'red')):
        if lo <= d < hi:
            return name
    return fill


def svg_to_text(path):
    cw, ch, rects, texts, paths = _parse(path)
    swatches = [r for r in rects if r['w'] <= 16 and r['h'] <= 16]
    cards = [r for r in rects if not (r['w'] <= 16 and r['h'] <= 16) and not (r['w'] >= cw - 1 and r['h'] >= ch - 1)]
    # label backgrounds drawn behind arrow labels are not boxes: they are small, white and one line high
    cards = [c for c in cards if not (c['h'] <= 16 and c['fill'] in ('#ffffff', '#fafafa'))]
    cards.sort(key=lambda c: (c['y'], c['x'], -c['w'] * c['h']))
    key, used = {}, set()
    for sw in swatches:
        near = [i for i, t in enumerate(texts) if abs(t['cy'] - (sw['y'] + 7)) <= 6 and sw['x'] + 14 <= t['x'] <= sw['x'] + 30]
        if near:
            key[sw['fill']] = texts[near[0]]['s']
            used.add(near[0])
    for c in cards:
        c['texts'] = []
    free = []
    for i, tx in enumerate(texts):
        if i in used:
            continue
        c = _container(tx['x'] + 2 if tx['anchor'] == 'start' else tx['cx'], tx['cy'], cards)
        if c is None:
            free.append(tx)
        else:
            c['texts'].append(tx)
    # nesting and ids
    for c in cards:
        parents = [p for p in cards if p is not c and p['w'] * p['h'] > c['w'] * c['h'] and _inside(c['x'] + 1, c['y'] + 1, p) and _inside(c['x'] + c['w'] - 1, c['y'] + c['h'] - 1, p)]
        c['parent'] = min(parents, key=lambda p: p['w'] * p['h']) if parents else None
        c['kids'] = []
    for c in cards:
        if c['parent'] is not None:
            c['parent']['kids'].append(c)
    n = [0]

    def number(c):
        n[0] += 1
        c['id'] = f'n{n[0]}'
        for k in sorted(c['kids'], key=lambda k: (k['y'], k['x'])):
            number(k)
    for c in [c for c in cards if c['parent'] is None]:
        number(c)

    def rows(c):
        out = []
        for tx in sorted(c['texts'], key=lambda t: (round(t['y'] / 3), t['x'])):
            if out and abs(out[-1][0]['y'] - tx['y']) <= 3:
                out[-1].append(tx)
            else:
                out.append([tx])
        return out

    def title_and_body(c):
        rs = rows(c)
        if not rs:
            return '', ''
        flat = [t for r in rs for t in r]
        first = max(flat, key=lambda t: (t['bold'], t['size'], -flat.index(t)))
        rest = [t for t in flat if t is not first]
        if re.fullmatch(r'\d', first['s']) and rest:  # band number in its circle
            first = dict(first, s=f"{first['s']}  {rest[0]['s']}")
            rest = rest[1:]
        return first['s'], (' | ' if c['kids'] else ' ').join(t['s'] for t in rest)

    # free text: title, subtitle, arrow labels (small), notes
    free.sort(key=lambda t: (t['y'], t['x']))
    title = next((t['s'] for t in free if t['size'] >= 18), '')
    ty = next((t['y'] for t in free if t['size'] >= 18), 0)
    subtitle = next((t['s'] for t in free if t is not None and t['size'] < 18 and 0 < t['y'] - ty <= 30), '')
    labels, notes = [], []
    for t in free:
        if t['size'] >= 18 or (t['s'] == subtitle and 0 < t['y'] - ty <= 30):
            continue
        (labels if t['size'] <= 10.6 else notes).append(t)
    edges = []
    for p in paths:
        s, e = p['pts'][0], p['pts'][-1]
        a = _container(s[0], s[1], cards, 4)
        b = _container(e[0], e[1], cards, 4)
        if a is not b:  # an arrow inside one box is a legend sample
            edges.append(dict(src=a, dst=b, p=p, lab=[]))
    for t in labels:
        best = min(edges, key=lambda e: _dist(t['cx'], t['cy'], e['p']['pts']), default=None)
        if best is not None and _dist(t['cx'], t['cy'], best['p']['pts']) <= 70:
            best['lab'].append(t)
        else:
            notes.append(t)
    notes.sort(key=lambda t: (t['y'], t['x']))

    lines = []
    if title:
        lines.append(f'**{title}.** {subtitle}'.strip())
    if key:
        lines.append('Colour key: ' + '; '.join(f'{_hue(fill)} = {lab}' for fill, lab in key.items()) + '.')

    def tag(c):
        lab = key.get(c['fill'])
        return f' ({lab})' if lab else ''

    def outline(c, depth):
        t, b = title_and_body(c)
        if t or b:
            lines.append('  ' * depth + f"- {c['id']} **{t}**{tag(c)}" + (f': {b}' if b else ''))
            depth += 1
        for k in sorted(c['kids'], key=lambda k: (k['y'], k['x'])):
            outline(k, depth)
    lines.append('')
    lines.append('Boxes, nested as drawn:')
    for c in [c for c in cards if c['parent'] is None]:
        outline(c, 0)

    def name(c):
        if c is None:
            return '(outside any box)'
        t, _ = title_and_body(c)
        return f"{c['id']} {t}".strip()
    if edges:
        lines.append('')
        lines.append('Arrows (from, to, label):')
        for e in edges:
            lab = ' '.join(t['s'] for t in sorted(e['lab'], key=lambda t: (t['y'], t['x'])))
            arrow = '<->' if e['p']['both'] else ('-->' if not e['p']['dashed'] else '..>')
            lines.append(f"- {name(e['src'])} {arrow} {name(e['dst'])}" + (f': {lab}' if lab else ''))
    if notes:
        lines.append('')
        lines.append('Notes on the diagram:')
        for t in notes:
            lines.append('- ' + re.sub(r'^- ', '', t['s']))
    lines.append('')
    lines.append('Arrows: `-->` solid, `..>` dashed.')
    return '\n'.join(lines)


def block(svg_rel):
    return f'<details>\n<summary>{SUMMARY}</summary>\n\n{svg_to_text(os.path.join(ROOT, svg_rel))}\n\n</details>\n'


def sync(write):
    problems = []
    for doc in DOCS:
        p = os.path.join(ROOT, doc)
        s = open(p, encoding='utf-8').read()

        def repl(m):
            return m.group(1) + '\n' + block(m.group(2))
        new = IMAGE.sub(repl, s)
        if new != s:
            problems.append(f'{doc}: text of a diagram is missing or out of date (python3 project/tools/diagram_text.py)')
            if write:
                open(p, 'w', encoding='utf-8').write(new)
    return problems


def check(bad):
    for msg in sync(False):
        bad(msg.split(':')[0], msg.split(': ', 1)[1])


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--print':
        print(svg_to_text(sys.argv[2]))
    else:
        probs = sync(write='--check' not in sys.argv)
        for pr in probs:
            print(pr)
        sys.exit(1 if probs and '--check' in sys.argv else 0)
