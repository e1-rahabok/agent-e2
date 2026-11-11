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
- CPU runs in nanoseconds. Observability code runs in milliseconds.
  - Result: CPU-derived values are not 100% exact.
  - Example: counting threads per thread state in Windows or Linux can vary by ~5%.
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
  - Consequence: there is VM CPU Demand, but no VM Memory Demand.
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
- Applying one threshold philosophy to all four resources → wrong. The same % means different things per resource.
- Comparing GHz across CPU generations or models → wrong. Work per GHz differs.
- Expecting a "memory demand" metric like CPU demand → wrong. Memory is space, not time.

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
- vsphere/architecture/resource-controls
- vsphere/technology/memory/metrics/virtual-motherboard/usage
- vsphere/technology/storage/metrics/virtual-motherboard/virtual-disk
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: The World of Metrics > Metrics Nuances > Complexity > Architecture Complexity
corrections:
- '2026-11-02: CPU has a space dimension (Yes), measured in vCPU or physical thread. Uploaded document table shows N/A.'
review_notes: []
status: draft
```
