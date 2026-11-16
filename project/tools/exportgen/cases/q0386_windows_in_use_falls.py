"""Question 0386: Windows memory In Use falls after an application restart, Consumed stays.

Two files for VM jas-prod-03 (Windows Server 2022, 32 GB), 72 five-minute
points from 2026-11-10 12:00Z, application restart at 15:02Z:
1. typeperf Memory counters (all instantaneous, so row 0 has values).
2. vCenter Past day style rows (5-minute points, generated directly).
Swapped and Compressed column names are assumed from the `<Measurement> for
<object>` pattern (README). Windows In Use is not a counter: it is
T - Modified - Standby - Free & Zero, so Available + Modified moves by -ΔInUse.
"""

import datetime as dt

from .. import core, formats

Z = dt.timezone.utc
GUEST = "JAS-PROD-03"
VM = "jas-prod-03"
T_MIB = 32_767
CFG_KB = 33_554_432
N = 72
BEFORE = 37
START = dt.datetime(2026, 11, 10, 12, 0, 0, tzinfo=Z)
LIMIT_MIB = T_MIB + 8_192
CTR = ["Available MBytes", "Committed Bytes", "Commit Limit", "% Committed Bytes In Use", "Cache Bytes",
       "Modified Page List Bytes", "Standby Cache Core Bytes", "Standby Cache Normal Priority Bytes",
       "Standby Cache Reserve Bytes", "Free & Zero Page List Bytes"]
TP_COLS = [formats.typeperf_name(GUEST, "Memory", None, c) for c in CTR]
VC_COLS = [f"{m} for {VM}" for m in ("Active", "Ballooned memory", "Consumed", "Granted", "Swapped", "Compressed")]
TP = "typeperf-memory.csv"
VC = "vcenter-vm-memory-past-day.csv"
MIB = 1_048_576


def _b(mib):
    return round(mib * 256) * 4096


@core.register
class WindowsInUseFalls(core.Case):
    question_id = "0386"
    seed = 386

    def generate(self, seed=None):
        rng = core.make_rng(self.seed if seed is None else seed, "win-mem")
        walk = core.bounded_walk(rng, BEFORE, 25_400, 60, 25_050, 25_750)
        nwalk = core.bounded_walk(rng, BEFORE, 4_700, 80, 4_400, 5_000)
        cache = core.bounded_walk(rng, N, 540, 40, 380, 720)
        times = core.time_axis(START, N, 300)
        tp, vc = [], []
        for i, t in enumerate(times):
            k = i - BEFORE
            if k < 0:
                inuse, normal = walk[i], nwalk[i]
                comm = rng.uniform(29_820, 29_980)
            else:
                inuse = core.clamp(12_600 + 3_200 * k / 34 + rng.gauss(0, 60), 12_300, 16_200)
                normal = 4_800 + 800 * k / 34 + rng.gauss(0, 60)
                comm = rng.uniform(29_420, 29_580)
            mod = _b(rng.uniform(520, 680))
            core_b = _b(rng.uniform(180, 220))
            res = _b(rng.uniform(850, 950))
            norm_b = _b(normal)
            free_b = _b(T_MIB - inuse) - mod - core_b - norm_b - res
            assert free_b >= 150 * MIB, (i, free_b / MIB)
            avail = (core_b + norm_b + res + free_b) // MIB
            commit_b = _b(comm)
            limit_b = LIMIT_MIB * MIB
            tp.append((t, [avail, commit_b, limit_b, 100 * commit_b / limit_b, _b(cache[i]),
                           mod, core_b, norm_b, res, free_b]))
        act_b = core.bounded_walk(rng, BEFORE, 3_400_000, 250_000, 2_200_000, 4_800_000)
        act_a = core.bounded_walk(rng, N - BEFORE, 2_400_000, 200_000, 1_600_000, 3_600_000)
        for i, t in enumerate(times):
            cons = round(core.clamp(32_830_000 + rng.gauss(0, 12_000), 32_780_000, 32_880_000))
            gran = cons + rng.randint(38_000, 46_000)
            k = i - BEFORE
            if k in (0, 1):
                act = rng.randint(5_500_000, 7_000_000)
            else:
                act = round(act_b[i] if k < 0 else act_a[k])
            vc.append((t, [act, 0, cons, gran, 0, 0]))
        return {TP: formats.typeperf_csv(TP_COLS, tp, "Coordinated Universal Time", 0),
                VC: formats.vcenter_csv(VC_COLS, vc)}

    def check(self, files):
        fails = []
        try:
            tc, tr = formats.parse_typeperf_csv(files[TP])
            vcols, vr = formats.parse_vcenter_csv(files[VC])
        except (KeyError, ValueError, IndexError) as e:
            return [f"parse: {e}"]
        if tc != TP_COLS or vcols != VC_COLS:
            return ["columns differ"]
        if len(tr) != N or len(vr) != N:
            return [f"row counts {len(tr)}, {len(vr)}"]
        if [t.replace(tzinfo=Z) for t, _ in tr] != [t for t, _ in vr]:
            fails.append("time stamps of the two files differ")
        if tr[0][0].replace(tzinfo=Z) != START or {(b[0] - a[0]).total_seconds() for a, b in zip(tr, tr[1:])} != {300.0}:
            fails.append("typeperf axis is not 5 min from 12:00")
        if any(None in v for _, v in tr):
            fails.append("a typeperf counter is empty (all are instantaneous)")
        limit0 = tr[0][1][2]
        D, fz, comm, pct = [], [], [], []
        for i, (t, v) in enumerate(tr):
            av, cb, lim, p, cache, mod, co, no, rs, fr = v
            if av != (co + no + rs + fr) // MIB:
                fails.append(f"row {i}: Available != floor(standby + free)")
            if abs(p - 100 * cb / lim) > 1e-9 or cb >= lim or lim != limit0:
                fails.append(f"row {i}: commit relation broken")
            if (mod + co + no + rs + fr) / MIB >= T_MIB:
                fails.append(f"row {i}: In Use not positive")
            if any(x % 4096 for x in (cb, lim, cache, mod, co, no, rs, fr)):
                fails.append(f"row {i}: byte value not a multiple of 4096")
            D.append(av + mod / MIB)
            fz.append(fr / MIB)
            comm.append(cb / MIB)
            pct.append(p)
        mean = lambda x: sum(x) / len(x)
        if min(D[BEFORE:]) - max(D[:BEFORE]) < 8_492:
            fails.append("A: Available + Modified does not show the fall of In Use")
        if abs(mean(pct[BEFORE:]) - mean(pct[:BEFORE])) > 2.0 or min(comm[BEFORE:]) < 0.97 * max(comm[:BEFORE]):
            fails.append("A: commit shows the fall")
        if mean(fz[BEFORE:]) < mean(fz[:BEFORE]) + 7_000:
            fails.append("C: Free & Zero does not rise by 7,000 MiB")
        col = lambda j: [v[j] for _, v in vr]
        act, bal, cons, gran, swp, cmp_ = (col(j) for j in range(6))
        if any(bal) or any(swp) or any(cmp_):
            fails.append("D: reclamation counter not 0")
        if any(not 32_780_000 <= c <= 32_880_000 for c in cons) or max(cons) - min(cons) > 335_544:
            fails.append("B: Consumed range")
        if any(abs(a - b) > 60_000 for a, b in zip(cons, cons[1:])):
            fails.append("B: Consumed step above 60,000 KB")
        if any(not a < c <= g <= CFG_KB for a, c, g in zip(act, cons, gran)):
            fails.append("vCenter: Active < Consumed <= Granted <= configured broken")
        if any(a >= 0.25 * CFG_KB for a in act):
            fails.append("F: Active reaches 0.25 x configured")
        return fails[:20]
