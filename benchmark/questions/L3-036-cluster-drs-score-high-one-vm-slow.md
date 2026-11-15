# A high Cluster DRS Score and one slow VM

## Prompt
- DRS cluster prod-cl02: 10 hosts, 420 powered-on VMs, DRS fully automated, default migration threshold.
- The cluster summary shows a Cluster DRS Score of 92%, steady all morning.
- Since 09:00 the owners of one VM, pay-db-01, report slow queries.

Which statements are correct?

- A. The Cluster DRS Score is a weighted average of the VM DRS Scores of the powered-on VMs.
- B. A Cluster DRS Score above 80% means every VM in the cluster, pay-db-01 included, has a VM DRS Score above 80%.
- C. The VM list under Monitor > vSphere DRS shows each VM's own DRS Score and can be sorted with the lowest first.
- D. vCenter keeps the VM DRS Score in its history at the default statistics level, so pay-db-01's score at 09:00 can be read.
- E. A VM DRS Score below 80% means the VM is waiting for CPU or memory at that moment.
- F. A VM-Host affinity rule can keep DRS from moving a VM whose score is low.
- G. A VM DRS Score reflects how efficiently the VM's demand is being met.
- H. The Cluster DRS Score carries no information about the health of the cluster.
- I. Set the DRS migration threshold to level 1, so that DRS moves pay-db-01 to a host with more room.

## Likely wrong answer
B: reading the cluster score as the state of every VM. Or H, the over-correction: since an average hides one VM, the cluster score is dismissed altogether.

## Expected key points
- Answer: A, C, D, F, G.
- A is true: the cluster score is a weighted average of the VM scores; one VM with a low score barely moves it among 420 VMs.
- B is false: the misconception. A weighted average does not bound any single VM; one VM can score far below 80% while the cluster stays above it.
- C is true: the per-VM list is where a low VM shows behind a high cluster score; sorted by score, the lowest come first.
- D is true: `clusterServices.vmDrsScore` is a level 1 counter, stored by default.
- E is false: a low VM DRS Score reflects execution efficiency, not contention; the VM's own contention counters (Ready, Co-stop, memory contention, disk latency) tell whether it waits.
- F is true: migrations filtered out by affinity or anti-affinity rules, or by VM-host incompatibilities, are causes of a low score that DRS cannot fix by itself.
- G is true: the VM DRS Score is the VM's execution efficiency (VM happiness).
- H is false: the over-correction. Since vSphere 7.0 the Cluster DRS Score is the indicator of cluster balance and health; it only cannot speak for any single VM.
- I is false: the wrong action. At level 1 DRS recommends only mandatory moves (rule violations, hosts entering maintenance mode); it no longer moves VMs to improve resource availability.

## Notes
- Paired with the screenshot question 0433 (design.md, section 3.9).
- Drafted 2026-11-12.
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): A one fact; C ("DRS would already have moved it") and E ("a steady 92% rules out a problem") dropped, as they repeat 0354 D; the VM list (C), the meaning of the VM score (E, G), a cause DRS cannot fix (F), the over-correction (H) and the wrong action (I) added. Key changed from A, D to A, C, D, F, G.
- Cluster DRS Score and VM DRS Score: vSphere 9.1 Resource Management, DRS Score.

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
source_path: "Drafted by Claude 2026-11-12"
answer: [A, C, D, F, G]
misconception: [B, H]
misconception_type: [average-hides-worst]
pair: "0433"
status: draft
```
