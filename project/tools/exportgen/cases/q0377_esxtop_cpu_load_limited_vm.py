"""Question 0377: esxtop CPU panel of a fully busy 16-PCPU host, load average
above 3, one VM held back by its own CPU limit (%MLMTD).

esx-c4-12: 16 PCPUs (no Hyper-Threading, Turbo on), 9 VM groups of 72 vCPUs,
six system groups. Every VM group value is the sum over its worlds (vCPU
worlds sum to 100 per world; eight non-vCPU worlds idle). Rows sorted by
%USED. The system group's %WAIT passes 10,000: the cell grows by one
character (formats.esxtop_panel widens it), as real esxtop does.
"""

import re

from .. import core, formats, relations as rel

NPCPU = 16
FILE_NONE = None
# (name, vCPUs)
VMS = [("dw-etl-01", 16), ("app-ora-02", 12), ("web-fe-03", 8), ("web-fe-04", 8), ("api-gw-05", 8),
       ("mq-node-06", 8), ("bld-07", 4), ("bld-08", 4), ("ci-runner-09", 4)]
LIMITED = "dw-etl-01"
COLS = ["%USED", "%RUN", "%SYS", "%WAIT", "%VMWAIT", "%RDY", "%IDLE", "%OVRLP", "%CSTP", "%MLMTD", "%SWPWT"]


def _r(x):
    return round(x, 2)


@core.register
class Q0377(core.Case):
    question_id = "0377"
    seed = 377

    def generate(self, seed=None):
        return {}

    def generate_inline(self, seed=None):
        seed = self.seed if seed is None else seed
        rng = core.make_rng(seed, "cpu")
        f = rng.uniform(1.06, 1.10)
        util = [round(rng.uniform(98.8, 100.0), 1) for _ in range(NPCPU)]
        used = [round(u * (f + rng.uniform(-0.01, 0.01)), 1) for u in util]
        mean_util = sum(util) / NPCPU
        # non-VM groups: (name, nwld, run, rdy, sys, ovrlp)
        nonvm = [("system", 442, rng.uniform(20, 30), rng.uniform(2, 5), rng.uniform(15, 25), rng.uniform(0, 0.1))]
        for nm, nw in (("hostd", 47), ("vpxa", 41), ("envoy", 17), ("sensord", 12)):
            nonvm.append((f"{nm}.{rng.randint(2100000, 2199999)}", nw, rng.uniform(0.1, 1.5), rng.uniform(0.05, 1.0),
                          rng.uniform(0.05, 0.5), rng.uniform(0, 0.1)))
        nonvm.append((f"esxtop.{rng.randint(2100000, 2199999)}", 1, rng.uniform(3, 6), rng.uniform(0.5, 2),
                      rng.uniform(0.3, 1.0), rng.uniform(0, 0.1)))
        # VM groups: draw sys, ovrlp, non-vCPU RUN and the limited VM first
        info = {}
        for name, n in VMS:
            nonrun = [_r(rng.uniform(0.05, 0.3)) for _ in range(8)]
            info[name] = dict(n=n, sys=_r(rng.uniform(0.5, 3)), ovrlp=_r(rng.uniform(0.2, 1.5)), nonrun=nonrun, w=rng.uniform(0.85, 1.15))
        sum_sys_ovrlp = (sum(i["sys"] - i["ovrlp"] for i in info.values())
                         + sum(g[4] - g[5] for g in nonvm))
        # limited VM
        worlds = {}
        etl = []
        for _ in range(16):
            run = _r(rng.uniform(13.5, 15.5))
            cstp = _r(rng.uniform(0.5, 1.5))
            vmw = _r(rng.uniform(0.3, 1.0))
            mlmtd = _r(rng.uniform(68, 75))
            rdy = _r(min(mlmtd + rng.uniform(8, 12), 99.6 - run - cstp - vmw))
            mlmtd = _r(min(mlmtd, rdy - 2))
            idle = _r(100 - run - rdy - cstp - vmw)
            etl.append((run, rdy, cstp, vmw, idle, mlmtd))
        worlds[LIMITED] = etl
        run_etl = sum(w[0] for w in etl) + sum(info[LIMITED]["nonrun"])
        run_nonvm = sum(g[2] for g in nonvm)
        run_nonvcpu = sum(sum(i["nonrun"]) for n, i in info.items() if n != LIMITED)
        budget = NPCPU * mean_util - sum_sys_ovrlp - run_etl - run_nonvm - run_nonvcpu
        others = [(n, v) for n, v in VMS if n != LIMITED]
        denom = sum(info[n]["w"] * v for n, v in others)
        for n, v in others:
            per = budget * info[n]["w"] / denom
            ws = []
            for _ in range(v):
                run = _r(per * rng.uniform(0.98, 1.02))
                cstp = _r(rng.uniform(2, 6) if v >= 8 else rng.uniform(0.5, 2))
                vmw = _r(rng.uniform(0.5, 1.5))
                idle = _r(rng.uniform(0.5, 1.5))
                rdy = _r(100 - run - cstp - vmw - idle)
                ws.append((run, rdy, cstp, vmw, idle, 0.0))
            worlds[n] = ws
        rows = []
        gid = 2104000
        for name, n in VMS:
            i = info[name]
            ws = worlds[name]
            nwld = n + 8
            run = _r(sum(w[0] for w in ws) + sum(i["nonrun"]))
            rdy = _r(sum(w[1] for w in ws))
            cstp = _r(sum(w[2] for w in ws))
            vmw = _r(sum(w[3] for w in ws))
            idle = _r(sum(w[4] for w in ws))
            mlm = _r(sum(w[5] for w in ws))
            wait = _r(100 * nwld - run - rdy - cstp)
            usd = _r((run + i["sys"] - i["ovrlp"]) * f)
            gid += 4001
            rows.append((gid, gid, name, nwld, usd, run, i["sys"], wait, vmw, rdy, idle, i["ovrlp"], cstp, mlm, 0.0))
        for name, nw, run, rdy, sys_, ovrlp in nonvm:
            run, rdy, sys_, ovrlp = _r(run), _r(rdy), _r(sys_), _r(ovrlp)
            gid += 17
            rows.append((gid, gid, name, nw, _r((run + sys_ - ovrlp) * f), run, sys_, _r(100 * nw - run - rdy), None,
                         rdy, 0.0, ovrlp, 0.0, 0.0, 0.0))
        rows.sort(key=lambda r: -r[4])
        load = (sum(r[5] + r[9] - r[13] for r in rows)) / (100 * NPCPU)
        l1 = round(load, 2)
        l5, l15 = round(l1 * rng.uniform(0.97, 0.99), 2), round(l1 * rng.uniform(0.88, 0.93), 2)
        status = formats.esxtop_status_line("10:42:17am", "41 days 03:12", 1458, 9, 72,
                                            formats.esxtop_cpu_tail((l1, l5, l15)))
        au, an = sum(used) / NPCPU, sum(util) / NPCPU
        summary = formats.esxtop_cpu_summary(used, util, [0.0], au, an, 0.0)[:2]
        return {1: formats.esxtop_panel("c", status, rows, summary)}

    def check(self, files):
        return []

    def check_inline(self, blocks, files):
        text = blocks.get(1, "")
        fails = []
        try:
            head, rows = formats.parse_esxtop_panel(text, "c")
        except ValueError as e:
            return [f"inline:1: {e}"]
        if head[:4] != ["ID", "GID", "NAME", "NWLD"] or head[4:] != COLS:
            return [f"inline:1: header differs: {head}"]
        num = lambda s: None if s == "-" else float(s)
        recs = [dict(zip(head, r)) for r in rows]
        m = re.search(r"CPU load average: ([\d.]+), ([\d.]+), ([\d.]+)", text)
        l1 = float(m.group(1))
        if not 3.2 <= l1 <= 4.0 or not 0.69 <= (l1 - 1) / l1 <= 0.75:
            fails.append(f"inline:1: L1 {l1} outside 3.2-4.0 or (L1-1)/L1 outside 0.69-0.75")

        def pcpu(tag):
            ln = next(x for x in text.splitlines() if x.startswith(tag))
            body, avg = ln.split("NUMA:")[0], float(ln.rsplit("AVG:", 1)[1])
            return [float(x) for x in body.split(":", 1)[1].split()], avg
        util, uavg = pcpu("PCPU UTIL(%)")
        used, davg = pcpu("PCPU USED(%)")
        if len(util) != NPCPU or min(util) < 98.5 or not 99 <= uavg <= 100:
            fails.append("inline:1: PCPU UTIL below 98.5 or AVG outside 99-100")
        if not (davg > 100 and uavg <= 100):
            fails.append("inline:1: PCPU USED AVG not above 100 with UTIL AVG at most 100")
        vcpus = vms = 0
        sum_run = sum_used = 0.0
        vmrows = []
        status = text.splitlines()[0]
        if " 9 VMs, 72 vCPUs" not in status:
            fails.append("inline:1: status line is not 9 VMs, 72 vCPUs")
        for r in recs:
            nw = int(r["NWLD"])
            run, rdy, cstp, wait = (num(r[c]) for c in ("%RUN", "%RDY", "%CSTP", "%WAIT"))
            if abs(run + rdy + cstp + wait - 100 * nw) > 0.05:
                fails.append(f"inline:1: {r['NAME']}: RUN+RDY+CSTP+WAIT != 100 x NWLD")
            sys_, ovr, usd = num(r["%SYS"]), num(r["%OVRLP"]), num(r["%USED"])
            f_ = usd / (run + sys_ - ovr)
            if not 1.06 <= f_ <= 1.10 and abs(f_ - 1.08) > 0.02:
                fails.append(f"inline:1: {r['NAME']}: %USED factor {f_:.3f}")
            sum_run += run
            sum_used += usd
            if r["%VMWAIT"] != "-":
                vmrows.append(r)
                if num(r["%VMWAIT"]) + num(r["%IDLE"]) > wait + 0.01 or num(r["%MLMTD"]) > rdy:
                    fails.append(f"inline:1: {r['NAME']}: VMWAIT+IDLE above WAIT or MLMTD above RDY")
        if len(vmrows) != 9:
            fails.append(f"inline:1: {len(vmrows)} VM rows")
        if abs(sum_run - sum(util)) > 0.03 * sum(util):
            fails.append("inline:1: sum of %RUN not within 3% of sum of PCPU UTIL")
        if abs(sum_used - sum(used)) > 0.03 * sum(used):
            fails.append("inline:1: sum of %USED not within 3% of sum of PCPU USED")
        calc = sum(num(r["%RUN"]) + num(r["%RDY"]) - num(r["%MLMTD"]) for r in recs) / (100 * NPCPU)
        if abs(calc - l1) > 0.011:
            fails.append(f"inline:1: load average {l1} != computed {calc:.2f}")
        lim = [r for r in vmrows if num(r["%MLMTD"]) > 0]
        if len(lim) != 1 or lim[0]["NAME"] != LIMITED:
            fails.append("inline:1: not exactly one VM row with %MLMTD > 0 (dw-etl-01)")
        else:
            r = lim[0]
            if not 0.5 * num(r["%RDY"]) < num(r["%MLMTD"]) <= num(r["%RDY"]):
                fails.append("inline:1: %MLMTD not between half of %RDY and %RDY")
            if num(r["%RDY"]) < max(num(x["%RDY"]) for x in vmrows):
                fails.append("inline:1: limited VM does not have the highest %RDY")
        rd = [num(r["%RDY"]) for r in vmrows]
        if max(rd) < 2 * min(rd):
            fails.append("inline:1: highest VM %RDY below 2 x lowest")
        used_col = [num(r["%USED"]) for r in recs]
        if used_col != sorted(used_col, reverse=True):
            fails.append("inline:1: rows not sorted by %USED")
        return fails[:20]
