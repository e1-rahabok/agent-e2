"""Question 0369: one Ready burst sample on the Real-time and the Past day chart.

erp-app-03 (8 vCPUs). Real-time, 20 s, 180 rows 09:00:20 to 10:00:00Z, and
Past day, 5 minutes, 288 rows 2026-11-14T09:30Z to 2026-11-15T09:25Z (stamp =
start of the window, as `core.rollup_stamps(label="start")`). One real-time
Ready sample (3,600-4,400 ms at 09:15:20Z) lifts the 09:15 Past day row to the
sum of its 15 samples (Ready is a summation counter; Usage is the mean).

Relations: every Past day row from 09:05 to 09:25 = sum of Ready, mean of Usage
of the 15 real-time samples whose stamps fall in its window; the 09:15 row is
the highest Ready of the day and below 10,000.
"""

import datetime as dt
import math

from .. import core, formats, relations as rel

VM = "erp-app-03"
UTC = core.UTC
RT_FILE = "erp-app-03-cpu-real-time.csv"
PD_FILE = "erp-app-03-cpu-last-day.csv"
COLS = [f"Usage for {VM}", f"Ready for {VM}"]
RT_START = dt.datetime(2026, 11, 15, 9, 0, 20, tzinfo=UTC)
RT_N = 180
PD_START = dt.datetime(2026, 11, 14, 9, 30, tzinfo=UTC)
PD_N = 288
BURST_AT = dt.datetime(2026, 11, 15, 9, 15, 20, tzinfo=UTC)
BURST_ROW = dt.datetime(2026, 11, 15, 9, 15, tzinfo=UTC)
CHECK_ROWS = [dt.datetime(2026, 11, 15, 9, m, tzinfo=UTC) for m in (5, 10, 15, 20, 25)]


def _realtime(rng):
    """Internal series from 09:00:00 (sample 0 is not exported): 181 (usage, ready) samples."""
    times = core.time_axis(RT_START - dt.timedelta(seconds=20), RT_N + 1, 20)
    walk = core.bounded_walk(rng, len(times), 45, 1.2, 38, 52)
    out = []
    for t, w in zip(times, walk):
        u = round(w, 2)
        r = rng.randint(110, 330)
        if t == BURST_AT:
            u = round(max(35.0, w - rng.uniform(2, 6)), 2)
            r = rng.randint(3600, 4400)
        out.append((t, u, r))
    return out


@core.register
class Q0369(core.Case):
    question_id = "0369"
    seed = 369

    def generate(self, seed=None):
        seed = self.seed if seed is None else seed
        rng = core.make_rng(seed, "realtime")
        rt = _realtime(rng)
        rt_rows = [(t, [u, r]) for t, u, r in rt[1:]]
        by_window = {}
        for t, u, r in rt:
            by_window.setdefault(core.align_down(t, 300), []).append((u, r))
        rng = core.make_rng(seed, "day")
        pd_rows = []
        for t in core.time_axis(PD_START, PD_N, 300):
            if t in by_window and len(by_window[t]) == 15:
                w = by_window[t]
                pd_rows.append((t, [round(rel.rollup_mean([u for u, _ in w]), 2),
                                    rel.rollup_sum([r for _, r in w])]))
                continue
            lh = (t.hour + 8) % 24
            u = 41 + 11 * math.cos(2 * math.pi * (lh - 14) / 24) + rng.gauss(0, 2.5)
            r = 3200 + 900 * math.cos(2 * math.pi * (lh - 14) / 24) + rng.gauss(0, 450)
            pd_rows.append((t, [round(core.clamp(u, 20, 55), 2), round(core.clamp(r, 1600, 4800))]))
        return {RT_FILE: formats.vcenter_csv(COLS, rt_rows), PD_FILE: formats.vcenter_csv(COLS, pd_rows)}

    def check(self, files):
        fails = []
        try:
            c1, rt = formats.parse_vcenter_csv(files[RT_FILE])
            c2, pd = formats.parse_vcenter_csv(files[PD_FILE])
        except (KeyError, ValueError, IndexError) as e:
            return [f"parse: {e}"]
        if c1 != COLS or c2 != COLS:
            return ["columns differ"]
        if len(rt) != RT_N or len(pd) != PD_N:
            return [f"row counts {len(rt)} / {len(pd)}, expected {RT_N} / {PD_N}"]
        if rt[0][0] != RT_START or rt[-1][0] != dt.datetime(2026, 11, 15, 10, 0, tzinfo=UTC):
            fails.append("Real-time range differs")
        if any((b[0] - a[0]).total_seconds() != 20 for a, b in zip(rt, rt[1:])):
            fails.append("Real-time step is not 20 s")
        if pd[0][0] != PD_START or any((b[0] - a[0]).total_seconds() != 300 for a, b in zip(pd, pd[1:])):
            fails.append("Past day axis differs")
        if pd[-1][0] != dt.datetime(2026, 11, 15, 9, 25, tzinfo=UTC):
            fails.append("Past day does not end at 09:25Z")
        if any(r[1][1] != int(r[1][1]) or r[1][1] < 0 for r in rt + pd):
            fails.append("a Ready value is not a non-negative integer")
        ready = [r[1][1] for r in rt]
        high = [i for i, v in enumerate(ready) if v > 400]
        peak = max(ready)
        if len(high) != 1 or not 3500 <= peak <= 4500:                          # A true, B false (20,000 ms is one vCPU)
            fails.append(f"A: {len(high)} samples above 400, peak {peak}")
        elif rt[high[0]][0] != BURST_AT:                                        # stem: about 45 minutes ago
            fails.append(f"burst: the burst sample is at {rt[high[0]][0]}, not 09:15:20Z")
        pdmap = {t: v for t, v in pd}
        for ws in CHECK_ROWS:
            win = [v for t, v in rt if core.align_down(t, 300) == ws]
            if len(win) != 15:
                fails.append(f"window {ws:%H:%M}: {len(win)} samples")
                continue
            if pdmap[ws][1] != rel.rollup_sum([v[1] for v in win]):             # C, G
                fails.append(f"C: Past day Ready {ws:%H:%M} is not the sum of its 15 samples")
            if abs(pdmap[ws][0] - rel.rollup_mean([v[0] for v in win])) > 0.006:   # E false
                fails.append(f"E: Past day Usage {ws:%H:%M} is not the mean of its 15 samples")
            if not pdmap[ws][0] < 0.5 * sum(v[0] for v in win):                  # E false: not the sum
                fails.append(f"E: Past day Usage {ws:%H:%M} is within reach of the sum of its samples")
        burst = pdmap[BURST_ROW][1]
        if not burst > peak:                                                    # G
            fails.append("G: the 09:15 Past day Ready is not above the burst sample")
        if not burst < 10000:                                                   # D
            fails.append("D: the 09:15 Past day Ready is not below 10,000")
        if any(v[1] >= burst for t, v in pd if t != BURST_ROW):                 # D
            fails.append("D: another Past day row has Ready at or above the 09:15 row")
        win = [v[1] for t, v in rt if core.align_down(t, 300) == BURST_ROW]
        if sorted(win)[-2] >= 400:                                              # F false
            fails.append("F: another sample of the 09:15 window is 400 or more")
        return fails[:20]
