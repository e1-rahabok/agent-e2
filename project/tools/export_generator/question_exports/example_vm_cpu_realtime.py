"""Example 1: vCenter Real-time VM CPU export, 4 vCPUs, one hour, one burst.

Not a real question. Proves the CSV path: invented VM name, per-row derived
values, a key checked against the re-parsed file.

Columns: Usage, Readiness (%), Ready (ms), Run, Co-stop, Wait (ms, summation
per 20 s sample). Relations kept on every row:
  Run + Ready + Co-stop + Wait = 4 x 20,000 ms
  Readiness = Ready / (4 x 20,000) x 100
Usage is Run / (4 x 20,000) x 100 (the Hyper-Threading charge is not modelled).
"""

from .. import export_framework, export_formats, counter_relations as rel

VM = "web-demo-01"
VCPUS = 4
N = 180            # one hour at 20 s
BURST_START = 100  # sample index
BURST_LEN = 20     # about 6.7 minutes


@export_framework.register
class ExampleVmCpuRealtime(export_framework.QuestionExport):
    question_id = "example-1"
    seed = 101
    filename = "vm-cpu-realtime.csv"

    COLUMNS = [f"{m} for {VM}" for m in ("Usage", "Readiness", "Ready", "Run", "Co-stop", "Wait")]

    def generate(self, seed=None):
        rng = export_framework.make_rng(self.seed if seed is None else seed, "vm-cpu")
        total = rel.vcpu_state_total_ms(VCPUS)
        w = export_framework.burst_profile(N, BURST_START, BURST_LEN)
        busy = export_framework.bounded_walk(rng, N, 0.18, 0.02, 0.08, 0.30)
        times = export_framework.time_axis(export_framework.DEFAULT_START, N, export_framework.INTERVAL_S["realtime"])
        rows = []
        for i, t in enumerate(times):
            ready_frac = export_framework.blend(0.004 + abs(rng.gauss(0, 0.002)), 0.10 + rng.uniform(-0.015, 0.02), w[i])
            run_frac = export_framework.blend(busy[i], 0.55 + rng.uniform(-0.04, 0.04), w[i])
            costop_frac = export_framework.blend(abs(rng.gauss(0, 0.0005)), 0.02 + rng.uniform(0, 0.01), w[i])
            run = round(total * run_frac)
            ready = round(total * ready_frac)
            costop = round(total * costop_frac)
            wait = rel.wait_from_states(VCPUS, run, ready, costop)
            rows.append((t, [round(rel.ms_to_pct(run / VCPUS), 2),
                             round(rel.readiness_pct(ready, VCPUS), 2),
                             ready, run, costop, wait]))
        return {self.filename: export_formats.vcenter_csv(self.COLUMNS, rows)}

    def check(self, files):
        fails = []
        try:
            cols, rows = export_formats.parse_vcenter_csv(files[self.filename])
        except (KeyError, ValueError) as e:
            return [f"{self.filename}: {e}"]
        if cols != self.COLUMNS:
            fails.append(f"columns differ: {cols}")
            return fails
        if len(rows) != N:
            fails.append(f"{len(rows)} rows, expected {N}")
        gaps = {(b[0] - a[0]).total_seconds() for a, b in zip(rows, rows[1:])}
        if gaps != {20.0}:
            fails.append(f"time step is not 20 s: {gaps}")
        c = lambda name: export_formats.column(cols, rows, f"{name} for {VM}")
        usage, readiness, ready, run, costop, wait = (c(n) for n in
                                                     ("Usage", "Readiness", "Ready", "Run", "Co-stop", "Wait"))
        total = rel.vcpu_state_total_ms(VCPUS)
        for i in range(len(rows)):
            s = rel.state_sum_ms(run[i], ready[i], costop[i], wait[i])
            if s != total:
                fails.append(f"row {i}: state sum {s} != {total}")
            if abs(rel.readiness_pct(ready[i], VCPUS) - readiness[i]) > 0.006:
                fails.append(f"row {i}: Readiness {readiness[i]} != Ready/total")
            if abs(rel.readiness_pct(run[i], VCPUS) - usage[i]) > 0.006:
                fails.append(f"row {i}: Usage {usage[i]} != Run/total")
            if min(run[i], ready[i], costop[i], wait[i]) < 0:
                fails.append(f"row {i}: negative state time")
        # the key: Readiness is high inside the burst window and low outside it
        inside = readiness[BURST_START:BURST_START + BURST_LEN]
        outside = readiness[:BURST_START - 3] + readiness[BURST_START + BURST_LEN + 3:]
        if min(inside) < 7.0:
            fails.append(f"burst window Readiness drops to {min(inside)}")
        if max(outside) > 2.0:
            fails.append(f"Readiness above 2 outside the burst: {max(outside)}")
        return fails[:20]
