"""Suggested questions for a whole page, chosen by the page's situation (POST /v1/suggest, answer_service.py).

The caller (PCM) sends the page: the object's kind, the pillar, the window and the page's KPI series. Agent E2 reads the
situation from them with its calculator and catalog, so the caller holds no domain rule (PCM decision D-124):

- level, from the KPI's band over the window. Performance: the band of the window's low end (the 5th percentile, so
  "good" means about 95% of the points are green) or of Now, whichever is worse; on a VM, the worse of its two layers.
  Capacity (cluster): the close-for-business decision (catalog/thresholds-capacity, decisions) over the last 24 hours:
  closed is bad, an orange input is medium, else good.
- movement. Performance: declining (last quarter against first quarter, at least the KPI change level, or a drop not
  recovered by Now) or dip (the worst point at least the change level from the median, and Now back within it). Capacity: rising Cluster Consumption, read only over
  7 days or more, since a 24-hour window shows the daily cycle, not growth.

Shown: with a movement, 2 movement questions and 1 metric question (how the page's KPI works, from the knowledge base); good
with no movement, 1 level and 2 metric questions; medium or bad, 2 level and 1 metric.

No model call: the situation is arithmetic and the questions are fixed text (user_suggestions.yaml).
"""
import os
import re
from datetime import datetime

import yaml

import arithmetic_calculator as calc
import expert_agent

HERE = os.path.dirname(os.path.abspath(__file__))
KPI = {('performance', 'cluster'): ['Cluster Performance'], ('performance', 'host'): ['ESXi Performance'],
       ('performance', 'vm'): ['VM Performance', 'Guest OS Performance']}
KIND = {'cluster': 'cluster', 'clustercomputeresource': 'cluster', 'host': 'host', 'esxi': 'host', 'esxi host': 'host',
        'hostsystem': 'host', 'vm': 'vm', 'virtualmachine': 'vm', 'virtual machine': 'vm'}
ORDER = ('green', 'yellow', 'orange', 'red')
LEVEL = {'green': 'good', 'yellow': 'medium', 'orange': 'bad', 'red': 'bad'}
MIN_POINTS = 12


def table(path=os.path.join(HERE, 'user_suggestions.yaml')):
    with open(path) as f:
        return yaml.safe_load(f)


def is_metric(question, tbl=None):
    """Whether the question is one of the metric questions (how a KPI works), as offered on a page: those are answered from
    the knowledge base, with no opening on how the page's KPI moved."""
    q = re.sub(r'\s+', ' ', str(question or '')).strip().lower()
    return any(q == m.lower() for kinds in (tbl or table()).values() for sets in kinds.values() for m in sets.get('metric') or [])


def _bare(name):
    return re.sub(r'\s*\(.*?\)\s*$', '', str(name or '')).strip().lower()


def _find(series, name):
    return next((s for s in series if _bare(s['name']) == name.lower()), None)


def _nums(s):
    return [v for v in s['values'] if isinstance(v, (int, float)) and not isinstance(v, bool)]


def _span_hours(s):
    ts = [t for t in (s.get('times') or []) if t]
    try:
        if len(ts) >= 2:
            return (datetime.fromisoformat(str(ts[-1])) - datetime.fromisoformat(str(ts[0]))).total_seconds() / 3600
    except ValueError:
        return None
    if s.get('minutes'):
        return s['minutes'] * (len(s['values']) - 1) / 60
    return None


def _last_day(s):
    """The values of the last 24 hours, which the close-for-business decision reads; the whole series without times."""
    ts = s.get('times') or []
    if len(ts) == len(s['values']) and ts and ts[-1]:
        try:
            end = datetime.fromisoformat(str(ts[-1]))
            return [v for t, v in zip(ts, s['values']) if t and (end - datetime.fromisoformat(str(t))).total_seconds() < 86400]
        except ValueError:
            pass
    minutes = s.get('minutes')
    return s['values'][-int(1440 // minutes):] if minutes else s['values']


def _performance(series, kind, cat):
    level, movement, worst_at, basis = None, None, None, []
    for name in KPI[('performance', kind)]:
        s = _find(series, name)
        if not s or len(_nums(s)) < MIN_POINTS:
            continue
        xs = _nums(s)
        low, now = calc.percentile(xs, 5), xs[-1]
        band = max(calc.score_band(low), calc.score_band(now), key=ORDER.index)
        level = band if level is None else max(level, band, key=ORDER.index)
        basis.append(f'{s["name"]}: 5th percentile {low:g}%, Now {now:g}%: {band}.')
        row = cat.change_level(name)
        if not row:
            basis.append(f'{s["name"]}: no change level, so no movement is read.')
            continue
        d = calc.decline(xs, 'higher', row['value'])
        t = calc.trend(s['values'], 'higher', row['value'])
        if d['declining']:
            movement = 'declining'
            basis.append(f'{s["name"]}: declining, median {d["first"]:g}% in the first quarter, {d["last"]:g}% in the last '
                         f'(change level {row["value"]:g} points).')
        elif t['verdict'] == 'worsened' and t['median'] - now >= row['value']:
            movement = 'declining'  # a drop not recovered by the end of the window is still under way
            basis.append(f'{s["name"]}: dropped to {t["worst"]:g}% and not recovered: Now {now:g}%, median {t["median"]:g}%.')
        elif t['verdict'] == 'worsened' and movement is None:
            movement, worst_at = 'dip', expert_agent._time_of(s, t['worst_index'])
            basis.append(f'{s["name"]}: dip to {t["worst"]:g}%, {t["worse_move"]:g} points below its median {t["median"]:g}%.')
    return (LEVEL[level] if level else None), movement, worst_at, basis


def _capacity(series, cat, production=True):
    basis = []
    cons, perf, risk = (_find(series, n) for n in ('Cluster Consumption', 'Cluster Performance', 'Cluster Risk'))
    if not cons or len(_nums(cons)) < MIN_POINTS:
        return None, None, basis
    lim = {r['id']: r['value'] for r in cat._q("SELECT id, value FROM thresholds WHERE use = 'decision' AND id LIKE 'closure-cluster-%'")}
    c95 = calc.percentile(_last_day(cons), 95)
    p5 = calc.percentile(_last_day(perf), 5) if perf and _nums(perf) else None
    r95 = calc.percentile(_last_day(risk), 95) if risk and _nums(risk) else None
    c_band = 'red' if c95 > lim['closure-cluster-consumption-red'] else 'orange' if c95 > lim['closure-cluster-consumption-orange'] else 'clear'
    p_band = None if p5 is None else 'red' if p5 < lim['closure-cluster-performance-red'] else \
        'orange' if p5 < lim['closure-cluster-performance-orange'] else 'clear'
    risk_limit = lim['closure-cluster-risk-prod' if production else 'closure-cluster-risk-nonprod']
    closed = 'red' in (c_band, p_band) or (c_band == p_band == 'orange' and r95 is not None and r95 > risk_limit)
    basis.append(f'Close-for-business, last 24 hours: Cluster Consumption 95th percentile {c95:g}% ({c_band})'
                 + (f', Cluster Performance 5th percentile {p5:g}% ({p_band})' if p5 is not None else '')
                 + (f', Cluster Risk 95th percentile {r95:g}%' if r95 is not None else '') + f': {"closed" if closed else "open"}.')
    level = 'bad' if closed else 'medium' if 'orange' in (c_band, p_band) else 'good'
    movement, span = None, _span_hours(cons)
    row = cat.change_level('Cluster Consumption')
    if span is not None and span >= 7 * 24 and row:
        d = calc.decline(_nums(cons), 'lower', row['value'])
        if d['declining']:
            movement = 'rising'
            basis.append(f'Cluster Consumption rising: median {d["first"]:g}% in the first quarter, {d["last"]:g}% in the last.')
    elif span is not None and span < 7 * 24:
        basis.append('Growth is not read under 7 days: the window shows the daily cycle.')
    return level, movement, basis


def suggest(facts, cat, tbl=None, screen_time=lambda x: x):
    """{situation: {pillar, kind, level, movement}, questions: [3 at most], basis: [plain lines]}. Empty questions when the
    page is outside release 1.0 or its KPI series is missing: the caller keeps its own general questions."""
    tbl = tbl or table()
    facts = facts or {}
    pillar = str(facts.get('pillar') or '').strip().lower()
    obj = facts.get('object') or {}
    kind = KIND.get(str(obj.get('kind') or facts.get('kind') or '').strip().lower())
    sets = (tbl.get(pillar) or {}).get(kind)
    out = {'situation': {'pillar': pillar, 'kind': kind, 'level': None, 'movement': None}, 'questions': [], 'basis': []}
    if not sets:
        out['basis'].append('No suggested questions for this page in release 1.0.')
        return out
    series = expert_agent._series(facts, [], limit=20)
    worst_at = None
    if pillar == 'performance':
        level, movement, worst_at, basis = _performance(series, kind, cat)
    else:
        level, movement, basis = _capacity(series, cat, production=facts.get('production', True) is not False)
    out['basis'] += basis
    out['situation'].update(level=level, movement=movement)
    if level is None:
        out['basis'].append('No KPI series with 12 points or more.')
        return out
    m = sets.get('metric') or []
    qs = sets[movement][:2] + m[:1] if movement else sets[level][:1] + m[:2] if level == 'good' else sets[level][:2] + m[:1]
    when = screen_time(str(worst_at)) if worst_at else 'its worst point'
    out['questions'] = [q.replace('at {time}', f'at {when}' if worst_at else 'at its worst point') for q in qs]
    return out
