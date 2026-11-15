# VM Memory Active

## Meaning
- Estimate of VM memory read or written recently. ESXi calls it Touch; vCenter calls it Active.
- An internal counter of kernel memory management.
- VCF Operations name: Memory | Non Zero Active (KB). Active Write counts writes only.
- Relevance for operations: on a host without memory tiering, none for capacity, sizing, performance or Guest OS need, because it is a sampled estimate made for VMkernel memory management. On a memory-tiered host, the Active of the VMs summed against host DRAM is the capacity constraint and the leading performance signal ([`vsphere/technology/memory/concepts/memory-tiering`](../../concepts/memory-tiering.md), section Capacity management).

## Mechanism
- Active is really a rate (pages touched per time), reported as space (KB).
- A page can be read and written many times. 100 reads + 100 writes can touch far fewer than 200 pages.
- Recent: ESXi estimates the working set by statistical sampling over a period of 60 seconds by default (Mem.SamplePeriod), smoothed over several periods; the estimate rises fast and falls slowly (vSphere 9.1 documentation, pp. 1838, 2104).
- Sampling: if ESXi samples every 2 seconds, vCenter has 10 samples per 20-second period. Samples can hit the same or different pages. Example: 100 MB then 150 MB active gives 150-250 MB for 4 seconds.
- Each sample is independent and averaged with earlier samples. Active becomes more accurate over time. esxtop has a longer-term Active; vSphere Client does not.
- Ballooned memory is excluded (inactive). Active is unaware of locked pages and large pages.
- VCF Operations averages 15 vCenter samples into 300 seconds. The same page is counted many times, so Active over-reports.
- Differs from the Guest OS working set estimate: different algorithms, plus ballooning and host swapping.

## Active vs Consumed
- Different calculation, different purpose. Not just aggressive vs conservative versions of the same thing.
- Neither suits Guest OS sizing. Little correlation with Guest OS memory use.
- Active is lower than Consumed and Guest OS Used: those two measure space held, including inactive pages.
- Active can fall while Consumed rises.
- Active is sampled. It can stay constant when it should not, and can stay at 100% for hours (see [`vsphere/technology/memory/concepts/guest-os-vs-vm-memory`](../../concepts/guest-os-vs-vm-memory.md)).
![Active falls while Consumed rises](../../images/vm-memory-active-falls-while-consumed-rises.png)

## Misconceptions
- "Active = VM memory utilization" → it is a sampled estimate for the kernel. Its one operations use is on a memory-tiered host, against DRAM.
- "Active over-reports, so it is always higher than Consumed" → it is usually far lower.

## Metadata
```yaml
id: vsphere/technology/memory/metrics/virtual-motherboard/active
retriever_guide: metric-meaning
scope: vsphere
technology:
- memory
pillar:
- performance
- capacity
product:
- vsphere
- vcf-operations
object:
- VirtualMachine
layer:
- virtual-motherboard
metric_class: consumption
internal_derive:
- vsphere/technology/memory/concepts/guest-os-vs-vm-memory
same_name: []
same_meaning: []
related:
- vsphere/technology/memory/metrics/comparisons/vm-memory-metrics
- vsphere/technology/memory/metrics/virtual-motherboard/consumed
- vsphere/technology/memory/metrics/virtual-motherboard/usage
images:
  - path: ../../images/vm-memory-active-falls-while-consumed-rises.png
    product: [vsphere]
    object: [VirtualMachine]
    metric: ['VM Memory Active', 'VM Memory Consumed']
    image_type: timeline
source:
  document: Knowledge base; vSphere 9.1 documentation (PDF built 2026-11-02)
  path: Memory > VM > Consumption Metrics > Active; Consumed vs Active; Resource Management, How ESX Hosts Allocate Memory (p. 1838); Monitoring and Performance, Virtual Machines, Memory (MB), Active (p. 2104)
corrections: []
review_notes:
- 'To check: Section ''Mechanism'': the sampling interval behind the 2-second example; vSphere 9.1 gives only the 60-second sample period (Mem.SamplePeriod, p. 1838); https://blogs.vmware.com/vsphere/2013/10/understanding-vsphere-active-memory.html.'
status: draft
```
