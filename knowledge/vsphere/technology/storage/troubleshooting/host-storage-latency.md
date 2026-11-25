# ESXi storage latency is high

## Symptom
- ESXi disk latency (GAVG) is high on a host, the disk rows of ESXi Performance (%) are yellow or worse, or many VMs on one host or datastore show disk latency.
- Entered from [`vsphere/object-types/esxi/esxi-health-check`](../../../object-types/esxi/esxi-health-check.md) (step 3) or [`vsphere/technology/storage/troubleshooting/vm-storage-performance-checks`](vm-storage-performance-checks.md) (step 5).

## Flow
```mermaid
flowchart TD
  S1[1. Split GAVG into KAVG and DAVG] -->|KAVG high| S2[2. QAVG and queue depths]
  S1 -->|DAVG high| S3[3. Array, fabric, HBA]
  S2 --> S4[4. Per adapter and path, read and write]
  S3 --> S4
  S4 --> S5[5. Read vs write]
  S5 --> S6[6. NVMe memory-tier device?]
  S6 --> S7[7. Known bug and log]
  S7 --> E7[Layer and cause]
```

## Checks, in order
1. Split GAVG into KAVG and DAVG (HostSystem) ([`vsphere/technology/storage/concepts/esxi-storage-latency-stack`](../concepts/esxi-storage-latency-stack.md)). KAVG above its flow test (catalog row flow-esxi-disk-kernel-latency) → step 2. DAVG above its flow test (flow-esxi-disk-device-latency) → step 3.
2. Kernel queue (HostSystem). QAVG and the queue depths at each level of the stack ([`vsphere/technology/storage/concepts/esxi-storage-io-path`](../concepts/esxi-storage-io-path.md), section Queues on the path). High QAVG with normal DAVG on the disks of one VM can be an IOPS limit on its virtual disks ([`vsphere/technology/storage/metrics/virtual-motherboard/iops`](../metrics/virtual-motherboard/iops.md), section IOPS limit). → step 4.
3. Device (HostSystem). DAVG high: check the array. Array latency low: the fabric or HBA configuration. → step 4.
4. Per adapter and path (HostSystem) ([`vsphere/technology/storage/metrics/host/adapter-and-path`](../metrics/host/adapter-and-path.md)). Read and write latency separately. Use the 95th or 99th percentile, not the maximum. → step 5.
5. Read vs write (HostSystem). Write-only latency is expected when reads hit cache. → step 6.
6. NVMe memory-tier device (HostSystem). High latency at near-zero IO is a wake-up from a power-saving state: the cause, not a reason to discard the reading. The VMs that read then did wait; their NVMe Wait shows how much. → step 7.
7. Known bug and log (HostSystem): driver and firmware versions against the compatibility guide and known issues; events in the window ([`vsphere/object-types/vm/troubleshooting/vm-slow`](../../../object-types/vm/troubleshooting/vm-slow.md), its known bug and log checks).

## Order rationale
- The split first: kernel and device latency have different owners, the ESXi host and the array.
- Per adapter and path after the split: one bad path hides in the host total.
- Percentiles, not the maximum: one outlier sample is not a host problem.
- Memory-tier devices last: their latency pattern looks like a fault and is not.

## Interpretation
- KAVG high, DAVG low: queuing inside ESXi; queue depths or a saturated adapter.
- DAVG high, array latency low: the fabric or the HBA configuration.
- DAVG high, array latency high: the array.
- Thresholds of the vSphere documentation differ: [`vsphere/tools/vsphere-client/performance-guidance`](../../../tools/vsphere-client/performance-guidance.md).

## Misconceptions
- "Kernel latency should correlate with device latency" → when both are healthy they need not.
- "The maximum latency of the hour shows the problem" → use the 95th or 99th percentile per adapter and path.

## Metadata
```yaml
id: vsphere/technology/storage/troubleshooting/host-storage-latency
retriever_guide: troubleshooting
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
- vsphere/technology/storage/concepts/esxi-storage-latency-stack
- vsphere/technology/storage/concepts/esxi-storage-io-path
- vsphere/technology/storage/metrics/host/adapter-and-path
- vsphere/technology/storage/metrics/virtual-motherboard/iops
- vsphere/object-types/vm/troubleshooting/vm-slow
related:
- vsphere/technology/storage/metrics/host/disk
- vsphere/technology/storage/metrics/host/datastore
- vsphere/tools/vsphere-client/performance-guidance
- vsphere/technology/storage/metrics/datastore/storage-io-control
- sp5-framework/performance/performance-management
source:
  document: Knowledge base
  path: Storage > ESXi > Disk or Device; Storage Adapter & Path
corrections: []
review_notes: []
status: draft
```
