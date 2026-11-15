# ESXi Memory Consumed

## Meaning
- Includes memory consumed by ESXi itself.
- Relevance for operations: capacity reporting and the VM footprint for migration. It is the capacity counter only on a host that runs with no ballooning by design; otherwise ESXi Memory Utilization is ([`vsphere/technology/memory/metrics/host/utilization`](utilization.md), section Reason). Not a performance counter: near 100% is normal.

## Scope
- ESXi pages, summed at host level: VMs plus the kernel's own memory plus VM overhead.
- Physical memory is shared by VMs and the hypervisor. Manage them as one.
- Very high Consumed triggers compression and swapping proactively. That alone does not mean VMs contend for RAM.

## Formula
```text
Consumed = physical memory - free
VCF Operations Usage (%) = Consumed / Total Capacity
```
- Only pages mapped in physical DIMM.
- excludes: ballooned (guest level), swapped (on disk or host cache).
- includes: the resulting compressed size (not the input), the result of TPS savings (not the shared amount), VM overhead, all kernel processes (user and kernel space).
- Compression: the compression cache (the zipped pages held in DRAM) is inside ESXi Memory Consumed, because cache pages are ESXi pages in use, not free. Only the memory compression freed leaves ESXi Memory Consumed.
- Example: a 4 KB page compressed to 1 KB keeps 1 KB in ESXi Memory Consumed and frees 3 KB.
- Includes actual kernel use, not kernel reservation.
- Excludes VM reservations as such: raising a running VM's reservation by several GB left host Consumed flat on a 9.1 lab host ([`vsphere/technology/memory/metrics/comparisons/host-memory-metrics`](../comparisons/host-memory-metrics.md), section VM reservation across counters).
- Sits above the Resource memory consumed counter of the host group: 12.45 GB against 11.88 GB on that host, a gap of about 0.5 GB.

## Behaviour
- The primary vCenter counter of host memory use (ESXi Memory Usage (%) is Consumed over Total Capacity), but full of cache and inactive pages. Near 100% in an overcommitted host is the goal, not a problem.
- Drops when balloon or swap out rises.
- ESXi Memory Consumed falling while ESXi Memory Compressed rises shows the compression saving plus any swap out. The compressed result stays inside Consumed.
- Includes non-VM consumers: kernel, vSAN, NSX. Can exceed the memory allocated to all running VMs.
![ESXi memory Consumed above the memory allocated to running VMs](../../images/esxi-memory-consumed-above-vm-allocated.png)
- Host with 0 VMs: example 17 GB consumed, likely vSAN.
- Same host: kernel reservation (VCF Operations Memory | ESX System Usage) about 57 GB, Consumed about 17.5 GB. Consumed is actual use, not reservation.
![ESXi with no VMs: ESX System Usage (kernel reservation) vs Consumed](../../images/esxi-memory-system-usage-vs-consumed-host-without-vms.png)
- Example: 255 GB host, 229 GB consumed = 191 GB by the one VM + 36 GB by the kernel. Kernel consumption = sum of 3 kernel resource pools.
- Evacuated host: Consumed fell from 400 GB to 32 GB (vSAN), not 0. Kernel usage stayed nearly constant; kernel reservation did not change.
![ESXi Consumed = VM consumed + kernel](../../images/esxi-memory-consumed-equals-vm-consumed-plus-kernel.png)

## Misconceptions
- "The sum of VM Memory Consumed equals ESXi Memory Consumed" → ESXi Memory Consumed adds the kernel, vSAN, NSX and VM overhead, so the sum of the VMs is lower.
- "Host Consumed near 100% is a problem" → memory is cache. Check balloon, swap-in and VM contention.
- "Host with no VMs should show 0 Consumed" → kernel, vSAN and NSX consume memory.
- "Consumed does not include compressed memory" → it includes the compressed result in DRAM; it excludes only what compression freed.

## Metadata
```yaml
id: vsphere/technology/memory/metrics/host/consumed
retriever_guide: metric-meaning
scope: vsphere
technology:
- memory
pillar:
- capacity
product:
- vsphere
object:
- HostSystem
metric_class: consumption
internal_derive:
- vsphere/architecture/provider-consumer
same_name:
- vsphere/technology/memory/metrics/cluster/consumed
- vsphere/technology/memory/metrics/virtual-motherboard/consumed
same_meaning: []
related:
- vsphere/technology/memory/metrics/comparisons/host-memory-metrics
- vsphere/technology/memory/concepts/memory-layers
- vsphere/technology/memory/metrics/host/granted
- vsphere/technology/memory/metrics/host/utilization
- vsphere/technology/memory/concepts/host-memory-states
images:
  - path: ../../images/esxi-memory-consumed-above-vm-allocated.png
    product: [vsphere]
    object: [HostSystem]
    metric: ['ESXi Memory Consumed']
    image_type: timeline
  - path: ../../images/esxi-memory-system-usage-vs-consumed-host-without-vms.png
    product: [vsphere]
    object: [HostSystem]
    metric: ['ESXi Memory ESX System Usage', 'ESXi Memory Consumed']
    image_type: timeline
    sample: '1 host, 0 VMs'
  - path: ../../images/esxi-memory-consumed-equals-vm-consumed-plus-kernel.png
    product: [vsphere]
    object: [HostSystem]
    metric: ['ESXi Memory Consumed']
    image_type: screenshot
source:
  document: Knowledge base; vSphere Web Services API 9.1; vSphere 9.1 documentation (PDF built 2026-11-02)
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity; Memory > Architecture > Virtual Memory; Relationship; Memory > ESXi > Consumption Metrics > Consumed; API 9.1 memory counters, consumed = total host memory minus free host memory (https://developer.broadcom.com/xapis/vsphere-web-services-api/9.1/memory_counters.html); esxtop Memory panel, CNSM excludes the memory saved by compression
corrections: []
review_notes:
- 'To check: Section ''Scope'': the gap of about 0.5 GB between host Consumed and the host group Resource memory consumed on a 9.1 lab host has no explanation yet (not VM overhead, which read 0); compare the two counters on another 9.1 host.'
status: draft
```
