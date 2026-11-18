"""Question 0432: a 2-minute burst in the Real-time export, averaged away in Past day.

hr-batch-02 (2 vCPUs), Real-time 90 rows and Past day 48 rows. The six burst
samples (02:01:20 to 02:03:00) sit inside the 02:00 five-minute point; every
Past day point inside the Real-time window is the mean of its 15 samples.
"""

import datetime as dt

from .. import export_framework, export_formats, counter_relations as rel

VM = "hr-batch-02"
RT, PD = "hr-batch-02-cpu-realtime.csv", "hr-batch-02-cpu-past-day.csv"
N_RT, N_PD = 90, 48
RT_START = dt.datetime(2026, 11, 15, 1, 45, 0, tzinfo=export_framework.UTC)
PD_START = dt.datetime(2026, 11, 14, 22, 30, 0, tzinfo=export_framework.UTC)
BURST_FIRST = 49          # index of 02:01:20
BURST_LEN = 6
RT_COLS = [f"Usage for {VM}", f"Readiness for {VM}", "Readiness for 1", "Readiness for 0"]
PD_COLS = [f"Usage for {VM}"]


@export_framework.register
class Q0432(export_framework.QuestionExport):
    question_id = "0432"
    seed = 432

    def generate(self, seed=None):
        seed = self.seed if seed is None else seed
        rng = export_framework.make_rng(seed, "cpu")
        times = export_framework.time_axis(RT_START, N_RT, 20)
        idle = export_framework.bounded_walk(rng, N_RT, 3.0, 0.6, 1.5, 6.0)
        rows, usage = [], []
        for i, t in enumerate(times):
            busy = BURST_FIRST <= i < BURST_FIRST + BURST_LEN
            u = round(rng.uniform(95.5, 99.8), 2) if busy else round(idle[i], 2)
            r0 = round(rng.uniform(0.4, 1.8) if busy else rng.uniform(0.02, 0.15), 2)
            r1 = round(rng.uniform(0.4, 1.8) if busy else rng.uniform(0.02, 0.15), 2)
            usage.append(u)
            rows.append((t, [u, round((r0 + r1) / 2, 2), r1, r0]))
        pd_times = export_framework.time_axis(PD_START, N_PD, 300)
        walk = export_framework.bounded_walk(rng, N_PD, 3.0, 0.6, 1.5, 6.0)
        stamps = export_framework.rollup_stamps(times, 15, label="start")
        means = {s: round(rel.rollup_mean(w), 2) for s, w in zip(stamps, rel.rollup_windows(usage, 15))}
        pd_rows = [(t, [means.get(t, round(walk[i], 2))]) for i, t in enumerate(pd_times)]
        return {RT: export_formats.vcenter_csv(RT_COLS, rows), PD: export_formats.vcenter_csv(PD_COLS, pd_rows)}

    def check(self, files):
        try:
            c1, r1 = export_formats.parse_vcenter_csv(files[RT])
            c2, r2 = export_formats.parse_vcenter_csv(files[PD])
        except (KeyError, ValueError) as e:
            return [str(e)]
        fails = []
        if c1 != RT_COLS or c2 != PD_COLS:
            return [f"columns differ: {c1} {c2}"]
        if len(r1) != N_RT or len(r2) != N_PD:
            fails.append(f"rows: {len(r1)} and {len(r2)}")
        if any((b[0] - a[0]).total_seconds() != 20 for a, b in zip(r1, r1[1:])):
            fails.append("Real-time step is not 20 s")
        if any((b[0] - a[0]).total_seconds() != 300 for a, b in zip(r2, r2[1:])):
            fails.append("Past day step is not 300 s")
        u = [r[1][0] for r in r1]
        vm, a, b = (export_formats.column(c1, r1, n) for n in (RT_COLS[1], "Readiness for 1", "Readiness for 0"))
        for i in range(len(r1)):
            if abs(vm[i] - (a[i] + b[i]) / 2) > 0.011:
                fails.append(f"row {i + 1}: Readiness != mean of the vCPUs")
            if u[i] > 100:
                fails.append(f"row {i + 1}: Usage above 100")
        runs, cur = [], 0
        for i, x in enumerate(u):
            if x >= 90:
                cur += 1
            else:
                if cur:
                    runs.append(cur)
                cur = 0
        if cur:
            runs.append(cur)
        if len(runs) != 1 or not 5 <= runs[0] <= 7:
            fails.append(f"C true: runs of Usage >= 90: {runs}")
        if any(10 <= x < 90 for x in u):
            fails.append("C: a Real-time row between 10 and 90")
        if max(max(vm), max(a), max(b)) >= 2.5:
            fails.append("C trap: a Readiness value reaches 2.5")
        pd = [r[1][0] for r in r2]
        if any(x > 100 for x in pd):
            fails.append("Past day Usage above 100")
        rt_at = {t: i for i, (t, _) in enumerate(r1)}
        holds = None
        for t, vals in r2:
            if t in rt_at and rt_at[t] + 15 <= len(u):
                m = rel.rollup_mean(u[rt_at[t]:rt_at[t] + 15])
                if abs(m - vals[0]) > 0.011:
                    fails.append(f"B true, E false: {t}: Past day point != mean of its 15 Real-time rows")
                if any(x >= 90 for x in u[rt_at[t]:rt_at[t] + 15]):
                    holds = vals[0]
        if holds is None or not 30 <= holds <= 50:
            fails.append(f"G: the Past day row that holds the burst is {holds}, not 30-50")
        if sum(x >= 10 for x in pd) != 1:
            fails.append("F false, G true: not exactly one Past day row at 10 or above")
        return fails[:20]
