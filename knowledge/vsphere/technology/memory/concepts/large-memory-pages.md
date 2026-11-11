# Large memory pages (2 MB)

## Definition
- ESX provides 4 KB pages and 2 MB pages.
- The source calls 2 MB pages "large pages". It does not cover 1 GB pages.

## ESX behaviour
- ESX backs guest memory with 2 MB ESXi pages (vendor term: machine pages) whenever possible.
- ESX does this even when the guest OS does not request large pages.

## Full benefit requires the guest
- The full benefit requires the guest OS and applications to use large pages as well.
- Guest OS and application configuration: see the guest OS documentation.
- The source says an OS or application that benefits from large pages on native hardware can achieve a similar improvement on a VM backed by 2 MB machine pages.

## Effect
- Large pages significantly reduce TLB misses.
- This improves the performance of most workloads, especially workloads with large active memory working sets.
- Large pages can slightly reduce the per-VM memory overhead. See [`vsphere/technology/memory/concepts/memory-overhead`](memory-overhead.md).
- Background on TLB misses in nested paging: see [`vsphere/technology/cpu/concepts/hardware-assisted-virtualization`](../../cpu/concepts/hardware-assisted-virtualization.md).

## Interaction with page sharing
- ESX does not share large pages. See [`vsphere/technology/memory/concepts/page-sharing`](page-sharing.md).
- Large pages can change sharing behaviour. Page sharing might not occur until overcommitment is high enough to force large pages to break into small pages.

## 1 GB pages
- ESXi backs VM memory with 2 MB pages by default. 1 GB pages are opt-in per VM: sched.mem.lpage.enable1GPage = TRUE, set while powered off.
- A 1 GB page VM powers on only with a full memory reservation. All its memory is preallocated at power-on and never reclaimed: Consumed stays at the configured size for the VM's lifetime.
- Backing is best effort: host memory fragments over time, so 1 GB pages are most likely on a freshly booted host.
- After vMotion, part of the memory may no longer be backed by 1 GB pages. DRS and HA ignore 1 GB capability in placement.
- 1 GB page VMs are excluded from memory tiering.
- The guest gains most when it also uses large pages. Hypervisor-only large pages still reduce TLB misses.

## Misconceptions
- "Large pages in ESX are enough" → the guest OS and applications must use large pages for the full benefit.
- "Large pages make page sharing more effective" → ESX does not share large pages.

## Metadata
```yaml
id: vsphere/technology/memory/concepts/large-memory-pages
retriever_guide: how-it-works
scope: vsphere
technology:
- memory
- cpu
pillar:
- performance
product:
- vsphere
object:
- HostSystem
- VirtualMachine
internal_derive: []
related:
- vsphere/technology/memory/concepts/page-sharing
- vsphere/technology/memory/concepts/memory-overhead
- vsphere/technology/cpu/concepts/hardware-assisted-virtualization
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: ESX Memory Considerations > 2MB Large Memory Pages (pp. 37-38); Guest Operating System Memory Considerations (p. 59)
corrections: []
review_notes:
- 'Section ''1 GB pages'': from the vSphere 9.1 documentation, vSphere Resource Management > Support for Large Page Sizes, Backing Guest vRAM with 1 GB Pages, Memory Tiering VM profiles (pp. 1837, 1846, 1947-1948).'
- Checked against 9.1 (revision 20260624). Pages 37-38 unchanged. Guest page reference now p. 59.
- 'Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices'
- Source uses 'large pages' only for 2 MB pages. It says 1 GB pages exist on some CPUs but are out of its scope.
status: draft
```
