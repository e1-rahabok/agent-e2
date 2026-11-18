"""Question 0372: CPU Wait on a quiet VM, Real-time chart as a table.

svc-int-08 (8 vCPUs, 160,000 ms per 20 s sample). Run 10,500-18,500 ms, Ready
90-650 ms, Co-stop mostly 0, Swap wait 0; Wait = 160,000 - Run - Ready -
Co-stop; Idle = Wait - Swap wait - hidden other wait (150-850 ms), so Wait
is nearly all Idle and Wait - Idle stays between 0 and 1,000.

Relations: Run + Ready + Co-stop + Wait = 160,000 in every row; 0 <= Wait -
Idle - Swap wait < 1,000; every value an integer except Usage (2 decimals).
"""

import datetime as dt

from .. import export_framework, export_formats, counter_relations as rel

VM = "svc-int-08"
FILE = "svc-int-08-cpu-real-time.csv"
N = 180
START = dt.datetime(2026, 11, 15, 3, 0, 20, tzinfo=export_framework.UTC)
COLS = [f"{m} for {VM}" for m in ("Usage", "Run", "Ready", "Co-stop", "Wait", "Idle", "Swap wait")]
TOTAL = rel.vcpu_state_total_ms(8)


@export_framework.register
class Q0372(export_framework.QuestionExport):
    question_id = "0372"
    seed = 372

    def generate(self, seed=None):
        rng = export_framework.make_rng(self.seed if seed is None else seed, "csv")
        walk = export_framework.bounded_walk(rng, N, 13500, 600, 10500, 18500)
        bump = set(rng.sample(range(N), 6))
        times = export_framework.time_axis(START, N, 20)
        rows = []
        for i, t in enumerate(times):
            run = round(export_framework.clamp(walk[i] + (rng.uniform(1500, 3000) if i in bump else 0), 10500, 18500))
            ready = rng.randint(90, 650)
            costop = rng.randint(1, 40) if rng.random() < 0.12 else 0
            wait = rel.wait_from_states(8, run, ready, costop)
            other = rng.randint(150, 850)
            idle = wait - 0 - other
            usage = round(run / TOTAL * 100 * rng.uniform(0.95, 1.05), 2)
            rows.append((t, [usage, run, ready, costop, wait, idle, 0]))
        return {FILE: export_formats.vcenter_csv(COLS, rows)}

    def check(self, files):
        fails = []
        try:
            cols, rows = export_formats.parse_vcenter_csv(files[FILE])
        except (KeyError, ValueError, IndexError) as e:
            return [f"parse: {e}"]
        if cols != COLS or len(rows) != N:
            return ["columns or row count differ"]
        if rows[0][0] != START or rows[-1][0] != dt.datetime(2026, 11, 15, 4, 0, tzinfo=export_framework.UTC):
            fails.append("time range differs")
        if any((b[0] - a[0]).total_seconds() != 20 for a, b in zip(rows, rows[1:])):
            fails.append("step is not 20 s")
        waits = []
        for t, (usage, run, ready, costop, wait, idle, swap) in rows:
            if min(run, ready, costop, wait, idle, swap, usage) < 0:
                fails.append(f"{t:%H:%M:%S}: negative value")
            if any(v != int(v) for v in (run, ready, costop, wait, idle, swap)):
                fails.append(f"{t:%H:%M:%S}: a millisecond value is not an integer")
            if not rel.state_sum_ms(run, ready, costop, wait) == TOTAL:         # C
                fails.append(f"C: {t:%H:%M:%S}: state sum {run + ready + costop + wait}")
            if not 0 < wait - idle < 1000:                                      # A, E
                fails.append(f"A: {t:%H:%M:%S}: Wait - Idle = {wait - idle}")
            if not 0 <= wait - idle - swap < 1000 or idle > wait:
                fails.append(f"{t:%H:%M:%S}: Wait, Idle, Swap wait relation broken")
            if not 140000 <= wait <= 150000:                                    # D
                fails.append(f"D: {t:%H:%M:%S}: Wait {wait} outside 140,000-150,000")
            if not (ready < 800 and costop <= 40):                              # B, F, J
                fails.append(f"B: {t:%H:%M:%S}: Ready {ready} or Co-stop {costop} too high")
            if swap != 0:
                fails.append(f"{t:%H:%M:%S}: Swap wait is not 0")
            waits.append(wait)
        if not 0.88 <= sum(waits) / len(waits) / TOTAL <= 0.94:                 # D
            fails.append("D: mean Wait share outside 0.88-0.94")
        return fails[:20]
