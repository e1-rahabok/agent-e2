---
id: vsphere/cpu/resource-management/drs-overview
type: concept
scope: vsphere
resources: [cpu, memory]
objects: [cluster, vm, esxi]
related:
  - vsphere/cpu/resource-management/drs-migration-levels
  - vsphere/cpu/resource-management/scalable-shares
  - vsphere/cpu/resource-management/vcls
  - vsphere/cpu/resource-management/dpm
  - vsphere/cpu/resource-management/resource-settings-guidance
  - vsphere/foundations/resource-management
source:
  document: Performance Best Practices for VMware vSphere 9.0 (revision 20250731)
  path: VMware Distributed Resource Scheduler (DRS) > DRS in General (p. 76); DRS Cluster Configuration Settings (pp. 76-79)
corrections: []
review_notes:
  - "Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-90-performance-best-practices"
status: draft
---

# DRS overview

## Dependencies in vSphere 9.0
- vSphere Cluster Services (vCLS) maintains cluster services such as DRS and HA.
- Source: vCLS maintains workload resources and health regardless of vCenter availability.
- As of vSphere 9.0, cluster services still require both the vCLS VMs and vCenter Server.
- Not all functions have moved to the vCLS VMs.
- If there are issues with the vCLS VMs, DRS cannot be activated. If DRS is already active, the issues stop it from operating.
- Warning on the Cluster Summary page indicates these issues.
- See `vsphere/cpu/resource-management/vcls`.

## Cluster health indicators
- Watch for manual recommendations. Unaddressed manual recommendations can stop DRS from generating new recommendations.
- Watch for DRS faults caused by affinity rule violations. Fixing them can significantly help load balancing.
- Since vSphere 7.0, the Cluster DRS Score replaces the cluster balance metric. See `vsphere/cpu/resource-management/drs-migration-levels`.

## Host homogeneity
- Group hosts that are as similar as possible in CPU and memory. This improves predictability and stability.
- When hosts have compatible CPUs but different frequencies or memory amounts, DRS prefers hosts with more memory and higher CPU frequency for VMs, other things being equal.
- Reason: those hosts have more capacity for peak loads.

## vMotion compatibility
- vMotion is not supported across incompatible CPUs.
- CPU compatibility requires:
  - the same CPU vendor,
  - similar CPU families,
  - matching SSE instruction-set capability.
- Enhanced vMotion Compatibility (EVC) allows vMotion between different CPU generations. See KB 1003212.
- Other blockers the source lists:
  - vMotion network adapters not connected by a 1 Gb/s or faster Ethernet link,
  - misconfigured vMotion gateway,
  - incompatible security policies between source and destination hosts,
  - VM hardware version incompatibility,
  - VM network not available on the destination host.
- More vMotion-compatible hosts give DRS more options for recommendations.
- Connectivity: every host in a DRS cluster should reach the full set of datastores that the other hosts reach.

## VM size and memory
- Smaller VMs (less memory and fewer vCPUs) give DRS more migration opportunities.
- Larger VMs add constraints to migration.
- Since vSphere 7.0, DRS uses granted memory (total RAM available to the VM) when it evaluates a VM memory demand for vMotion recommendations.
- Over-provisioned VM memory therefore constrains DRS migration options more than in earlier versions.
- Configure each VM with only as many vCPUs and as much memory as its workload requires.

## Powered-on idle VMs
- Powered-on VMs consume memory, and typically some CPU, even when idle.
- Idle VMs can affect DRS decisions.
- Shutting down or suspending VMs that are not in use can give a marginal performance gain.

## Affinity rules
- VM/VM affinity: keeps VMs on the same host.
- VM/VM anti-affinity: keeps VMs on different hosts.
- VM/Host affinity: a group of VMs runs only on, or preferably on, a group of hosts.
- VM/Host anti-affinity: a group of VMs never runs on, or preferably does not run on, a group of hosts.
- Default affinity setting types:
  - Keep Virtual Machines Together: lower communication latency between VMs.
  - Separate Virtual Machines: higher availability. Co-locating I/O-intensive VMs can saturate host I/O capacity.
  - Virtual Machines to Hosts: Must run on, Should run on, Must not run on, Should not run on. Useful for licensing or availability zone requirements.
- In most cases, leave the affinity settings at their defaults. In rare cases, rules improve performance.

## Flexibility guidance
- Place VMs on shared datastores accessible from all hosts in the cluster.
- Do not connect VMs to host devices that prevent them from moving off the host.
- DRS includes NetIOC bandwidth reservations in its calculations.
- Leave unused and unreserved CPU capacity in the cluster for vMotion. ESX reserves some CPU resources for each vMotion operation.
