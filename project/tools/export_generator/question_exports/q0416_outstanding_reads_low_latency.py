"""Question 0416: many outstanding reads at a sub-millisecond read latency.

db-sql-09, scsi0:1 on NVMe, Real-time 30 rows. Reads 26,000-30,000/s at
650-850 us: Little's law gives 16-26 outstanding. No millisecond latency column
(it would print 0 or 1 and break the arithmetic).
"""

from .. import export_framework, export_formats, counter_relations as rel

N = 30
STEP_S = 20
START = export_framework.DEFAULT_START.replace(year=2026, month=11, day=13, hour=9, minute=30)
FILE = "vcenter-vm-virtual-disk-realtime.csv"
D = "scsi0:1"
NAMES = ["Average read requests per second", "Average write requests per second", "Read Latency (us)",
         "Write Latency (us)", "Average number of outstanding read requests",
         "Average number of outstanding write requests", "Read rate"]
COLS = [f"{n} for {D}" for n in NAMES]


@export_framework.register
class Q0416(export_framework.QuestionExport):
    question_id = "0416"
    seed = 416

    def generate(self, seed=None):
        seed = self.seed if seed is None else seed
        rng = export_framework.make_rng(seed, "disk")
        walk = export_framework.bounded_walk(rng, N, 28000, 600, 26000, 30000)
        times = export_framework.time_axis(START, N, STEP_S)
        rows = []
        for i, t in enumerate(times):
            reads = round(walk[i] * (1 + rng.uniform(-0.02, 0.02)))
            lat = rng.randint(650, 850)
            for _ in range(100):
                out = round(reads * lat / 1e6 * rng.uniform(0.93, 1.07))
                if out >= 16:
                    break
            writes = rng.randint(300, 600)
            wlat = rng.randint(400, 900)
            wout = round(writes * wlat / 1e6)
            rate = round(reads * 8 * rng.uniform(0.995, 1.005))
            rows.append((t, [reads, writes, lat, wlat, out, wout, rate]))
        return {FILE: export_formats.vcenter_csv(COLS, rows)}

    def check(self, files):
        try:
            cols, rows = export_formats.parse_vcenter_csv(files[FILE])
        except (KeyError, ValueError) as e:
            return [f"{FILE}: {e}"]
        if cols != COLS:
            return [f"columns differ: {cols}"]
        fails = []
        if len(rows) != N:
            fails.append(f"{len(rows)} rows")
        if any((b[0] - a[0]).total_seconds() != STEP_S for a, b in zip(rows, rows[1:])):
            fails.append("time step is not 20 s")
        c = {n: export_formats.column(cols, rows, f"{n} for {D}") for n in NAMES}
        rq, wq, rl, wl, ro, wo, rate = (c[n] for n in NAMES)
        for i in range(N):
            k = f"row {i + 1}"
            if abs(rel.outstanding_io(rq[i], rl[i] / 1000) - ro[i]) > 0.20 * ro[i]:
                fails.append(f"{k}: A reads x latency differs from outstanding reads by more than 20%")
            if not 7.9 <= rate[i] / rq[i] <= 8.1:
                fails.append(f"{k}: Read rate / reads {rate[i] / rq[i]:.2f}")
            if abs(wo[i] - wq[i] * wl[i] / 1e6) > 1:
                fails.append(f"{k}: outstanding writes off")
            if ro[i] < 16 or rl[i] >= 1000:
                fails.append(f"{k}: B/C/E outstanding {ro[i]} or latency {rl[i]} us")
            if not 200 <= rl[i] <= 1000:
                fails.append(f"{k}: I latency outside 200-1000 us")
        m = lambda v: sum(v) / len(v)
        if abs(rel.outstanding_io(m(rq), m(rl) / 1000) - m(ro)) > 0.20 * m(ro):
            fails.append("A: 30-row means off")
        return fails[:20]
