"""Question 0385: host memory Usage high (about 95%) without balloon.

1. vCenter Past week style (30-minute points, generated directly) for host
   esx-p14.example.com (512 GB): Usage, Ballooned memory, Consumed, Active.
2. VCF Operations list of the 18 VMs (ASSUMED list format, README): Contention,
   Balloon, Swap In Rate all 0, Consumed (Max) per VM. Group prefix `Memory|`.
"""

import datetime as dt
import math

from .. import core, formats

HOST = "esx-p14.example.com"
TOTAL = 536_870_912
Z = dt.timezone.utc
N = 336
START = dt.datetime(2026, 11, 3, 0, 0, 0, tzinfo=Z)
VC_COLS = [f"{m} for {HOST}" for m in ("Usage", "Ballooned memory", "Consumed", "Active")]
LIST_COLS = ["Memory|Contention (%) (Max)", "Memory|Balloon (%) (Max)",
             "Memory|Swap In Rate (KBps) (Max)", "Memory|Consumed (KB) (Max)"]
VMS = ([("crm-db-01", 96), ("crm-db-02", 96)] + [(f"crm-app-0{i}", 32) for i in range(1, 5)]
       + [(f"crm-web-0{i}", 16) for i in range(1, 5)] + [("bi-etl-01", 48), ("bi-etl-02", 48),
          ("bi-rpt-01", 24), ("file-01", 16), ("print-01", 8), ("mon-01", 16), ("dc-03", 8), ("jump-02", 8)])
F1 = "vcenter-host-memory-past-week.csv"
F2 = "vcf-operations-host-vms-memory-7-days.csv"
GB_KB = 1_048_576


@core.register
class HostMemoryUsageHigh(core.Case):
    question_id = "0385"
    seed = 385

    def generate(self, seed=None):
        rng = core.make_rng(self.seed if seed is None else seed, "host-mem")
        rows, cons_all = [], []
        for i, t in enumerate(core.time_axis(START, N, 1800)):
            h = i / 2
            c = core.clamp(95.5 + 1.0 * math.sin(2 * math.pi * (h - 6) / 24) + rng.gauss(0, 0.15), 94.2, 96.8)
            cons = round(c * TOTAL / 100)
            a = core.clamp(22 + 8 * math.sin(2 * math.pi * (h - 8) / 24) + rng.gauss(0, 1.5), 12, 34)
            rows.append((t, [round(100 * cons / TOTAL, 2), 0, cons, round(TOTAL * a / 100)]))
            cons_all.append(cons)
        w = [(n, g * GB_KB * rng.uniform(0.80, 0.99), g * GB_KB) for n, g in VMS]
        f = 0.93 * (sum(cons_all) / N) / sum(x[1] for x in w)
        lst = [(n, [0, 0, 0, round(x * f)]) for n, x, _ in w]
        return {F1: formats.vcenter_csv(VC_COLS, rows), F2: formats.vcf_list_csv(LIST_COLS, lst)}

    def check(self, files):
        fails = []
        try:
            cols, rows = formats.parse_vcenter_csv(files[F1])
            lc, lrows = formats.parse_vcf_list_csv(files[F2])
        except (KeyError, ValueError, IndexError) as e:
            return [f"parse: {e}"]
        if cols != VC_COLS or lc != LIST_COLS:
            return ["columns differ"]
        if len(rows) != N or len(lrows) != 18:
            return [f"row counts {len(rows)}, {len(lrows)}"]
        if rows[0][0] != START or {(b[0] - a[0]).total_seconds() for a, b in zip(rows, rows[1:])} != {1800.0}:
            fails.append("axis is not 30 min from 2026-11-03T00:00Z")
        for t, (u, bal, c, a) in rows:
            if abs(u - 100 * c / TOTAL) > 0.006:
                fails.append(f"{t}: Usage != Consumed / total")
            if not a < c:
                fails.append(f"{t}: Active not below Consumed")
            if bal != 0:
                fails.append(f"{t}: Ballooned memory {bal}")
            if not 94.0 <= u <= 97.0:
                fails.append(f"{t}: Usage {u} outside 94..97")
        for n, v in lrows:
            if v[0] != 0 or v[1] != 0 or v[2] != 0:
                fails.append(f"{n}: contention, balloon or swap in not 0")
        cfg = dict(VMS)
        for n, v in lrows:
            if v[3] > cfg[n] * GB_KB:
                fails.append(f"{n}: Consumed above configured")
        s = sum(v[3] for _, v in lrows)
        cons = [r[1][2] for r in rows]
        if s > max(cons) or s < 0.85 * sum(cons) / N:
            fails.append("VM Consumed sum outside host Consumed relation")
        return fails[:20]
