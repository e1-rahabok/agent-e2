# Windows processor queue with idle vCPUs

## Prompt
- Windows Server 2022 VM, 8 vCPUs, an in-house order service. Users report slow screens at 11:00-11:30.
- Performance Monitor, 15-second samples, 11:00-11:30:
  - System \ Processor Queue Length: 40-52.
  - Processor(_Total) \ % Processor Time: 33%.
  - Per vCPU % Processor Time: vCPU 0 at 97-100%; vCPUs 1-7 at 15-30%.
  - Processor(_Total) \ % Privileged Time: 24% of the 33%.
- vCenter, same window: VM CPU Ready 0.4% per vCPU, Co-stop 0, CPU Usage about 30%.
- The application owner asks for 8 more vCPUs.

Which statements are correct?

- A. Add the vCPUs: a queue of about 6 threads per processor is far above the guidance of 2, so Windows is short of processors.
- B. A long queue while 7 of 8 vCPUs are mostly idle means the waiting threads cannot use the idle vCPUs (for example, processor affinity); more vCPUs do not shorten it.
- C. Ready at 0.4% shows that ESXi runs the vCPUs when Windows asks; the wait is inside Windows.
- D. Privileged time making up most of the busy time points at kernel or driver work; check the drivers and the DPC and interrupt time on vCPU 0.
- E. The queue is vCPUs waiting for physical CPUs on the host; a CPU reservation for the VM shortens it.
- F. Windows Processor Queue Length includes the threads running on the 8 vCPUs, so only 32-44 threads are waiting.

## Likely wrong answer
A: a long processor queue read as a vCPU shortage. Or E: the Windows queue taken for host CPU contention.

## Expected key points
- Answer: B, C, D.
- A is wrong: the queue guidance holds when the processors are busy. Here 7 vCPUs sit at 15-30%. Adding vCPUs to a queue that idle vCPUs cannot drain adds context switching and can make it worse.
- B is correct: Processor Queue Length counts ready threads only. Ready threads that wait while 7 vCPUs sit idle cannot be scheduled on those vCPUs (affinity, or work bound to vCPU 0): the application or its configuration, not the vCPU count. (A thread blocked on a lock waits, it is not in the queue.)
- C is correct: Ready and Co-stop are low, so the vCPUs get physical CPU time. The queue is a Windows queue, invisible to ESXi.
- D is correct: high privileged time with low user time points at driver or kernel locking; vCPU 0 at 100% with the others idle fits interrupt or DPC work landing on one processor.
- E is wrong: Processor Queue Length is threads waiting for a vCPU inside Windows. Ready is the VM-side wait for a physical CPU, and it is low.
- F is wrong: Windows excludes running threads from Processor Queue Length (Linux includes them). All 40-52 are waiting.

## Notes
- Paired with the Linux load average question: the Windows queue excludes running threads; the Linux run queue includes them.

## Metadata
```yaml
id: "0261"
title: "Windows processor queue with idle vCPUs"
product: [windows, vsphere]
technology: [cpu]
task: decide-capacity
level: 400
answer_type: deterministic
input: [text]
object: [guest-os, vm]
tool: [guest-os-tools, vcenter]
knowledge:
  - guest-os/system/troubleshooting/ms-windows-slow
  - guest-os/cpu/metrics/run-queue
  - guest-os/cpu/metrics/processor-time
  - vsphere/technology/cpu/concepts/guest-os-vs-vm-cpu
knowledge_main: guest-os/cpu/metrics/run-queue
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
answer: [B, C, D]
misconception: [A, E]
misconception_type: [layer-confusion]
status: draft
```
