# Guest OS run queue, context switch, Windows thread states

## Prompt
An application team runs Windows and Linux VMs and asks how to read the guest CPU counters. Which statements are correct?

- A. The Guest OS is aware of Hyper-Threading and schedules its processes accordingly.
- B. VCF Operations Guest|CPU Queue for a VM shows the same value as Windows Processor Queue Length.
- C. A high context switch rate calls for more vCPUs.
- D. Windows Processor Queue Length leaves out the running threads; the Linux run queue counts them.
- E. A context switch costs CPU time that could otherwise run application work.
- F. In Windows, the queue counts threads in the Ready, Standby and Deferred Ready (Unknown) states.
- G. A thread blocked on a lock adds to the Windows processor queue length.
- H. A sustained queue of 1 thread per vCPU is reason enough to add vCPUs.

## Answers
D, E, F

## Explanation
- A is false: the Guest OS is unaware of host Hyper-Threading.
- B is false: both VCF Operations queue metrics are the guest's total queue divided by the vCPU count; multiply by the vCPU count to compare with PerfMon.
- C is false: a high switch rate is not a CPU shortage; check the run queue. More vCPUs can raise switching.
- D is true: Windows excludes running threads from the queue; Linux includes them.
- E is true: a switch costs scheduler work, TLB flushes and cache reloads.
- F is true: Ready, Standby and Deferred Ready all indicate a CPU problem, and all three are in the counter.
- G is false: a thread blocked on a lock is in the Wait state; it joins the queue only when the lock is released.
- H is false: 1 per vCPU is below MSDN's 2 per processor sustained and PerfMon's 10 per processor; and before adding vCPUs, VM CPU contention is checked first.
- Misconception: A (the Guest OS assumed to know about Hyper-Threading), B (the VCF Operations queue taken for the PerfMon total), or C (a high switch rate read as a CPU shortage).

## Notes
- Hint moved out of the prompt (author, 2026-11-14: a hint helps the frontier model, not the local model), for reviewers: "Windows or Linux performance affects application performance. Some of these issues are not visible to the VM."
- Changed in the 2026-11-15 audit: stem anchored to a situation; throwaway B replaced by the per-vCPU scale of the VCF Operations queue (run-queue, Misconceptions line 1); H reworded to a wrong action so it stays false against windows-cpu-scheduling "Ready should be near 0".

## Metadata
```yaml
id: "0010"
title: "Guest OS run queue, context switch, Windows thread states"
product: [vsphere, windows, linux, vcf-operations]
technology: [cpu]
input: [text]
task: read-metric
object: [guest-os]
tool: [guest-os-tools, vcf-operations]
knowledge:
  - guest-os/cpu/windows-cpu-scheduling
  - guest-os/cpu/metrics/run-queue
  - guest-os/cpu/metrics/context-switch
  - vsphere/technology/cpu/concepts/guest-os-vs-vm-cpu
  - guest-os/system/troubleshooting/ms-windows-slow
knowledge_main: guest-os/cpu/windows-cpu-scheduling
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > CPU > Q7 Guest OS CPU"
answer_type: deterministic
level: 300                      # author 2026-11-05
misconception: [A, B, C]
misconception_type: [layer-confusion, frequency-and-hyper-threading, unit-and-normalization]
pair: "0434"
status: draft
```
