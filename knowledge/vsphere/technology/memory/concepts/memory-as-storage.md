# Memory as storage

## Purpose
- Memory acts as a disk cache. Use all the cache given.
- All else equal, 100% memory usage performs better than 99%.

## Memory vs CPU
| CPU | Memory |
|---|---|
| Transient. Instructions enter and leave the pipelines in under a nanosecond. | A form of storage. Behaves like disk space. |
| A reservation does not apply while the VM does not use the CPU. Other VMs use it. | A reservation can stay in place even if the VM has not read or written the page in days. |

## Pages
- Memory is a collection of blocks in physical DIMMs.
- Data is stored in standard block sizes, typically 4 KB or 2 MB. Each block is a page.
- At the lowest level a page is a series of zeroes and ones.
- Windows initializes its pages with 0. That is why ESXi has a zero-page counter.

## Two dimensions
| Dimension | Unit | Facts |
|---|---|---|
| Speed | Nanoseconds | Generally ignored for RAM monitoring. DDR5 is faster than DDR4, but the difference does not matter for general monitoring. |
| Speed | Nanoseconds | Matters with memory tiering: the second tier is NVMe, not DIMM. |
| Speed | % of time | The only ESXi speed counter is Memory Latency (page-fault latency, esxtop %LAT_M). Share of time a vCPU waits on page-fault completion. Not the latency in ns. See `vsphere/technology/memory/metrics/virtual-motherboard/latency`. |
| Space | Bytes | The bulk of memory metrics. Relatively static. |

- Disk tracks latency as time per IO (ms). Memory tracks it as share of time waiting (%).
- The storage nature of memory makes memory monitoring harder than CPU monitoring.
- Space is static enough for a heat map of all Guest OS or VM memory consumption.
- Target: near 100% use, with page-in and page-out rates within normal expectation.

## Traps
- "Memory at 100% is a problem" → memory is cache. Check paging and contention, not utilization.
- "Memory Latency is in nanoseconds" → it is a percentage of time, not a duration.
- "Memory Latency is the share of memory space facing latency" → it is a share of time.
- "Memory reservation frees up when idle, like CPU" → memory reservation stays.

## Metadata
```yaml
id: vsphere/technology/memory/concepts/memory-as-storage
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
- HostSystem
internal_derive: []
related:
- vsphere/technology/memory/concepts/memory-layers
- vsphere/technology/memory/metrics/virtual-motherboard/latency
- vsphere/architecture/resource-controls
- vsphere/technology/memory/concepts/memory-tiering
source:
  document: PART 3 - Counters.docx
  path: Memory > Architecture > Architecture intro
corrections: []
review_notes: []
status: draft
```
