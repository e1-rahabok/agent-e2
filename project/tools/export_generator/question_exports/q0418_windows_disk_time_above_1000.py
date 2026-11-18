"""Question 0418: Windows % Disk Time above 1,000 % (typeperf) against the vCenter
Virtual disk chart of the same 10 minutes.

fp-app-03, diskspd with 24 requests outstanding on PhysicalDisk 1 E: (scsi0:1).
typeperf: 31 rows at 20 s (row 0 is the first sample of a rate counter: blank).
Per sample: queue Q about 24, guest time per transfer g about 10 ms,
transfers T = Q / g; Avg. Disk Queue Length = T x g; % Disk Time = 100 x that.
vCenter rows: reads about T, Read latency about g less the guest queue wait
(9-10 ms), no outstanding-requests column. typeperf row i pairs with vCenter row i-1.
"""

import datetime as dt

from .. import export_framework, export_formats, counter_relations as rel

HOST = "FP-APP-03"
N = 30
T0 = dt.datetime(2026, 11, 13, 9, 0, 0, tzinfo=export_framework.UTC)
F_TP, F_VC = "typeperf-physicaldisk.csv", "vcenter-vm-virtual-disk-realtime.csv"
INST = "1 E:"
CTRS = ["% Disk Time", "% Idle Time", "Avg. Disk Queue Length", "Current Disk Queue Length", "Disk Transfers/sec",
        "Disk Reads/sec", "Disk Writes/sec", "Avg. Disk sec/Transfer", "Avg. Disk sec/Read"]
TP_COLS = ([export_formats.typeperf_name(HOST, "PhysicalDisk", INST, c) for c in CTRS]
           + [export_formats.typeperf_name(HOST, "Processor", "_Total", "% Processor Time")])
VC_NAMES = ["Average read requests per second", "Average write requests per second", "Read latency",
            "Write latency", "Read rate"]
VC_COLS = [f"{n} for scsi0:1" for n in VC_NAMES]


@export_framework.register
class Q0418(export_framework.QuestionExport):
    question_id = "0418"
    seed = 418

    def generate(self, seed=None):
        seed = self.seed if seed is None else seed
        rng = export_framework.make_rng(seed, "perf")
        tp, vc = [], []
        base = T0 + dt.timedelta(milliseconds=7341)
        tp.append((base, [None, None, None, rng.randint(22, 26), None, None, None, None, None, None]))
        for i in range(1, N + 1):
            t = base + dt.timedelta(seconds=20 * i, milliseconds=rng.randint(-4, 4))
            g = rng.uniform(0.0096, 0.0106)
            q = rng.uniform(23.4, 24.6)
            tr = q / g
            aq = tr * g * rng.uniform(0.99, 1.01)
            tp.append((t, [aq * 100, rng.uniform(0.0, 0.4), aq, rng.randint(21, 27), tr, tr, 0.0, g, g,
                           rng.uniform(8, 18)]))
            reads = round(tr * rng.uniform(0.97, 1.03))
            vc.append((T0 + dt.timedelta(seconds=20 * i), [reads, 0, round(g * 1000 - rng.uniform(0.3, 0.9)), 0, reads * 8]))
        return {F_TP: export_formats.typeperf_csv(TP_COLS, tp, tz_label="Coordinated Universal Time", bias_minutes=0),
                F_VC: export_formats.vcenter_csv(VC_COLS, vc)}

    def check(self, files):
        try:
            tc, tr_ = export_formats.parse_typeperf_csv(files[F_TP])
            vc, vr = export_formats.parse_vcenter_csv(files[F_VC])
        except (KeyError, ValueError) as e:
            return [str(e)]
        if tc != TP_COLS or vc != VC_COLS:
            return ["columns differ"]
        fails = []
        if len(tr_) != N + 1 or len(vr) != N:
            return [f"rows: typeperf {len(tr_)}, vCenter {len(vr)}"]
        if any(abs((b[0] - a[0]).total_seconds() - 20) > 0.02 for a, b in zip(tr_, tr_[1:])):
            fails.append("typeperf step is not 20 s")
        if any((b[0] - a[0]).total_seconds() != 20 for a, b in zip(vr, vr[1:])):
            fails.append("vCenter step is not 20 s")
        col = lambda n: [r[1][TP_COLS.index(export_formats.typeperf_name(HOST, "PhysicalDisk", INST, n))] for r in tr_]
        dtm, idle, aq, cq, tx, rd, wr, st, sr = (col(c) for c in CTRS)
        cpu = [r[1][-1] for r in tr_]
        if any(x is not None for x in (dtm[0], aq[0], tx[0], cpu[0])) or cq[0] is None:
            fails.append("row 0: counters must be blank except Current Disk Queue Length")
        vcol = lambda n: export_formats.column(vc, vr, f"{n} for scsi0:1")
        vreads, vwrites, vlat, vwlat, vrate = (vcol(n) for n in VC_NAMES)
        for i in range(1, N + 1):
            k = f"row {i}"
            if abs(aq[i] - tx[i] * st[i]) > 0.05 * aq[i]:                   # C
                fails.append(f"{k}: C queue != transfers x sec/transfer")
            if abs(dtm[i] - 100 * aq[i]) > 0.01:
                fails.append(f"{k}: % Disk Time != 100 x queue")
            if abs(tx[i] - rd[i] - wr[i]) > 1e-9 or wr[i] != 0 or st[i] != sr[i]:
                fails.append(f"{k}: transfers / reads / writes / sec per transfer relations")
            if dtm[i] < 1000:                                              # A, B
                fails.append(f"{k}: A true, B false: % Disk Time {dtm[i]:.0f} below 1,000")
            if cpu[i] >= 20:                                               # H
                fails.append(f"{k}: H false: % Processor Time {cpu[i]:.1f}")
            j = i - 1
            if vwrites[j] != 0 or abs(vrate[j] / vreads[j] - 8) > 0.1:
                fails.append(f"{k}: G true: vCenter writes or Read rate / reads (8 KB reads, reads only)")
            if abs(st[i] * 1000 - vlat[j]) > 0.15 * st[i] * 1000:           # D, L
                fails.append(f"{k}: D true, L false: guest {st[i] * 1000:.2f} ms vs vCenter {vlat[j]} ms")
            if abs(tx[i] - vreads[j]) > 0.10 * tx[i]:
                fails.append(f"{k}: D true, L false: transfers vs vCenter reads")
            if not 0.80 <= tx[i] * vlat[j] / 1000 / aq[i] <= 1.05:          # I true: the queue is transfers x time below the virtual disk, so halving the time halves it
                fails.append(f"{k}: I: transfers x latency / queue outside 0.80-1.05")
        return fails[:20]
