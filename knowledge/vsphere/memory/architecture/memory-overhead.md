---
id: vsphere/memory/architecture/memory-overhead
type: concept
scope: vsphere
resources: [memory]
objects: [esxi, vm]
related:
  - vsphere/foundations/overhead
  - vsphere/memory/architecture/host-level-swapping
  - vsphere/memory/resource-management/memory-sizing
source:
  document: Performance Best Practices for VMware vSphere 9.0 (revision 20250731)
  path: ESX Memory Considerations > Memory Overhead (pp. 34-35)
corrections: []
review_notes:
  - "Superseded: vSphere 9.1 (revision 20260624) exists. This file was written from the 9.0 document (revision 20250731). Re-check against 9.1 before review."
  - "Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-90-performance-best-practices"
  - "Source links the per-VM overhead section to vSphere Resource Management for overhead details. Not read."
status: draft
---

# Memory overhead

## Definition
- Virtualization needs more physical memory than the configured memory of the VMs.
- Reason: ESX needs memory for its own code and data structures.
- The extra memory has two components:
  1. system-wide overhead,
  2. per-VM overhead.

## System-wide overhead
- Covers the VMkernel and host agents, for example hostd and vpxa.
- Under memory pressure, ESX can use a system swap file to reduce this overhead by up to 1 GB.
- The system swap file must be created manually first.
- Command, run from the ESX console:
```text
esxcli sched swap system set -d true -n <datastore name>
```
- The system swap file is 1 GB. It is created at the root of the specified datastore.
- It is separate from the per-VM swap files.

## Per-VM overhead
- Memory reserved for the VMX process: data structures that bootstrap and support the guest. Examples: thread stacks, text, heap.
- Memory reserved for the VMM: data structures the virtual hardware requires. Examples: TLB, memory mappings, CPU state.
- Memory reserved for virtual devices: for example mouse, keyboard, SVGA, USB.
- Memory reserved for other subsystems: for example the kernel and management agents.
- The amount depends on:
  - the number of vCPUs,
  - the configured memory of the VM,
  - whether the guest OS is 32-bit or 64-bit,
  - the VMM execution mode,
  - the features activated for the VM.
- The VMM and virtual device memory are fully reserved when the VM powers on.

## VMX swap
- VMX swap can significantly reduce the per-VM VMX memory reservation, which allows more memory to be swapped out when the host is overcommitted.
- A VMX swap file is created automatically for each VM. This reduces the host memory reserved for that VM.
- Location: the VM working directory, which is `workingDir` in the VMX file or, if that is not set, the directory of the VMX file.
- Alternative location: `sched.swap.vmxSwapDir`.
- Disk space: typically less than 100 MB for a large VM. Less than 300 MB if the VM uses 3D graphics.
- The VMX swap file retains a small working set. It is not swapped under ordinary use.
- Extraordinary use can cause swapping. Examples from the source: taking screenshots every second, or collecting a support dump.
- Deadlock risk: a datastore backed by a VM on the same host. The source does not recommend this configuration.
- To prevent VMX swap file creation: `sched.swap.vmxSwapEnabled` set to FALSE. The cost is a significantly increased memory reservation.
- VMX swap is unrelated to swap to host cache and to regular host-level swapping.

## Offsets
- ESX page sharing and other optimizations can save more memory than the overhead described here in some cases.

## Traps
- "Overhead is counted inside the configured memory of the VM" → the per-VM overhead is reserved in addition to the configured memory.
- "The VMX swap file is a regular swap file" → it is unrelated to host-level swapping and swap to host cache.
- "The system swap file is the same as a VM swap file" → it is a separate 1 GB file for the VMkernel and host agents.
