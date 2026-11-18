"""Question 0381: Linux top shows st 0.0, vCenter shows Ready about 21%.

File: vCenter real-time CPU chart of a 4-vCPU RHEL 9 VM. Inline: the `top`
summary (inline:1) and `sar -u ALL 60 10` (inline:2) of the same ten minutes.
The guest has no steal clock (default VM settings), so st and %steal are 0
while the frozen time is counted inside us and sy.

Relations: Run + Ready + Co-stop + Wait = 80,000 ms; Readiness = Ready /
80,000; Co-stop < Ready; Usage < Run %; every sar row and the top CPU line
sum to 100; sar us + sy follows the busy share (Run + Ready + Co-stop) / 800.
"""

import datetime as dt
import re

from .. import export_framework, export_formats, counter_relations as rel

VM = "app-lnx-03"
VCPUS = 4
ROWS = 30
KERNEL = "5.14.0-427.13.1.el9_4.x86_64"
VC = [f"{m} for {VM}" for m in ("Usage", "Readiness", "Ready", "Run", "Co-stop", "Wait")]
TOTAL = rel.vcpu_state_total_ms(VCPUS)
START = dt.datetime(2026, 11, 10, 14, 0, 0, tzinfo=export_framework.UTC)
SAR_COLS = ("%usr", "%nice", "%sys", "%iowait", "%steal", "%irq", "%soft", "%guest", "%gnice", "%idle")
TOP_KEYS = ("us", "sy", "ni", "id", "wa", "hi", "si", "st")


def _build(seed):
    rng = export_framework.make_rng(seed, "linux-st-zero")
    target = export_framework.bounded_walk(rng, ROWS, 21, 1.5, 15, 27)
    runpct = export_framework.bounded_walk(rng, ROWS, 56, 1.5, 50, 62)
    vc_rows, busy, runs = [], [], []
    for i in range(ROWS):
        ready = round(rel.ready_ms_from_readiness(target[i], VCPUS))
        run = round(runpct[i] * 800)
        costop = rng.randint(400, 1200)
        wait = rel.wait_from_states(VCPUS, run, ready, costop)
        assert wait > 0 and costop < ready
        readiness = round(rel.readiness_pct(ready, VCPUS), 2)
        usage = round(runpct[i] * rng.uniform(0.84, 0.92), 2)
        vc_rows.append((START + dt.timedelta(seconds=20 * (i + 1)), [usage, readiness, ready, run, costop, wait]))
        busy.append((run + ready + costop) / 800)
        runs.append(run)
    load = tuple(round(b + rng.uniform(-0.15, 0.15), 2) for b in (4.62, 4.41, 3.37))
    b = busy[-1]
    sy = round(rng.uniform(6.0, 9.0), 1)
    hi = 0.3
    si = round(rng.uniform(0.4, 0.8), 1)
    wa = round(rng.uniform(0.3, 1.5), 1)
    us = round(b - sy - hi - si - 0.0, 1)
    idle = round(100.0 - (us + sy + 0.0 + wa + hi + si + 0.0), 1)
    cpu = {"us": us, "sy": sy, "ni": 0.0, "id": idle, "wa": wa, "hi": hi, "si": si, "st": 0.0}
    top = export_formats.top_summary(
        "14:10:00", "12 days,  3:12", 1, load, (287, 5, 282, 0, 0), cpu,
        (15731.4, 2210.6, 9876.3, round(15731.4 - 2210.6 - 9876.3, 1)), (4096.0, 4096.0, 0.0, 5402.8),
        [(2214, "appsvc", "20", 0, 6876544, 742131, 30212, "S", round(4 * b - 12, 1), 4.6, "1832:41.07", "java"),
         (1088, "root", "20", 0, 19876, 11024, 9472, "S", 0.7, 0.1, "0:12.44", "sshd"),
         (711, "root", "20", 0, 52140, 21980, 20112, "S", 0.3, 0.1, "1:02.18", "systemd-journal")])
    sar_rows = []
    for k in range(10):
        bk = sum(busy[3 * k:3 * k + 3]) / 3
        io = round(rng.uniform(0.30, 1.50), 2)
        irq = round(rng.uniform(0.20, 0.60), 2)
        soft = round(rng.uniform(0.30, 0.90), 2)
        sys_ = round(rng.uniform(6.00, 10.00), 2)
        usr = round(bk - sys_ - irq - soft, 2)
        vals = [usr, 0.0, sys_, io, 0.0, irq, soft, 0.0, 0.0]
        vals.append(round(100.0 - sum(vals), 2))
        sar_rows.append((f"02:{k + 1:02d}:00 PM", vals))
    avg = [round(sum(r[1][c] for r in sar_rows) / 10, 2) for c in range(10)]
    avg[9] = round(100.0 - sum(avg[:9]), 2)
    sar = export_formats.sar_u(KERNEL, VM, "11/10/2026", 4, "02:00:00 PM", sar_rows, avg, cols=SAR_COLS)
    return vc_rows, top, sar


@export_framework.register
class LinuxStZeroReadyHigh(export_framework.QuestionExport):
    question_id = "0381"
    seed = 381
    f_vc = "vcenter-vm-cpu-realtime.csv"

    def generate(self, seed=None):
        vc, _, _ = _build(self.seed if seed is None else seed)
        return {self.f_vc: export_formats.vcenter_csv(VC, vc)}

    def generate_inline(self, seed=None):
        _, top, sar = _build(self.seed if seed is None else seed)
        return {1: top, 2: sar}

    def check(self, files):
        try:
            cols, rows = export_formats.parse_vcenter_csv(files[self.f_vc])
        except (KeyError, ValueError, IndexError) as e:
            return [f"parse: {e}"]
        if cols != VC:
            return ["columns differ"]
        fails = []
        if len(rows) != ROWS:
            return [f"{len(rows)} rows"]
        for i, (t, v) in enumerate(rows):
            if t != START + dt.timedelta(seconds=20 * (i + 1)):
                fails.append(f"row {i}: time off the 20 s axis")
            usage, readiness, ready, run, costop, wait = v
            if rel.state_sum_ms(run, ready, costop, wait) != TOTAL:
                fails.append(f"row {i}: state sum")
            if abs(readiness - rel.readiness_pct(ready, VCPUS)) > 0.006:
                fails.append(f"row {i}: Readiness vs Ready")
            if not costop < ready:
                fails.append(f"row {i}: Co-stop not below Ready")
            if not usage < run / 800:
                fails.append(f"row {i}: Usage not below Run %")
            if wait <= 0:
                fails.append(f"row {i}: Wait not positive")
            if not ready / run > 0.2:                      # B true; A false (the wait is in the export)
                fails.append(f"row {i}: Ready / Run {ready / run:.3f} not above 0.2")
            if readiness < 14:                             # C false (Readiness 14-28%), D false
                fails.append(f"row {i}: Readiness {readiness} below 14")
        return fails[:20]

    def check_inline(self, blocks, files):
        fails = []
        try:
            _, rows = export_formats.parse_vcenter_csv(files[self.f_vc])
        except (KeyError, ValueError, IndexError) as e:
            return [f"parse: {e}"]
        top, sar = blocks.get(1, ""), blocks.get(2, "")
        m = re.search(r"^%Cpu\(s\):(.*)$", top, re.M)
        if not m:
            return ["inline:1: no %Cpu(s) line"]
        vals = {k: float(x) for x, k in re.findall(r"([\d.]+) (us|sy|ni|id|wa|hi|si|st)\b", m.group(1))}
        if set(vals) != set(TOP_KEYS):
            return [f"inline:1: %Cpu(s) fields {sorted(vals)}"]
        if abs(sum(vals.values()) - 100.0) > 0.15:
            fails.append("inline:1: the eight %Cpu values do not sum to 100")
        if vals["us"] + vals["sy"] < 60:                    # G
            fails.append("inline:1: us + sy below 60")
        if vals["wa"] >= 2:                                 # H
            fails.append("inline:1: wa not below 2")
        if vals["st"] != 0.0:                               # A false, E true (steal clock off on defaults, st stays 0.0)
            fails.append("inline:1: st not 0.0")
        runs = [v[3] for _, v in rows]
        k = 0
        avg_seen = False
        for ln in sar.split("\n"):
            f = ln.split()
            if len(f) == 13 and f[1] in ("AM", "PM") and f[2] == "all":
                c = dict(zip(SAR_COLS, (float(x) for x in f[3:])))
            elif len(f) == 12 and f[0] == "Average:" and f[1] == "all":
                avg_seen = True
                c = dict(zip(SAR_COLS, (float(x) for x in f[2:])))
                if abs(sum(c.values()) - 100.0) > 0.011:
                    fails.append("inline:2: Average row does not sum to 100")
                continue
            else:
                continue
            if abs(sum(c.values()) - 100.0) > 0.011:
                fails.append(f"inline:2 row {k}: columns do not sum to 100")
            mean_run = sum(runs[3 * k:3 * k + 3]) / 3 / 800
            if c["%usr"] + c["%sys"] < mean_run + 5:        # G
                fails.append(f"inline:2 row {k}: %usr + %sys below Run % + 5")
            if c["%iowait"] >= 2:                           # H
                fails.append(f"inline:2 row {k}: %iowait not below 2")
            if c["%steal"] != 0.0:                          # A false, E true
                fails.append(f"inline:2 row {k}: %steal not 0.00")
            k += 1
        if k != 10 or not avg_seen:
            fails.append(f"inline:2: {k} sar rows, Average row {'present' if avg_seen else 'missing'}")
        return fails[:20]
