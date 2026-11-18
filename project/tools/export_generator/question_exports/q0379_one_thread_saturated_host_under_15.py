"""Question 0379: one saturated thread, host under 15%.

1: vCenter real-time chart of host esx-rpt-03 with all 48 CPU instances. One
hot thread (instance 13, then 37 after the job's vCPU moved), its Hyper-
Threading sibling nearly idle, everything else background. The host value is
the mean of the 48 instances.
2: vCenter real-time chart of VM rpt-db-02 (4 vCPUs) with vCPU instances 0-3.
The job's vCPU runs above the 3,000 MHz base clock (Turbo Boost); the VM's
Usage is about 30%.

Inline:1 is the literal PowerCLI text of the question; the check only asserts
it is unchanged.

Relations: host = mean of the 48 instances (+- 0.006); VM Usage in MHz >= sum
of the four vCPUs; Usage = VM MHz / 120 (+- 0.006).
"""

import datetime as dt

from .. import export_framework, export_formats

HOST = "esx-rpt-03"
VM = "rpt-db-02"
ROWS = 30
START = dt.datetime(2026, 11, 10, 1, 20, 0, tzinfo=export_framework.UTC)
HOST_COLS = [f"Utilization for {HOST}"] + [f"Utilization for {k}" for k in range(48)]
VM_COLS = [f"Usage for {VM}", f"Usage in MHz for {VM}"] + [f"Usage in MHz for {k}" for k in range(4)] + \
          [f"Readiness for {VM}"]
LITERAL = """Name                 : esx-rpt-03
ProcessorType        : Intel(R) Xeon(R) Gold 5317 CPU @ 3.00GHz
NumCpu               : 24
CpuTotalMhz          : 71832
HyperthreadingActive : True""".split("\n")


def _hot(i):
    return (13, 12) if i < 18 else (37, 36)


@export_framework.register
class OneThreadSaturated(export_framework.QuestionExport):
    question_id = "0379"
    seed = 379
    f_host = "vcenter-host-cpu-instances-realtime.csv"
    f_vm = "vcenter-vm-cpu-realtime.csv"

    def generate(self, seed=None):
        rng = export_framework.make_rng(self.seed if seed is None else seed, "one-thread")
        offset = [rng.uniform(-1.5, 2.0) for _ in range(48)]
        host_rows, vm_rows = [], []
        for i in range(ROWS):
            t = START + dt.timedelta(seconds=20 * (i + 1))
            hot, sib = _hot(i)
            vals = []
            for k in range(48):
                if k == hot:
                    v = rng.uniform(96.0, 99.8)
                elif k == sib:
                    v = rng.uniform(0.3, 3.0)
                else:
                    v = export_framework.clamp(rng.gauss(4.5, 2.5), 0.3, 14.0) + offset[k]
                    if v < 0.3:
                        v = rng.uniform(0.3, 0.9)
                vals.append(round(v, 2))
            host_rows.append((t, [round(sum(vals) / 48, 2)] + vals))
            cores = [rng.randint(3250, 3550)] + [rng.randint(30, 280) for _ in range(3)]
            mhz = sum(cores) + rng.randint(8, 30)
            vm_rows.append((t, [round(mhz / 120, 2), mhz] + cores + [round(rng.uniform(0.10, 0.70), 2)]))
        return {self.f_host: export_formats.vcenter_csv(HOST_COLS, host_rows),
                self.f_vm: export_formats.vcenter_csv(VM_COLS, vm_rows)}

    def check(self, files):
        try:
            hcols, hrows = export_formats.parse_vcenter_csv(files[self.f_host])
            vcols, vrows = export_formats.parse_vcenter_csv(files[self.f_vm])
        except (KeyError, ValueError, IndexError) as e:
            return [f"parse: {e}"]
        if hcols != HOST_COLS or vcols != VM_COLS:
            return ["columns differ"]
        if len(hrows) != ROWS or len(vrows) != ROWS:
            return [f"{len(hrows)} / {len(vrows)} rows"]
        fails = []
        hots = []
        for i, ((th, h), (tv, v)) in enumerate(zip(hrows, vrows)):
            if th != tv or th != START + dt.timedelta(seconds=20 * (i + 1)):
                fails.append(f"row {i}: time stamps differ or off the 20 s axis")
            host, inst = h[0], h[1:]
            if abs(host - sum(inst) / 48) > 0.006:
                fails.append(f"row {i}: host != mean of the instances")
            if any(not 0 <= x <= 100 for x in h):
                fails.append(f"row {i}: a value outside 0-100")
            if host >= 10:                                     # A true, C false
                fails.append(f"row {i}: host {host} not below 10")
            hot, sib = _hot(i)
            over = [k for k, x in enumerate(inst) if x >= 50]
            if over != [hot]:                                  # B false, H true: one saturated thread per row
                fails.append(f"row {i}: instances at 50 or more {over}, expected only {hot}")
            hots.append(over[0] if over else None)
            if inst[hot] < 95 or inst[sib] > 3.0:
                fails.append(f"row {i}: hot instance {inst[hot]} / sibling {inst[sib]}")
            usage, mhz, c0, c1, c2, c3, ready = v
            if mhz < c0 + c1 + c2 + c3:
                fails.append(f"row {i}: VM MHz below the sum of the vCPUs")
            if abs(usage - mhz / 120) > 0.006:
                fails.append(f"row {i}: Usage != VM MHz / 120")
            if not c0 >= 3250 or not c0 > 3000:               # D false, F true: one vCPU saturated above base
                fails.append(f"row {i}: instance 0 at {c0} MHz")
            if any(c >= 300 for c in (c1, c2, c3)):            # D
                fails.append(f"row {i}: a quiet vCPU at 300 MHz or more")
            if not 25 <= usage <= 36:                          # I false: Usage about 30% hides the saturated vCPU
                fails.append(f"row {i}: VM Usage {usage} outside 25-36")
            if ready >= 1:                                     # E true
                fails.append(f"row {i}: Readiness {ready} not below 1")
        changes = sum(1 for a, b in zip(hots, hots[1:]) if a != b)
        if changes != 1 or hots[0] != 13 or hots[-1] != 37:    # H true: the saturated thread changes once, 13 to 37
            fails.append(f"H: the saturated thread sequence {sorted(set(hots))} changes {changes} times, expected once from 13 to 37")
        for inst_no in (13, 37):                               # B false
            col = export_formats.column(hcols, hrows, f"Utilization for {inst_no}")
            if max(col) < 95:
                fails.append(f"instance {inst_no} never reaches 95")
        return fails[:20]

    def check_inline(self, blocks, files):
        got = [ln.rstrip() for ln in blocks.get(1, "").split("\n")]
        if got != [ln.rstrip() for ln in LITERAL]:
            return ["inline:1: the PowerCLI text differs from the literal text"]
        return []
