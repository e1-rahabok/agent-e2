# Resource settings: when and how

## Principle
- Use Reservation, Shares and Limits only where the environment requires them.
- Each setting has its own job. Set each for its purpose. See `vsphere/resource-management/concepts/resource-controls`.

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
- For resource pool and sibling design, see `vsphere/resource-management/concepts/scalable-shares`.

## Traps
- "Reservation is a target to aim for" → Reservation is a minimum. Shares divide the rest.
- "Set reservations high to be safe" → high reservations limit how many VMs can power on, and stop DRS migrations when they fully commit capacity.

## Metadata
```yaml
id: vsphere/resource-management/configuration/resource-settings-guidance
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
- vsphere/resource-management/concepts/resource-controls
- vsphere/resource-management/concepts/scalable-shares
- vsphere/resource-management/concepts/drs-overview
- vsphere/resource-management/concepts/dpm
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: Virtual Infrastructure Management > General Resource Management (p. 65)
corrections: []
review_notes:
- Checked against 9.1 (revision 20260624). Page 65 unchanged.
- 'Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices'
- The source does not define a headroom percentage for memory virtualization overhead and migration overhead. Author to confirm whether the book gives one.
status: draft
```
