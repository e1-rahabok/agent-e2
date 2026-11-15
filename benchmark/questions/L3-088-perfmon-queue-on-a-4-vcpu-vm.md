# Performance Monitor: queue on a 4-vCPU VM

## Prompt
- The owner of a 4-vCPU Windows Server VM says the nightly batch runs slowly and asks for 4 more vCPUs.
- He sends [the Performance Monitor graph of the batch hour](0434/perfmon-cpu-queue-batch-hour.png) and [its report view](0434/perfmon-cpu-queue-batch-hour-report.png).

Which statements are correct?

- A. The Processor Queue Length, sustained above about 2 per vCPU, shows threads waiting for a processor.
- B. Threads already executing on a vCPU are part of the queue figure in the graph.
- C. A rising Context Switches/sec line is reason enough to add vCPUs.
- D. With all 4 vCPUs near 100% and a long queue, the batch wants more CPU time than Windows gets.
- E. Check the VM's CPU Ready and Co-stop for the same hour before adding vCPUs.
- F. Add 4 vCPUs now: a queue above 2 per vCPU settles it.
- G. vCenter shows the VM's CPU Usage at the same value as Windows % Processor Time.
- H. With all four processors this busy, the queue length adds nothing to the diagnosis.
- I. The graph shows the queue at 0 for most of the hour.

## Input to supply
- Product and version: Windows Server 2022 or 2025 in a VM on vSphere 9.1, 4 vCPUs, VMware Tools running, no CPU limit.
- How to produce it: run a CPU load with about 16 busy threads for about an hour (for example Sysinternals CPUSTRES with 16 threads at Maximum activity, or 16 busy-loop jobs in PowerShell).
- Counters (Performance Monitor, a Data Collector Set or a live graph, sample every 15 seconds, about 1 hour): Processor(0), Processor(1), Processor(2), Processor(3) and Processor(_Total) \ % Processor Time; System \ Processor Queue Length; System \ Context Switches/sec.
- Screen 1: the Line view of the hour with all counters and the legend. Save as `0434/perfmon-cpu-queue-batch-hour.png`.
- Screen 2: the Report view of the same data (averages). Save as `0434/perfmon-cpu-queue-batch-hour-report.png`.
- Condition the key depends on: each of the 4 processors at 90-100% % Processor Time for most of the hour; Processor Queue Length above 8 (2 per vCPU) for most of the hour, not only in single spikes; Context Switches/sec visible at any value.
- Masking: mask the computer name and every VM, host, datastore and cluster name.

## Likely wrong answer
F: the queue read as proof that more vCPUs are needed, without the VM's view. Or C: the context switch rate read as a CPU shortage.

## Expected key points
- Answer: A, D, E.
- A true: Windows excludes running threads from the queue, so a queue sustained above about 2 per processor means threads wait for a processor (MSDN reads above 2 sustained as congestion).
- B false: Windows counts threads in the Ready, Standby and Deferred Ready states; running threads are not in the queue (Linux counts them).
- C false: the misconception. A high or rising switch rate is not a CPU shortage on its own; the queue is the counter to read, and more vCPUs can raise switching.
- D true: queue high with every vCPU busy is the case where the workload demands more runtime than the Guest OS gets.
- E true: a vCPU waiting for a physical thread is invisible to Windows; Ready and Co-stop show whether the VM got the runtime it asked for, and more vCPUs on a busy host can raise them.
- F false: the wrong action. The Guest OS view alone does not settle it; VM contention comes first.
- G false: the two are measured in different layers. Windows CPU usage ignores the host's Hyper-Threading; VM CPU Usage, measured by the VMkernel, accounts for it (for example 62.5% for a Windows vCPU at 100% on a shared core).
- H false: the over-correction. Busy processors alone do not show that threads wait; the queue is the primary Guest OS counter for whether the CPU keeps up.
- I false: the queue stays above 8 (2 per vCPU) for most of the hour.

## Notes
- Review 2026-11-15: B, C and H reworded away from the options of 0010; I added as a false reading of the graph. Key unchanged.
- Practical half of 0010 (pair: design.md, section 3.9).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C30). The options hold for any capture that meets the condition above. Counts only after author approval.

## Metadata
```yaml
id: "0434"
title: "Performance Monitor: queue on a 4-vCPU VM"
product: [windows, vsphere]
technology: [cpu]
task: troubleshoot
level: 300
answer_type: deterministic
input: [screenshot]
object: [guest-os, vm]
tool: [guest-os-tools]
knowledge:
  - guest-os/system/troubleshooting/ms-windows-slow
  - guest-os/cpu/metrics/run-queue
  - guest-os/cpu/metrics/context-switch
  - guest-os/cpu/windows-cpu-scheduling
  - vsphere/technology/cpu/concepts/guest-os-vs-vm-cpu
knowledge_main: guest-os/system/troubleshooting/ms-windows-slow
attachments:
  - 0434/perfmon-cpu-queue-batch-hour.png
  - 0434/perfmon-cpu-queue-batch-hour-report.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C30"
answer: [A, D, E]
misconception: [C, F]
misconception_type: [layer-confusion, consumption-as-contention]
pair: "0010"
status: awaiting-input
```
