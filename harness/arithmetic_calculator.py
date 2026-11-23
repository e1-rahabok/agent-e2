"""Calculator tool: exact arithmetic and unit conversion, so the model only chooses what to compute.

One entry point, evaluate(expression). Numbers without thousands separators. The expression may use + - * / ** % ( ), numbers, lists, and these functions:

  summation_to_percent(ms, interval_seconds=20, vcpus=1)   Summation time counter (Ready, Co-stop, Run ms) -> %
  percent_to_summation(percent, interval_seconds=20, vcpus=1)
  convert(value, "from_unit", "to_unit")                    KB MB GB TB (binary, vCenter), KiB..TiB, KBd..TBd (decimal),
                                                            b kb Mb Gb (bits, decimal), rates with ps or /s,
                                                            ns us µs ms s min h, Hz kHz MHz GHz
  capacity_ghz(cores, ghz_per_core)                         nominal CPU capacity
  pct(part, whole)                                          part as % of whole
  cpu_states(run, ready, costop, wait, vcpus=1)             esxtop state sum; 100% per vCPU
  used_pct(run, system, overlap)                            esxtop %USED = %RUN + %SYS - %OVRLP
  nvme_wait_pct(read_mbps, latency_s, vcpus=1)              share of vCPU time a VM waits for NVMe tier pages (Little's law)
  min max abs round sum avg

Every function adds a note naming the knowledge file or source that defines the rule.

A second entry point, trend(values, better, change), reads a whole KPI series (a list, not an expression): median, range,
the worst point's move from the median, and a verdict against the KPI change level.

step(values, better, change, width) finds when a score changed level; decline(values, better, change) tells a decline across the window (the last quarter against the first) from a single
dip; percentile(values, p) is the nearest-rank percentile the screens show.

A third, kpi_parts(rows), scores the parts of a KPI at one point with their catalog limits and splits the score the KPI
lost among them, so the model never ranks the parts by eye.
"""
import ast
import math
import operator

BYTE = {'B': 1, 'KB': 1024, 'MB': 1024 ** 2, 'GB': 1024 ** 3, 'TB': 1024 ** 4,
        'KIB': 1024, 'MIB': 1024 ** 2, 'GIB': 1024 ** 3, 'TIB': 1024 ** 4,
        'KBD': 1e3, 'MBD': 1e6, 'GBD': 1e9, 'TBD': 1e12}
BIT = {'b': 1 / 8, 'bit': 1 / 8, 'kb': 1e3 / 8, 'Kb': 1e3 / 8, 'Mb': 1e6 / 8, 'Gb': 1e9 / 8, 'Tb': 1e12 / 8}
TIME = {'NS': 1e-9, 'US': 1e-6, 'MS': 1e-3, 'S': 1, 'SEC': 1, 'SECONDS': 1, 'MIN': 60, 'MINUTES': 60, 'H': 3600, 'HOURS': 3600}
FREQ = {'HZ': 1, 'KHZ': 1e3, 'MHZ': 1e6, 'GHZ': 1e9}
SRC_STATS = 'vsphere/tools/vsphere-client/vcenter-statistics'


class CalcError(ValueError):
    pass


def _unit(u):
    """Return (kind, factor to base, is_rate, warning). Bits vs bytes is decided by letter case: b = bit, B = byte."""
    raw = u.strip().replace('\u00b5', 'u').replace('\u03bc', 'u')  # micro sign and Greek mu: µs = us
    warn = None
    rate = False
    for suf in ('/s', '/sec', 'ps'):
        if raw.endswith(suf) and len(raw) > len(suf):
            raw, rate = raw[:-len(suf)], True
            break
    if rate and raw == 'Kb':
        warn = ('"Kbps" is ambiguous: vCenter labels net.received and net.transmitted Kbps but measures kilobytes per second. '
                'Treated as kilobits; use KBps for those counters. See ' + SRC_STATS)
    if raw in BIT:
        return 'data', BIT[raw], rate, warn
    if raw.upper() in BYTE and raw[-1] != 'b':
        return 'data', BYTE[raw.upper()], rate, warn
    if not rate and raw.upper() in TIME:
        return 'time', TIME[raw.upper()], False, warn
    if not rate and raw.upper() in FREQ:
        return 'freq', FREQ[raw.upper()], False, warn
    raise CalcError(f'unknown unit {u!r}')


class Evaluator:
    OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv,
           ast.Mod: operator.mod, ast.FloorDiv: operator.floordiv, ast.Pow: operator.pow}

    def __init__(self):
        self.notes = []
        self.funcs = {
            'summation_to_percent': self.summation_to_percent, 'percent_to_summation': self.percent_to_summation,
            'convert': self.convert, 'capacity_ghz': self.capacity_ghz, 'pct': self.pct, 'cpu_states': self.cpu_states,
            'used_pct': self.used_pct, 'nvme_wait_pct': self.nvme_wait_pct, 'min': min, 'max': max, 'abs': abs, 'round': round, 'sum': sum,
            'avg': lambda xs: sum(xs) / len(xs), 'sqrt': math.sqrt}

    def note(self, text):
        if text not in self.notes:
            self.notes.append(text)

    # ---------- domain functions ----------
    def summation_to_percent(self, ms, interval_seconds=20, vcpus=1):
        self.note(f'Summation time counters (Ready, Co-stop, Run, Wait in ms): 100% = {interval_seconds:g} s x 1,000 ms per vCPU '
                  f'per sample. Real-time samples are 20 s; 1 Day points are 5 minutes (300 s). See {SRC_STATS} and '
                  'vsphere/technology/cpu/metrics/virtual-motherboard/ready.')
        return ms / (interval_seconds * 1000 * vcpus) * 100

    def percent_to_summation(self, percent, interval_seconds=20, vcpus=1):
        self.summation_to_percent(0, interval_seconds, vcpus)
        return percent / 100 * interval_seconds * 1000 * vcpus

    def convert(self, value, from_unit, to_unit):
        k1, f1, r1, w1 = _unit(str(from_unit))
        k2, f2, r2, w2 = _unit(str(to_unit))
        if k1 != k2 or r1 != r2:
            raise CalcError(f'cannot convert {from_unit} to {to_unit}')
        for w in (w1, w2):
            if w:
                self.note(w)
        if k1 == 'data':
            self.note('vCenter counters: KB = 1,024 bytes, KBps = 1,024 bytes per second; kb = 1,000 bits, kbps = 1,000 bits per '
                      f'second. 1 byte = 8 bits. esxtop network is in megabits. See {SRC_STATS}, section Units.')
        if k1 == 'freq':
            self.note('CPU frequency is decimal: 1 GHz = 1,000 MHz. See sp5-framework/observability/units.')
        return value * f1 / f2

    def capacity_ghz(self, cores, ghz_per_core):
        self.note('Nominal capacity = physical cores x base frequency (vSphere 9.1 docs, cluster totalmhz example). '
                  'Usage and Demand can exceed it with Turbo. See vsphere/technology/cpu/metrics/virtual-motherboard/demand.')
        return cores * ghz_per_core

    def pct(self, part, whole):
        if whole == 0:
            raise CalcError('pct: whole is 0')
        return part / whole * 100

    def cpu_states(self, run, ready, costop, wait, vcpus=1):
        self.note(f'esxtop: 100% = %RUN + %RDY + %CSTP + %WAIT per vCPU world; a VM group sums its vCPUs '
                  f'(expected total {100 * vcpus:g}%). Source: catalog/esxtop-fields formulas.')
        return run + ready + costop + wait

    def used_pct(self, run, system, overlap):
        self.note('esxtop: %USED = %RUN + %SYS - %OVRLP. %USED also moves with CPU frequency. Source: catalog/esxtop-fields formulas.')
        return run + system - overlap

    def nvme_wait_pct(self, read_mbps, latency_s, vcpus=1):
        self.note("NVMe wait (%) = VM NVMe read bandwidth (MB/s) x 256 pages per MB x host NVMe read latency (s) / VM vCPUs x 100 "
                  "(Little's law). It assumes one 4 KB page per fetch and that the fetch stalls the vCPU; if either fails, it "
                  'overstates the wait; during a vMotion, precopy reads may count too. Memory Contention does not count this wait. '
                  'See vsphere/object-types/cluster/cluster-performance, sections NVMe wait formula and Limitations.')
        if vcpus <= 0:
            raise CalcError('nvme_wait_pct: vcpus must be above 0')
        return read_mbps * 256 * latency_s / vcpus * 100

    # ---------- safe evaluation ----------
    def eval(self, node):
        if isinstance(node, ast.Expression):
            return self.eval(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float, str)) and not isinstance(node.value, bool):
            return node.value
        if isinstance(node, ast.List):
            return [self.eval(e) for e in node.elts]
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
            v = self.eval(node.operand)
            return -v if isinstance(node.op, ast.USub) else v
        if isinstance(node, ast.BinOp) and type(node.op) in self.OPS:
            a, b = self.eval(node.left), self.eval(node.right)
            if isinstance(node.op, ast.Pow) and abs(b) > 100:
                raise CalcError('exponent too large')
            if isinstance(a, str) or isinstance(b, str):
                raise CalcError('arithmetic on text')
            return self.OPS[type(node.op)](a, b)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in self.funcs:
            args = [self.eval(a) for a in node.args]
            kwargs = {k.arg: self.eval(k.value) for k in node.keywords}
            return self.funcs[node.func.id](*args, **kwargs)
        if isinstance(node, ast.Tuple):
            raise CalcError('write numbers without thousands separators (13856, not 13,856)')
        raise CalcError(f'not allowed: {ast.dump(node)[:80]}')


def trend(values, better='higher', change=None):
    """How a KPI score moved across a window, so the model never judges the size of a move (KPI change, thresholds-performance).

    values: the points in time order (None skipped). better: 'higher' or 'lower'. change: the KPI change level in points of
    the score, or None when the KPI has no row. The move is measured from the median of the window, never from one point:
    the worst point of a flat window is the bottom of its normal movement, not an event.
    Returns {points, median, low, high, worst, worst_index, worse_move, better_move, verdict, notes}; verdict is
    'worsened' or 'improved' (a move of at least the change level), 'steady', or None when no change level is set."""
    xs = [(i, float(v)) for i, v in enumerate(values) if isinstance(v, (int, float)) and not isinstance(v, bool)]
    if not xs:
        raise CalcError('trend: no values')
    srt = sorted(v for _, v in xs)
    n = len(srt)
    median = srt[n // 2] if n % 2 else (srt[n // 2 - 1] + srt[n // 2]) / 2
    sign = 1 if better == 'higher' else -1
    wi, worst = min(xs, key=lambda x: sign * x[1])
    best = srt[-1] if sign == 1 else srt[0]
    worse_move, better_move = round(sign * (median - worst), 2), round(sign * (best - median), 2)
    verdict = None
    if change is not None:
        verdict = 'worsened' if worse_move >= change else 'improved' if better_move >= change else 'steady'
    note = ('A KPI score moves at every point: it is a weighted average of sub-metrics read from the worst VM and the 90th '
            'percentile, and the VMs on top change. A move counts only from the median of the window and only at the KPI '
            'change level or more. See sp5-framework/performance/performance-kpi-design, section Reading a KPI over time, and '
            'catalog/thresholds-performance, section change.')
    return {'points': n, 'median': round(median, 2), 'low': srt[0], 'high': srt[-1], 'worst': worst, 'worst_index': wi,
            'worse_move': worse_move, 'better_move': better_move, 'verdict': verdict, 'notes': [note]}


SCORE_AT = (100.0, 75.0, 50.0, 25.0)
BANDS = ('green', 'yellow', 'orange', 'red')
SRC_SCORING = 'sp5-framework/performance/performance-kpi-design, section Scoring'


def percentile(values, p):
    """Nearest-rank percentile of the numbers in values (None skipped), as the screens show the 95th percentile."""
    xs = sorted(float(v) for v in values if isinstance(v, (int, float)) and not isinstance(v, bool))
    if not xs:
        raise CalcError('percentile: no values')
    return xs[max(0, math.ceil(p / 100 * len(xs)) - 1)]


def decline(values, better='higher', change=None):
    """Whether a KPI series declined across the window, not only dipped: the median of its last quarter against the median
    of its first quarter, in points of the score. A decline is a move of at least the KPI change level the worse way; a
    dip that recovered leaves the two quarters level. Returns {first, last, move, declining}; declining is None without a
    change level, and the series needs 12 points or more (3 per quarter)."""
    xs = [float(v) for v in values if isinstance(v, (int, float)) and not isinstance(v, bool)]
    if len(xs) < 12:
        raise CalcError('decline: fewer than 12 points')
    q = len(xs) // 4

    def med(part):
        s = sorted(part)
        n = len(s)
        return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
    first, last = med(xs[:q]), med(xs[-q:])
    move = round((first - last) if better == 'higher' else (last - first), 2)
    return {'first': round(first, 2), 'last': round(last, 2), 'move': move,
            'declining': None if change is None else move >= change}


def step(values, better='higher', change=None, width=12):
    """Where a KPI series made its largest step the worse way: at each point, the median of the width points before it
    against the median of the width points from it (width 12 = one hour at 5 minutes), so a single noisy point is no step.
    Returns {index, before, after, move, stepped}; stepped is True when the move is at least the KPI change level, None
    without one. A step tells when a score changed level; trend tells how far its worst point is from the median."""
    xs = [float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None for v in values]
    if sum(v is not None for v in xs) < 2 * width:
        raise CalcError('step: fewer than two widths of points')

    def med(part):
        s = sorted(v for v in part if v is not None)
        if not s:
            return None
        n = len(s)
        return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
    sign = 1 if better == 'higher' else -1
    best = None
    for i in range(width, len(xs) - width + 1):
        b, a = med(xs[i - width:i]), med(xs[i:i + width])
        if b is None or a is None:
            continue
        move = sign * (b - a)
        if best is None or move > best['move']:
            best = {'index': i, 'before': round(b, 2), 'after': round(a, 2), 'move': round(move, 2)}
    best['stepped'] = None if change is None else best['move'] >= change
    return best


def score_band(score):
    """The band of a 0-100% score where higher is better: green 100-75, yellow 75-50, orange 50-25, red 25-0
    (sp5-framework/performance/performance-kpi-design, section Scoring)."""
    for at, band in zip(SCORE_AT, BANDS):
        if score >= at - 25:
            return band
    return 'red'


def part_score(value, limits):
    """The score of one part (100 best, 0 worst) and its band, from its five limits: the values where the score is 100,
    75, 50, 25 and 0, falling in a straight line in between (SRC_SCORING). Limits going down mean higher is better.
    A range with no width (green as one value) holds no value."""
    lim = [float(x) for x in limits]
    v = float(value)
    if lim[-1] < lim[0]:
        v, lim = -v, [-x for x in lim]
    if v <= lim[0]:
        return 100.0, 'green'
    start = lim[0]
    for s0, band, end in zip(SCORE_AT, BANDS, lim[1:]):
        if end == start:
            continue
        if v < end or band == 'red':
            return s0 - min((v - start) / (end - start), 1.0) * 25.0, band
        start = end
    return 0.0, 'red'


def kpi_parts(rows):
    """How a KPI at one point is made of its parts (SRC_SCORING).

    rows: [{'name', 'value', 'limits' (five numbers), 'excluded_when_green' (bool)}]; a row without a value is left out.
    KPI = sum(score x weight) / sum(weight), weight = 2 ^ ((100 - score) / 25). The score the KPI lost, 100 - KPI, is
    the sum over the parts of (100 - score) x weight / sum(weight): each part's points lost, exact, adding up to the loss.
    A row marked excluded_when_green is left out while green (catalog/thresholds-performance, kpi).
    Returns {'kpi', 'lost', 'rows': [{'name', 'value', 'score', 'band', 'weight', 'points_lost', 'share'}] worst first,
    'left_out': [names], 'notes'}."""
    scored, left_out = [], []
    for r in rows:
        v = r.get('value')
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            continue
        score, band = part_score(v, r['limits'])
        if r.get('excluded_when_green') and band == 'green':
            left_out.append(r['name'])
            continue
        scored.append({'name': r['name'], 'value': v, 'score': score, 'band': band, 'weight': 2 ** ((100.0 - score) / 25.0)})
    if not scored:
        if not left_out:
            raise CalcError('kpi_parts: no part has a value')
        return {'kpi': 100.0, 'lost': 0.0, 'rows': [], 'left_out': left_out, 'notes': [f'Every part was left out while green: KPI 100. See {SRC_SCORING}.']}
    total = sum(r['weight'] for r in scored)
    kpi = sum(r['score'] * r['weight'] for r in scored) / total
    lost = 100.0 - kpi
    for r in scored:
        r['points_lost'] = (100.0 - r['score']) * r['weight'] / total
        r['share'] = 100.0 * r['points_lost'] / lost if lost > 0 else 0.0
    scored.sort(key=lambda r: -r['points_lost'])
    for r in scored:
        for k in ('score', 'weight', 'points_lost', 'share'):
            r[k] = round(r[k], 2)
    note = (f'Score per part from its five limits, KPI = sum(score x weight) / sum(weight), weight = 2 ^ ((100 - score) / 25); '
            f'points lost per part = (100 - score) x weight / sum(weight), which add up to 100 - KPI. See {SRC_SCORING}.')
    return {'kpi': round(kpi, 2), 'lost': round(lost, 2), 'rows': scored, 'left_out': left_out, 'notes': [note]}


def evaluate(expression):
    """Evaluate an expression. Returns {'expression', 'result', 'notes'} or {'expression', 'error'}."""
    expr = (expression or '').strip().replace('×', '*').replace('−', '-')
    ev = Evaluator()
    try:
        tree = ast.parse(expr, mode='eval')
        val = ev.eval(tree)
    except (CalcError, SyntaxError, TypeError, ZeroDivisionError, ValueError) as e:
        return {'expression': expression, 'error': f'{type(e).__name__}: {e}'}
    if isinstance(val, float):
        val = float(f'{val:.6g}') if abs(val) < 1e15 else val
    return {'expression': expression, 'result': val, 'notes': ev.notes}


if __name__ == '__main__':
    import json
    import sys
    print(json.dumps(evaluate(' '.join(sys.argv[1:])), indent=1, ensure_ascii=False))
