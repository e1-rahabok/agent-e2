# VM Memory Consumed

## Meaning
- Excludes overhead.
- Includes reserved memory only once the VM has touched it: a reservation alone does not raise Consumed. See [`vsphere/architecture/resource-controls`](../../../../architecture/resource-controls.md).
- Relevance for operations: capacity: the VM's footprint on ESXi, for migration and host capacity ([`sp5-framework/capacity/vm-footprint-sizing`](../../../../../sp5-framework/capacity/vm-footprint-sizing.md), section Memory). Not the Guest OS need and not a Guest OS sizing input.

## vMotion effect
- After vMotion, Consumed on the destination can increase. Swapped or compressed pages can become regular pages. See [`vsphere/architecture/overhead`](../../../../architecture/overhead.md).

## View
- ESXi view (ESXi pages) of the VM: memory that has been active.
- Shared pages count once: 3 VM pages shared into 1 ESXi page count as 1.
- Ballooned and swapped VM pages have no ESXi page here.
- Consumed can hold a lot of guest cache.
- Does not exist in Windows. No Guest OS counterpart.

## Formula
```text
Consumed = Granted - savings (sharing)
```
- ESXi memory mapped to the VM.
- ESXi backs VM memory with 2 MB pages whenever possible, even if the guest does not request them. Fewer TLB misses, but the VM consumes more than the guest uses.
- Excludes overhead (transparent to the guest) and swapped memory (not readily usable).
- Compressed: the compressed result stays in Consumed; only the freed part leaves. A 4 KB page compressed to 1 KB keeps 1 KB in Consumed and frees 3 KB (esxtop CNSM excludes the memory saved by compression, vSphere 9.1 documentation, esxtop Memory panel).
- Includes touched reserved memory; untouched reserved memory is not counted.
- Capped by a limit. Can reach, not exceed, configured memory.
- The vSphere API quick statistics of a VM carry two memory values with similar names. Guest memory usage (`guestMemoryUsage`) is active guest memory: the Active estimate, not Consumed and not a Guest OS counter. Host memory usage (`hostMemoryUsage`) is consumed host memory including the VM's overhead, so it reads above this counter, which excludes overhead.

## Mechanism: second-level page tables
- Three address spaces: the process's virtual memory inside the Guest OS, VM pages (the memory the VM presents to the Guest OS; vendor term: guest physical memory) and ESXi pages (the host's physical memory; vendor term: machine pages).
- The CPU translates VM pages to ESXi pages in hardware, through second-level page tables (Intel EPT, AMD RVI). The Guest OS keeps its own page tables for process virtual memory to VM pages.
- First touch: the guest writes a VM page with no mapping. The CPU raises an EPT violation, the VMkernel allocates an ESXi page, writes the mapping and resumes the vCPU. Consumed grows by 4 KB, or 2 MB with large pages.
- The mapping stays until ESXi reclaims the page (sharing, balloon, compression, swap). Nothing else removes it.
- An idle guest does not shrink Consumed: halting or waiting vCPUs do not touch the page tables, and with free host memory ESXi has no reason to reclaim.

## Consumed after the guest frees memory
- A guest that frees a page only updates its free list. The hypervisor does not see the list, so the ESXi page stays mapped.
- The free list is ordinary guest memory, already mapped, so updating it causes no VM exit. Freed pages are not zeroed or handed back.
- When the guest later gives those pages to a new process, the existing mapping is reused: no EPT violation, no ESXi work, no swap and no balloon. Consumed does not move. VMware Tools plays no part here.
- So Consumed is higher than Guest OS In Use and stays high after Active has dropped.
- Consumed and Guest OS In Use are managed independently. They do not match.
- Consumed below Guest OS Used: check Shared and Zero pages.

## Misconceptions
- "VM Memory Consumed falls when the Guest OS frees memory" → a freed guest page stays mapped; Consumed falls only when ESXi reclaims (sharing, balloon, compression, swap). Read free memory inside the Guest OS.
- "Consumed near configured memory means the VM needs more memory" → Consumed holds every page the guest touched, cache and freed pages included. Guest OS need is read inside the Guest OS: paging, free memory, cache.
- "A memory reservation raises VM Memory Consumed" → Consumed grows only as the guest touches pages; untouched reserved memory is not counted.

## Metadata
```yaml
id: vsphere/technology/memory/metrics/virtual-motherboard/consumed
retriever_guide: metric-meaning
scope: vsphere
technology:
- memory
pillar:
- capacity
product:
- vsphere
object:
- VirtualMachine
layer:
- virtual-motherboard
metric_class: consumption
internal_derive:
- vsphere/architecture/resource-controls
- vsphere/architecture/overhead
same_name:
- vsphere/technology/memory/metrics/host/consumed
- vsphere/technology/memory/metrics/cluster/consumed
same_meaning: []
related:
- vsphere/technology/memory/metrics/comparisons/vm-memory-metrics
- vsphere/technology/memory/concepts/memory-layers
- vsphere/technology/memory/concepts/guest-os-vs-vm-memory
- vsphere/technology/memory/metrics/virtual-motherboard/granted
- vsphere/technology/memory/metrics/virtual-motherboard/shared
- vsphere/technology/memory/metrics/virtual-motherboard/zero-pages
- vsphere/technology/memory/metrics/virtual-motherboard/active
source:
  document: Knowledge base; vSphere Web Services API 9.1; vSphere 9.1 documentation (PDF built 2026-11-02)
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity; Memory > Architecture > Guest OS vs VM; Memory > VM > Consumption Metrics > Consumed; esxtop Memory panel, CNSM; VirtualMachineQuickStats, guestMemoryUsage and hostMemoryUsage (https://developer.broadcom.com/xapis/vsphere-web-services-api/9.1/vim.vm.Summary.QuickStats.html)
corrections: []
review_notes: []
status: draft
```
