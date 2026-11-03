# VM CPU System

## Meaning
- CPU time the hypervisor spends on behalf of the VM: privileged instructions and IO commands.
- Unit: ms. Charged to the VM. Part of the VM's VMX world.

## Mechanism
- IO is processed twice: first by the Guest OS storage subsystem, then by the hypervisor storage subsystem.
- IP-based storage adds ESXi network stack processing.
- ESXi typically uses another core for this work and puts the vCPU in a wait state.
- Run does not include this work. It must be charged back to the VM.
- The Guest OS does not see the second processing. It sees a slower disk.
- Snapshots add work: the kernel traverses the snapshot chain.
- ESXi processes IO for all VMs issuing IO at that time. It may serialize random IO into sequential IO.
![IO is processed twice: Guest OS first, then VMkernel; System is charged at VM level](../../images/vm-cpu-system-io-processed-by-guest-os-and-vmkernel.png)

## Instance
- Not available per vCPU. The physical core doing the IO may serve more than one vCPU. No breakdown is possible.
- In vCenter, selecting System shows no per-vCPU instances.
- System is charged to vCPU 0. vCPU 0 can show higher Used than the others while Run is balanced. This is accounting, not a scheduling problem.

## Scope
- CPU accounting only, not storage accounting.
- Since vSphere 6.5, Storage vMotion effort is not charged to the VM being moved.

## Values
- Most VMs: System below 0.5 vCPU most of the time (2,431 VMs observed).
- IO-intensive VMs such as NSX Edge: System is noticeable (Broadcom KB 59640). Adding vCPUs makes performance worse.
- The System counter in Linux differs from System in vSphere.

## Traps
- "Higher Used on vCPU 0 is a scheduling imbalance" → System is charged to vCPU 0.
- "Add vCPUs to a high-System VM" → for NSX Edge it makes performance worse.
- "Guest OS System = VM System" → different counters.

## Metadata
```yaml
id: vsphere/cpu/metrics/virtual-machine/system
retriever_guide: metric-meaning
scope: vsphere
technology:
- cpu
pillar:
- performance
- capacity
product:
- vsphere
object:
- VirtualMachine
metric_class: consumption
internal_derive:
- vsphere/foundations/kernel-worlds
same_name: []
same_meaning: []
related:
- vsphere/cpu/metrics/virtual-machine/used
- vsphere/cpu/metrics/virtual-machine/usage
- vsphere/cpu/metrics/virtual-machine/overlap
- vsphere/cpu/concepts/guest-os-vs-vm-cpu
images:
  - path: ../../images/vm-cpu-system-io-processed-by-guest-os-and-vmkernel.png
    product: [vsphere]
    object: [VirtualMachine]
    metric: ['VM CPU System']
    image_type: diagram
source:
  document: PART 3 - Counters.docx
  path: CPU > VM (pp. 78-118) > Consumption Metrics > System
corrections: []
review_notes:
- 'Section ''Instance'': the book text says System is charged to vCPU 0, while its diagram says charged at VM level, not at vCPU 1, and Chapter 1 says per-vCPU Used excludes System. Open question in docs/author-questions.md.'
- 'Section ''Values'': KB from the book: https://kb.vmware.com/s/article/59640 (not read).'
- 'vCenter counter description reads: amount of time spent on system processes on each virtual CPU in the virtual machine. Differs from the book''s per-vCPU statement.'
status: draft
```
