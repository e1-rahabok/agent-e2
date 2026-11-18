"""Question 0436: Windows shows two sockets, one NUMA node; esxtop NUMA fields.

No file. Inline:1 is the literal `coreinfo -s -n` text (hand-written, only
checked). Inline:2 is the esxtop memory panel with the NUMA STATS fields.

Relations on every VM row: CNSM <= GRANT <= MEMSZ; NRMEM + NLMEM = CNSM;
GST_ND0 + GST_ND1 = CNSM; N%L = round(100 x NLMEM / CNSM); the home node's
GST field equals NLMEM; PMEM free = total - vmk - other.
"""

import re

from .. import export_framework, export_formats

COLS = ["GID", "NAME", "MEMSZ", "GRANT", "CNSM", "NHN", "NMIG", "NRMEM", "NLMEM", "N%L",
        "GST_ND0", "OVD_ND0", "GST_ND1", "OVD_ND1"]
TOTAL, VMK, OTHER = 786112, 3210, 612480
FREE = TOTAL - VMK - OTHER
NODE_MB = 393216
KERNEL_VMS = ("hostd", "vpxa")


def _build(seed):
    rng = export_framework.make_rng(seed, "numa-panel")
    gids = rng.sample(range(30000, 90000), 7)
    u = rng.uniform
    r2 = lambda x: round(x, 2)
    rows = []
    # etl-big-02: bigger than one node, steady remote memory
    memsz = grant = 458752.0
    cnsm = r2(grant - u(200, 900))
    nr = r2(458752 - NODE_MB + u(-500, 500))
    nl = r2(cnsm - nr)
    rows.append((gids[0], "etl-big-02", memsz, grant, cnsm, "0", 0, nr, nl, round(100 * nl / cnsm),
                 nl, r2(u(180, 260)), nr, 0.0))
    # sql-prd-04: one home node, all local
    memsz = grant = 98304.0
    cnsm = r2(grant - u(100, 600))
    rows.append((gids[1], "sql-prd-04", memsz, grant, cnsm, "1", 0, 0.0, cnsm, 100,
                 0.0, 0.0, cnsm, r2(u(90, 140))))
    for k, (name, nhn, size, lo) in enumerate((("app-web-11", "1", 16384.0, 14000),
                                               ("app-web-12", "0", 16384.0, 14000),
                                               ("vdi-pool-07", "0", 8192.0, 6000))):
        grant = r2(u(lo, size))
        cnsm = r2(grant - u(50, 400))
        ovd = r2(u(40, 70))
        g0, o0, g1, o1 = (cnsm, ovd, 0.0, 0.0) if nhn == "0" else (0.0, 0.0, cnsm, ovd)
        rows.append((gids[2 + k], name, size, grant, cnsm, nhn, 0, 0.0, cnsm, 100, g0, o0, g1, o1))
    for k, name in enumerate(("hostd.2098385", "vpxa.8526799")):
        m = r2(u(60, 140))
        rows.append((gids[5 + k], name, m, m, r2(m - u(1, 10)), None, None, None, None, None,
                     None, None, None, None))
    status = export_formats.esxtop_status_line("2:14:07pm", "64 days 03:41", 1312, 7, 46,
                                        "MEM overcommit avg: 0.00, 0.00, 0.00")
    summary = export_formats.esxtop_mem_summary(TOTAL, VMK, OTHER, FREE, 782420, 9840, 18110, 762200, "high")
    return export_formats.esxtop_panel("m-numa", status, rows, summary)


@export_framework.register
class TwoSocketsOneNumaNode(export_framework.QuestionExport):
    question_id = "0436"
    seed = 436

    def generate(self, seed=None):
        return {}

    def generate_inline(self, seed=None):
        return {2: _build(self.seed if seed is None else seed)}

    def check(self, files):
        return []

    def check_inline(self, blocks, files):
        fails = []
        cs = blocks.get(1, "")
        socket = re.findall(r"^([*-]+)  Socket (\d)\s*$", cs, re.M)
        numa = re.findall(r"^([*-]+)  NUMA Node (\d+)\s*$", cs, re.M)
        if len(socket) != 2 or any(len(m) != 16 or m.count("*") != 8 for m, _ in socket):
            fails.append("inline:1: expected two socket maps of 16 characters with 8 stars each")
        if len(numa) != 1 or numa[0][0] != "*" * 16:           # A false, C true
            fails.append("inline:1: expected exactly one NUMA Node line with all 16 logical processors")
        if cs.count("NUMA Node") != 2:                          # header line plus the one map line
            fails.append("inline:1: NUMA Node appears more than in the header and one map line")
        try:
            head, rows = export_formats.parse_esxtop_panel(blocks.get(2, ""), "m-numa")
        except ValueError as e:
            return fails + [f"inline:2: {e}"]
        if head != COLS:
            return fails + [f"inline:2: header differs: {head}"]
        pm = re.search(r"PMEM\s+/MB:\s+(\d+)\s+total:\s+(\d+)\s+vmk,\s*(\d+) other,\s+(\d+) free", blocks[2])
        if not pm or int(pm[1]) - int(pm[2]) - int(pm[3]) != int(pm[4]):
            fails.append("inline:2: PMEM free != total - vmk - other")
        recs = {r[1]: dict(zip(head, r)) for r in rows}
        f = lambda s: None if s == "-" else float(s)
        for name, r in recs.items():
            memsz, grant, cnsm = f(r["MEMSZ"]), f(r["GRANT"]), f(r["CNSM"])
            if not cnsm <= grant <= memsz:
                fails.append(f"{name}: CNSM <= GRANT <= MEMSZ broken")
            if name.startswith(("hostd", "vpxa")):
                if any(r[c] != "-" for c in COLS[5:]):
                    fails.append(f"{name}: NUMA fields must be '-'")
                continue
            if not (len(r["NHN"]) == 1 and r["NHN"].isdigit()):
                fails.append(f"{name}: NHN not a single node number")
            nr, nl = f(r["NRMEM"]), f(r["NLMEM"])
            g0, g1 = f(r["GST_ND0"]), f(r["GST_ND1"])
            if abs(nr + nl - cnsm) > 0.011:
                fails.append(f"{name}: NRMEM + NLMEM != CNSM")
            if abs(g0 + g1 - cnsm) > 0.011:
                fails.append(f"{name}: GST_ND0 + GST_ND1 != CNSM")
            if abs(int(r["N%L"]) - round(100 * nl / cnsm)) > 1:
                fails.append(f"{name}: N%L != 100 x NLMEM / CNSM")
            home = g0 if r["NHN"] == "0" else g1
            if abs(home - nl) > 0.011:
                fails.append(f"{name}: home node GST != NLMEM")
        sql, etl = recs.get("sql-prd-04"), recs.get("etl-big-02")
        if not sql or not etl:
            return fails + ["inline:2: sql-prd-04 or etl-big-02 row missing"]
        if sql["NHN"] != "1" or f(sql["NRMEM"]) != 0.0 or int(sql["N%L"]) != 100 or \
                abs(f(sql["NLMEM"]) - f(sql["CNSM"])) > 0.011:          # B true, D false
            fails.append("sql-prd-04: must have one home node, NRMEM 0.00, N%L 100, NLMEM == CNSM")
        if not (f(etl["NRMEM"]) > 0 and int(etl["N%L"]) < 100):       # decoy
            fails.append("etl-big-02: must show remote memory (NRMEM > 0, N%L < 100)")
        if len({r[0] for r in rows}) != len(rows):
            fails.append("inline:2: GIDs not distinct")
        return fails[:20]
