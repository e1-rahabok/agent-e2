# ESXi storage latency is high

## Checks, in order
1. Split GAVG into KAVG and DAVG.
2. KAVG above 0.5 ms: check QAVG and the queue depths at each level of the stack.
3. DAVG high (healthy is well within 5 ms): check the array. Array latency low: the fabric or HBA configuration.
4. Per adapter and path: read and write latency separately. Use the 95th or 99th percentile, not the maximum.
5. Read vs write: write-only latency is expected when reads hit cache.
6. NVMe memory-tier device: high latency at near-zero IO is a wake-up penalty, not a fault.

## Traps
- "Kernel latency should correlate with device latency" → when both are healthy they need not.

## Metadata
```yaml
id: vsphere/storage/diagnosis/host-storage-latency
retriever_guide: what-to-check
scope: vsphere
technology:
- storage
pillar:
- performance
product:
- vsphere
object:
- HostSystem
internal_derive:
- vsphere/storage/concepts/esxi-storage-latency-stack
related:
- vsphere/storage/metrics/host/disk
- vsphere/storage/metrics/host/adapter-and-path
- vsphere/storage/metrics/host/datastore
source:
  document: PART 3 - Counters.docx
  path: Storage > ESXi > Disk or Device; Storage Adapter & Path
corrections: []
review_notes: []
status: draft
```
