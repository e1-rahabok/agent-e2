# Ballooning

## Mechanism
- The balloon is a kernel driver inside the Guest OS. It takes instructions from the VMkernel to inflate or deflate.
- Inflate: the driver asks the Guest OS to allocate memory to it. ESXi does not back that memory with physical pages, so other VMs can use it.
- Deflate: when the Balloon Target falls below the balloon size, the VMkernel deflates the balloon and the driver releases its pages to the Guest OS (vSphere 9.1 documentation, memory counters, pp. 2073, 2104). Ballooned returns to 0 when the target reaches 0.
- Purpose: the guest gives up the pages it values least, so ESXi reclaims memory without picking pages blind, as host swapping does (vSphere 9.1 documentation, Memory Balloon Driver, p. 1839).
- The VM initiates the reallocation, so Balloon Target can be 0 while Ballooned is still above 0 (vSphere 9.1 documentation, p. 2073).
- Balloon Target above 0: the hypervisor has asked this VM to give back memory through the balloon driver.
- A 1 GB balloon does not free 1 GB in ESXi when the pages were shared (TPS). It can be less.
- The Guest OS allocates to the balloon from Free pages first, then Cache, then Modified, then In Use.
- The Guest OS must have enough swap space configured for ballooning: at least configured memory minus the memory reservation (vSphere 9.1 documentation, Swap Space and Memory Overcommitment, p. 1874).
- How much is requested depends on the VM's allocation target, which charges idle memory more than active memory (Mem.IdleTax). Changing Mem.IdleTax is rarely appropriate (vSphere 9.1 documentation, pp. 1838-1839).

## Inflate and deflate, step by step
1. The memory scheduler sets a Balloon Target for the VM (the counter VM Memory Balloon Target).
2. The driver polls the hypervisor about once per second and sees its size is below the target.
3. It asks the Guest OS for 4 KB pages. The guest gives free pages first; when none are left, it drops clean cache, then pages cold pages out to guest swap.
4. The driver pins those pages, so the guest cannot reuse them, and passes their page numbers to the VM monitor through a hypercall.
5. The VM monitor invalidates their second-level page table entries and returns the ESXi pages to the VMkernel. Consumed falls at once.
- The scheduler lowers the target when host memory pressure ends, when a limit is raised, or when the VM's working-set estimate grows: the allocation target follows shares and the working set and taxes idle memory (vSphere 9.1 documentation, How ESX Hosts Allocate Memory, p. 1838). An idle VM on a host that stays overcommitted therefore keeps its balloon; the guest asking for memory does not deflate it.
- Deflate: the scheduler lowers the target; the driver unpins its pages and frees them to the guest allocator. ESXi allocates nothing at that moment. When the guest next writes a freed page, an EPT violation exits to the VM monitor, which maps a new zero-filled ESXi page. So Consumed rises again only as the guest touches pages.
- Ceiling: the driver stops at 65% of configured memory by default (host option Mem.CtlMaxPercent; `sched.mem.maxmemctl`, in MB, sets it per VM). What is still above the target is compressed or swapped.
- Second-level page tables and the EPT violation: see [`vsphere/technology/memory/metrics/virtual-motherboard/consumed`](../metrics/virtual-motherboard/consumed.md).

## Performance impact
- Ballooning by itself does not cause a performance problem.
- A problem occurs when the Guest OS needs data it dropped from cache or paged out to fill the balloon: it reads the data back from disk or from guest swap.
- The more ballooned, swapped and compressed, the higher the chance of a future performance hit.
- Severity depends on VM shares, reservation, limit and configured RAM. 10 MB ballooned hurts a 4 GB VM more than a 512 GB VM.
- Example: a 16 GB VM with about 10 GB ballooned, near the 65% ceiling, for 4 weeks, flat. The Guest OS never requested those pages; it worked within the remaining 6 GB. Granted + Swapped + Compressed was a flat line.
![Heavily ballooned VM: latency spikes are rare](../images/vm-memory-heavy-balloon-with-rare-latency-spikes.png)

## Capacity impact
- A balloon is a request from ESXi, not from the application: its size says nothing about what the application demands.
- Guest OS In Use rises when the balloon allocates: the driver is treated like any process, and its pinned pages are neither free nor cache.
- Pages taken from Free: In Use rises by the balloon size while the application's need does not change.
- Pages taken from In Use: In Use does not change; the Guest OS paged the data out, and that data is still demand.
- The Guest OS counters show the balloon size, not how much of it came from Free, so the distortion of Guest OS sizing is bounded by the balloon size but not measured.
- Sizing rule for ballooned memory (include it, no deduction): [`guest-os/system/concepts/guest-os-sizing`](../../../../guest-os/system/concepts/guest-os-sizing.md), section Ballooned memory in sizing.

## Ballooned vs compressed and swapped
- ESXi knows nothing of free memory inside the guest. Compression and swapping pick pages at random. Ballooning lets the guest choose.
- Balloon can be 0 while Compressed or Swapped are above 0, although ballooning comes first in the reclamation order.
- Reason: past pressure. Compressed and swapped pages come back only when the guest touches them (it costs CPU); the balloon deflates when the Balloon Target falls, without a guest request.

## Trigger and requirement
- Two triggers. Host pressure: host memory begins to get low and the VM's memory usage approaches its memory target; the balloon inflates when the host enters the Soft state (free memory at 64% of minFree; see [`vsphere/technology/memory/concepts/host-memory-states`](host-memory-states.md)). A limit: the VM, or a pool above it, would grow past its limit; the balloon inflates on a host with free memory too (see [`vsphere/technology/memory/concepts/memory-limit`](memory-limit.md)).
- No host pressure and no limit, no balloon: a VM inside its configured memory on a host with free memory is never ballooned, with or without VMware Tools. It reuses its own mapped pages.
- The balloon driver makes the guest OS give up the pages it considers least valuable. Windows: the driver ships with VMware Tools. Linux: the driver is `vmw_balloon`, in the upstream kernel and loaded automatically on a VMware VM; open-vm-tools does not contain it (Broadcom KB 313773).
- Performance closely matches a native system under similar memory constraints.
- In Linux OS, ballooning can be done even if the VMware Tools service (vmtoolsd) is stopped.
- Without the driver (Windows without VMware Tools, Linux with the module missing or blacklisted), ESXi can only compress or swap, blind to which pages the guest uses.

## Misconceptions
- "ESXi can balloon any VM" → only a VM with the balloon driver loaded (VMware Tools on Windows, the kernel module on Linux); otherwise the host compresses and swaps.
- "Ballooned 10 GB, so the guest is slow" → the cost comes only when the guest needs data it gave up for the balloon. VM Memory Latency does not count the balloon; check Guest OS paging (Performance Best Practices for vSphere 9.1, step d).
- "Ballooned stays above 0 after the pressure, so the guest has not asked for the pages back" → the balloon deflates when the Balloon Target falls, not on a guest request. A flat Ballooned means the target held: host pressure, a limit, or an idle VM on an overcommitted host.
- "Balloon frees exactly its size in ESXi" → shared pages free less.
- "A VM that frees memory and then needs it again gets swapped or ballooned to make room" → no: the guest reuses pages it already has mapped; ESXi is not involved unless the host is under pressure.

## Metadata
```yaml
id: vsphere/technology/memory/concepts/ballooning
retriever_guide: how-it-works
scope: vsphere
technology:
- memory
pillar:
- performance
- capacity
product:
- vsphere
object:
- VirtualMachine
internal_derive:
- vsphere/technology/memory/concepts/memory-layers
- vsphere/technology/memory/concepts/host-memory-states
related:
- vsphere/technology/memory/metrics/virtual-motherboard/ballooned
- vsphere/technology/memory/metrics/virtual-motherboard/balloon-target
- vsphere/technology/memory/concepts/swap-and-compression
- vsphere/technology/memory/concepts/memory-limit
- vsphere/technology/memory/metrics/virtual-motherboard/latency
- guest-os/system/concepts/guest-os-sizing
images:
  - path: ../images/vm-memory-heavy-balloon-with-rare-latency-spikes.png
    product: [vsphere]
    object: [VirtualMachine]
    metric: ['VM Memory Ballooned', 'VM Memory Latency']
    image_type: timeline
source:
  document: Knowledge base; Performance Best Practices for VMware vSphere 9.1 (revision 20260624); vSphere 9.1 documentation (PDF built 2026-11-02); Broadcom KB 313773
  path: Memory > VM > Contention Metrics > Balloon; Swap + Compress > Balloon; ESX Memory Considerations > Memory Overcommit Techniques (pp. 33-34); Resource Management, How ESX Hosts Allocate Memory, Memory Tax for Idle Virtual Machines, Memory Balloon Driver, Swap Space and Memory Overcommitment (pp. 1838-1840, 1874); Monitoring and Performance, Balloon Target (pp. 2073, 2104)
corrections: []
review_notes:
- 'To check: Section ''Inflate and deflate, step by step'': the one-second polling interval of the driver; vSphere 9.1 documentation, Memory Balloon Driver (p. 1839), does not state it.'
status: draft
```
