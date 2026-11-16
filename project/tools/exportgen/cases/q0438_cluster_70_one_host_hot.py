"""Question 0438: cluster at 70%, one host near 100%.

VCF Operations List view CSV (ASSUMED format, see the exportgen README), one
row per hour, 168 rows from Sunday 2026-11-08 00:00 GMT+08:00, each value the
hourly average of the 5-minute values. One column per object, named
`<object> - <metric label> (Avg)` after the captured chart title
`<object> - <metric label>`. Cluster prod-cl07, six identical hosts, hot host
esx-b23 on Mon-Thu 10:00-15:00. The cluster value is the mean of the six
rounded host values, so it stays under 72 while the hot host is above 95.
"""

import datetime as dt

from .. import core, formats, relations as rel

TZ = 8
START = dt.datetime(2026, 11, 8, 0, 0, tzinfo=dt.timezone(dt.timedelta(hours=TZ)))
HOURS = 168
HOSTS = [f"esx-b{n}" for n in range(21, 27)]
HOT_HOST = "esx-b23"
METRIC = "CPU|Usage (%) (Avg)"
COLS = [f"prod-cl07 - {METRIC}"] + [f"{h} - {METRIC}" for h in HOSTS]


def _cls(t):
    wd, h = t.weekday(), t.hour
    if wd >= 5:
        return "weekend"
    if wd <= 3 and 10 <= h <= 15:
        return "hot"
    if wd <= 3 and h in (9, 16):
        return "ramp"
    if 9 <= h <= 17:
        return "business"
    if h in (7, 8, 18, 19):
        return "shoulder"
    return "night"


_RANGE = {"hot": (60, 66), "ramp": (50, 58), "business": (50, 62),
          "shoulder": (35, 50), "night": (22, 38), "weekend": (18, 32)}


@core.register
class ClusterAt70OneHostHot(core.Case):
    question_id = "0438"
    seed = 438
    filename = "vcf-operations-cluster-hosts-cpu-usage-7-days.csv"

    def generate(self, seed=None):
        rng = core.make_rng(self.seed if seed is None else seed, "hosts-cpu")
        rows = []
        for i in range(HOURS):
            t = START + dt.timedelta(hours=i)
            c = _cls(t)
            vals = []
            for h in HOSTS:
                if h == HOT_HOST and c == "hot":
                    v = rng.uniform(95.5, 99.2)
                elif h == HOT_HOST and c == "ramp":
                    v = rng.uniform(80, 88)
                else:
                    v = rng.uniform(*_RANGE[c])
                vals.append(round(v, 2))
            rows.append((formats.vcf_time(t, TZ), [round(rel.cluster_mean(vals), 2)] + vals))
        return {self.filename: formats.vcf_list_csv(COLS, rows, name_header="Time")}

    def check(self, files):
        fails = []
        try:
            cols, rows = formats.parse_vcf_list_csv(files[self.filename])
        except (KeyError, ValueError, IndexError) as e:
            return [f"{self.filename}: {e}"]
        if cols != COLS:
            return ["columns differ"]
        if len(rows) != HOURS:
            return [f"{len(rows)} rows, expected {HOURS}"]
        for i, (n, v) in enumerate(rows):
            if formats.parse_vcf_time(n) != START + dt.timedelta(hours=i):
                fails.append(f"row {i}: time off the hourly axis")
                break
            if abs(v[0] - sum(v[1:]) / 6) > 0.006:
                fails.append(f"C true: row {i}: cluster {v[0]} != mean of hosts")
            if any(not 0 <= x <= 100 for x in v):
                fails.append(f"row {i}: value outside 0..100")
        cl = [v[0] for _, v in rows]
        hot = [v[HOSTS.index(HOT_HOST) + 1] for _, v in rows]
        top = sorted(range(HOURS), key=lambda i: -cl[i])[:10]
        for i in top:
            if hot[i] < 95 or cl[i] > 72:
                fails.append(f"A/B: TOP row {i}: hot host {hot[i]}, cluster {cl[i]}")
            if not max(rows[i][1][1:]) > cl[i]:
                fails.append(f"TOP row {i}: max host not above cluster")
        if not 65 <= max(cl) <= 72:
            fails.append(f"max cluster {max(cl)} outside 65..72")
        if max(hot) < 95:
            fails.append("hot host never reaches 95")
        for h in HOSTS:
            if h != HOT_HOST and any(v[HOSTS.index(h) + 1] >= 75 for _, v in rows):
                fails.append(f"E false: {h} reaches 75 or more")
        # G true: outside weekday business hours (Mon-Fri 09:00-17:00) the hot host is no hotter than the others
        off = [v for n, v in rows if not (formats.parse_vcf_time(n).weekday() < 5 and 9 <= formats.parse_vcf_time(n).hour <= 17)]
        hot_off = max(v[HOSTS.index(HOT_HOST) + 1] for v in off)
        other_off = max(v[HOSTS.index(h) + 1] for v in off for h in HOSTS if h != HOT_HOST)
        if not off or hot_off > 50 or hot_off > other_off:
            fails.append(f"G: off-hours hot host max {hot_off} above 50 or above the other hosts' max {other_off}")
        return fails[:20]
