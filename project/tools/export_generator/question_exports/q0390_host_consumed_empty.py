"""Question 0390: host Consumed after maintenance-mode evacuation.

esx-v14 (768 GB), 30-minute rows for 3 days. VMs leave in rows 50-51
(2026-11-12 01:00-01:30 UTC), the host is empty from row 52. Consumed keeps the
kernel's own use (about 25.6 GB), Granted keeps the management agents' mapped
memory. Column names follow the template's host Memory view.
"""

from .. import export_framework, export_formats

HOST = "esx-v14"
HOST_KB = 768 * 1024 * 1024
GB = 1024 * 1024
N = 144
STEP_S = 1800
START = export_framework.DEFAULT_START.replace(year=2026, month=11, day=11, hour=0, minute=0)
E1, E2, EMPTY = 50, 51, 52
FILE = "vcenter-host-memory-3-days.csv"
NAMES = ["Active", "Ballooned memory", "Consumed", "Granted", "Shared common", "Swap consumed"]
COLS = [f"{n} for {HOST}" for n in NAMES]
SCALE = {E1: 0.45, E2: 0.12}


def _walk(rng, n, lo, hi, step):
    return export_framework.bounded_walk(rng, n, (lo + hi) / 2, step, lo, hi)


@export_framework.register
class Q0390(export_framework.QuestionExport):
    question_id = "0390"
    seed = 390

    def generate(self, seed=None):
        seed = self.seed if seed is None else seed
        rng = export_framework.make_rng(seed, "host")
        g = _walk(rng, EMPTY, 605 * GB, 625 * GB, 3 * GB)
        s = _walk(rng, EMPTY, 5.5 * GB, 6.5 * GB, 0.15 * GB)
        rows = []
        for i, t in enumerate(export_framework.rollup_stamps(export_framework.time_axis(START, N * 2, STEP_S // 2), 2)):
            k = 26_843_546 * (1 + rng.uniform(-0.015, 0.015))
            a_mgmt = 2.1 * GB * (1 + rng.uniform(-0.02, 0.02))
            if i < EMPTY:
                f = SCALE.get(i, 1.0)
                gv, sv = f * g[i], f * s[i]
                ov = f * 6.0 * GB * (1 + rng.uniform(-0.02, 0.02))
                shared = sv * {E1: 0.35 / 0.45, E2: 0.1 / 0.12}.get(i, 1.0)
                cons = gv - 2 * shared + ov + k
                active = 0.14 * gv * (1 + rng.uniform(-0.10, 0.10)) + 1.2 * GB * (1 + rng.uniform(-0.1, 0.1))
                grant = gv + a_mgmt
            else:
                shared = rng.uniform(180_000, 260_000)
                cons = k
                active = 1.2 * GB * (1 + rng.uniform(-0.08, 0.08))
                grant = a_mgmt
            rows.append((t, [round(active), 0, round(cons), round(grant), round(shared), 0]))
        return {FILE: export_formats.vcenter_csv(COLS, rows)}

    def check(self, files):
        try:
            cols, rows = export_formats.parse_vcenter_csv(files[FILE])
        except (KeyError, ValueError) as e:
            return [f"{FILE}: {e}"]
        if cols != COLS:
            return [f"columns differ: {cols}"]
        fails = []
        if len(rows) != N or rows[0][0] != START:
            fails.append("row count or first time stamp differs")
        for a, b in zip(rows, rows[1:]):
            if (b[0] - a[0]).total_seconds() != STEP_S:
                fails.append(f"{b[0]}: not {STEP_S} s after the previous row")
        c = {n: export_formats.column(cols, rows, f"{n} for {HOST}") for n in NAMES}
        cons, gr, sh = c["Consumed"], c["Granted"], c["Shared common"]
        for i in range(N):
            if cons[i] > HOST_KB:
                fails.append(f"row {i}: Consumed above host memory")
            if c["Ballooned memory"][i] != 0 or c["Swap consumed"][i] != 0:
                fails.append(f"row {i}: Ballooned or Swap consumed not 0")
            if i >= EMPTY and not gr[i] < cons[i]:
                fails.append(f"row {i}: Granted not below Consumed on the empty host")
            if i < E1:                      # Consumed = (Granted - agents) - 2 x Shared + overhead + kernel
                resid = cons[i] - (gr[i] - 2.1 * GB) + 2 * sh[i]
                if abs(resid - 31.6 * GB) > 0.8 * GB:
                    fails.append(f"row {i}: Consumed does not follow Granted - 2 x Shared + overhead + kernel")
        if sum(cons[:E1]) / E1 < 600 * GB:                       # A
            fails.append("A: mean Consumed before the evacuation below 600 GB")
        if not cons[EMPTY] < 0.1 * cons[E1 - 1]:
            fails.append("A: Consumed(52) not below 10% of Consumed(49)")
        flat = cons[EMPTY:]
        if max(flat) / min(flat) > 1.10:
            fails.append("A/F: empty-host Consumed not flat (max/min above 1.10)")
        if sum(cons[132:144]) / 12 > sum(cons[52:64]) / 12 * 1.02:
            fails.append("A/F: upward trend on the empty host")
        if min(flat) <= 10 * GB or min(flat) <= 24 * GB:        # B
            fails.append("B: an empty-host Consumed value at or below 24 GB")
        med = sorted(flat)[len(flat) // 2]
        lit = 38_273_024                                         # 36.5 GB, literal in the prompt
        if abs(lit - med) / max(lit, med) < 0.20:                # D, E
            fails.append("D/E: median empty Consumed within 20% of 36.5 GB")
        for g in (17, 32, 41, 49, 57):
            if abs(med - g * GB) <= GB or abs(lit - g * GB) <= GB:
                fails.append(f"number guard: within 1 GB of {g} GB")
        return fails[:20]
