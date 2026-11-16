"""Question 0371: Usage reads above 100 while Net Run stays below 82.

fin-rpt-05 (4 vCPUs). Daily Maximum over 7 days (VCF Operations List view,
ASSUMED format) and the afternoon of 2026-11-15 as two VCF Operations chart
CSVs (Usage and Net Run, 72 points, stamped at the end of the 5-minute cycle,
12:05 PM to 6:00 PM GMT+08:00).

Model: 2,016 five-minute points per metric. Net Run plateau 73-81 from 13:30 to
17:15; Usage = Net Run x r with r about 1.38 on the plateau (turbo), 1.07-1.15
at low load. Each day's maximum of Usage and of Net Run is the same point.
Demand follows Usage. Ready and Co-stop stay low.
"""

import datetime as dt

from .. import core, formats

TZ = 8
Z = dt.timezone(dt.timedelta(hours=TZ))
DAY0 = dt.datetime(2026, 11, 9, 0, 0, tzinfo=Z)
DAYS = 7
PER_DAY = 288
VM = "fin-rpt-05"
FD = "fin-rpt-05-cpu-daily-max-7-days.csv"
FU = "fin-rpt-05-cpu-usage-afternoon.csv"
FN = "fin-rpt-05-cpu-net-run-afternoon.csv"
CD = ["CPU|Usage (%) (Max)", "CPU|Net Run (%) (Max)", "CPU|Demand (%) (Max)",
      "CPU|Ready (%) (Max)", "CPU|Co-stop (%) (Max)"]
PLATEAU = range(162, 207)    # 13:30 to 17:15
AFTERNOON = range(144, 216)  # 12:00 to 18:00; stamps are the cycle ends 12:05 .. 18:00


def _net_run_day(rng):
    plateau_walk = core.bounded_walk(rng, len(PLATEAU), 77.5, 1.2, 73.2, 80.2)
    out = []
    for i in range(PER_DAY):
        h = i / 12
        if i in PLATEAU:
            v = plateau_walk[i - PLATEAU.start]
        elif 144 <= i < 162:
            v = core.blend(30, 70, (i - 144) / 18) + rng.gauss(0, 1.5)
        elif 207 <= i < 216:
            v = core.blend(77, 20, (i - 207) / 9) + rng.gauss(0, 1.5)
        elif h < 12:
            v = rng.uniform(4, 15)
        else:
            v = rng.uniform(8, 20)
        out.append(core.clamp(v, 3, 80.4))
    peak = rng.choice(list(PLATEAU))
    out[peak] = rng.uniform(80.6, 81.4)
    return out, peak


def _model(seed):
    """Per day: (net_run, usage, demand, ready, costop) lists of 288 points."""
    days = []
    for d in range(DAYS):
        rng = core.make_rng(seed, f"day{d}")
        nr, peak = _net_run_day(rng)
        r = [1.05 + 0.33 * min(1.0, x / 75) + rng.gauss(0, 0.006) for x in nr]
        r[peak] = max(r) + 0.002
        usage = [core.clamp(x * k, x, 115) for x, k in zip(nr, r)]
        demand = [u * rng.uniform(0.98, 1.02) for u in usage]
        ready = [rng.uniform(0.05, 0.6) for _ in range(PER_DAY)]
        for i in rng.sample(list(AFTERNOON), 4) if d == DAYS - 1 else []:
            ready[i] = rng.uniform(0.65, 0.85)
        costop = [rng.uniform(0.0, 0.25) for _ in range(PER_DAY)]
        days.append((nr, usage, demand, ready, costop))
    return days


@core.register
class Q0371(core.Case):
    question_id = "0371"
    seed = 371

    def generate(self, seed=None):
        days = _model(self.seed if seed is None else seed)
        rows = []
        for d, (nr, usage, demand, ready, costop) in enumerate(days):
            rows.append((formats.vcf_time(DAY0 + dt.timedelta(days=d), TZ),
                         [max(usage), max(nr), max(demand), max(ready), max(costop)]))
        last = days[-1]
        start = DAY0 + dt.timedelta(days=DAYS - 1)
        stamps = [start + dt.timedelta(minutes=5 * (i + 1)) for i in AFTERNOON]
        usage = [(t, last[1][i]) for t, i in zip(stamps, AFTERNOON)]
        net = [(t, last[0][i]) for t, i in zip(stamps, AFTERNOON)]
        return {FD: formats.vcf_list_csv(CD, rows, name_header="Time"),
                FU: formats.vcf_chart_csv(f"{VM} - CPU|Usage (%)", usage, TZ),
                FN: formats.vcf_chart_csv(f"{VM} - CPU|Net Run (%)", net, TZ)}

    def check(self, files):
        fails = []
        try:
            cols, rows = formats.parse_vcf_list_csv(files[FD])
            tu, pu = formats.parse_vcf_chart_csv(files[FU])
            tn, pn = formats.parse_vcf_chart_csv(files[FN])
        except (KeyError, ValueError, IndexError) as e:
            return [f"parse: {e}"]
        if cols != CD or len(rows) != DAYS or len(pu) != 72 or len(pn) != 72:
            return ["columns or row counts differ"]
        if tu != f"{VM} - CPU|Usage (%)" or tn != f"{VM} - CPU|Net Run (%)":
            fails.append("chart titles differ")
        stamps = [t for t, _ in pu]
        if stamps != [t for t, _ in pn]:
            fails.append("afternoon stamps differ between the files")
        first = DAY0 + dt.timedelta(days=DAYS - 1, hours=12, minutes=5)
        if stamps[0] != first or any((b - a).total_seconds() != 300 for a, b in zip(stamps, stamps[1:])):
            fails.append("afternoon stamps are not 5 minutes apart from 12:05 PM")
        if formats.vcf_time(stamps[-1]).split(" GMT")[0] != "November 15, 2026, 6:00:00 PM":
            fails.append("last afternoon stamp is not 6:00:00 PM")
        usage = [v for _, v in pu]
        net = [v for _, v in pn]
        for i, (u, n) in enumerate(zip(usage, net)):
            if n > 100 or u < n - 1e-9:
                fails.append(f"afternoon point {i}: Usage {u}, Net Run {n}")
                break
        if max(net) >= 82:                                                       # B, K
            fails.append("B: an afternoon Net Run value is 82 or above")
        for i, (label, v) in enumerate(rows):
            if formats.parse_vcf_time(label) != DAY0 + dt.timedelta(days=i):
                fails.append(f"daily row {i}: label {label}")
            u, n, dem, rd, cs = v
            if not 72 <= n <= 82:                                                # K
                fails.append(f"K: {label}: Net Run Max {n} outside 72-82")
            if not (rd < 1 and cs < 0.5):                                        # G
                fails.append(f"G: {label}: Ready Max {rd} or Co-stop Max {cs} too high")
            if not 100 <= u <= 115 or not u - n >= 20:                           # L, A, H
                fails.append(f"L: {label}: Usage Max {u}, Net Run Max {n}")
            if u < n or abs(dem - u) > 3:
                fails.append(f"{label}: Usage Max / Demand Max relation broken")
            if not dem > n + 15:                                                 # E
                fails.append(f"E: {label}: Demand Max {dem} not above Net Run Max + 15")
        last = rows[-1][1]
        if abs(last[0] - round(max(usage), 4)) > 5e-5 or abs(last[1] - round(max(net), 4)) > 5e-5:
            fails.append("daily row of November 15 differs from the afternoon maxima")
        if usage.index(max(usage)) != net.index(max(net)):
            fails.append("the Usage and Net Run maxima of November 15 are at different stamps")
        hot = [(u, n) for u, n in zip(usage, net) if u >= 100]
        if len(hot) < 6 or any(u - n < 20 for u, n in hot):                      # L
            fails.append(f"L: {len(hot)} points with Usage >= 100, or a gap below 20")
        return fails[:20]
