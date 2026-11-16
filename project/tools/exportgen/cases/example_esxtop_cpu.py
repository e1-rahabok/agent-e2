"""Example 2: esxtop CPU panel, one 4-vCPU VM expanded into its worlds.

Not a real question. Relations kept:
  group row = sum of its worlds (every column)
  vCPU world: %WAIT = %VMWAIT + %IDLE
  vCPU world: %RUN + %RDY + %CSTP + %WAIT = 100
Non-vCPU worlds (vmx, mks) show '-' in %VMWAIT, and are small.
"""

from .. import core, formats, relations as rel

VM = "web-demo-01"
GID = 41233
VCPUS = 4
COLS = ["%USED", "%RUN", "%SYS", "%WAIT", "%VMWAIT", "%RDY", "%IDLE", "%OVRLP", "%CSTP", "%MLMTD", "%SWPWT"]
SUMMED = [c for c in COLS if c != "%VMWAIT"]  # %VMWAIT is '-' on non-vCPU worlds; summed over vCPU worlds


@core.register
class ExampleEsxtopCpu(core.Case):
    question_id = "example-2"
    seed = 102
    filename = "esxtop-cpu.txt"

    def generate(self, seed=None):
        rng = core.make_rng(self.seed if seed is None else seed, "esxtop-cpu")
        worlds = []  # (id, name, values list of 11, is_vcpu)
        for v in range(VCPUS):
            run = round(rng.uniform(14, 30), 2)
            rdy = round(rng.uniform(5, 9), 2)
            cstp = round(rng.uniform(0.3, 1.5), 2)
            sys_ = round(rng.uniform(0.1, 0.6), 2)
            wait = round(100 - run - rdy - cstp, 2)
            vmwait = round(rng.uniform(0.2, 1.2), 2)
            idle = round(wait - vmwait, 2)
            ovrlp = round(rng.uniform(0, 0.3), 2)
            used = round(max(0.0, run + sys_ - ovrlp), 2)
            worlds.append((GID + 1 + v, f"vmx-vcpu-{v}:web01", [used, run, sys_, wait, vmwait, rdy, idle, ovrlp, cstp, 0.0, 0.0], True))
        worlds.append((GID + 10, f"vmx", [0.05, 0.08, 0.0, round(99.9, 2), None, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0], False))
        worlds.append((GID + 11, f"mks:web01", [0.01, 0.02, 0.0, round(99.97, 2), None, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], False))
        group = []
        for k, name in enumerate(COLS):
            vals = [w[2][k] for w in worlds if w[2][k] is not None]
            group.append(round(sum(vals), 2))
        rows = [(GID + 5000, GID + 5000, "other-demo-02", 9,
                 0.62, 0.55, 0.02, 902.41, 1.21, 0.14, 801.3, 0.01, 0.0, 0.0, 0.0),
                (GID, GID, VM, len(worlds), *group)]
        for wid, name, vals, _ in worlds:
            rows.append((wid, GID, name, 1, *vals))
        status = formats.esxtop_status_line("11:30:05am", "40 days 02:15", 812, 2, 8,
                                            formats.esxtop_cpu_tail([0.21, 0.19, 0.17]))
        summary = formats.esxtop_cpu_summary([4.1, 3.2, 8.0, 2.2, 5.5, 1.9, 2.4, 3.0],
                                             [6.0, 5.1, 9.2, 4.0, 7.7, 3.1, 4.4, 5.0],
                                             [9.0, 11.2, 8.0, 6.5], 4.1, 6.0, 8.7)
        return {self.filename: formats.esxtop_panel("c", status, rows, summary)}

    def check(self, files):
        try:
            head, rows = formats.parse_esxtop_panel(files[self.filename], "c")
        except (KeyError, ValueError) as e:
            return [f"{self.filename}: {e}"]
        fails = []
        if head[:4] != ["ID", "GID", "NAME", "NWLD"] or head[4:] != COLS:
            return [f"header differs: {head}"]
        recs = [dict(zip(head, r)) for r in rows]
        num = lambda s: None if s == "-" else float(s)
        group = [r for r in recs if r["NAME"] == VM and r["ID"] == r["GID"]]
        if len(group) != 1:
            return ["group row missing"]
        g = group[0]
        worlds = [r for r in recs if r["GID"] == g["GID"] and r["ID"] != r["GID"]]
        if int(g["NWLD"]) != len(worlds):
            fails.append(f"NWLD {g['NWLD']} != {len(worlds)} worlds")
        vcpus = [w for w in worlds if w["NAME"].startswith("vmx-vcpu-")]
        if len(vcpus) != VCPUS:
            fails.append(f"{len(vcpus)} vCPU worlds")
        for c in SUMMED:
            expect = rel.group_sum([[num(w[c])] for w in worlds])[0]
            if abs(expect - num(g[c])) > 0.011:
                fails.append(f"group {c} {g[c]} != sum of worlds {expect:.2f}")
        if abs(sum(num(w["%VMWAIT"]) for w in vcpus) - num(g["%VMWAIT"])) > 0.011:
            fails.append("group %VMWAIT != sum over vCPU worlds")
        for w in vcpus:
            if abs(rel.esxtop_wait(num(w["%VMWAIT"]), num(w["%IDLE"])) - num(w["%WAIT"])) > 0.011:
                fails.append(f"{w['NAME']}: %WAIT != %VMWAIT + %IDLE")
            tot = sum(num(w[c]) for c in ("%RUN", "%RDY", "%CSTP", "%WAIT"))
            if abs(tot - 100.0) > 0.05:
                fails.append(f"{w['NAME']}: RUN+RDY+CSTP+WAIT = {tot:.2f}")
        return fails
