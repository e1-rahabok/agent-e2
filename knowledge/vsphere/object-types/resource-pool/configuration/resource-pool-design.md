# Resource pool design

## When to use a pool
- Use resource pools sparingly. A pool divides resources; it is not a folder for VMs.
- Delegated resource management: a pool sold as a service, where the tenant's contract sets the pool's reservation and limit. A tenant that bought 1 TB of RAM with no burst gets a 1 TB limit.
- A multi-tier service: group its VMs in one pool, so resources go to the service as a whole.
- One pool alone makes no operational sense. Create at least two, or none.
- Reservation and shares on the parent pool are easier to keep consistent than per-VM values for the VMs of one application.
- Read pool and VM shares and reservations together; with Scalable Shares, more so.

## Pool settings are cluster-wide
- A pool's reservation, limit and shares apply across the cluster, while each of its VMs runs on one host. In a large cluster a pool limit or share setting can hurt its VMs in ways hard to see from one host.
- Fixed vs expandable reservation is a design choice: Fixed isolates the pool (only its own reservation is admitted); expandable is flexible, but one child pool can take all of the parent's spare reservation. To isolate a pool fully, set it to Fixed with a reservation and a limit. How the admission check walks the tree: [`vsphere/object-types/cluster/concepts/admission-control-and-cluster-state`](../../cluster/concepts/admission-control-and-cluster-state.md).

## Siblings and Scalable Shares
- Rule: pools and VMs are not siblings. Each level of the tree holds only pools or only VMs. The rule holds with Scalable Shares off or on; only the reason changes.
- Scalable Shares (vSphere 7.0 and later) is set per cluster or per resource pool and is inherited. Off is the default.
- Off: a pool gets a fixed default share value (Normal: 4,000 CPU, 163,840 memory), divided among all its VMs. The more VMs in the pool, the less each gets, while a sibling VM keeps its full shares: dilution.
- On: a pool's shares follow its VMs: the sum of its VMs' shares × 4, 2 or 1 for High, Normal or Low. Dilution inside the pool is gone.
- On, with siblings: a Normal pool's VMs weigh twice a sibling Normal VM, and that weight moves with every VM added to the pool. Hard to read, so siblings stay a design error.
- Recommend Scalable Shares on for clusters with pools.
- Compare sibling pool values: if Gold should get 2x Silver, its shares must give 2x.
- Default share values per level: [`vsphere/architecture/resource-controls`](../../../architecture/resource-controls.md), section Shares.

## Nested pools
- Nested pools are often folders by mistake. Each level adds complexity to performance management; avoid sub-pools.

## Misconceptions
- "A resource pool is a folder for VMs" → it divides resources; a single or nested pool adds complexity without purpose.
- "Resource pools and VMs can be siblings once Scalable Shares is on" → dilution is gone, but the pool's VMs then weigh 2x a sibling VM at Normal and the weight changes as VMs are added. Keep each level pools only or VMs only.
- "A pool with High shares protects each of its VMs" → without Scalable Shares the pool's shares are divided among its VMs; a crowded High pool can give each VM less than a sibling VM.
- "A pool limit is felt the same on every host" → the limit is cluster-wide; a VM on one host can be capped by load elsewhere in the pool.

## Metadata
```yaml
id: vsphere/object-types/resource-pool/configuration/resource-pool-design
retriever_guide: what-to-set
scope: vsphere
technology:
- cpu
- memory
pillar:
- performance
product:
- vsphere
object:
- ClusterComputeResource
- VirtualMachine
internal_derive:
- vsphere/architecture/resource-controls
related:
- vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
- vsphere/object-types/vm/configuration/resource-settings-guidance
- vsphere/object-types/cluster/concepts/drs-overview
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624); Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'VMware Distributed Resource Scheduler (DRS) > DRS in General (p. 77); DRS Cluster Sizing and Resource Settings (p. 78); Configuration Management > Review List > Resource Pool'
corrections: []
review_notes:
- 'Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices'
- 'To check: Section Siblings and Scalable Shares: default off and the 4, 2, 1 multiplier, against vSphere 9.1 documentation, DRS Scalable Shares (Q110 c).'
status: draft
```
