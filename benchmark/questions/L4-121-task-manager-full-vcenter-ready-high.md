# Task Manager at 100%, vCenter shows a different picture

## Prompt
- The owner of the 4-vCPU Windows Server VM app-win-07 writes: "Task Manager shows 100%. The CPU is maxed out. Give the VM 4 more vCPUs." He attaches [the typeperf export from the guest](0368/typeperf-processor.csv), ten minutes at 20-second samples.
- You export [the vCenter CPU chart of the VM](0368/vcenter-vm-cpu-realtime.csv), Real-time, for the same ten minutes. The VM has no CPU limit.

Which statements are correct?

- A. Task Manager's figure includes the time its vCPUs sat frozen in Ready, which Windows cannot see.
- B. In the vCenter export, Run plus Ready comes to at least 75,000 ms in every row.
- C. In the vCenter export, Run stays below 64,000 ms in every row: under 80% per vCPU.
- D. In the vCenter export, Readiness stays below 5%, so the host gives the VM what it asks.
- E. In the typeperf export, only one of the four processors is busy: the guest runs a single thread.
- F. The two tools disagree this much, so one of the two counters is collected wrongly.
- G. Add 4 vCPUs to the VM: the guest already keeps all four of its processors busy.
- H. Task Manager is of no use on a VM: its CPU figure is simply wrong and can be ignored.
- I. With VMware Tools running, Windows would report the frozen time as steal time.
- J. Next, check the shares of the VM and its resource pool, the host's overcommit and other VMs' Ready.

## Likely wrong answer
G: Task Manager shows the CPU maxed out, so the VM needs more vCPUs. Or F: the tools disagree, so one is wrong.

## Expected key points
- Answer: A, B, C, J.
- A true: a frozen vCPU stays in the state it was in; Windows has no steal accounting, so a busy vCPU's frozen time counts as busy. The typeperf `% Processor Time` of each processor (93.8-100 in every row) matches Run + Ready + Co-stop of the vCenter export, not Run.
- B true: reading. `Run for app-win-07` + `Ready for app-win-07` is at least 75,000 ms in every row, of the 80,000 ms that four vCPUs hold per 20-second sample (Ready is summed over the vCPUs); `Wait for app-win-07` stays small. The vCPUs wanted to run nearly all the time and ran for only part of it.
- C true: reading. `Run for app-win-07` stays between 54,570 and 59,690 ms in every row (68-75% per vCPU); Ready takes a fifth or more of the time, so Run cannot reach the figure Task Manager shows.
- D false: reading. `Readiness for app-win-07` stays between 23.00% and 27.54% in every row.
- E false: reading. `Processor(0)` to `Processor(3)` `% Processor Time` are all 93.8-100 in every row.
- F false: the misconception. The tools count at different layers: the guest kernel cannot see the time it was frozen, vSphere can.
- G false: the wrong action. The vCPUs wait for physical threads; more vCPUs on a busy host are harder to schedule and tend to raise Ready and Co-stop.
- H false: over-correction. Each layer shows its own problems (run queue, processes); read both, each at its own layer.
- I false: Windows has no steal time; VMware Tools does not change that.
- J true: with no limit (`Max limited for app-win-07` is 0 in every row), Ready comes from low shares on the VM or its resource pool, or from the host's load; many VMs in Ready at once points to an overcommitted host.

## Reasoning path
1. Readiness at a fifth to a third of each sample: the vCPUs wait for physical threads.
2. Task Manager and typeperf cannot see that wait, so they read near 100% on all four processors: Run plus Ready, not Run.
3. The cure is the VM's shares or the host's load and placement, not the vCPU count.

## Notes
- Key-point ranges tightened 2026-11-16 (re-review) to the export as generated: Run 54,570-59,690 ms, Readiness 23.00-27.54%, each processor 93.8-100.
- Paired with the theory question 0266 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C1). Counts only after author approval.
- Review 2026-11-15: stem no longer quotes the value; screen readings added (C true; D, E false); J names the VM's shares as a VM-side check. Key changed from A, B, C, F, I to A, B, C, J (options relettered).
- Changed in the 2026-11-15 audit: J names the resource pool too; A, B, F, G and H reworded to similar lengths (the correct options were the longest); B states the reading only (at least 75,000 ms, as the export guarantees).
- Converted to exports 2026-11-15 (project/practical-questions-as-exports-2026-11-15.md): Task Manager has no export, so its figure stays in the owner's words; typeperf carries the per-processor reading. B (the Ready definition, also in 0009, 0376 and 0381) became a reading of Run plus Ready, the partner's fact (Windows busy figure close to Run plus Ready); still true. C, D, E read from the exports; truth unchanged.

## Metadata
```yaml
id: "0368"
title: "Task Manager at 100%, vCenter shows a different picture"
product: [vsphere, windows]
technology: [cpu]
task: troubleshoot
level: 400
answer_type: deterministic
input: [table]
object: [vm, guest-os, esxi]
tool: [vcenter, guest-os-tools]
knowledge:
  - vsphere/technology/cpu/concepts/guest-os-vs-vm-cpu
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/technology/cpu/concepts/vcpu-states
  - vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high
knowledge_main: vsphere/technology/cpu/concepts/guest-os-vs-vm-cpu
attachments:
  - 0368/typeperf-processor.csv
  - 0368/vcenter-vm-cpu-realtime.csv
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C1"
answer: [A, B, C, J]
misconception: [F, G]
misconception_type: [layer-confusion, tool-confusion]
pair: "0266"
status: draft
```
