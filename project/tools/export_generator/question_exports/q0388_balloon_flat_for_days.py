"""Question 0388: a VM balloon that rose once and stayed flat for days.

mq-broker-02 (12 GB), Past week rollup (30 min, 336 rows). Balloon target
rises in three rows from 2026-11-09 14:00 UTC and holds a plateau of 27.5% of
configured memory; Ballooned memory follows from below and sits within 0.3% of
the target. Latency and swap rates are 0 in every row. Column names other
than Ballooned memory follow the "<Measurement> for <object>" pattern (assumed).
"""

from .. import export_framework, export_formats

VM = "mq-broker-02"
CONFIGURED_KB = 12 * 1024 * 1024
N = 336
STEP_S = 1800
START = export_framework.DEFAULT_START.replace(year=2026, month=11, day=8, hour=0, minute=0)
R = 76
PLATEAU = 3_460_000
F_MEM = "vcenter-vm-memory-past-week.csv"
F_SWAP = "vcenter-vm-swap-rates-past-week.csv"
C_MEM = [f"Balloon target for {VM}", f"Ballooned memory for {VM}", f"Latency for {VM}"]
C_SWAP = [f"Swap in rate for {VM}", f"Swap out rate for {VM}"]


def _times():
    return export_framework.rollup_stamps(export_framework.time_axis(START, N * 2, STEP_S // 2), 2)


@export_framework.register
class Q0388(export_framework.QuestionExport):
    question_id = "0388"
    seed = 388

    def generate(self, seed=None):
        seed = self.seed if seed is None else seed
        rng = export_framework.make_rng(seed, "balloon")
        target = []
        hold, cur = 0, 0
        for i in range(N):
            if i < R:
                cur = 0
            elif i == R:
                cur = round(1_150_000 + rng.uniform(-50_000, 50_000))
            elif i == R + 1:
                cur = round(2_600_000 + rng.uniform(-80_000, 80_000))
            else:
                if hold == 0:
                    cur = round(PLATEAU * (1 + rng.uniform(-0.004, 0.004)))
                    hold = rng.randint(2, 6)
                hold -= 1
            target.append(cur)
        ball = []
        for i in range(N):
            if i < R:
                b = 0
            elif i == R:
                b = int(0.55 * target[i])
            elif i == R + 1:
                b = int(0.80 * target[i])
            elif i == R + 2:
                b = int(0.97 * target[i])
            else:
                b = int(target[i] * (1 + rng.uniform(-0.003, 0)))
            ball.append(min(b, target[i]))
        times = _times()
        mem = [(t, [target[i], ball[i], 0]) for i, t in enumerate(times)]
        swap = [(t, [0, 0]) for t in times]
        return {F_MEM: export_formats.vcenter_csv(C_MEM, mem), F_SWAP: export_formats.vcenter_csv(C_SWAP, swap)}

    def check(self, files):
        fails = []
        try:
            cm, rm = export_formats.parse_vcenter_csv(files[F_MEM])
            cs, rs = export_formats.parse_vcenter_csv(files[F_SWAP])
        except (KeyError, ValueError) as e:
            return [str(e)]
        if cm != C_MEM or cs != C_SWAP:
            return [f"columns differ: {cm} {cs}"]
        if len(rm) != N or len(rs) != N:
            return [f"rows {len(rm)}/{len(rs)}, expected {N}"]
        if [r[0] for r in rm] != [r[0] for r in rs]:
            fails.append("time stamps differ between the two files")
        if rm[0][0] != START:
            fails.append("first time stamp differs")
        for a, b in zip(rm, rm[1:]):
            if (b[0] - a[0]).total_seconds() != STEP_S:
                fails.append(f"{b[0]}: not {STEP_S} s after the previous row")
        if any(v is None for r in rm + rs for v in r[1]):
            fails.append("a None cell")
        tg = export_formats.column(cm, rm, C_MEM[0])
        bl = export_formats.column(cm, rm, C_MEM[1])
        lat = export_formats.column(cm, rm, C_MEM[2])
        si = export_formats.column(cs, rs, C_SWAP[0])
        so = export_formats.column(cs, rs, C_SWAP[1])
        for i in range(N):
            if not 0 <= bl[i] <= tg[i]:
                fails.append(f"row {i}: Ballooned {bl[i]} outside 0..target {tg[i]}")
            if bl[i] > 0.65 * CONFIGURED_KB:
                fails.append(f"row {i}: Ballooned above the balloon ceiling")
            if si[i] == 0 and lat[i] != 0:
                fails.append(f"row {i}: Latency without swap in")
        tail = bl[192:]                                    # A
        if max(tail) / min(tail) > 1.02:
            fails.append("A: Ballooned varies more than 2% over the last three days")
        if not all(0.15 * CONFIGURED_KB <= v <= 0.50 * CONFIGURED_KB for v in tail):
            fails.append("A: Ballooned outside 15-50% of configured memory in the last three days")
        if any(v != 0 for v in bl[:R]) or any(v <= 0 for v in bl[R:]):
            fails.append("A: Ballooned is not 0 before row 76 and positive from it")
        if any(b < a for a, b in zip(bl[:R + 3], bl[1:R + 3])):
            fails.append("A: rise is not a single non-decreasing step")
        flat_t, flat_b = tg[R + 3:], bl[R + 3:]            # B false, H false: the target held, flat and equal to Ballooned
        if max(flat_t) / min(flat_t) > 1.02:
            fails.append("B/H: target varies in the flat rows")
        if any(abs(t - b) / t > 0.01 for t, b in zip(flat_t, flat_b)):
            fails.append("B/H: Ballooned further than 1% from the target in the flat rows")
        if any(v != 0 for v in lat) or any(v != 0 for v in si):  # C true, D false, F false
            fails.append("C/D: Latency or Swap in rate not 0")
        if any(v != 0 for v in so):
            fails.append("Swap out rate not 0")
        if any(abs(v - 10_430 * 1024) < 500_000 for v in bl[R:]):
            fails.append("Ballooned close to the knowledge-base example 10,430 MB")
        return fails[:20]
