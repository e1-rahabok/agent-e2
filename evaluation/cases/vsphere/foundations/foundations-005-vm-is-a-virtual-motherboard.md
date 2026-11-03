---
id: vsphere-foundations-005
title: "VM (virtual motherboard) vs Guest OS metrics"
scope: vsphere
area: foundations
input: text
tests: distinction
knowledge:
  - vsphere/foundations/vm-vs-guest-os
  - vsphere/storage/metrics/guest-os/disk-queue
  - vsphere/cpu/metrics/guest-os/run-queue
  - vsphere/cpu/metrics/virtual-motherboard/ready
  - vsphere/cpu/concepts/guest-os-vs-vm-cpu
attachments: []
origin: synthetic
source_path: "Author's book, opening chapter: Think virtual motherboard, not virtual machine. Author instruction 2026-11-03."
format: multiple-choice
level: l400
answer: [A, C, E]
trap: [B, D]
status: draft
---

## Prompt
A Windows VM with 8 vCPUs is slow. VCF Operations shows these values on the VM object, averaged over the last hour:

| Counter | Value |
|---|---|
| Guest OS Disk Queue | 40 |
| VM Disk Latency | 1 ms |
| Guest OS CPU Run Queue | 25 |
| VM CPU Ready | 0.5% |
| VM CPU Usage | 35% |
| Guest OS Processor Time (% Processor Time, _Total) | 70% |

Choose all the correct statements. There can be more than one.

A. Guest OS Disk Queue can be high while VM disk latency is good: IO waiting inside Windows has not reached the hypervisor yet.
B. Because VCF Operations shows Guest OS CPU Run Queue on the VM object, it is a VM metric measured by ESXi.
C. VM CPU Ready is invisible to Windows: the Guest OS cannot see time when no physical thread runs its vCPU.
D. If VMware Tools is not running, ESXi still reports Guest OS Run Queue from the VM's vCPU activity.
E. Guest OS Processor Time (70%) and VM CPU Usage (35%) can differ, because two kernels calculate them independently: Windows and the VMkernel.
F. VM CPU Ready and Guest OS Run Queue measure the same queue from two angles.

## Likely wrong answer
B (data stored on the VM object read as a VM metric) or D (Guest OS counters assumed to come from the hypervisor).

## Expected key points
- A VM is a virtual motherboard. The Guest OS is a separate layer running on it.
- Guest OS counters come from inside Windows through VMware Tools; without Tools they do not exist.
- Where a counter is stored (the VM object) does not decide which layer it belongs to.
- Guest OS queues (Run Queue, Disk Queue) and VM contention (Ready, disk latency) are different queues at different layers.
- F is false: Run Queue is threads waiting for a vCPU inside Windows; Ready is a vCPU waiting for a physical thread in ESXi.
