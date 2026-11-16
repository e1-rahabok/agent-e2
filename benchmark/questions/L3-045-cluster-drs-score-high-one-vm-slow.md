# A high Cluster DRS Score and one slow VM

## Prompt
- DRS cluster prod-cl02: 10 hosts, 420 powered-on VMs, DRS fully automated, default migration threshold.
- The cluster summary shows a Cluster DRS Score of 92%, steady all morning.
- Since 09:00 the owners of one VM, pay-db-01, report slow queries.

Which statements are correct?

- A. The Cluster DRS Score is a weighted average of the VM DRS Scores of the powered-on VMs.
- B. A Cluster DRS Score above 80% means every VM in the cluster, pay-db-01 included, has a VM DRS Score above 80%.
- C. The VM list under Monitor > vSphere DRS shows each VM's own DRS Score, sortable lowest first.
- D. vCenter keeps the VM DRS Score in its history at the default statistics level; pay-db-01's score at 09:00 is there.
- E. A VM DRS Score below 80% can only mean the VM waits for CPU or memory at that moment.
- F. A VM DRS Score reflects how efficiently the VM's demand is being met.
- G. The Cluster DRS Score carries no information about the health of the cluster.
- H. Moving the DRS migration threshold to level 1 makes DRS move pay-db-01 to a host with more room.

## Answers
A, C, D, F

## Explanation
- A is correct: the cluster score is a weighted average of the VM scores; one VM with a low score barely moves it among 420 VMs.
- B is wrong: the misconception. A weighted average does not bound any single VM; one VM can score far below 80% while the cluster stays above it.
- C is correct: the per-VM list is where a low VM shows behind a high cluster score; sorted by score, the lowest come first.
- D is correct: `clusterServices.vmDrsScore` is a level 1 counter, stored by default.
- E is wrong: a low VM DRS Score reflects execution efficiency, not contention; the VM's own contention counters (Ready, Co-stop, memory contention, disk latency) tell whether it waits.
- F is correct: the VM DRS Score is the VM's execution efficiency (VM happiness).
- G is wrong: the over-correction. Since vSphere 7.0 the Cluster DRS Score replaces the load-balance metric and indicates cluster health; it only cannot speak for any single VM.
- H is wrong: the wrong action. At level 1 DRS recommends only mandatory moves (rule violations, hosts entering maintenance mode); it does not move VMs to improve resource availability.
- Misconception: B: reading the cluster score as the state of every VM. Or G, the over-correction: since an average hides one VM, the cluster score is dismissed altogether.

## Notes
- Paired with the screenshot question 0433 (design.md, section 3.9).
- Synthetic, 2026-11-12.
- Cluster DRS Score and VM DRS Score: vSphere 9.1 Resource Management, DRS Score; Performance Best Practices for vSphere 9.1, p. 76.
- 2026-11-15 audit: old F (an affinity rule keeps a low-score VM in place) dropped, as 0065 and 0438 test the DRS-blocker fact; "can" no longer appears only in correct options. Letters: A-E unchanged; F dropped; G -> F; H -> G; I -> H.

## Metadata
```yaml
id: "0232"
title: "A high Cluster DRS Score and one slow VM"
product: [vsphere]
technology: [system]
task: troubleshoot
level: 300
answer_type: deterministic
input: [text]
object: [cluster, vm]
tool: [vcenter]
knowledge:
  - vsphere/object-types/cluster/configuration/drs-migration-levels
  - vsphere/tools/vsphere-client/vcenter-statistics
  - vsphere/object-types/cluster/concepts/cluster-utilization-vs-contention
  - vsphere/object-types/cluster/cluster-health-check
knowledge_main: vsphere/object-types/cluster/configuration/drs-migration-levels
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-12"
misconception: [B, G]
misconception_type: [average-hides-worst]
pair: "0433"
status: draft
```
