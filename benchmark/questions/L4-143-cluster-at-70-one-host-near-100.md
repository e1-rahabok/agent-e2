# Cluster at 70%, one host near 100%

## Prompt
- The capacity manager plans to place 40 new VMs on cluster prod-cl07, six identical hosts. He looked at the cluster's CPU for last week: "The cluster never got high, so no host did either. There is room."
- You export [the CPU usage of the cluster and each host for the same week](0438/vcf-operations-cluster-hosts-cpu-usage-7-days.csv) from VCF Operations, one row per hour.

Which statements are correct?

- A. The hosts all stayed as low as the cluster, so any of them can take new VMs.
- B. At the cluster's busiest hours, one host ran near 100% while the cluster stayed near 70%.
- C. Each hourly value of the cluster blends the hot host with the lighter ones.
- D. The cluster cannot take the 40 VMs: one host at 100% means the cluster is full.
- E. Add hosts before placing the 40 VMs, since one of the six hosts reached 100%.
- F. Check why the load stays on one host: VM-Host rules, DRS automation level, VMs that cannot move.
- G. In the rows outside 09:00 to 17:00 on weekdays, esx-b23 runs at about the level of the other five hosts.
- H. DRS at its default threshold balances the hosts whenever one runs hotter than the others.

## Answers
B, C, F, G

## Explanation
- A is wrong: the misconception. In the rows where the cluster's `CPU|Usage (%) (Avg)` is highest (65% to 72%), esx-b23 reads 95% or more.
- B is correct: at the cluster's busiest hours (weekday business hours, cluster peak between 65% and 72%), esx-b23 reads 95% or more.
- C is correct: with identical hosts, the cluster's value in every row is the mean of the six host values; for it to reach about 70%, at least one host was higher.
- D is wrong: the over-correction. Capacity is planned per cluster, from the cluster average against usable capacity; the hot host is a placement and risk finding, not the capacity input.
- E is wrong: the wrong action. The other five hosts stay below 75% in every row; the load that stays on one host is a pocket (affinity rules, host groups) that more hosts do not spread.
- F is correct: affinity rules and host groups act as sub-clusters and hold a pocket of load that DRS cannot spread.
- G is correct: in the 123 rows outside 09:00 to 17:00 on weekdays, esx-b23 stays at 49.3% or below against at most 50.0% for the other hosts, with a mean of 30.3% against 30.1%. It is the hottest host in 21 of those rows, about one in six, as any one of six similar hosts would be. The hot spot is a daytime load held on one host, which fits a pocket (F).
- H is wrong: since vSphere 7.0 DRS works on each VM's DRS Score (VM happiness), not on even host utilization; a hot host whose VMs are served, or whose load a rule or setting holds, is left as it is.
- Misconception: A: the cluster peak read as a ceiling for every host. Or E: one host at 100% read as a cluster short of capacity.

## Notes
- Changed in the 2026-11-15 audit: G replaced (per-VM contention rather than host usage is tested by the pair 0019/0431) by a true reading of the export (esx-b23 outside weekday business hours at most 49.3%, the others at most 50.0%); H replaced (a misread of the host column, the negation of B) by a DRS misconception, worded without rules so that it is not F's reason (drs-migration-levels: VM DRS Score). Key unchanged: B, C, F, G.
- Converted to an export 2026-11-15 (project/practical-questions-as-exports-2026-11-15.md, row 0438): a seeded VCF Operations list view, one row per hour for 7 days, the cluster and its six hosts; the cluster equals the mean of the identical hosts in every row. The export does not show the cause of the hot host (F stays open). A, B, C and H reworded from chart and line to the export's values. The list view CSV format is assumed (project/tools/export_generator/README.md). The key holds for the generated export; the generator checks every condition against the rows.
- Practical half of the new pair D3; theory half: 0437 (design.md, section 3.9).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item D3). Counts only after the author's approval.
- Changed in the 2026-11-16 re-review: G said esx-b23 "runs no hotter than" the others off-hours, false in the 21 rows where it is the hottest (by up to 7 points); G now says "at about the level of", and option and key point name the same window (rows 09:00 to 17:00 on weekdays, as the generator's check uses). Still true; the export is unchanged.

## Metadata
```yaml
id: "0438"
title: "Cluster at 70%, one host near 100%"
product: [vcf-operations, vsphere]
technology: [cpu, system]
task: decide-capacity
level: 400
answer_type: deterministic
input: [table]
object: [cluster, esxi]
tool: [vcf-operations]
knowledge:
  - sp5-framework/observability/aggregation
  - sp5-framework/concepts/performance-vs-capacity
  - sp5-framework/capacity/supply
  - vsphere/object-types/cluster/configuration/drs-migration-levels
knowledge_main: sp5-framework/observability/aggregation
attachments:
  - 0438/vcf-operations-cluster-hosts-cpu-usage-7-days.csv
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D3"
misconception: [A, E]
misconception_type: [average-hides-worst, consumption-as-contention]
pair: "0437"
status: draft
```
