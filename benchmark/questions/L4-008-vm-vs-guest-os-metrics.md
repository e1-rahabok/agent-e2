# VM vs Guest OS metrics

## Prompt
- The application team complains that their Windows Server 2025 VM (8 vCPUs) was slow at 10:15 this morning.
- Users waited several seconds for each screen.

- You open VCF Operations on the VM object.
- Each value below is the data point at 10:15, which covers 10:10-10:15.
- The 20-second peak counters show the same picture as these values.

| Counter | Value |
|---|---|
| Guest OS Disk Queue | 40 |
| VM Disk Latency | 1 ms |
| Guest\|CPU Queue | 3 |
| VM CPU Ready | 0.5% |
| VM CPU Usage | 35% |
| Guest OS Processor Time (% Processor Time, _Total) | 70% |

Which statements are correct?

- A. Guest OS Disk Queue can be high while VM disk latency is good: IO waiting in Windows has not reached ESXi.
- B. Because VCF Operations shows Guest OS CPU Run Queue on the VM object, it is a VM metric measured by ESXi.
- C. A Guest|CPU Queue of 3 on this VM means about 24 threads were waiting for a vCPU inside Windows.
- D. If VMware Tools is not running, ESXi still reports Guest OS Run Queue from the VM's vCPU activity.
- E. Guest OS Processor Time (70%) and VM CPU Usage (35%) can differ: Windows and the VMkernel calculate them independently.
- F. VM CPU Ready and the Guest|CPU Queue measure the same queue, seen from two angles.

## Answers
A, C, E

## Explanation
- A is correct: VM disk latency starts at the virtual disk; IO queued inside Windows has not been sent to the hypervisor yet, so a guest queue of 40 at 1 ms means most of those requests wait above the virtual disk (40 requests at 1 ms would need about 40,000 IOPS at the virtual disk).
- B is wrong: a counter belongs to the layer that produces it, not to the object that stores it; Windows produces the run queue and VMware Tools carries it to the VM object.
- C is correct: VCF Operations shows the guest CPU queue per vCPU, the guest's total divided by the vCPU count; 3 on 8 vCPUs is about 24 threads in the Windows queue (PerfMon would show the total).
- D is wrong: Guest OS counters come from inside Windows through VMware Tools; without Tools they have no data, and ESXi cannot derive them from vCPU activity.
- E is correct: two kernels compute them independently from different views; VM CPU Usage also moves with Hyper-Threading and frequency, which Windows does not see.
- F is wrong: the run queue is threads waiting for a vCPU inside Windows; Ready is a vCPU waiting for a physical thread in ESXi. Different queues at different layers.
- Misconception: B (data stored on the VM object read as a VM metric) or D (Guest OS counters assumed to come from the hypervisor).

## Notes
- Changed in the 2026-11-15 audit: the run queue row reads the VCF Operations value per vCPU (3, about 24 threads; the old 25 read as 200 threads, Q217); key points one bullet per option with an Answer line; C replaced (the Guest OS cannot see Ready is tested by the pair 0266/0368) by the per-vCPU queue reading (true); the stem's closing instruction dropped (the runner adds it). Needs the author's review.

## Metadata
```yaml
id: "0018"
title: "VM vs Guest OS metrics"
product: [vsphere, windows]
technology: [system]
input: [text]
task: troubleshoot
object: [guest-os, vm]
tool: [vcf-operations, guest-os-tools]
knowledge:
  - vsphere/architecture/vm-vs-guest-os
  - guest-os/storage/disk-queue
  - guest-os/cpu/metrics/run-queue
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/technology/cpu/concepts/guest-os-vs-vm-cpu
knowledge_main: vsphere/architecture/vm-vs-guest-os
attachments: []
origin: synthetic
source_path: "Opening chapter: Think virtual motherboard, not virtual machine; 2026-11-03"
answer_type: deterministic
level: 400                      # author 2026-11-05
misconception: [B, D]
misconception_type: [layer-confusion]
status: draft
```
