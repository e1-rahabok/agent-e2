# vSphere Cluster Services (vCLS)

## Status in vCenter 9.x
- vCenter 9.0 deprecates vCLS; the service is to be removed in a future vCenter release (Broadcom KB 312147).
- vCenter 9.0 also deprecates the requirement for vCLS to be active on a cluster and recommends switching vCLS to Retreat Mode (KB 312147). Retreat Mode deletes the vCLS VMs of the cluster; it is set per cluster under Configure > vSphere Cluster Services > General > Edit vCLS Mode (Broadcom KB 316514).
- From vCenter 9.0, deactivating vCLS does not impact vSphere DRS or vSphere HA (KB 312147). Before 9.0, Retreat Mode affected some cluster services.
- The vSphere 9.1 documentation still carries older text: a note in the Fault Tolerance pages says DRS depends on the vCLS VMs since vSphere 7.0 Update 1 (p. 2000), and the cluster Summary page shows a Cluster Services health status (pp. 1899-1900). KB 312147 states that its 9.0 update overrides earlier statements about the dependency.
- Performance Best Practices for vSphere 9.1 has no vCLS statement; the 9.0 edition said DRS requires the vCLS VMs and vCenter (p. 76).

## Footprint when vCLS runs
- A cluster that still runs vCLS VMs carries their reservations: 100 MHz CPU per vCLS VM, and 100 MB (External vCLS) or 160 MB (Embedded vCLS) memory per VM (Performance Best Practices 9.0, p. 79).
- External vCLS: at most 3 VMs per cluster, no more than about 400 MB memory and 400 MHz CPU per cluster. Embedded vCLS (vSphere 8.0 Update 3 and later): at most 2 VMs, about 400 MB and 200 MHz per cluster, no disk on a datastore.
- Embedded vCLS replaces External vCLS when vCenter is 8.0 Update 3 or later and at least one host of the cluster runs ESXi 8.0 Update 3 or later.

## Misconceptions
- "vCLS is required for DRS in vCenter 9.0 and later" → KB 312147 says deactivating vCLS does not impact DRS or HA from vCenter 9.0. The vSphere 9.1 note that DRS depends on vCLS is text kept from 7.0 Update 1.
- "vCLS VMs are a large cost to cluster capacity" → at most 3 small VMs per cluster, each with a small CPU and memory reservation (section Footprint when vCLS runs); Retreat Mode deletes them.
- "External and Embedded vCLS are the same" → they differ in VM count, memory and CPU footprint, and disk: Embedded vCLS has no virtual disk on a datastore.

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
- vsphere/object-types/resource-pool/resource-pool-design
source:
  document: vSphere Cluster Services (vCLS) in vSphere 7.0 Update 1 and newer versions (Broadcom KB 312147); Broadcom KB 316514; VMware vSphere 9.1 product documentation (PDF built 2026-11-02; the copyright page carries no revision number); Performance Best Practices for VMware vSphere 9.0 (revision 20250731); Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: KB 312147, Status (vCenter 9.0 section); vSphere 9.1 pp. 1899-1900 (Edit Cluster Settings), p. 2000 (Fault Tolerance, DRS note); Performance Best Practices 9.0 pp. 76, 79 (vSphere Cluster Services)
corrections:
- 'Section ''Status in vCenter 9.x'': the vSphere 9.1 documentation (p. 2000, Fault Tolerance note) says DRS depends on the availability of the vCLS VMs since vSphere 7.0 Update 1. Broadcom KB 312147 says that from vCenter 9.0 deactivating vCLS does not impact DRS or HA, and that this overrides earlier statements about the dependency. The knowledge base follows the KB.'
review_notes:
- 'To check: Section ''Status in vCenter 9.x'': the vCLS default state and whether it can be re-enabled in vCenter 9.1; no official 9.1 statement found (KB 312147 covers 9.0; vSphere 9.1 release notes and Product Support Notes, techdocs.broadcom.com).'
status: draft
```
