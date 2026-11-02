---
id: vsphere/foundations/overhead
retriever_guide: how-it-works
scope: vsphere
technology:
- cpu
- memory
- storage
pillar:
- capacity
- value
product:
- vsphere
object:
- VirtualMachine
- HostSystem
- ClusterComputeResource
internal_derive: []
related:
- vsphere/foundations/visibility-layers
- vsphere/memory/metrics/virtual-machine/usage
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Virtualization Impact > Overhead vs Not Overhead
corrections:
- '2026-11-02: The item that enables memory overcommit at ESXi level is the VM swap file (.vswp). Uploaded document names it ''VM memory snapshot''.'
- '2026-11-02: Four buffer types listed. Uploaded document says ''at least 3''.'
review_notes: []
status: draft
---

# Overhead vs not overhead

## Definition
- Overhead: mandatory (cannot be avoided) AND has negative impact (slower performance or more resource required).
- Not overhead: optional. You choose to use it. Typically brings a capability not possible without virtualization.
- Do not label every additional load as overhead.

## Overhead
| Item | Note |
|---|---|
| ESXi kernel | Delivers value, but not optional and not negligible. Reduces usable capacity. |
| IO processing by the hypervisor | Extra processing by the kernel. Can cause the IO blender effect. Does not reduce the resources allocated to the Guest OS. |
| VM CPU and memory overhead for the VM Monitor (VMM) | Small. Operationally negligible. |
| vSAN processes | ESXi memory consumed and CPU used by vSAN processes. |
| VM log files | The VM is a layer of its own; its logs provide necessary observability. |

## Not overhead
| Item | Note |
|---|---|
| VM snapshot | Optional. Delivers functionality not available in the Guest OS. |
| VM swap file (`.vswp`) | Enables memory overcommit at ESXi level. |
| vSphere HA spare capacity | Extra ESXi hosts provide availability protection. |
| vSAN Failures-to-Tolerate (FTT) policy | Availability protection, because vSAN does not use hardware-level redundancy. For transient VMs with a master template, FTT can be 0 (no protection). |

## Buffers
- Buffers are a separate category, in addition to overhead. Four types:

| Buffer | Effect |
|---|---|
| Capacity buffer | Reduces Usable Capacity. |
| Cost buffer | Reduces Sellable Capacity. Typically on top of the capacity buffer. |
| Disaster Recovery buffer | — |
| Security Attack buffer | Also called the clean room. |

## vMotion
- Not overhead to the VM. Can change VM metrics on the destination host.
- Unshared swapped page on the source can become a regular memory page on the destination → VM Memory Consumed increases.
- Source and destination ESXi versions can use different memory compression algorithms → a compressed page can become a regular page → consumption increases.

## Traps
- Counting snapshots, HA spare hosts or vSAN FTT as virtualization overhead → wrong. They are optional capabilities.
- Area C in `vsphere/foundations/visibility-layers` (work invisible to the guest) is not the same as overhead.
