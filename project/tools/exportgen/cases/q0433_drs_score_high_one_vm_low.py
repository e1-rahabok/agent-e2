"""Question 0433: the cluster DRS score is green, one VM is not.

1: vSphere Client VM DRS Score grid of cluster cl-prod-02 (ASSUMED export
layout, see the exportgen README): 24 powered-on VMs, lowest score first.
pay-api-03 (8 vCPUs) has a low score and a high CPU Readiness; rpt-batch-09
has a low score for memory reasons (swapped and ballooned memory, low Ready).
2: vCenter real-time CPU chart of pay-api-03, 30 minutes, Readiness 6-11%.
Inline:1: PowerCLI line and the cluster score (mean of the 24 VM scores, the
stand-in for the weights VMware does not publish).

Relations: Run + Ready + Co-stop + Wait = 160,000 ms per sample; Readiness =
Ready / 160,000; Co-stop < Ready; Usage <= Run %; Used CPU <= Active CPU; the
grid's Readiness of pay-api-03 = mean Readiness of the last 15 chart rows.
"""

import datetime as dt

from .. import core, formats, relations as rel

CLUSTER = "cl-prod-02"
VM = "pay-api-03"
DECOY = "rpt-batch-09"
VCPUS = 8
ROWS = 90
START = dt.datetime(2026, 11, 10, 8, 30, 0, tzinfo=core.UTC)
GRID_COLS = ["Name", "DRS Score", "Active CPU", "Used CPU", "CPU Readiness", "Granted Memory",
             "Swapped Memory", "Ballooned Memory"]
VC = [f"{m} for {VM}" for m in ("Usage", "Readiness", "Ready", "Run", "Co-stop", "Wait", "Max limited")]
OTHERS = [f"app-web-{n:02d}" for n in range(1, 9)] + [f"svc-q-{n:02d}" for n in range(1, 7)] + \
         [f"db-ro-{n:02d}" for n in range(1, 5)] + ["jump-02", "mon-03", "ci-run-01", "ci-run-02"]
TOTAL = rel.vcpu_state_total_ms(VCPUS)
PS = f"PS> (Get-Cluster {CLUSTER}).ExtensionData.Summary.DrsScore"


def _gb(x):
    return f"{int(x)} GB" if float(x).is_integer() else f"{x:.1f} GB"


def _build(seed):
    rng = core.make_rng(seed, "drs-score")
    u = rng.uniform
    target = [u(2.2, 4.8) for _ in range(10)] + core.bounded_walk(rng, 80, 8, 0.8, 5.6, 11.5)
    runpct = core.bounded_walk(rng, ROWS, 60, 2, 48, 72)
    vc, readiness, runs, usages = [], [], [], []
    for i in range(ROWS):
        ready = round(rel.ready_ms_from_readiness(target[i], VCPUS))
        run = round(runpct[i] * 1600)
        costop = round(TOTAL * u(0.003, 0.012))
        wait = rel.wait_from_states(VCPUS, run, ready, costop)
        assert wait > 0 and costop < ready
        rd = round(rel.readiness_pct(ready, VCPUS), 2)
        usage = round(run / 1600 * u(0.85, 0.95), 2)
        vc.append((START + dt.timedelta(seconds=20 * (i + 1)), [usage, rd, ready, run, costop, wait, 0]))
        readiness.append(rd)
        runs.append(run / 1600)
        usages.append(usage)
    m15 = lambda xs: sum(xs[-15:]) / 15
    rows = []   # (drs, name, cells)
    drs = rng.randint(38, 46)
    rows.append((drs, VM, [f"{drs}%", f"{round(m15(runs) + m15(readiness))}%", f"{round(m15(usages))}%",
                            f"{m15(readiness):.2f}%", _gb(32), _gb(0), _gb(0)]))
    drs = rng.randint(50, 58)
    active = rng.randint(20, 35)
    rows.append((drs, DECOY, [f"{drs}%", f"{active}%", f"{active - rng.randint(1, 4)}%",
                              f"{u(0.20, 0.80):.2f}%", _gb(48), _gb(round(u(2.5, 4.0), 1)),
                              _gb(round(u(5.0, 7.5), 1))]))
    for name in OTHERS:
        drs = rng.randint(95, 100)
        active = rng.randint(3, 45)
        used = max(1, active - rng.randint(0, 3))
        rows.append((drs, name, [f"{drs}%", f"{active}%", f"{used}%", f"{u(0.05, 1.40):.2f}%",
                                 _gb(rng.choice([4, 8, 16, 24, 32])), _gb(0), _gb(0)]))
    rows.sort(key=lambda r: (r[0], r[1]))
    score = round(sum(r[0] for r in rows) / len(rows))
    grid = formats.vsphere_grid_csv(GRID_COLS, [[name] + cells for _, name, cells in rows])
    return formats.vcenter_csv(VC, vc), grid, f"{PS}\n{score}\n"


@core.register
class DrsScoreHighOneVmLow(core.Case):
    question_id = "0433"
    seed = 433
    f_grid = "vcenter-cluster-vm-drs-scores.csv"
    f_vc = "vcenter-vm-cpu-realtime.csv"

    def generate(self, seed=None):
        vc, grid, _ = _build(self.seed if seed is None else seed)
        return {self.f_grid: grid, self.f_vc: vc}

    def generate_inline(self, seed=None):
        return {1: _build(self.seed if seed is None else seed)[2]}

    @staticmethod
    def _pct(s):
        if not s.endswith("%"):
            raise ValueError(f"not a percent cell: {s!r}")
        return float(s[:-1])

    @staticmethod
    def _gb(s):
        if not s.endswith(" GB"):
            raise ValueError(f"not a GB cell: {s!r}")
        return float(s[:-3])

    def check(self, files):
        try:
            gcols, grows = formats.parse_vsphere_grid_csv(files[self.f_grid])
            vcols, vrows = formats.parse_vcenter_csv(files[self.f_vc])
        except (KeyError, ValueError, IndexError) as e:
            return [f"parse: {e}"]
        if gcols != GRID_COLS or vcols != VC:
            return ["columns differ"]
        fails = []
        if len(grows) != 24 or len(vrows) != ROWS:
            return [f"{len(grows)} grid rows, {len(vrows)} chart rows"]
        try:
            g = [{"name": r[0], "drs": self._pct(r[1]), "active": self._pct(r[2]), "used": self._pct(r[3]),
                  "ready": self._pct(r[4]), "granted": self._gb(r[5]), "swap": self._gb(r[6]),
                  "balloon": self._gb(r[7])} for r in grows]
        except ValueError as e:
            return [f"grid: {e}"]
        if [x["drs"] for x in g] != sorted(x["drs"] for x in g):
            fails.append("grid not sorted by DRS Score ascending")
        for a, b in zip(g, g[1:]):
            if a["drs"] == b["drs"] and a["name"] > b["name"]:
                fails.append("grid ties not sorted by name")
        for x in g:
            if x["used"] > x["active"]:
                fails.append(f"{x['name']}: Used CPU above Active CPU")
        readiness = []
        for i, (t, v) in enumerate(vrows):
            usage, rd, ready, run, costop, wait, maxlim = v
            if t != START + dt.timedelta(seconds=20 * (i + 1)):
                fails.append(f"row {i}: time off the 20 s axis")
            if rel.state_sum_ms(run, ready, costop, wait) != TOTAL:
                fails.append(f"row {i}: state sum")
            if abs(rd - rel.readiness_pct(ready, VCPUS)) > 0.006:
                fails.append(f"row {i}: Readiness vs Ready")
            if not costop < ready or maxlim != 0 or wait <= 0 or usage > run / 1600:
                fails.append(f"row {i}: Co-stop, Max limited, Wait or Usage relation broken")
            readiness.append(rd)
        pay, decoy = g[0], g[1]
        if pay["name"] != VM or decoy["name"] != DECOY:                          # B, H
            fails.append("first grid row is not pay-api-03 or second is not rpt-batch-09")
        m15 = sum(readiness[-15:]) / 15
        if abs(pay["ready"] - m15) > 0.01:
            fails.append(f"grid Readiness {pay['ready']} != mean of the last 15 chart rows {m15:.2f}")
        if min(readiness) < 2:                                                    # C
            fails.append("a Readiness below 2")
        if not (sum(readiness) / ROWS > 5 and sum(1 for x in readiness if x > 5) >= 0.8 * ROWS):   # D
            fails.append("D: mean Readiness not above 5, or fewer than 80% of rows above 5")
        if not (decoy["drs"] < 60 and decoy["ready"] < 1 and decoy["swap"] > 0 and decoy["balloon"] > 0):   # H
            fails.append("H: rpt-batch-09 does not show a low score with low Ready and swap/balloon")
        if not pay["drs"] < 50:
            fails.append("B: pay-api-03 DRS Score not below 50")
        return fails[:20]

    def check_inline(self, blocks, files):
        lines = blocks.get(1, "").split("\n")
        if len(lines) != 2 or lines[0] != PS or not lines[1].isdigit():
            return ["inline:1: expected the PowerCLI line and a bare integer score"]
        try:
            _, grows = formats.parse_vsphere_grid_csv(files[self.f_grid])
            scores = [self._pct(r[1]) for r in grows]
        except (KeyError, ValueError, IndexError) as e:
            return [f"inline:1: grid: {e}"]
        score = int(lines[1])
        fails = []
        if score != round(sum(scores) / len(scores)):
            fails.append("inline:1: cluster score != round(mean of the grid's DRS Scores)")
        if score < 90:                                                            # A false
            fails.append("inline:1: cluster score below 90")
        if score - scores[0] < 40:                                                # B
            fails.append("inline:1: pay-api-03 is not at least 40 points below the cluster score")
        return fails
