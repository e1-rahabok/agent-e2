"""Question 0421: Peak Transmitted Packet Dropped (%) of one 5-minute cycle.

ledger-app-03, VCF Operations chart exports, 72 points of 5 minutes (06:00 to
11:55 GMT+08:00). One hidden model of 20-second transmit counts (15 per point)
feeds four files; one 20-second sample at 09:25 holds all the drops.
"""

import datetime as dt

from .. import core, formats

OBJ = "ledger-app-03"
N = 72
STEP_S = 300
TZ = 8
START = dt.datetime(2026, 11, 13, 22, 0, 0, tzinfo=core.UTC)   # 06:00 GMT+08:00 on 2026-11-14
KSTAR = 41                                                      # 0-based index = the 09:25 point
FILES = {
    "peak": ("ledger-app-03-peak-tx-dropped-pct.csv", "Network|Peak Transmitted Packet Dropped within collection cycle (%)"),
    "total_drop": ("ledger-app-03-total-tx-dropped.csv", "Network|Total Transmitted Packets Dropped"),
    "total_tx": ("ledger-app-03-total-packets-tx.csv", "Network|Total Packets Transmitted"),
    "dep": ("ledger-app-03-tx-dropped.csv", "Network|(DEP) Transmitted Packets Dropped"),
}


@core.register
class Q0421(core.Case):
    question_id = "0421"
    seed = 421

    def generate(self, seed=None):
        seed = self.seed if seed is None else seed
        rng = core.make_rng(seed, "tx")
        base = core.bounded_walk(rng, N, 340_000, 2_500, 320_000, 360_000)
        jstar = rng.randint(0, 14)
        r = rng.uniform(0.028, 0.032)
        times = core.time_axis(START, N, STEP_S)
        tot, drop, peak, dep = [], [], [], []
        for k in range(N):
            t = [round(base[k] * core.clamp(rng.gauss(1, 0.01), 0.97, 1.03)) for _ in range(15)]
            d = [0] * 15
            if k == KSTAR:
                d[jstar] = round(t[jstar] * r)
            total = sum(t)
            tot.append(total)
            drop.append(sum(d))
            dep.append(sum(d) / 15)
            peak.append(max(d) / (total / 15) * 100)
        series = {"peak": [round(x, 6) for x in peak], "total_drop": drop, "total_tx": tot,
                  "dep": [round(x, 6) for x in dep]}
        out = {}
        for key, (fname, label) in FILES.items():
            out[fname] = formats.vcf_chart_csv(f"{OBJ} - {label}", list(zip(times, series[key])), TZ)
        return out

    def check(self, files):
        data, fails = {}, []
        for key, (fname, label) in FILES.items():
            try:
                title, rows = formats.parse_vcf_chart_csv(files[fname])
            except (KeyError, ValueError) as e:
                return [f"{fname}: {e}"]
            if title != f"{OBJ} - {label}":
                fails.append(f"{fname}: title {title!r}")
            if len(rows) != N:
                fails.append(f"{fname}: {len(rows)} rows")
            data[key] = rows
        stamps = [t for t, _ in data["peak"]]
        for key, rows in data.items():
            if [t for t, _ in rows] != stamps:
                fails.append(f"{key}: time stamps differ from the peak file")
        if fails:
            return fails
        if len(set(stamps)) != N or any((b - a).total_seconds() != STEP_S for a, b in zip(stamps, stamps[1:])):
            fails.append("stamps are not 72 distinct points 300 s apart")
        v = {k: [x for _, x in rows] for k, rows in data.items()}
        for i in range(N):
            if abs(v["dep"][i] - v["total_drop"][i] / 15) > 1e-5:
                fails.append(f"row {i + 1}: (DEP) != Total dropped / 15")
            if abs(v["peak"][i] - 15 * v["total_drop"][i] / v["total_tx"][i] * 100) > 1e-3:
                fails.append(f"row {i + 1}: A false, C false: Peak != 15 x Total dropped / Total transmitted x 100")
            if v["total_tx"][i] <= 4_500_000:
                fails.append(f"row {i + 1}: Total transmitted {v['total_tx'][i]} not above 4,500,000")
        pos = [i for i, x in enumerate(v["peak"]) if x > 0]
        if len(pos) != 1:
            return fails + [f"G true, H false: {len(pos)} rows with Peak > 0 (one burst cycle expected)"]
        i = pos[0]
        if not 2.5 <= v["peak"][i] <= 3.5:
            fails.append(f"G: Peak {v['peak'][i]} outside 2.5-3.5")
        ratio = 100 * v["total_drop"][i] / v["total_tx"][i]
        if not 0.15 <= ratio <= 0.25:
            fails.append(f"B true: Total ratio {ratio:.3f}% outside 0.15-0.25")
        if not 14.5 <= v["peak"][i] / ratio <= 15.5:
            fails.append("B true, G true: Peak / Total ratio not about 15")
        if not 100 * v["dep"][i] / v["total_tx"][i] < 0.02:
            fails.append("B true: (DEP) ratio not below 0.02%")
        for j in range(N):
            if j != i and (v["peak"][j] or v["total_drop"][j] or v["dep"][j]):
                fails.append(f"E false, H false: row {j + 1} has a non-zero drop value")
        return fails[:20]
