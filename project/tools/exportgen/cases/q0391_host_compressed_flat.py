"""Question 0391: host compressed memory flat over 90 days, balloon at zero.

One VCF Operations list (ASSUMED list format, README), four hosts of cluster
cl-east-02, columns First/Last/Min/Max of the 5-minute values over 90 days.
Group prefix `Memory|` as the other list cases (TechDocs prints `Mem|`).
The subject esx-e203 holds about 2 GB compressed, the same value all quarter:
with Compression Rate and Decompression Rate at 0 and no VM moved or powered
off, nothing can add or remove compressed pages (re-review 2026-11-16).
"""

from .. import core, formats

HOSTS = [f"esx-e20{i}.example.com" for i in range(1, 5)]
SUBJECT = "esx-e203.example.com"
COLS = ["Memory|Usage (%) (Min)", "Memory|Usage (%) (Max)", "Memory|Balloon (KB) (Max)",
        "Memory|Compressed (KB) (First)", "Memory|Compressed (KB) (Last)",
        "Memory|Compressed (KB) (Min)", "Memory|Compressed (KB) (Max)",
        "Memory|Compression Rate (KBps) (Max)", "Memory|Decompression Rate (KBps) (Max)"]
FILE = "vcf-operations-cluster-hosts-memory-90-days.csv"


@core.register
class HostCompressedFlat(core.Case):
    question_id = "0391"
    seed = 391

    def generate(self, seed=None):
        rng = core.make_rng(self.seed if seed is None else seed, "compressed")
        rows = []
        for h in HOSTS:
            if h == SUBJECT:
                x = rng.randint(2_000_000, 2_400_000)
                last = x
                v = [round(rng.uniform(58, 64), 4), round(rng.uniform(80, 86), 4), 0, x, last, last, x, 0, 0]
            else:
                v = [round(rng.uniform(52, 65), 4), round(rng.uniform(72, 87), 4), 0, 0, 0, 0, 0, 0, 0]
            rows.append((h, v))
        return {FILE: formats.vcf_list_csv(COLS, rows)}

    def check(self, files):
        fails = []
        try:
            cols, rows = formats.parse_vcf_list_csv(files[FILE])
        except (KeyError, ValueError, IndexError) as e:
            return [f"parse: {e}"]
        if cols != COLS or [n for n, _ in rows] != HOSTS:
            return ["columns or rows differ"]
        for n, v in rows:
            umin, umax, bal, first, last, cmin, cmax, comp, dec = v
            if not (cmin <= first <= cmax and cmin <= last <= cmax) or not umin < umax <= 100 or min(v) < 0:
                fails.append(f"{n}: relation broken")
            if dec != 0:
                fails.append(f"E, G: {n} Decompression Rate Max not 0")
        v = dict(rows)[SUBJECT]
        umin, umax, bal, first, last, cmin, cmax, comp, dec = v
        if bal != 0 or cmin < 512_000 or umax >= 90:
            fails.append("A (balloon 0, no pressure) / C: balloon, compressed or Usage Max condition")
        if cmax > 1.10 * cmin or comp != 0:
            fails.append("D, G: Compressed not near one value or Compression Rate not 0")
        if last < 0.9 * first or cmin < 0.9 * cmax:
            fails.append("H: Compressed falls below 0.9")
        if (cmin != cmax) and comp == 0 and dec == 0:
            fails.append("E: Compressed changes with Compression and Decompression Rate at 0")
        if cmax >= 4_500_000:
            fails.append("size guard: Compressed Max >= 4,500,000")
        return fails[:20]
