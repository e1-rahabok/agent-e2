"""Question 0414: Command latency of a LUN that hides slow writes.

esx-db-02, host Disk view of one LUN, Real-time 90 rows. Reads about 1,500/s,
writes 1/8 of reads; read latency prints 3 ms, write latency 13-17 ms. Command
latency is the request-weighted mean of the printed values, rounded; the
Physical device and Kernel columns split it (Kernel 0, 1 in at most 10% of rows).
"""

from .. import core, formats, relations as rel

N = 90
STEP_S = 20
START = core.DEFAULT_START.replace(year=2026, month=11, day=12, hour=14, minute=0)
FILE = "vcenter-host-disk-lun-realtime.csv"
DEV = "Fibre Channel Disk (naa.6000d31000a4b5000000000000000117)"
NAMES = ["Read latency", "Write latency", "Command latency", "Physical device command latency",
         "Kernel command latency", "Average read requests per second", "Average write requests per second"]
COLS = [f"{n} for {DEV}" for n in NAMES]


@core.register
class Q0414(core.Case):
    question_id = "0414"
    seed = 414

    def generate(self, seed=None):
        seed = self.seed if seed is None else seed
        rng = core.make_rng(seed, "lun")
        walk = core.bounded_walk(rng, N, 1500, 45, 1250, 1750)
        times = core.time_axis(START, N, STEP_S)
        rows = []
        for i, t in enumerate(times):
            reads = round(walk[i] * (1 + rng.uniform(-0.03, 0.03)))
            writes = round(reads / rng.uniform(7.0, 9.0))
            rd = round(rng.uniform(2.8, 3.2))
            wr = round(rng.uniform(13.0, 17.0))
            cmd = round(rel.weighted_latency(rd, reads, wr, writes))
            kern = 1 if rng.random() < 0.08 else 0
            rows.append((t, [rd, wr, cmd, cmd - kern, kern, reads, writes]))
        return {FILE: formats.vcenter_csv(COLS, rows)}

    def check(self, files):
        try:
            cols, rows = formats.parse_vcenter_csv(files[FILE])
        except (KeyError, ValueError) as e:
            return [f"{FILE}: {e}"]
        if cols != COLS:
            return [f"columns differ: {cols}"]
        fails = []
        if len(rows) != N:
            fails.append(f"{len(rows)} rows")
        if any((b[0] - a[0]).total_seconds() != STEP_S for a, b in zip(rows, rows[1:])):
            fails.append("time step is not 20 s")
        c = {n: formats.column(cols, rows, f"{n} for {DEV}") for n in NAMES}
        rd, wr, cmd, phy, ker, rq, wq = (c[n] for n in NAMES)
        for i in range(N):
            k = f"row {i + 1}"
            if abs(cmd[i] - rel.weighted_latency(rd[i], rq[i], wr[i], wq[i])) > 0.5:
                fails.append(f"{k}: G true: Command latency not the weighted mean")
            if cmd[i] != phy[i] + ker[i]:
                fails.append(f"{k}: Command != Physical + Kernel")
            if not 6 <= rq[i] / wq[i] <= 10:
                fails.append(f"{k}: A: reads / writes {rq[i] / wq[i]:.1f}")
            self._keys(fails, k, rd[i], wr[i], cmd[i])
        if sum(x > 0 for x in ker) > 0.10 * N:
            fails.append("H false: Kernel latency above 0 in more than 10% of rows")
        m = lambda v: sum(v) / len(v)
        self._keys(fails, "means", m(rd), m(wr), m(cmd))
        return fails[:20]

    @staticmethod
    def _keys(fails, k, r, w, cm):
        if not 1.2 <= cm / r <= 1.8:
            fails.append(f"{k}: A true: Command / Read {cm / r:.2f}")
        if not cm < 0.9 * (r + w) / 2:
            fails.append(f"{k}: B false: Command not below 0.9 x plain mean")
        if not 4 <= w / r <= 6 or not cm < w / 2:
            fails.append(f"{k}: C true, D false: Write / Read or Command < Write / 2")
        if not cm > r:
            fails.append(f"{k}: E false: Command not above Read")
        if not (cm - r) < (w - cm) or cm - r > 2 or w - cm < 8:
            fails.append(f"{k}: A, D: Command not near Read: Command - Read, Write - Command")
