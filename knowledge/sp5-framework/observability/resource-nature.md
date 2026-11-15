# Nature of the four infrastructure resources

## Definition
- Infrastructure has four basic resources: CPU, memory, storage, network.
- Each resource has two possible dimensions: speed and space.
- The two dimensions apply differently per resource. This drives which metrics exist and how they behave.

## Speed vs space

| Resource | Speed | Space | Measured as |
|---|---|---|---|
| CPU | Yes | Yes | Speed: Hertz. Space: vCPU or physical thread. |
| Memory | Limited | Yes | Speed: latency in nanoseconds, practically not used in performance management. Space: bytes. |
| Storage | Yes | Yes | Speed: IOPS and throughput (bytes/second). Space: bytes. |
| Network | Depends on the component | Depends on the component | Network is both a line and a dot: cables are lines, switches are dots. |

## CPU
- CPU-derived values are approximations: the CPU runs in nanoseconds and observability code in milliseconds ([`sp5-framework/observability/measurement-precision`](measurement-precision.md), section Observer speed vs CPU speed).
- The primary speed unit (GHz) is not comparable across hardware generations or architectures.
  - 1 GHz on a newer CPU does more work than 1 GHz on an older CPU.
  - GHz is also not comparable across CPU model variants of the same generation from the same vendor.

## Memory
- Memory speed matters only for applications that require very low latency, such as GenAI.
- Memory functions as a cache. Cache is much smaller than its source.
  - Memory counters are expected to run near 100%.
  - Below 100% means the memory is not fully used for caching.
- CPU and memory utilization have different natures:
  - 95% memory utilization can be low.
  - 85% CPU utilization can already be high.
- Memory is a form of storage. Its metrics are mostly about space, not speed.
  - Consequence: vCenter has a VM CPU Demand counter, the runtime the vCPUs demand, but no memory counter of that kind. Memory demand in capacity is a model, the higher of utilization and reservation per VM, not a counter ([`sp5-framework/capacity/demand`](../capacity/demand.md)).
  - Same reason there is no "demand" metric for disk space on a laptop.

## Storage
- Both dimensions (speed and space) have consumption metrics.
- Speed has two consumption components: IOPS and throughput.
- Throughput depends on block size.
- Disk throughput is measured in bytes/second, not bits/second.
  - Reason: it measures the amount of disk space read or written, at the node.
  - Network throughput instead measures the cable or wire.

## Network
- Servers and storage are nodes. Network is the interconnect.
- Network takes more than one shape: line (cable) and dot (switch). This makes network metrics harder than node metrics.

## Misconceptions
- "Memory at 95% is as bad as CPU at 95%" → memory is a cache and is expected to run near 100%; 85% CPU utilization can already be high. Read each resource by its contention: VM Memory Latency for memory, VM CPU Ready and Co-stop for CPU.
- "This host has more GHz, so it does more work" → work per GHz differs across CPU generations and models; compare GHz only within one CPU model.
- "VM memory demand is a counter, like VM CPU Demand" → memory is space, not time: no memory counter measures demanded runtime. Capacity memory demand is a model, the higher of utilization and reservation per VM.

## Metadata
```yaml
id: sp5-framework/observability/resource-nature
retriever_guide: how-it-works
scope: sp5-framework
technology:
- cpu
- memory
- storage
- network
pillar:
- performance
- capacity
product:
- vsphere
- vcf-operations
internal_derive: []
related:
- sp5-framework/observability/measurement-precision
- sp5-framework/capacity/demand
- vsphere/architecture/resource-controls
- vsphere/technology/memory/metrics/virtual-motherboard/usage
- vsphere/technology/storage/metrics/virtual-motherboard/virtual-disk
source:
  document: Knowledge base
  path: The World of Metrics > Metrics Nuances > Complexity > Architecture Complexity
corrections: []
review_notes: []
status: draft
```
