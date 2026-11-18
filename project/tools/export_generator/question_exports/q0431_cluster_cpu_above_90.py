"""Question 0431: cluster CPU above 90%, request for more hosts.

Two VCF Operations List view CSVs (ASSUMED format, see the export_generator README).
1: cluster prod-cl03, one row per hour (each row aggregates the hour's twelve
5-minute values), 168 rows from Sunday 2026-11-08 00:00 GMT+08:00.
2: the 140 VMs of the cluster, each value the maximum over the same 7 days,
sorted by CPU contention (Max) descending.

Relations: Usage Max >= Usage Avg, every Usage <= 100, every hourly cluster
Contention Avg <= the top VM's weekly Contention Max.
"""

import datetime as dt

from .. import export_framework, export_formats

TZ = 8
START = dt.datetime(2026, 11, 8, 0, 0, tzinfo=dt.timezone(dt.timedelta(hours=TZ)))
HOURS = 168
C1 = ["CPU|Usage (%) (Avg)", "CPU|Usage (%) (Max)", "CPU|Contention (%) (Avg)"]
C2 = ["CPU|Contention (%) (Max)", "CPU|Usage (%) (Max)"]
FAMILIES = [("web", 30), ("app", 40), ("batch", 30), ("db", 12), ("svc", 28)]


def _hour_class(t):
    if t.weekday() >= 5:
        return "weekend"
    if 9 <= t.hour <= 17:
        return "business"
    if t.hour in (7, 8, 18, 19):
        return "shoulder"
    return "night"


@export_framework.register
class ClusterCpuAbove90(export_framework.QuestionExport):
    question_id = "0431"
    seed = 431
    f1 = "vcf-operations-cluster-cpu-7-days.csv"
    f2 = "vcf-operations-cluster-vms-cpu-7-days.csv"

    def generate(self, seed=None):
        rng = export_framework.make_rng(self.seed if seed is None else seed, "cluster-cpu")
        times = [START + dt.timedelta(hours=i) for i in range(HOURS)]
        classes = [_hour_class(t) for t in times]
        biz = [i for i, c in enumerate(classes) if c == "business"]
        low = set()
        days_used = set()
        for i in rng.sample(biz, len(biz)):
            if times[i].date() not in days_used:
                low.add(i)
                days_used.add(times[i].date())
            if len(low) == 3:
                break
        rows1 = []
        for i, t in enumerate(times):
            c = classes[i]
            if c == "business":
                avg = rng.uniform(86, 89.5) if i in low else rng.uniform(90.5, 95.5)
                cont = rng.uniform(0.08, 0.30)
            elif c == "shoulder":
                avg, cont = rng.uniform(78, 88), rng.uniform(0.04, 0.15)
            elif c == "night":
                avg, cont = rng.uniform(55, 70), rng.uniform(0.01, 0.06)
            else:
                avg, cont = rng.uniform(50, 66), rng.uniform(0.01, 0.06)
            avg = round(avg, 2)
            bump = rng.uniform(0.8, 3.5) if c in ("business", "shoulder") else rng.uniform(1.5, 6)
            mx = round(min(avg + bump, 99.5), 2)
            rows1.append((export_formats.vcf_time(t, TZ), [avg, mx, round(cont, 2)]))
        names = [f"{fam}-{n:02d}" for fam, cnt in FAMILIES for n in range(1, cnt + 1)]
        order = rng.sample(names, len(names))
        rows2 = []
        for rank, name in enumerate(order):
            if rank == 0:
                cont = rng.uniform(0.70, 0.92)
            elif rank < 10:
                cont = rng.uniform(0.45, 0.70)
            else:
                cont = rng.uniform(0.03, 0.45)
            fam = name.split("-")[0]
            lo, hi = {"batch": (88, 100), "app": (88, 100), "web": (45, 85),
                      "db": (55, 90), "svc": (8, 40)}[fam]
            rows2.append((name, [round(cont, 2), round(rng.uniform(lo, hi), 2)]))
        rows2.sort(key=lambda r: (-r[1][0], r[0]))
        return {self.f1: export_formats.vcf_list_csv(C1, rows1, name_header="Time"),
                self.f2: export_formats.vcf_list_csv(C2, rows2, name_header="Name")}

    def check(self, files):
        fails = []
        try:
            c1, r1 = export_formats.parse_vcf_list_csv(files[self.f1])
            c2, r2 = export_formats.parse_vcf_list_csv(files[self.f2])
        except (KeyError, ValueError, IndexError) as e:
            return [f"parse: {e}"]
        if c1 != C1 or c2 != C2:
            return ["columns differ"]
        if len(r1) != HOURS:
            fails.append(f"file 1 has {len(r1)} rows, expected {HOURS}")
        if len(r2) != 140:
            fails.append(f"file 2 has {len(r2)} rows, expected 140")
        if len({n for n, _ in r2}) != len(r2):
            fails.append("file 2 names are not unique")
        times = [export_formats.parse_vcf_time(n) for n, _ in r1]
        for i, t in enumerate(times):
            if t != START + dt.timedelta(hours=i):
                fails.append(f"file 1 row {i}: time {t} off the hourly axis")
                break
        top = max(v[0] for _, v in r2)
        biz_avg, biz_n = 0, 0
        for (n, (avg, mx, cont)), t in zip(r1, times):
            if mx < avg or cont < 0 or avg > 100 or mx > 100:
                fails.append(f"file 1 {n}: relation broken ({avg}, {mx}, {cont})")
            if cont > top:
                fails.append(f"file 1 {n}: cluster contention {cont} above top VM {top}")
            if _hour_class(t) == "business":
                biz_n += 1
                biz_avg += avg >= 90
        cons = [v[0] for _, v in r2]
        if cons != sorted(cons, reverse=True):
            fails.append("file 2 is not sorted by contention descending")
        if any(v[1] > 100 or v[1] < 0 for _, v in r2):
            fails.append("file 2: Usage Max outside 0..100")
        # A false / B true / D true / H false (the top VM is below 1% anyway: the average and the worst give the same reading)
        if not max(cons) < 1.0:
            fails.append("A, B, D, H: a VM weekly contention max is 1.0 or more")
        if sum(1 for _, v in r2 if v[1] >= 88) < 40:
            fails.append("A/B: fewer than 40 VMs with Usage Max >= 88")
        # E true; the cluster is busy (A false needs busy without contention)
        if biz_n != 45 or biz_avg < 40:
            fails.append(f"E: {biz_avg} of {biz_n} business rows have Avg >= 90")
        if not max(v[0] for _, v in r1) >= 90:
            fails.append("A/E: max Usage Avg below 90")
        if not max(v[1] for _, v in r1) > 80:
            fails.append("A/E: max Usage Max not above 80")
        return fails[:20]
