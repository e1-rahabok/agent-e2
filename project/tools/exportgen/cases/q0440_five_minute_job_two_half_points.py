"""Question 0440: a five-minute job shows as two half points on Past 2 hours.

VM rpt-batch-11, 4 vCPUs. One hidden 20-second Usage series S (360 samples,
01:03:00Z .. 03:02:40Z) drives both files.
1. vCenter Real-time CSV (90 rows, 01:55:20Z .. 02:25:00Z): Usage = S, plus
   Readiness per vCPU and the VM value (mean of the four).
2. VCF Operations chart CSV (24 five-minute cycles, 09:07:40 .. 11:02:40
   GMT+08:00): value at stamp t = mean of the 15 samples in (t-300 s, t].
The job runs 02:05:00Z .. 02:10:00Z, so it straddles the cycle border at
02:07:40Z: 8 busy samples fall in one cycle and 7 in the next.
"""

import datetime as dt

from .. import core, formats, relations as rel

VM = "rpt-batch-11"
VCPUS = 4
Z = dt.timezone.utc
S_START = dt.datetime(2026, 11, 13, 1, 3, 0, tzinfo=Z)
S_N = 360
F1_START = dt.datetime(2026, 11, 13, 1, 55, 20, tzinfo=Z)
F1_N = 90
VCF_START = dt.datetime(2026, 11, 13, 1, 7, 40, tzinfo=Z)
VCF_N = 24
BUSY_FIRST = dt.datetime(2026, 11, 13, 2, 5, 20, tzinfo=Z)
BUSY_LAST = dt.datetime(2026, 11, 13, 2, 10, 0, tzinfo=Z)
F1_COLS = [f"Usage for {VM}", f"Readiness for {VM}",
           "Readiness for 3", "Readiness for 2", "Readiness for 1", "Readiness for 0"]
TITLE = f"{VM} - CPU|Usage (%)"


def _busy(t):
    return BUSY_FIRST <= t <= BUSY_LAST


@core.register
class FiveMinuteJobTwoHalfPoints(core.Case):
    question_id = "0440"
    seed = 440
    f1 = "vcenter-vm-cpu-real-time.csv"
    f2 = "vcf-operations-vm-cpu-usage-2-hours.csv"

    def generate(self, seed=None):
        rng = core.make_rng(self.seed if seed is None else seed, "five-minute-job")
        times = core.time_axis(S_START, S_N, 20)
        s = [round(rng.uniform(96.5, 99.8) if _busy(t) else rng.uniform(1.2, 4.5), 2) for t in times]
        by_time = dict(zip(times, s))
        rows1 = []
        for t in core.time_axis(F1_START, F1_N, 20):
            busy = _busy(t)
            vc = [round(rng.uniform(0.3, 1.2) if busy else rng.uniform(0.01, 0.08), 2) for _ in range(VCPUS)]
            vm = round(rel.rollup_mean(vc), 2)
            rows1.append((t, [by_time[t], vm, vc[3], vc[2], vc[1], vc[0]]))
        rows2 = []
        for t in core.time_axis(VCF_START, VCF_N, 300):
            win = [by_time[t - dt.timedelta(seconds=20 * k)] for k in range(14, -1, -1)]
            rows2.append((t, rel.rollup_mean(win)))
        return {self.f1: formats.vcenter_csv(F1_COLS, rows1),
                self.f2: formats.vcf_chart_csv(TITLE, rows2, tz_hours=8)}

    def check(self, files):
        fails = []
        try:
            cols, r1 = formats.parse_vcenter_csv(files[self.f1])
            title, r2 = formats.parse_vcf_chart_csv(files[self.f2])
        except (KeyError, ValueError, IndexError) as e:
            return [f"parse: {e}"]
        if cols != F1_COLS or title != TITLE:
            return ["columns or title differ"]
        if len(r1) != F1_N or len(r2) != VCF_N:
            return [f"row counts {len(r1)}, {len(r2)}"]
        if {(b[0] - a[0]).total_seconds() for a, b in zip(r1, r1[1:])} != {20.0}:
            fails.append("file 1 step is not 20 s")
        if {(b[0] - a[0]).total_seconds() for a, b in zip(r2, r2[1:])} != {300.0}:
            fails.append("file 2 step is not 300 s")
        if r1[0][0] != F1_START or r2[0][0] != VCF_START:
            fails.append("start stamps differ")
        for t, v in r1:
            if abs(v[1] - sum(v[2:]) / 4) > 0.006:
                fails.append(f"{t}: VM Readiness != mean of vCPUs")
            if any(not 0 <= x <= 100 for x in v):
                fails.append(f"{t}: value outside 0..100")
        for t, v in r2:
            if abs(v * 1500 - round(v * 1500)) > 1e-6:
                fails.append(f"{t}: not a mean of 15 two-decimal values")
        usage = {t: v[0] for t, v in r1}
        # D: the covered cycles
        covered = 0
        for t, v in r2:
            win = [t - dt.timedelta(seconds=20 * k) for k in range(15)]
            if all(w in usage for w in win):
                covered += 1
                m = sum(usage[w] for w in win) / 15
                if abs(v - m) > 1e-6:
                    fails.append(f"D: VCF {t} {v} != mean of file 1 window {m}")
        if covered != 5:
            fails.append(f"D: {covered} covered cycles, expected 5")
        # A / F
        hi = [t for t, v in r1 if v[0] >= 90]
        if hi != core.time_axis(BUSY_FIRST, 15, 20):
            fails.append("F: busy rows are not 15 consecutive rows 02:05:20Z..02:10:00Z")
        if any(v[0] >= 10 for t, v in r1 if t not in hi):
            fails.append("F: an idle row is 10 or more")
        # B / C
        c1 = dt.datetime(2026, 11, 13, 2, 7, 40, tzinfo=Z)
        c2 = dt.datetime(2026, 11, 13, 2, 12, 40, tzinfo=Z)
        by = dict(r2)
        for c in (c1, c2):
            if not 40 <= by[c] <= 60:
                fails.append(f"B: VCF value at {c} is {by[c]}")
        for t, v in r2:
            if t not in (c1, c2) and v >= 10:
                fails.append(f"B: VCF {t} is {v}, not idle")
        n1 = sum(1 for t in hi if c1 - dt.timedelta(seconds=280) <= t <= c1)
        n2 = sum(1 for t in hi if c2 - dt.timedelta(seconds=280) <= t <= c2)
        if (n1, n2) != (8, 7) or not (6 <= n1 <= 9 and 6 <= n2 <= 9):
            fails.append(f"C: busy rows per cycle {n1}, {n2}")
        if any(v >= 70 for _, v in r2):
            fails.append("G: a VCF value is 70 or more")
        return fails[:20]
