"""Question 0417: datastore Read IOPS against one host's Read IOPS for it.

Two VCF Operations list exports (ASSUMED format, see formats.vcf_list_csv):
the cluster's two datastores and its four hosts, 24-hour averages and (Max).
A 288-point series of 5 minutes is built per host and datastore; the
datastore series is the sum of its hosts' series (jitter 0.97-1.02), so the
averages agree within 4%. Host A (esx-c3-02) carries about a third of ds-shared-07.
"""

from .. import core, formats, relations as rel

DS = ["ds-shared-07", "ds-shared-08"]
HOSTS = ["esx-c3-01", "esx-c3-02", "esx-c3-03", "esx-c3-04"]
HOST_A = "esx-c3-02"
F_DS, F_HOSTS = "vcf-operations-datastores-24h.csv", "vcf-operations-hosts-24h.csv"
N = 288
DCOLS = ["Datastore I/O|Read IOPS", "Datastore I/O|Read IOPS (Max)", "Datastore I/O|Write IOPS",
         "Datastore I/O|Read Latency (ms)", "Datastore I/O|Write Latency (ms)"]
HCOLS = ["Datastore:ds-shared-07|Read IOPS", "Datastore:ds-shared-07|Read IOPS (Max)",
         "Datastore:ds-shared-07|Write IOPS", "Datastore:ds-shared-07|Read Latency (ms)",
         "Datastore:ds-shared-08|Read IOPS", "Datastore:ds-shared-08|Write IOPS",
         "Datastore:ds-shared-08|Read Latency (ms)"]


def _shape(i):
    h = (8 + i * 5 / 60) % 24         # the window starts at 08:00
    return 1.6 if 1 <= h < 4 else 0.7 if h >= 18 or h < 1 else 1.0


def _avg(v):
    return sum(v) / len(v)


@core.register
class Q0417(core.Case):
    question_id = "0417"
    seed = 417

    def _model(self, seed):
        rng = core.make_rng(seed, "ds")
        shape = [_shape(i) for i in range(N)]
        mean = _avg(shape)
        res = {}
        a07 = rng.uniform(0.31, 0.36)
        w = [0.27 + rng.uniform(-0.02, 0.02), 0.22 + rng.uniform(-0.02, 0.02), 0.17 + rng.uniform(-0.02, 0.02)]
        sh07 = dict(zip(HOSTS, [w[0] * (1 - a07) / sum(w), a07, w[1] * (1 - a07) / sum(w), w[2] * (1 - a07) / sum(w)]))
        a08 = rng.uniform(0.23, 0.27)
        v = [rng.uniform(0.9, 1.1) for _ in range(3)]
        sh08 = dict(zip(HOSTS, [v[0] * (1 - a08) / sum(v), a08, v[1] * (1 - a08) / sum(v), v[2] * (1 - a08) / sum(v)]))
        for d, total, sh in ((DS[0], rng.uniform(2200, 2700), sh07), (DS[1], rng.uniform(850, 950), sh08)):
            host = {}
            for h in HOSTS:
                wr = rng.uniform(0.25, 0.40)
                lat_r, lat_w = rng.uniform(1.6, 2.8), rng.uniform(0.8, 1.6)
                rd = [total * sh[h] * s / mean * (1 + rng.gauss(0, 0.05)) for s in shape]
                host[h] = dict(rd=rd, wr=[x * wr for x in rd],
                               lr=[lat_r * (1 + rng.gauss(0, 0.05)) for _ in range(N)],
                               lw=[lat_w * (1 + rng.gauss(0, 0.05)) for _ in range(N)])
            jit = [rng.uniform(0.97, 1.02) for _ in range(N)]
            ds_rd = [sum(host[h]["rd"][i] for h in HOSTS) * jit[i] for i in range(N)]
            ds_wr = [sum(host[h]["wr"][i] for h in HOSTS) * jit[i] for i in range(N)]
            wl = lambda key, base: [sum(host[h][key][i] * host[h][base][i] for h in HOSTS)
                                    / sum(host[h][base][i] for h in HOSTS) for i in range(N)]
            res[d] = dict(host=host, rd=ds_rd, wr=ds_wr, lr=wl("lr", "rd"), lw=wl("lw", "wr"))
        return res

    def generate(self, seed=None):
        m = self._model(self.seed if seed is None else seed)
        a, b = m[DS[0]], m[DS[1]]
        drow = [(DS[0], [_avg(a["rd"]), max(a["rd"]), _avg(a["wr"]), _avg(a["lr"]), _avg(a["lw"])]),
                (DS[1], [_avg(b["rd"]), max(b["rd"]), _avg(b["wr"]), _avg(b["lr"]), _avg(b["lw"])])]
        hrow = []
        for h in HOSTS:
            x, y = a["host"][h], b["host"][h]
            hrow.append((h, [_avg(x["rd"]), max(x["rd"]), _avg(x["wr"]), _avg(x["lr"]),
                             _avg(y["rd"]), _avg(y["wr"]), _avg(y["lr"])]))
        return {F_DS: formats.vcf_list_csv(DCOLS, drow), F_HOSTS: formats.vcf_list_csv(HCOLS, hrow)}

    def check(self, files):
        try:
            dc, dr = formats.parse_vcf_list_csv(files[F_DS])
            hc, hr = formats.parse_vcf_list_csv(files[F_HOSTS])
        except KeyError as e:
            return [f"missing {e}"]
        if dc != DCOLS or hc != HCOLS:
            return ["columns differ"]
        if [n for n, _ in dr] != DS or [n for n, _ in hr] != HOSTS:
            return ["row names differ"]
        fails = []
        d = {n: dict(zip(dc, v)) for n, v in dr}
        h = {n: dict(zip(hc, v)) for n, v in hr}
        for ds in DS:
            for metric in ("Read IOPS", "Write IOPS"):
                tot = d[ds][f"Datastore I/O|{metric}"]
                s = sum(h[x][f"Datastore:{ds}|{metric}"] for x in HOSTS)
                if abs(s - tot) > 0.10 * tot:                       # D
                    fails.append(f"D: {ds} {metric}: sum of hosts {s:.1f} vs datastore {tot:.1f}")
            wm = (sum(h[x][f"Datastore:{ds}|Read Latency (ms)"] * h[x][f"Datastore:{ds}|Read IOPS"] for x in HOSTS)
                  / sum(h[x][f"Datastore:{ds}|Read IOPS"] for x in HOSTS))
            if abs(d[ds]["Datastore I/O|Read Latency (ms)"] - wm) > 0.10 * wm:
                fails.append(f"{ds}: Read Latency not within 10% of the IOPS-weighted host mean")
        mx = d[DS[0]]["Datastore I/O|Read IOPS (Max)"]
        hmx = [h[x]["Datastore:ds-shared-07|Read IOPS (Max)"] for x in HOSTS]
        if not max(hmx) <= mx <= 1.05 * sum(hmx):
            fails.append("datastore Read IOPS (Max) outside host max .. 1.05 x sum of host max")
        for x in HOSTS:
            if h[x]["Datastore:ds-shared-07|Read IOPS (Max)"] < h[x]["Datastore:ds-shared-07|Read IOPS"]:
                fails.append(f"{x}: (Max) below the average")
        if mx < d[DS[0]]["Datastore I/O|Read IOPS"]:
            fails.append("datastore (Max) below the average")
        ds07 = d[DS[0]]["Datastore I/O|Read IOPS"]
        a = h[HOST_A]["Datastore:ds-shared-07|Read IOPS"]
        if not 0.25 * ds07 <= a <= 0.40 * ds07:                     # C
            fails.append(f"C: host A share {a / ds07:.3f} outside 0.25-0.40")
        if not a < ds07 or not a < 0.5 * ds07:                      # E, I
            fails.append("E/I: host A not below the datastore / half of it")
        if a != max(h[x]["Datastore:ds-shared-07|Read IOPS"] for x in HOSTS):
            fails.append("I: host A is not the largest of the four hosts")
        return fails[:20]
