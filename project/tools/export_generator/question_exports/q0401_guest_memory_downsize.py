"""Question 0401: guest memory over four weeks across a downsize (40 GB -> 20 GB).

One VCF Operations List view CSV, one row per day, each value the day's
maximum of the 5-minute values. The List view format is ASSUMED (not
captured), see the export_generator README. VM erp-app-04 (Windows Server), cut on
Saturday 2026-10-31 at about 23:00 local: the Oct 31 row still carries the
old size because its daily max includes the hours before.

Relations on every row: Total is 40 GB before the cut and 20 GB after,
Consumed <= Total, Free + Needed <= Total, Contention 0. Needed follows the
VMware Tools formula with its 5% buffer: Needed = underlying need + 0.05 x
configured size, so the same workload shows a Needed that is about 1 GB lower
after the downsize while Needed/Total roughly doubles.
"""

import datetime as dt

from .. import export_framework, export_formats

GB = 1_048_576  # KB
TZ = 8
FIRST_DAY = dt.date(2026, 10, 18)
DAYS = 28
CUT = 14  # rows 0..13 before, 14..27 after
TOTAL_BEFORE = 40 * GB
TOTAL_AFTER = 20 * GB
PATCH_DAY = dt.date(2026, 10, 21)

COLS = ["Memory|Total Capacity (KB) (Max)",
        "Memory|Consumed (KB) (Max)",
        "Guest|Free Memory (KB) (Max)",
        "Guest|Needed Memory (KB) (Max)",
        "Guest|Peak Guest OS Page-out Rate within collection cycle (Max)",
        "Memory|Contention (%) (Max)"]


def _midnight(d):
    return dt.datetime(d.year, d.month, d.day, tzinfo=dt.timezone(dt.timedelta(hours=TZ)))


@export_framework.register
class GuestMemoryDownsize(export_framework.QuestionExport):
    question_id = "0401"
    seed = 401
    filename = "vcf-operations-vm-memory-28-days.csv"

    def generate(self, seed=None):
        rng = export_framework.make_rng(self.seed if seed is None else seed, "mem-downsize")
        rows = []
        for i in range(DAYS):
            day = FIRST_DAY + dt.timedelta(days=i)
            weekend = day.weekday() >= 5
            after = i >= CUT
            total = TOTAL_AFTER if after else TOTAL_BEFORE
            size_gb = 20 if after else 40
            need = rng.uniform(8.4, 8.6) if weekend else rng.uniform(8.6, 9.0)
            needed = round((need + 0.05 * size_gb) * GB)
            free_gb = rng.uniform(3.0, 5.0) if after else rng.uniform(18.0, 22.0)
            free = round(free_gb * GB)
            free = min(free, int(0.98 * total) - needed)
            consumed = round(rng.uniform(0.96, 0.99) * total)
            if weekend:
                pageout = rng.randint(60, 300)
            else:
                pageout = int(min(1800, max(250, rng.lognormvariate(6.35, 0.45))))
            if day == PATCH_DAY:
                pageout = rng.randint(2200, 2600)
            rows.append([day, total, consumed, free, needed, pageout])
        before_max = max(r[5] for r in rows[:CUT])
        cap = int(0.85 * before_max)
        out = []
        for i, r in enumerate(rows):
            if i >= CUT:
                r[5] = min(r[5], cap)
            out.append((export_formats.vcf_time(_midnight(r[0]), TZ), r[1:] + [0]))
        return {self.filename: export_formats.vcf_list_csv(COLS, out, name_header="Time")}

    def check(self, files):
        fails = []
        try:
            cols, rows = export_formats.parse_vcf_list_csv(files[self.filename])
        except (KeyError, ValueError, IndexError) as e:
            return [f"{self.filename}: {e}"]
        if cols != COLS:
            return [f"columns differ: {cols}"]
        if len(rows) != DAYS:
            return [f"{len(rows)} rows, expected {DAYS}"]
        for i, (name, _) in enumerate(rows):
            want = _midnight(FIRST_DAY + dt.timedelta(days=i))
            if export_formats.parse_vcf_time(name) != want:
                fails.append(f"row {i}: Time {name!r} is not local midnight {want}")
        v = lambda j: [r[1][j] for r in rows]
        total, cons, free, need, po, cont = (v(j) for j in range(6))
        for i in range(DAYS):
            want = TOTAL_BEFORE if i < CUT else TOTAL_AFTER
            if total[i] != want:
                fails.append(f"row {i}: Total {total[i]} != {want}")
            if cons[i] > total[i]:
                fails.append(f"row {i}: Consumed above Total")
            if free[i] + need[i] > total[i]:
                fails.append(f"row {i}: Free + Needed above Total")
            if cont[i] != 0:
                fails.append(f"row {i}: Contention {cont[i]} != 0")
            if any(x != int(x) for x in (total[i], cons[i], free[i], need[i], po[i])):
                fails.append(f"row {i}: KB or page-out value is not an integer")
        # A true
        lim = 0.75 * TOTAL_AFTER
        if max(need) >= lim:
            fails.append(f"A: max Needed {max(need)} >= 0.75 x new Total")
        # B false
        mean = lambda xs: sum(xs) / len(xs)
        if mean(free[CUT:]) > 0.35 * mean(free[:CUT]):
            fails.append("B: Free after is not far lower than before")
        # C true
        if not max(po[CUT:]) < max(po[:CUT]):
            fails.append("C: page-out peak after is not below before")
        # E true: Needed about 1 GB lower after the cut (5% buffer of a 20 GB VM against 40 GB)
        gap = (mean(need[:CUT]) - mean(need[CUT:])) / 1_048_576
        if not 0.8 <= gap <= 1.3:
            fails.append(f"E: mean Needed before - after = {gap:.2f} GB, not 0.8-1.3 GB")
        rb = mean([n / t for n, t in zip(need[:CUT], total[:CUT])])
        ra = mean([n / t for n, t in zip(need[CUT:], total[CUT:])])
        if not 0.24 <= rb <= 0.29 or not 0.44 <= ra <= 0.52 or not 1.7 <= ra / rb <= 2.3:
            fails.append(f"Needed/Total before {rb:.3f}, after {ra:.3f}")
        # F (false): Needed did not fall by half
        nb = mean(need[:CUT])
        if not 0.85 <= mean(need[CUT:]) / nb <= 1.0:
            fails.append("F: mean Needed ratio outside [0.85, 1.0]")
        if any(not 0.85 * nb <= x <= 1.15 * nb for x in need[CUT:]):
            fails.append("F: an after-row Needed outside 0.85..1.15 x mean before")
        return fails[:20]
