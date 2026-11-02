---
id: vsphere/memory/architecture/memory-tiering
type: concept
scope: vsphere
resources: [memory, storage]
objects: [esxi, vm]
related:
  - vsphere/memory/architecture/overcommit-techniques
  - vsphere/memory/architecture/host-level-swapping
source:
  document: Performance Best Practices for VMware vSphere 9.0 (revision 20250731)
  path: Memory Hardware Considerations > Memory Tiering Hardware (p. 14); ESX Memory Considerations > Memory Tiering (p. 36)
corrections: []
review_notes:
  - "Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-90-performance-best-practices"
  - "Newly supported in vSphere 9.0, per the source. Source refers to white paper 'Memory Tiering Performance: VMware Cloud Foundation 9.0' and to 'Memory Tiering over NVMe' in vSphere Resource Management. Not read."
status: draft
---

# Memory tiering

## Definition
- Newly supported in vSphere 9.0.
- Uses two types of memory devices to increase memory capacity at a reduced cost.
- Tier 1: DRAM, fast and relatively expensive.
- Tier 2: NVMe storage, secondary, slower and relatively less expensive.

## Mechanism
- Memory tiering transparently monitors VM memory activity.
- Frequently accessed data stays on DRAM.
- Infrequently accessed data is placed on the NVMe tier.

## Hardware selection
- Select a high-performance NVMe device with:
  - at least 100,000 writes per second,
  - endurance of at least 3 full Drive Writes per Day (DWPD),
  - sufficient capacity.

## Performance thresholds (from the source)
- Active memory:
  - ideal: no more than 50% of the host DRAM capacity,
  - some workloads do not begin to suffer until active memory approaches 75%.
- NVMe read latency:
  - ideal: below 200 microseconds,
  - some workloads do not begin to suffer until latency approaches 400 microseconds.

## Traps
- "Tiered memory performs like DRAM" → infrequently accessed data sits on the NVMe tier.
- "Any SSD works for memory tiering" → the source specifies a high-performance NVMe device with the write rate and endurance above.
- "Active memory at 75% of DRAM is the limit" → 75% is the point where some workloads begin to suffer. The ideal is 50%.
