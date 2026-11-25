"""Shared drawing helpers for the hand-laid SVG diagrams of the root documents.

Used by knowledge_diagram.py and document_diagrams.py. Call begin(), draw with t, box, band, frame, arrow and
legend, then finish(path). Each diagram defines the meaning of its colours in its own key; the hues are shared.
"""
from xml.sax.saxutils import escape

LH = 15
out = []
canvas = {'w': 0, 'h': 0}

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
    out.append(f'<rect x="10" y="{y}" width="{canvas["w"] - 20}" height="{h}" rx="10" fill="#fafafa" stroke="#c9c9c9"/>')
    out.append(f'<circle cx="38" cy="{y + 28}" r="14" fill="#333"/>')
    t(38, y + 33, str(num), 14, 'bold', '#fff', 'middle')
    t(62, y + 33, label, 16, 'bold', '#222')
    t(62, y + 52, sub, 12, 'normal', '#555')


def frame(x, y, w, h, label, sub=None):
    """A light group rectangle with a label, for boxes that belong together."""
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#fafafa" stroke="#c9c9c9"/>')
    t(x + 12, y + 22, label, 14, 'bold', '#222')
    if sub:
        t(x + 12, y + 38, sub, 11, 'normal', '#555')


def arrow(pts, label=None, lx=None, ly=None, color='#555555', dash=False):
    d = 'M ' + ' L '.join(f'{x} {y}' for x, y in pts)
    ds = ' stroke-dasharray="5 4"' if dash else ''
    out.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.5"{ds} marker-end="url(#ah)"/>')
    if label:
        wpx = len(label) * 6.1 + 8
        out.append(f'<rect x="{lx - wpx / 2:.0f}" y="{ly - 11}" width="{wpx:.0f}" height="15" fill="#ffffff" opacity="0.92"/>')
        t(lx, ly, label, 10.5, 'normal', color, 'middle')


def legend(x, y, items):
    """Colour key: items are (label, kind). Returns the x after the last item."""
    for label, kind in items:
        fill, stroke, _ = C[kind]
        out.append(f'<rect x="{x}" y="{y}" width="14" height="14" rx="3" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>')
        t(x + 20, y + 12, label, 11.5, 'normal', '#333')
        x += 20 + len(label) * 6.3 + 22
    return x


def begin(w, h):
    out.clear()
    canvas['w'], canvas['h'] = w, h
    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
               f'font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif">')
    out.append('<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
               'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#555555"/></marker></defs>')
    out.append(f'<rect width="{w}" height="{h}" fill="#ffffff"/>')


def finish(path):
    out.append('</svg>')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out) + '\n')
    print('wrote', path)
