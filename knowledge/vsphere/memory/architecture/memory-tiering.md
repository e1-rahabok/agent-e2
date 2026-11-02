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
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: Memory Hardware Considerations > Memory Tiering Hardware (p. 14); ESX Memory Considerations > Memory Tiering (p. 38)
corrections: []
review_notes:
  - "Checked against 9.1 (revision 20260624). Pages 14 and 38 read. Setup changes and CPU headroom bullet added (p. 38)."
  - "Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices"
  - "Introduced in vSphere 9.0. The 9.1 document (p. 38) refers to 'More Memory, Less Effort: Configuring Memory Tiering in VCF 9.1' and the 'Memory Tiering Resource Hub'. Not read."
status: draft
---

# Memory tiering

## Definition
- Introduced in vSphere 9.0. Increased performance and redundancy in vSphere 9.1 (p. 38).
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

## Setup (9.1 p. 38)
- Setup no longer requires manual ESX CLI commands or scripts.
- Setup uses vSphere Configuration Profiles, at cluster level.
- Software mirroring: a new feature in 9.1, also configured at cluster level.
- Hosts go into maintenance mode for the changes to take effect. A reboot is not necessary.

## Performance thresholds (from the source)
- Active memory:
  - ideal: no more than 50% of the host DRAM capacity,
  - some workloads do not begin to suffer until active memory approaches 75%.
- NVMe read latency:
  - ideal: below 200 microseconds,
  - some workloads do not begin to suffer until latency approaches 400 microseconds.

- Make sure there is enough CPU headroom to handle the CPU cost of memory tiering (9.1 p. 38).

## Traps
- "Tiered memory performs like DRAM" → infrequently accessed data sits on the NVMe tier.
- "Any SSD works for memory tiering" → the source specifies a high-performance NVMe device with the write rate and endurance above.
- "Active memory at 75% of DRAM is the limit" → 75% is the point where some workloads begin to suffer. The ideal is 50%.
