# Terminology

What Agent E2 needs to read the user's words and answer in one consistent vocabulary: synonyms, defined terms and confusable pairs. Writing rules (dimensions, words to avoid) are in `project/vocabulary.md`.

## Synonyms (same thing, several names)
| Preferred term | Also called | Note |
|---|---|---|
| ESXi | ESX, ESXi Host, HostSystem | HostSystem is the vSphere API object type. The 9.1 performance document uses "ESX". |
| Physical CPU (esxtop) | Logical Processor (vSphere Client), PCPU | One hardware execution context: a thread with Hyper-Threading on, a core with it off. |
| VM pages | guest physical pages, guest physical memory | Pages in the VM address space. Vendor term kept for search. |
| ESXi pages | machine pages, machine memory | Pages ESXi manages on DIMM, host cache or tiered NVMe. |
| Guest OS sizing | VM rightsizing (inside the guest) | Sized from Guest OS counters. The external view is VM footprint. |
| Usage Disparity | vCPU imbalance | Spread of usage across the vCPUs of one VM. |

## Defined terms
| Term | Meaning | Also called |
|---|---|---|
| Virtual motherboard | What a VM is: vCPU, memory, virtual disks and vNICs that run a Guest OS. The Guest OS is not part of it. | VM |
| KPI | Key performance indicator; performance only. One metric for the performance of one object. `operations-management/performance/kpi-vs-sla` | - |
| KAI, KCI | Key availability indicator, key compliance indicator. Not called KPI. | - |
| SLI | SLA leading indicator: pass or fail every 5 minutes; the SLA is its mean over the calendar month. Not service level indicator. | - |
| Security SLA | Preferred over compliance SLA, which is correct but narrower: security also covers activity, not only settings. | Compliance SLA |
| Noisy neighbour | A consumer whose demand degrades others on shared capacity (villain and victims). `vsphere/foundations/noisy-neighbour` | Resource management |
| Class of service | Gold, Silver, Bronze: each with its own overcommit ratio, maximum VM size and Performance SLA. | Tier |
| Usable capacity | Total capacity minus HA, buffer and hypervisor overhead. A capacity term only. | - |
| Closed cluster | A cluster that accepts no new VM and no VM upsize, decided from Capacity Remaining, Performance (%) and Risk (%). `operations-management/capacity/diagnosis/can-cluster-take-more-vms` | Stop provisioning |
| vSphere World | VCF Operations object above all vCenter Server instances. | - |
| Run Time | How long a CPU or vCPU runs. Binary per moment. Used for capacity. | Run (VM), Utilization (ESXi) |
| Run Quality | Cycles completed while running. Varies with frequency and Hyper-Threading. Used for performance. | - |
| CPU Throughput | Productive cycles attributed to a thread or vCPU. Excludes the idle loop. | Usage (MHz), Used |
| Efficiency (CPU) | Hyper-Threading effect on cycles completed. Accounted as 1.25x per core, 0.625x per thread. | - |
| Efficacy (CPU) | Work per cycle from core architecture. Not accounted by any metric. | - |
| Base frequency | Nominal frequency. vSphere uses it as total capacity. | Nominal frequency, base clock speed |
| All-Core Turbo | Frequency when all cores of a socket are busy. | All Core Boost (AMD) |
| Single-Core Turbo | Highest frequency of one busy core. | Max Turbo Frequency (Intel) |
| Frozen time | Time a vCPU is de-scheduled. The Guest OS sees a time jump. | Steal Time (Linux, for Ready) |
| Co-stop | vCPU state: held back because a sibling vCPU of the same VM is too far behind. | Co-Stop, CoStop |
| SMT | Simultaneous multithreading. | Hyper-Threading (Intel) |
| CCD | Core Complex Die. A group of cores sharing one L3 cache inside an AMD socket. | - |
| CPPC | Collaborative Processor Performance Control (ACPI 5.0+). | Intel HWP |
| Readiness | Ready expressed in %, normalized by vCPU count. | Ready (%) |
| Max Limited | Part of Ready caused by a CPU limit. | Limbo time |
| Overlap | Time a running vCPU is interrupted by a kernel system service. | Stolen (some VMware documents) |
| Other Wait | Wait not caused by idle or swap: disk IO, network IO, vMotion, snapshots. | VM Wait |
| Net Run | VCF Operations metric: Run - Overlap. | - |
| Contention (VCF Operations) | Overlap + Co-stop + Ready + Other Wait. Before July 2024: mapped to CPU Latency. | - |
| Usage Disparity | Spread of usage across the vCPUs of one VM. | Imbalance vCPU Usage (avoid) |
| MKS, VMX, Helper | VM worlds charged to VM-level Used: console, VM management and emulation, IO helpers. | - |
| Thread Utilization | ESXi Utilization (%) read per physical thread. Binary per moment. | Utilization (%) |
| Core Utilization | 100% when 1 or 2 threads of a core run. | - |
| NHCC | Non-Halted Core Cycles. Hardware counter behind Used. | - |
| Peak Core Usage | VCF Operations: highest Usage among the cores of a host. | Peak CPU Core Usage |
| ESXi CPU Imbalance | Running threads / running cores. | Imbalance Score |
| Consumed CPU (%) | Host list column in vSphere Client. Maps to Usage (%). | - |
| CPU Utilization for Resources | 17 legacy rescpu.* metrics. Avoid. | rescpu |
| VM pages | Pages in the VM address space. Vendor term: guest physical pages. | - |
| ESXi pages | Pages ESXi manages on DIMM, host cache or tiered NVMe. Vendor term: machine pages. | - |
| Page-fault latency | VM memory Latency (%), esxtop %LAT_M. VCF Operations: VM Memory Contention. | Memory Latency |
| Granted | VM pages with ESXi pages mapped. VM view. | - |
| Entitlement (memory) | Granted + Overhead. | - |
| Swap Target | Memory ESXi aims to reclaim by compression and swapping. | Compress-swap target |
| Balloon Target | Memory ESXi asks the balloon driver to reclaim. | - |
| Active (memory) | Sampled estimate of recently touched VM memory. | Touch (ESXi), Non Zero Active (VCF Operations) |
| Guest OS Needed Memory | VCF Operations guest metric behind VM Memory Usage (%). | - |
| Symptom | A minor, non-urgent issue, read in the daily health check. A symptom that persists becomes an alert. `operations-management/performance/alerts-and-insights` | - |
| Insight | A top-down finding from alerts, symptoms, context and supporting metrics. Proactive; no ticket, no automatic close. | - |
| Prevention window | Time between the operations team knowing of a problem (insight) and customers noticing it (alert). | - |
| Leading indicator, lagging indicator | Leading: underlying metric read in insights. Lagging: customer-facing metric used in alerts. | - |
| Operational Availability (%) | Availability relative to the availability architecture. | - |
| Actual Availability (%) | Availability as it happened. Usually lower than Operational Availability. | - |
| Crown jewels | Mission-critical business applications: few VMs, essential to revenue, profit or image. | Mission-critical applications |
| Slow time | Time a VM spends above the Performance SLA threshold; the performance counterpart of downtime. `operations-management/performance/sla-metrics` | - |
| Finding | Result of a diagnosis or analysis from logs, events, metrics, tasks. Positive feeds insight; negative is an issue. | - |
| Issue | A negative finding, identified by one or more symptoms. | - |
| Notification | How VCF Operations pushes an insight or alert to a person: email, message, on screen at login. | - |
| Present health | Real problems now: availability, performance, security incidents. `operations-management/performance/health-risk-efficiency` | Health |
| Future health | Risk: no problem yet; security exposure, compliance, configuration, capacity. | Risk |
| Primary metric, secondary metric | Primary: 0-100%, defines performance (the what). Secondary: explains the primary (the why). | - |

## Confusable pairs
Pairs that public text mixes up. Each row points to the file that holds the mechanism.

| Pair | Difference | File |
|---|---|---|
| ESXi CPU Usage vs Utilization | Usage counts frequency and Hyper-Threading (both threads busy = core 100%); Utilization is static-frequency busy time, per thread | `vsphere/technology/cpu/metrics/host/utilization` |
| ESXi CPU Demand vs Usage | Demand is the sum over the VMs of what they would use with no contention; kernel work is in Usage only, so a host with no VMs shows Demand 0 | `vsphere/technology/cpu/metrics/host/demand` |
| VM CPU Ready vs Latency | Ready is time waiting for a physical CPU; Latency also rises with lower frequency, with no wait | `vsphere/technology/cpu/metrics/virtual-motherboard/latency` |
| VM CPU Run vs Used | Run is time only; Used is scaled by frequency and Hyper-Threading, plus System, minus Overlap | `vsphere/technology/cpu/diagnosis/run-vs-used-gap` |
| VM Memory Consumed vs Active | Consumed is the ESXi pages of the VM, kept once touched; Active is an estimate of pages touched recently, with no operational use | `vsphere/technology/memory/metrics/virtual-motherboard/active` |
| VM Memory Ballooned vs Swapped | Ballooned is reclaimed through the Guest OS, past tense; Swapped is paged out by ESXi at random, as it cannot see guest free memory | `vsphere/technology/memory/metrics/virtual-motherboard/swapped` |
| Compression ZIP/s vs UNZIP/s | ZIP/s is a capacity signal of the host; UNZIP/s means the VM waits | `vsphere/tools/esxtop/memory` |
| Reservation vs usage | Admission control checks reservations; usage plays no part | `vsphere/object-types/cluster/concepts/admission-control-and-cluster-state` |
| VM vs Guest OS | The VM is a virtual motherboard; the Guest OS is a separate layer with its own counters | `vsphere/foundations/vm-vs-guest-os` |
| Storage vs disk | Storage is the whole IO path; disk is one layer of it, and each vCenter counter group has its own scope | `vsphere/technology/storage/concepts/storage-layers` |
| Device vs disk vs LUN | Device is generic; disk is physical; LUN is a logical volume on the array | `vsphere/technology/storage/concepts/storage-layers` |
| vCenter vs VCF Operations | vCenter administers; VCF Operations monitors and plans, and every metric it shows derives from a source | `vcf-operations/concepts/vcf-operations-role` |
| Alert vs insight | Alert: urgent, bottom up, one object above a threshold, a ticket. Insight: proactive, top down, from many metrics and context | `operations-management/performance/alerts-and-insights` |
| Metric vs property | Metric: produced every interval, even when constant (power state, VM count). Property: set by configuration (configured hosts, maximum VMs) | `foundations/input-types` |
| Allocation vs reservation | Allocation is a maximum and can be overcommitted; reservation is a guarantee and cannot | `vsphere/foundations/resource-controls` |
| Monitoring vs troubleshooting | Monitoring: what, proactive, one primary metric, no logs. Troubleshooting: why, reactive, many metrics and logs | `operations-management/performance/monitoring-vs-troubleshooting` |
| Inventory vs configuration | Inventory counts what is where and its movement; configuration is the settings and their drift. Configuration maximums are inventory maximums | `operations-management/performance/pillars-of-operations` |
| Security vs compliance | Security tracks attacks and malicious activity; compliance checks settings against a benchmark and is binary | `operations-management/performance/pillars-of-operations` |
| Short-term vs long-term capacity | Short term: now, stop provisioning, no projection. Long term: future, buy hardware, projection mandatory | `operations-management/performance/pillars-of-operations` |
| Demand (capacity) vs ESXi CPU Demand | Capacity demand is the higher of utilization and reservation, per powered-on VM; ESXi CPU Demand is a counter of runtime demanded | `operations-management/capacity/capacity-dimensions` |
| Idle vs oversized vs unused VM | Idle: below an absolute MHz every day; oversized: relative to its size; unused: busy but of no business value | `operations-management/capacity/reclamation` |


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
  - "2026-11-07: Defined terms Slow time to Primary metric and the pairs Monitoring vs troubleshooting, Inventory vs configuration, Security vs compliance, Short-term vs long-term capacity added from Part 1, Your Private Cloud (Service Level Agreement to SP5 Framework: Process). Proposals; author to confirm. Present and future health grouping: Q102."
  - "2026-11-07: Defined terms Symptom to Crown jewels and the pairs Alert vs insight, Metric vs property added from Part 1, Your Private Cloud (Overview, Purpose-Driven Architecture). Proposals; author to confirm."
  - "2026-11-07 (author decision): knowledge/ is for Agent E2 only. Kept here: synonyms, defined terms, confusable pairs. Moved out: Core words and Words to avoid to project/vocabulary.md; Term distinctions to vsphere/foundations/resource-controls and vsphere/technology/storage/concepts/storage-layers (the OpenTelemetry note was already in foundations/naming-patterns); Object types to catalog/objects.yaml. 'Book terminology' and 'Proposed terms' merged as 'Defined terms'."
  - "Section 'Confusable pairs': drafted by Claude 2026-11-06 from the files in its File column, as block 3 of the agent up-front knowledge (harness/AGENT.md). Author to confirm (Q059)."
  - "Section 'Defined terms': rows from Run Time onward were added 2026-11-02 from the book (CPU and Memory chapters) as proposals. Author to confirm each term and its preferred name. Class of service 'also called Tier' and the new Synonyms rows from Words to avoid are Claude's."
  - "Moved 2026-11-02 from knowledge/vsphere/glossary/ to knowledge/glossary/: applies to all products. Scope set to vendor-neutral."
  - "2026-11-04: merged glossary and glossary into this file (author decision); allowed tag values moved to tools/tags.yaml."
status: draft
```
