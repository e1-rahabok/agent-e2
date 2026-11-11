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
  min max abs round sum avg

Every function adds a note naming the knowledge file or source that defines the rule.
"""
import ast
import math
import operator

BYTE = {'B': 1, 'KB': 1024, 'MB': 1024 ** 2, 'GB': 1024 ** 3, 'TB': 1024 ** 4,
        'KIB': 1024, 'MIB': 1024 ** 2, 'GIB': 1024 ** 3, 'TIB': 1024 ** 4,
        'KBD': 1e3, 'MBD': 1e6, 'GBD': 1e9, 'TBD': 1e12}
BIT = {'b': 1 / 8, 'bit': 1 / 8, 'kb': 1e3 / 8, 'Kb': 1e3 / 8, 'Mb': 1e6 / 8, 'Gb': 1e9 / 8, 'Tb': 1e12 / 8}
TIME = {'NS': 1e-9, 'US': 1e-6, 'µS': 1e-6, 'MS': 1e-3, 'S': 1, 'SEC': 1, 'SECONDS': 1, 'MIN': 60, 'MINUTES': 60, 'H': 3600, 'HOURS': 3600}
FREQ = {'HZ': 1, 'KHZ': 1e3, 'MHZ': 1e6, 'GHZ': 1e9}
SRC_STATS = 'vsphere/tools/vsphere-client/vcenter-statistics'


class CalcError(ValueError):
    pass


def _unit(u):
    """Return (kind, factor to base, is_rate, warning). Bits vs bytes is decided by letter case: b = bit, B = byte."""
    raw = u.strip()
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
            'used_pct': self.used_pct, 'min': min, 'max': max, 'abs': abs, 'round': round, 'sum': sum,
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
