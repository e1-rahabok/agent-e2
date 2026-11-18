"""Question 0425: a scan held at 250 reads/s of 128 KB by a 1,000 IOPS limit.

rpt-scan-03, Virtual disk view (Real-time, 30 rows) plus inline:1, the esxtop
disk device panel of the same minutes (generated). inline:2 (PowerCLI limits)
is hand-written and left alone. The case device shows low DAVG, KAVG made of
QAVG (the limit queues requests in the kernel), about 16 outstanding.
"""

import re

from .. import export_framework, export_formats, counter_relations as rel

N = 30
STEP_S = 20
START = export_framework.DEFAULT_START.replace(year=2026, month=11, day=14, hour=2, minute=31)
FILE = "vcenter-vm-virtual-disk-realtime.csv"
CASE_DEV = "naa.624a93701c2d3e4f5a6b7c8d00011a07"
NAMES = [("Average read requests per second", "scsi0:1"), ("Read rate", "scsi0:1"), ("Read latency", "scsi0:1"),
         ("Average number of outstanding read requests", "scsi0:1"), ("Average write requests per second", "scsi0:1"),
         ("Write latency", "scsi0:1"), ("Average read requests per second", "scsi0:0"), ("Read latency", "scsi0:0")]
COLS = [f"{n} for {o}" for n, o in NAMES]


@export_framework.register
class Q0425(export_framework.QuestionExport):
    question_id = "0425"
    seed = 425

    def generate(self, seed=None):
        seed = self.seed if seed is None else seed
        rng = export_framework.make_rng(seed, "csv")
        times = export_framework.time_axis(START, N, STEP_S)
        rows = []
        for t in times:
            reads = rng.randint(240, 256)
            rate = round(reads * 128 * rng.uniform(0.997, 1.003))
            out = 15 if rng.random() < 0.15 else 16
            lat = round(out / reads * 1000)
            writes = rng.randint(0, 2)
            wlat = 0 if writes == 0 else rng.randint(0, 2)
            rows.append((t, [reads, rate, lat, out, writes, wlat, rng.randint(5, 25), rng.randint(1, 2)]))
        return {FILE: export_formats.vcenter_csv(COLS, rows)}

    def generate_inline(self, seed=None):
        seed = self.seed if seed is None else seed
        rng = export_framework.make_rng(seed, "esxtop")
        _, rows = export_formats.parse_vcenter_csv(self.generate(seed)[FILE])
        mean_reads = sum(r[1][0] for r in rows) / N
        reads = export_framework.clamp(mean_reads * rng.uniform(0.995, 1.005), 241.0, 255.0)
        writes = rng.uniform(0.0, 0.6)
        cmds = reads + writes
        davg = rng.uniform(0.45, 0.85)
        qavg = rng.uniform(58, 66)
        kavg = qavg + rng.uniform(0.3, 1.5)
        actv = round(cmds * davg / 1000)
        qued = round(cmds * qavg / 1000)
        other_c = rng.uniform(350, 450)
        o_r = other_c * rng.uniform(0.58, 0.62)
        o_w = other_c - o_r
        od, ok = rng.uniform(0.55, 0.80), rng.uniform(0.01, 0.03)
        status = export_formats.esxtop_status_line("2:41:07am", "41 days 03:12", 1214, 18, 64,
                                            export_formats.esxtop_cpu_tail((0.20, 0.19, 0.20)))
        z = 0.0
        rows = [
            ("naa.624a93701c2d3e4f5a6b7c8d00011a02", "-", 64, None, 1, 0, 2 if rng.random() < 0.5 else 1, 0.02,
             other_c, o_r, o_w, o_r * 8 / 1024, o_w * 8 / 1024, od, ok, od + ok, rng.uniform(0.0, 0.01)),
            (CASE_DEV, "-", 64, None, actv, qued, round(actv / 64 * 100), (actv + qued) / 64,
             cmds, reads, writes, reads * 128 / 1024, rng.uniform(0.0, 0.01), davg, kavg, davg + kavg, qavg),
            ("mpx.vmhba32:C0:T0:L0", "-", 1, None, 0, 0, 0, z, z, z, z, z, z, z, z, z, z),
        ]
        return {1: export_formats.esxtop_panel("u", status, rows)}

    def check(self, files):
        try:
            cols, rows = export_formats.parse_vcenter_csv(files[FILE])
        except (KeyError, ValueError) as e:
            return [f"{FILE}: {e}"]
        if cols != COLS:
            return [f"columns differ: {cols}"]
        fails = []
        if len(rows) != N or any((b[0] - a[0]).total_seconds() != STEP_S for a, b in zip(rows, rows[1:])):
            fails.append("rows or 20 s step differ")
        c = lambda n, o: export_formats.column(cols, rows, f"{n} for {o}")
        rq, rate, lat, out = (c(*NAMES[i]) for i in range(4))
        for i in range(len(rows)):
            k = f"row {i + 1}"
            if not 127 <= rate[i] / rq[i] <= 129:
                fails.append(f"{k}: A Read rate / reads {rate[i] / rq[i]:.2f}")
            if not 230 <= rq[i] <= 260:
                fails.append(f"{k}: B/C reads {rq[i]}")
            if lat[i] < 30:
                fails.append(f"{k}: E latency {lat[i]}")
            if abs(rel.outstanding_io(rq[i], lat[i]) - out[i]) > 0.15 * out[i]:
                fails.append(f"{k}: reads x latency differs from outstanding by more than 15%")
        if max(rq) - min(rq) > 20:
            fails.append("B/C: reads not flat (max - min above 20)")
        return fails[:20]

    def check_inline(self, blocks, files):
        fails = []
        try:
            head, rows = export_formats.parse_esxtop_panel(blocks.get(1, ""), "u")
        except ValueError as e:
            return [f"inline:1: {e}"]
        r = next((dict(zip(head, x)) for x in rows if x[0] == CASE_DEV), None)
        if r is None:
            return ["inline:1: case device row missing"]
        if [x[0] for x in rows] != ["naa.624a93701c2d3e4f5a6b7c8d00011a02", CASE_DEV, "mpx.vmhba32:C0:T0:L0"]:
            fails.append("inline:1: device rows or their order differ")
        f = lambda k: float(r[k])
        d, k_, g, q = f("DAVG/cmd"), f("KAVG/cmd"), f("GAVG/cmd"), f("QAVG/cmd")
        if not (d < 1.0 and k_ >= 10 * d and abs(q - k_) <= 0.20 * k_ and abs(g - (d + k_)) <= 0.01):
            fails.append("inline:1: D/I DAVG, KAVG, QAVG, GAVG relations broken")
        if not (int(r["ACTV"]) <= 1 and int(r["DQLEN"]) == 64):
            fails.append("inline:1: H ACTV above 1 or DQLEN not 64")
        if not 230 <= f("READS/s") <= 260 or not 127 <= f("MBREAD/s") * 1024 / f("READS/s") <= 129:
            fails.append("inline:1: READS/s or MBREAD/s outside the expected range")
        if abs(f("CMDS/s") - f("READS/s") - f("WRITES/s")) > 0.011:
            fails.append("inline:1: CMDS/s != READS/s + WRITES/s")
        if FILE in files:
            cols, rows_csv = export_formats.parse_vcenter_csv(files[FILE])
            m = sum(export_formats.column(cols, rows_csv, "Read latency for scsi0:1")) / len(rows_csv)
            if abs(g - m) > 0.15 * m:
                fails.append("inline:1: GAVG/cmd not within 15% of the CSV mean read latency")
        t = blocks.get(2, "")
        if not re.search(r"Hard disk 2\s+1\s+1000\b", t):
            fails.append("inline:2: Hard disk 2 with LimitIOPS 1000 not found")
        return fails
