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
- The exact overhead of a VM is written to its vmware.log at power-on: search for VMMEM.
- Representative per-VM overhead (documentation): about 4.5% of VM memory for a 256 GB VM, 5.5% for 64 GB, 6% for 16 GB. Smaller VMs carry proportionally more.
- The largest VM that powers on with a full reservation is smaller than free host memory: its overhead is reserved too.
- Hypervisor overhead: about 2% of memory on a 1 TB non-tiered host; about 7.96% on a host with 512 GB DRAM + 512 GB NVMe tiering.
- Reconfiguration changes overhead. Example: lowering a reservation from 250 GB to 0 adds about 25 MB of overhead for page-table mappings. Since vSphere 8.0 Update 3, DRS raises the VM's overhead limit before a reconfiguration, so the change does not fail on overhead.

## Overhead counter
- vCenter stores `mem.overhead` at level 1 on the VM, the ESXi host, the cluster and the resource pool: host physical memory consumed by ESXi data structures for running the VMs, in KB.
- ESXi and cluster values include the VMkernel overhead, not only the VMs' overhead.
- The resource pool value is the sum of its VMs' overhead. It is negligible: a resource pool has no overhead of its own.
- VM-level reading: `vsphere/technology/memory/metrics/virtual-motherboard/overhead`.

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
- "Resource pool overhead is a cost of the pool" → it is the sum of its VMs' overhead; the pool adds none.
- "Overhead is counted inside the configured memory of the VM" → the per-VM overhead is reserved in addition to the configured memory.
- "The VMX swap file is a regular swap file" → it is unrelated to host-level swapping and swap to host cache.
- "The system swap file is the same as a VM swap file" → it is a separate 1 GB file for the VMkernel and host agents.

## Metadata
```yaml
id: vsphere/technology/memory/concepts/memory-overhead
retriever_guide: how-it-works
scope: vsphere
technology:
- memory
pillar:
- capacity
product:
- vsphere
object:
- HostSystem
- VirtualMachine
internal_derive: []
related:
- vsphere/foundations/overhead
- vsphere/technology/memory/configuration/host-level-swapping
- vsphere/technology/memory/configuration/memory-sizing
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: ESX Memory Considerations > Memory Overhead (pp. 36-37)
corrections: []
review_notes:
- 'Section ''Overhead counter'': objects, level, unit and summary from the author''s vCenter 9.1.0 API export, https://github.com/e1-rahabok/Observability-vSphere/blob/main/vsphere-metrics.csv. What the host, cluster and resource pool values include: author answer (2026-11-04): ESXi and cluster include VMkernel overhead; resource pool is the sum of VM overhead, negligible.'
- 'Section ''Per-VM overhead'': VMMEM, the overhead percentages, hypervisor overhead and the DRS overhead limit from the vSphere 9.1 documentation, vSphere Resource Management > Overhead Memory on Virtual Machines, DRS Overhead Memory Management for VMs, Memory Tiering Troubleshooting > The Reservable Memory is Lower than Expected (pp. 1838, 1902-1903, 1958).'
- Checked against 9.1 (revision 20260624). Pages 36-37 unchanged.
- 'Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices'
- Source links the per-VM overhead section to vSphere Resource Management for overhead details. Not read.
status: draft
```
