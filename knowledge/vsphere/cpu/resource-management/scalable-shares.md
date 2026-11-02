---
id: vsphere/cpu/resource-management/scalable-shares
type: concept
scope: vsphere
resources: [cpu, memory]
objects: [cluster, vm]
related:
  - vsphere/foundations/resource-management
  - vsphere/cpu/resource-management/drs-overview
source:
  document: Performance Best Practices for VMware vSphere 9.0 (revision 20250731)
  path: VMware Distributed Resource Scheduler (DRS) > DRS Cluster Sizing and Resource Settings (p. 79); DRS in General (p. 77)
corrections: []
review_notes:
  - "Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-90-performance-best-practices"
  - "Source does not state whether Scalable Shares is on or off by default. Not read."
status: draft
---

# Scalable Shares and resource pool siblings

## Scalable Shares (introduced in vSphere 7.0)
- Can be activated at the cluster level or at the resource pool level.
- Effect: resource pools and VMs receive dynamic, relative entitlements, based on their share values.
- Effect: resource pools and VMs can be siblings in one hierarchy without the dilution problem.

## When Scalable Shares is deactivated
- Do not make resource pools and VMs siblings in the same hierarchy level.
- Each level should contain only resource pools, or only VMs.
- Reason: resource pools then get default share values. These may not compare appropriately with VM share values.
- Result: unexpected performance.

## Reservations and shares
- Use a reservation to guarantee the minimum a VM must receive, not what the VM would like to get.
- Shares take effect only when there is resource contention.
- Memory overhead reserved for a VM must be included when sizing cluster resources.
- If cluster capacity may not meet peak demand, give higher shares to mission-critical VMs or pools. This reduces interference from less critical VMs.

## Reservations and limits in DRS
- Reservations set too high leave few unreserved resources in the cluster. This limits the vMotion options DRS can recommend.
- Limits set too low keep VMs from using extra resources available in the cluster, which would improve their performance.

## Traps
- "Shares guarantee CPU" → shares apply only under contention. A reservation is the guarantee.
- "Resource pools and VMs can always be siblings" → only with Scalable Shares active. Without it, mixing them causes dilution.
