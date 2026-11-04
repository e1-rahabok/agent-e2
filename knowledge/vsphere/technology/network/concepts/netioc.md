# Network I/O Control (NetIOC)

## Purpose
- NetIOC allocates network bandwidth to network resource pools.
- Predefined resource pools (nine):
  - management traffic,
  - Fault Tolerance traffic,
  - iSCSI traffic,
  - NFS traffic,
  - vSAN traffic,
  - vMotion traffic,
  - vSphere Replication (VR) traffic,
  - vSphere Data Protection backup traffic,
  - virtual machine traffic.
- User-defined resource pools are also possible.
- Each resource pool is associated with a portgroup.
- Effect: guarantees bandwidth for specific needs, and stops one resource pool from affecting the others.

## Version
- NetIOC version 3 (NetIOCv3), introduced in vSphere 6.0, allocates bandwidth at the level of the whole distributed switch. NetIOCv2 allocated at the physical adapter level.
- The source describes NetIOCv3 only.
- A new vDS in vSphere 9.1 uses NetIOCv3 by default.
- vDS switches upgraded from earlier versions may not be upgraded to NetIOCv3 automatically.

## Scope
- NetIOC controls transmit traffic only. It does not limit receive traffic.
- Traffic shaping limits the bandwidth of a vNIC. It can be set separately for transmit and receive. See Network Traffic Shaping (p. 46, not read).
- DRS includes NetIOC bandwidth reservations in its load-balancing calculations. See `vsphere/object-types/cluster/concepts/drs-overview`.

## Shares
- A share gives a proportion of the physical link bandwidth: the pool's shares divided by the total shares.
- Unused bandwidth from a pool or vNIC is available to other consumers on the same physical NIC.

## Reservations
- A reservation guarantees a minimum bandwidth, in Mb/s, for a resource pool or a vNIC.
- Total reservations are limited to 75% of the capacity of the underlying physical adapter.
- Unused reservation is available to other consumers on the same physical NIC.

## Limits
- A limit sets a maximum bandwidth, in Mb/s or Gb/s, per physical NIC through a vDS.
- Limits are enforced even if the vDS is not saturated.
- If usage is below the limit, the unused bandwidth is available to other consumers on the same physical NIC.

## Advanced performance options
- By default, NetIOC scales the number of hardware transmit queues with link speed. Source: one hardware queue on the NIC for each 12.5 Gb/s of link speed.
- Multiple vNICs or vmknics can spread traffic across multiple hardware transmit queues on one physical NIC.
- Benefit: can improve performance, especially for small packets and high packet rates.

## HClock Multiqueue (p. 48)
- Activation: `/Net/NetSchedHClkMQ` through `esxcli system advanced set`.
  - 0: deactivated,
  - 1: activated without automatic scaling,
  - 2: activated with automatic scaling (default).
- With value 1, the maximum number of hardware transmit queues is set by `/Net/NetSchedHClkMaxHwQueue` (default 2).
- After a change, take each physical NIC down and up again: `esxcli network nic down -n vmnicX`, then `esxcli network nic up -n vmnicX`.
- Once activated, `NetSchedHClkMaxHwQueue` determines how many hardware transmit queues can be used.

## Traps
- "NetIOC limits receive traffic" → NetIOC controls transmit only.
- "A reservation can be set to the full adapter capacity" → total reservations are limited to 75% of the adapter capacity.
- "A share guarantees bandwidth" → shares divide the link only among consumers that want bandwidth. Reservations are the guarantee.
- "An upgraded vDS uses NetIOCv3" → the source says upgraded switches may not be upgraded automatically.

## Metadata
```yaml
id: vsphere/technology/network/concepts/netioc
retriever_guide: how-it-works
scope: vsphere
technology:
- network
pillar:
- performance
product:
- vsphere
object:
- VirtualMachine
- HostSystem
- ClusterComputeResource
internal_derive: []
related:
- vsphere/technology/network/concepts/passthrough-and-offload
- vsphere/technology/network/configuration/rss-and-interrupt-coalescing
- vsphere/object-types/cluster/concepts/drs-overview
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: ESX Networking Considerations > Network I/O Control (NetIOC) (pp. 47-48)
corrections: []
review_notes:
- Checked against 9.1 (revision 20260624). Written from 9.1 pages 47-48. New in the 9.1 document.
- 'Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices'
- New in the 9.1 document. Not in the 9.0 table of contents as a separate section.
- Network Traffic Shaping (p. 46), Enhanced Data Path (p. 46) not read.
status: draft
```
