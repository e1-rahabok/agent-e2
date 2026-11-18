"""Question 0374: host CPU Usage above 100% (Turbo Boost), host with 64 threads.

1: vCenter real-time chart of host esx-prod-11, the hour up to the alert at
02:10 (180 rows, 01:10:20-02:10:00). Quiet until about 01:55, then busy cores (Core Utilization 91-97.5%), half of the
threads idle (Utilization about 55%), Usage 106-116% (cycles beyond base).
2: VCF Operations list (ASSUMED layout) of the 12 VMs, maximum over the hour.

Relations: Usage >= Core Utilization >= Utilization >= Core Utilization / 2;
Usage in MHz = Usage x 768 (+- 1); Usage > 100 only where Core Utilization
>= 90; Peak vCPU Ready >= Ready and Peak vCPU Co-Stop >= Co-stop; a 1-vCPU
VM has Co-stop 0.
"""

import datetime as dt

from .. import export_framework, export_formats

HOST = "esx-prod-11"
ROWS = 180
START = dt.datetime(2026, 11, 10, 1, 10, 0, tzinfo=export_framework.UTC)   # export ends at the 02:10 alert
BUSY_FROM = dt.datetime(2026, 11, 10, 1, 55, 0, tzinfo=export_framework.UTC)
VC = [f"{m} for {HOST}" for m in ("Usage", "Usage in MHz", "Core Utilization", "Utilization")]
VCF = ["CPU|Usage (%) (Max)", "CPU|Ready (%) (Max)", "CPU|Co-stop (%) (Max)",
       "CPU|Peak vCPU Ready within collection cycle (%) (Max)",
       "CPU|Peak vCPU Co-Stop within collection cycle (%) (Max)"]
VMS = [(f"batch-etl-{n:02d}", 8) for n in range(1, 5)] + [(f"app-web-{n:02d}", 2) for n in range(1, 5)] + \
      [("db-rpt-01", 4), ("db-rpt-02", 4), ("mon-agg-01", 2), ("jump-01", 1)]


@export_framework.register
class HostUsageAbove100(export_framework.QuestionExport):
    question_id = "0374"
    seed = 374
    f_vc = "vcenter-host-cpu-realtime.csv"
    f_vcf = "vcf-operations-host-vms.csv"

    def generate(self, seed=None):
        rng = export_framework.make_rng(self.seed if seed is None else seed, "host-usage")
        w = export_framework.burst_profile(ROWS, 134, 46, ramp=4)      # busy from 01:55:00 (row 134) to the end
        c_quiet = export_framework.bounded_walk(rng, ROWS, 68, 1.5, 62, 75)
        c_busy = export_framework.bounded_walk(rng, ROWS, 95, 1.0, 91, 97.5)
        u_busy = export_framework.bounded_walk(rng, ROWS, 55, 0.8, 52.5, 57.5)
        rows = []
        for i in range(ROWS):
            c = round(export_framework.blend(c_quiet[i], c_busy[i], w[i]), 2)
            u = export_framework.blend(rng.uniform(38, 46), u_busy[i], w[i])
            u = round(export_framework.clamp(u, c / 2 + 0.5, c - 0.5), 2)
            t = export_framework.blend(rng.uniform(1.02, 1.08), rng.uniform(1.13, 1.19), w[i])
            usage = c * t
            if w[i] == 1:
                usage = export_framework.clamp(usage, 106, 116)
            elif c < 90:
                usage = min(usage, 99.9)
            usage = round(usage, 2)
            rows.append((START + dt.timedelta(seconds=20 * (i + 1)), [usage, round(usage * 768), c, u]))
        vcf = []
        for name, vcpus in VMS:
            heavy = name.startswith("batch-etl")
            usage = round(rng.uniform(88, 96) if heavy else rng.uniform(40, 80), 4)
            ready = round(rng.uniform(0.05, 0.45), 4)
            costop = 0.0 if vcpus == 1 else round(rng.uniform(0.0, 0.12), 4)
            pready = round(min(ready * rng.uniform(1.4, 2.0), 0.95), 4)
            pcostop = 0.0 if vcpus == 1 else round(min(costop * rng.uniform(1.5, 3.0), 0.45), 4)
            vcf.append((name, [usage, ready, costop, pready, pcostop]))
        return {self.f_vc: export_formats.vcenter_csv(VC, rows),
                self.f_vcf: export_formats.vcf_list_csv(VCF, vcf)}

    def check(self, files):
        try:
            vcols, vrows = export_formats.parse_vcenter_csv(files[self.f_vc])
            lcols, lrows = export_formats.parse_vcf_list_csv(files[self.f_vcf])
        except (KeyError, ValueError, IndexError) as e:
            return [f"parse: {e}"]
        if vcols != VC or lcols != VCF:
            return ["columns differ"]
        fails = []
        if len(vrows) != ROWS or len(lrows) != len(VMS):
            return [f"{len(vrows)} chart rows, {len(lrows)} list rows"]
        first_over = None
        for i, (t, (usage, mhz, core_u, util)) in enumerate(vrows):
            if t != START + dt.timedelta(seconds=20 * (i + 1)):
                fails.append(f"row {i}: time off the 20 s axis")
            if not usage >= core_u >= util >= core_u / 2:
                fails.append(f"row {i}: Usage >= Core >= Utilization >= Core / 2 broken")
            if abs(mhz - usage * 768) > 1:
                fails.append(f"row {i}: Usage in MHz != Usage x 768")
            if usage > 100 and core_u < 90:
                fails.append(f"row {i}: Usage above 100 with Core Utilization {core_u}")
            if usage > 100 and first_over is None:
                first_over = t
            if t >= BUSY_FROM:                              # A, B false (Turbo, valid reading above 100)
                if not 106 <= usage <= 116 or not usage > core_u:
                    fails.append(f"row {i}: busy Usage {usage}")
                if not 52 <= util <= 58:
                    fails.append(f"row {i}: busy Utilization {util} outside 52-58")
            if usage > 100:                                 # C true: busy cores mostly ran one thread
                one, two = 2 * core_u - 2 * util, 2 * util - core_u     # share of time with one / both threads busy
                if not (90 <= core_u <= 98 and 52 <= util <= 58 and one > 0.5 * core_u and one > 2 * two >= 0):
                    fails.append(f"row {i}: C: one-thread core time {one:.1f} not most of Core Utilization {core_u} (two-thread {two:.1f})")
            if core_u > 98:                                 # C
                fails.append(f"row {i}: Core Utilization {core_u} above 98")
            if util > 58:                                   # D false: never above 75
                fails.append(f"row {i}: Utilization {util} above 58")
        if first_over is None or first_over > dt.datetime(2026, 11, 10, 2, 10, 0, tzinfo=export_framework.UTC):
            fails.append("alert: first Usage above 100 is not at or before 02:10:00")
        if vrows and vrows[-1][0] != dt.datetime(2026, 11, 10, 2, 10, 0, tzinfo=export_framework.UTC):
            fails.append("alert: the export does not end at the 02:10:00 alert")
        for name, (u, rd, cs, prd, pcs) in lrows:
            one = name == "jump-01"
            if prd < rd or pcs < cs or (one and (cs != 0 or pcs != 0)):
                fails.append(f"{name}: peak/base relation broken")
            if not (prd < 1 and pcs < 0.5):                 # F true: VMs rarely waited
                fails.append(f"{name}: peak Ready {prd} or peak Co-Stop {pcs} too high")
        return fails[:20]
