---
id: vsphere/glossary/terminology
retriever_guide: term-meaning
scope: vsphere
technology: [cpu, memory, storage, network, system]
pillar: [availability, performance, security, capacity, value]
product: [vsphere, vcf-operations]
internal_derive: []
related:
  - vsphere/glossary/logical-processor
  - foundations/terminology
  - foundations/naming-patterns
source:
  document: Author statements (2026-11-02); vSphere API type names; VCF Operations object types
  path: n/a
corrections: []
review_notes:
  - "Section 'Book terminology' is a placeholder. The author will provide the book's terminology."
  - "Section 'Core words' is drafted by Claude to prevent mixing dimensions. Author to correct."
  - "Section 'VCF Operations object types': names other than vSphere World are from Claude's own knowledge. Verify against current VCF Operations documentation."
status: draft
---

# Terminology

Single source of truth for terms, synonyms, and words to avoid.
Tag values in front matter must use the terms defined here.

## Book terminology
- Placeholder. To be provided by the author.

## Synonyms (same thing, several names)
| Preferred term | Also called | Note |
|---|---|---|
| ESXi | ESX, ESXi Host, HostSystem | HostSystem is the vSphere API object type. The 9.1 performance document uses "ESX". |

## Core words (do not mix these dimensions)
| Term | Meaning | Is not |
|---|---|---|
| Object type | A kind of managed object in vSphere or VCF Operations. It has a name per instance. Examples: VirtualMachine, HostSystem, Folder, VmwareDistributedVirtualSwitch. | A component inside an object (vCPU, vmnic). |
| Object | One named instance of an object type. Example: a VM called "db01". | A metric or a layer. |
| Instance (metric) | A sub-component a metric is reported for, inside one object. Examples: vCPU 0, vmnic1, vmhba0. Tag: `instance`. | An object type. |
| Layer | A level of the stack: Guest OS, VM, hypervisor, physical. | An object type. Guest OS is a layer, not a vSphere object type. |
| Vantage point | The layer or object a metric is observed from. Consumer (VM) vs provider (ESXi). | A tag value by itself. Expressed through `object` and `layer`. |
| Perspective (book) | One of three angles on metrics: technology, pillar of operations, product. | A layer or vantage point. |
| Technology | cpu, memory, storage, network, system. System = the box as a whole: OS, BIOS, or a whole device. | A product. |
| Pillar | availability, performance, security, capacity, value. | A technology. |
| Metric | A measured value with a name, unit and formula, for one object type. | A counter ID alone. |
| Counter | The raw performance counter as exposed by the source (for example vCenter `cpu.ready.summation`). A metric may be built from one or more counters. | The interpreted meaning. |
| Property | A configuration or inventory attribute of an object (for example number of vCPUs). Often used as context. | A measured value over time. |
| Metric class | contention, consumption, context. | A pillar. |

## Object types
### vSphere (API type names)
- VirtualMachine, HostSystem, ClusterComputeResource, ResourcePool, Datastore, StoragePod (datastore cluster), Datacenter, Folder, VmwareDistributedVirtualSwitch, DistributedVirtualPortgroup.

### VCF Operations
- vSphere World: the top-level object covering all vCenter Server instances.
- vCenter Server, Datacenter, Cluster Compute Resource, Host System, Virtual Machine, Datastore, Datastore Cluster, Resource Pool, vSphere Distributed Switch, Distributed Port Group.

## Words to avoid
| Avoid | Use instead | Why |
|---|---|---|
| need, want, wish (for a vCPU or VM) | demands runtime; the kernel decides how much it gets | A vCPU is a thread in the scheduler. It has no intent. |
| "uses only X% of what it needs" | "is charged X%" or "gets X% of the runtime it demands" | Same reason. |
| object (for vCPU, Guest OS) | instance (vCPU), layer (Guest OS) | vCPU and Guest OS are not vSphere object types. |
| kind (as a field name) | retriever_guide | "kind" does not say what the field is for. |
| architecture (for settings) | configuration | Architecture means the big picture, not individual settings. |
| interpretation (as a folder) | diagnosis | Interpretation is the purpose of every metric file. |

## Allowed tag values
Read by `scripts/validate.py`. Change values here, not in the script.

```yaml
retriever_guide: [how-it-works, metric-meaning, term-meaning, what-to-set, what-to-check]
scope: [vendor-neutral, vsphere]
technology: [cpu, memory, storage, network, system]
pillar: [availability, performance, security, capacity, value]
product: [vsphere, vsan, nsx, vcf-operations, windows, linux, kubernetes]
object: [VirtualMachine, HostSystem, ClusterComputeResource, ResourcePool, Datastore, StoragePod, Datacenter, Folder, VmwareDistributedVirtualSwitch, DistributedVirtualPortgroup, vSphereWorld, VCenterServer]
instance: [aggregate, per-vcpu, per-vmnic, per-vmhba, per-virtual-disk]
metric_class: [contention, consumption, context]
status: [draft, reviewed]
# Phrases rejected in body text of files whose technology includes cpu (scheduling language rule).
avoid_in_cpu_files: ['\bneeds?\b', '\bneeded\b', '\bwants?\b', '\bwish(es)?\b', 'uses only .* of what it needs']
# Phrases rejected in body text of every knowledge file.
avoid_everywhere: ['\[author-correction', '\[claude-knowledge\]']
```
