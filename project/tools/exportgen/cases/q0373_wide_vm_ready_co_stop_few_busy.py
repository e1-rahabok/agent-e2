"""Question 0373: a 16-vCPU Linux VM with Ready and Co-stop while a third of it works.

Two VCF Operations List view CSVs (ASSUMED format, see the exportgen README):
the VM's 168 hourly rows (each the mean of 12 five-minute values, 2026-11-09
00:00 to 2026-11-15 23:00 GMT+08:00) and the 9 VMs of its host with their
7-day maximum Ready and Co-stop. inline:1 is `mpstat -P ALL 60 1` from the
guest at a peak hour (2026-11-13 14:16 local).

Relations: Co-stop < Ready in every row (Co-stop = Ready x k, k < 1 at every
5-minute point); the host-file Max for the VM is at least every hourly value;
mpstat rows sum to 100, `all` is the mean of the CPU rows, the Average block
equals the sample block, and the busy CPUs add up to Net Run x 16.
"""

import datetime as dt
import re

from .. import core, formats

TZ = 8
Z = dt.timezone(dt.timedelta(hours=TZ))
START = dt.datetime(2026, 11, 9, 0, 0, tzinfo=Z)
HOURS = 168
VM = "app-java-04"
F1 = "app-java-04-cpu-hourly-7-days.csv"
F2 = "host-vms-cpu-ready-7-days.csv"
C1 = ["CPU|Ready (%)", "CPU|Co-stop (%)", "CPU|Net Run (%)"]
C2 = ["CPU|Ready (%) (Max)", "CPU|Co-stop (%) (Max)"]
OTHERS = [("web-21", 2), ("web-22", 2), ("web-23", 2), ("api-31", 4), ("api-32", 4),
          ("cache-41", 2), ("mq-51", 2), ("batch-61", 4)]
SAMPLE_IDX = 4 * 24 + 14  # 2026-11-13 14:00 local
KERNEL = "5.14.0-427.13.1.el9_4.x86_64"
NCPU = 16
CLOCK = "02:16:01 PM"
DATE = "11/13/2026"
MP_COLS = ["%usr", "%nice", "%sys", "%iowait", "%irq", "%soft", "%steal", "%guest", "%gnice", "%idle"]


def _weight(hour):
    """1 in the peak 10:00-17:59, 0.5 at 09:00 and 18:00, 0 elsewhere."""
    if 10 <= hour <= 17:
        return 1.0
    if hour in (9, 18):
        return 0.5
    return 0.0


def _model(seed):
    """Five-minute points: 2,016 per metric, lists of (netrun, ready, costop)."""
    rng = core.make_rng(seed, "model")
    pts = []
    for i in range(HOURS * 12):
        w = _weight((i // 12) % 24)
        if w == 1.0:
            nr, rd, k = rng.uniform(29, 39), rng.uniform(1.6, 4.5), rng.uniform(0.30, 0.60)
        elif w == 0.0:
            nr, rd, k = rng.uniform(3, 12), rng.uniform(0.2, 0.8), rng.uniform(0.1, 0.5)
        else:
            nr = rng.uniform(core.blend(3, 29, w), core.blend(12, 39, w))
            rd = rng.uniform(core.blend(0.2, 1.6, w), core.blend(0.8, 4.5, w))
            k = rng.uniform(core.blend(0.1, 0.30, w), core.blend(0.5, 0.60, w))
        pts.append((nr, rd, rd * k))
    return pts


def _mpstat(seed, netrun):
    """Per-CPU rows (list of 16 lists of 10 values) whose busy sum matches Net Run x 16 / 100."""
    rng = core.make_rng(seed, "mpstat")
    target = netrun * NCPU / 100
    b = rng.choice([5, 6])
    for attempt in range(4000):
        if attempt == 2000:
            b = 11 - b
        busy_idx = set(rng.sample(range(NCPU), b))
        cpus = []
        for c in range(NCPU):
            if c in busy_idx:
                usr, sys_ = rng.uniform(78, 90), rng.uniform(3, 7)
                steal, soft, iow = rng.uniform(0.3, 2.0), rng.uniform(0.1, 0.6), rng.uniform(0, 0.3)
                usr, sys_, steal, soft, iow = (round(x, 2) for x in (usr, sys_, steal, soft, iow))
                idle = round(100 - usr - sys_ - steal - soft - iow, 2)
                lo, hi = 2, 15
            else:
                usr, sys_ = rng.uniform(1, 8), rng.uniform(0.5, 2)
                steal, soft, iow = rng.uniform(0, 0.3), rng.uniform(0, 0.2), rng.uniform(0, 0.1)
                usr, sys_, steal, soft, iow = (round(x, 2) for x in (usr, sys_, steal, soft, iow))
                idle = round(100 - usr - sys_ - steal - soft - iow, 2)
                lo, hi = 86, 98
            if not lo <= idle <= hi:
                break
            cpus.append([usr, 0.0, sys_, iow, 0.0, soft, steal, 0.0, 0.0, idle])
        else:
            s = sum((100 - c[9]) / 100 for c in cpus)
            if target - 0.2 <= s <= target + 0.8:
                return cpus
    raise RuntimeError("no mpstat sample matches Net Run")


@core.register
class Q0373(core.Case):
    question_id = "0373"
    seed = 373

    def _hourly(self, seed):
        pts = _model(seed)
        rows = []
        for h in range(HOURS):
            chunk = pts[h * 12:(h + 1) * 12]
            m = [sum(p[k] for p in chunk) / 12 for k in range(3)]
            rows.append((formats.vcf_time(START + dt.timedelta(hours=h), TZ), [m[1], m[2], m[0]]))
        return pts, rows

    def generate(self, seed=None):
        seed = self.seed if seed is None else seed
        pts, rows = self._hourly(seed)
        rng = core.make_rng(seed, "host")
        host = [(VM, [max(p[1] for p in pts), max(p[2] for p in pts)])]
        for name, vcpus in OTHERS:
            cs = rng.uniform(0.0, 0.05) if vcpus == 2 else rng.uniform(0.0, 0.12)
            host.append((name, [rng.uniform(0.08, 0.45), cs]))
        host.sort(key=lambda r: -r[1][0])
        return {F1: formats.vcf_list_csv(C1, rows, name_header="Time"),
                F2: formats.vcf_list_csv(C2, host, name_header="Name")}

    def generate_inline(self, seed=None):
        seed = self.seed if seed is None else seed
        _, rows = self._hourly(seed)
        netrun = round(rows[SAMPLE_IDX][1][2], 4)
        cpus = _mpstat(seed, netrun)
        allrow = [round(sum(c[k] for c in cpus) / NCPU, 2) for k in range(10)]
        per_cpu = [allrow] + cpus
        return {1: formats.mpstat_all(KERNEL, VM, DATE, NCPU, CLOCK, per_cpu, per_cpu)}

    def check(self, files):
        fails = []
        try:
            c1, r1 = formats.parse_vcf_list_csv(files[F1])
            c2, r2 = formats.parse_vcf_list_csv(files[F2])
        except (KeyError, ValueError, IndexError) as e:
            return [f"parse: {e}"]
        if c1 != C1 or c2 != C2:
            return ["columns differ"]
        if len(r1) != HOURS or len(r2) != 9:
            return [f"row counts {len(r1)} / {len(r2)}, expected {HOURS} / 9"]
        t0 = formats.parse_vcf_time(r1[0][0])
        if t0 != START:
            fails.append(f"first hour {t0} is not {START}")
        for i, (label, (rd, cs, nr)) in enumerate(r1):
            t = formats.parse_vcf_time(label)
            if t != START + dt.timedelta(hours=i):
                fails.append(f"row {i}: time {label} off the hourly axis")
                break
            if min(rd, cs, nr) < 0 or nr > 100:
                fails.append(f"row {i}: value out of range")
            if not cs < rd:                                         # F
                fails.append(f"F: row {label}: Co-stop {cs} not below Ready {rd}")
            if 10 <= t.hour <= 17:
                if not 1.5 <= rd <= 4.0 or not 0.5 <= cs <= 2.0:
                    fails.append(f"F: peak row {label}: Ready {rd}, Co-stop {cs} outside the ranges")
                if not 28 <= nr <= 40:                              # I
                    fails.append(f"I: peak row {label}: Net Run {nr} outside 28-40")
        names = [n for n, _ in r2]
        if len(set(names)) != 9 or names[0] != VM:
            fails.append("host file: names not unique or VM not first")
        mx = [v[0] for _, v in r2]
        if mx != sorted(mx, reverse=True):
            fails.append("host file is not sorted by Ready (Max) descending")
        top = dict(r2)[VM]
        if not 2 < top[0] <= 6:                                     # G
            fails.append(f"G: VM Ready Max {top[0]} not in (2, 6]")
        if top[0] < max(r[1][0] for r in r1) or top[1] < max(r[1][1] for r in r1):
            fails.append("VM Max is below an hourly value")
        for n, v in r2:
            if n != VM and not v[0] < 0.5:
                fails.append(f"G: {n} Ready Max {v[0]} is not below 0.5")
            if n != VM and v[1] > 0.12:
                fails.append(f"{n}: Co-stop Max {v[1]} above 0.12")
        return fails[:20]

    def check_inline(self, blocks, files):
        text = blocks.get(1)
        if text is None:
            return ["inline:1 missing"]
        lines = text.split("\n")
        fails = []
        if not lines[0].startswith(f"Linux {KERNEL} ({VM})") or f"({NCPU} CPU)" not in lines[0]:
            fails.append("banner differs")
        sample, average, cur = [], [], None
        for ln in lines[1:]:
            f = ln.split()
            if not f:
                continue
            if "CPU" in f and "%idle" in f:
                cur = average if f[0] == "Average:" else sample
                continue
            idx = 1 if f[0] == "Average:" else 2
            cur.append((f[idx], [float(x) for x in f[idx + 1:]]))
        if sample != average:
            fails.append("Average block differs from the sample block")
        if [n for n, _ in sample] != ["all"] + [str(i) for i in range(NCPU)]:
            return fails + ["sample block rows are not all, 0..15"]
        allrow, cpus = sample[0][1], [v for _, v in sample[1:]]
        for n, v in sample:
            if abs(sum(v) - 100) > 0.05:
                fails.append(f"CPU {n}: columns sum to {sum(v):.2f}")
        for k in range(10):
            if abs(sum(c[k] for c in cpus) / NCPU - allrow[k]) > 0.011:
                fails.append(f"all row column {MP_COLS[k]} is not the mean of the CPU rows")
        busy = [c for c in cpus if c[9] < 20]
        if len(busy) not in (5, 6) or any(c[9] <= 80 for c in cpus if c[9] >= 20):   # A
            fails.append("A: not 5 or 6 CPUs with %idle < 20 and the others > 80")
        for c in busy:
            if not (78 <= c[0] <= 90 and c[4] == 0):
                fails.append("busy CPU outside the template ranges")
                break
        if files and F1 in files:
            _, r1 = formats.parse_vcf_list_csv(files[F1])
            row = next((r for r in r1 if formats.parse_vcf_time(r[0]) == dt.datetime(2026, 11, 13, 14, 0, tzinfo=Z)), None)
            if row is None:
                fails.append("I: hour 2026-11-13 14:00 not in the hourly file")
            else:
                s = sum((100 - c[9]) / 100 for c in cpus)
                t = row[1][2] * 0.16
                if abs(s - t) > 1.0 or s < t - 0.2:                  # I
                    fails.append(f"I: busy CPUs {s:.2f} vs Net Run x 16 = {t:.2f}")
        return fails[:20]
