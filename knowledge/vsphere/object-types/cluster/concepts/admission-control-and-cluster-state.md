# Admission control, expandable reservations and cluster state

## Admission control
- At power-on, and at every reservation or resource pool change, the system checks that all reservations can still be guaranteed.
- It compares the VM's reservation with the unreserved capacity of its host, resource pool or cluster. Not enough → the power-on fails with Insufficient Resources.
- Admission control counts reservations, not usage. A host at 10% CPU usage can refuse a VM if its capacity is already reserved.
- Per-VM overhead memory counts as reserved, on top of the memory reservation.
- A VM with no reservation passes CPU and memory admission control; its overhead memory is still checked.
- CPU admission control ignores CPU affinity. A pinned VM can be admitted and still not receive its full reservation.
- vCenter stores `clusterServices.failover` on the cluster (level 1, rollup latest). Its counter summary: vSphere HA number of failures that can be tolerated. Low priority. Trap: when the hosts of the cluster are not identical, failures to tolerate counted in hosts does not equal capacity lost: losing the largest host costs more.
- With DPM, capacity of hosts in standby counts as available; DRS recommends powering them on when a VM cannot be admitted without them.

## Fixed vs expandable reservation (resource pools)
| Type | Admission check |
|---|---|
| Fixed | Only the pool's own unreserved capacity. |
| Expandable (default) | The pool's own capacity, then its parent's, recursively up the tree while each ancestor is expandable. |

- A resource pool reservation is subtracted from the parent at creation, whether or not VMs use it.
- Expandable reservations give flexibility but lose isolation: one child pool can take all of the parent's spare reservation, leaving none for its siblings.

## Worked example
- RP-MOM reserves 6 GHz and runs VM-M1 with 1 GHz reserved. Child RP-KID (expandable) reserves 2 GHz.
- VM-K1 (2 GHz) powers on from RP-KID's own 2 GHz.
- VM-K2 (2 GHz) borrows from RP-MOM: 6 - 1 - 2 = 3 GHz unreserved. It powers on.
- If RP-MOM instead runs 3 GHz of VM reservations: 6 - 3 - 2 = 1 GHz unreserved. VM-K2 cannot power on.

## Cluster state (DRS)
- **Valid**
  - Condition: Every reservation in the resource pool tree fits within its parent and within cluster capacity.
  - Running VMs: All get their reservations.
- **Overcommitted (yellow)**
  - Condition: The tree is consistent, but cluster capacity no longer covers all resource pool reservations. Typical cause: a host fails or leaves.
  - Running VMs: Still covered: the VMs of the lost host are no longer running.
  - Fix: Add hosts, or lower resource pool reservations.
- **Invalid (red)**
  - Condition: The tree is inconsistent: children's reservations exceed a parent's fixed reservation. Can happen at any level, even with free capacity at the root.
  - Running VMs: Some may not get their reservations.
  - Fix: Power off or move VMs, or edit the pool settings. Adding capacity does not fix red.

- A cluster also turns red when HA can no longer meet its failover capacity.
- Changing a pool reservation while a VM is failing over can turn the cluster red: the failing-over VM is not charged to the pool until the failover completes.

## Headroom
- The documentation advises leaving at least 10% of capacity unreserved.
- Near 100% reserved, reservation changes and resource pool edits fail admission control.
- Reservations that fully commit a host or the cluster stop DRS from migrating VMs: no destination can admit them.

## Traps
- "The host is at 30% CPU, so the VM will power on" → admission control checks unreserved capacity, not usage.
- "Yellow cluster means VMs are starving" → running VMs still have their reservations; resource pool reservations cannot all be met.
- "Add a host to fix a red cluster" → red is an inconsistency in the tree; fix the reservations.
- "Expandable pools isolate departments" → only Fixed pools isolate.

## Metadata
```yaml
id: vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
retriever_guide: how-it-works
scope: vsphere
technology:
- cpu
- memory
pillar:
- performance
- capacity
product:
- vsphere
object:
- ClusterComputeResource
- ResourcePool
- HostSystem
- VirtualMachine
internal_derive:
- vsphere/architecture/resource-controls
related:
- vsphere/object-types/vm/configuration/resource-settings-guidance
- vsphere/object-types/resource-pool/configuration/scalable-shares
- vsphere/object-types/cluster/troubleshooting/vm-insufficient-resources-in-drs-cluster
- vsphere/technology/memory/concepts/memory-overhead
source:
  document: VMware vSphere 9.1 product documentation (PDF built 2026-11-02; the copyright page carries no revision number)
  path: vSphere Resource Management > Admission Control in vSphere, Resource Allocation Settings Suggestions, Potential Issues with CPU Affinity, Resource Pool Admission Control, Expandable Reservations Examples, DRS Cluster Validity, DRS Troubleshooting > Cluster Problems (pp. 1825-1826, 1831, 1891-1892, 1908-1911, 1950)
corrections: []
review_notes:
- 'Section ''Admission control'': the trap of non-identical hosts is from the author (Q051, 2026-11-06); the example (losing the largest host costs more) is Claude''s own knowledge.'
- 'Section ''Admission control'': the failover counter, level and summary from the author''s vCenter 9.1.0 API export, https://github.com/e1-rahabok/Observability-vSphere/blob/main/vsphere-metrics.csv.'
- 'Whole file: from the vSphere 9.1 documentation, not the book.'
status: draft
```
