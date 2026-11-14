# Other Wait on two VMs after the weekend backup

## Prompt
- On Monday morning, VCF Operations shows high CPU Other Wait on two VMs (5-minute averages, 09:00-11:00):
  - fs-02, an 8-vCPU file server: Other Wait 14%, Net Run 45%, Idle 38%. Users say file copies are slow.
  - jump-01, a 2-vCPU jump host nobody used: Other Wait 15%, Net Run 1%, Idle 84%.
- A backup job ran on Sunday. In vCenter, fs-02 still has a snapshot the job created on Sunday at 01:00.
- fs-02 disk latency is about 4 ms. The storage team says the array is healthy.
- The hosts run ESXi 7.0 U3.

Which VM is really waiting, why, and what do you do? Which statements are correct?

- A. fs-02 is really waiting: it is busy, and its vCPUs are blocked about 14% of the time, felt as short freezes.
- B. jump-01 is not waiting: with Net Run near 0, its Idle and Other Wait add up to about 100%.
- C. The snapshot left by the backup on Sunday is the likely cause of the Other Wait on fs-02.
- D. Other Wait is IO wait: the storage is slow, and both VMs suffer from the same storage problem.
- E. A disk latency of 4 ms and a healthy array rule out the snapshot as the cause on fs-02.
- F. jump-01, with the highest Other Wait of the two, is the VM that suffers the most from the wait.
- G. High Other Wait on both VMs points to a host short of CPU, since Other Wait rises with Ready.
- H. The Other Wait of fs-02 includes the time its Guest OS sat idle, waiting for file requests.
- I. Remove or consolidate the snapshot off-peak, fix the backup job so it cleans up, then read Other Wait again.
- J. If Other Wait stays high once the snapshot is gone: vMotion the VM, update ESXi, virtual hardware and Tools, then call support.
- K. Moving jump-01 to a faster datastore would clear its Other Wait, as its IO would complete sooner.

## Likely wrong answer
- D: "Other Wait is IO wait: storage is slow, and both VMs have the same problem."
- F: "jump-01 has the highest Other Wait, so it is the worst VM."

## Expected key points
- Answer: A, B, C, I, J.
- A true: 45% Net Run with 14% Other Wait: a busy VM whose vCPUs are blocked.
- B true: 1% + 84% + 15% = 100%: when Run is low, Idle and Other Wait add up to about 100% by accounting (a known accounting issue inflates the wait of idle VMs: Broadcom KB 85393, KB 338438).
- C true: snapshots are a common cause of Other Wait, and every IO now walks the snapshot chain.
- D false: Other Wait showed no correlation with disk latency or outstanding IO; jump-01 is idle, not waiting.
- E false: Other Wait is not disk latency; a low latency and a healthy array do not clear the snapshot.
- F false: jump-01 does almost no work; its Other Wait is accounting on an idle VM.
- G false: Other Wait showed no correlation with Ready; it is a vCPU blocked in the VMM, not one waiting for a physical thread.
- H false: Other Wait = Wait - Idle - Swap Wait: idle time is excluded.
- I true: the snapshot is a configuration that can be removed now; reading Other Wait again confirms the cause.
- J true: the known accounting issue and the low-level causes need build updates and debug data from Broadcom.
- K false: jump-01 is not waiting for anything, and Other Wait does not follow disk latency.

## Notes
- Converted from judged to multiple choice (Q199 F, 2026-11-14). Dropped from the old key: the affected and fixed ESXi builds of the accounting issue (no knowledge file names them) and "consolidation briefly stuns the VM" (no knowledge file states it).

## Metadata
```yaml
id: "0108"
title: "Other Wait on two VMs after the weekend backup"
product: [vsphere, vcf-operations]
technology: [cpu, storage]
task: troubleshoot
level: 400
answer_type: deterministic
answer: [A,B,C,I,J]
misconception: [D,F]
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
source_path: "Drafted by Claude 2026-11-12"
misconception_type: [consumption-as-contention, same-name-other-object]
status: draft
```
