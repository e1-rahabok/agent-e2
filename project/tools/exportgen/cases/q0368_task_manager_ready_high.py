"""Question 0368: Task Manager shows 100%, vCenter shows Ready about 28%.

Two files: the guest's typeperf (Processor counters, 20 s) and the vCenter
real-time CPU chart of the 4-vCPU VM. The guest counts the time its vCPUs
sat frozen in Ready as busy; vCenter splits it out.

Relations: Run + Ready + Co-stop + Wait = 80,000 ms per sample; Readiness =
Ready / 80,000; Co-stop < Ready; Usage < Run %; typeperf _Total = mean of
the four processors; each typeperf _Total within 3 points of the guest's
busy share (Run + Ready + Co-stop) / 800 of the vCenter sample it ends.
"""

import datetime as dt

from .. import core, formats, relations as rel

VM = "app-win-07"
GUEST = "APP-WIN-07"
VCPUS = 4
ROWS = 30
VC = [f"{m} for {VM}" for m in ("Usage", "Readiness", "Ready", "Run", "Co-stop", "Wait", "Max limited")]
OBJ_P = "Processor"
TP_COLS = [formats.typeperf_name(GUEST, OBJ_P, str(k), "% Processor Time") for k in range(4)] + [
    formats.typeperf_name(GUEST, OBJ_P, "_Total", "% Processor Time"),
    formats.typeperf_name(GUEST, OBJ_P, "_Total", "% Privileged Time"),
    formats.typeperf_name(GUEST, "System", None, "Processor Queue Length"),
]
TOTAL = rel.vcpu_state_total_ms(VCPUS)


@core.register
class TaskManagerReadyHigh(core.Case):
    question_id = "0368"
    seed = 368
    f_tp = "typeperf-processor.csv"
    f_vc = "vcenter-vm-cpu-realtime.csv"

    def generate(self, seed=None):
        rng = core.make_rng(self.seed if seed is None else seed, "task-manager")
        start = core.DEFAULT_START
        target = core.bounded_walk(rng, ROWS, 28, 1.5, 23, 34)
        vc_rows, busy = [], []
        for i in range(ROWS):
            ready = round(rel.ready_ms_from_readiness(target[i], VCPUS))
            while True:
                costop = rng.randint(400, 1600)
                wait = rng.randint(800, 2800)
                run = TOTAL - ready - costop - wait
                if 40000 <= run <= 60000 and costop < ready:
                    break
            readiness = round(rel.readiness_pct(ready, VCPUS), 2)
            usage = round(rel.ms_to_pct(run / VCPUS) * rng.uniform(0.82, 0.92), 2)
            vc_rows.append((start + dt.timedelta(seconds=20 * (i + 1)),
                            [usage, readiness, ready, run, costop, wait, 0]))
            busy.append((run + ready + costop) / 800)
        tp_rows = [(start, [None] * 6 + [3])]
        for j in range(1, ROWS + 1):
            base = busy[j - 1]
            procs = [core.clamp(base + rng.gauss(0, 1.5), 90, 100) for _ in range(4)]
            total = sum(procs) / 4
            priv = rng.uniform(2.5, 6.0)
            q = rng.choices([0, 1, 2, 3], weights=[0.2, 0.35, 0.3, 0.15])[0]
            tp_rows.append((start + dt.timedelta(seconds=20 * j), procs + [total, priv, q]))
        return {self.f_tp: formats.typeperf_csv(TP_COLS, tp_rows, "Coordinated Universal Time", 0),
                self.f_vc: formats.vcenter_csv(VC, vc_rows)}

    def check(self, files):
        try:
            tcols, trows = formats.parse_typeperf_csv(files[self.f_tp])
            vcols, vrows = formats.parse_vcenter_csv(files[self.f_vc])
        except (KeyError, ValueError, IndexError) as e:
            return [f"parse: {e}"]
        if tcols != TP_COLS or vcols != VC:
            return ["columns differ"]
        fails = []
        if len(trows) != ROWS + 1 or len(vrows) != ROWS:
            return [f"row counts {len(trows)} / {len(vrows)}"]
        first = trows[0][1]
        if any(v is not None for v in first[:6]):
            fails.append("typeperf first row must print blank for the rate counters")
        mins, maxs = [], []
        for i, (t, v) in enumerate(vrows):
            usage, readiness, ready, run, costop, wait, maxlim = v
            if rel.state_sum_ms(run, ready, costop, wait) != TOTAL:
                fails.append(f"vcenter row {i}: state sum {rel.state_sum_ms(run, ready, costop, wait)}")
            if abs(readiness - rel.readiness_pct(ready, VCPUS)) > 0.006:
                fails.append(f"vcenter row {i}: Readiness {readiness} vs Ready")
            if not costop < ready:
                fails.append(f"vcenter row {i}: Co-stop not below Ready")
            if not usage < rel.ms_to_pct(run / VCPUS):
                fails.append(f"vcenter row {i}: Usage not below Run %")
            if min(v) < 0:
                fails.append(f"vcenter row {i}: negative value")
            if maxlim != 0:                                   # J
                fails.append(f"vcenter row {i}: Max limited {maxlim}")
            if run + ready < 75000 or wait > 3000:           # B
                fails.append(f"vcenter row {i}: Run + Ready {run + ready}, Wait {wait}")
            if run >= 64000 or run / 800 > 75:               # C, A
                fails.append(f"vcenter row {i}: Run {run}")
            if not 22 <= readiness <= 35:                    # D
                fails.append(f"vcenter row {i}: Readiness {readiness} outside 22-35")
            if vrows[i][0] != trows[i + 1][0].replace(tzinfo=dt.timezone.utc):
                fails.append(f"row {i}: time stamps of the two files differ")
            tv = trows[i + 1][1]
            procs, tot, priv, queue = tv[:4], tv[4], tv[5], tv[6]
            if abs(tot - sum(procs) / 4) > 0.01:
                fails.append(f"typeperf row {i + 1}: _Total != mean")
            if not priv < tot:
                fails.append(f"typeperf row {i + 1}: Privileged not below _Total")
            if any(not 90 <= p <= 100 for p in procs):      # E
                fails.append(f"typeperf row {i + 1}: a processor outside 90-100")
            if tot < 90:                                     # A
                fails.append(f"typeperf row {i + 1}: _Total {tot} below 90")
            if abs(tot - (run + ready + costop) / 800) > 3:
                fails.append(f"typeperf row {i + 1}: _Total not within 3 points of the guest-busy share")
            if queue != int(queue) or not 0 <= queue <= 3:
                fails.append(f"typeperf row {i + 1}: queue length {queue}")
        return fails[:20]
