"""Question 0412: esxtop network panel (Mb/s) against the vCenter Real-time
export (KBps) for one iperf3 stream of about 3 Gb/s.

rpt-lnx-14, 60 rows at 20 s. Instances: the VM, its vNIC 4000, vmnic1 (the
team uplink of its port) and vmnic0 (idle); Usage = receive + transmit.
inline:1 is the esxtop network panel of the same minute (generated from the
last CSV row); every PSZ = Mb x 1e6 / 8 / PKT, uplink rows are sums of ports.
"""

import re

from .. import export_framework, export_formats, counter_relations as rel

VM = "rpt-lnx-14"
N = 60
STEP_S = 20
START = export_framework.DEFAULT_START.replace(year=2026, month=11, day=15, hour=13, minute=55)
FILE = "rpt-lnx-14-network-realtime.csv"
BASE_TX = 366_000
RX_ORDER = [VM, "vmnic1", "4000", "vmnic0"]
TX_ORDER = ["vmnic0", "4000", "vmnic1", VM]
US_ORDER = ["vmnic1", VM, "4000", "vmnic0"]
COLS = ([f"Data receive rate for {o}" for o in RX_ORDER] + [f"Data transmit rate for {o}" for o in TX_ORDER]
        + [f"Usage for {o}" for o in US_ORDER])


def vm_series(rng):
    """(rx, tx) per row, KBps integers: idle, ramp, steady."""
    out = []
    for i in range(N):
        if i < 15:
            out.append((rng.randint(1, 30), rng.randint(2, 40)))
        elif i < 17:
            f = (0.4, 0.9)[i - 15]
            out.append((round(7_750 * f * rng.uniform(0.95, 1.05)), round(BASE_TX * f * rng.uniform(0.97, 1.03))))
        else:
            tx = round(BASE_TX * export_framework.clamp(rng.gauss(1, 0.012), 0.97, 1.03))
            out.append((rng.randint(7_500, 8_000), tx))
    return out


@export_framework.register
class Q0412(export_framework.QuestionExport):
    question_id = "0412"
    seed = 412

    def generate(self, seed=None):
        seed = self.seed if seed is None else seed
        rng = export_framework.make_rng(seed, "csv")
        times = export_framework.time_axis(START, N, STEP_S)
        rows = []
        for t, (rx, tx) in zip(times, vm_series(rng)):
            r = {VM: rx, "4000": rx, "vmnic1": rx, "vmnic0": 0}
            x = {VM: tx, "4000": tx, "vmnic1": tx, "vmnic0": 0}
            u = {o: rel.vmnic_usage(r[o], x[o]) for o in r}
            rows.append((t, [r[o] for o in RX_ORDER] + [x[o] for o in TX_ORDER] + [u[o] for o in US_ORDER]))
        return {FILE: export_formats.vcenter_csv(COLS, rows)}

    def generate_inline(self, seed=None):
        seed = self.seed if seed is None else seed
        rng = export_framework.make_rng(seed, "esxtop")
        last_tx = vm_series(export_framework.make_rng(seed, "csv"))[-1][1]
        mb = rel.kbps_to_mbps(last_tx) * (1 + rng.uniform(-0.02, 0.02))
        pkttx = mb * 1e6 / 8 / 1514
        pktrx = pkttx * 0.48
        vm_port = dict(id=100663320, name="2104417:rpt-lnx-14", team="vmnic1", dname="vSwitch1",
                       pkttx=pkttx, mbtx=mb, psztx=1514, pktrx=pktrx, mbrx=pktrx * 66 * 8 / 1e6, pszrx=66)

        def small(pid, name, team, dname, pkt, size):
            ptx = pkt
            prx = ptx * rng.uniform(0.5, 1.1)
            szr = rng.uniform(66, 600)
            return dict(id=pid, name=name, team=team, dname=dname, pkttx=ptx, mbtx=ptx * size * 8 / 1e6,
                        psztx=size, pktrx=prx, mbrx=prx * szr * 8 / 1e6, pszrx=szr)
        ports = [small(100663308, "vmk0", "vmnic0", "vSwitch0", rng.uniform(5, 40), rng.uniform(150, 400)),
                 small(100663309, "vmk1", "vmnic0", "vSwitch0", rng.uniform(0.5, 5), rng.uniform(100, 300))]
        names = ["app-web-21", "app-web-22", "db-rep-05", "ci-agent-03", "mon-col-01"]
        rng.shuffle(names)
        for k in range(rng.randint(4, 6)):
            mbv = 10 ** rng.uniform(-1, 1.47)          # 0.1 - 30 Mb/s
            size = rng.uniform(300, 1400)
            nm = names[k % len(names)] + ("" if k < len(names) else "b")
            ports.append(small(100663330 + k, f"{2104500 + k * 37}:{nm}", rng.choice(["vmnic0", "vmnic1"]),
                               "vSwitch1", mbv * 1e6 / 8 / size, size))
        ports.append(vm_port)
        rows = [(100663303, "Management", "n/a", "vSwitch0", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)]

        def row(p):
            return (p["id"], p["name"], p["team"], p["dname"], p["pkttx"], p["mbtx"], p["psztx"],
                    p["pktrx"], p["mbrx"], p["pszrx"], 0.0, 0.0)
        rows += [row(p) for p in ports]
        for nic, pid in (("vmnic0", 2248146951), ("vmnic1", 2248146952)):
            ps = [p for p in ports if p["team"] == nic]
            s = {k: sum(p[k] for p in ps) for k in ("pkttx", "mbtx", "pktrx", "mbrx")}
            sztx = s["mbtx"] * 1e6 / 8 / s["pkttx"] if s["pkttx"] else 0.0
            szrx = s["mbrx"] * 1e6 / 8 / s["pktrx"] if s["pktrx"] else 0.0
            rows.append((pid, nic, None, "vSwitch0" if nic == "vmnic0" else "vSwitch1",
                         s["pkttx"], s["mbtx"], sztx, s["pktrx"], s["mbrx"], szrx, 0.0, 0.0))
        status = export_formats.esxtop_status_line("2:14:40pm", "63 days 04:21", 1196, 11, 38,
                                            export_formats.esxtop_cpu_tail((0.41, 0.39, 0.37)))
        return {1: export_formats.esxtop_panel("n", status, rows)}

    def check(self, files):
        try:
            cols, rows = export_formats.parse_vcenter_csv(files[FILE])
        except (KeyError, ValueError) as e:
            return [f"{FILE}: {e}"]
        if cols != COLS:
            return [f"columns differ: {cols}"]
        fails = []
        if len(rows) != N:
            fails.append(f"{len(rows)} rows")
        if any((b[0] - a[0]).total_seconds() != STEP_S for a, b in zip(rows, rows[1:])):
            fails.append("time step is not 20 s")
        c = lambda kind, o: export_formats.column(cols, rows, f"{kind} for {o}")
        for i in range(len(rows)):
            for o in RX_ORDER:
                if c("Usage", o)[i] != c("Data receive rate", o)[i] + c("Data transmit rate", o)[i]:
                    fails.append(f"row {i + 1}: Usage != receive + transmit for {o}")
            for kind in ("Data receive rate", "Data transmit rate"):
                if not c(kind, VM)[i] == c(kind, "4000")[i] == c(kind, "vmnic1")[i]:
                    fails.append(f"row {i + 1}: {kind} differs between VM, 4000 and vmnic1")
                if c(kind, "vmnic0")[i] != 0:
                    fails.append(f"row {i + 1}: vmnic0 {kind} not 0")
        tx = c("Data transmit rate", VM)
        if not 340_000 <= tx[-1] <= 390_000:
            fails.append("last transmit outside 340,000-390,000")
        last30 = tx[-30:]
        mean = sum(last30) / 30
        if max(abs(x - mean) for x in last30) > 0.05 * mean:
            fails.append("G false: last 30 rows not within 5% of their mean")
        last3 = sum(tx[-3:]) / 3
        self._mbps_csv = rel.kbps_to_mbps(last3)
        return fails[:20]

    def check_inline(self, blocks, files):
        try:
            head, rows = export_formats.parse_esxtop_panel(blocks.get(1, ""), "n")
        except ValueError as e:
            return [f"inline:1: {e}"]
        fails = []
        recs = [dict(zip(head, r)) for r in rows]
        f = lambda r, k: float(r[k])
        for r in recs:
            for t, p, s in (("MbTX/s", "PKTTX/s", "PSZTX"), ("MbRX/s", "PKTRX/s", "PSZRX")):
                if f(r, p) == 0:
                    if f(r, t) != 0 or f(r, s) != 0:
                        fails.append(f"inline:1: {r['USED-BY']}: zero packets with non-zero size or rate")
                    continue
                lo, hi = (f(r, t) - 0.005) * 1e6 / 8 / f(r, p), (f(r, t) + 0.005) * 1e6 / 8 / f(r, p)
                if not lo * 0.99 - 0.01 <= f(r, s) <= hi * 1.01 + 0.01:
                    fails.append(f"inline:1: {r['USED-BY']}: {s} {r[s]} != {t} x 1e6 / 8 / {p}")
        vm = [r for r in recs if r["USED-BY"].endswith(":" + VM)]
        if len(vm) != 1:
            return fails + ["inline:1: VM port row missing"]
        vm = vm[0]
        if vm["TEAM-PNIC"] != "vmnic1" or vm["PSZTX"] != "1514.00" or vm["%DRPTX"] != "0.00" or vm["%DRPRX"] != "0.00":
            fails.append("inline:1: VM port TEAM-PNIC, PSZTX or drops differ")
        pk = f(vm, "PKTTX/s")
        if not 1400 <= 1e6 / 8 * f(vm, "MbTX/s") / pk <= 1550:     # L true: average packet size near 1,500 bytes
            fails.append("inline:1: L: PKTTX/s and MbTX/s do not give an average packet size near 1,500 bytes")
        mb = f(vm, "MbTX/s")
        if not 2800 <= mb <= 3200:
            fails.append(f"inline:1: VM MbTX/s {mb} outside 2,800-3,200")
        if "files" and FILE in files:
            _, rows_csv = export_formats.parse_vcenter_csv(files[FILE])
            tx = [r[1][COLS.index(f"Data transmit rate for {VM}")] for r in rows_csv]
            if abs(tx[-1] * 8 / 1000 - mb) > 0.1 * mb:                  # C
                fails.append("inline:1: transmit x 8 / 1000 not within 10% of MbTX/s")
            if not 110 <= tx[-1] / mb <= 140:                          # K false (about 125 times larger, not smaller)
                fails.append("inline:1: transmit / MbTX/s outside 110-140")
            if abs(rel.kbps_to_mbps(sum(tx[-3:]) / 3) - mb) > 0.05 * mb:  # B, J, I
                fails.append("inline:1: last-minute mean converted not within 5% of MbTX/s")
        for nic in ("vmnic0", "vmnic1"):
            up = [r for r in recs if r["USED-BY"] == nic]
            if len(up) != 1 or up[0]["TEAM-PNIC"] != "-":
                fails.append(f"inline:1: uplink row {nic} missing or TEAM-PNIC not '-'")
                continue
            ports = [r for r in recs if r["TEAM-PNIC"] == nic]
            for k in ("PKTTX/s", "MbTX/s", "PKTRX/s", "MbRX/s"):
                s = sum(f(r, k) for r in ports)
                if abs(s - f(up[0], k)) > 0.011 * len(ports) + 0.001 * s:
                    fails.append(f"inline:1: {nic} {k} {up[0][k]} != sum of its ports {s:.2f}")
        if not 4 <= len([r for r in recs if ":" in r["USED-BY"] and not r["USED-BY"].endswith(VM)]) <= 6:
            fails.append("inline:1: not 4-6 other VM ports")
        if any(len(r["USED-BY"]) > 30 for r in recs):
            fails.append("inline:1: a name is longer than 30 characters")
        return fails
