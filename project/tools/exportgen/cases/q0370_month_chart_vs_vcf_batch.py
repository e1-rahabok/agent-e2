"""Question 0370: vCenter Past month chart against a VCF Operations batch window.

rpt-db-02 (16 vCPUs). vCenter Past month, 2-hour points (360 rows, stamped at
the start of the window): the row 2026-11-10T14:00Z is the mean of 24
five-minute VCF Operations Usage values, a 20-minute batch (4 points at
82-97%) inside a quiet baseline (22-38%). Five VCF Operations chart CSVs
(Usage, Contention, Ready, Co-stop, Overlap) cover that window with 24 points
stamped at the end of their cycle (22:05 to 00:00 GMT+08:00).

Relations: Contention = Overlap + Co-stop + Ready + Other Wait (hidden, below
1) at every point; the vCenter row = mean of the 24 Usage values (2 decimals);
the batch row is the month's highest.
"""

import datetime as dt
import math

from .. import core, formats, relations as rel

VM = "rpt-db-02"
UTC = core.UTC
MONTH_START = dt.datetime(2026, 10, 17, 2, 0, tzinfo=UTC)
MONTH_ROWS = 360
BATCH_ROW = dt.datetime(2026, 11, 10, 14, 0, tzinfo=UTC)
VCF_START = dt.datetime(2026, 11, 10, 14, 5, tzinfo=UTC)     # 22:05 GMT+08:00
N = 24
BATCH_IDX = range(8, 12)
FM = "rpt-db-02-cpu-usage-last-month.csv"
VCF = {
    "usage": ("rpt-db-02-vcf-cpu-usage.csv", "CPU|Usage (%)"),
    "contention": ("rpt-db-02-vcf-cpu-contention.csv", "CPU|Contention (%)"),
    "ready": ("rpt-db-02-vcf-cpu-ready.csv", "CPU|Ready (%)"),
    "costop": ("rpt-db-02-vcf-cpu-co-stop.csv", "CPU|Co-stop (%)"),
    "overlap": ("rpt-db-02-vcf-cpu-overlap.csv", "CPU|Overlap (%)"),
}


def _series(seed):
    """The 24-point series of every metric (full precision) and the vCenter month rows."""
    for attempt in range(200):
        rng = core.make_rng(seed, f"vcf{attempt}")
        walk = core.bounded_walk(rng, N, 30, 1.5, 24, 36)
        b = set(BATCH_IDX)
        usage = [rng.uniform(82, 97) if i in b else walk[i] + rng.uniform(-1.5, 1.5) for i in range(N)]
        usage = [u if i in b else core.clamp(u, 22, 38) for i, u in enumerate(usage)]
        ready = [rng.uniform(1.0, 2.2) if i in b else rng.uniform(0.15, 0.6) for i in range(N)]
        costop = [rng.uniform(2.4, 4.0) if i in b else rng.uniform(0.03, 0.3) for i in range(N)]
        overlap = [rng.uniform(0.10, 0.35) if i in b else rng.uniform(0.01, 0.08) for i in range(N)]
        other = [rng.uniform(0.05, 0.3) if i in b else rng.uniform(0.02, 0.4) for i in range(N)]
        cont = [overlap[i] + costop[i] + ready[i] + other[i] for i in range(N)]
        batch_value = round(rel.rollup_mean(usage), 2)
        if min(usage[i] for i in b) - batch_value >= 42:
            break
    else:
        raise RuntimeError("no series with a 42-point gap")
    rng = core.make_rng(seed, "month")
    times = core.time_axis(MONTH_START, MONTH_ROWS, 7200)
    rows = []
    for t in times:
        if t == BATCH_ROW:
            rows.append((t, [batch_value]))
            continue
        lh = (t.hour + 8) % 24
        v = 23 + 7 * math.cos(2 * math.pi * (lh - 2) / 24) + rng.gauss(0, 2.5)
        rows.append((t, [round(core.clamp(v, 12, 34), 2)]))
    series = {"usage": usage, "contention": cont, "ready": ready, "costop": costop, "overlap": overlap}
    return series, rows


@core.register
class Q0370(core.Case):
    question_id = "0370"
    seed = 370

    def generate(self, seed=None):
        seed = self.seed if seed is None else seed
        series, rows = _series(seed)
        times = core.time_axis(VCF_START, N, 300)
        files = {FM: formats.vcenter_csv([f"Usage for {VM}"], rows)}
        for key, (fname, label) in VCF.items():
            files[fname] = formats.vcf_chart_csv(f"{VM} - {label}", list(zip(times, series[key])), tz_hours=8)
        return files

    def check(self, files):
        fails = []
        try:
            cols, mrows = formats.parse_vcenter_csv(files[FM])
            parsed = {k: formats.parse_vcf_chart_csv(files[f]) for k, (f, _) in VCF.items()}
        except (KeyError, ValueError, IndexError) as e:
            return [f"parse: {e}"]
        if cols != [f"Usage for {VM}"] or len(mrows) != MONTH_ROWS:
            return ["vCenter file: columns or row count differ"]      # D: vCenter export holds Usage only, no Contention
        for i, (t, _) in enumerate(mrows):
            if t != MONTH_START + dt.timedelta(seconds=7200 * i):
                fails.append(f"vCenter row {i}: step is not 7,200 s")
                break
        for k, (fname, label) in VCF.items():
            title, pts = parsed[k]
            if title != f"{VM} - {label}":
                fails.append(f"{fname}: title {title!r}")
            if len(pts) != N:
                fails.append(f"{fname}: {len(pts)} rows, expected {N}")
                return fails
            if [t for t, _ in pts] != [t for t, _ in parsed["usage"][1]]:
                fails.append(f"{fname}: stamps differ from the Usage file")
        times = [t for t, _ in parsed["usage"][1]]
        if times[0] != VCF_START or any((b - a).total_seconds() != 300 for a, b in zip(times, times[1:])):
            fails.append("VCF stamps are not 5 minutes apart from 22:05 GMT+08:00")
        if formats.vcf_time(times[0]).split(" GMT")[0] != "November 10, 2026, 10:05:00 PM":
            fails.append("first VCF stamp differs from November 10, 2026, 10:05:00 PM")
        usage = [v for _, v in parsed["usage"][1]]
        ready = [v for _, v in parsed["ready"][1]]
        costop = [v for _, v in parsed["costop"][1]]
        overlap = [v for _, v in parsed["overlap"][1]]
        cont = [v for _, v in parsed["contention"][1]]
        for i in range(N):
            hidden = cont[i] - overlap[i] - costop[i] - ready[i]
            if not -1e-9 <= hidden < 1:
                fails.append(f"point {i}: Contention - Overlap - Co-stop - Ready = {hidden} (outside [0, 1))")
        row = dict(mrows)[BATCH_ROW][0]
        mean = rel.rollup_mean(usage)
        if abs(row - mean) > 0.006:                                              # A true, C false (same mean, same counter)
            fails.append(f"A: vCenter row {row} vs mean of the 24 Usage values {mean:.4f}")
        idx = [i for i, u in enumerate(usage) if 80 <= u <= 100]
        if len(idx) != 4 or idx != list(range(idx[0], idx[0] + 4)):
            return fails + ["A: not exactly 4 consecutive Usage values in 80-100"]
        if sum(1 for u in usage if 20 <= u <= 40) != 20:
            fails.append("A: the other 20 Usage values are not all in 20-40")
        if not row < min(usage[i] for i in idx) or not row < max(usage):      # vCenter row below the batch
            fails.append("the vCenter row is not below the batch values")
        for i in idx:
            if not cont[i] - ready[i] >= 2.0:                                  # E false: Contention is not Ready
                fails.append(f"E: point {i}: Contention - Ready = {cont[i] - ready[i]:.3f} below 2.0")
            if not costop[i] >= 0.67 * (cont[i] - ready[i]):                   # F true: Co-stop is most of the gap
                fails.append(f"F: point {i}: Co-stop below 0.67 x (Contention - Ready)")
            if not usage[i] - row >= 40:                                       # the batch is far above the vCenter row
                fails.append(f"point {i}: Usage exceeds the vCenter row by less than 40")
        if max(v[0] for t, v in mrows if t != BATCH_ROW) >= row:
            fails.append("the batch row is not the month's highest")
        if any(not 12 <= v[0] <= 34 for t, v in mrows if t != BATCH_ROW):
            fails.append("a month row is outside 12-34")
        return fails[:20]
