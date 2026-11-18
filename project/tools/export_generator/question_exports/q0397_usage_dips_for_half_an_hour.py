"""Question 0397: VM memory Usage dips while Guest Needed Memory has a gap.

fs-print-02 (16 GB), six VCF Operations chart downloads, 24 five-minute rows
from 10:00 GMT+08:00. Guest Needed Memory is blank in rows 9-14 (10:45-11:10
local, 30 minutes). Usage then falls back to non-zero active over total; the
guest keeps a large cache so Consumed stays near 15.4 GB. Metric labels other
than CPU|Ready (%) follow the Group|Label (unit) form (assumed).
"""

from .. import export_framework, export_formats

VM = "fs-print-02"
T = 16_777_216
N = 24
STEP_S = 300
START = export_framework.DEFAULT_START.replace(year=2026, month=11, day=14, hour=2, minute=0, second=38)
GAP = range(9, 15)
FILES = {
    "usage": ("vcf-operations-memory-usage.csv", "Memory|Usage (%)"),
    "needed": ("vcf-operations-guest-needed-memory.csv", "Guest|Needed Memory (KB)"),
    "active": ("vcf-operations-memory-non-zero-active.csv", "Memory|Non Zero Active (KB)"),
    "util": ("vcf-operations-memory-utilization.csv", "Memory|Utilization (KB)"),
    "cons": ("vcf-operations-memory-consumed.csv", "Memory|Consumed (KB)"),
    "total": ("vcf-operations-memory-total-capacity.csv", "Memory|Total Capacity (KB)"),
}
TITLE = {k: f"{VM} - {v[1]}" for k, v in FILES.items()}


@export_framework.register
class Q0397(export_framework.QuestionExport):
    question_id = "0397"
    seed = 397

    def generate(self, seed=None):
        seed = self.seed if seed is None else seed
        rng = export_framework.make_rng(seed, "dip")
        gb = 1024 * 1024
        act = export_framework.bounded_walk(rng, N, 1.7 * gb, 0.08 * gb, 1.45 * gb, 1.95 * gb)
        need = export_framework.bounded_walk(rng, N, 12.3 * gb, 0.12 * gb, 12.0 * gb, 12.6 * gb)
        times = export_framework.time_axis(START, N, STEP_S)
        s = {k: [] for k in FILES}
        for i in range(N):
            cons = 15.4 * gb * (1 + rng.uniform(-0.01, 0.01))
            if i in GAP:
                n = None
                use = act[i] / T * 100 + rng.uniform(-0.4, 0.4)
                util = cons * (1 + rng.uniform(-0.015, 0.015))
            else:
                n = need[i]
                use = n / T * 100 + rng.uniform(-0.4, 0.4)
                util = (n + 358_400) * (1 + rng.uniform(-0.005, 0.005))
                util = max(util, n)
            s["usage"].append(use)
            s["needed"].append(n)
            s["active"].append(act[i])
            s["util"].append(util)
            s["cons"].append(cons)
            s["total"].append(T)
        return {FILES[k][0]: export_formats.vcf_chart_csv(TITLE[k], list(zip(times, s[k]))) for k in FILES}

    def check(self, files):
        fails, d = [], {}
        for k, (name, _) in FILES.items():
            try:
                title, rows = export_formats.parse_vcf_chart_csv(files[name])
            except (KeyError, ValueError) as e:
                return [f"{name}: {e}"]
            if title != TITLE[k] or len(rows) != N:
                fails.append(f"{name}: title or row count differs")
                continue
            if [r[0] for r in rows] != export_framework.time_axis(START, N, STEP_S):
                fails.append(f"{name}: time stamps differ")
            d[k] = [r[1] for r in rows]
        if fails:
            return fails
        u, nd, a, z, c, t = (d[k] for k in ("usage", "needed", "active", "util", "cons", "total"))
        if [i for i, v in enumerate(nd) if v is None] != list(GAP):       # A
            fails.append("A: Guest Needed Memory not blank exactly in rows 9..14")
        if sorted(range(N), key=lambda i: u[i])[:6] != sorted(GAP, key=lambda i: u[i]):
            fails.append("A: the gap rows are not the six lowest Usage values")
        if any(v != T for v in t):
            fails.append("Total Capacity not constant")
        mean0 = sum(u[:9]) / 9
        for i in range(N):
            if not a[i] < c[i] <= T:
                fails.append(f"row {i}: relation A < Consumed <= Total broken")
            if i in GAP:
                if abs(u[i] - a[i] / T * 100) > 2:                        # B
                    fails.append(f"row {i}: Usage not within 2 points of active / total")
                if u[i] > mean0 - 20:
                    fails.append(f"row {i}: Usage not 20 points below the early mean")
                if abs(z[i] - c[i]) / c[i] > 0.05:                        # C
                    fails.append(f"row {i}: Utilization not within 5% of Consumed")
            else:
                if abs(u[i] - nd[i] / T * 100) > 2 or z[i] < nd[i]:
                    fails.append(f"row {i}: Usage or Utilization does not follow Needed")
                if abs(u[i] - a[i] / T * 100) < 40:                       # F
                    fails.append(f"row {i}: Usage within 40 points of active / total")
        if min(z[i] for i in GAP) <= max(z[:9]):
            fails.append("C: Utilization in the gap not above rows 0..8")
        if max(c) / min(c) > 1.05:                                        # D
            fails.append("D: Consumed varies more than 5%")
        return fails[:20]
