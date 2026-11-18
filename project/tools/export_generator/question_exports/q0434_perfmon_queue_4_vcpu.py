"""Question 0434: Perfmon processor queue on a 4-vCPU VM (batch-win-04).

typeperf -si 60 -sc 61: 61 rows from 01:00. Row 0 prints " " for every rate
counter (% columns, Context Switches/sec); Processor Queue Length is
instantaneous and has a value. About 16 runnable threads on 4 vCPUs.
"""

import datetime as dt

from .. import export_framework, export_formats

GUEST = "BATCH-WIN-04"
START = dt.datetime(2026, 11, 10, 1, 0, 0)
SPEC = ([("Processor", f"{k}", "% Processor Time") for k in range(4)]
        + [("Processor", "_Total", "% Processor Time"), ("Processor", "_Total", "% Privileged Time"),
           ("Processor Information", "_Total", "% Processor Utility"),
           ("System", None, "Processor Queue Length"), ("System", None, "Context Switches/sec")])
COLS = [export_formats.typeperf_name(GUEST, o, i, c) for o, i, c in SPEC]
FILE = "typeperf-cpu.csv"


@export_framework.register
class PerfmonQueue4Vcpu(export_framework.QuestionExport):
    question_id = "0434"
    seed = 434

    def generate(self, seed=None):
        rng = export_framework.make_rng(self.seed if seed is None else seed, "perfmon-queue")
        while True:
            pause = rng.sample(range(5, 56), 3)
            extra = rng.sample([j for j in range(1, 61) if j not in pause], 3)
            low = sorted(set(pause + extra))
            run, best = 0, 0
            for j in range(1, 61):
                run = run + 1 if j in low else 0
                best = max(best, run)
            if best <= 2:
                break
        ratio = export_framework.bounded_walk(rng, 60, 1.20, 0.01, 1.15, 1.26)
        rows = [(START, [None] * 7 + [rng.randint(10, 14), None])]
        for j in range(1, 61):
            if j in pause:
                cpu = [round(rng.uniform(70, 88), 6) for _ in range(4)]
            else:
                cpu = [round(export_framework.clamp(97.5 + rng.gauss(0, 2.0), 85, 100), 6) for _ in range(4)]
            total = round(sum(cpu) / 4, 6)
            priv = round(rng.uniform(4.0, 9.0), 6)
            util = round(total * ratio[j - 1], 6)
            if j in low:
                q = rng.randint(4, 8)
            else:
                q = int(export_framework.clamp(12 + round(rng.gauss(0, 1.5)), 9, 16))
            cs = round(export_framework.noisy(rng, 18_000 + 16_000 * (j - 1) / 59, 0.06), 6)
            rows.append((START + dt.timedelta(minutes=j), cpu + [total, priv, util, q, cs]))
        return {FILE: export_formats.typeperf_csv(COLS, rows, "Coordinated Universal Time", 0)}

    def check(self, files):
        fails = []
        try:
            cols, rows = export_formats.parse_typeperf_csv(files[FILE])
        except (KeyError, ValueError, IndexError) as e:
            return [f"parse: {e}"]
        if cols != COLS or len(rows) != 61:
            return ["columns or row count differ"]
        if rows[0][0] != START or {(b[0] - a[0]).total_seconds() for a, b in zip(rows, rows[1:])} != {60.0}:
            fails.append("axis is not 60 s from 01:00")
        r0 = rows[0][1]
        if any(x is not None for i, x in enumerate(r0) if i != 7) or r0[7] is None:
            fails.append("row 0 must be empty except Processor Queue Length")
        data = [v for _, v in rows[1:]]
        if any(None in v for v in data):
            fails.append("an empty value after row 0")
            return fails
        for j, v in enumerate(data, 1):
            cpu, total, priv, util, q, cs = v[:4], v[4], v[5], v[6], v[7], v[8]
            if abs(total - sum(cpu) / 4) > 0.01 or not priv < total or not util > total:
                fails.append(f"row {j}: relation broken")
            if any(not 0 <= x <= 100 for x in cpu) or q != int(q) or q < 0:
                fails.append(f"row {j}: range")
        q = [v[7] for v in data]
        if sum(x > 8 for x in q) < 50:
            fails.append("A: Queue Length above 8 in fewer than 50 rows")
        run = best = 0
        for x in q:
            run = run + 1 if x <= 8 else 0
            best = max(best, run)
        if best > 2:
            fails.append("A: run of more than 2 rows at 8 or below")
        for k in range(4):
            if sum(v[k] >= 90 for v in data) < 54:
                fails.append(f"D: Processor({k}) at 90 or above in fewer than 54 rows")
        if rows[0][1][7] == 0 or any(x == 0 for x in q) or sorted(q)[30] <= 8:
            fails.append("I false: queue is 0 or median not above 8")
        if sum(v[6] > 100 for v in data) < 45 or any(v[4] > 100 for v in data):   # J true: Utility above 100, Processor Time never
            fails.append("J: % Processor Utility not above 100 in at least 45 rows, or % Processor Time above 100")
        cs = [v[8] for v in data]
        if sum(cs[50:]) / 10 < 1.5 * sum(cs[:10]) / 10:
            fails.append("C false (stem): Context Switches/sec do not rise 1.5x")
        return fails[:20]
