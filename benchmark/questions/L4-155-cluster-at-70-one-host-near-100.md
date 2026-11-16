# Cluster at 70%, one host near 100%

## Prompt
- The capacity manager plans to place 40 new VMs on cluster prod-cl07, six identical hosts. He looked at the cluster's CPU for last week: "The cluster never got high, so no host did either. There is room."
- You export [the CPU usage of the cluster and each host for the same week](0438/vcf-operations-cluster-hosts-cpu-usage-7-days.csv) from VCF Operations, one row per hour.

Which statements are correct?

- A. The hosts all stayed as low as the cluster, so any of them can take new VMs.
- B. At the cluster's busiest hours, one host ran near 100% while the cluster stayed near 70%.
- C. Each hourly value of the cluster blends the hot host with the lighter ones.
- D. The cluster cannot take the 40 VMs: one host at 100% means it is full.
- E. Add hosts before placing the 40 VMs, since one host reached 100%.
- F. Check why the load stays on one host: VM-Host rules, the DRS automation level, VMs that cannot move.
- G. The VMs on the hot host may wait for CPU at those hours; their CPU Ready shows whether they did.
- H. The busiest host's CPU|Usage (%) peaks below 80%.

## Likely wrong answer
A: the cluster peak read as a ceiling for every host. Or E: one host at 100% read as a cluster short of capacity.

## Expected key points
- Answer: B, C, F, G.
- A false: the misconception. In the rows where the cluster's `CPU|Usage (%) (Avg)` is highest (65% to 72%), esx-b23 reads 95% or more.
- B true: at the cluster's busiest hours (weekday business hours, cluster peak between 65% and 72%), esx-b23 reads 95% or more.
- C true: with identical hosts, the cluster's value in every row is the mean of the six host values; for it to reach about 70%, at least one host was higher.
- D false: the over-correction. Capacity is planned per cluster, from the cluster average against usable capacity; the hot host is a placement and risk finding, not the capacity input.
- E false: the wrong action. The other five hosts stay below 75% in every row; the load that stays on one host is a pocket (affinity rules, host groups) that more hosts do not spread.
- F true: affinity rules and host groups act as sub-clusters and hold a pocket of load that DRS cannot spread.
- G true: high usage is consumption; whether the VMs on that host waited shows in their contention, such as CPU Ready.
- H false: esx-b23 reaches 95% or more.

## Notes
- Review 2026-11-15: the manager's quote no longer gives the chart's value; A, C and D reworded away from the theory half 0437; H added as a false reading; identical hosts added to the condition. Key unchanged.
- Converted to an export 2026-11-15 (project/practical-questions-as-exports-2026-11-15.md, row 0438): a seeded VCF Operations list view, one row per hour for 7 days, the cluster and its six hosts; the cluster equals the mean of the identical hosts in every row. The export does not show the cause of the hot host (F stays open). A, B, C and H reworded from chart and line to the export's values. The list view CSV format is assumed (project/tools/exportgen/README.md). The key holds for the generated export; the generator checks every condition against the rows.
- Practical half of the new pair D3; theory half: 0437 (design.md, section 3.9).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item D3). Counts only after author approval.

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
answer: [B, C, F, G]
misconception: [A, E]
misconception_type: [average-hides-worst, consumption-as-contention]
pair: "0437"
status: draft
```
