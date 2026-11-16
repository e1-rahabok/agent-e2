"""Question 0423: one of eight virtual disks reads at 16 ms for an hour while the
VM-level latency stays under 3 ms.

rpt-db-12, VCF Operations: two chart exports (36 points of 5 minutes, 01:05 to
04:00 GMT+08:00) and a list view over 02:05-03:00 (12 points). The aggregate is
the IOPS-weighted mean of the eight disks; scsi1:2 is slow and light (about 6%
of the IOPS). The peak chart is driven by scsi1:2 inside the window.
Labels are assumed (see the spec); the list format is the assumed one.
"""

import datetime as dt

from .. import core, formats, relations as rel

VM = "rpt-db-12"
N = 36
STEP_S = 300
START = dt.datetime(2026, 11, 13, 17, 5, 0, tzinfo=core.UTC)     # 01:05 GMT+08:00 on 2026-11-14
WIN = range(12, 24)                                               # 02:05 .. 03:00
SLOW = "scsi1:2"
DISKS = ["scsi0:0", "scsi0:1", "scsi0:2", "scsi0:3", "scsi1:0", "scsi1:1", "scsi1:2", "scsi1:3"]
AGG = "Aggregate of all instances"
F_LAT = "vcf-operations-vm-disk-read-latency.csv"
F_PEAK = "vcf-operations-vm-peak-latency.csv"
F_LIST = "vcf-operations-vm-virtual-disks-0200-0300.csv"
T_LAT = f"{VM} - Virtual Disk:{AGG}|Read Latency (ms)"
T_PEAK = f"{VM} - Virtual Disk|Peak Latency within collection cycle (ms)"
LIST_COLS = [f"Virtual Disk:{x}|{m}" for x in [AGG] + DISKS
             for m in ("Read Latency (ms)", "Read Latency (ms) (Min)", "Read Latency (ms) (Max)", "Read IOPS")]


@core.register
class Q0423(core.Case):
    question_id = "0423"
    seed = 423

    def generate(self, seed=None):
        seed = self.seed if seed is None else seed
        rng = core.make_rng(seed, "disks")
        iops, lat = {}, {}
        for d in DISKS:
            if d == SLOW:
                iops[d] = [rng.uniform(150, 250) if i in WIN else rng.uniform(0.5, 5) for i in range(N)]
                lat[d] = [rng.uniform(15.2, 16.8) if i in WIN else rng.uniform(0.5, 1.0) for i in range(N)]
            else:
                iops[d] = core.bounded_walk(rng, N, rng.uniform(420, 480), 20, 380, 520)
                lat[d] = [rng.uniform(0.5, 1.0) for _ in range(N)]
        agg_iops = [sum(iops[d][i] for d in DISKS) for i in range(N)]
        agg_lat = [rel.iops_weighted_mean([lat[d][i] for d in DISKS], [iops[d][i] for d in DISKS]) for i in range(N)]
        peak = [max([lat[d][i] * rng.uniform(1.2, 2.0) for d in DISKS] + [rng.uniform(1, 4) for _ in DISKS])
                for i in range(N)]
        times = core.time_axis(START, N, STEP_S)
        lat_rows = [(t, round(v, 3)) for t, v in zip(times, agg_lat)]
        peak_rows = [(t, round(v, 3)) for t, v in zip(times, peak)]
        vals = []
        for x in [AGG] + DISKS:
            L = agg_lat if x == AGG else lat[x]
            I = agg_iops if x == AGG else iops[x]
            w = [L[i] for i in WIN]
            vals += [sum(w) / 12, min(w), max(w), sum(I[i] for i in WIN) / 12]
        return {F_LAT: formats.vcf_chart_csv(T_LAT, lat_rows, 8), F_PEAK: formats.vcf_chart_csv(T_PEAK, peak_rows, 8),
                F_LIST: formats.vcf_list_csv(LIST_COLS, [(VM, vals)])}

    def check(self, files):
        fails = []
        try:
            t1, lat = formats.parse_vcf_chart_csv(files[F_LAT])
            t2, peak = formats.parse_vcf_chart_csv(files[F_PEAK])
            cols, lrows = formats.parse_vcf_list_csv(files[F_LIST])
        except (KeyError, ValueError) as e:
            return [str(e)]
        if (t1, t2) != (T_LAT, T_PEAK) or cols != LIST_COLS or [n for n, _ in lrows] != [VM]:
            return ["titles, list columns or the list row name differ"]
        stamps = [t for t, _ in lat]
        if len(lat) != N or stamps != [t for t, _ in peak] or any((b - a).total_seconds() != STEP_S for a, b in zip(stamps, stamps[1:])):
            return ["charts: rows, stamps or step differ"]
        v = dict(zip(cols, lrows[0][1]))
        g = lambda x, m: v[f"Virtual Disk:{x}|{m}"]
        for x in [AGG] + DISKS:
            if not g(x, "Read Latency (ms) (Min)") <= g(x, "Read Latency (ms)") <= g(x, "Read Latency (ms) (Max)"):
                fails.append(f"{x}: Min <= average <= Max broken")
        s = sum(g(d, "Read IOPS") for d in DISKS)
        if abs(g(AGG, "Read IOPS") - s) > 0.01 * s:
            fails.append("aggregate Read IOPS != sum of the eight disks")
        win = [lat[i][1] for i in WIN]
        if abs(g(AGG, "Read Latency (ms)") - sum(win) / 12) > 0.02 * sum(win) / 12:
            fails.append("aggregate list latency not within 2% of the chart's window mean")
        if g(SLOW, "Read Latency (ms) (Min)") < 15:                  # A
            fails.append("A: scsi1:2 Min below 15")
        if g(AGG, "Read Latency (ms) (Max)") > 3 or max(x for _, x in lat) > 3:
            fails.append("A: aggregate above 3 ms")
        avgs = [g(d, "Read Latency (ms)") for d in DISKS]
        if sum(avgs) / 8 > 3 or sum(a > 3 for a in avgs) != 1:
            fails.append("A: unweighted mean above 3 or not exactly one disk above 3 ms")
        for i, ((_, p), (_, a)) in enumerate(zip(peak, lat)):
            if p < a:
                fails.append(f"point {i + 1}: peak below aggregate")
            if (i in WIN and p < 15) or (i not in WIN and p >= 10):
                fails.append(f"point {i + 1}: C/D peak {p} outside the window rule")
        if g(SLOW, "Read IOPS") >= 0.10 * g(AGG, "Read IOPS") or g(SLOW, "Read IOPS") >= 0.10 * s:
            fails.append("H: scsi1:2 carries 10% or more of the IOPS")
        for d in DISKS:
            if d != SLOW and g(d, "Read Latency (ms) (Max)") > 1.2:
                fails.append(f"B/E: {d} Max above 1.2")
        return fails[:20]
