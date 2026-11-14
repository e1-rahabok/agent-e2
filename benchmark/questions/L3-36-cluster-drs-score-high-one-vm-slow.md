# A high Cluster DRS Score and one slow VM

## Prompt
- DRS cluster prod-cl02: 10 hosts, 420 powered-on VMs, DRS fully automated, default migration threshold.
- The cluster summary shows a Cluster DRS Score of 92%, steady all morning.
- Since 09:00 the owners of one VM, pay-db-01, report slow queries.

Which statements are correct?

- A. The Cluster DRS Score is a weighted average of the VM DRS Scores of the powered-on VMs, so it can stay high while a few VMs score low.
- B. A Cluster DRS Score above 80% means every VM in the cluster, pay-db-01 included, has a VM DRS Score above 80%.
- C. If pay-db-01 were short of resources, DRS would already have moved it, so the cause must be inside the Guest OS.
- D. vCenter keeps the VM DRS Score in its history at the default statistics level, so you can read pay-db-01's score at 09:00.
- E. One VM that suffers lowers a weighted cluster average quickly, so a steady 92% rules out a problem on pay-db-01.

## Likely wrong answer
B or E: reading the cluster score as the state of every VM.

## Expected key points
- Answer: A, D.
- A: the cluster score is an average of the VM scores; one VM with a low score barely moves it among 420 VMs. Check the VM list under Monitor > vSphere DRS, sorted by score, and the VM's own contention counters (Ready, Co-stop, Memory Contention, disk latency).
- B is wrong: a weighted average does not bound any single VM; one VM can score far below 80% while the cluster stays above it.
- C is wrong: DRS may be unable or unwilling to move the VM: VM-Host rules, incompatibility with other hosts, a migration cost above the expected benefit, or a cluster with no better host.
- D: `clusterServices.vmDrsScore` is a level 1 counter, stored by default.
- E is wrong: a weighted average of 420 VMs hides one VM.

## Notes
- Drafted 2026-11-12.
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
knowledge_main: vsphere/object-types/cluster/configuration/drs-migration-levels
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
answer: [A, D]
misconception: [B, E]
misconception_type: [average-hides-worst]
status: draft
```
