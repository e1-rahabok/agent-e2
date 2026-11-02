---
id: vsphere/cpu/resource-management/vcls
type: concept
scope: vsphere
resources: [cpu, memory, storage]
objects: [cluster, vm]
related:
  - vsphere/cpu/resource-management/drs-overview
  - vsphere/cpu/resource-management/scalable-shares
source:
  document: Performance Best Practices for VMware vSphere 9.0 (revision 20250731)
  path: VMware Distributed Resource Scheduler (DRS) > DRS in General (p. 76); DRS Cluster Sizing and Resource Settings (p. 79)
corrections: []
review_notes:
  - "Superseded: vSphere 9.1 (revision 20260624) exists. This file was written from the 9.0 document (revision 20250731). Re-check against 9.1 before review."
  - "Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-90-performance-best-practices"
  - "Table values come from the 9.0 source. Check them against VMware Configuration Maximums before use."
status: draft
---

# vSphere Cluster Services (vCLS)

## Purpose
- vCLS runs cluster services, such as DRS and HA, as agent VMs.
- See `vsphere/cpu/resource-management/drs-overview` for the vCenter dependency that remains in vSphere 9.0.

## Versions
- External vCLS:
  - created automatically on a new installation of vSphere 7.0 Update 1 or later,
  - or when a vCenter Server deployment is upgraded to vSphere 7.0 Update 1 or later.
  - In vSphere 8.0 Update 3, the earlier version is called External vCLS.
- Embedded vCLS:
  - introduced in vSphere 8.0 Update 3,
  - used instead of External vCLS when vCenter is 8.0 Update 3 or later and at least one host in the cluster runs ESXi 8.0 Update 3 or later.

## Footprint per cluster
- Either version has only a minimal impact on cluster capacity.
- External vCLS:
  - maximum 3 VMs per cluster,
  - consumes no more than about 400 MB memory and 400 MHz CPU per cluster.
- Embedded vCLS:
  - maximum 2 VMs per cluster,
  - consumes no more than about 400 MB memory and 200 MHz CPU per cluster.

## Per VM specification
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

## Limits
- Exceeding the VMware Configuration Maximums for a DRS cluster is not supported.
- Source: even when it seems to work, exceeding the maximums can adversely affect vCenter Server or DRS performance.

## Traps
- "vCLS VMs are a large cost to cluster capacity" → the source describes the footprint as minimal, with a 100 MHz CPU reservation per VM.
- "External and Embedded vCLS are the same" → they differ in VM count, memory and CPU limits, and disk footprint.
