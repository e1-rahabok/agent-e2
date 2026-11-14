# Cluster at 70%, one host near 100%

## Prompt
- The capacity manager plans to place 40 new VMs on a cluster. He sends [the cluster CPU chart of last week](0438/vcf-operations-cluster-cpu-usage-7-days.png): "The cluster never passed about 70%, so no host did either. There is room."
- You add [the CPU usage of each host for the same week](0438/vcf-operations-hosts-cpu-usage-7-days.png).

Which statements are correct?

- A. No host ran above about 70% last week, so every host has room for more VMs.
- B. At the cluster's busiest hours, one host ran near 100% while the cluster line stayed near 70%.
- C. The cluster line is the average of its hosts at each point.
- D. Plan the cluster's capacity on the hot host's peak: the cluster is full.
- E. Add hosts before placing the 40 VMs, since one host reached 100%.
- F. Check why the load stays on one host: VM-Host rules, the DRS automation level, VMs that cannot move.
- G. The VMs on the hot host may wait for CPU at those hours; their CPU Ready shows whether they did.

## Input to supply
- Product and version: VCF Operations 9.1, a vSphere 9.1 cluster with DRS (6-8 hosts).
- How to produce it in a lab: a "must run on" VM-Host rule that keeps a group of CPU-burner VMs on one host, with their vCPUs about equal to that host's physical threads; the other hosts carry a lighter load. Run the burners at business hours on several days of the week.
- Screen 1: the cluster > Metrics, CPU|Usage (%), last 7 days. Save as `0438/vcf-operations-cluster-cpu-usage-7-days.png`.
- Screen 2: the hosts of the cluster on one chart (or a list view with Maximum over the 7 days), metric CPU|Usage (%), same 7 days. Save as `0438/vcf-operations-hosts-cpu-usage-7-days.png`.
- Condition the key depends on: the cluster's CPU|Usage (%) peaks between 65% and 72%; one host reaches 95% or more at the cluster's busiest hours; the other hosts stay mostly below 75%.
- Masking: mask every VM, host, datastore and cluster name, including names in chart titles and legends.

## Likely wrong answer
A: the cluster peak read as a ceiling for every host. Or E: one host at 100% read as a cluster short of capacity.

## Expected key points
- Answer: B, C, F, G.
- A false: the misconception. The average of the hosts at each point hides a host near 100%.
- B true: the host chart shows one host at 95% or more at the hours when the cluster line peaks below about 72%.
- C true: cluster utilization is an average across hosts; for it to reach 70%, at least one host was above 70%.
- D false: the over-correction. Capacity is planned per cluster, from the cluster average against usable capacity; the hot host is a placement and risk finding, not the capacity input.
- E false: the wrong action. The other hosts have room; more hosts do not move load that stays on one host.
- F true: affinity rules and host groups act as sub-clusters and hold a pocket of load that DRS cannot spread.
- G true: high usage is consumption; whether the VMs on that host waited shows in their contention, such as CPU Ready.

## Notes
- Practical half of the new pair D3; theory half: 0437 (design.md, section 3.9).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item D3). The options hold for any capture that meets the condition above. Counts only after author approval.

## Metadata
```yaml
id: "0438"
title: "Cluster at 70%, one host near 100%"
product: [vcf-operations, vsphere]
technology: [cpu, system]
task: decide-capacity
level: 400
answer_type: deterministic
input: [screenshot]
object: [cluster, esxi]
tool: [vcf-operations]
knowledge:
  - sp5-framework/observability/aggregation
  - sp5-framework/concepts/performance-vs-capacity
  - sp5-framework/capacity/supply
  - vsphere/object-types/cluster/configuration/drs-migration-levels
knowledge_main: sp5-framework/observability/aggregation
attachments:
  - 0438/vcf-operations-cluster-cpu-usage-7-days.png
  - 0438/vcf-operations-hosts-cpu-usage-7-days.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D3"
answer: [B, C, F, G]
misconception: [A, E]
misconception_type: [average-hides-worst, consumption-as-contention]
pair: "0437"
status: awaiting-input
```
