"""Question 0399: esxtop memory panel header of a quiet host (768 GB, high
state) whose MEM overcommit average reads about 0.4-0.5.

Only inline:1 (no CSV): status line with the three overcommit values, PMEM,
VMKMEM, PSHARE, SWAP, ZIP and MEMCTL lines; no MEMTIER (no tiering), no VM table.
The overcommit value is requested memory / managed memory - 1, from a hidden
requested total Q that is not printed.
"""

import re

from .. import core, formats


@core.register
class Q0399(core.Case):
    question_id = "0399"
    seed = 399

    def generate(self, seed=None):
        return {}

    def generate_inline(self, seed=None):
        seed = self.seed if seed is None else seed
        rng = core.make_rng(seed, "mem")
        t = 786_350 + rng.randint(-200, 200)
        vmk = rng.randint(2800, 3200)
        other = rng.randint(300_000, 360_000)
        free = t - vmk - other
        managed = t - rng.randint(300, 500)
        minfree = round(900 + 0.01 * (t - 28_672))
        rsvd = minfree + rng.randint(9000, 15000)
        ursvd = managed - rsvd
        q = managed * (1 + rng.uniform(0.40, 0.50))
        l1 = round(q / managed - 1, 2)
        l5 = round(l1 - rng.uniform(0.0, 0.02), 2)
        l15 = round(l1 - rng.uniform(0.01, 0.04), 2)
        common = rng.randint(900, 1600)
        saving = rng.randint(3500, 6000)
        mx = round(0.6 * other)
        lines = [formats.esxtop_status_line("3:07:44pm", "112 days 06:40", 1311, 38, 164,
                                            "MEM overcommit avg: %.2f, %.2f, %.2f" % (l1, l5, l15))]
        lines += formats.esxtop_mem_summary(t, vmk, other, free, managed, minfree, rsvd, ursvd, "high")
        lines += [f"PSHARE/MB: {common + saving:7d}  shared, {common:7d}  common: {saving:7d} saving",
                  "SWAP  /MB:       0    curr,       0 rclmtgt:                 0.00 r/s,   0.00 w/s",
                  "ZIP   /MB:       0  zipped,       0   saved",
                  f"MEMCTL/MB:       0    curr,       0  target, {mx:7d} max"]
        return {1: "\n".join(lines) + "\n"}

    def check(self, files):
        return []

    def check_inline(self, blocks, files):
        t = blocks.get(1, "")
        fails = []
        m = re.search(r"MEM overcommit avg: ([\d.]+), ([\d.]+), ([\d.]+)", t)
        p = re.search(r"PMEM  /MB:\s+(\d+)\s+total:\s+(\d+)\s+vmk,\s*(\d+) other,\s+(\d+) free", t)
        v = re.search(r"VMKMEM/MB:\s+(\d+) managed:\s+(\d+) minfree,\s+(\d+) rsvd,\s+(\d+) ursvd,\s+(\w+) state", t)
        s = re.search(r"PSHARE/MB:\s+(\d+)\s+shared,\s+(\d+)\s+common:\s+(\d+) saving", t)
        w = re.search(r"SWAP  /MB:\s+(\d+)\s+curr,\s+(\d+) rclmtgt:\s+([\d.]+) r/s,\s+([\d.]+) w/s", t)
        z = re.search(r"ZIP   /MB:\s+(\d+)\s+zipped,\s+(\d+)\s+saved", t)
        c = re.search(r"MEMCTL/MB:\s+(\d+)\s+curr,\s+(\d+)\s+target,\s+(\d+) max", t)
        if not all((m, p, v, s, w, z, c)):
            return ["inline:1: a header line is missing or malformed"]
        if "MEMTIER" in t:
            fails.append("inline:1: MEMTIER line present")
        loads = [float(x) for x in m.groups()]
        if any(not 0.30 <= x <= 0.60 for x in loads):
            fails.append(f"inline:1: overcommit values outside 0.30-0.60: {loads}")
        if max(loads) - min(loads) > 0.05:
            fails.append("inline:1: overcommit values spread above 0.05")
        total, vmk, other, free = (int(x) for x in p.groups())
        managed, minfree, rsvd, ursvd = (int(x) for x in v.groups()[:4])
        if total != vmk + other + free:
            fails.append("inline:1: PMEM total != vmk + other + free")
        if managed > total or rsvd + ursvd != managed or minfree >= rsvd:
            fails.append("inline:1: VMKMEM relations broken")
        if v.group(5) != "high" or not free > 4 * minfree or not free > 0.5 * total:
            fails.append("inline:1: not the high state with free > 4 x minfree and > 0.5 x total")
        if int(s.group(1)) != int(s.group(2)) + int(s.group(3)):
            fails.append("inline:1: PSHARE shared != common + saving")
        if int(w.group(1)) or int(z.group(1)) or int(c.group(1)):
            fails.append("inline:1: SWAP, ZIP or MEMCTL curr not 0")
        return fails
