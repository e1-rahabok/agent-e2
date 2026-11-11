# Storage configuration review

## Scope
- Every storage component of VCF: datastores, datastore clusters, RDM, vVols, vSAN, the physical array and general settings. One list, for the discussion with the storage team.
- VM-level storage settings (virtual disks, snapshots, RDM use, VM-to-datastore mapping): [`vsphere/object-types/vm/configuration/vm-configuration-review`](../../../object-types/vm/configuration/vm-configuration-review.md). Host paths and zoning: [`vsphere/object-types/esxi/configuration/esxi-configuration-review`](../../../object-types/esxi/configuration/esxi-configuration-review.md).

## Architecture variants
- Too many variants: VMFS over FC, VMFS over iSCSI, NFS, vSAN, vVols, physical RDM, virtual RDM.
- Each has its fit, and each needs its own expertise in performance, security, availability and upgrade. Every extra variant costs skills to keep current and raises the risk of overlooking something.
- vVols are deprecated in VCF 9.

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
- Queue depth: mismatches along the stack. Calibrate from the VM down to the array ([`vsphere/technology/storage/concepts/esxi-storage-latency-stack`](../concepts/esxi-storage-latency-stack.md)).
- VAAI: configured per practice.
- vSAN Max: no VMs in the storage cluster. It is meant as an array (simple, more than two controllers); running VMs on it adds a server dimension, like running VMs on your array.

## Misconceptions
- "The datastore has free space, so it is healthy" → check whether it is used at all, by how many VMs, and from how many clusters.
- "Local datastores are fine for backup targets" → backups there are forgotten, and backup reads compete with the VM.
- "The array is fast, so queue depth does not matter" → a mismatch anywhere in the stack queues IO in the kernel.
- "Gold at the array means Gold in vSphere" → priority must match at every layer.
- "vSAN Max can host a few VMs too" → it is the array; VMs on it add a server dimension.
- "Plan new designs on vVols" → vVols are deprecated in VCF 9.

## Metadata
```yaml
id: vsphere/technology/storage/configuration/storage-configuration-review
retriever_guide: what-to-set
scope: vsphere
technology:
- storage
pillar:
- availability
- performance
- compliance
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
- vsphere/technology/storage/concepts/esxi-storage-latency-stack
- vsphere/technology/storage/concepts/storage-layers
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Configuration Management > Review List > Storage (Datastore, Others)'
corrections: []
review_notes:
- 'To check: whether vSphere 9.1 still supports vVols (vSphere 9.1 release notes). vVols deprecated in VCF 9.0: Broadcom KB 401070 (https://knowledge.broadcom.com/external/article/401070); Protection and Recovery 9.1 release notes (https://techdocs.broadcom.com/us/en/vmware-cis/vcf/protection-and-recovery/9-1/release-notes/protection-and-recovery-91-release-notes.html) say 9.1 is its last release supporting vVols.'
- 'Queue depth misconception: the kernel queueing mechanism is from vsphere/technology/storage/concepts/esxi-storage-latency-stack, not from the book.'
status: draft
```
