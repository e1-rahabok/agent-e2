"""Question 0420: VM receive drops that Linux does not count.

ingest-04, Real-time, 90 rows. Receive packets dropped is 0 except two isolated
rows (9, 17) and a 12-minute window (rows 31-66); Linux shows none (inline:1,
generated `ip -s link`; inline:2, the hand-written `ethtool -S` block, is only
checked). Dropped packets are not in Packets received or Data receive rate.
"""

import re

from .. import export_framework, export_formats, counter_relations as rel

VM = "ingest-04"
N = 90
STEP_S = 20
START = export_framework.DEFAULT_START.replace(year=2026, month=11, day=12, hour=6, minute=10)
WIN = (31, 66)          # 1-based, inclusive
ISOLATED = (9, 17)
FILE = "ingest-04-network-real-time.csv"
COLS = [f"{m} for {VM}" for m in (
    "Packets received", "Receive packets dropped", "Data receive rate",
    "Packets transmitted", "Transmit packets dropped", "Data transmit rate")]


@export_framework.register
class Q0420(export_framework.QuestionExport):
    question_id = "0420"
    seed = 420

    def generate(self, seed=None):
        seed = self.seed if seed is None else seed
        rng = export_framework.make_rng(seed, "csv")
        walk = export_framework.bounded_walk(rng, WIN[1] - WIN[0] + 1, 1000, 120, 650, 1600)
        times = export_framework.time_axis(START, N, STEP_S)
        rows = []
        for i, t in enumerate(times):
            r = i + 1
            pps = export_framework.clamp(export_framework.noisy(rng, 20000, 0.03), 19000, 21000)
            rx = round(pps * STEP_S)
            drops = 0
            if WIN[0] <= r <= WIN[1]:
                drops = round(walk[r - WIN[0]] * STEP_S)
            elif r in ISOLATED:
                drops = rng.randint(20, 200)
            rx_size = rng.uniform(980, 1060)
            rx_kbps = round(rel.kbytes_per_s_for_packets(rx / STEP_S, rx_size))
            tx = rng.randint(600, 1400)
            tx_size = rng.uniform(90, 160)
            tx_kbps = round(rel.kbytes_per_s_for_packets(tx / STEP_S, tx_size))
            rows.append((t, [rx, drops, rx_kbps, tx, 0, tx_kbps]))
        return {FILE: export_formats.vcenter_csv(COLS, rows)}

    def generate_inline(self, seed=None):
        seed = self.seed if seed is None else seed
        rng = export_framework.make_rng(seed, "ip")
        rxp = rng.randint(3_100_000_000, 3_400_000_000)
        rxb = round(rxp * rng.uniform(1020, 1040))
        txp = rng.randint(12_000_000, 16_000_000)
        txb = round(txp * rng.uniform(120, 200))
        mc = rng.randint(2000, 20000)
        iface = dict(index=2, name="ens192", flags="BROADCAST,MULTICAST,UP,LOWER_UP", mtu=1500,
                     qdisc="mq", state="UP", kind="ether",
                     rx=(rxb, rxp, 0, 0, 0, mc), tx=(txb, txp, 0, 0, 0, 0))
        return {1: export_formats.ip_s_link([iface])}

    def check(self, files):
        try:
            cols, rows = export_formats.parse_vcenter_csv(files[FILE])
        except (KeyError, ValueError) as e:
            return [f"{FILE}: {e}"]
        if cols != COLS:
            return [f"columns differ: {cols}"]
        fails = []
        if len(rows) != N:
            fails.append(f"{len(rows)} rows, expected {N}")
        if rows[0][0] != START:
            fails.append("first time stamp differs")
        for a, b in zip(rows, rows[1:]):
            if (b[0] - a[0]).total_seconds() != STEP_S:
                fails.append(f"{b[0]}: not {STEP_S} s after the previous row")
        c = lambda n: export_formats.column(cols, rows, f"{n} for {VM}")
        rx, rd, rk = c("Packets received"), c("Receive packets dropped"), c("Data receive rate")
        tx, td, tk = c("Packets transmitted"), c("Transmit packets dropped"), c("Data transmit rate")
        for i in range(len(rows)):
            if any(v is None or v != int(v) for v in (rx[i], rd[i], rk[i], tx[i], td[i], tk[i])):
                fails.append(f"row {i + 1}: non-integer or empty value")
            bpp = rel.bytes_per_packet(rk[i], rx[i] / STEP_S)
            if not 950 <= bpp <= 1100:
                fails.append(f"row {i + 1}: receive bytes per packet {bpp:.0f}")
            bpt = rel.bytes_per_packet(tk[i], tx[i] / STEP_S)
            if not 60 <= bpt <= 200:
                fails.append(f"row {i + 1}: transmit bytes per packet {bpt:.0f}")
            if td[i] != 0:
                fails.append(f"row {i + 1}: Transmit packets dropped {td[i]}")
        # B true (ESXi counts drops Linux does not), H true: one 12-minute run plus two small counts before it
        if sum(d > 0 for d in rd) < 30:
            fails.append("B: fewer than 30 rows with Receive packets dropped > 0")
        run = [i + 1 for i, d in enumerate(rd) if d > 0 and WIN[0] <= i + 1 <= WIN[1]]
        lone = [(i + 1, d) for i, d in enumerate(rd) if d > 0 and not WIN[0] <= i + 1 <= WIN[1]]
        if len(run) != WIN[1] - WIN[0] + 1 or len(lone) != 2 or any(r > WIN[0] or d >= 100 for r, d in lone):
            fails.append(f"H: drops are not one run of rows {WIN} plus two earlier counts under 100: {len(run)} run rows, outside {lone}")
        win = rd[WIN[0] - 1:WIN[1]]
        if min(win) < 13000 or max(win) > 32000:
            fails.append(f"burst drops outside 13,000-32,000: {min(win)}-{max(win)}")
        # I: the worst row loses 3-8.5% of Packets received
        worst = max(d / p for d, p in zip(rd, rx))
        if not 0.03 <= worst <= 0.085:
            fails.append(f"I false: worst drop share {worst:.3f}, expected 0.03-0.085")
        return fails[:20]

    def check_inline(self, blocks, files):
        fails = []
        ip = blocks.get(1, "")
        try:
            d = export_formats.parse_ip_s_link(ip)["ens192"]
            rx, tx = d["RX"], d["TX"]
        except (KeyError, ValueError, IndexError):
            return ["inline:1: cannot parse ip -s link output for ens192"]
        if rx["dropped"] != 0 or rx["errors"] != 0 or rx["missed"] != 0:
            fails.append("inline:1: B true, C false: RX errors, dropped or missed is not 0")
        if tx["dropped"] != 0:
            fails.append("inline:1: TX dropped is not 0")
        if FILE in files:
            _, rows = export_formats.parse_vcenter_csv(files[FILE])
            total = sum(r[1][0] for r in rows)
            if rx["packets"] < total:
                fails.append("inline:1: RX packets below the sum of Packets received")
        eth = blocks.get(2, "")
        if len(re.findall(r"Rx Queue#:", eth)) != 4:
            fails.append("inline:2: not exactly 4 Rx Queue# lines")
        if [int(x) for x in re.findall(r"Rx Queue#:\s*(\d+)", eth)] != [0, 1, 2, 3]:
            fails.append("inline:2: Rx queue indices are not 0-3")
        if len(re.findall(r"pkts rx OOB: 0\s*$", eth, re.M)) != 4:    # D true, A false, F false
            fails.append("inline:2: D: pkts rx OOB is not 0 on four lines")
        if len(re.findall(r"drv dropped rx total: 0\s*$", eth, re.M)) != 4:
            fails.append("inline:2: drv dropped rx total is not 0 on four lines")
        nonzero = [n for ln in eth.splitlines() if ":" in ln and "Queue#" not in ln
                   for n in re.findall(r"\d+", ln.split(":", 1)[1]) if int(n) != 0]
        if nonzero:
            fails.append(f"inline:2: non-zero counter after a colon: {nonzero}")
        return fails
