# A slow Windows application: where to start

## Prompt
- The application team says their order-entry application on a Microsoft Windows Server 2022 VM (8 vCPUs, 32 GB) "has been slow lately".
- They send a Task Manager screenshot from this morning: CPU 30%, memory 62%.
- Their monitoring tool shows the VM's daily average CPU at 25% for the last month.
- They ask you to prove VMware vSphere is not the cause, or to give the VM more vCPUs and memory.

Where do you start, what do you ask them to measure, and how do you decide whether the cause is inside Windows or below it?

## Likely wrong answer
"CPU averages 25% and memory 62%, so the VM has headroom" (no slow window found). Or: "Give it more vCPUs and memory to be safe."

## Expected key points
- Start by quantifying the slowness with the application team: which transaction is slow, how slow against normal, and when (a time, a schedule, or all the time).
- That time window drives every later check, in Windows and in vSphere. A daily average or a morning screenshot hides the slow minutes.
- Read the Windows queues at high resolution in the window (Performance Monitor): CPU queue per processor; paging with the disk queue and % Committed Bytes In Use; disk queue or latency; network discards. Any order.
- A queue found inside Windows (CPU queue, paging, disk queue with low VM disk latency) is a Windows or application cause: sizing or configuration inside the guest.
- No wait inside Windows, or signs that point down (every vCPU busy, disk queue with high VM disk latency): check the VM in the same window: CPU Ready and Co-stop, memory contention, virtual disk latency, dropped packets.
- Windows cannot see a vCPU waiting for a physical CPU, and ESXi cannot see a queue inside Windows, so both layers are read; neither proves the other healthy.
- Do not add vCPUs or memory before the queues are read: a queue with idle vCPUs gets worse with more vCPUs.

## Notes
- Follows the Windows slow flow (knowledge_main). The key does not require the flow's order of Windows counters: that order comes from a score that is not public.

## Metadata
```yaml
id: "0262"
title: "A slow Windows application: where to start"
product: [windows, vsphere]
technology: [system, cpu, memory, storage]
task: troubleshoot
level: 400
answer_type: judged
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
source_path: "Drafted by Claude 2026-11-12 for the Guest OS slots (project/plan.md, M2)"
misconception_type: [rollup-and-interval, layer-confusion]
status: reviewed
```
