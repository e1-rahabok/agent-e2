"""Question 0387: Linux guest free memory low all week, web-arc-02.

1. VCF Operations list of four Linux VMs (ASSUMED list format, README), 16 GB
   each. Group prefix `Memory|` and `Guest|` as the other list cases.
2. inline:1, a terminal on web-arc-02: uptime, swap counters, PSI memory
   (PSI format ASSUMED: the Photon template kernel had no PSI).
"""

import re

from .. import core, formats

T = 16_777_216
VMS = ["web-arc-01", "web-arc-02", "web-arc-03", "web-arc-04"]
SUBJECT = "web-arc-02"
COLS = ["Memory|Total Capacity (KB) (Last)", "Guest|Free Memory (KB) (Min)", "Guest|Free Memory (KB) (Max)",
        "Guest|Needed Memory (KB) (Min)", "Guest|Needed Memory (KB) (Max)", "Memory|Consumed (KB) (Max)"]
FILE = "vcf-operations-web-vms-memory-7-days.csv"


@core.register
class LinuxFreeMemoryLow(core.Case):
    question_id = "0387"
    seed = 387

    def generate(self, seed=None):
        rng = core.make_rng(self.seed if seed is None else seed, "linux-free")
        rows = []
        for n in VMS:
            if n == SUBJECT:
                fmin, fmax = rng.randint(120_000, 200_000), rng.randint(520_000, 700_000)
                nmin, nmax = T * rng.uniform(0.22, 0.26), T * rng.uniform(0.38, 0.43)
                cons = T * rng.uniform(0.97, 0.99)
            else:
                fmin, fmax = rng.randint(90_000, 260_000), rng.randint(400_000, 900_000)
                nmin, nmax = T * rng.uniform(0.20, 0.30), T * rng.uniform(0.33, 0.47)
                cons = T * rng.uniform(0.95, 0.99)
            rows.append((n, [T, fmin, fmax, round(nmin), round(nmax), round(cons)]))
        return {FILE: formats.vcf_list_csv(COLS, rows)}

    def generate_inline(self, seed=None):
        rng = core.make_rng(self.seed if seed is None else seed, "terminal")
        clock = f"10:{rng.randint(40, 49)}:{rng.randint(0, 59):02d}"
        days, h, m = rng.randint(11, 14), rng.randint(0, 23), rng.randint(0, 59)
        load = ", ".join(f"{rng.uniform(0.20, 0.60):.2f}" for _ in range(3))
        s = rng.randint(900_000, 2_400_000)
        f = round(s * rng.uniform(0.35, 0.55))
        text = (f"$ uptime\n {clock} up {days} days, {h:2d}:{m:02d},  1 user,  load average: {load}\n"
                "$ grep -E '^(pswpin|pswpout) ' /proc/vmstat\n" + formats.vmstat_swap_counters(0, 0)
                + "$ cat /proc/pressure/memory\n" + formats.proc_pressure_memory((0, 0, 0, s), (0, 0, 0, f)))
        return {1: text}

    def check(self, files):
        fails = []
        try:
            cols, rows = formats.parse_vcf_list_csv(files[FILE])
        except (KeyError, ValueError, IndexError) as e:
            return [f"parse: {e}"]
        if cols != COLS or [n for n, _ in rows] != VMS:
            return ["columns or rows differ"]
        for n, (tot, fmin, fmax, nmin, nmax, cons) in rows:
            if not (fmin < fmax and nmin < nmax and nmax + fmax < T and cons <= T and tot == T):
                fails.append(f"{n}: relation broken")
        tot, fmin, fmax, nmin, nmax, cons = dict(rows)[SUBJECT]
        if fmax >= 0.05 * T:
            fails.append("A false / B true: Free Max not below 5%")
        if nmax >= 0.5 * T or nmin < 0.2 * T:
            fails.append("E true: Needed range")
        return fails[:20]

    def check_inline(self, blocks, files):
        t = blocks.get(1, "")
        fails = []
        m = re.search(r"^ \d\d:\d\d:\d\d up (\d+) days,", t, re.M)
        if not m or int(m.group(1)) < 8:
            fails.append("inline:1: uptime shows fewer than 8 days")
        if not re.search(r"^pswpin 0$", t, re.M) or not re.search(r"^pswpout 0$", t, re.M):
            fails.append("inline:1: C: swap counters not 0")
        try:
            psi = formats.parse_pressure(t[t.index("some avg10"):])
        except (ValueError, IndexError):
            return fails + ["inline:1: PSI lines missing"]
        for tag in ("some", "full"):                      # D false: no stall in the last 10 s, minute or 5 minutes
            if any(psi[tag][k] != 0 for k in ("avg10", "avg60", "avg300")):
                fails.append(f"inline:1: PSI {tag} average not 0.00")
        if psi["full"]["total"] > psi["some"]["total"]:
            fails.append("inline:1: PSI full above some")
        return fails
