# VM (virtual motherboard) vs Guest OS metrics

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
| Guest OS CPU Run Queue | 25 |
| VM CPU Ready | 0.5% |
| VM CPU Usage | 35% |
| Guest OS Processor Time (% Processor Time, _Total) | 70% |

Choose all the correct statements. There can be more than one.

- A. Guest OS Disk Queue can be high while VM disk latency is good: IO waiting inside Windows has not reached the hypervisor yet.
- B. Because VCF Operations shows Guest OS CPU Run Queue on the VM object, it is a VM metric measured by ESXi.
- C. VM CPU Ready is invisible to Windows: the Guest OS cannot see time when no physical thread runs its vCPU.
- D. If VMware Tools is not running, ESXi still reports Guest OS Run Queue from the VM's vCPU activity.
- E. Guest OS Processor Time (70%) and VM CPU Usage (35%) can differ, because two kernels calculate them independently: Windows and the VMkernel.
- F. VM CPU Ready and Guest OS Run Queue measure the same queue from two angles.

## Likely wrong answer
B (data stored on the VM object read as a VM metric) or D (Guest OS counters assumed to come from the hypervisor).

## Expected key points
- A VM is a virtual motherboard. The Guest OS is a separate layer running on it.
- Guest OS counters come from inside Windows through VMware Tools; without Tools they do not exist.
- Where a counter is stored (the VM object) does not decide which layer it belongs to.
- Guest OS queues (Run Queue, Disk Queue) and VM contention (Ready, disk latency) are different queues at different layers.
- F is false: Run Queue is threads waiting for a vCPU inside Windows; Ready is a vCPU waiting for a physical thread in ESXi.

## Notes
- Previous id: vsphere-foundations-005 (renamed 2026-11-05).

## Metadata
```yaml
id: "0018"
title: "VM (virtual motherboard) vs Guest OS metrics"
product: [vsphere, windows]
technology: [system]
input: [text]
task: troubleshoot
knowledge:
  - vsphere/architecture/vm-vs-guest-os
  - guest-os/storage/disk-queue
  - guest-os/cpu/metrics/run-queue
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/technology/cpu/concepts/guest-os-vs-vm-cpu
attachments: []
origin: synthetic
source_path: "Author's book, opening chapter: Think virtual motherboard, not virtual machine. Author instruction 2026-11-03."
answer_type: deterministic
level: 400                      # author 2026-11-05
answer: [A, C, E]
misconception: [B, D]
status: reviewed
```
