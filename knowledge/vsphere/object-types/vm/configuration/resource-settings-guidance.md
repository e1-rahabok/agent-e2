# Resource settings: when and how

## Principle
- Use Reservation, Shares and Limits only where the environment requires them.
- Each setting has its own job. Set each for its purpose. See `vsphere/foundations/resource-controls`.

## Shares vs reservation
- Use Shares, not Reservation, to allocate resources fairly when total available resources change often.
- Reason: after a hardware change, a VM keeps the same relative priority (same share count), even though each share now represents a larger amount of memory or CPU.
- Reservation is not affected by the same change. It stays a fixed absolute amount.

## Reservation: minimum, not desired amount
- Use Reservation to set the minimum acceptable amount of CPU or memory for a VM.
- Resources above the reservations are allocated by shares, within the limits of the VM.
- Reservations give the minimum reserved CPU and memory for each VM. They do not change when VMs are added or removed.
- Do not set reservations too high. A reservation that is too high can limit the number of VMs that can be powered on in a resource pool, cluster, or host.

## Headroom
- When setting reservations, leave headroom for:
  - memory virtualization overhead,
  - migration overhead.
- Reservations that fully commit cluster or host capacity can stop DRS from migrating VMs between hosts.
- As capacity approaches full reservation, changing reservations or the resource pool hierarchy becomes harder without breaking admission control.

## Resource pools
- Use resource pools for delegated resource management.
- To isolate a resource pool fully, set its resource pool type to Fixed, and use Reservation and Limit.
- Group the VMs of a multi-tier service into one resource pool. Resources are then assigned to the service as a whole.
- For resource pool and sibling design, see `vsphere/foundations/scalable-shares`.

## Review: how each control affects operations
- Shares, reservation and limit sit in one dialog and are learned together, but they affect operations differently. Over years in a large environment they drift out of consistency.
![VM Limit: impacts the VM; should not be used, rightsize instead; unpredictable Guest OS performance; incorrect configuration. VM Reservation: impacts the infrastructure; keep the total low against cluster capacity; absolute (2 GHz is 2 GHz); no overcommit on the reserved part; suboptimal configuration. VM Share: impacts the infrastructure; at most 3 variations, 1 per class of service; relative to other VMs, so it changes when the VM moves cluster; harder troubleshooting as entitlements fluctuate; complex configuration](../images/vm-limit-reservation-share-impact-table.png)
- **Limit** (affects the VM; incorrect configuration):
  - a hard ceiling. Spare capacity is wasted rather than used; in return the consumer never exceeds what it paid for, and a denial-of-service attack is contained. It cuts both ways: cost against performance;
  - matters more for containers, which have no ceiling by default;
  - on a VM, avoid it: the Guest OS cannot see it and performance becomes unpredictable. Rightsize the VM instead;
  - VM limits exist for CPU, memory and disk IOPS;
  - valid use: a resource pool sold as a service. A tenant that bought 1 TB of RAM with no burst in the contract gets a 1 TB limit.
- **Reservation** (affects the infrastructure; suboptimal configuration):
  - a floor and a guarantee, so the total cannot exceed capacity. Absolute: 2 GHz is 2 GHz;
  - reserved capacity cannot be overcommitted, so use is less efficient;
  - high CPU and memory reservations complicate the cluster: they raise the HA slot size and narrow DRS placement. Reserve only for important VMs;
  - disk has no reservation for IOPS or throughput;
  - per VM or on the parent resource pool: for VMs of one application, the pool is easier.
- **Share** (affects the infrastructure; complex configuration):
  - works only on what is left after reservations, and only when demand exceeds it. With 80% reserved, shares divide the other 20%;
  - relative to siblings (VMs or resource pools), and by default proportional to configured size: a VM 10x bigger gets 10x the shares;
  - a VM moved to another cluster keeps its number, but the number means something else there. Keep share values consistent across clusters;
  - many share values per vCPU and per GB make troubleshooting harder: each VM's entitlement fluctuates more. Keep one value per class of service (Gold, Silver), at most 3.

## Review: share values
- Default VM shares:

| Level | CPU (per vCPU) | Memory |
|---|---|---|
| Low | 500 | 5 per MB |
| Normal | 1,000 | 10 per MB (10,240 per GB) |
| High | 2,000 | 20 per MB |

- Default resource pool shares:

| Level | CPU | Memory |
|---|---|---|
| Low | 2,000 | 81,920 |
| Normal | 4,000 | 163,840 |
| High | 8,000 | 327,680 |

- A Normal resource pool weighs as much as a Normal VM with 4 vCPU and 16 GB. Against a 1-vCPU, 1-GB sibling VM it gets 4x the CPU shares and 16x the memory shares.
- Resizing a VM in the vSphere Client recalculates default shares; resizing through the API does not. VMs whose shares were set by hand keep their number after a resize.
- Audit regularly: shares per vCPU should be 1,000 and per GB of RAM 10,240 (Normal). In one sample of 1,500 VMs, most sat at 1,000 per vCPU, with others at 4,000, 2,000, 1,500, 800, 650, 500, 250, 125 and 0. Some VMs carried resource pool values (4,000 CPU, 163,840 memory) on 1-2 vCPU VMs: 160 shares per GB on a 1 GB VM.
![Shares per vCPU across about 1,500 VMs, sorted: about 1,330 VMs at 1,000; outliers at 4,000, 2,000, 1,500, 800, 650, 500, 250, 125 and 0](../images/vm-cpu-shares-per-vcpu-across-vms-scatter.png)
- Example: a 10 GHz host, a 1-vCPU VM (1,000 shares) and a 2-vCPU VM (2,000 shares), both demanding more than the host has. Ignoring overhead, the split is 1:2, 3.33 and 6.67 GHz, but a 1-vCPU VM cannot take more than one physical core's worth. If each demands 5 GHz or less in total, each gets its demand: shares act only under contention.

## Review: resource pools
- Use them sparingly: when selling resource pools as a service. Read pool and VM shares and reservations together, more so with Scalable Shares.
- Children: without Scalable Shares, the pool's shares are divided among its VMs; the more VMs, the less each gets. Scalable Shares fixes this (`vsphere/foundations/scalable-shares`).
- Pool settings are cluster-wide while a VM runs on one host: in a large cluster, a pool limit or share setting can hurt its VMs in ways hard to see.
- Siblings:
  - a pool with VMs as siblings is a common mistake; one pool alone makes no operational sense (it is not a folder). Create at least two;
  - compare sibling values: if Gold should have 2x Silver, its shares must be 2x.
- Cascading: nested pools are often folders by mistake. Each level adds complexity to performance management; avoid sub-pools.

## Traps
- "Reservation is a target to aim for" → Reservation is a minimum. Shares divide the rest.
- "A CPU limit caps a noisy VM safely" → the Guest OS cannot see it; performance turns unpredictable. Rightsize instead.
- "The VM was resized, so its shares followed" → only a resize in the vSphere Client recalculates default shares; API resizes and hand-set values do not.
- "2,000 shares means the same priority on every cluster" → shares are relative to siblings; the same number means another share elsewhere.
- "A resource pool is a folder for VMs" → it divides resources; a single or nested pool adds complexity without purpose.
- "Set reservations high to be safe" → high reservations limit how many VMs can power on, and stop DRS migrations when they fully commit capacity.

## Metadata
```yaml
id: vsphere/object-types/vm/configuration/resource-settings-guidance
retriever_guide: what-to-set
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
- VirtualMachine
- HostSystem
internal_derive: []
related:
- operations-management/sp5-framework/configuration-management
- operations-management/sp5-framework/class-of-service
- vsphere/foundations/resource-controls
- vsphere/foundations/scalable-shares
- vsphere/object-types/cluster/concepts/drs-overview
- vsphere/object-types/cluster/concepts/dpm
images:
  - path: ../images/vm-limit-reservation-share-impact-table.png
    product: [vsphere]
    object: [VirtualMachine]
    topic: 'VM limit, reservation and share: what each affects and its configuration class'
    image_type: table
  - path: ../images/vm-cpu-shares-per-vcpu-across-vms-scatter.png
    product: [vsphere]
    object: [VirtualMachine]
    metric: [CPU shares per vCPU]
    topic: 'Share audit: shares per vCPU across VMs'
    image_type: scatter
    sample: 'about 1,500 VMs'
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624); PART 1 - Concepts of Operations Management.docx
  path: 'Virtual Infrastructure Management > General Resource Management (p. 65); Part 1, Configuration Management > Review List > Resource Management, Share, Reservation, Limit, Resource Pool (pp. 138-141)'
corrections: []
review_notes:
- Checked against 9.1 (revision 20260624). Page 65 unchanged.
- 'Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices'
- The source does not define a headroom percentage for memory virtualization overhead and migration overhead. Author to confirm whether the book gives one.
- 'Sections Review (2026-11-07) from the book. Default memory shares: the book''s table says 5, 10, 20 per GB; its text and the vSphere defaults are per MB (10,240 per GB at Normal). Written per MB. Q108.'
- 'Share example: the book has both VMs demanding 10 GHz; a 1-vCPU VM cannot exceed one physical core. The book''s last line says VM 1 twice. Q108.'
- 'The impact table image says a share of 2,000 depends on other VMs'' reservations; meant as shares. Q108.'
- 'Resource pool weighing as a 4-vCPU, 16-GB VM: Claude''s explanation of the book''s 4x and 16x (the book says it is unsure why).'
- 'Limit: the book says there is no network limit; vSphere has per-vNIC limits under Network I/O Control (vsphere/foundations/noisy-neighbour). Q109.'
- 'HA slot size: only under the slot policy admission control. Q110.'
- 'Siblings: the book calls VM and pool siblings a mistake; with Scalable Shares the dilution is solved (vsphere/foundations/scalable-shares). Both kept. Q110.'
status: draft
```
