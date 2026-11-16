"""Question 0413: vmnic Usage above the link speed.

esx-17, Real-time, 45 rows, KBps. vmnic2 receives at 85-95% of a 10 Gb/s link
and transmits 30-60%; Usage = receive + transmit, so it passes the link speed
while neither direction does. Host columns are sums of the four vmnics.
Column order follows the template (grouped by measurement, objects unsorted).
The `esxcli network nic list` block is hand-written; check reads it.
"""

import re

from .. import core, formats, relations as rel

HOST = "esx-17"
N = 45
STEP_S = 20
START = core.DEFAULT_START.replace(year=2026, month=11, day=10, hour=13, minute=40)
FILE = "esx-17-network-real-time.csv"
LINK = rel.mbps_to_kbps(10_000)
ORDER_RX = ["esx-17", "vmnic2", "vmnic0", "vmnic3", "vmnic1"]
ORDER_TX = ["vmnic0", "vmnic2", "vmnic1", "vmnic3", "esx-17"]
ORDER_US = ["vmnic3", "vmnic1", "vmnic2", "esx-17", "vmnic0"]
COLS = ([f"Data receive rate for {o}" for o in ORDER_RX]
        + [f"Data transmit rate for {o}" for o in ORDER_TX]
        + [f"Usage for {o}" for o in ORDER_US])
NICS = ["vmnic0", "vmnic1", "vmnic2", "vmnic3"]


@core.register
class Q0413(core.Case):
    question_id = "0413"
    seed = 413

    def generate(self, seed=None):
        seed = self.seed if seed is None else seed
        rng = core.make_rng(seed, "nic")
        tx2 = core.bounded_walk(rng, N, 550_000, 15_000, 480_000, 620_000)
        rx3 = core.bounded_walk(rng, N, 200_000, 12_000, 150_000, 260_000)
        tx3 = core.bounded_walk(rng, N, 140_000, 10_000, 90_000, 200_000)
        times = core.time_axis(START, N, STEP_S)
        rows = []
        for i, t in enumerate(times):
            rx = {"vmnic2": round(core.clamp(core.noisy(rng, 1_100_000, 0.02), 1_045_000, 1_155_000)),
                  "vmnic3": round(rx3[i]),
                  "vmnic0": rng.randint(20, 90),
                  "vmnic1": rng.randint(0, 6)}
            tx = {"vmnic2": round(tx2[i]), "vmnic3": round(tx3[i]),
                  "vmnic0": rng.randint(10, 70), "vmnic1": rng.randint(0, 6)}
            rx[HOST], tx[HOST] = sum(rx[n] for n in NICS), sum(tx[n] for n in NICS)
            us = {o: rel.vmnic_usage(rx[o], tx[o]) for o in rx}
            vals = ([rx[o] for o in ORDER_RX] + [tx[o] for o in ORDER_TX] + [us[o] for o in ORDER_US])
            rows.append((t, vals))
        return {FILE: formats.vcenter_csv(COLS, rows)}

    def check(self, files):
        try:
            cols, rows = formats.parse_vcenter_csv(files[FILE])
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
        rx = {o: formats.column(cols, rows, f"Data receive rate for {o}") for o in ORDER_RX}
        tx = {o: formats.column(cols, rows, f"Data transmit rate for {o}") for o in ORDER_TX}
        us = {o: formats.column(cols, rows, f"Usage for {o}") for o in ORDER_US}
        for i in range(len(rows)):
            for o in ORDER_RX:
                if us[o][i] != rel.vmnic_usage(rx[o][i], tx[o][i]):     # C true, H false
                    fails.append(f"row {i + 1}: Usage for {o} != receive + transmit")
            if rx[HOST][i] != sum(rx[n][i] for n in NICS):
                fails.append(f"row {i + 1}: host receive != sum of vmnics")
            if tx[HOST][i] != sum(tx[n][i] for n in NICS):
                fails.append(f"row {i + 1}: host transmit != sum of vmnics")
            u, r, x = us["vmnic2"][i], rx["vmnic2"][i], tx["vmnic2"][i]
            if not u > LINK:                      # A true, B false, F false
                fails.append(f"row {i + 1}: Usage for vmnic2 {u} not above link")
            if not 1_040_000 <= r <= 1_159_000:   # D true
                fails.append(f"row {i + 1}: vmnic2 receive {r} outside 1,040,000-1,159,000")
            if not 0.62 <= (u / 2) / LINK <= 0.73:  # E false
                fails.append(f"row {i + 1}: half of Usage / link outside 0.62-0.73")
            if not u > max(r, x):                 # H false
                fails.append(f"row {i + 1}: Usage not above max(receive, transmit)")
            if not 366_000 <= x <= 732_000:       # I false
                fails.append(f"row {i + 1}: vmnic2 transmit {x} outside 366,000-732,000")
        if max(rx["vmnic2"]) >= 1_160_000:        # G
            fails.append("G: max vmnic2 receive not below 1,160,000")
        if max(tx["vmnic2"]) >= min(rx["vmnic2"]):
            fails.append("I: vmnic2 transmit reaches the receive rate")
        return fails[:20]

    def check_inline(self, blocks, files):
        text = blocks.get(1, "")
        ok = any(re.match(r"vmnic2\s", ln) and re.search(r"\s10000\s+Full\s", ln) for ln in text.splitlines())
        return [] if ok else ["inline:1: no vmnic2 line with Speed 10000 and Duplex Full"]
