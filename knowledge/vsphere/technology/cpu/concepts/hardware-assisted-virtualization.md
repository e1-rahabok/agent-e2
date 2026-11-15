# Hardware-assisted virtualization

Three hardware features assist virtualization: CPU, MMU, and I/O MMU.

## CPU: VT-x (Intel) and AMD-V
- Hardware automatically traps sensitive events and instructions.
- Trap-and-emulate style virtualization is then carried out with hardware help.
- The hardware assist reduces the overhead of handling traps.
- ESXi 6.7 and later do not support software CPU virtualization.

## MMU: Intel EPT and AMD RVI (nested page tables)
- Adds a second level of page tables.
- These tables map VM pages (vendor term: guest physical memory) to ESXi pages (vendor term: host physical memory).
- ESX does not maintain shadow page tables.
- Effects:
  - reduces memory consumption,
  - speeds up workloads where the guest OS modifies page tables often,
  - increases the time to service a TLB miss.
- Workloads that stress the TLB can slow down.
- The increased TLB miss cost can be mitigated with large memory pages (Performance Best Practices for vSphere 9.1, 2MB Large Memory Pages, p. 37): [`vsphere/technology/memory/concepts/large-memory-pages`](../../memory/concepts/large-memory-pages.md).
- ESXi 6.7 and later do not support software MMU virtualization.

## I/O MMU: Intel VT-d and AMD-Vi (IOMMU)
- A chipset feature, not a CPU feature.
- Remaps I/O DMA transfers and device interrupts.
- Lets VMs access hardware I/O devices directly. Examples: network cards, storage controllers (HBAs), GPUs.
- Related options: DirectPath I/O (p. 48) and SR-IOV (p. 49): [`vsphere/technology/network/concepts/passthrough-and-offload`](../../network/concepts/passthrough-and-offload.md).

## Misconceptions
- "Hardware MMU assist is always faster" → it reduces page table overhead, but it increases TLB miss service time. Workloads that stress the TLB can slow down.
- "VT-d is a CPU feature" → it is a chipset feature.

## Metadata
```yaml
id: vsphere/technology/cpu/concepts/hardware-assisted-virtualization
retriever_guide: how-it-works
scope: vsphere
technology:
- cpu
- memory
- storage
- network
pillar:
- performance
product:
- vsphere
object:
- VirtualMachine
- HostSystem
internal_derive: []
related:
- vsphere/technology/cpu/concepts/numa
- vsphere/technology/cpu/configuration/side-channel-scheduling
- vsphere/architecture/overhead
- vsphere/technology/memory/concepts/large-memory-pages
- vsphere/technology/network/concepts/passthrough-and-offload
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: CPU Hardware Considerations > Hardware-Assisted Virtualization (p. 11)
corrections: []
review_notes: []
status: draft
```
