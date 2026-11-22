# Terminology

Agent E2's vocabulary: one entry per concept, with its other names, the term it is confused with, and the file that holds the mechanism.

### Objects and layers

- **ESXi**: HostSystem is the vSphere API object type. The 9.1 performance document uses "ESX".
  - Also called: ESX, ESXi Host, HostSystem
- **Virtual motherboard**: What a VM is: vCPU, memory, virtual disks and vNICs that run a Guest OS. The Guest OS is not part of it.
  - Also called: VM
  - File: [`vsphere/architecture/vm-vs-guest-os`](vsphere/architecture/vm-vs-guest-os.md)
- **vSphere World**: VCF Operations object above all vCenter Server instances.

### CPU

- **All-Core Turbo**: Frequency when all cores of a socket are busy.
  - Also called: All Core Boost (AMD)
- **Base frequency**: Nominal frequency: the clock that Total Capacity (GHz) counts.
  - Also called: Nominal frequency, base clock speed
- **CCD**: Core Complex Die: a die of cores inside an AMD socket. On most generations one CCD is one L3 domain; on Zen 4c a CCD holds two 8-core CCX, each its own L3 domain.
- **Co-stop**: vCPU state: held back because a sibling vCPU of the same VM is too far behind.
  - Also called: Co-Stop, CoStop
- **Contention (VCF Operations)**: Overlap + Co-stop + Ready + Other Wait (when below 1%). Before Aria Operations 8.18 (July 2024): mapped to CPU Latency.
  - File: [`vsphere/technology/cpu/metrics/virtual-motherboard/contention`](vsphere/technology/cpu/metrics/virtual-motherboard/contention.md)
- **Core Utilization**: 100% when 1 or 2 threads of a core run.
  - Not to confuse with Thread Utilization: ESXi Core Utilization counts a core as fully used when one of its two threads runs; ESXi Thread Utilization counts each thread, at most 100% each, so it shows the idle thread that can still take work.
  - File: [`vsphere/technology/cpu/metrics/host/core-utilization`](vsphere/technology/cpu/metrics/host/core-utilization.md)
- **CPPC**: Collaborative Processor Performance Control (ACPI 5.0+).
  - Also called: Intel HWP
- **CPU Usage (MHz)**: Productive cycles attributed to a vCPU or a physical thread, scaled by frequency. Excludes the idle loop.
  - Product label: Usage (MHz) (vSphere Client, VM and host CPU charts); Used (host summary)
  - Invites: how busy the CPU is, as busy time.
  - Better name: CPU Throughput: completed work, not busy time; at Run 100% it falls as the host fills up. Busy time is Run on a VM, Utilization on ESXi.
  - File: [`vsphere/technology/cpu/concepts/run-time-vs-run-quality`](vsphere/technology/cpu/concepts/run-time-vs-run-quality.md)
- **CPU Utilization for Resources**: 17 legacy rescpu.* metrics. Avoid.
  - Also called: rescpu
  - File: [`vsphere/technology/cpu/metrics/host/cpu-utilization-for-resources`](vsphere/technology/cpu/metrics/host/cpu-utilization-for-resources.md)
- **Efficacy (CPU)**: Work per cycle from core architecture. Not accounted by any metric.
- **Efficiency (CPU)**: Hyper-Threading effect on cycles completed. Accounted as 1.25x per core in VM CPU Used and VM CPU Usage: 0.625x per vCPU when the sibling thread runs. ESXi CPU Used gives each thread of a busy pair 0.5x.
- **ESXi CPU Demand**: vCenter: sum over the running VMs of the CPU they would use with no contention. VCF Operations: per VM the higher of that and its CPU reservation (the Demand (capacity) model), plus the kernel's CPU reservation.
  - Not to confuse with ESXi CPU Usage: kernel work is in ESXi CPU Usage only, so a host with no VMs shows ESXi CPU Demand 0 in vCenter (flat at the kernel reservation in VCF Operations) and ESXi CPU Usage above 0.
  - File: [`vsphere/technology/cpu/metrics/host/demand`](vsphere/technology/cpu/metrics/host/demand.md)
- **ESXi CPU Imbalance**: Running threads / running cores, per host.
  - Also called: Imbalance Score
  - File: [`vsphere/technology/cpu/metrics/host/imbalance`](vsphere/technology/cpu/metrics/host/imbalance.md)
- **ESXi CPU Usage (%)**: Busy time per physical core, scaled by frequency against the base clock: one or both threads busy count once, 100% at the base clock.
  - Product label: Usage (%) (vSphere Client, host CPU chart; VCF Operations); Consumed CPU (%) (vSphere Client host list)
  - Invites: the host is full at 100%, with no headroom left.
  - Better name: CPU Throughput (% of nominal): Turbo takes it above 100%, power saving below Core Utilization. Headroom is read in Thread and Core Utilization, performance in contention counters.
  - Not to confuse with Thread Utilization: ESXi Thread Utilization is busy time per thread at static frequency; ESXi CPU Usage (%) counts per core and moves with Turbo and power saving.
  - File: [`vsphere/technology/cpu/metrics/comparisons/host-consumption-metrics`](vsphere/technology/cpu/metrics/comparisons/host-consumption-metrics.md)
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
  - File: [`vsphere/technology/cpu/metrics/host/utilization`](vsphere/technology/cpu/metrics/host/utilization.md)
- **Total Capacity (GHz)**: Cores × base frequency, for an ESXi host or a cluster: no Turbo, no Hyper-Threading.
  - Product label: Total Capacity, GHz (vSphere Client host and cluster CPU; VCF Operations)
  - Invites: the CPU capacity of the host, so vCPUs are sized and bought in GHz.
  - Better name: Total Base Capacity (GHz): capacity at base (nominal) frequency, no Turbo, no Hyper-Threading; not the throughput the host delivers, which is activity. Capacity is the count of physical threads: 16 cores with Hyper-Threading = 32 threads, at any clock.
  - File: [`vsphere/technology/cpu/concepts/cpu-measurement-levels`](vsphere/technology/cpu/concepts/cpu-measurement-levels.md)
- **Usage Disparity**: Spread of usage across the vCPUs of one VM.
  - Also called: vCPU imbalance, Imbalance vCPU Usage (avoid)
- **VM CPU Latency**: Overlap, Co-stop and Ready without Max Limited, plus the Hyper-Threading and power-saving effects.
  - Product label: Latency (%) (vSphere Client, VM CPU); %LAT_C (esxtop)
  - Invites: the VM waits for CPU, so it has CPU contention.
  - Better name: VM CPU Latency (label kept): not a throughput loss, because it includes the Hyper-Threading effect; it counts time lost against a whole core at nominal frequency, by waiting or by running slower. It rises with no wait and leaves out a limit; the wait is in Ready and Co-stop.
  - File: [`vsphere/technology/cpu/metrics/virtual-motherboard/latency`](vsphere/technology/cpu/metrics/virtual-motherboard/latency.md)
- **VM CPU Used**: Run minus Overlap, scaled by frequency and Hyper-Threading; at VM level plus System and the VMX, MKS and Helper worlds.
  - Also called: %USED (esxtop)
  - Not to confuse with VM CPU Run: VM CPU Run is time only; VM CPU Used moves with frequency, Hyper-Threading and System, so it can sit far above or below Run.
  - File: [`vsphere/technology/cpu/troubleshooting/run-vs-used-gap`](vsphere/technology/cpu/troubleshooting/run-vs-used-gap.md)

### Memory

- **Active (memory)**: Sampled estimate of recently touched VM memory.
  - Also called: Touch (ESXi), Non Zero Active (VCF Operations)
  - File: [`vsphere/technology/memory/metrics/virtual-motherboard/active`](vsphere/technology/memory/metrics/virtual-motherboard/active.md)
- **Balloon Target**: Memory ESXi asks the balloon driver to reclaim.
- **Entitlement (memory)**: Host memory the ESXi scheduler allocates to the VM, from its estimated demand and the reservation, limit and shares policies. A VMkernel value, not an operations counter: troubleshooting reads it only when below configured memory, with Ballooned, Swapped, Compressed and Latency.
  - File: [`vsphere/technology/memory/metrics/virtual-motherboard/entitlement`](vsphere/technology/memory/metrics/virtual-motherboard/entitlement.md)
- **ESXi Memory Usage (%)**: ESXi Memory Consumed / Total Capacity: pages held by VMs, VM overhead, the kernel, vSAN and NSX.
  - Product label: Usage (%) (vSphere Client and VCF Operations, host and cluster memory)
  - Invites: the host is short of memory near 95%.
  - Better name: ESXi Memory Usage (%) (label kept): it maps closest to Consumed; pages held, much of it cache; near 100% is normal. Pressure shows in ballooning, compression, swapping and VM Memory Contention.
  - File: [`vsphere/technology/memory/metrics/host/usage`](vsphere/technology/memory/metrics/host/usage.md)
- **ESXi pages**: Pages ESXi manages on DIMM, host cache or tiered NVMe.
  - Also called: machine pages, machine memory
- **Granted**: VM pages with ESXi pages mapped. VM view.
- **Guest OS In Use**: Windows page class In Use (beside Modified, Cache, Free); Windows can compress part of it.
  - Also called: In Use (Windows)
  - Not to confuse with VM Memory Consumed: Windows In Use is a Guest OS page class; VM Memory Consumed counts the ESXi pages the VM has touched and does not drop when Windows frees memory; the two have no mapping.
  - File: [`vsphere/technology/memory/concepts/guest-os-vs-vm-memory`](vsphere/technology/memory/concepts/guest-os-vs-vm-memory.md)
- **Guest OS Needed Memory**: VCF Operations guest metric behind VM Memory Usage (%) and VM Memory Utilization, the per-VM memory input of capacity Demand.
- **Swap Target**: Memory ESXi aims to reclaim by compression and swapping.
  - Also called: Compress-swap target
- **VM Memory Consumed**: Granted minus sharing savings: the ESXi pages mapped to the VM, without overhead and swapped pages.
  - Product label: Consumed (vSphere Client, VM memory)
  - Invites: what the Guest OS uses now, so a VM near its configured memory needs more.
  - Better name: VM Memory Consumed (label kept): ESXi pages the VM holds from first touch until ESXi reclaims them, guest cache and freed pages included; it does not drop when the Guest OS frees memory. Guest OS need is read inside the Guest OS.
  - File: [`vsphere/technology/memory/metrics/virtual-motherboard/consumed`](vsphere/technology/memory/metrics/virtual-motherboard/consumed.md)
- **Memory Wait**: Memory Contention plus NVMe wait: the share of a VM's vCPU time spent waiting for memory. The memory row of VM Performance, and the source of the memory rows of Cluster Performance and ESXi Performance. Created because Memory Contention is unaware of memory tiering and can read near 0 while the VM waits on NVMe.
  - Also called: memory latency + NVMe wait, Memory Latency (the KPI row)
  - File: [`vsphere/object-types/vm/vm-performance`](vsphere/object-types/vm/vm-performance.md)
- **VM Memory Latency**: Share of time a vCPU waits for a page fault to complete: mostly swap-in, plus decompression and copy-on-write breaks. The only VM memory speed counter. VCF Operations: VM Memory Contention.
  - Also called: page-fault latency, Memory Latency (%), esxtop %LAT_M
  - File: [`vsphere/technology/memory/metrics/virtual-motherboard/latency`](vsphere/technology/memory/metrics/virtual-motherboard/latency.md)
- **VM Memory Usage (%)**: vCenter: from Active. VCF Operations: Guest OS Needed Memory / VM memory, falling back to Active without Guest OS data. Disabled by default in VCF Operations 9.1; Guest|Needed Memory over Mem|Total Capacity gives the same ratio.
  - Product label: Usage (%) (vSphere Client and VCF Operations, VM memory)
  - Invites: the VM needs more memory; read beside ESXi Memory Usage (%) as the same metric.
  - Better name: Active (%) in vCenter, Guest OS Needed Memory (%) in VCF Operations: a kernel estimate or a Guest OS counter, not VM capacity. Guest OS need is read inside the Guest OS: paging, free memory, cache.
  - Not to confuse with ESXi Memory Usage (%): ESXi and cluster Memory Usage (%) is Consumed, a capacity reading; VM Memory Usage (%) is Active (vCenter) or Guest OS Needed Memory (VCF Operations), not a capacity reading. Read as one metric, they have led customers to buy RAM they did not need.
  - File: [`vsphere/technology/memory/metrics/virtual-motherboard/usage`](vsphere/technology/memory/metrics/virtual-motherboard/usage.md)
- **VM pages**: Pages in the VM address space. Vendor term kept for search.
  - Also called: guest physical pages, guest physical memory

### Storage

- **Disk (device)**: A physical disk or LUN presented to ESXi. The vSphere Client uses device and disk for the same thing; a LUN is the array's logical volume, which can span RAID groups.
  - Also called: device, LUN
  - Not to confuse with Virtual disk, datastore: the vSphere Client shows a VM's storage in 3 layers: virtual disk (the VM's own), datastore (VMFS, NFS, vSAN or vVol), disk (the device, shared by every VM on it). Each has its own counters; compare values only within one layer.
  - File: [`vsphere/technology/storage/concepts/storage-layers`](vsphere/technology/storage/concepts/storage-layers.md)

### Performance, SLA and KPI

- **Actual Availability (%)**: Availability as it happened. Same scope as the Availability SLA: the Guest OS. Usually lower than Operational Availability.
- **Class of service**: Gold, Silver, Bronze: classes of the data centre infrastructure a VM runs on, each with its own price, overcommit ratio, maximum VM size and availability SLA. Gold is mission critical, Silver standard production and DR, Bronze test and development or non-production.
  - Also called: Tier, standard production (Silver), test and development (Bronze), non-production (Bronze)
- **Crown jewels**: The critical business applications, strategic to the core business: few VMs, essential to revenue, reputation or both. Each gets a KPI at the infrastructure layer.
  - Also called: Mission-critical applications
  - File: [`sp5-framework/performance/business-application-kpi`](sp5-framework/performance/business-application-kpi.md)
- **KAI**: Key availability indicator: the internal availability indicator, the availability counterpart of the KPI. Provider objects carry a KPI and a KAI, never an SLA.
  - Also called: availability KPI, uptime KPI
  - File: [`sp5-framework/performance/performance-kpi-design`](sp5-framework/performance/performance-kpi-design.md)
- **KPI**: Key performance indicator: an internal baseline for performance only, the P in KPI. Performance monitoring and troubleshooting use the KPI only: no performance SLA, SLI or SLO. One 0-100% score per object: VM, Guest OS, ESXi and Cluster Performance. Availability has KAI; security has KSI.
  - Also called: Key Performance Indicator, performance SLA, SLI, SLO, service level (for performance)
  - Not to confuse with SLA: the KPI is for operations, covers performance, says how bad, is read daily, per object; the SLA is a business contract between two parties, on the consumer's object (VM, pod), read monthly. When a user cites an SLA, ask its metric, object, target and window.
  - File: [`sp5-framework/performance/kpi-vs-sla`](sp5-framework/performance/kpi-vs-sla.md)
- **KSI**: Key security indicator: the internal security and compliance indicator, 100% where the contract (SLA) says 99.95%.
  - Also called: security KPI, compliance KPI
  - File: [`sp5-framework/performance/performance-kpi-design`](sp5-framework/performance/performance-kpi-design.md)
- **Noisy neighbour**: A consumer whose demand degrades others on shared capacity (villain and victims).
  - File: [`sp5-framework/performance/noisy-neighbour`](sp5-framework/performance/noisy-neighbour.md)
- **Operational Availability (%)**: Availability without the downtime inside the green zone or caused by the customer, accounting for the HA design: the number the Availability SLA reports. Usually higher than Actual Availability.
  - File: [`sp5-framework/concepts/sla-metrics`](sp5-framework/concepts/sla-metrics.md)
- **Security SLA**: The contract's security and compliance figure: 99.95% for every class of service; the internal KSI is 100%. The term, not compliance SLA, which is correct but narrower: security also covers activity (attacks, misuse of administrator accounts), not only settings. The IT security industry has not defined it well.
  - Also called: Compliance SLA
  - File: [`sp5-framework/concepts/sla-metrics`](sp5-framework/concepts/sla-metrics.md)

### Capacity

- **Capacity Remaining (%)**: VCF Operations: usable capacity minus the highest projected utilization in the next 3 days, for the most constrained resource.
  - Product label: Capacity Remaining (%), Capacity Remaining Percentage (%) (VCF Operations, cluster and other containers)
  - Invites: the capacity free now, so the next peak fits.
  - Better name: 3-Day Forecast Capacity Remaining (%): the tightest point of a 3-day projection, against usable capacity. A month-end peak beyond the 3 days shows only in Time Remaining.
  - File: [`vcf-operations/features/capacity-forecast`](vcf-operations/features/capacity-forecast.md)
- **Close for Business**: The cluster decision: 1 = closed (no new VM, no VM upsize), 0 = open, decided from Cluster Consumption (%), Cluster Performance (%) and Cluster Risk (%).
  - Also called: Closed cluster, Stop provisioning
  - File: [`vsphere/object-types/cluster/models/close-for-business`](vsphere/object-types/cluster/models/close-for-business.md)
- **Cluster Consumption (%)**: How much of a cluster's usable capacity is consumed: utilization plus saturation, a model, not a KPI. 0 nothing consumed, 100 fully consumed.
  - Also called: Cluster Consumption KPI
  - File: [`vsphere/object-types/cluster/models/cluster-consumption`](vsphere/object-types/cluster/models/cluster-consumption.md)
- **Cluster Risk (%)**: How close the worst ESXi host of a cluster is to contention: a leading indicator and a model, not a KPI. 0 no risk, 100 maximum risk.
  - Also called: Cluster Risk KPI
  - Not to confuse with Time Remaining: Cluster Risk reads the running cluster now (short-term capacity: stop provisioning, no projection); Time Remaining is the long-term runway, days until the forecast crosses usable capacity (buy hardware).
  - File: [`vsphere/object-types/cluster/models/cluster-risk`](vsphere/object-types/cluster/models/cluster-risk.md)
- **Demand (capacity)**: Per VM, the higher of utilization and reservation.
  - Not to confuse with CPU Demand (VM and ESXi): VM CPU Demand and vCenter ESXi CPU Demand are the runtime the VMs would use with no contention, reservations left out; capacity Demand also counts reservations, and VCF Operations ESXi CPU Demand follows it. Two more uses: the VCF Operations setting Capacity Buffer (Demand); memory Demand on the VCF Operations capacity pages, which is ESXi Memory Utilization, this model applied to memory (Broadcom KB 439253). Not the VM footprint (Consumed plus ballooned, compressed and swapped).
  - File: [`sp5-framework/capacity/demand`](sp5-framework/capacity/demand.md)
- **Guest OS sizing**: Sizing vCPU and memory from Guest OS counters (inside).
  - Also called: VM rightsizing (inside the guest)
  - Not to confuse with VM footprint: Guest OS sizing reads Guest OS counters (inside), guest queue included, VM overhead excluded; VM footprint reads vSphere counters (outside), VM overhead included, guest queue excluded. Two jobs, two formulas.
  - File: [`guest-os/system/guest-os-sizing`](guest-os/system/guest-os-sizing.md)
- **Model**: How one pillar of one object is quantified into a number and a decision: capacity, availability, security model. Example: Cluster Consumption and Cluster Risk decide, with Cluster Performance, whether a cluster is closed.
  - Not to confuse with KPI: a KPI scores performance only; capacity and risk are scored by models, so Cluster Risk is a model, not a KPI.
  - File: [`sp5-framework/concepts/modelling`](sp5-framework/concepts/modelling.md)
- **Saturation**: The part of consumption beyond utilization: ballooned, compressed and swapped memory, and the NVMe tier in use. Consumption = Utilization + Saturation. Not contention: nothing is slow yet.
  - File: [`vsphere/object-types/cluster/models/cluster-consumption`](vsphere/object-types/cluster/models/cluster-consumption.md)
- **Enterprise Readiness**: The architectural, operational, security and governance maturity an enterprise requires before it runs a system at scale: availability, recoverability, security, observability, governance, IT operations management, and extra environment copies for development, test and QA. Mandatory by policy, not by technology; it consumes capacity but is not virtualization overhead, because a physical server needs it too.
  - Not to confuse with virtualization overhead: overhead is added by the virtualization layer and cannot be negotiated; Enterprise Readiness is set by a requirement (N+1 or N+2, number of test copies, retention) and can be tuned.
  - File: [`vsphere/architecture/overhead`](vsphere/architecture/overhead.md)
- **Usable capacity**: Total capacity minus HA, buffer and hypervisor overhead. Performance management is never measured against Usable Capacity numbers.

### Operations management

- **Compliance**: Settings measured against internal policy, industry benchmarks and regulation; binary.
  - Not to confuse with Security: security covers live threats and activity, and a security issue is present and urgent; a non-compliant setting is risk (future health) until it is exploited or exposed.
  - File: [`sp5-framework/concepts/overview`](sp5-framework/concepts/overview.md)
- **Decision tree**: A flow that answers one operational question (can it, should it, how much) and ends in a choice to act, with its reason. Folder `decision-tree/`.
  - Not to confuse with Health check: a decision tree answers one question, usually on one pillar; a health check covers every pillar of one object and may read a decision tree's result as one step.
  - File: [`sp5-framework/concepts/health-check`](sp5-framework/concepts/health-check.md)
- **Finding**: Result of troubleshooting or analysis from logs, events, metrics, tasks. Positive feeds insight; negative is an issue.
- **Framework**: How IT operations are managed: policy, pillars, process, people, platform. The SP5 framework; ITIL and COBIT are other frameworks.
  - File: [`sp5-framework/concepts/overview`](sp5-framework/concepts/overview.md)
- **Future health**: Risk: no problem yet; security exposure, compliance, configuration, capacity.
  - Also called: Risk
- **Green zone**: The change window: the agreed time when approved changes, deployments and patches may enter production. Downtime inside it is excluded from Operational Availability.
  - Also called: Change window, maintenance window, authorized execution window
  - File: [`sp5-framework/concepts/sla-metrics`](sp5-framework/concepts/sla-metrics.md)
- **Health check**: Check of one object type (VM, host, cluster), never a technology or a single pillar, in the order availability, performance, security, capacity, with configuration as the drill-down. The what; a superset of troubleshooting. A failed step opens a troubleshooting flow.
  - Also called: what to monitor, monitoring checklist, verification, daily check
  - File: [`sp5-framework/concepts/health-check`](sp5-framework/concepts/health-check.md)
- **Insight**: A top-down reading of alerts, symptoms and findings, with their context and supporting metrics. Proactive; no ticket, no automatic close.
  - Not to confuse with Alert: an alert is an urgent issue (red or orange), bottom up, on one object, with a ticket; yellow is not urgent, so it is an insight, read in the daily health check.
  - File: [`sp5-framework/outputs/alerts-and-insights`](sp5-framework/outputs/alerts-and-insights.md)
- **Issue**: A negative finding, identified by one or more symptoms.
- **Leading indicator, lagging indicator**: Leading: underlying metric read in insights. Lagging: customer-facing metric used in alerts.
- **Notification**: How VCF Operations pushes an alert to a person at once, by email or mobile: red alerts only (urgent and important). An orange alert stays in the NOC alert list; an insight is read on a dashboard.
  - File: [`sp5-framework/outputs/alerts-and-insights`](sp5-framework/outputs/alerts-and-insights.md)
- **Present health**: Real problems now: availability, performance, security incidents.
  - Also called: Health
  - File: [`sp5-framework/concepts/health-risk-efficiency`](sp5-framework/concepts/health-risk-efficiency.md)
- **Prevention window**: Time between the operations team knowing of a problem (insight) and customers noticing it (alert).
- **Primary metric, secondary metric**: Primary: the what of one use case, usually 0-100% and colour coded (VM Performance (%), Capacity Remaining (%)); read in monitoring. Secondary: the why, the possible causes of the primary value; read in troubleshooting.
  - File: [`sp5-framework/observability/triple-see-method`](sp5-framework/observability/triple-see-method.md)
- **Property**: An input set by configuration or capability (configured hosts, maximum VMs), not produced every interval.
  - Not to confuse with Metric: a metric is produced every interval, even when constant (a power state or a VM count is a metric); a property is set by configuration.
  - File: [`sp5-framework/observability/input-types`](sp5-framework/observability/input-types.md)
- **Realm**: A world with a boundary: its owner controls it, and the layer below cannot see into it. Two levels: business, application and IaaS; the Guest OS against the VM. Each realm has its own KPIs, with SLAs between realms.
  - File: [`sp5-framework/concepts/realms-and-layers`](sp5-framework/concepts/realms-and-layers.md)
- **Symptom**: A test on one metric, property or event (VCF Operations). A symptom definition is reusable across alert definitions; a condition is the same test written inside one alert definition. Triggered alone, it is a minor, non-urgent issue, read in the daily health check; when its alert's set of symptoms holds, the issue has become urgent: an alert.
  - Also called: Condition
  - File: [`sp5-framework/outputs/alerts-and-insights`](sp5-framework/outputs/alerts-and-insights.md)
- **Triple See Method**: The SP5 Framework's observability method for VCF: read contention, consumption and context metrics as one set before concluding.
  - Also called: Triple See
  - File: [`sp5-framework/observability/triple-see-method`](sp5-framework/observability/triple-see-method.md)
- **Troubleshooting**: The reactive process for an object that is down or slow: why, and the fix, in the order of checks of its pillar. A security breach gets a forensic investigation instead; compliance is drift detection.
  - Also called: diagnosis, diagnose, root cause analysis, triage
  - Not to confuse with Health check: the health check first finds whether there is a problem (the what); troubleshooting starts from a known one (complaint, alert, failed health check step) and asks why.
  - File: [`sp5-framework/concepts/health-check`](sp5-framework/concepts/health-check.md)
- **Value (pillar)**: One of the five SP5 pillars. Keeps apart cost (what IT spends on infrastructure), price (what IT charges a tenant) and business value (what the investment returns). Formerly cost management.
  - Also called: Cost and price
  - File: [`sp5-framework/concepts/overview`](sp5-framework/concepts/overview.md)

## Metadata

```yaml
id: glossary
retriever_guide: term-meaning
scope: sp5-framework
technology: [cpu, memory, storage, network, system]
pillar: [availability, performance, security, capacity, value]
product: [vsphere, vcf-operations]
internal_derive: []
related:
  - sp5-framework/observability/naming-patterns
  - vsphere/architecture/resource-controls
source:
  document: Knowledge base; vSphere API type names; VCF Operations object types
  path: "n/a"
corrections: []
review_notes:
  - "To check: Sections 'CPU', 'Memory' and 'Capacity': the Product label line of each of the eight label entries, verbatim; vSphere Client 9.1 and VCF Operations 9.1.1 screens (live product), and the chart label tables of the vSphere 9.1 documentation (Overview Performance Charts, p. 2033 onward)."
status: reviewed
```
