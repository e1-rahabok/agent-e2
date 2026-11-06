# Terminology

Single source of truth for terms, synonyms, distinctions and words to avoid, across all products.
Allowed tag values (machine settings for the linter) are in `project/tools/tags.yaml`.

## Book terminology
- From Part 1, Performance Management. Proposals until the author confirms.
- KPI: key performance indicator; performance only. One metric that quantifies the performance of a logical entity. See `operations-management/performance/kpi-vs-sla`.
- KAI: key availability indicator. KCI: key compliance indicator. Not called KPI.
- SLI: service level indicator; the 5-minute tracking value behind an SLA. The SLA is its monthly result.
- Noisy neighbour: a consumer whose demand degrades other consumers on shared capacity (villain and victims). Used instead of resource management. See `vsphere/foundations/noisy-neighbour`.
- Class of service: Gold, Silver, Bronze; each with its own overcommit ratio, maximum VM size and performance threshold.
- Usable capacity: total capacity minus HA, buffer and hypervisor overhead. A capacity term only; there is no usable performance.

## Synonyms (same thing, several names)
| Preferred term | Also called | Note |
|---|---|---|
| ESXi | ESX, ESXi Host, HostSystem | HostSystem is the vSphere API object type. The 9.1 performance document uses "ESX". |
| Physical CPU (esxtop) | Logical Processor (vSphere Client), PCPU | One hardware execution context: a thread with Hyper-Threading on, a core with it off. The author prefers the pair virtual vs physical; "logical" is confusing. |

## Core words (do not mix these dimensions)
- **Object type**
  - Meaning: A kind of managed object in vSphere or VCF Operations. It has a name per instance. Examples: VirtualMachine, HostSystem, Folder, VmwareDistributedVirtualSwitch.
  - Is not: A component inside an object (vCPU, vmnic).
- **Object**
  - Meaning: One named instance of an object type. Example: a VM called "db01".
  - Is not: A metric or a layer.
- **Instance (metric)**
  - Meaning: A sub-component a metric is reported for, inside one object. Examples: vCPU 0, vmnic1, vmhba0. Tag: `instance`.
  - Is not: An object type.
- **Layer**
  - Meaning: A level of the stack: Guest OS, VM, hypervisor, physical.
  - Is not: An object type. Guest OS is a layer, not a vSphere object type.
- **Virtual motherboard**
  - Meaning: What a VM is: a virtual circuit board (vCPU, memory, virtual disks, vNICs) that runs a Guest OS. Folder name for VM metrics: `virtual-motherboard`. Tag: `layer: virtual-motherboard`, `object: VirtualMachine`.
  - Is not: A complete machine. The Guest OS is not part of it: Guest OS knowledge is a separate layer and lives in `knowledge/guest-os/` (`scope: guest-os`, `layer: guest-os`). Author's book.
- **Vantage point**
  - Meaning: The layer or object a metric is observed from. Consumer (VM) vs provider (ESXi).
  - Is not: A tag value by itself. Expressed through `object` and `layer`.
- **Perspective (book)**
  - Meaning: One of three angles on metrics: technology, pillar of operations, product.
  - Is not: A layer or vantage point.
- **Technology**
  - Meaning: cpu, gpu, memory, storage, network, system. System = the box as a whole: OS, BIOS, or a whole device.
  - Is not: A product.
- **Storage**
  - Meaning: The whole IO path from the Guest OS to the array: virtual disk, vSCSI, datastore, storage adapter (vmhba), path, device (LUN), array, vSAN. Folder and tag: `storage`.
  - Is not: Disk. A disk is one layer of storage. Datastores, adapters, paths and vSAN are storage but not disks. vCenter keeps separate counter groups for each layer (`virtualDisk`, `disk`, `datastore`, `storageAdapter`, `storagePath`): the same label (latency, IOPS) means a different scope in each group. See `vsphere/technology/storage/concepts/storage-layers`.
- **Disk**
  - Meaning: One layer of storage. In vCenter, the `disk` counter group reports the device (LUN) as seen by ESXi, or the virtual disk as seen by the VM.
  - Is not: The storage technology as a whole.
- **vCenter**
  - Meaning: The administrative tool of vSphere: create VMs, configure switches, set reservations and limits. It keeps performance charts with short history.
  - Is not: The operations tool. Capacity planning and performance troubleshooting are done in VCF Operations, not in vCenter. Admins often use the two names interchangeably; the knowledge base does not.
- **VCF Operations**
  - Meaning: Monitoring and operations management software. A thin layer above the source systems (vSphere, vSAN, NSX, Windows, Linux, VKS): every metric it shows is derived, passed through or computed from a source. See `vcf-operations/concepts/vcf-operations-role`.
  - Is not: The source of a metric's meaning. A passed-through metric means what it means at its source object.
- **Pillar**
  - Meaning: availability, performance, security, capacity, value.
  - Is not: A technology.
- **Metric**
  - Meaning: A measured value with a name, unit and formula, for one object type.
  - Is not: A counter ID alone.
- **Counter**
  - Meaning: The raw performance counter as exposed by the source (for example vCenter `cpu.ready.summation`). A metric may be built from one or more counters.
  - Is not: The interpreted meaning.
- **Property**
  - Meaning: A configuration or inventory attribute of an object (for example number of vCPUs). Often used as context.
  - Is not: A measured value over time.
- **Metric class**
  - Meaning: contention, consumption, context.
  - Is not: A pillar.
- **Trap**
  - Meaning: A wrong conclusion drawn from a true observation: the number is right, the reading is wrong. Written in each file's `## Traps` section as "wrong conclusion" → correct reading. Types and format: `KNOWLEDGE-ENGINEERING.md`, section Traps and Level 400.
  - Is not: A wrong number or a data error.
- **Level 400**
  - Meaning: Knowledge that explains the mechanism behind a metric, predicts where its reading misleads (the trap), and says what to check instead.
  - Is not: Level 300: using a metric and a common threshold at face value.
- **Thread (physical)**
  - Meaning: Hardware thread of a CPU core. A provider.
  - Is not: A software thread.
- **Thread (software)**
  - Meaning: Thread in an OS (VMkernel, Windows, Linux). A consumer.
  - Is not: A physical thread.

## Term distinctions
### Allocation vs Reservation
- Allocation and reservation are two different concepts.
- Allocation: what is given to a consumer. Not guaranteed. It is a maximum: utilization cannot exceed it.
- Reservation: a guarantee. It is a minimum.
- Actual utilization can be below the reservation. It cannot exceed the allocation.
```text
utilization <= allocation
reservation is guaranteed; utilization may be < reservation
```
- Allocation can be overcommitted, because it is not a guarantee.
- Reservation cannot be overcommitted, because it is a guarantee.
- pattern when mixed: mixing-terminology. Invalid metric names:
  - "Allocation Reservation": meaningless.
  - "Maximum Reservation": means Allocation.
  - "Minimum Allocation": means Reservation.

### Device vs Disk vs LUN
- These three words are often used interchangeably. They are not identical.
- Device: generic. Not necessarily storage. Can be a network device or a security device.
- Disk: physical. Typically part of a disk group (RAID).
- LUN: a logical volume created by a storage array. Can span multiple RAID groups. "Logical volume" is the more accurate name; "LUN" is the common name.
- ESXi mounts a LUN and formats it with the VMFS filesystem.

### Usage vs Utilization (OpenTelemetry convention)
- Usage: amount used out of a known total.
- Utilization: fraction of usage out of its limit.
- vSphere does not follow this convention. See `foundations/naming-patterns`.

## Confusable pairs
Pairs that public text mixes up. Each row points to the file that holds the mechanism.

| Pair | Difference | File |
|---|---|---|
| ESXi CPU Usage vs Utilization | Usage counts frequency and Hyper-Threading (both threads busy = core 100%); Utilization is static-frequency busy time, per thread | `vsphere/technology/cpu/metrics/host/utilization` |
| ESXi CPU Demand vs Usage | Demand is the sum over the VMs of what they would use with no contention; an internal scheduler metric | `vsphere/technology/cpu/metrics/host/demand` |
| VM CPU Ready vs Latency | Ready is time waiting for a physical CPU; Latency also rises with lower frequency, with no wait | `vsphere/technology/cpu/metrics/virtual-motherboard/latency` |
| VM CPU Run vs Used | Run is time only; Used is scaled by frequency and Hyper-Threading, plus System, minus Overlap | `vsphere/technology/cpu/diagnosis/run-vs-used-gap` |
| VM Memory Consumed vs Active | Consumed is the ESXi pages of the VM, kept once touched; Active is an estimate of pages touched recently, with no operational use | `vsphere/technology/memory/metrics/virtual-motherboard/active` |
| VM Memory Ballooned vs Swapped | Ballooned is reclaimed through the Guest OS, past tense; Swapped is paged out by ESXi at random, as it cannot see guest free memory | `vsphere/technology/memory/metrics/virtual-motherboard/swapped` |
| Compression ZIP/s vs UNZIP/s | ZIP/s is a capacity signal of the host; UNZIP/s means the VM waits | `vsphere/tools/esxtop/memory` |
| Reservation vs usage | Admission control checks reservations; usage plays no part | `vsphere/object-types/cluster/concepts/admission-control-and-cluster-state` |

## Object types
### vSphere (API type names)
- VirtualMachine, HostSystem, ClusterComputeResource, ResourcePool, Datastore, StoragePod (datastore cluster), Datacenter, Folder, VmwareDistributedVirtualSwitch, DistributedVirtualPortgroup.

### VCF Operations
- vSphere World: the top-level object covering all vCenter Server instances.
- vCenter Server, Datacenter, Cluster Compute Resource, Host System, Virtual Machine, Datastore, Datastore Cluster, Resource Pool, vSphere Distributed Switch, Distributed Port Group.

## Proposed terms (author to confirm)
| Term | Meaning | Also called | Source |
|---|---|---|---|
| Run Time | How long a CPU or vCPU runs. Binary per moment. Used for capacity. | Run (VM), Utilization (ESXi) | Book, CPU > Architecture > 2 Metrics Not 1 |
| Run Quality | Cycles completed while running. Varies with frequency and Hyper-Threading. Used for performance. | - | Book, same section |
| CPU Throughput | Productive cycles attributed to a thread or vCPU. Excludes the idle loop. | Usage (MHz), Used | Book, CPU > Architecture > CPU Throughput |
| Efficiency (CPU) | Hyper-Threading effect on cycles completed. Accounted as 1.25x per core, 0.625x per thread. | - | Book, Frequency \| Efficiency \| Efficacy |
| Efficacy (CPU) | Work per cycle from core architecture. Not accounted by any metric. | - | Book, same section |
| Base frequency | Nominal frequency. vSphere uses it as total capacity. | Nominal frequency, base clock speed | Book, CPU Frequency |
| All-Core Turbo | Frequency when all cores of a socket are busy. | All Core Boost (AMD) | Book, CPU Frequency |
| Single-Core Turbo | Highest frequency of one busy core. | Max Turbo Frequency (Intel) | Book, CPU Frequency |
| Frozen time | Time a vCPU is de-scheduled. The Guest OS sees a time jump. | Steal Time (Linux, for Ready) | Book, Guest OS vs VM |
| Co-stop | vCPU state: held back because a sibling vCPU of the same VM is too far behind. | Co-Stop, CoStop | Book, State of a VM vCPU |
| SMT | Simultaneous multithreading. | Hyper-Threading (Intel) | Book, CPU Efficiency |
| CCD | Core Complex Die. A group of cores sharing one L3 cache inside an AMD socket. | - | Book, System on a Chip |
| CPPC | Collaborative Processor Performance Control (ACPI 5.0+). | Intel HWP | Book, ESXi Level |
| Readiness | Ready expressed in %, normalized by vCPU count. | Ready (%) | Book, CPU > VM > Ready \| Readiness |
| Max Limited | Part of Ready caused by a CPU limit. | Limbo time | Book, CPU > VM > Ready |
| Overlap | Time a running vCPU is interrupted by a kernel system service. | Stolen (some VMware documents) | Book, CPU > VM > Overlap |
| Other Wait | Wait not caused by idle or swap: disk IO, network IO, vMotion, snapshots. | VM Wait | Book, CPU > VM > Other Wait |
| Net Run | VCF Operations metric: Run - Overlap. | - | Book, CPU > VM > Run \| Net Run |
| Contention (VCF Operations) | Overlap + Co-stop + Ready + Other Wait. Before July 2024: mapped to CPU Latency. | - | Book, CPU > VM > Contention |
| Usage Disparity | Spread of usage across the vCPUs of one VM. | Imbalance vCPU Usage (avoid) | Book, CPU > VM > CPU Usage Disparity |
| MKS, VMX, Helper | VM worlds charged to VM-level Used: console, VM management and emulation, IO helpers. | - | Book, CPU > VM > Used |
| Thread Utilization | ESXi Utilization (%) read per physical thread. Binary per moment. | Utilization (%) | Book, CPU > ESXi > High Load Example |
| Core Utilization | 100% when 1 or 2 threads of a core run. | - | Book, CPU > ESXi > Thread Utilization |
| NHCC | Non-Halted Core Cycles. Hardware counter behind Used. | - | Book, CPU > ESXi > Used \| Usage |
| Peak Core Usage | VCF Operations: highest Usage among the cores of a host. | Peak CPU Core Usage | Book, CPU > ESXi > Peak Core CPU Usage |
| ESXi CPU Imbalance | Running threads / running cores. | Imbalance Score | Book, CPU > ESXi > Imbalance |
| Consumed CPU (%) | Host list column in vSphere Client. Maps to Usage (%). | - | Book, CPU > ESXi > Consumed |
| CPU Utilization for Resources | 17 legacy rescpu.* metrics. Avoid. | rescpu | Book, CPU > ESXi > Metrics to Avoid |
| VM pages | Pages in the VM address space. Vendor term: guest physical pages. | - | Book, Memory > Architecture > Relationship |
| ESXi pages | Pages ESXi manages on DIMM, host cache or tiered NVMe. Vendor term: machine pages. | - | Book, Memory > Architecture > Relationship |
| Page-fault latency | VM memory Latency (%), esxtop %LAT_M. VCF Operations: VM Memory Contention. | Memory Latency | Book, Memory > VM > Latency |
| Granted | VM pages with ESXi pages mapped. VM view. | - | Book, Memory > VM > Granted |
| Entitlement (memory) | Granted + Overhead. | - | Book, Memory > VM > Consumption Metrics |
| Swap Target | Memory ESXi aims to reclaim by compression and swapping. | Compress-swap target | Book, Memory > VM > Transition |
| Balloon Target | Memory ESXi asks the balloon driver to reclaim. | - | Book, Memory > VM > Balloon |
| Active (memory) | Sampled estimate of recently touched VM memory. | Touch (ESXi), Non Zero Active (VCF Operations) | Book, Memory > VM > Active |
| Guest OS Needed Memory | VCF Operations guest metric behind VM Memory Usage (%). | - | Book, Memory > VM > Usage (%) |

## Words to avoid
| Avoid | Use instead | Why |
|---|---|---|
| VM rightsizing | Guest OS sizing (internal, Guest OS counters) or VM footprint (external, vSphere counters) | Two different jobs with two formulas. Author's other book, VM Footprint and Guest OS Sizing. |
| VM metric (for a Guest OS counter such as Run Queue, Disk Queue, Processor Time) | Guest OS metric | The VM is a virtual motherboard; the Guest OS is a separate layer. Author correction, 2026-11-03. |
| virtual machine, thought of as a complete machine | virtual motherboard (VM) | A VM has no OS of its own; Guest OS and VM are not interchangeable. Author's book. |
| need, want, wish (for a vCPU or VM) | demands runtime; the kernel decides how much it gets | A vCPU is a thread in the scheduler. It has no intent. |
| "uses only X% of what it needs" | "is charged X%" or "gets X% of the runtime it demands" | Same reason. |
| object (for vCPU, Guest OS) | instance (vCPU), layer (Guest OS) | vCPU and Guest OS are not vSphere object types. |
| kind (as a field name) | retriever_guide | "kind" does not say what the field is for. |
| Utilization (ESXi CPU, when threads are meant) | Thread Utilization | Plain "Utilization" is easily confused with Core Utilization. Author correction, Q008. |
| architecture (for settings) | configuration | Architecture means the big picture, not individual settings. |
| interpretation (as a folder) | diagnosis | Interpretation is the purpose of every metric file. |
| Imbalance (for vCPU usage) | Usage Disparity | Imbalance implies the vCPUs should be balanced. |
| guest physical memory, guest physical page, machine page, machine memory | VM pages, ESXi pages | Only ESXi manages physical memory. Author: the term is illogical. Keep the vendor term once in parentheses for retrieval. |


## Metadata
```yaml
id: glossary
retriever_guide: term-meaning
scope: vendor-neutral
technology: [cpu, memory, storage, network, system]
pillar: [availability, performance, security, capacity, value]
product: [vsphere, vcf-operations]
internal_derive: []
related:
  - foundations/naming-patterns
  - vsphere/foundations/resource-controls
source:
  document: Author statements (2026-11-02); vSphere API type names; VCF Operations object types
  path: "n/a. Section 'Term distinctions' and the Physical CPU synonym from PART 3 - Counters.docx, The World of Metrics > Metrics Nuances > Complexity > Naming Complexity"
corrections: []
review_notes:
  - "Section 'Book terminology' is a placeholder. The author will provide the book's terminology."
  - "Section 'Core words' is drafted by Claude to prevent mixing dimensions. Author to correct."
  - "Section 'Confusable pairs': drafted by Claude 2026-11-06 from the files in its File column, as block 3 of the agent up-front knowledge (harness/AGENT.md). Author to confirm (Q059)."
  - "Section 'VCF Operations object types': names other than vSphere World are from Claude's own knowledge. Verify against current VCF Operations documentation."
  - "Section 'Proposed terms': added 2026-11-02 from the book, CPU > Architecture. Not yet in use as tag values. Author to confirm each term and its preferred name."
  - "Moved 2026-11-02 from knowledge/vsphere/glossary/ to knowledge/glossary/: applies to all products. Scope set to vendor-neutral."
  - "2026-11-04: merged glossary and glossary into this file (author decision); allowed tag values moved to tools/tags.yaml."
status: draft
```
