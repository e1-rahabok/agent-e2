# Other Wait on two VMs after the weekend backup

## Prompt
- On Monday morning, VCF Operations shows high CPU Other Wait on two VMs (5-minute averages, 09:00-11:00):
  - fs-02, an 8-vCPU file server: Other Wait 14%, Net Run 45%, Idle 38%. Users say file copies are slow.
  - jump-01, a 2-vCPU jump host nobody used: Other Wait 15%, Net Run 1%, Idle 84%.
- A backup job ran on Sunday. In vCenter, fs-02 still has a snapshot the job created on Sunday at 01:00.
- fs-02 disk latency is about 4 ms. The storage team says the array is healthy.
- fs-02 runs on an ESXi 8.0 Update 3j host; jump-01 runs on an ESXi 8.0 Update 2 host.

Which VM is really waiting, why, and what do you do? Which statements are correct?

- A. fs-02 is really waiting: it is busy and its vCPUs are blocked about 14% of the time.
- B. jump-01 is not waiting: with Net Run near 0, its Idle and Other Wait add up to about 100%.
- C. The snapshot left by the backup on Sunday is the likely cause of the Other Wait on fs-02.
- D. Other Wait is IO wait: the storage is slow, and both VMs suffer from the same storage problem.
- E. A disk latency of 4 ms and a healthy array rule out the snapshot as the cause on fs-02.
- F. jump-01, with the highest Other Wait of the two, is the VM that suffers the most from the wait.
- G. High Other Wait on both VMs points to a host short of CPU: Other Wait tends to rise with Ready.
- H. The Other Wait of fs-02 includes the time its Guest OS sat idle, waiting for file requests.
- I. Remove the snapshot off-peak, fix the backup job so it cleans up, then read Other Wait again.
- J. If Other Wait stays high without the snapshot: vMotion, update ESXi, hardware and Tools, then support.
- K. A faster datastore for jump-01 would likely clear its Other Wait within a few samples.
- L. Updating jump-01's host to ESXi 8.0 Update 3j or later should move its Other Wait back into Idle.
- M. VCF Operations CPU Contention for jump-01 includes its 15% Other Wait in full.

## Answers
A, B, C, I, J, L

## Explanation
- A is correct: 45% Net Run with 14% Other Wait: a busy VM whose vCPUs are blocked. Its host runs ESXi 8.0 Update 3j, where the idle-accounting issue is fixed, so the 14% is not halted time.
- B is correct: 1% + 84% + 15% = 100%: when Run is low, Idle and Other Wait add up to about 100% by accounting. jump-01's host runs ESXi 8.0 Update 2, inside the range of the known accounting issue (ESXi 7.0 Update 2 and later, fixed in 8.0 Update 3j; Broadcom KB 338438, legacy 85393), where halted time is not always counted as Idle.
- C is correct: snapshots are a common cause of Other Wait, and every IO now walks the snapshot chain.
- D is wrong: Other Wait showed no correlation with disk latency or outstanding IO; jump-01 is idle, not waiting.
- E is wrong: Other Wait is not disk latency; a low latency and a healthy array do not clear the snapshot.
- F is wrong: jump-01 does almost no work; its Other Wait is accounting on an idle VM.
- G is wrong: Other Wait showed no correlation with Ready; it is a vCPU blocked in the VMM, not one waiting for a physical thread.
- H is wrong: Other Wait = Wait - Idle - Swap Wait: idle time is excluded.
- I is correct: the snapshot is a configuration that can be removed now; reading Other Wait again confirms the cause.
- J is correct: the flow's next steps after the snapshot: vMotion, then update ESXi (to 8.0 Update 3j or later where the build is older), virtual hardware and VMware Tools; the low-level causes need debug data from Broadcom support.
- K is wrong: jump-01 is not waiting for anything, and Other Wait does not follow disk latency.
- L is correct: the fix in ESXi 8.0 Update 3j counts halted vCPU time as Idle again, so the idle jump host's Other Wait falls and its Idle rises.
- M is wrong: CPU Contention adds Other Wait only when it is below 1%, a condition set for exactly this accounting issue on idle VMs.
- Misconception: D: "Other Wait is IO wait: storage is slow, and both VMs have the same problem." - F: "jump-01 has the highest Other Wait, so it is the worst VM."

## Notes
- Converted from judged to multiple choice (Q199 F, 2026-11-14). Dropped from the old key: "consolidation briefly stuns the VM" (no knowledge file states it).
- 2026-11-15 audit: the knowledge base now names the builds of the accounting issue (other-wait, idle, vm-other-wait-high: ESXi 7.0 Update 2 and later, fixed in 8.0 Update 3j). The stem splits the hosts (fs-02 on 8.0 Update 3j, jump-01 on 8.0 Update 2; ESXi 7.0 U3 is past general support), so A is decided and B stays true. L (the update fixes jump-01's accounting) and M (Contention adds Other Wait only below 1%) added; G and K reworded so hedges sit in wrong options too (truth kept).

## Metadata
```yaml
id: "0108"
title: "Other Wait on two VMs after the weekend backup"
product: [vsphere, vcf-operations]
technology: [cpu, storage]
task: troubleshoot
level: 400
answer_type: deterministic
misconception: [D,F]
input: [text]
object: [vm]
tool: [vcf-operations, vcenter]
knowledge:
  - vsphere/technology/cpu/troubleshooting/vm-other-wait-high
  - vsphere/technology/cpu/metrics/virtual-motherboard/other-wait
  - vsphere/technology/storage/concepts/snapshot-impact
  - vsphere/technology/cpu/metrics/virtual-motherboard/idle
  - vsphere/technology/cpu/metrics/virtual-motherboard/contention
knowledge_main: vsphere/technology/cpu/troubleshooting/vm-other-wait-high
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-12"
misconception_type: [consumption-as-contention, same-name-other-object]
status: draft
```
