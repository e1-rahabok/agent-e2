"""Question 0376: esxtop CPU panel, VM erp-05 (4 vCPUs) expanded with `e`.

No file. Inline:1 is the panel. Four other VM groups are shown as group rows
only. The erp-05 group row is the sum of its seven worlds.

Relations: vcpu world %WAIT = %VMWAIT + %IDLE; %RUN + %RDY + %CSTP + %WAIT =
100; %USED = %RUN + %SYS - %OVRLP; %SWPWT <= %VMWAIT; group row = sum of its
worlds per column (%VMWAIT: sum over the four vcpu worlds).
"""

from .. import core, formats, relations as rel

VM = "erp-05"
GID = 52817
COLS = ["ID", "GID", "NAME", "NWLD", "%USED", "%RUN", "%SYS", "%WAIT", "%VMWAIT", "%RDY",
        "%IDLE", "%OVRLP", "%CSTP", "%MLMTD", "%SWPWT"]
VALS = COLS[4:]
OTHERS = ["web-31", "web-32", "bld-agent-07", "sql-12"]


def _build(seed):
    rng = core.make_rng(seed, "esxtop-erp")
    u = rng.uniform
    r2 = lambda x: round(x, 2)
    load = [round(b + u(-0.04, 0.04), 2) for b in (1.12, 1.08, 1.03)]
    used = [u(70, 98) for _ in range(16)]
    util = [min(100.0, x * u(0.92, 1.0)) for x in used]
    core_u = [u(92, 100) for _ in range(8)]
    mean = lambda xs: sum(xs) / len(xs)
    summary = formats.esxtop_cpu_summary(used, util, core_u, mean(used), mean(util), mean(core_u))
    status = formats.esxtop_status_line("3:42:18pm", "88 days 06:12", 1104, 5, 22, formats.esxtop_cpu_tail(load))
    ids = rng.sample(range(20000, 60000), 4)
    rows = []
    for gid, name in zip(ids, OTHERS):
        nw = rng.randint(5, 9)
        run, rdy, cstp = r2(u(20, 160)), r2(u(2, 15)), r2(u(0.2, 6))
        sys_, ovrlp = r2(u(0.2, 3)), r2(u(0.1, 1.5))
        wait = r2(100 * nw - run - rdy - cstp)
        vmwait = r2(u(1, 6))
        rows.append((gid, gid, name, nw, r2(run + sys_ - ovrlp), run, sys_, wait, vmwait, rdy,
                     r2(wait * u(0.8, 0.95)), ovrlp, cstp, 0.0, 0.0))
    worlds = []   # (id, name, values for VALS)
    worlds.append((GID + 1, "vmx", None))
    for k in range(4):
        run, rdy = r2(u(35, 45)), r2(u(3, 8))
        cstp = r2(u(0.60, 1.50) if k == 2 else u(0.10, 0.45))
        wait = r2(100 - run - rdy - cstp)
        swpwt = r2(u(0.80, 2.50))
        vmwait = r2(swpwt + u(0.50, 3.00))
        idle = r2(wait - vmwait)
        sys_, ovrlp = r2(u(0.30, 1.20)), r2(u(0.20, 0.80))
        worlds.append((GID + 2 + k, f"vmx-vcpu-{k}:{VM}",
                       [r2(run + sys_ - ovrlp), run, sys_, wait, vmwait, rdy, idle, ovrlp, cstp, 0.0, swpwt]))
    worlds.append((GID + 6, f"vmx-mks:{VM}", None))
    worlds.append((GID + 7, f"vmx-svga:{VM}", None))
    full = []
    for wid, name, v in worlds:
        if v is None:
            run, rdy = r2(u(0.02, 0.30)), r2(u(0.0, 0.03))
            v = [run, run, 0.0, r2(100 - run - rdy), None, rdy, 0.0, 0.0, 0.0, 0.0, 0.0]
        full.append((wid, name, v))
    group = []
    for c in range(len(VALS)):
        group.append(r2(sum(v[c] for _, _, v in full if v[c] is not None)))
    rows.append((GID, GID, VM, len(full), *group))
    for wid, name, v in full:
        rows.append((wid, GID, name, 1, *v))
    return formats.esxtop_panel("c", status, rows, summary)


@core.register
class EsxtopVcpuCouldNotRun(core.Case):
    question_id = "0376"
    seed = 376

    def generate(self, seed=None):
        return {}

    def generate_inline(self, seed=None):
        return {1: _build(self.seed if seed is None else seed)}

    def check(self, files):
        return []

    def check_inline(self, blocks, files):
        try:
            head, rows = formats.parse_esxtop_panel(blocks.get(1, ""), "c")
        except ValueError as e:
            return [f"inline:1: {e}"]
        if head != COLS:
            return [f"inline:1: header differs: {head}"]
        num = lambda s: None if s == "-" else float(s)
        recs = [dict(zip(head, r)) for r in rows]
        group = [r for r in recs if r["NAME"] == VM and r["ID"] == r["GID"]]
        if len(group) != 1 or group[0]["GID"] != str(GID):
            return ["inline:1: erp-05 group row missing"]
        g = group[0]
        worlds = [r for r in recs if r["GID"] == g["GID"] and r["ID"] != r["GID"]]
        vcpus = [w for w in worlds if "-vcpu-" in w["NAME"]]
        fails = []
        if int(g["NWLD"]) != 7 or len(worlds) != 7 or len(vcpus) != 4:
            fails.append(f"inline:1: {len(worlds)} worlds, {len(vcpus)} vcpu worlds, NWLD {g['NWLD']}")
        if [r["NAME"] for r in recs[:4]] != OTHERS or recs[4]["NAME"] != VM:
            fails.append("inline:1: row order differs (four other VMs, then erp-05 and its worlds)")
        if any(int(w["NWLD"]) != 1 for w in worlds):
            fails.append("inline:1: a world with NWLD != 1")
        for c in VALS:
            vals = [num(w[c]) for w in worlds if num(w[c]) is not None]
            if abs(sum(vals) - num(g[c])) > 0.011 * 7:
                fails.append(f"inline:1: group {c} {g[c]} != sum of worlds {sum(vals):.2f}")
        for r in recs:
            if any(num(r[c]) is not None and num(r[c]) < 0 for c in VALS):
                fails.append(f"inline:1: {r['NAME']}: negative value")
        for w in vcpus:
            n, f = w["NAME"], {c: num(w[c]) for c in VALS}
            if abs(rel.esxtop_wait(f["%VMWAIT"], f["%IDLE"]) - f["%WAIT"]) > 0.011:
                fails.append(f"inline:1: {n}: %WAIT != %VMWAIT + %IDLE")
            if abs(f["%RUN"] + f["%RDY"] + f["%CSTP"] + f["%WAIT"] - 100) > 0.02:
                fails.append(f"inline:1: {n}: RUN + RDY + CSTP + WAIT != 100")
            if abs(f["%USED"] - (f["%RUN"] + f["%SYS"] - f["%OVRLP"])) > 0.02:
                fails.append(f"inline:1: {n}: %USED != RUN + SYS - OVRLP")
            if f["%SWPWT"] > f["%VMWAIT"]:
                fails.append(f"inline:1: {n}: %SWPWT above %VMWAIT")
            if not 2 <= f["%RDY"] <= 10:                                  # A
                fails.append(f"inline:1: {n}: %RDY outside 2-10")
            if f["%OVRLP"] <= 0:                                          # D
                fails.append(f"inline:1: {n}: %OVRLP not above 0")
            if not (f["%WAIT"] >= 40 and f["%WAIT"] - f["%IDLE"] <= 6 and f["%IDLE"] > f["%WAIT"] / 2):   # E
                fails.append(f"inline:1: {n}: %IDLE is not most of %WAIT")
            if f["%SWPWT"] < 0.80:                                        # K false
                fails.append(f"inline:1: {n}: %SWPWT below 0.80")
        if not any(num(w["%CSTP"]) > 0.5 for w in vcpus):                 # B
            fails.append("inline:1: no vcpu world with %CSTP above 0.5")
        if any(num(r["%MLMTD"]) != 0 for r in [g] + worlds):               # H
            fails.append("inline:1: %MLMTD not 0.00 on the erp-05 rows")
        return fails[:20]
