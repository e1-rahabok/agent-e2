"""Question 0395: VM memory Usage differs between vCenter and VCF Operations.

erp-db-11 (24 GB), 12 hours. vCenter Usage is active memory over configured
(about 7-14%), VCF Operations Usage is guest needed memory over total (about
65-75%). Consumed is flat near 22.3 GB. The VCF Operations file is one list
row with aggregates over 144 five-minute samples (assumed list format).
"""

from .. import core, formats

VM = "erp-db-11"
CONF = 25_165_824
GB = 1024 * 1024
N = 144
STEP_S = 300
START = core.DEFAULT_START.replace(year=2026, month=11, day=14, hour=0, minute=0)
F_VC = "vcenter-vm-memory-12h.csv"
F_VCF = "vcf-operations-vm-memory-12h.csv"
VC_NAMES = ["Usage", "Active", "Ballooned memory", "Consumed", "Granted"]
VC_COLS = [f"{n} for {VM}" for n in VC_NAMES]
VCF_COLS = ["Memory|Usage (%) (Max)", "Memory|Usage (%) (Min)", "Memory|Usage (%) (First)",
            "Memory|Usage (%) (Last)", "Guest|Needed Memory (KB) (Max)", "Guest|Needed Memory (KB) (Min)",
            "Guest|Needed Memory (KB) (First)", "Guest|Needed Memory (KB) (Last)",
            "Memory|Total Capacity (KB) (Last)", "Memory|Contention (%) (Max)"]


def _pearson(a, b):
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    den = (sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)) ** 0.5
    return num / den


@core.register
class Q0395(core.Case):
    question_id = "0395"
    seed = 395

    def generate(self, seed=None):
        seed = self.seed if seed is None else seed
        rng = core.make_rng(seed, "usage")
        lo, hi = round(1.76 * GB), round(3.55 * GB)
        base = core.bounded_walk(rng, N, 2.2 * GB, 0.06 * 2.2 * GB, lo, 2.6 * GB)
        burst = [max(core.burst_profile(N, 30, 12, 2)[i], core.burst_profile(N, 96, 15, 2)[i]) for i in range(N)]
        active = []
        for i in range(N):
            top = rng.uniform(3.2, 3.55) * GB
            active.append(round(core.clamp(core.blend(base[i], top, burst[i]), lo, hi)))
        rows = []
        for i, t in enumerate(core.rollup_stamps(core.time_axis(START, N, STEP_S), 1)):
            cons = round(22.3 * GB * (1 + rng.uniform(-0.005, 0.005)))
            grant = round(cons + 0.9 * GB * (1 + rng.uniform(-0.01, 0.01)))
            rows.append((t, [round(active[i] / CONF * 100, 2), active[i], 0, cons, grant]))
        need = core.bounded_walk(rng, 144, 16.7 * GB, 0.35 * GB, 15.6 * GB, 17.9 * GB)
        need = [round(x) for x in need]
        usage = [n / CONF * 100 + rng.uniform(-0.3, 0.3) for n in need]
        row = [max(usage), min(usage), usage[0], usage[-1], max(need), min(need), need[0], need[-1], CONF, 0]
        return {F_VC: formats.vcenter_csv(VC_COLS, rows),
                F_VCF: formats.vcf_list_csv(VCF_COLS, [(VM, row)])}

    def check(self, files):
        try:
            cols, rows = formats.parse_vcenter_csv(files[F_VC])
            vcols, vrows = formats.parse_vcf_list_csv(files[F_VCF])
        except (KeyError, ValueError) as e:
            return [str(e)]
        if cols != VC_COLS or vcols != VCF_COLS:
            return [f"columns differ: {cols} {vcols}"]
        fails = []
        if len(rows) != N or rows[0][0] != START:
            fails.append("vCenter rows or first time stamp differ")
        if any((b[0] - a[0]).total_seconds() != STEP_S for a, b in zip(rows, rows[1:])):
            fails.append("E: vCenter time stamps do not step by 300 s")
        c = {n: formats.column(cols, rows, f"{n} for {VM}") for n in VC_NAMES}
        use, act, con, gr = c["Usage"], c["Active"], c["Consumed"], c["Granted"]
        for i in range(len(rows)):
            exp = act[i] / CONF * 100
            if abs(use[i] - exp) > 0.01 or use[i] > 15:
                fails.append(f"row {i}: Usage {use[i]} vs Active/configured {exp:.2f}")
            if not con[i] <= gr[i] <= CONF or c["Ballooned memory"][i] != 0:
                fails.append(f"row {i}: Consumed/Granted/Ballooned relation broken")
            if con[i] < 0.85 * CONF:
                fails.append(f"row {i}: Consumed below 85% of configured")
        if _pearson(use, act) <= 0.95:
            fails.append("A: Usage does not follow Active")
        if max(con) / min(con) > 1.02:
            fails.append("A: Consumed not flat")
        if len(vrows) != 1 or vrows[0][0] != VM:
            return fails + ["VCF Operations file: not one row for the VM"]
        v = vrows[0][1]
        for k in range(4):
            if abs(v[k] - v[4 + k] / v[8] * 100) > 2:
                fails.append(f"B: aggregate {VCF_COLS[k]} not within 2 points of Needed / Total")
            if v[k] < 60:
                fails.append(f"B: {VCF_COLS[k]} below 60")
        if v[9] != 0:
            fails.append("F: Contention (Max) not 0")
        if max(act) >= 0.3 * v[5]:
            fails.append("G: Active not far below Needed")
        return fails[:20]
