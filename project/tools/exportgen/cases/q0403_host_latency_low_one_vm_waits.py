"""Question 0403: one VM waits while the host Latency stays low.

esx-c22 runs 24 VMs; ord-api-03 waits for memory (Latency 5-10%, Swap in rate
above 0) in six rows (04:15-04:40 UTC). Host Latency is the mean over the 24 VMs
and never passes 0.5. Host Usage is unrelated to the wait. Column names
"Latency" and "Swap in rate" follow the "<Measurement> for <object>" pattern.
"""

from .. import core, formats

HOST, VM = "esx-c22", "ord-api-03"
N = 144
STEP_S = 300
START = core.DEFAULT_START.replace(year=2026, month=11, day=14, hour=0, minute=0)
W = range(51, 57)
HUMP = [5.4, 6.8, 8.9, 9.4, 7.6, 5.9]
F_HOST = "vcenter-host-memory-12h.csv"
F_VM = "vcenter-vm-memory-12h.csv"
C_HOST = [f"Latency for {HOST}", f"Usage for {HOST}"]
C_VM = [f"Latency for {VM}", f"Swap in rate for {VM}"]


@core.register
class Q0403(core.Case):
    question_id = "0403"
    seed = 403

    def generate(self, seed=None):
        seed = self.seed if seed is None else seed
        rng = core.make_rng(seed, "wait")
        usage = core.bounded_walk(rng, N, 84.0, 0.5, 81.0, 87.0)
        times = core.time_axis(START, N, STEP_S)
        host, vm = [], []
        for i, t in enumerate(times):
            if i in W:
                lat = round(core.clamp(HUMP[i - W.start] + rng.uniform(-0.3, 0.3), 5.0, 10.0), 2)
                sw = round((1200 + 520 * lat) * (1 + rng.uniform(-0.15, 0.15)))
            else:
                lat, sw = 0, 0
            vals = [0 if rng.random() < 0.97 else rng.uniform(0.05, 0.6) for _ in range(23)]
            b = min(sum(vals) / 23, 0.05)
            hl = round((lat + 23 * b) / 24, 2)
            host.append((t, [hl, round(usage[i], 2)]))
            vm.append((t, [lat, sw]))
        return {F_HOST: formats.vcenter_csv(C_HOST, host), F_VM: formats.vcenter_csv(C_VM, vm)}

    def check(self, files):
        try:
            ch, rh = formats.parse_vcenter_csv(files[F_HOST])
            cv, rv = formats.parse_vcenter_csv(files[F_VM])
        except (KeyError, ValueError) as e:
            return [str(e)]
        if ch != C_HOST or cv != C_VM:
            return [f"columns differ: {ch} {cv}"]
        fails = []
        if len(rh) != N or len(rv) != N:
            return [f"rows {len(rh)}/{len(rv)}, expected {N}"]
        stamps = [r[0] for r in rh]
        if stamps != [r[0] for r in rv] or stamps != core.time_axis(START, N, STEP_S):
            fails.append("time stamps differ from the 12-hour 5-minute axis")
        hl = formats.column(ch, rh, C_HOST[0])
        vl = formats.column(cv, rv, C_VM[0])
        sw = formats.column(cv, rv, C_VM[1])
        for i in range(N):
            if not hl[i] >= vl[i] / 24 - 0.01 or hl[i] > 0.5:
                fails.append(f"row {i}: host Latency {hl[i]} not the mean over 24 VMs")
            if (vl[i] > 0) != (sw[i] > 0):
                fails.append(f"row {i}: VM Latency > 0 differs from Swap in rate > 0")
            if i in W:                                                   # C, B, F
                if not 5 <= vl[i] <= 10:
                    fails.append(f"row {i}: VM Latency outside 5-10")
            elif vl[i] != 0:
                fails.append(f"row {i}: VM Latency not 0 outside the wait")
        if sum(hl[i] for i in W) / len(W) <= sum(hl[i] for i in range(N) if i not in W) / (N - len(W)):  # A
            fails.append("A: host Latency not higher during the wait")
        if max(vl) < 5:
            fails.append("B: max VM Latency below 5")
        if max(hl) > 0.5:
            fails.append("D: host Latency above 0.5")
        return fails[:20]
