# Other Wait on two VMs after the weekend backup

## Prompt
- On Monday morning, VCF Operations shows high CPU Other Wait on two VMs (5-minute averages, 09:00-11:00):
  - fs-02, an 8-vCPU file server: Other Wait 14%, Net Run 45%, Idle 38%. Users say file copies are slow.
  - jump-01, a 2-vCPU jump host nobody used: Other Wait 15%, Net Run 1%, Idle 84%.
- A backup job ran on Sunday. In vCenter, fs-02 still has a snapshot the job created on Sunday at 01:00.
- fs-02 disk latency is about 4 ms. The storage team says the array is healthy.
- The hosts run ESXi 7.0 U3.

Which VM is really waiting, why, and what do you do?

## Likely wrong answer
"Other Wait is IO wait: storage is slow, and both VMs have the same problem."

## Expected key points
- jump-01 is not waiting: with Net Run near 0, Idle and Other Wait add up to about 100%. A known accounting issue on ESXi 7.0.2-7.0.3 inflates the wait of idle VMs (Broadcom KB 85393, KB 338438); it is fixed in later releases (8.0 U3j).
- fs-02 is waiting: it is busy (45% Net Run) and its vCPUs are blocked 14% of the time. The guest sees short freezes.
- The likely cause is the snapshot the backup left: snapshots are a common cause of Other Wait, and every IO now walks the snapshot chain.
- Other Wait is not disk latency: 4 ms and a healthy array do not clear it.
- Delete or consolidate the snapshot off-peak (consolidation briefly stuns the VM), fix the backup job so it removes its snapshots, then read Other Wait again.
- If it stays high after the snapshot is gone: vMotion the VM and update ESXi, virtual hardware and VMware Tools; then open a support request.

## Metadata
```yaml
id: "0108"
title: "Other Wait on two VMs after the weekend backup"
product: [vsphere, vcf-operations]
technology: [cpu, storage]
task: troubleshoot
level: 400
answer_type: judged
input: [text]
object: [vm]
tool: [vcf-operations, vcenter]
knowledge:
  - vsphere/technology/cpu/troubleshooting/vm-other-wait-high
  - vsphere/technology/cpu/metrics/virtual-motherboard/other-wait
  - vsphere/technology/storage/concepts/snapshot-impact
knowledge_main: vsphere/technology/cpu/troubleshooting/vm-other-wait-high
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12 for the CPU slots (project/plan.md, M2)"
misconception_type: [consumption-as-contention, same-name-other-object]
status: draft
```
