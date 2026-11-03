---
id: vsphere-cpu-010
title: "Guest OS run queue, context switch, Windows thread states"
scope: vsphere
area: cpu
input: text
tests: concept
knowledge:
  - vsphere/cpu/concepts/windows-cpu-scheduling
  - vsphere/cpu/metrics/virtual-machine/guest-run-queue
  - vsphere/cpu/metrics/virtual-machine/guest-context-switch
  - vsphere/cpu/concepts/guest-os-vs-vm-cpu
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > CPU > Q7 Guest OS CPU"
status: draft
---

## Prompt
Windows or Linux performance affects application performance. Some of these issues are not visible to the VM.

Choose all the correct sentences:

A. The Guest OS is aware of Hyper-Threading and schedules its processes accordingly.
B. CPU Run Queue has nothing to do with performance, as it is common for Windows and Linux to form a queue.
C. CPU Context Switch does not affect application performance at all. The CPU does it all the time.
D. All else being equal, a longer Windows or Linux CPU queue can affect application performance, as more processes are waiting.
E. Guest OS CPU Context Switch does affect performance: the CPU could complete other tasks instead of switching between processes.
F. In Windows, the processor queue length counter includes thread states such as Ready, Standby and Deferred Ready (Unknown).

## Likely wrong answer
A (Guest OS assumed Hyper-Threading aware), B or C (queue and context switch dismissed as normal).

## Expected key points
- Answer: D, E, F.
- A is wrong: the Guest OS is unaware of host Hyper-Threading.
- B is wrong: Run Queue directly accounts for lack of CPU.
- C is wrong: a context switch swaps the thread out. It is expensive.
- D is correct: queued threads cannot run.
- E is correct: context switch is expensive.
- F: Windows has 8 thread states. Ready, Standby and Deferred Ready measure a CPU problem.

## Notes
- Author confirmed D, E, F (Q036, 2026-11-03). The quiz document's answer column lists D, E only.
