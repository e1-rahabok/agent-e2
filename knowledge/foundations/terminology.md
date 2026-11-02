# Terminology

Precise definitions used across this knowledge base.

## Allocation vs Reservation
- Allocation and reservation are two different concepts.
- Allocation: what is given to a consumer. Not guaranteed. It is a maximum: utilization cannot exceed it.
- Reservation: a guarantee. It is a minimum.
- Actual utilization can be below the reservation. It cannot exceed the allocation.
```text
utilization <= allocation
reservation is guaranteed; utilization may be < reservation
```
- Allocation can be overcommitted, because it is not a guarantee.
- Reservation cannot be overcommitted, because it is a guarantee.
- pattern when mixed: mixing-terminology. Invalid metric names:
  - "Allocation Reservation": meaningless.
  - "Maximum Reservation": means Allocation.
  - "Minimum Allocation": means Reservation.

## Device vs Disk vs LUN
- These three words are often used interchangeably. They are not identical.
- Device: generic. Not necessarily storage. Can be a network device or a security device.
- Disk: physical. Typically part of a disk group (RAID).
- LUN: a logical volume created by a storage array. Can span multiple RAID groups. "Logical volume" is the more accurate name; "LUN" is the common name.
- ESXi mounts a LUN and formats it with the VMFS filesystem.

## Usage vs Utilization (OpenTelemetry convention)
- Usage: amount used out of a known total.
- Utilization: fraction of usage out of its limit.
- vSphere does not follow this convention. See `foundations/naming-patterns`.

## Metadata
```yaml
id: foundations/terminology
retriever_guide: how-it-works
scope: vendor-neutral
technology:
- cpu
- memory
- storage
- network
pillar:
- capacity
- performance
product: []
internal_derive: []
related:
- foundations/naming-patterns
- vsphere/foundations/resource-management
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity
corrections: []
review_notes: []
status: draft
```
