# Host-level swapping

## Bounded overcommit
- ESX supports a bounded amount of memory overcommitment without host-level swapping.
- If overcommitment is so large that the other reclamation techniques are not enough, ESX uses host-level swapping.
- Host-level swapping can have a significant impact on VM performance.

## Other reclamation techniques
- Do not deactivate page sharing, ballooning or memory compression.
- These techniques reduce the need for host-level swapping.

## Swap file size
- At every power-on, ESX creates a swap file (.vswp) for the VM, and at power-off it deletes the file. A powered-off VM holds no swap file, so powering on many VMs at once needs the free space of all their swap files at that moment.
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
- Preferred order, from Performance Best Practices for vSphere 9.1:
  1. local SSD, usually the best choice,
  2. remote SSD, if the host has no local SSD. Still provides low latency, with the added latency of remote access.
  3. the fastest available storage, if no SSD can be used, for example a Fibre Channel SAN array or a fast local disk.
- Local SSD is recommended for the swap to host cache. Performance Best Practices for vSphere 9.1 notes that local SSD space is often too small for a host's entire swap file needs.
- Placing swap files on local storage can reduce vMotion performance. Pages in a local swap file must be swapped back into memory before the vMotion can proceed.
- Regardless of storage type, swap files should not be placed on thin-provisioned storage. Reason: performance and the risk of running out of space.
- Swap file location per VM: vSphere Client, right-click the VM, Edit Settings, VM Options tab, expand Advanced, select Swap file location.
- Default location: the directory specified by `workingDir` in the VMX file, or the directory of the VMX file if `workingDir` is not set.

## Swap file location and vMotion
- The swap file location is set per cluster: Virtual machine directory (the default) or Datastore specified by host. With the second, each host names its own swap datastore. A VM setting can override the cluster setting.
- A host with no swap datastore specified, a host that cannot reach the specified datastore, or a specified datastore that cannot hold the file: the swap file goes with the VM configuration file (vSphere 9.1 documentation, pp. 624, 1875-1876). A half-configured cluster therefore keeps some swap files on the shared datastore.
- vMotion with the same swap location on source and destination (a shared datastore) does not move the swap file.
- vMotion with different swap locations on source and destination copies the swap file to the destination location. The vSphere documentation says this can slow the migration. The copy happens because the locations differ, whether or not any page was swapped.
- With host-local swap, pages already swapped to the local swap file of the source host must also be transferred across the network to the destination host.
- A DRS cluster that migrates often pays the swap file copy on every migration between hosts with different swap locations.
- A shared datastore on cheaper storage as the swap location of all hosts frees the VM datastores without the vMotion copy, because both ends use the same location.
- vSAN and vVols datastores cannot be specified as the host-local swap location.

## Swap space per host
- The swap file is created at power-on with its full size (configured memory minus reservation), whether or not the host ever swaps. An empty swap file still takes its full size on the datastore.
- When the swap datastore the host specifies cannot hold the swap file, ESXi stores the file in the VM's folder instead (vSphere 9.1 documentation, pp. 1875-1876). A VM powers on only when its swap file can be created (p. 1873): it fails when the VM's folder cannot hold the file either. This includes a VM restarted by vSphere HA on another host.
- With host-local swap, swap space is a per-host limit, not a cluster total. A local swap datastore that runs short sends the overflow to the VMs' folders on the shared datastores, which then hold the swap files the design meant to keep off them. Size each local swap datastore for the largest set of VMs the host can run, including VMs moved there by DRS, maintenance mode or an HA restart after a host failure.
- Check the cluster total with one host out: the sum of swap file sizes against the local swap datastores of the remaining hosts.
- Changing the swap file location does not move the swap file of a running VM. The file moves at the next power-on, or when a vMotion copies it to a host with a different location, so the old datastore frees space gradually.
- Raising memory reservations shrinks the swap files. A reservation equal to configured memory gives a swap file of zero bytes, at the cost of host memory that other VMs cannot use.

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
- "Powered-off VMs keep their swap files, so powering them on needs no new space" → the swap file is created at each power-on and deleted at power-off; a VM whose swap file fits neither on the host's swap datastore nor in its own folder does not power on.
- "Put the swap file on the fastest datastore" → Performance Best Practices for vSphere 9.1 ranks local SSD first, then remote SSD, then fastest available storage. Thin-provisioned storage is excluded.
- "Local swap files speed up vMotion" → Performance Best Practices for vSphere 9.1 says they can reduce vMotion performance.
- "The swap file is empty when memory is not overcommitted, so its location costs nothing" → the file takes its full size from power-on, and vMotion copies it whenever source and destination use different swap locations.
- "Local NVMe is faster than the SAN, so host-local swap speeds up vMotion" → device latency helps only host-level swapping. vMotion gets slower: the swap file is copied between locations, and swapped pages cross the network.
- "Total local swap space above the total swap file size is enough" → the limit is per host. A swap file that does not fit on the host's swap datastore goes to the VM's folder on shared storage; the power-on fails, also after an HA restart, only when that folder cannot hold it either. Check with one host out.
- "Setting the cluster swap location frees the old datastore at once" → a running VM keeps its swap file until its next power-on or a vMotion that copies it.
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
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624); vSphere 9.1 vCenter Server and Host Management and vSphere Resource Management (PDF build of 2026-11-02)
  path: ESX Memory Considerations > Memory Swapping Optimizations (pp. 35-36); Virtual Machines Swap File Location and vSphere vMotion Compatibility (p. 624); Using Swap Files, Swap File Location (p. 1873); Configure Virtual Machine Swapfile Properties for the Host, Configure a Virtual Machine Swap File Location for a Cluster, Delete Swap Files (pp. 1875-1876)
corrections: []
review_notes:
- 'To check: Section ''Swap space per host'': that a running VM keeps its swap file until its next power-on or a vMotion copy is inferred from creation at power-on (p. 1873) and the copy when locations differ (p. 624); no vendor page states it.'
status: draft
```
