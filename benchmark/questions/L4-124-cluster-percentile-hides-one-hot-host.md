# Cluster health check: 14 VMs of 200 hide behind the percentile

## Prompt
- Cluster prod-cl11: 8 hosts, 200 powered-on VMs, DRS fully automated. Cluster state green, HA failover capacity met, Cluster DRS Score 91%.
- Cluster CPU Utilization is 46%. Cluster CPU Ready, averaged over all vCPUs, is 0.6%.
- VCF Operations, one hour, per VM, the highest 20-second Ready per vCPU:
  - 14 VMs show 6%. All 14 run on esx-04, which hosts 22 VMs in total.
  - The other 186 VMs show 0.3%.
- Across the 200 VMs, that gives: worst VM 6%, 90th percentile 0.3%, mean 0.70%.
- The team's alert on the cluster fires when the 90th percentile of VM Ready passes 1%, or the mean passes 2%.

Which reading is correct?

- A. The cluster is healthy: only 7% of the VMs are affected, the 90th percentile is 0.3%, and no alert fired.
- B. The cluster needs a performance finding: the worst VM at 6% proves it, and adding a host to the cluster is the first step.
- C. The finding sits on esx-04, where 14 of 22 VMs are affected; the cluster figures dilute it, so the check drills into that host.
- D. DRS Score at 91% shows DRS has already balanced the cluster, so the 14 VMs are a transient and need no check.
- E. The mean of 0.70% is the right cluster figure, and it is below the 2% alert level, so the cluster is healthy.

## Likely wrong answer
A or E: the cluster aggregates are read as the verdict, with a small share of VMs treated as a minor issue.

## Expected key points
- Answer: C.
- A percentile cannot see a group smaller than the remaining share: 14 of 200 is 7%, under the 10% the 90th percentile leaves out, so it reads the unaffected VMs (0.3%). The cluster mean (0.70%) and the cluster average Ready (0.6%) are diluted the same way.
- Depth (the worst VM, 6%) and breadth (how many VMs) must be read together, and the cluster is the entry point, not the end: the 14 VMs are 64% of the VMs on esx-04, a host finding. The next step is that host's VMs: why only there (a hot host and its balance, CPU limits or a resource pool on those VMs, NUMA placement).
- B is wrong: the cluster has 46% utilization and 186 VMs with no wait; a host does not fix a problem confined to one host, and the cause is not yet known.
- D is wrong: the DRS Score measures how well the demand of a VM is met (its execution efficiency), it is not a contention counter, and the cluster value is a weighted average of the VM scores, so it can stay high with a few VMs low. That DRS has not moved the VMs is itself something to check (rules, overrides, migration threshold).
- Averaging the VM values to a cluster figure repeats the mistake: aggregate from the VMs by worst and by percentile, and look at the host.

## Notes
- Public source: vSphere 9.1 Resource Management, VM DRS score (VM DRS score as the execution efficiency of a VM, cluster DRS score as the weighted average of the VM scores; I did not re-open the page, the statement is the one used in question L3-37); VCF Operations peak metrics (Broadcom KB 444403). The arithmetic is in the prompt: mean = (14 x 6 + 186 x 0.3) / 200 = 0.70%; 7% of VMs is below the 10% tail a 90th percentile ignores.
- Why one answer: the numbers show the dilution, and only C names the host where the VMs concentrate. The alert levels are given in the prompt as the team's own, so no threshold is asked.
- Debatable risk: moderate. The 90th percentile, the 1% and 2% alert levels are design choices; they are stated as facts of the scenario, and the key does not rest on them being right, only on what a percentile can and cannot show. The statement that DRS Score is not a contention counter is also covered by question L3-37.
- Rests on: the design logic of the cluster health check (Principle: depth and breadth, averages hide one VM; step 2 aggregation by worst and 90th percentile; step 3 hot host) and the vendor definition of DRS Score.

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
tool: [vcf-operations]
knowledge:
  - vsphere/object-types/cluster/cluster-health-check
  - vsphere/object-types/cluster/concepts/cluster-utilization-vs-contention
  - vsphere/object-types/cluster/troubleshooting/cluster-vm-contention
  - vsphere/object-types/cluster/configuration/drs-migration-levels
knowledge_main: vsphere/object-types/cluster/cluster-health-check
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
answer: [C]
misconception: [A, E]
misconception_type: [average-hides-worst, provider-vs-consumer]
status: draft
```
