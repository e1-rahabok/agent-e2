# vSphere Cluster Services (vCLS)

## Status
- vCenter 9.0: deprecated. Removal planned for a future vCenter release. Source: KB 312147.
- vCenter 9.0 deprecates the requirement for vCLS to be active on clusters. KB 312147 recommends Retreat Mode.
- vCenter 9.1: 
  - vCLS is off by default,
  - it cannot be re-enabled,
  - SDDC Manager and VCF Installer controls were removed.
  - Not verified against official 9.1 documents.
- DRS and HA, vCenter 9.0 and later: KB 312147 says deactivating vCLS does not impact DRS or HA.
- Conflict: the 9.0 performance document (p. 76) says DRS requires the vCLS VMs and vCenter Server. KB 312147 overrides that statement for 9.0 and later.
- The 9.1 performance document has no vCLS statement in its DRS pages (76-79).

## Purpose (historical)
- vCLS runs cluster services as agent VMs.
- Before vCenter 9.0, KB 312147 describes vCLS as mandatory from vSphere 7.0 Update 1. DRS depended on it, and Retreat Mode affected some cluster services.

## Versions (historical)
- External vCLS:
  - created automatically on a new installation of vSphere 7.0 Update 1 or later,
  - or when a vCenter Server deployment is upgraded to vSphere 7.0 Update 1 or later.
  - In vSphere 8.0 Update 3, the earlier version is called External vCLS.
- Embedded vCLS:
  - introduced in vSphere 8.0 Update 3,
  - used instead of External vCLS when vCenter is 8.0 Update 3 or later and at least one host in the cluster runs ESXi 8.0 Update 3 or later.

## Footprint per cluster (9.0 document, historical)
- Either version has only a minimal impact on cluster capacity.
- External vCLS:
  - maximum 3 VMs per cluster,
  - consumes no more than about 400 MB memory and 400 MHz CPU per cluster.
- Embedded vCLS:
  - maximum 2 VMs per cluster,
  - consumes no more than about 400 MB memory and 200 MHz CPU per cluster.

## Per VM specification (9.0 document, historical)
| Resource | External vCLS VM | Embedded vCLS VM |
|---|---|---|
| Memory | 128 MB | Maximum 200 MB |
| Memory reservation | 100 MB | 160 MB |
| Swap size | 256 MB | 0 MB |
| vCPUs | 1 | 1 |
| CPU reservation | 100 MHz | 100 MHz |
| Hard disk | 2 GB, thin provisioned | 0 GB |
| Network interfaces | 0 (no NIC) | 0 (no NIC) |
| VMDK size | About 245 MB | 0 MB |
| Storage space | About 480 MB | 0.1 MB |

## Limits (9.0 document)
- Exceeding the VMware Configuration Maximums for a DRS cluster is not supported.
- Source: even when it seems to work, exceeding the maximums can adversely affect vCenter Server or DRS performance.

## Traps
- "vCLS is required for DRS in vCenter 9.0 and later" → KB 312147 says DRS and HA do not depend on vCLS in 9.0 and later. The 9.0 performance document says otherwise. KB overrides it.
- "vCLS is available in vCenter 9.1" → it is deprecated. Third-party sources say it is off by default and cannot be re-enabled. Verify against official 9.1 notes.
- "vCLS VMs are a large cost to cluster capacity" → the 9.0 document describes the footprint as minimal, with a 100 MHz CPU reservation per VM.
- "External and Embedded vCLS are the same" → they differ in VM count, memory and CPU limits, and disk footprint.

## Metadata
```yaml
id: vsphere/object-types/cluster/concepts/vcls
retriever_guide: how-it-works
scope: vsphere
technology:
- cpu
- memory
- storage
pillar:
- availability
product:
- vsphere
object:
- ClusterComputeResource
- VirtualMachine
internal_derive: []
related:
- vsphere/object-types/cluster/concepts/drs-overview
- vsphere/object-types/resource-pool/configuration/scalable-shares
source:
  document: vSphere Cluster Services (vCLS) in vSphere 7.0 Update 1 and newer versions (Broadcom KB 312147)
  path: Status (vCenter 9.0 section); Context (pre-9.0). Footprint section from Performance Best Practices for VMware vSphere 9.0 (revision 20250731), pp. 76 and 79.
corrections: []
review_notes:
- 'Source URL: https://knowledge.broadcom.com/external/article?articleNumber=312147 (last updated date not shown on the page). Source states: ''vCenter 9.0 deprecates vCLS, and the service will be removed in a future vCenter release.'' and ''Deactivating vCLS does not impact the operation of vSphere DRS and vSphere HA services.'''
- Broadcom KB 316514 (Retreat Mode) is referenced by KB 312147. Not read.
- 'vCenter 9.1: user states vCLS is deprecated in 9.1. Third-party sources (vinfrastructure.it, May 2026; StarWind) say vCenter 9.1 turns vCLS off by default and it cannot be re-enabled, and that SDDC Manager and VCF Installer controls were removed. Not verified against official 9.1 release notes or Product Support Notes. Author to confirm the 9.1 status and wording.'
- Footprint tables are from the 9.0 performance document (pp. 76, 79). The 9.1 document has no vCLS section. Treat as historical (7.0 Update 1 to 8.x). Check VMware Configuration Maximums before any use.
status: draft
```
