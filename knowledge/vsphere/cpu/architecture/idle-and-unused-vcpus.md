---
id: vsphere/cpu/architecture/idle-and-unused-vcpus
type: concept
scope: vsphere
resources: [cpu]
objects: [vcpu, vm, guest-os, esxi]
related:
  - vsphere/cpu/architecture/virtualization-overhead
  - vsphere/cpu/architecture/virtual-numa
  - vsphere/foundations/vm-vs-guest-os
source:
  document: Performance Best Practices for VMware vSphere 9.0 (revision 20250731)
  path: ESX CPU Considerations (pp. 24-25); Guest Operating System CPU Considerations (p. 55); Virtual NUMA (pp. 55-57)
corrections: []
review_notes:
  - "Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-90-performance-best-practices"
status: draft
---

# Unused and idle vCPUs

## Cost of extra vCPUs
- A VM with more vCPUs than its workload uses has slightly increased resource usage.
- On heavily loaded systems, this can affect performance.
- Common cases:
  - a single-threaded workload in a multi-vCPU VM,
  - a multi-threaded workload in a VM with more vCPUs than the workload can use effectively.

## Costs that remain when vCPUs are idle
- Some guest OSes send timer interrupts to unused vCPUs.
- Tickless timer kernels do not send these interrupts.
- A consistent memory view across vCPUs uses resources in the guest OS and in ESX.
- Guest idle loops:
  - most guest OSes halt an idle vCPU with the HLT or MWAIT instruction,
  - some guest OSes busy-wait instead: Windows 2000 (with certain HALs), Solaris 8 and 9, MS-DOS.
- Busy-wait loops use resources that other VMs, the VMkernel and other tasks could use.

## How ESX handles idle vCPUs
- ESX detects HLT and MWAIT idle loops.
- ESX de-schedules the idle vCPU.
- Effect: lower CPU overhead.
- Side effect: possibly reduced performance for some I/O-heavy workloads.

## Guest scheduler migration
- The guest OS scheduler can move a single-threaded workload from one vCPU to another.
- Each move incurs a small CPU overhead.
- Each move loses cache locality.
- Pinning guest threads or processes to specific vCPUs can help.
- Pinning is another reason not to configure VMs with more vCPUs than the workload uses.

## Scaling out vs scaling up
- The same vCPU count can run as more, smaller VMs ("scaling out") or as fewer, larger VMs ("scaling up").
- Scaling out can perform better. Scaling up can perform better.
- The better option depends on:
  - NUMA node size,
  - CPU cache locality,
  - workload implementation.
- The source recommends testing with the specific workload in the specific environment.

## CPU Hot Add
- Adding vCPUs to a running VM with CPU Hot Add deactivates vNUMA for that VM.
- The guest then sees a single vNUMA node.
- Without vNUMA, the guest OS has no knowledge of the host CPU and memory topology.
- Result: sub-optimal guest scheduling decisions, and reduced performance for applications in large VMs.
- Activate CPU Hot Add only if the VM is expected to use it.
- Alternatives:
  - power off the VM before adding vCPUs,
  - configure the VM with the maximum vCPU count the workload might require.
- Unused vCPUs cost a small amount of overhead, and can cause poor guest scheduling decisions.

## Traps
- "Idle vCPUs cost nothing" → idle vCPUs still cost timer interrupts (some guests), memory-view upkeep, and busy-wait loops (some guests).
- "More vCPUs is always safer" → extra vCPUs add overhead and can degrade scheduling in the guest.
