"""Question 0393: Windows Commit Limit equals RAM (no paging file), build failures.

1. typeperf Memory counters of build-agent-12 (60 s, 60 rows from 01:30).
   Pages/sec is a rate counter: row 0 prints " ".
2. inline:1 systeminfo (filtered), taken at 02:05 from the same rows.
   inline:2 is the literal empty Win32_PageFileUsage result, not touched.
"""

import datetime as dt
import re

from .. import export_framework, export_formats

GUEST = "BUILD-AGENT-12"
P = 16_383
N = 60
START = dt.datetime(2026, 11, 10, 1, 30, 0)
MIB = 1_048_576
CTR = ["Available MBytes", "Committed Bytes", "Commit Limit", "% Committed Bytes In Use", "Cache Bytes", "Pages/sec"]
COLS = [export_formats.typeperf_name(GUEST, "Memory", None, c) for c in CTR]
FILE = "typeperf-memory.csv"
FAIL = range(25, 51)  # 01:55 .. 02:20
SNAP = 35             # 02:05


def _b(mib):
    return round(mib * 256) * 4096


def _rows(seed):
    rng = export_framework.make_rng(seed, "build-agent")
    walk = export_framework.bounded_walk(rng, 10, 8_600, 120, 8_000, 9_200)
    cache = export_framework.bounded_walk(rng, N, 420, 30, 300, 600)
    rows = []
    for i in range(N):
        if i < 10:
            comm, av = walk[i], rng.uniform(7_600, 8_200)
        elif i < 25:
            f = (i - 10) / 14
            comm, av = 9_000 + 6_800 * f + rng.gauss(0, 80), 7_800 - 4_200 * f
        elif i < 51:
            comm, av = rng.uniform(15_900, 16_250), rng.uniform(2_700, 3_600)
        else:
            f = (i - 50) / 9
            comm, av = 15_900 - 5_400 * f + rng.gauss(0, 80), 3_000 + 3_500 * f
        comm = min(comm, P - 40)
        limit_b = P * MIB
        cb = _b(comm)
        pages = None if i == 0 else (rng.uniform(20, 180) if i in FAIL else rng.uniform(0, 40))
        rows.append((START + dt.timedelta(minutes=i), [int(av), cb, limit_b, 100 * cb / limit_b, _b(cache[i]), pages]))
    return rows


@export_framework.register
class WindowsCommitLimit(export_framework.QuestionExport):
    question_id = "0393"
    seed = 393

    def generate(self, seed=None):
        rows = _rows(self.seed if seed is None else seed)
        return {FILE: export_formats.typeperf_csv(COLS, rows, "Coordinated Universal Time", 0)}

    def generate_inline(self, seed=None):
        r = _rows(self.seed if seed is None else seed)[SNAP][1]
        u = r[1] // MIB
        text = ("C:\\> systeminfo | findstr /C:\"Physical Memory\" /C:\"Virtual Memory\"\n"
                f"Total Physical Memory:     {P:,} MB\n"
                f"Available Physical Memory: {r[0]:,} MB\n"
                + export_formats.systeminfo_virtual_memory(P, P - u, u, []))
        return {1: text}

    def check(self, files):
        fails = []
        try:
            cols, rows = export_formats.parse_typeperf_csv(files[FILE])
        except (KeyError, ValueError, IndexError) as e:
            return [f"parse: {e}"]
        if cols != COLS or len(rows) != N:
            return ["columns or row count differ"]
        if rows[0][1][5] is not None or any(v[5] is None for _, v in rows[1:]) or any(None in v[:5] for _, v in rows):
            fails.append("only Pages/sec of row 0 may be empty")
        if rows[0][0] != START or {(b[0] - a[0]).total_seconds() for a, b in zip(rows, rows[1:])} != {60.0}:
            fails.append("axis is not 60 s from 01:30")
        for i, (t, v) in enumerate(rows):
            av, cb, lim, p, cache, pg = v
            if abs(p - 100 * cb / lim) > 1e-9 or cb >= lim or lim != rows[0][1][2] or av >= P:
                fails.append(f"row {i}: relation broken")
            if any(x % 4096 for x in (cb, lim, cache)):
                fails.append(f"row {i}: byte value not a multiple of 4096")
            if abs(lim / MIB - P) > 1 or abs(lim / MIB - 16_384) > 0.05 * 16_384:
                fails.append(f"row {i}: D true: Commit Limit not about 16 GB")
            if i in FAIL:
                if cb / lim < 0.97:
                    fails.append(f"row {i}: A commit below 97%")
                if cb / MIB - (P - av) < 2_048 or av < 2_600:
                    fails.append(f"row {i}: B RAM in use or Available condition")
        return fails[:20]

    def check_inline(self, blocks, files):
        t = blocks.get(1, "")
        fails = []
        if blocks.get(2, "") != ("PS C:\\> Get-CimInstance Win32_PageFileUsage | Format-List Name, AllocatedBaseSize, "
                                 "CurrentUsage, PeakUsage\nPS C:\\>"):
            fails.append("inline:2: C true: not the literal empty result")
        num = lambda label: (lambda m: int(m.group(1).replace(",", "")) if m else None)(
            re.search(rf"^{re.escape(label)}\s+([\d,]+) MB$", t, re.M))
        tot, av = num("Total Physical Memory:"), num("Available Physical Memory:")
        mx, va, use = num("Virtual Memory: Max Size:"), num("Virtual Memory: Available:"), num("Virtual Memory: In Use:")
        if tot != P or mx != P:
            fails.append("inline:1: Total Physical Memory or Max Size not 16,383")
        if None in (av, va, use) or va != mx - use:
            fails.append("inline:1: Virtual Memory Available != Max Size - In Use")
        if FILE in files:
            _, rows = export_formats.parse_typeperf_csv(files[FILE])
            v = rows[SNAP][1]
            if av != int(v[0]) or use != int(v[1]) // MIB or mx != int(v[2]) // MIB:
                fails.append("inline:1: values differ from the 02:05 typeperf row")
        return fails
