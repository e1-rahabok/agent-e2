"""Question 0375: esxtop CPU panel of a half-busy host with a co-stopped 16-vCPU VM.

inline:1 is the whole panel (status line, PCPU USED, PCPU UTIL and CORE UTIL
lines, header, rows): one interactive sample, ora-db-07 expanded into its 22
worlds. One socket, 24 cores, Hyper-Threading on (48 PCPUs, one NUMA node), so
the NUMA value and AVG are the same number. No CSV files.

Relations: group row of ora-db-07 = sum of its worlds (printed values); every
vcpu world: %RUN + %RDY + %CSTP + %WAIT = 100, %WAIT = %VMWAIT + %IDLE,
%USED = %RUN + %SYS - %OVRLP; %MLMTD <= %RDY on every row; PCPU UTIL AVG = mean
of the 48 values; CORE UTIL from its two threads.
Key: AVG in [45, 55] while at least 6 vcpu worlds show %CSTP > 2; %MLMTD 0.00
with %RDY > 0; 1-vCPU VMs show %CSTP 0.00.
"""

import re

from .. import core, formats, relations as rel

GID = 41877211
VM = "ora-db-07"
NPCPU = 48
COLS = ["%USED", "%RUN", "%SYS", "%WAIT", "%VMWAIT", "%RDY", "%IDLE", "%OVRLP", "%CSTP", "%MLMTD", "%SWPWT"]
SUMMED = [c for c in COLS if c != "%VMWAIT"]
APPS = [f"app-{n}" for n in range(11, 17)]
SMALL = ["jump-01", "dns-02", "ntp-03"]
NONVM = [("system", 95), ("hostd.2098125", 47), ("vpxa.2098398", 41), ("envoy.2098611", 17), ("esxtop.2561833", 1)]


def _r(x):
    return round(x, 2)


def _vals(used, run, sys_, wait, vmwait, rdy, idle, ovrlp, cstp):
    return [_r(used), _r(run), _r(sys_), _r(wait), None if vmwait is None else _r(vmwait),
            _r(rdy), _r(idle), _r(ovrlp), _r(cstp), 0.0, 0.0]


def _sum_cols(rows):
    """Sum of printed values, column by column; None cells are skipped."""
    return [_r(sum(v[k] for v in rows if v[k] is not None)) for k in range(len(COLS))]


def _ora_worlds(rng):
    worlds = []  # (id, name, values)
    non_vcpu = ["vmx", f"vmast.{GID}", "vmx-vthread-40", "vmx-vthread-41", "vmx-mks:ora-db-", "vmx-svga:ora-db"]
    for i, name in enumerate(non_vcpu):
        run = _r(rng.uniform(0.0, 0.15))
        sys_ = _r(rng.uniform(0.0, 0.05))
        rdy = _r(rng.uniform(0.0, 0.03))
        worlds.append((GID + 1 + i, name,
                       _vals(run + sys_, run, sys_, 100 - run - rdy, None, rdy, 0, 0, 0)))
    big_cstp = set(rng.sample(range(16), 9))
    big_rdy = set(rng.sample(range(16), 7))
    for v in range(16):
        run = _r(rng.uniform(52, 70))
        rdy = _r(rng.uniform(0.5, 3.0) if v in big_rdy else rng.uniform(0.05, 0.45))
        cstp = _r(rng.uniform(2.2, 6.0) if v in big_cstp else rng.uniform(0.8, 2.0))
        sys_ = _r(rng.uniform(0.2, 1.0))
        ovrlp = _r(rng.uniform(0.05, 0.5))
        vmwait = _r(rng.uniform(0.2, 1.5))
        wait = _r(100 - run - rdy - cstp)
        idle = _r(wait - vmwait)
        used = _r(run + sys_ - ovrlp)
        name = f"vmx-vcpu-{v}:ora-" if v < 10 else f"vmx-vcpu-{v}:ora"
        worlds.append((GID + 7 + v, name, _vals(used, run, sys_, wait, vmwait, rdy, idle, ovrlp, cstp)))
    return worlds


def _vm_group(rng, vcpus, run_range, rdy_range, cstp_range, sys_range, ovrlp_range, vmwait_range):
    """Group row of a VM that is not expanded: vcpu worlds plus 5 other worlds in %WAIT."""
    nwld = vcpus + 5
    runs = [_r(rng.uniform(*run_range)) for _ in range(vcpus)]
    run = _r(sum(runs))
    rdy = _r(rng.uniform(*rdy_range))
    cstp = _r(rng.uniform(*cstp_range)) if cstp_range[1] > 0 else 0.0
    sys_ = _r(rng.uniform(*sys_range))
    ovrlp = _r(rng.uniform(*ovrlp_range))
    vmwait = _r(rng.uniform(*vmwait_range))
    wait = _r(100 * nwld - run - rdy - cstp)
    idle = _r(wait - vmwait - 500)
    used = _r(run + sys_ - ovrlp)
    return nwld, _vals(used, run, sys_, wait, vmwait, rdy, idle, ovrlp, cstp)


@core.register
class Q0375(core.Case):
    question_id = "0375"
    seed = 375

    def generate(self, seed=None):
        return {}

    def _build(self, seed):
        rng = core.make_rng(seed, "panel")
        worlds = _ora_worlds(rng)
        group = _sum_cols([w[2] for w in worlds])
        # VMWAIT of the group: vcpu worlds only (None cells skipped by _sum_cols)
        groups = [(GID, GID, VM, len(worlds), group)]
        gid = 41900000
        for name in APPS:
            gid += rng.randint(100000, 400000)
            n, v = _vm_group(rng, 4, (45, 62), (0.1, 1.5), (0.0, 0.3), (0.2, 1.2), (0.05, 0.4), (0.4, 3.0))
            groups.append((gid, gid, name, n, v))
        for name in SMALL:
            gid += rng.randint(100000, 400000)
            n, v = _vm_group(rng, 1, (20, 55), (0.05, 0.6), (0.0, 0.0), (0.05, 0.4), (0.01, 0.1), (0.1, 1.0))
            groups.append((gid, gid, name, n, v))
        for name, nwld in NONVM:
            gid += rng.randint(1000, 90000)
            if name == "system":
                run, rdy = rng.uniform(2, 4), rng.uniform(0.5, 3)
                used = rng.uniform(1, 3)
                sys_ = 0.0
            else:
                run, rdy = rng.uniform(0.01, 1.0), rng.uniform(0.0, 0.2)
                used = run * rng.uniform(0.7, 1.0)
                sys_ = 0.0
            wait = 100 * nwld - run - rdy
            groups.append((gid, gid, name, nwld, _vals(used, run, sys_, wait, None, rdy, 0, 0, 0)))
        groups.sort(key=lambda g: (g[0] != GID, -g[4][0]))
        rows = []
        for gid_, id_, name, nwld, v in groups:
            rows.append((id_, gid_, name, nwld, *v))
            if gid_ == GID:
                for wid, wname, wv in worlds:
                    rows.append((wid, GID, wname, 1, *wv))
        # summary lines
        run_sum = sum(g[4][1] for g in groups if g[2] in [VM] + APPS + SMALL)
        target = run_sum / NPCPU
        mean_t = core.clamp(target + rng.uniform(-3, 3), 46, 54)
        util = [core.clamp(rng.gauss(mean_t, 9), 30, 75) for _ in range(NPCPU)]
        for _ in range(8):
            d = mean_t - sum(util) / NPCPU
            util = [core.clamp(u + d, 30, 75) for u in util]
        util = [round(u, 1) for u in util]
        used_t = [round(u * rng.uniform(0.85, 0.95), 1) for u in util]
        core_u = [round(100 * (1 - (1 - util[2 * c] / 100) * (1 - util[2 * c + 1] / 100)), 1) for c in range(24)]
        avg_u = round(sum(util) / NPCPU, 1)
        avg_used = round(sum(used_t) / NPCPU, 1)
        avg_core = round(sum(core_u) / 24, 1)
        summary = formats.esxtop_cpu_summary(used_t, util, core_u, avg_used, avg_u, avg_core)
        load = sorted(round(rng.uniform(0.48, 0.58), 2) for _ in range(3))
        status = formats.esxtop_status_line("10:42:17am", "63 days 04:11", 903, 10, 43,
                                            formats.esxtop_cpu_tail(load))
        return formats.esxtop_panel("c", status, rows, summary)

    def generate_inline(self, seed=None):
        return {1: self._build(self.seed if seed is None else seed)}

    def check(self, files):
        return []

    def check_inline(self, blocks, files):
        text = blocks.get(1)
        if text is None:
            return ["inline:1 missing"]
        text = text.rstrip("\n") + "\n"
        try:
            head, rows = formats.parse_esxtop_panel(text, "c")
        except ValueError as e:
            return [f"panel: {e}"]
        fails = []
        if head[:4] != ["ID", "GID", "NAME", "NWLD"] or head[4:] != COLS:
            return [f"header differs: {head}"]
        lines = text.split("\n")
        if "\n\n" in text.rstrip("\n"):
            fails.append("blank line inside the panel")
        m = re.match(r"\S+ up .*, (\d+) worlds, (\d+) VMs, (\d+) vCPUs; CPU load average: ([\d., ]+)$", lines[0])
        if not m:
            return ["status line differs"]
        if int(m.group(2)) != 10 or int(m.group(3)) != 43:
            fails.append("status line: expected 10 VMs and 43 vCPUs")
        load = [float(x) for x in m.group(4).split(",")]
        if not all(0.48 <= x <= 0.58 for x in load):
            fails.append(f"CPU load average outside 0.48-0.58: {load}")

        def nums(prefix):
            ln = next((l for l in lines if l.startswith(prefix)), None)
            if ln is None:
                raise ValueError(prefix)
            body, tail = ln[len(prefix):].split(" NUMA:")
            numa, avg = re.match(r"\s*([\d.]+) AVG:\s*([\d.]+)", tail).groups()
            return [float(x) for x in body.split()], float(numa), float(avg)

        try:
            used_t, used_numa, used_avg = nums("PCPU USED(%):")
            util, numa, avg = nums("PCPU UTIL(%):")
            core_u, core_numa, core_avg = nums("CORE UTIL(%):")
        except (ValueError, AttributeError) as e:
            return fails + [f"summary line missing or malformed: {e}"]
        if len(util) != 48 or len(used_t) != 48 or len(core_u) != 24:
            fails.append("PCPU/CORE value counts are not 48/48/24")
            return fails
        if not all(30 <= u <= 75 for u in util):
            fails.append("a PCPU UTIL value is outside 30-75")
        if abs(sum(util) / 48 - avg) > 0.1 or numa != avg:
            fails.append("PCPU UTIL AVG is not the mean of the 48 values")
        if abs(sum(used_t) / 48 - used_avg) > 0.1 or used_numa != used_avg:
            fails.append("PCPU USED AVG is not the mean of the 48 values")
        if any(u > t for u, t in zip(used_t, util)):
            fails.append("a PCPU USED value is above its UTIL")
        for c in range(24):
            exp = 100 * (1 - (1 - util[2 * c] / 100) * (1 - util[2 * c + 1] / 100))
            if abs(exp - core_u[c]) > 0.11:
                fails.append(f"CORE UTIL {c}: {core_u[c]} != {exp:.1f}")
                break
        if abs(sum(core_u) / 24 - core_avg) > 0.1 or core_numa != core_avg:
            fails.append("CORE UTIL AVG is not the mean of the 24 values")

        recs = [dict(zip(head, r)) for r in rows]
        num = lambda s: None if s == "-" else float(s)
        g = [r for r in recs if r["NAME"] == VM and r["ID"] == r["GID"]]
        if len(g) != 1:
            return fails + ["group row of ora-db-07 missing"]
        g = g[0]
        worlds = [r for r in recs if r["GID"] == g["GID"] and r["ID"] != r["GID"]]
        vc = [w for w in worlds if w["NAME"].startswith("vmx-vcpu-")]
        if int(g["NWLD"]) != 22 or len(worlds) != 22 or len(vc) != 16:
            fails.append(f"D: NWLD {g['NWLD']}, {len(worlds)} worlds, {len(vc)} vcpu worlds")
        # the worlds sit directly under the group row
        gi = recs.index(next(r for r in recs if r is not None and r["ID"] == g["ID"] and r["NAME"] == VM))
        if recs[gi + 1:gi + 23] != worlds:
            fails.append("worlds are not directly under the group row")
        for c in SUMMED:
            exp = rel.group_sum([[num(w[c])] for w in worlds])[0]
            if abs(exp - num(g[c])) > 0.01 * 22:
                fails.append(f"group {c} {g[c]} != sum of worlds {exp:.2f}")
        if abs(sum(num(w["%VMWAIT"]) for w in vc) - num(g["%VMWAIT"])) > 0.01 * 22:
            fails.append("group %VMWAIT != sum over vcpu worlds")
        if any(w["%VMWAIT"] != "-" for w in worlds if w not in vc):
            fails.append("a non-vcpu world prints a %VMWAIT value")
        for w in vc:
            if abs(rel.esxtop_wait(num(w["%VMWAIT"]), num(w["%IDLE"])) - num(w["%WAIT"])) > 0.011:
                fails.append(f"{w['NAME']}: %WAIT != %VMWAIT + %IDLE")
            tot = sum(num(w[c]) for c in ("%RUN", "%RDY", "%CSTP", "%WAIT"))
            if abs(tot - 100) > 0.02:
                fails.append(f"{w['NAME']}: RUN+RDY+CSTP+WAIT = {tot:.2f}")
            if abs(num(w["%RUN"]) + num(w["%SYS"]) - num(w["%OVRLP"]) - num(w["%USED"])) > 0.011:
                fails.append(f"{w['NAME']}: %USED != %RUN + %SYS - %OVRLP")
            if num(w["%IDLE"]) < 0:
                fails.append(f"{w['NAME']}: negative %IDLE")
        for r in recs:
            if num(r["%MLMTD"]) > num(r["%RDY"]) + 1e-9:
                fails.append(f"{r['NAME']}: %MLMTD above %RDY")
        order = [num(r["%USED"]) for r in recs if r["ID"] == r["GID"]]
        if order != sorted(order, reverse=True):
            fails.append("group rows are not sorted by %USED descending")
        names = {r["NAME"] for r in recs if r["ID"] == r["GID"]}
        if not set(APPS + SMALL + [VM]) <= names or len(names) != 15:
            fails.append("group rows differ from the host's VMs and the five non-VM groups")
        for n in APPS:
            r = next(r for r in recs if r["NAME"] == n)
            if int(r["NWLD"]) != 9:
                fails.append(f"{n}: NWLD {r['NWLD']} != 9")
        # key conditions
        if not (45 <= numa <= 55 and 45 <= avg <= 55):
            fails.append(f"A: PCPU UTIL NUMA {numa} / AVG {avg} not in 45-55")
        run_sum = sum(num(r["%RUN"]) for r in recs if r["ID"] == r["GID"] and r["NAME"] in [VM] + APPS + SMALL)
        if abs(avg - run_sum / 48) > 6:
            fails.append("PCPU UTIL AVG differs from the VM %RUN sum / 48 by more than 6")
        if sum(1 for w in vc if num(w["%CSTP"]) > 2.0) < 6:
            fails.append("A: fewer than 6 vcpu worlds with %CSTP > 2")
        if not avg < 60:
            fails.append("B: AVG not below 60")
        if num(g["%MLMTD"]) != 0 or any(num(w["%MLMTD"]) != 0 for w in worlds) or not num(g["%RDY"]) > 0:
            fails.append("C: %MLMTD not 0.00 on the group and all worlds, or group %RDY not above 0")
        if sum(1 for w in vc if num(w["%RDY"]) >= 0.5) < 4 or any(not num(w["%RDY"]) > 0 for w in vc):
            fails.append("H: need at least 4 vcpu worlds with %RDY >= 0.5 and every vcpu world %RDY > 0")
        if not num(g["%CSTP"]) > 2:
            fails.append("E, G: group %CSTP not above 2")
        for n in SMALL:
            r = next(r for r in recs if r["NAME"] == n)
            if num(r["%CSTP"]) != 0:
                fails.append(f"F: {n} %CSTP is not 0.00")
        return fails[:20]
