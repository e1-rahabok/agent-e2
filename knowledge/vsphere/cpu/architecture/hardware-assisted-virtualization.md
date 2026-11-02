---
id: vsphere/cpu/architecture/hardware-assisted-virtualization
type: concept
scope: vsphere
resources: [cpu, memory, storage, network]
objects: [vm, esxi]
related:
  - vsphere/cpu/architecture/numa
  - vsphere/cpu/architecture/side-channel-scheduling
  - vsphere/foundations/overhead
source:
  document: Performance Best Practices for VMware vSphere 9.0 (revision 20250731)
  path: CPU Hardware Considerations > Hardware-Assisted Virtualization (p. 12)
corrections: []
review_notes:
  - "Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-90-performance-best-practices"
  - "Not read: 2MB Large Memory Pages (p. 35), DirectPath I/O (p. 46), SR-IOV (p. 46), AES-NI Support (p. 13)."
status: draft
---

# Hardware-assisted virtualization

Three hardware features assist virtualization: CPU, MMU, and I/O MMU.

## CPU: VT-x (Intel) and AMD-V
- Hardware automatically traps sensitive events and instructions.
- Trap-and-emulate style virtualization is then carried out with hardware help.
- The hardware assist reduces the overhead of handling traps.
- ESXi 6.7 and later do not support software CPU virtualization.

## MMU: Intel EPT and AMD RVI (nested page tables)
- Adds a second level of page tables.
- These tables map guest physical memory to host physical memory.
- ESX does not maintain shadow page tables.
- Effects:
  - reduces memory consumption,
  - speeds up workloads where the guest OS modifies page tables often,
  - increases the time to service a TLB miss.
- Workloads that stress the TLB can slow down.
- The increased TLB miss cost can be mitigated with large memory pages. See the source section "2MB Large Memory Pages" (p. 35).
- ESXi 6.7 and later do not support software MMU virtualization.

## I/O MMU: Intel VT-d and AMD-Vi (IOMMU)
- A chipset feature, not a CPU feature.
- Remaps I/O DMA transfers and device interrupts.
- Lets VMs access hardware I/O devices directly. Examples: network cards, storage controllers (HBAs), GPUs.
- Related options: DirectPath I/O and SR-IOV (p. 46).

## Traps
- "Hardware MMU assist is always faster" → it reduces page table overhead, but it increases TLB miss service time. Workloads that stress the TLB can slow down.
- "VT-d is a CPU feature" → it is a chipset feature.
