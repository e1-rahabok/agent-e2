# Cluster health check: 14 VMs of 200 hide behind the percentile

## Prompt
- Cluster prod-cl11: 8 hosts, 200 powered-on VMs, DRS fully automated. Cluster state green, HA failover capacity met, Cluster DRS Score 91%.
- Cluster CPU Utilization is 46%. Cluster CPU Ready, averaged over all vCPUs, is 0.6%.
- VCF Operations, one hour, per VM, the highest 20-second Ready per vCPU:
  - 14 VMs show 6%. All 14 run on esx-04, which hosts 22 VMs in total.
  - The other 186 VMs show 0.3%.
- Across the 200 VMs, that gives: worst VM 6%, 90th percentile 0.3%, mean 0.70%.
- The team's alert on the cluster fires when the 90th percentile of VM Ready passes 1%, or the mean passes 2%.

Which readings are correct?

- A. The cluster is healthy: only 7% of the VMs are affected, the 90th percentile is 0.3%, and no alert fired.
- B. The cluster is short of CPU: the worst VM at 6% proves it, so adding a host is the first step.
- C. The finding sits on esx-04, where 14 of its 22 VMs wait; the check drills into that host.
- D. DRS Score at 91% shows DRS has already balanced the cluster, so the 14 VMs are a transient and need no check.
- E. The mean of 0.70% is the right cluster figure, and it is below the 2% alert level, so the cluster is healthy.
- F. With 22 VMs at 6% and 178 at 0.3%, the team's 90th percentile alert would have fired.
- G. The 90th percentile of VM Ready here is above the cluster's average Ready.

## Answers
C, F

## Explanation
- A is wrong: a percentile cannot see a group smaller than the share it leaves out: 14 of 200 is 7%, under the 10% the 90th percentile ignores, so it reads the unaffected VMs. No alert is not a healthy cluster.
- B is wrong: the cluster runs at 46% utilization and 186 VMs show no wait; the wait is confined to one host, so it is not a cluster capacity shortage and a host does not fix it.
- C is correct: 14 of the 22 VMs on esx-04 (64%) wait; the cluster figures dilute a host finding. The next step is that host's VMs: why only there (balance, CPU limits or a resource pool on those VMs, NUMA placement).
- D is wrong: the DRS Score measures execution efficiency, not contention, and the cluster value is a weighted average of the VM scores, so it stays high with a few VMs low. That DRS has not moved the VMs is itself something to check (rules, overrides, migration threshold).
- E is wrong: the mean dilutes the 14 VMs the same way; aggregate the VMs by worst and by percentile, and look at the host.
- F is correct: 22 of 200 is 11%, more than the 10% the 90th percentile leaves out, so the 90th percentile becomes 6%, above the 1% alert level.
- G is wrong: here the 90th percentile (0.3%) is below the cluster average Ready (0.6%), because the few high values lift the average but stay inside the ignored 10%.
- Misconception: A or E: the cluster aggregates are read as the verdict, with a small share of VMs treated as a minor issue.

## Notes
- Synthetic, 2026-11-13, for the coverage gap (project/plan.md).
- Public source: vSphere 9.1 Resource Management, VM DRS score (execution efficiency of a VM; the cluster DRS score is the weighted average of the VM scores); VCF Operations peak metrics (Broadcom KB 444403). The arithmetic in the prompt: mean = (14 x 6 + 186 x 0.3) / 200 = 0.70%.
- The 90th percentile and the 1% and 2% alert levels are the team's design choices, stated as case facts; the key rests only on what a percentile can and cannot show.
- Rests on: cluster-health-check (averages hide one VM; step 2 aggregation by worst and 90th percentile; step 3 hot host) and drs-migration-levels (DRS Score).
- 2026-11-15 audit: B made one false claim (its first half was true); F (the 11% case) and G (percentile below the average) added; `vcenter` added to tool (Cluster DRS Score, cluster state, HA failover capacity).

## Metadata
```yaml
id: "0354"
title: "Cluster health check: 14 VMs of 200 hide behind the percentile"
product: [vsphere, vcf-operations]
technology: [cpu, system]
task: troubleshoot
level: 400
answer_type: deterministic
input: [text]
object: [cluster, esxi, vm]
tool: [vcenter, vcf-operations]
knowledge:
  - vsphere/object-types/cluster/cluster-health-check
  - vsphere/object-types/cluster/concepts/cluster-utilization-vs-contention
  - vsphere/object-types/cluster/cluster-vm-contention
  - vsphere/object-types/cluster/configuration/drs-migration-levels
knowledge_main: vsphere/object-types/cluster/cluster-health-check
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-13"
misconception: [A, E]
misconception_type: [average-hides-worst, provider-vs-consumer]
status: draft
```
