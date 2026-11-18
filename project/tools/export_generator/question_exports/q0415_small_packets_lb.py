"""Question 0415: a load balancer VM times out at low bandwidth.

lb-web-01, Real-time, 90 rows. Three phases: quiet (rows 1-30, large share of
bytes, fewer packets), peak (rows 31-75, highest packet rate, lowest Data
receive rate) and easing (76-90). Drops occur only at the peak packet rates,
so the rows with drops are not the rows with the highest Data receive rate.
"""

from .. import export_framework, export_formats, counter_relations as rel

VM = "lb-web-01"
N = 90
STEP_S = 20
START = export_framework.DEFAULT_START.replace(year=2026, month=11, day=13, hour=11, minute=0)
FILE = "lb-web-01-network-real-time.csv"
COLS = [f"{m} for {VM}" for m in (
    "Packets received", "Receive packets dropped", "Data receive rate",
    "Packets transmitted", "Transmit packets dropped", "Data transmit rate", "Usage")]
# phase: (first row, last row, pps range, KBps range)
PHASES = [(1, 30, (122_000, 140_000), (27_000, 29_500)),
          (31, 75, (172_000, 190_000), (24_000, 25_500)),
          (76, 90, (145_000, 165_000), (25_500, 27_000))]
DROP_AT = 3_500_000


def _phase(r):
    return next(p for p in PHASES if p[0] <= r <= p[1])


@export_framework.register
class Q0415(export_framework.QuestionExport):
    question_id = "0415"
    seed = 415

    def generate(self, seed=None):
        seed = self.seed if seed is None else seed
        rng = export_framework.make_rng(seed, "lb")
        pps, kbps = [], []
        for a, b, (pl, ph), (kl, kh) in PHASES:
            n = b - a + 1
            pps += export_framework.bounded_walk(rng, n, (pl + ph) / 2, (ph - pl) * 0.06, pl, ph)
            kbps += export_framework.bounded_walk(rng, n, (kl + kh) / 2, (kh - kl) * 0.07, kl, kh)
        times = export_framework.time_axis(START, N, STEP_S)
        rows = []
        for i, t in enumerate(times):
            r = i + 1
            _, _, _, (kl, kh) = _phase(r)
            rx = round(pps[i] * STEP_S)
            k = round(kbps[i])
            for _ in range(50):                     # redraw the KBps when the size leaves 125-250
                size = rel.bytes_per_packet(k, rx / STEP_S)
                if 125 <= size <= 250:
                    break
                k = rng.randint(kl, kh)
            size = rel.bytes_per_packet(k, rx / STEP_S)
            drops = 0
            if rx >= DROP_AT and rng.random() >= 0.2:
                drops = round(rx * rng.uniform(0.003, 0.015))
            tx = round(rx * rng.uniform(0.92, 1.00))
            tx_size = size * rng.uniform(0.95, 1.10)
            tk = round(rel.kbytes_per_s_for_packets(tx / STEP_S, tx_size))
            rows.append((t, [rx, drops, k, tx, 0, tk, rel.vmnic_usage(k, tk)]))
        return {FILE: export_formats.vcenter_csv(COLS, rows)}

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
        for a, b in zip(rows, rows[1:]):                      # A/B/K
            if (b[0] - a[0]).total_seconds() != STEP_S:
                fails.append(f"{b[0]}: not {STEP_S} s after the previous row")
        c = lambda n: export_formats.column(cols, rows, f"{n} for {VM}")
        rx, rd, rk = c("Packets received"), c("Receive packets dropped"), c("Data receive rate")
        tx, td, tk, us = c("Packets transmitted"), c("Transmit packets dropped"), c("Data transmit rate"), c("Usage")
        for i in range(len(rows)):
            n = i + 1
            if any(v is None or v != int(v) for v in (rx[i], rd[i], rk[i], tx[i], td[i], tk[i], us[i])):
                fails.append(f"row {n}: non-integer or empty value")
            if us[i] != rel.vmnic_usage(rk[i], tk[i]):
                fails.append(f"row {n}: Usage != receive + transmit")
            if td[i] != 0:
                fails.append(f"row {n}: Transmit packets dropped {td[i]}")
            if tx[i] > rx[i]:
                fails.append(f"row {n}: Packets transmitted above Packets received")
            if not 2_400_000 <= rx[i] <= 3_800_000:           # C/K
                fails.append(f"row {n}: Packets received {rx[i]} outside 2.4-3.8 million")
            size = rel.bytes_per_packet(rk[i], rx[i] / STEP_S)  # D
            if not 125 <= size <= 250:
                fails.append(f"row {n}: bytes per packet {size:.0f}")
            if rd[i] > 0 and rx[i] < DROP_AT:                 # H
                fails.append(f"row {n}: drops with Packets received below {DROP_AT}")
        if max(us) >= 0.06 * rel.mbps_to_kbps(10_000):        # E/G stem
            fails.append("max Usage is not under 6% of 10 Gb/s")
        drop_rows = [i for i, d in enumerate(rd) if d > 0]
        if len(drop_rows) < 20:
            fails.append(f"H: only {len(drop_rows)} rows with drops")
        elif max(rk[i] for i in drop_rows) >= min(rk[:30]):
            fails.append("H: a drop row has Data receive rate not below every row 1-30")
        if rd[rk.index(max(rk))] != 0:
            fails.append("H: the row with the highest Data receive rate has drops")
        return fails[:20]
