# Host-level swapping and swap placement

## Bounded overcommit
- ESX supports a bounded amount of memory overcommitment without host-level swapping.
- If overcommitment is so large that the other reclamation techniques are not enough, ESX uses host-level swapping.
- Host-level swapping can have a significant impact on VM performance.

## Keep the other techniques active
- Do not deactivate page sharing, ballooning or memory compression.
- These techniques reduce the need for host-level swapping.

## Swap file size
- At first power-on, ESX creates a swap file for each VM.
- Size of the swap file: configured memory of the VM minus the memory reservation of the VM.
- Disk space must be at least this large, plus the space for VMX swap. See [`vsphere/technology/memory/concepts/memory-overhead`](../concepts/memory-overhead.md).

## Swap to host cache
- Optional. Configured on an SSD, if one is installed.
- Shared by all VMs on the host. The host-level swapping of their most active pages benefits from the low latency of the SSD.
- Gives a large performance gain for a relatively small amount of SSD storage.
- Swap to host cache and a regular swap file on SSD are two different approaches to improving swapping performance.
- ESX still creates regular swap files when swap to host cache is used.
- Swap to host cache matters less for the speed of the storage holding the regular swap files.

## Regular swap file placement
- Preferred order, from the source:
  1. local SSD, usually the best choice,
  2. remote SSD, if the host has no local SSD. Still provides low latency, with the added latency of remote access.
  3. the fastest available storage, if no SSD can be used. The source gives a Fibre Channel SAN array or a fast local disk as examples.
- Local SSD is recommended for the swap to host cache. The source notes that local SSD space is often too small for a host's entire swap file needs.
- Placing swap files on local storage can reduce vMotion performance. Pages in a local swap file must be swapped back into memory before the vMotion can proceed.
- Regardless of storage type, swap files should not be placed on thin-provisioned storage. Reason: performance and the risk of running out of space.
- Swap file location per VM: vSphere Client, right-click the VM, Edit Settings, VM Options tab, expand Advanced, select Swap file location.
- Default location: the directory specified by `workingDir` in the VMX file, or the directory of the VMX file if `workingDir` is not set.

## Reservations reduce host-level swapping
- Reserving memory at least equal to the active working set of a VM can reduce host-level swapping for that VM.
- Reserving memory equal to the full memory of a VM can eliminate host-level swapping for that VM.
- Effect on a running VM can appear gradually. Power-cycle the VM to see the full effect immediately.
- A reservation is a guaranteed lower bound on the physical memory ESX reserves for the VM.
- Set through vSphere Client: right-click the VM, Edit Settings, Virtual Hardware tab, expand Memory, set the reservation.
- Trade-off: reservations reduce the number of VMs that can run on a host, cluster or resource pool. ESX keeps enough memory for all reservations, so it does not power on a VM if that would reduce available memory below the reserved amount.
- See [`vsphere/object-types/vm/configuration/resource-settings-guidance`](../../../object-types/vm/configuration/resource-settings-guidance.md) for reservation guidance.

## Misconceptions
- "Swap file size equals configured memory" → size is configured memory minus reservation.
- "Put the swap file on the fastest datastore" → the source ranks local SSD first, then remote SSD, then fastest available storage. Thin-provisioned storage is excluded.
- "Local swap files speed up vMotion" → the source says they can reduce vMotion performance.
- "Turning off page sharing or compression improves performance" → they reduce the need for host-level swapping, and should stay active.

## Metadata
```yaml
id: vsphere/technology/memory/configuration/host-level-swapping
retriever_guide: what-to-set
scope: vsphere
technology:
- memory
- storage
pillar:
- performance
product:
- vsphere
object:
- HostSystem
- VirtualMachine
- Datastore
internal_derive: []
related:
- vsphere/technology/memory/concepts/host-memory-states
- vsphere/technology/memory/concepts/memory-overhead
- vsphere/technology/memory/decision-tree/is-overcommit-affecting-vm
- vsphere/object-types/vm/configuration/resource-settings-guidance
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: ESX Memory Considerations > Memory Swapping Optimizations (pp. 35-36)
corrections: []
review_notes:
- Checked against 9.1 (revision 20260624). Pages 35-36 unchanged. Swap file location menu path unchanged (p. 36).
- 'Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices'
- Swap file location menu path is unchanged in the 9.1 document (p. 36).
status: draft
```
