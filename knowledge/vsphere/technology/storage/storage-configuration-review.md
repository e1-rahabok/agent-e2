# Storage configuration review

## Scope
- Every storage component of VCF: datastores, datastore clusters, RDM, vVols, vSAN, the physical array and general settings. One list, for the discussion with the storage team.
- VM-level storage settings (virtual disks, snapshots, RDM use, VM-to-datastore mapping): [`vsphere/object-types/vm/configuration/vm-configuration-review`](../../object-types/vm/configuration/vm-configuration-review.md). Host paths and zoning: [`vsphere/object-types/esxi/configuration/esxi-configuration-review`](../../object-types/esxi/configuration/esxi-configuration-review.md).

## Architecture variants
- Too many variants: VMFS over FC, VMFS over iSCSI, NFS, vSAN, vVols, physical RDM, virtual RDM.
- Each has its fit, and each needs its own expertise in performance, security, availability and upgrade. Every extra variant costs skills to keep current and raises the risk of overlooking something.
- vVols are deprecated from VCF 9.0 and will be removed in a future major release; vSphere 9.1 still supports them (vSphere 9.1 documentation, p. 1488; Broadcom KB 401070).

## Datastore
- Version: outdated VMFS or NFS versions.
- Local datastores: only for agent VMs or VMs that need neither vMotion nor backup. A backup read from a slow local disk competes with the VM for the same disk. Never a place for backups: they are forgotten there.
- Unused: no host accesses it (no path), or it holds no VM.
- Hardly used: few VMs, low activity (idle VMs), or low space use. Many such datastores mean sprawl and pockets of unused space.
- Small datastores fill faster from snapshots and over-provisioning.
- Too many datastore sizes.
- Paths: a single path has no redundancy; too many paths add complexity.
- Shared by more than one cluster: harder capacity monitoring and performance troubleshooting.
- Datastore cluster: members that differ cause capacity or performance problems.

## Other components
- LUN: unused (no VMFS or vVols on it). Inconsistent priority, such as Gold at the array and Silver in vSphere.
- NFS: current security for authentication.
- vVols: inventory matches expectation.
- Physical array: firmware compatible with the ESXi version.
- Queue depth: mismatches along the stack. Calibrate from the VM down to the array ([`vsphere/technology/storage/concepts/esxi-storage-io-path`](concepts/esxi-storage-io-path.md), section Queues on the path).
- VAAI: configured per practice.
- vSAN Max: no VMs in the storage cluster. It is meant as an array (simple, more than two controllers); running VMs on it adds a server dimension, like running VMs on your array.

## Misconceptions
- "The datastore has free space, so it is healthy" → check whether it is used at all, by how many VMs, and from how many clusters.
- "Local datastores are fine for backup targets" → backups there are forgotten, and backup reads compete with the VM.
- "The array is fast, so queue depth does not matter" → a mismatch anywhere in the stack queues IO in the kernel.
- "Gold at the array means Gold in vSphere" → priority must match at every layer.
- "vSAN Max can host a few VMs too" → it is the array; VMs on it add a server dimension.
- "Plan new designs on vVols" → vVols are deprecated from VCF 9.0 and will be removed in a future major release.

## Metadata
```yaml
id: vsphere/technology/storage/storage-configuration-review
retriever_guide: what-to-set
scope: vsphere
technology:
- storage
pillar:
- availability
- performance
- security
- capacity
product:
- vsphere
- vsan
object:
- Datastore
- StoragePod
- HostSystem
internal_derive:
- sp5-framework/concepts/configuration-management
related:
- vsphere/object-types/vm/configuration/vm-configuration-review
- vsphere/object-types/esxi/configuration/esxi-configuration-review
- vsphere/technology/storage/concepts/esxi-storage-io-path
- vsphere/technology/storage/concepts/esxi-storage-latency-stack
- vsphere/technology/storage/concepts/storage-layers
source:
  document: Knowledge base; VMware vSphere 9.1 product documentation (PDF built 2026-11-02; the copyright page carries no revision number); Broadcom KB 401070
  path: 'Configuration Management > Review List > Storage (Datastore, Others); vSphere Storage > Working with Virtual Volumes (p. 1488)'
corrections: []
review_notes: []
status: draft
```
