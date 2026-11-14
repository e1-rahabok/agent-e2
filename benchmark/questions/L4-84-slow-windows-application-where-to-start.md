# A slow Windows application: where to start

## Prompt
- The application team says their order-entry application on a Microsoft Windows Server 2022 VM (8 vCPUs, 32 GB) "has been slow lately".
- They send a Task Manager screenshot from this morning: CPU 30%, memory 62%.
- Their monitoring tool shows the VM's daily average CPU at 25% for the last month.
- They ask you to prove VMware vSphere is not the cause, or to give the VM more vCPUs and memory.

Which statements are correct?

- A. Start by pinning down the slowness with the team: which transaction is slow, how slow against normal, and when.
- B. The time window of the slowness becomes the window of every later check, in Windows and in vSphere.
- C. A 25% daily CPU average and 62% memory in Task Manager show the VM has headroom, so resources are not the cause.
- D. In that window, read the Windows wait signs at high resolution: CPU queue, paging, disk queue, network discards.
- E. A wait inside Windows that the VM does not share, such as a disk queue with low VM disk latency, points to the guest.
- F. If Windows shows no wait, or the signs point down, read Ready, Co-stop, memory contention and disk latency of the VM.
- G. Windows cannot see the time a vCPU waits for a physical CPU, so a clean Windows does not prove the VM is healthy.
- H. ESXi cannot see a queue inside Windows, so a VM with no contention does not prove Windows is healthy.
- I. Adding vCPUs and memory first is a safe step; measure afterwards whether the slowness has gone away.
- J. A processor queue with idle vCPUs shrinks when vCPUs are added, since more threads can run at once.
- K. High page-in on its own proves Windows is short of memory, even without page-out or a disk queue.
- L. If the VM's virtual disk latency is fine, the application inside Windows cannot be seeing a storage delay.

## Likely wrong answer
- C: "CPU averages 25% and memory 62%, so the VM has headroom."
- I: "Give it more vCPUs and memory to be safe."

## Expected key points
- Answer: A, B, D, E, F, G, H.
- A true: quantify first; the team describes the symptom in Windows terms.
- B true: the window found by quantifying steers every later step; a daily average or a morning screenshot hides the slow minutes.
- C false: a daily average and one snapshot outside the slow window cannot show a wait; no slow window was found yet.
- D true: the Windows wait signs, read at their highest resolution in the window. Any order.
- E true: IO stuck in the Windows queue never reaches the VM; a wait inside Windows is a Guest OS or application cause (sizing, configuration).
- F true: with no wait in Windows, or every vCPU busy, or a disk queue with high VM disk latency, the wait is below Windows: read the VM.
- G true: a busy vCPU can be waiting for a physical thread; Windows cannot see it.
- H true: the two layers are separate; the VM and ESXi cannot see Windows' queues.
- I false: a queue with idle vCPUs gets worse with more vCPUs (more context switching); read the queues before any change.
- J false: queue high with idle vCPUs means locks, threads that cannot run in parallel or kernel work; more vCPUs make it worse.
- K false: binaries, memory-mapped files and prefetch cause page-in; look for page-in and page-out together with a high disk queue.
- L false: IO waiting in the Windows queue (filter driver, antivirus, application) never reaches the VM, so VM disk latency stays low.

## Notes
- Follows the Windows slow flow (knowledge_main). The key does not require the flow's order of Windows counters: that order is a design choice of the flow.
- No option uses a queue band: whether Guest Peak CPU Queue is per vCPU or a total is open (Q217).
- Converted from judged to multiple choice (Q199 F, 2026-11-14).

## Metadata
```yaml
id: "0262"
title: "A slow Windows application: where to start"
product: [windows, vsphere]
technology: [system, cpu, memory, storage]
task: troubleshoot
level: 400
answer_type: deterministic
answer: [A, B, D, E, F, G, H]
misconception: [C, I]
input: [text]
object: [guest-os, vm]
tool: [guest-os-tools, vcenter]
knowledge:
  - guest-os/system/troubleshooting/ms-windows-slow
  - vsphere/architecture/vm-vs-guest-os
  - guest-os/cpu/metrics/run-queue
  - guest-os/memory/windows-memory
  - guest-os/storage/disk-queue
knowledge_main: guest-os/system/troubleshooting/ms-windows-slow
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
misconception_type: [rollup-and-interval, layer-confusion]
status: reviewed
```
