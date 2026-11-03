# VMkernel worlds

## Definition
- The ESXi kernel (VMkernel) is an OS whose purpose is to run multiple virtual motherboards (VMs).
- Its metrics therefore differ from those of general-purpose OSes such as Windows and Linux.
- From the kernel's vantage point, a VM is a collection of processes that must run together.
- Each schedulable process is called a world.
- Each vCPU of a VM is a separate world, because each vCPU is scheduled independently.
- VM worlds and non-VM worlds run side by side. Examples of non-VM worlds: `hostd`, `vpxa`, `vsanmgmtd`, `system`.
- esxtop shows both kinds in the same list.

## VM process groups
From the kernel's viewpoint, a VM is a group of user worlds. Three main types:

| Group | Role | Accounting |
|---|---|---|
| VMX (VM Executable) | Handles I/O for devices not critical to performance. Communicates with user interfaces, snapshot manager, remote console. | — |
| VMM (VM Monitor) | Virtualizes guest OS instructions. Manages memory mapping. Passes storage and network I/O to the kernel; passes other requests to VMX. | One VMM per vCPU. |
| MKS (Mouse Keyboard Screen) and SVGA | Render guest video. Handle guest user input. | Console work via the vSphere Client is charged to MKS, which is charged to the VM, not to a specific vCPU. |

- Example errors in these processes: https://kb.vmware.com/s/article/1019471

## Consequences for metrics
- Work charged at VM level (e.g. MKS, System) does not appear in per-vCPU metrics. See `vsphere/cpu/metrics/virtual-motherboard/used`.

## Metadata
```yaml
id: vsphere/foundations/kernel-worlds
retriever_guide: how-it-works
scope: vsphere
technology:
- cpu
pillar:
- performance
product:
- vsphere
object:
- VirtualMachine
- HostSystem
internal_derive: []
related:
- vsphere/foundations/vm-vs-guest-os
- vsphere/foundations/visibility-layers
- vsphere/cpu/metrics/comparisons/consumption-metrics
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Virtualization Impact > What, exactly, is a VM? > Kernel
corrections: []
review_notes: []
status: draft
```
