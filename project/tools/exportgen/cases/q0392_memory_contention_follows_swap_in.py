"""Question 0392: Memory Contention follows Swap In Rate, not Balloon.

rpt-svc-04, VCF Operations list view with a 15-minute time breakdown (assumed
format), 96 rows on 2026-11-14 local (GMT+08:00). Swap in happens in nine rows;
Contention is above 0 exactly there. Balloon sits at 12-26% all day and does not
follow Contention. Swap out comes first in front of each swap-in interval.
"""

import math

from .. import core, formats

N = 96
STEP_S = 900
TZ = 8
START = core.DEFAULT_START.replace(year=2026, month=11, day=13, hour=16, minute=0)  # 00:00 GMT+08:00
FILE = "vcf-operations-vm-memory-15min.csv"
COLS = ["Memory|Contention (%)", "Memory|Balloon (%)", "Memory|Swap In Rate (KBps)", "Memory|Swap Out Rate (KBps)"]
SWAP_IN = [(38, 39, 40), (58, 59, 60, 61), (75, 76)]
PEAK = {38: 39, 58: 60, 75: 75}
SWAP_OUT = [(35, 36, 37, 38), (56, 57, 58), (73, 74, 75)]


def _balloon(rng):
    out = []
    walk = core.bounded_walk(rng, N, 24.0, 0.45, 22.0, 26.0)
    for i in range(N):
        if i < 28:
            out.append(12.0 + rng.uniform(-0.3, 0.3))
        elif i < 35:
            out.append(core.blend(12.0, 22.0, (i - 27) / 7) + rng.uniform(-0.2, 0.2))
        elif i < 72:
            out.append(walk[i])
        else:
            w = min(1.0, (i - 71) / 9)
            out.append(core.blend(walk[71], 15.0, w) + (rng.uniform(-0.5, 0.5) if w == 1 else rng.uniform(-0.2, 0.2)))
    return out


def _pearson(a, b):
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    den = math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))
    return num / den if den else 0.0


def _runs(flags):
    runs, prev = 0, False
    for f in flags:
        runs += f and not prev
        prev = f
    return runs


@core.register
class Q0392(core.Case):
    question_id = "0392"
    seed = 392

    def generate(self, seed=None):
        seed = self.seed if seed is None else seed
        rng = core.make_rng(seed, "contention")
        w_rows = {i for g in SWAP_IN for i in g}
        out_rows = {i for g in SWAP_OUT for i in g}
        sin = {}
        for g in SWAP_IN:
            for i in g:
                sin[i] = round(rng.uniform(3_600, 6_200)) if i == PEAK[g[0]] else round(rng.uniform(350, 3_400))
        bal = _balloon(rng)
        rows = []
        for i, t in enumerate(core.time_axis(START, N, STEP_S)):
            si = sin.get(i, 0)
            so = round(rng.uniform(900, 4_800)) if i in out_rows else 0
            con = core.clamp(0.6 + 0.00045 * si + rng.uniform(0, 0.4), 0.6, 3.8) if i in w_rows else 0
            rows.append((formats.vcf_time(t, TZ), [round(con, 4) if con else 0, round(bal[i], 2), si, so]))
        return {FILE: formats.vcf_list_csv(COLS, rows, name_header="Time")}

    def check(self, files):
        try:
            cols, rows = formats.parse_vcf_list_csv(files[FILE])
        except (KeyError, ValueError) as e:
            return [f"{FILE}: {e}"]
        if cols != COLS:
            return [f"columns differ: {cols}"]
        fails = []
        if len(rows) != N:
            return [f"{len(rows)} rows, expected {N}"]
        times = [formats.parse_vcf_time(r[0]) for r in rows]
        if times[0] != START or any((b - a).total_seconds() != STEP_S for a, b in zip(times, times[1:])):
            fails.append("time stamps are not 96 x 15 minutes from 00:00 GMT+08:00")
        con, bal, si, so = ([r[1][k] for r in rows] for k in range(4))
        for i in range(N):
            if (con[i] > 0) != (si[i] > 0):
                fails.append(f"row {i}: Contention > 0 differs from Swap In Rate > 0")
            if min(con[i], bal[i], si[i], so[i]) < 0 or bal[i] > 65:
                fails.append(f"row {i}: negative value or Balloon above 65")
        if _runs([c > 0.5 for c in con]) < 2:                     # A
            fails.append("A: fewer than two separate runs with Contention above 0.5")
        if sum(c > 0 for c in con) >= 24 or sum(s > 0 for s in si) >= 24:  # C
            fails.append("C: Contention or Swap In in a quarter of the rows or more")
        if sum(b >= 10 for b in bal) < 80 or sum(b >= 10 and c == 0 for b, c in zip(bal, con)) < 60:  # D
            fails.append("D: Balloon not at 10 or more outside Contention in enough rows")
        if _pearson(bal, con) >= 0.5:
            fails.append("D: Balloon correlates with Contention")
        if sum(s > 0 and c == 0 for s, c in zip(so, con)) < 4:
            fails.append("neighbour: fewer than 4 rows with Swap Out and no Contention")
        for i in range(N):
            if con[i] > 0:
                for j in (i - 1, i + 1):
                    if 0 <= j < N and con[j] == 0 and abs(bal[j] - bal[i]) >= 2:
                        fails.append(f"row {j}: Balloon differs from the Contention row {i} by 2 or more")
        return fails[:20]
