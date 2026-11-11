# Terminology

Agent E2's vocabulary: one entry per concept, under its preferred name. An entry is the term in bold with its meaning, then up to three lines:
- Also called: other names for the same thing (vendor variants, screen labels, esxtop fields, words users write).
- Not to confuse with: the term it is mixed up with, and the difference. Written once, under the term users misuse.
- File: the knowledge file that holds the mechanism.

A metric with its own file is an entry only when it has another name or a confusable partner; its file holds the rest. Entries are grouped by area, alphabetical within each.

### Objects and layers

- **ESXi**: HostSystem is the vSphere API object type. The 9.1 performance document uses "ESX".
  - Also called: ESX, ESXi Host, HostSystem
- **Virtual motherboard**: What a VM is: vCPU, memory, virtual disks and vNICs that run a Guest OS. The Guest OS is not part of it.
  - Also called: VM
  - File: `vsphere/architecture/vm-vs-guest-os`
- **vSphere World**: VCF Operations object above all vCenter Server instances.

### CPU

- **All-Core Turbo**: Frequency when all cores of a socket are busy.
  - Also called: All Core Boost (AMD)
- **Base frequency**: Nominal frequency. vSphere uses it as total capacity.
  - Also called: Nominal frequency, base clock speed
- **CCD**: Core Complex Die. A group of cores sharing one L3 cache inside an AMD socket.
- **Co-stop**: vCPU state: held back because a sibling vCPU of the same VM is too far behind.
  - Also called: Co-Stop, CoStop
- **Contention (VCF Operations)**: Overlap + Co-stop + Ready + Other Wait (when below 1%). Before VCF Operations 8.18 (July 2024): mapped to CPU Latency.
  - File: `vsphere/technology/cpu/metrics/virtual-motherboard/contention`
- **Core Utilization**: 100% when 1 or 2 threads of a core run.
  - Not to confuse with Thread Utilization: Core Utilization counts a core as fully used when one of its two threads runs; Thread Utilization counts each thread (esxtop shows 200% for a core with both threads busy), so it shows the idle thread that can still take work.
  - File: `vsphere/technology/cpu/metrics/host/core-utilization`
- **CPPC**: Collaborative Processor Performance Control (ACPI 5.0+).
  - Also called: Intel HWP
- **CPU Throughput**: Productive cycles attributed to a thread or vCPU. Excludes the idle loop.
  - Also called: Usage (MHz), Used
- **CPU Utilization for Resources**: 17 legacy rescpu.* metrics. Avoid.
  - Also called: rescpu
- **Efficacy (CPU)**: Work per cycle from core architecture. Not accounted by any metric.
- **Efficiency (CPU)**: Hyper-Threading effect on cycles completed. Accounted as 1.25x per core, 0.625x per thread.
- **ESXi CPU Demand**: Sum over the VMs of the CPU they would use with no contention.
  - Not to confuse with ESXi CPU Usage: kernel work is in Usage only, so a host with no VMs shows Demand 0 and Usage above 0.
  - File: `vsphere/technology/cpu/metrics/host/demand`
- **ESXi CPU Imbalance**: Running threads / running cores.
  - Also called: Imbalance Score
- **ESXi CPU Usage**: Busy time that counts frequency (Turbo, power saving) and Hyper-Threading: a core with both threads busy is 100%.
  - Also called: Consumed CPU (%) (vSphere Client host list)
  - Not to confuse with Thread Utilization: Utilization is busy time per thread at static frequency; Usage moves with Turbo and power saving and counts per core.
  - File: `vsphere/technology/cpu/metrics/comparisons/host-consumption-metrics`
- **Frozen time**: Time a vCPU is de-scheduled. The Guest OS sees a time jump.
  - Also called: Steal Time (Linux, for Ready)
- **Max Limited**: Part of Ready caused by a CPU limit.
  - Also called: Limbo time
- **MKS, VMX, Helper**: VM worlds charged to VM-level Used: console, VM management and emulation, IO helpers.
- **Net Run**: VCF Operations metric: Run - Overlap.
- **NHCC**: Non-Halted Core Cycles. Hardware counter behind Used.
- **Other Wait**: Wait not caused by idle or swap: disk IO, network IO, vMotion, snapshots.
  - Also called: VM Wait
- **Overlap**: Time a running vCPU is interrupted by a kernel system service.
  - Also called: Stolen (some VMware documents)
- **Peak Core Usage**: VCF Operations: highest Usage among the cores of a host.
  - Also called: Peak CPU Core Usage
- **Physical CPU (esxtop)**: One hardware execution context: a thread with Hyper-Threading on, a core with it off.
  - Also called: Logical Processor (vSphere Client), PCPU
- **Readiness**: Ready expressed in %, normalized by vCPU count.
  - Also called: Ready (%)
- **Run Quality**: Cycles completed while running. Varies with frequency and Hyper-Threading. Used for performance.
- **Run Time**: How long a CPU or vCPU runs. Binary per moment. Used for capacity.
  - Also called: Run (VM), Utilization (ESXi)
- **Single-Core Turbo**: Highest frequency of one busy core.
  - Also called: Max Turbo Frequency (Intel)
- **SMT**: Simultaneous multithreading.
  - Also called: Hyper-Threading (Intel)
- **Thread Utilization**: ESXi Utilization (%) read per physical thread. Binary per moment.
  - Also called: Utilization (%)
  - File: `vsphere/technology/cpu/metrics/host/utilization`
- **Usage Disparity**: Spread of usage across the vCPUs of one VM.
  - Also called: vCPU imbalance, Imbalance vCPU Usage (avoid)
- **VM CPU Used**: Run scaled by frequency and Hyper-Threading, plus System, minus Overlap.
  - Also called: %USED (esxtop)
  - Not to confuse with VM CPU Run: Run is time only; Used moves with frequency and Hyper-Threading, so it can sit far above or below Run.
  - File: `vsphere/technology/cpu/troubleshooting/run-vs-used-gap`

### Memory

- **Active (memory)**: Sampled estimate of recently touched VM memory.
  - Also called: Touch (ESXi), Non Zero Active (VCF Operations)
  - File: `vsphere/technology/memory/metrics/virtual-motherboard/active`
- **Balloon Target**: Memory ESXi asks the balloon driver to reclaim.
- **Entitlement (memory)**: Granted + Overhead.
- **ESXi pages**: Pages ESXi manages on DIMM, host cache or tiered NVMe.
  - Also called: machine pages, machine memory
- **Granted**: VM pages with ESXi pages mapped. VM view.
- **Guest OS In Use**: Windows page class In Use (beside Modified, Cache, Free); Windows can compress part of it.
  - Also called: In Use (Windows)
  - Not to confuse with VM Memory Consumed: Consumed counts the ESXi pages the VM has touched and does not drop when Windows frees memory; the two have no mapping.
  - File: `vsphere/technology/memory/concepts/guest-os-vs-vm-memory`
- **Guest OS Needed Memory**: VCF Operations guest metric behind VM Memory Usage (%).
- **Page-fault latency**: VM memory Latency (%), esxtop %LAT_M. VCF Operations: VM Memory Contention.
  - Also called: Memory Latency
- **Swap Target**: Memory ESXi aims to reclaim by compression and swapping.
  - Also called: Compress-swap target
- **VM Memory Usage (%)**: vCenter: from Active. VCF Operations: Guest OS Needed Memory / VM memory, falling back to Active without Guest OS data.
  - Not to confuse with ESXi Memory Usage (%): ESXi and cluster Usage is Consumed, a capacity reading; VM Usage is not. Read as one metric, they have led customers to buy RAM they did not need.
  - File: `vsphere/technology/memory/metrics/virtual-motherboard/usage`
- **VM pages**: Pages in the VM address space. Vendor term kept for search.
  - Also called: guest physical pages, guest physical memory

### Storage

- **Disk (device)**: A physical disk or LUN presented to ESXi. The vSphere Client uses device and disk for the same thing; a LUN is the array's logical volume, which can span RAID groups.
  - Also called: device, LUN
  - Not to confuse with Virtual disk, datastore: the vSphere Client shows a VM's storage in 3 layers: virtual disk (the VM's own), datastore (the filesystem), disk (the device, shared by every VM on it). Each has its own counters; compare values only within one layer.
  - File: `vsphere/technology/storage/concepts/storage-layers`

### Performance, SLA and KPI

- **Actual Availability (%)**: Availability as it happened. Usually lower than Operational Availability.
- **Class of service**: Gold, Silver, Bronze: each with its own price, overcommit ratio, maximum VM size and availability SLA.
  - Also called: Tier
- **Crown jewels**: The critical business applications, strategic to the core business: few VMs, essential to revenue, profit or image. Each gets a KPI at the infrastructure layer.
  - Also called: Mission-critical applications
  - File: `sp5-framework/performance/business-application-kpi`
- **KAI**: Key availability indicator: the internal availability target, the availability counterpart of the KPI.
  - Also called: availability KPI, uptime KPI
  - File: `sp5-framework/performance/kpi-vs-sla`
- **KPI**: Key performance indicator: an internal baseline for performance only, the P in KPI. Performance monitoring and troubleshooting use the KPI only: no performance SLA, SLI or SLO. One 0-100% score per object: VM, Guest OS, ESXi and Cluster Performance. Availability has KAI; security has KSI.
  - Also called: Key Performance Indicator, performance SLA, SLI, SLO, service level (for performance)
  - Not to confuse with SLA: the KPI is for operations, covers performance, says how bad, is read daily, per object; the SLA is a business contract between two parties, on the consumer's object (VM, pod), read monthly. When a user cites an SLA, ask its metric, object, target and window.
  - File: `sp5-framework/performance/kpi-vs-sla`
- **KSI**: Key security indicator: the internal security and compliance target.
  - Also called: security KPI, compliance KPI
  - File: `sp5-framework/performance/kpi-vs-sla`
- **Noisy neighbour**: A consumer whose demand degrades others on shared capacity (villain and victims).
  - Also called: Resource management
  - File: `sp5-framework/performance/noisy-neighbour`
- **Operational Availability (%)**: Availability relative to the availability architecture.
- **Security SLA**: Preferred over compliance SLA, which is correct but narrower: security also covers activity, not only settings. The IT security industry has not defined it well.
  - Also called: Compliance SLA

### Capacity

- **Closed cluster**: A cluster that accepts no new VM and no VM upsize, decided from Cluster Consumption (%), Cluster Performance (%) and Cluster Risk (%).
  - Also called: Stop provisioning
  - File: `vsphere/object-types/cluster/decision-tree/can-cluster-take-more-vms`
- **Cluster Risk (%)**: How close the worst ESXi host of a cluster is to contention: a leading indicator, 0 no risk, 100 maximum risk.
  - Not to confuse with Time Remaining: Cluster Risk reads the running cluster now (short-term capacity: stop provisioning, no projection); Time Remaining is the long-term runway, days until the forecast crosses usable capacity (buy hardware).
  - File: `vsphere/object-types/cluster/models/cluster-risk`
- **Demand (capacity)**: Per VM, the higher of utilization and reservation.
  - Not to confuse with ESXi CPU Demand: ESXi CPU Demand is the runtime the VMs demand; capacity demand also counts reservations.
  - File: `sp5-framework/capacity/demand`
- **Guest OS sizing**: Sizing vCPU and memory from Guest OS counters (inside).
  - Also called: VM rightsizing (inside the guest)
  - Not to confuse with VM footprint: VM footprint sizes from vSphere counters (outside); two jobs, two formulas.
  - File: `sp5-framework/capacity/rightsizing`
- **Model**: How one pillar of one object is quantified into a number and a decision: capacity, availability, security model. Example: Cluster Consumption and Cluster Risk decide, with Cluster Performance, whether a cluster is closed.
  - Not to confuse with KPI: a KPI scores performance only; capacity and risk are scored by models, so Cluster Risk is a model, not a KPI.
  - File: `vsphere/object-types/cluster/models/cluster-consumption`
- **Usable capacity**: Total capacity minus HA, buffer and hypervisor overhead. Performance management is never measured against Usable Capacity numbers.

### Operations management

- **Compliance**: Settings measured against internal policy, industry benchmarks and regulation; binary.
  - Not to confuse with Security: security covers live threats and activity, and a security issue is present and urgent; a non-compliant setting is risk (future health) until it is exploited or exposed.
  - File: `sp5-framework/concepts/overview`
- **Decision tree**: A flow that answers one operational question (can it, should it, how much) and ends in a choice to act, with its reason. Folder `decision-tree/`.
  - Not to confuse with Health check: a decision tree answers one question, usually on one pillar; a health check covers every pillar of one object and may read a decision tree's result as one step.
  - File: `vsphere/object-types/cluster/decision-tree/can-cluster-take-more-vms`
- **Finding**: Result of troubleshooting or analysis from logs, events, metrics, tasks. Positive feeds insight; negative is an issue.
- **Framework**: How IT operations are managed: policy, pillars, process, people, platform. The SP5 framework; ITIL and COBIT are other frameworks.
  - File: `sp5-framework/concepts/overview`
- **Future health**: Risk: no problem yet; security exposure, compliance, configuration, capacity.
  - Also called: Risk
- **Green zone**: The change window: the agreed time when approved changes, deployments and patches may enter production. Downtime inside it is excluded from Operational Availability.
  - Also called: Change window, maintenance window, authorized execution window
  - File: `sp5-framework/concepts/sla-metrics`
- **Health check**: Check of one object type (VM, host, cluster), never a technology or a single pillar, in the order availability, performance, security, capacity, with configuration as the drill-down. The what; a superset of troubleshooting. A failed step opens a troubleshooting flow.
  - Also called: what to monitor, monitoring checklist, verification, daily check
  - File: `sp5-framework/concepts/health-check`
- **Insight**: A top-down finding from alerts, symptoms, context and supporting metrics. Proactive; no ticket, no automatic close.
  - Not to confuse with Alert: an alert is an urgent issue (red or orange), bottom up, on one object, with a ticket; yellow is not urgent, so it is an insight, read in the daily health check.
  - File: `sp5-framework/outputs/alerts-and-insights`
- **Issue**: A negative finding, identified by one or more symptoms.
- **Leading indicator, lagging indicator**: Leading: underlying metric read in insights. Lagging: customer-facing metric used in alerts.
- **Notification**: How VCF Operations pushes an insight or alert to a person: email, message, on screen at login.
- **Present health**: Real problems now: availability, performance, security incidents.
  - Also called: Health
  - File: `sp5-framework/concepts/health-risk-efficiency`
- **Prevention window**: Time between the operations team knowing of a problem (insight) and customers noticing it (alert).
- **Primary metric, secondary metric**: Primary: 0-100%, defines performance (the what). Secondary: explains the primary (the why).
- **Property**: An input set by configuration or capability (configured hosts, maximum VMs), not produced every interval.
  - Not to confuse with Metric: a metric is produced every interval, even when constant (a power state or a VM count is a metric); a property is set by configuration.
  - File: `sp5-framework/observability/input-types`
- **Symptom**: A test on one metric, property or event (VCF Operations). A symptom definition is reusable across alert definitions; a condition is the same test written inside one alert definition. Triggered alone, it is a minor, non-urgent issue, read in the daily health check; when its alert's set of symptoms holds, the issue has become urgent: an alert.
  - Also called: Condition
  - File: `sp5-framework/outputs/alerts-and-insights`
- **Triple See Method**: The SP5 Framework's observability method for VCF: read contention, consumption and context metrics as one set before concluding. Not based on the USE, RED or Golden Signals.
  - Also called: Triple See
  - File: `sp5-framework/observability/triple-see-method`
- **Troubleshooting**: The reactive process for an object that is down or slow: why, and the fix, in the order of checks of its pillar. A security breach gets a forensic investigation instead; compliance is drift detection.
  - Also called: diagnosis, diagnose, root cause analysis, triage
  - Not to confuse with Health check: the health check first finds whether there is a problem (the what); troubleshooting starts from a known one (complaint, alert, failed health check step) and asks why.
  - File: `sp5-framework/concepts/health-check`
- **Value (pillar)**: One of the five SP5 pillars. Keeps apart cost (what IT spends on infrastructure), price (what IT charges a tenant) and business value (what the investment returns). Formerly cost management.
  - Also called: Cost and price
  - File: `sp5-framework/concepts/overview`

## Metadata

```yaml
id: glossary
retriever_guide: term-meaning
scope: sp5-framework
technology: [cpu, memory, storage, network, system]
pillar: [availability, performance, compliance, capacity, value]
product: [vsphere, vcf-operations]
internal_derive: []
related:
  - sp5-framework/observability/naming-patterns
  - vsphere/architecture/resource-controls
source:
  document: Knowledge base; vSphere API type names; VCF Operations object types
  path: "n/a. Section 'Term distinctions' and the Physical CPU synonym from Private Cloud Management by Iwan Rahabok (https://isvara.io/download), The World of Metrics > Metrics Nuances > Complexity > Naming Complexity"
corrections: []
review_notes:
  - "To check: column 'Not to confuse with': each pair against the file in its File column."
  - "To check: the entries added 2026-11-11 to carry a pair (ESXi CPU Demand, ESXi CPU Usage, VM CPU Used, Guest OS In Use, VM Memory Usage (%), Disk (device), Cluster Risk (%), Compliance, Property)."
  - "To check: each term and its preferred name in section 'CPU', from Run Quality onward."
status: draft
```
