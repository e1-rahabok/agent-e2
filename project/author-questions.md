# Questions for the author

Not indexed. One entry per question.

How to answer:
- Write your reply after `Answer:` under each question. Any length.
- Leave `Answer:` empty to skip a question for now.
- Then tell Claude the file is updated. Claude applies each answer to the knowledge base and moves the entry to Resolved.

Each entry has:
- Section: book chapter and Heading 3.
- Files: knowledge-base files affected.
- Search: verbatim strings to find in the book.
- Written as now: what the knowledge base currently says.

## Open

### Q020 · Chapter 3 Memory > ESXi · Consumed and compressed
- Files: [ESXi Memory Consumed](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/host/consumed.md)
- Search 1: "It only includes the resultant zipped, not the amount subjected to compression"
- Search 2: "Consumed does not include compressed"
- Question: does host Consumed include the compressed result in DIMM?
- Written as now: includes the result, flagged. Your diagram (physical view) also shows it inside Consumed.
- Answer:

### Q053 · vCenter API counters · gpu.mem.reserved vs gpu.mem.used
- Files: [GPU monitoring](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/gpu/concepts/gpu-monitoring.md) (sections Counters, Reading the counters, vGPU capacity).
- Search: not from the book. Counters and vCenter 9.1.0 API summaries, on ClusterComputeResource and ResourcePool, level 1:
  - `gpu.mem.reserved` (latest, KB): "The amount of GPU memory consumed by virtual GPUs in kilobytes".
  - `gpu.mem.used` (average, KB): "The amount of GPU memory used by workloads in kilobytes".
  - `gpu.mem.total` (latest, KB): "The total amount of GPU memory in kilobytes".
  - `gpu.utilization` (average, %): "The compute utilization of a GPU in percentage".
- Context: the knowledge base says a vGPU profile fixes the frame buffer per VM, reserved at power-on, so host GPU memory can look high while VMs are idle. Per-device host counters (GPU Memory Usage) are level 4 in the chart tables.
- Question:
  1. Is `gpu.mem.reserved` the sum of the vGPU profile frame buffers of powered-on VMs?
  2. Is `gpu.mem.used` the frame buffer the workloads actually touch, so it is always at or below reserved?
  3. When reserved approaches total, can no further vGPU be placed even with low utilization? (Placement is per physical GPU, so the cluster total may hide fragmentation.)
- Written as now: reserved and used named, with your rule that reservation is a setting and used is activity, so reserved can exceed used. Points 1-3 not stated.
- Answer:

### Q059 · Agent · Core rules and confusable pairs given to the agent up front
- Files: [harness/misreadings.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/misreadings.md) (Level 300 misreadings; moved out of the knowledge base 2026-11-07); [Terminology](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/glossary.md) (section Confusable pairs); design: [harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md), section 3.
- Search: not from the book. Each rule and pair summarises the knowledge file it points to.
- Question:
  1. Are these the 12 rules an expert would give a new colleague first? Which would you drop, add or reword?
  2. Are the 8 confusable pairs right, and is any pair missing?
- Written as now: drafted by Claude 2026-11-06, status draft. The agent receives them only when the switches are on (all off by default).
- Answer: 

### Q060 · Operations flows · Users say the VM is slow: your order of checks
- Files: [Users say the VM is slow: triage](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/performance/troubleshooting/vm-slow-triage.md) (sections Checks, in order; Why this order). Review: [project/review-2026-11-06.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/review-2026-11-06.md), section 3.3.
- Search: not from the book. Drafted from the VM overview file and the per-resource flows.
- Question:
  1. Is this the order you follow in the field: time window, breadth (many VMs?), VM contention per resource, Guest OS queues, then context (limits, snapshots, vMotion)?
  2. What do you check that is missing, for example the application team's own evidence, or a recent change?
  3. Is the SLI bar (Ready 2.5%, memory contention 1%, disk latency 10 ms, transmit dropped 0%) the right first bar for one VM, or do you use other values?
- Written as now: 5 steps, status draft. It hands over to the existing CPU, memory, storage, network and cluster flows.
- Answer:

### Q061 · Operations flows · Can this cluster take more VMs: your order of checks
- Files: [Can this cluster take more VMs?](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/health-check/can-cluster-take-more-vms.md) (sections Checks, in order; Why this order).
- Search: not from the book. Drafted from the capacity model, Cluster Performance, Cluster Risk, Cluster Consumption, admission control and host memory states.
- Question:
  1. Is this your order: cluster state and HA, contention today, Cluster Risk, room after HA and buffer, fit of the new VMs (reservations, overcommit, monster size), balance?
  2. Which resource do you find fills first in practice, and does that change the order?
  3. How do you state the answer to the requester: a yes/no, a number of VMs, or a date?
- Written as now: 6 steps, status draft.
- Answer:

### Q062 · Operations flows · Is this host or cluster healthy right now
- Files: [ESXi: what to monitor, in priority order](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/esxi/health-check/esxi-health-check.md); [vSphere cluster: what to monitor, in priority order](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/health-check/cluster-health-check.md).
- Search: not from the book.
- Question: what is your daily health check of an ESXi host and of a cluster, in order? The overview files list what to monitor, but not the order of checks with a stop at each step. With your order, a health-check flow can be written for each.
- Written as now (2026-11-08): the three overview files are now health checks ([ESXi: health check](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/esxi/health-check/esxi-health-check.md), [vSphere cluster: health check](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/health-check/cluster-health-check.md), [VM: health check](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/vm/health-check/vm-health-check.md)) with numbered steps in the order of health-risk-efficiency. The order inside each pillar is still Claude's.
- Partial answer (author, in session, 2026-11-08): "what to monitor" is a health check; troubleshooting is part of the health check and comes only after an object fails it (monitor is the what, troubleshoot is the why); availability flows, security and compliance are future, after 1.0. Still open: your order inside each pillar, and Q133.
- Answer:

### Q063 · Sources · Book Part 1 and the VCF Operations chapters
- Files: [operations-management/](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management) (4 files and 2 new flows); [vcf-operations/](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations) (1 concept, 12 metrics, 5 KPIs). Review: [project/review-2026-11-06.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/review-2026-11-06.md), section 3.3.
- Search: not applicable.
- Question: please upload Part 1 of the book (capacity and performance management) and your VCF Operations chapters to [project/sources](https://github.com/e1-rahabok/agent-e2/blob/main/project/sources). Today 159 of 206 files come from Part 3, and operators work in VCF Operations, which a third of the screenshot questions show. Claude will fetch the VCF Operations 9.1 metric reference from TechDocs for the catalog.
- Written as now: Part 3 extracted; operations-management and vcf-operations hold only what Part 3 and the vCommunity adapter documentation give.
- Answer:

### Q064 · Review · Which files to review first
- Files: the 25 most-cited knowledge files below (119 files are cited by at least one benchmark question). Review: [project/review-2026-11-06.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/review-2026-11-06.md), section 3.4.
- Search: not applicable.
- Question: 0 of 208 files are `status: reviewed`. Reviewing them in this order puts your review where the benchmark scores. After the first benchmark run, the files behind wrong answers come first. Please confirm the order, or name your own.

| # | Cited by | File |
|---|---|---|
| 1 | 9 | [VM vs Guest OS: two realms and their visibility layers](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/vm-vs-guest-os.md) |
| 2 | 6 | [Resource controls: reservation, limit, shares, entitlement](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/resource-controls.md) |
| 3 | 6 | [VM CPU Ready](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/ready.md) |
| 4 | 6 | [VM Network Packets Dropped](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/network/metrics/virtual-motherboard/packets-dropped.md) |
| 5 | 5 | [VM Disk Latency](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/metrics/virtual-motherboard/disk-latency.md) |
| 6 | 4 | [Overhead: classification, hypervisor overhead and CPU virtualization overhead](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/overhead.md) |
| 7 | 4 | [esxtop storage counters](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/tools/esxtop/storage.md) |
| 8 | 4 | [Cluster SLA and SLI](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/kpis/cluster-sla-sli.md) |
| 9 | 4 | [Capacity model: total, usable, buffer, projection](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/capacity-model.md) |
| 10 | 4 | [CPU frequency, Turbo and their impact on a VM](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/concepts/cpu-frequency.md) |
| 11 | 4 | [Snapshot impact on metrics](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/concepts/snapshot-impact.md) |
| 12 | 4 | [Ballooning](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/ballooning.md) |
| 13 | 4 | [VM Memory Latency](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/virtual-motherboard/latency.md) |
| 14 | 4 | [Hyper-Threading: scheduling and accounting](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/concepts/hyper-threading.md) |
| 15 | 4 | [ESXi CPU Core Utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/core-utilization.md) |
| 16 | 3 | [ESXi Storage adapter and storage path metrics](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/metrics/host/adapter-and-path.md) |
| 17 | 3 | [Guest OS memory vs VM memory](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/guest-os-vs-vm-memory.md) |
| 18 | 3 | [VM Memory Active](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/virtual-motherboard/active.md) |
| 19 | 3 | [vNIC receive drops: find the reason with vsish](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/network/troubleshooting/vnic-rx-drops.md) |
| 20 | 3 | [ESXi storage latency stack: GAVG, KAVG, QAVG, DAVG](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/concepts/esxi-storage-latency-stack.md) |
| 21 | 3 | [Cluster Performance (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/kpis/cluster-performance.md) |
| 22 | 3 | [Cluster Risk (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-risk.md) |
| 23 | 3 | [Why rightsizing matters for VMs](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/rightsizing.md) |
| 24 | 3 | [ESXi storage latency is high](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/troubleshooting/host-storage-latency.md) |
| 25 | 3 | [Admission control, expandable reservations and cluster state](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/concepts/admission-control-and-cluster-state.md) |

- Written as now: all files draft.
- Answer:

### Q072 · Part 1 > The Layers in IT Systems · Apdex
- Files: [Business, application and IaaS: layers, lost context and metric types](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/realms-and-layers.md) (image troubleshooting-layers-loss-of-context-example-table.png).
- Search 1: "Johnny’s transaction was the worst at 20.1 seconds"
- Search 2: "I like the principle behind apdex, but not its implementation"
- Question: (a) and (b), book typos, closed 2026-11-08 (book edition does not matter to Agent E2, author on Q107). (c) The book offers an improved Apdex formula. Give it to the knowledge base, or leave it out, since it is not IaaS?
- Written as now: no number from the image in the text; no Apdex.
- Answer:

### Q086 · Part 1 > Your Private Cloud > Overview > Key Metrics · Operational Availability and green zone
- Files: [IaaS as a service: variants, class of service and what each layer checks](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/iaas-business.md) (section Metrics per pillar).
- Search: "Relative Availability, against your availability architecture and green zone."
- Question: what is the green zone here? (a) the planned availability band of the architecture (for example the HA design target), or (b) something else. The formula comes later, in the Service Level Agreement section; this asks only for the term.
- Written as now: Operational Availability is relative to the availability architecture; green zone left out.
- Answer:

### Q087 · Part 1 > Purpose-Driven Architecture > Day 0 | Day 1 | Day 2 · Host specification example
- Files: [ESXi host specification from class of service and VM profile](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/host-spec-from-class-of-service.md); [Purpose-driven architecture: Day 2 first, business context, automation last, two sides of VCF](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/purpose-driven-architecture.md) (section Day 2 → Day 0 → Day 1); [Noisy neighbour: limit, reservation and share per resource](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/noisy-neighbour.md) (sections Avoiding it, Maximum VM size).
- Search 1: "If 1 CPU typically uses 4 GB RAM, then a 64-core ESXi host will only need 256 GB."
- Search 2: "If you buy a 64-core ESXi, you have 56 cores left and you will be able to sell 224 vCPU."
- Search 3: "For Silver, you plan to overcommit 4:1 for CPU and 2:1 for memory."
- Search 4: "I’ve seen multiple customers having 32-node production clusters running 1K – 2K VMs."
- Question:
  - (a) Basis. Your Q079 answer: overcommit is per physical thread. Silver here is 4:1 per core (56 cores × 4 = 224 vCPU), which is 2:1 per thread. If Silver is meant as 4:1 per thread: 112 threads × 4 = 448 vCPU, 448 × 4 GB / 2 + 64 = 960 GB. Which is meant?
  - (b) Gold keeps no cores or RAM for vSAN, NSX and replication; Silver keeps 8 cores and 64 GB. With the same share, Gold is 56 vCPU and 224 + 64 = 288 GB. Should Gold keep the share too? And is Gold 1 vCPU per core (as here) or per thread?
  - (c) Silver memory overcommit is 2:1 here and 1.5:1 in the Noisy Neighbour table. Keep both as examples, or align them?
  - (d) The 32-node clusters with 1,000-2,000 VMs: a counter-example to the cap of 300 VMs per cluster failure?
- Written as now: the book's numbers, with the basis stated (4:1 per core = 2:1 per thread); Gold with the share shown as Claude's arithmetic; both memory ratios kept as examples; (d) stated without a verdict.
- Answer:

### Q088 · Part 1 > Observability > Symptom | Alert | Insight · Thresholds in the prevention window image
- Files: [Alerts, symptoms and insights: why alert-driven operations stay reactive](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/alerts-and-insights.md) (section Prevention window); [Cluster SLA and SLI](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/kpis/cluster-sla-sli.md); [VM CPU Co-stop](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/co-stop.md); [ESXi storage latency stack: GAVG, KAVG, QAVG, DAVG](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/concepts/esxi-storage-latency-stack.md).
- Search 1: "In the following example, the alerts use the SLA metrics and threshold."
- Search 2: "Correct means the SLA is measured on each paying VM, and not at the infrastructure level."
- Image text (not searchable): "SLA: VM CPU Ready > 5%", "SLA: VM Disk Latency > 10 ms", "Cluster average CPU Ready.", "VM CPU Co-Stop > 2.5%", "VM CPU IO Wait > 1%", "ESXi VMkernel queue > 1 ms", "vMotion stun time > 0.2 second".
- Question:
  - (a) SLA VM CPU Ready above 5%; the SLI table says 2.5%. Which is the SLA threshold?
  - (b) Co-stop 2.5% as an insight threshold; the Co-stop file says below 1% in a high-performing environment. The insight should fire before the alert, yet 2.5% Co-stop is above the 2.5% Ready SLI. Is 2.5% right?
  - (c) VMkernel queue above 1 ms: QAVG or KAVG? The knowledge base says KAVG above 0.5 ms: check QAVG.
  - (d) Cluster average CPU Ready and memory contention listed as SLA alerts. The litmus test says an SLA is measured on each paying VM, not at the infrastructure level. Should the image say cluster worst VM, or are cluster averages meant as provider-side alerts outside the SLA?
  - (e) VM CPU IO Wait: is this VM Other Wait (vCenter), or a Guest OS IO wait?
- Written as now: metric names only, no numbers; nothing added to the threshold catalog until answered.
- Answer:

### Q090 · Part 1 > Observability > Input | Output · Property types, the second Event row, DRS automation level
- Files: [Input types: metric, property, event, log, trace, NetFlow](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/foundations/input-types.md) (sections Property, Event).
- Search 1: "There are 3 types of properties:"
- Search 2: "It can be a setting change, a state change, or a label change."
- Search 3: "Cluster 007 DRS automation level was changed from 2 to 5."
- Search 4: "That’s why state is a metric, not a property."
- Question:
  - (a) The three property types are announced but not listed. Which are they?
  - (b) The table has two rows named Event. Is the second (setting, state, label change) meant as Property? If so, state is listed both as a metric and as a property type.
  - (c) DRS automation level is Manual, Partially Automated or Fully Automated; the 1-5 scale is the migration threshold. Change the example to migration threshold?
- Written as now: setting, state and label change as change events; the example written as migration threshold, flagged.
- Answer:

### Q092 · Part 1 > Begin with The End in Mind > The Crown Jewel · Health across tiers
- Files: [Purpose-driven architecture: Day 2 first, business context, automation last, two sides of VCF](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/purpose-driven-architecture.md) (section Health of an application tier).
- Search: "The health of a tier is the average health of its members."
- Question:
  - (a) Inside a tier, the average. Across tiers (web → application → database) work runs in sequence, like a convoy. Is the application's health the minimum of its tiers?
  - (b) A database tier with active and passive nodes: the passive node serves no requests. Average both, or count the active node only for performance?
- Written as now: tier = average of members; nothing on across tiers or active/passive.
- Answer:


### Q095 · Part 1 > Service Level Agreement > SLA Calculation · Pass scored as 0%, and partial VM scores
- Files: [IaaS SLAs: what each measures and how it is computed](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/sla-metrics.md) (section SLA calculation); [Cluster SLA and SLI](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/kpis/cluster-sla-sli.md) (section Cluster SLI).
- Search 1: "If VM CPU Ready > 2.5% then 100% else 0%"
- Search 2: "So, every 5 minutes, a VM gets a score of 100% or 75%"
- Search 3: "Since SLA is binary, this is simply counted as failure"
- Question:
  - (a) As written, a breach scores 100% and a pass 0%, so a good month averages near 0%, not 99.9%. Should all four lines read "If ... > threshold then 0% else 100%"?
  - (b) The VM SLI is the average of four pass/fail values (100, 75, 50, 25, 0). Penalty Quantification says there is no partial failure. Which holds for the VM: (A) partial, one counter breached = 75% for that interval; (B) binary, any counter breached = 0% for that interval?
  - (c) The Cluster SLI file says a VM must pass all four (option B), while its formula counts breaches divided by 4 (option A). Which should both files say?
- Written as now: pass = 100%; VM SLI = average of the four (option A); Cluster SLI file unchanged, flagged.
- Answer:

### Q096 · Part 1 > Service Level Agreement > Availability SLA · The database restore in Actual Availability
- Files: [IaaS SLAs: what each measures and how it is computed](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/sla-metrics.md) (section Availability SLA, example).
- Search 1: "the large database took 45 minutes to fully restore"
- Search 2: "Actual Availability (%) = 717 / 720 = 99.58%"
- Search 3: "If it takes the application 15 minutes to become fully operational"
- Question: the definition counts the Guest OS only; application start-up is not counted. The example counts 15 minutes of Windows plus 45 minutes of database restore, 3 times: 99.58%. By the definition it is 3 × 15 = 45 minutes: 99.90%. Which is meant: (A) the IaaS Actual Availability is 99.90% and 99.58% is what the application owner sees; (B) 99.58%, because Actual Availability counts everything users see, including the application; (C) other?
- Written as now: both numbers, each with its scope; the SLA covers the Guest OS only.
- Answer:

### Q097 · Part 1 > Service Level Agreement > Performance SLA · Co-stop exclusion and Memory Contention unit
- Files: [IaaS SLAs: what each measures and how it is computed](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/sla-metrics.md) (sections Performance SLA, What the numbers mean); [VM Memory Latency](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/virtual-motherboard/latency.md).
- Search 1: "exclude CPU Co-Stop and CPU Contention from the Performance SLA"
- Search 2: "Memory Contention is relative to the amount of memory being used"
- Search 3: "Unlike CPU, it is not measured across time"
- Question:
  - (a) The book gives the reason for excluding CPU Contention (up to 37.5% unnoticed) but not for Co-stop. What is the reason for Co-stop? Is the 37.5% the Hyper-Threading effect inside Contention?
  - (b) Your Q015 answer: Memory Latency (VCF Operations: Memory Contention) is a share of time a vCPU waits on page faults. This section says it is relative to memory used and not measured across time. Book correction to time?
- Written as now: Co-stop listed as excluded with no reason; Contention excluded for the Hyper-Threading effect (Claude's reading); Memory Contention written as time.
- Answer:

### Q098 · Part 1 > Service Level Agreement > Recommended SLA · Compliance 99.95% or 100%
- Files: [IaaS SLAs: what each measures and how it is computed](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/sla-metrics.md) (section Compliance SLA); [Class of service: price, overcommit, SLA numbers, size limit and cluster design](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/class-of-service.md) (sections Recommended SLA per class, Sample offering).
- Search 1: "I did not put 99.99% as that"
- Search 2: "You should maintain perfect compliance with your compliance requirements for all classes of service"
- Search 3: "you should guarantee to your customers that you will be perfectly (100%) compliant"
- Question: the recommended table gives Compliance 99.95% for every class; the sample offering, the Compliance SLA definition and the Compliance pillar give 100%. Which number goes in the contract? Is 99.95% the contract value, with perfect compliance as the promise outside the maintenance window?
- Written as now: both tables as the book gives them; the definition says perfect compliance outside an ad hoc window.
- Answer:

### Q099 · Part 1 > Service Level Agreement > Price & SLA · Silver ratios, notation and the 64-core licence
- Files: [Class of service: price, overcommit, SLA numbers, size limit and cluster design](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/class-of-service.md) (section Planning example); [ESXi host specification from class of service and VM profile](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/host-spec-from-class-of-service.md) (section Silver at 3:1 CPU).
- Search 1: "For Silver, you decide on 3:1 CPU overcommit and no RAM overcommit"
- Search 2: "(67% of Gold)" and the cells "CPU 1:2", "RAM 1:1.5" in the same table
- Search 3: "Buying 64 cores maximizes your vSphere license"
- Question:
  - (a) The table gives Silver CPU 1:2 and RAM 1:1.5 (price 58% of Gold by the 50/50 rule); the text gives 3:1 and 1:1 (67%). Which is Silver?
  - (b) The book writes overcommit both ways (1:2 in two tables, 2:1 and 4:1 in the sample offering). The knowledge base writes N:1 (consumer : physical). Keep that?
  - (c) 768 GB = 64 cores × 3 vCPU × 4 GB is per core. Per thread (your Q079 rule) it is 1,536 GB. Which basis?
  - (d) VCF 9 is licensed per core with a 16-core minimum per CPU (Broadcom KB 313548); 64 cores no longer maximizes a licence. Drop the reason in the next edition?
- Written as now: Silver from the text (3:1, 1:1, 67%); N:1 notation; per core, flagged; licence reason replaced with the per-core rule.
- Related (2026-11-08, Capacity Management session): Q119 and Q120 (the capacity plan states CPU per thread: Silver 2:1, Bronze 4:1; memory 1.5:1 and 2:1). One answer can settle (b), (c) and Q120.
- Answer:

### Q100 · Part 1 > Service Level Agreement > Size Limit · Socket or logical CPUs
- Files: [Class of service: price, overcommit, SLA numbers, size limit and cluster design](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/class-of-service.md) (section Size limit per class); [Noisy neighbour: limit, reservation and share per resource](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/noisy-neighbour.md) (section Maximum VM size).
- Search 1: "Capping the size at each tier"
- Search 2: "If you allow a single VM to be the same size as the ESXi host"
- Image text (not searchable): "Tier 1 ≤ 1 socket 32 vCPU, 512 GB RAM", "Tier 2 ≤ 50% of a socket", "Tier 3 ≤ 25% of a socket".
- Question: here the cap is per socket (Tier 1 one socket). Noisy Neighbour caps by host logical CPUs (1:1 up to all of them; 2:1 half; 4:1 a quarter). For a 2-socket, 48-core, 96-thread host, Tier 1 is 48 logical CPUs here and 96 there. Which rule should the agent give: (A) socket (NUMA) based; (B) logical-CPU based; (C) both, the smaller wins? Is 32 vCPU per socket meant as 32 cores or 32 threads?
- Written as now: both, each in its file, linked.
- Related: Q111 (VM size by physical cores) and Q125 (8-core block and VM size).
- Answer:

### Q101 · Part 1 > SP5 Framework: Pillars · Relationship lines and what is troubleshot
- Files: [SP5 framework and the five pillars of operations: scope, relationships, non-pillars](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/overview.md) (sections Relationships, Capacity); [Proactive operations: dual track, daily cadence, NOC screens and the VM life cycle](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/proactive-operations.md) (section Who does which day).
- Search 1: "Lines without arrowheads means there is relationship but not impact"
- Search 2: "Availability and Capacity should not overlap"
- Search 3: "Why isn’t there a line to Performance?"
- Search 4: "You troubleshoot availability, performance, and security"
- Question:
  - (a) The text puts Availability-Capacity among lines without arrowheads; the diagram draws an arrow from Availability to Capacity. Arrow or not?
  - (b) The detailed diagram that follows draws Availability → Performance; the text says there is no line. Remove it from the diagram?
  - (c) The detailed capacity diagram says a reservation becomes a share. What is the mechanism you mean?
  - (d) The Day 0-2 table marks compliance not applicable for troubleshooting; the Troubleshoot section troubleshoots security. Is security troubleshot and compliance not?
- Written as now: text version for (a) and (b); (c) written as the label; (d) both, flagged.
- Answer:

### Q102 · Part 1 > SP5 Framework > Health · Where compliance and inventory sit
- Files: [Health: present health, risk and efficiency, not one score](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/health-risk-efficiency.md).
- Search 1: "There are 4 problems that create risk in operations"
- Image text (not searchable): present/future health image, "Is it safe? Security Compliance" under Present Health and "Inventory" under Future Health.
- Question: the table and the grouping image put compliance under risk (future health) and inventory outside health (environment). The present/future health image puts compliance with security in present health and inventory in future health. Which grouping should the agent use?
- Written as now: table and grouping image; the other image's details used as text only.
- Answer:

### Q103 · Part 1 > SP5 Framework > Basic Terminology · Alert: urgent or important; symptom
- Files: [Alerts, symptoms and insights: why alert-driven operations stay reactive](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/alerts-and-insights.md) (sections Symptom, alert, insight; Finding, issue, alert, notification). Related: Q089.
- Search 1: "It’s an urgent Issue with Symptom crossing threshold"
- Search 2: "An issue is identified by its 1 or more Symptom"
- Image text (not searchable): "Important issues" (Issue → Alert), "Urgent issue" (Alert → Notification), "Non-important issue" (Alert → Daily Check).
- Question:
  - (a) The table defines an alert as an urgent issue; the diagram routes important issues to alerts, then urgent ones to notification and non-important ones to the daily check. Is an alert defined by urgency, by importance, or by a symptom crossing a threshold (either)?
  - (b) Symptom: here part of an issue (an issue has 1 or more symptoms); in Observability, a minor non-urgent issue that becomes an alert if it persists. One definition?
- Written as now: both, flagged.
- Answer:

### Q105 · Part 1 > Monitor | Troubleshoot; SP5 Framework: Process · Logs in monitoring and the length of the daily check
- Files: [Monitoring vs troubleshooting, root cause analysis and validating a log alert](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/monitoring-vs-troubleshooting.md); [Proactive operations: dual track, daily cadence, NOC screens and the VM life cycle](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/proactive-operations.md).
- Search 1: "Not required. Metrics, properties, and Event suffice."
- Search 2: "Should take just 5 minutes"
- Search 3: "The check must be quick, ~1 minute"
- Search 4: "There are 3 techniques we can apply"
- Image text (not searchable): "Daily Check (10 minutes)"; present health "Data is mostly coming from logs, not metrics".
- Question:
  - (a) Monitoring needs no logs, yet availability data comes mostly from logs and the daily SOP reads logs for soft errors. Is log analysis (daily, in the cadence image) part of monitoring?
  - (b) Monitoring 5 minutes, daily check about 1 minute, timeline 10 minutes. One number?
  - (c) 3 techniques announced, 4 listed (text) and 4 in the diagram with other names. Use the diagram names?
- Written as now: (a) and the interval applied 2026-11-08 (monitoring-vs-troubleshooting: Logs row required, 20-second peak within the 5-minute interval, 20-second visibility for mission-critical systems); (b) applied: about 5 minutes when there is no problem; (c) the diagram's four techniques.
- Answer: Monitoring needs log. Monitoring depends on what is being monitored. Log is streaming continuously not discrete every 5 minutes or 1 minute. Performance monitoring reports peak of 20 seconds within 5 minutes reporting interval. An exception is mission critical system where 20 seconds visibility is worth the cost of monitoring. I'll review item 105(c).
- Answer (b), 2026-11-08: A daily check, if there is no problem, it should take a few minutes. That's why I put 5 minutes. Now, if there is a problem, logically, it can take a lot longer than that, depending on the problem.
- Applied (b): proactive-operations (A 24-hour day, Dual track, Traps), monitoring-vs-troubleshooting (Duration row).
- Still open: (c).

### Q106 · Part 1 > Service Level Agreement > Performance SLA · SLA counters vs the prevention window alerts
- Files: [IaaS SLAs: what each measures and how it is computed](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/sla-metrics.md); [knowledge/catalog/thresholds-performance.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-performance.yaml) (rows vm-sli-*). Related: Q088 (a).
- Search: "Use the above threshold as they are."
- Question: the four SLI thresholds are now catalog rows at 5-minute VM level (CPU Ready 2.5%, Memory Contention 1%, Disk Latency 10 ms, Transmit Dropped 0%). Q088 (a) asks about the 5% Ready in the prevention window image. Confirm the rows, and that the SLA reading is the 5-minute VM average, never the 20-second peak?
- Written as now: four rows, interval 5m, instance aggregate.
- Answer:

### Q108 · Part 1 > Configuration Management > Resource Management, Share · Memory share unit and the share example
- Files: [Resource settings: when and how](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/vm/configuration/resource-settings-guidance.md) (sections Review: how each control affects operations, Review: share values).
- Search 1: "10 per GB" (default VM memory shares table)
- Search 2: "per VM GB of RAM = 10240"
- Search 3: "Both VMs want to consume 10 GHz"
- Search 4: "In this case, VM 1 gets 5 GHz and VM 1 gets 5 GHz"
- Image text (not searchable): "A 2000 worth of reservation depends on the value of other VMs reservation" (VM Share row).
- Question:
  - (a) The table gives memory shares per GB (5, 10, 20); the text and the vSphere defaults are per MB (10,240 per GB at Normal). Correct the table to per MB?
  - (b) A 1-vCPU VM cannot consume 10 GHz on a host whose cores run at about 2-3 GHz; it is capped at one core. Change the example (for example, two 2-vCPU and 4-vCPU VMs on a 10 GHz host), or keep it and say the cap?
  - (c) Second VM 1 should read VM 2; the image says reservation where it means share. Confirm both.
  - (d) You were unsure why a resource pool is 4x a VM for CPU and 16x for memory. The knowledge base explains it as a Normal pool weighing as much as a Normal 4-vCPU, 16-GB VM. Agree?
- Written as now: per MB; the 1:2 split with the one-core cap stated; (d) as Claude's explanation.
- Answer:

### Q109 · Part 1 > Configuration Management > Limit · Is there a network limit
- Files: [Resource settings: when and how](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/vm/configuration/resource-settings-guidance.md) (section Review: how each control affects operations, Limit); [Noisy neighbour: limit, reservation and share per resource](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/noisy-neighbour.md) (section Network).
- Search: "There is no network limit"
- Question: with Network I/O Control each VM network adapter has share, reservation and limit, and port groups have traffic shaping. Noisy Neighbour says so (and your Q083 withdrew the 8 Gb/s limit as a recommendation, not as a feature). Change to: a network limit exists per vNIC but is not recommended?
- Written as now: VM limits for CPU, memory and disk IOPS; the network sentence left out.
- Answer:

### Q110 · Part 1 > Configuration Management > Reservation, Cluster, Resource Pool · Admission control, slot size and siblings
- Files: [Cluster configuration review: HA, DRS, DPM and cluster variants](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/configuration/cluster-configuration-review.md) (section HA); [Resource settings: when and how](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/vm/configuration/resource-settings-guidance.md); [Admission control, expandable reservations and cluster state](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/concepts/admission-control-and-cluster-state.md); [Scalable Shares and resource pool siblings](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/scalable-shares.md).
- Search 1: "Reservation is respected only when Admission Control is enabled"
- Search 2: "this will impact the HA Slot Size"
- Search 3: "Resource Pool with VM as sibling is a common mistake"
- Question:
  - (a) Host and DRS admission control enforce reservations at power-on whether or not HA admission control is on; HA admission control only keeps failover capacity for them. Reword to: with HA admission control off, reservations are not protected after a host failure?
  - (b) Reservations change the slot size only under the slot policy; the default policy is cluster resource percentage. Add that condition?
  - (c) With Scalable Shares (vSphere 7 and later) a pool and VMs as siblings no longer dilute. Is the sibling rule still a mistake, or only without Scalable Shares?
- Written as now: (a) and (b) worded with the condition; (c) both kept, flagged.
- Answer:

### Q111 · Part 1 > Configuration Management > Compute-related, ESXi · Cores or threads, and 48 or 64 cores
- Files: [VM configuration review: VMware Tools, hardware, compute and storage settings](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/vm/configuration/vm-configuration-review.md) (section Compute); [ESXi configuration review: hardware, versions, availability, security, capacity, consistency](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/esxi/configuration/esxi-configuration-review.md) (sections Memory, Capacity). Related: Q079, Q099, Q100.
- Search 1: "do not count the logical processors"
- Search 2: "So a machine with 64 cores 128 threads get 512 GB of RAM"
- Search 3: "Aim for 48 to maximise software license"
- Question:
  - (a) Relative VM size counts physical cores, not logical processors; Noisy Neighbour sizes by logical CPUs (Q079: overcommit per thread). Which basis for the maximum VM size?
  - (b) 512 GB for 64 cores and 128 threads at 4 GB per vCPU is 1 vCPU per thread; the Price & SLA example (768 GB) is per core. Which?
  - (c) 48 cores here, 64 cores in Price & SLA, both to maximize the licence. Under per-core licensing (16-core minimum per CPU) neither holds. Drop both?
- Written as now: physical cores for VM size; the 512 GB rule as given; licence reason dropped.
- Related: Q099, Q100, Q120 (per thread in the capacity plan) and Q125.
- Answer:

### Q114 · Part 1 > Capacity Management > Stages and Capacity Model · Book text fixes
- Files: [Capacity management: demand, supply, phases and planning inputs](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/capacity-management-process.md), [Capacity dimensions](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/capacity-dimensions.md).
- Search 1: "e first place, by using progressive pricing"
- Search 2: "They need to be reviewed as complimentary"
- Search 3: "measured againsts usable"
- Question: (a) Search 1 is a sentence fragment after the four-phase table; text seems lost before it. What was meant? (b) "complimentary" should be "complementary". (c) "againsts" should be "against". Confirm (b) and (c) for your next edition.
- Written as now: fragment left out; the knowledge base uses the corrected words.
- Answer:

### Q115 · Part 1 > Capacity Management > "Good" Advice · Why each statement is wrong
- Files: [Capacity dimensions](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/capacity-dimensions.md) (section Traps), [Capacity management: demand, supply, phases and planning inputs](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/capacity-management-process.md) (section Traps).
- Search 1: "Memory Active should not exceed 50-60%"
- Search 2: "Memory should be running at high state"
- Question: the book lists 9 statements as wrong but does not say why. Claude wrote one reason per statement as a trap. Confirm or correct each:
  - (a) 2:1 RAM overcommit is risky → a ratio ignores utilization, VM size and class; Bronze can run 2:1.
  - (b) 90% memory, aim for 80% because of HA → usable capacity already excludes the HA host; subtracting HA again counts it twice.
  - (c) Active below 50-60% → Active is a sampled estimate; capacity reads demand against usable capacity.
  - (d) Each host in the high memory state → High means much free memory: wastage.
  - (e) 5:1 CPU on an important cluster → important clusters take a lower ratio.
  - (f) 3:1 gives buffer for spikes and HA → allocation ignores utilization and VM size; buffer and HA belong in usable capacity.
  - (g) 4:1 for Tier 3 → not used as a trap; what is wrong with it?
  - (h) UAT at 70%, worry at 85% → utilization alone does not close a cluster; read contention and risk.
  - (i) 25% CPU is good, plenty left → below 40% of usable is wastage.
- Written as now: (a)-(f), (h), (i) as traps.
- Answer:

### Q116 · Part 1 > 4 Dimensions of Capacity > Utilization · Zones vs Cluster Consumption bands
- Files: [Capacity dimensions](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/capacity-dimensions.md) (section Utilization), [Cluster Consumption (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-consumption.md), [thresholds-capacity.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-capacity.yaml) (rows cluster-utilization-usable-wastage, cluster-utilization-usable-best).
- Search: "I divide the capacity into 10 equal chunks"
- Question: the book puts 40-80% of usable capacity in green and 80% as best. Cluster Consumption (%) has CPU green 0-55, yellow 55-70, orange 70-85, red 85-100, and memory green 0-70. A 10-host N+1 cluster at the best 80% of usable is 72% of total: orange on CPU in Cluster Consumption. (a) Is Cluster Consumption measured against total or usable capacity? (b) Which governs? (c) Give values for yellow, orange and red above 80%. (d) Should Cluster Consumption get a grey band (0-40%) for wastage? The plan lists grey values for capacity bands as open.
- Written as now: zones as rules (grey below 40%, best 80%); Cluster Consumption bands unchanged.
- Answer:

### Q117 · Part 1 > 4 Dimensions of Capacity > Allocation · Memory tiering version
- Files: [Capacity dimensions](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/capacity-dimensions.md) (section Allocation), [Memory tiering](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/memory-tiering.md).
- Search: "a new feature in vSphere 8"
- Question: memory tiering was a tech preview in vSphere 8.0 Update 3 and is supported from vSphere 9.0. The knowledge base says introduced in 9.0. Change the book to vSphere 9?
- Written as now: no version in the capacity file; memory-tiering says 9.0.
- Answer:

### Q118 · Part 1 > 4 Dimensions of Capacity > Reservation | Share · Unit of CPU reservation
- Files: [Capacity dimensions](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/capacity-dimensions.md) (section Reservation and share).
- Search: "That’s why the unit is Hertz, milliseconds"
- Question: CPU reservation is set in MHz. What does "milliseconds" refer to? Share is the runtime one (time slices). Remove "milliseconds" from the reservation column?
- Written as now: reservation in Hz; share in time slices.
- Answer:

### Q119 · Part 1 > Capacity Model > Planning Phase · Is the gap 2x everywhere
- Files: [Class of service in capacity planning](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/class-of-service-planning.md) (section Example implementation), [Noisy neighbour](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/noisy-neighbour.md) (section Avoiding it).
- Search: "Notice the consistent 2x gap"
- Question: the implementation table keeps 2x for reservation (50/25/12.5% CPU, 100/50/25% RAM), CPU allocation (1:1, 2:1, 4:1) and contention (0.5/1/2% unmet). Memory allocation is 1:1, 1.5:1, 2:1, and utilization (50/70/90% CPU) is not 2x. Is memory deliberately less than 2x (risk of swapping), and should the text say so?
- Written as now: the values as in the table, with a note that memory and utilization do not follow 2x.
- Answer:

### Q120 · Part 1 > Planning Phase vs Cluster Risk · Bronze plan scores red
- Files: [Class of service in capacity planning](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/class-of-service-planning.md), [Cluster Risk (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-risk.md) (Allocation rows).
- Search: "Notice the consistent 2x gap"
- Question: Bronze CPU 4:1 per thread is 8 vCPUs per core with Hyper-Threading. Cluster Risk counts vCPUs per physical core and marks 3-4 as red; Silver 2:1 per thread (4 per core) is red too. Bronze memory 2:1 sits in the Cluster Risk red range 1.8-2.2. So a cluster built to your plan always shows red overcommit rows, and with the production closure limit (Risk above 50%) it may close. (a) Should the Cluster Risk overcommit bands depend on the class of service? (b) Or is Cluster Risk meant only for Gold and Silver clusters?
- Written as now: both files unchanged; the conflict is noted in review_notes.
- Answer:

### Q121 · Part 1 > Capacity Model > Cluster Closure > Logic · Non-production capacity and the orange case
- Files: [Can this cluster take more VMs?](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/health-check/can-cluster-take-more-vms.md) (steps 4 and 5), [thresholds-capacity.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-capacity.yaml) (rows closure-*).
- Search 1: "If both capacity and performance are orange"
- Search 2: book table after "Implementing the above with actual threshold"
- Question: (a) Non-production closes on performance and risk later than production (red below 20% vs 40%; risk above 75% vs 50%), but on Capacity Remaining earlier (red below 15% vs 10%; orange below 30% vs 20%). Intended (smaller buffer in non-production), or swapped? (b) One orange and one green: open without a risk check? (c) The flow now follows your closure logic for steps 2-5; Q061 stays open for the full order (state, fit, balance).
- Written as now: as in the book table; (b) read as open.
- Answer:

### Q122 · Part 1 > Cluster Closure vs Planning Phase · Performance (%) closure values
- Files: [Can this cluster take more VMs?](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/health-check/can-cluster-take-more-vms.md) (step 4), [Class of service in capacity planning](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/class-of-service-planning.md) (section Example implementation), [Cluster Performance (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/kpis/cluster-performance.md).
- Search: book table after "Implementing the above with actual threshold"
- Question: production closes when Performance (%) at the 95th percentile of 24 hours drops below 40% (red) or 60% (orange). The class minimum for VM Performance (%) is 98-99.5%. The knowledge base reads the first as the cluster KPI (Cluster Performance, worst VM and 90th percentile rows) and the second as the VM KPI. Correct? With the weighted scoring, one row a quarter into red already gives about 53%; is 40% the value you want?
- Written as now: both, as different metrics.
- Answer:

### Q123 · Part 1 > Capacity Management > Reclamation · Benefit table and scope
- Files: [Reclamation](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/reclamation.md) (sections When reclamation is the provider's job, What each area frees).
- Search 1: "Cluster RAM as idle RAM pages tend to occupy ESXi memory"
- Search 2: "It is only applicable when VMs are free"
- Question: (a) In the benefit table, cells seem shifted: Idle VM, Storage holds "Cluster RAM as idle RAM pages tend to occupy ESXi memory"; Oversized VM, Memory holds the context-switch text (a CPU benefit). Claude rewrote the table from the chapter text: unused VM frees real CPU and memory; oversized VM frees memory and performance, CPU in allocation only; idle VM frees memory, CPU in allocation only; storage only on delete. Correct? (b) The chapter starts with reclamation applying only when VMs are free, then applies the stocktake to internal IT with chargeback. Which scope is right?
- Written as now: the rewritten table; both scope statements.
- Answer:

### Q124 · Part 1 > Reclamation > TRIM and Unmap · Per datastore
- Files: [ESXi Datastore metrics (host view)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/metrics/host/datastore.md) (section Unmap).
- Search: "but you can’t aggregate them per datastore"
- Question: the knowledge base reads this as: the metrics are on the ESXi host with one instance per datastore, and no datastore-wide total across hosts exists. Correct?
- Written as now: as above; sum the hosts that mount the datastore.
- Answer:

### Q125 · Part 1 > Rightsizing > Best Practices · 8-core block, 8 and 16 vCPU
- Files: [Rightsizing VMs](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/rightsizing.md) (section Practices), [Cluster Risk (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-risk.md) (section Monster VM).
- Search: "AMD EPYC and Intel Xeon use an 8-core block"
- Question: AMD EPYC uses 8-core CCDs (16 cores on Zen 4c and Zen 5c). Intel Xeon has no 8-core block: Sapphire Rapids and Emerald Rapids use up to 4 tiles, Granite Rapids compute dies of over 40 cores, each a shared-LLC mesh. (a) Limit the 8-core block to AMD? (b) Why does a VM above 8 vCPU risk the Hyper-Threading effect? HT sharing depends on host load, not on VM size against a CCD. (c) A NUMA node on current hosts holds 32-128 cores; is above 16 vCPU about the CCD (L3) effect inside a socket, not NUMA? Cluster Risk repeats "most Xeon and EPYC use 8-core CCDs".
- Written as now: the book rule, attributed, with a review note.
- Related (2026-11-08): the Configuration Management review list says a 64-core CPU is 8 chiplets of 8 cores and a VM above 8 vCPU spans chiplets ([VM configuration review](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/vm/configuration/vm-configuration-review.md), section Compute). The same answer applies there. Also Q111.
- Answer:

### Q126 · Part 1 > Rightsizing > Optimization vs The Big Picture · 100% or 40%
- Files: [Rightsizing VMs](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/rightsizing.md) (sections What to optimize, Big picture).
- Search 1: "utilization should be 100% to minimize ping pong"
- Search 2: "You expect this number to hover around 40%"
- Question: per VM, CPU utilization should be near 100%; across hundreds of large right-sized VMs, the average is about 40% and the max about 80%. The knowledge base reads the first as the aim per VM at its busy time, the second as the fleet average over every 5 minutes. Correct?
- Written as now: as above.
- Answer:

### Q127 · Part 1 > Performance | Capacity vs Capacity Model > Demand · Reservation: supply or demand side
- Files: [Performance vs capacity](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/performance-vs-capacity.md) (section Usable capacity exists only in capacity), [Capacity dimensions](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/capacity-dimensions.md) (section Demand).
- Search 1: "Demand = Max (Utilization, Reservation)"
- Search 2: Performance Management chapter, Performance | Capacity, the usable capacity diagram.
- Question: performance-vs-capacity says capacity subtracts HA, buffer, hypervisor overhead and reservation from total capacity. This chapter puts reservation on the demand side: demand = Max (utilization, reservation), per VM, against usable capacity. Subtracting it from supply as well counts it twice. Remove reservation from the usable capacity sentence?
- Written as now: both files as they are.
- Answer:

### Q128 · Glossary · Proposed terms from Capacity Management
- Files: [Terminology](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/glossary.md) (Defined terms, Confusable pairs).
- Search: "Stop Provisioning (Yes/No)"
- Question: three proposals, in use as drafts: (a) defined term "Closed cluster" (also called stop provisioning); (b) pair "Demand (capacity) vs ESXi CPU Demand"; (c) pair "Idle vs oversized vs unused VM". Keep, rename or drop?
- Written as now: all three in the glossary.
- Answer:

### Q129 · VCF Operations 9.1 · Prometheus access for scripts
- Files: [Real-time metrics](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/concepts/real-time-metrics.md).
- Search: not from the book. TechDocs "Real-time Data in the Workbench": "Use the Add Query input field to enter and run your PromQL query."
- Question: you say 2-second metrics are for programmatic use, with native Prometheus compatibility. The 9.1 docs show PromQL only in the Workbench Custom Query sub-tab; no Prometheus endpoint or API is described. How do scripts reach it (endpoint, auth, doc link)?
- Written as now: PromQL in Custom Query; programmatic use stated from you.
- Answer:

### Q130 · Benchmark · Retrieval check: what number is good enough to release
- Files: [benchmark/retrieval-check.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/retrieval-check.md) (section What is a good number); [project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md) (M3 exit criteria: target to set with the author).
- Search: not from the book.
- Question: proposed gate for classic mode: release at least 90% of questions with every needed file in context (81 of 90) and context recall at least 95%; target 97% (87 of 90) and 98%; perfect (100%) not a goal, except that no question may miss its main file. Today: 54-57 of 90. (a) Accept these levels? (b) Should each question mark its main file in `knowledge`, so the check can report main-file misses separately?
- Written as now: the proposal, marked as not agreed.
- Answer:

### Q131 · VCF-vCommunity-Adapter · KPI is performance only: names in the adapter documentation
- Files: [Cluster Risk (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-risk.md), [Cluster Consumption (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-consumption.md), [Close for Business](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/close-for-business.md); [Cluster SLA and SLI](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/kpis/cluster-sla-sli.md).
- Search: adapter docs/reference/metrics/README.md: "KPIs: Cluster Performance, Cluster Risk, Cluster Consumption, ESXi Performance, VM Performance, Guest OS Performance"; periodic-cluster-check.md: "the three cluster KPIs".
- Question: your decision (2026-11-08): KPI is strictly performance; capacity and risk are models. (a) The adapter documentation still lists Cluster Risk and Cluster Consumption as KPIs: will you rename them there, or should the knowledge base keep a synonym? (b) Cluster SLA and SLI stays in `kpis/`: an SLA covers performance here (SLI on contention), so it stays. Correct, or a folder of its own?
- Written as now: Cluster Risk and Cluster Consumption moved to `vcf-operations/models/` and titled as models; SLA and SLI unchanged.
- Answer:

### Q132 · VCF-vCommunity-Adapter vs Part 1 > Cluster Closure · Which closure thresholds does Agent E2 apply
- Files: [Close for Business](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/close-for-business.md), [Can this cluster take more VMs?](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/health-check/can-cluster-take-more-vms.md) (step 4). Related: Q121, Q122.
- Search: book table after "Implementing the above with actual threshold"; adapter periodic-cluster-check.md, section The rule.
- Question: the book closes production at Performance (%) below 40% (red) and Risk above 50%, non-production below 20% and Risk above 75%, with Capacity Remaining bands. The pack closes every cluster at Performance or Consumption below 25 / above 75 (red), or both orange with Risk orange or red. (a) When a user asks "is this cluster closed", which applies: the book (class of service) or the pack (one band set)? (b) Is the pack the current version of the book table?
- Written as now: both, each in its own file; the closure flow says the pack automates steps 4 and 5.
- Answer:

### Q133 · Health check · Decisions still open from the 2026-11-08 review
- Files: [KNOWLEDGE-ENGINEERING.md](https://github.com/e1-rahabok/agent-e2/blob/main/KNOWLEDGE-ENGINEERING.md) (section 10); the three health checks.
- Search: not from the book.
- Question: (a) Without VCF Operations (vCenter only), should a health check fall back to the raw counters of each KPI sub-metric? Answered (author, 2026-11-08): the question is invalid; there is no vCenter without VCF Operations. The fallback line was removed from the ESXi health check. (b) Order: answered by Q104 (2026-11-08): availability, performance, security, with configuration as the drill-down under each; every performance flow checks configuration. Still open: does risk (capacity, compliance) and efficiency follow, as in health-risk-efficiency? (c) Keep the word triage for the first troubleshooting step after a complaint (vm-slow-triage), or drop it?
- Written as now: (a) resolved, no fallback; (b) as stated; (c) triage kept.
- Answer:

### Q134 · Part 3 > Metric Mastery > Triple See Method · Why not USE, RED, Golden Signals
- Files: [Triple See Method](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/triple-see-method.md) (section Why not USE, RED or Golden Signals).
- Search: "Based on their strengths and weaknesses, I came up with The Triple See Method"
- Question: the book does not say what each method lacks. Claude wrote: USE starts from utilization (consumption), which does not show who waits in an overcommitted cluster; RED and the Golden Signals are request-centric, built for services, and a VM has no request to time; none has a context type; none maps metric types to pillars. Correct, and anything to add?
- Written as now: as above.
- Answer:

### Q135 · Why a New Framework? > Complexity · ITIL 4 or ITIL 5
- Files: [Why SP5 and not ITIL](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/why-a-new-framework.md) (section Complexity).
- Search: "ITIL 5 has 34 management practices"
- Question: the 34 practices are ITIL 4 (the linked list is ITIL 4). Is "ITIL 5" a typo, or does ITIL 5 keep the same 34?
- Written as now: ITIL 4.
- Answer:

## Resolved

### Q094 · Repository · Where cross-pillar operations files go
- Files: [IaaS as a service: variants, class of service and what each layer checks](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/iaas-business.md); [Purpose-driven architecture: Day 2 first, business context, automation last, two sides of VCF](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/purpose-driven-architecture.md); [Alerts, symptoms and insights: why alert-driven operations stay reactive](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/alerts-and-insights.md).
- Search: not applicable. Rule: [project/tools/lint.py](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/lint.py) allows only pillar folders (performance, capacity) under [knowledge/operations-management](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management).
- Also (2026-11-07, Service Level Agreement to SP5 Framework: Process): [IaaS SLAs: what each measures and how it is computed](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/sla-metrics.md), [Class of service: price, overcommit, SLA numbers, size limit and cluster design](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/class-of-service.md), [SP5 framework and the five pillars of operations: scope, relationships, non-pillars](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/overview.md), [Health: present health, risk and efficiency, not one score](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/health-risk-efficiency.md), [Monitoring vs troubleshooting, root cause analysis and validating a log alert](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/monitoring-vs-troubleshooting.md), [Proactive operations: dual track, daily cadence, NOC screens and the VM life cycle](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/proactive-operations.md): same placement, same question.
- Also (2026-11-07, Configuration Management): [Configuration management: standards, review dimensions and the four types of check](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/configuration-management.md). There is no configuration pillar; it sits in performance/ for now.
- Question: these three files cover several pillars (availability, performance, capacity, security) and the platform itself. They are in `operations-management/performance/` to pass lint. Options: (A) keep them in performance/; (B) allow files at the root of `operations-management/`; (C) a new folder such as `operations-management/service/`.
- Written as now: option A, pillars in the tags.
- Answer: (B). C is wrong as the jargon service is incorrect here. Applied 2026-11-08: 12 cross-pillar files and their images moved to [knowledge/operations-management](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management); lint allows files at its root; every reference updated.

### Q091 · Part 1 > Purpose-Driven Architecture > The 2 Sides of VCF · Workload and the pillar list
- Files: [Purpose-driven architecture: Day 2 first, business context, automation last, two sides of VCF](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/purpose-driven-architecture.md) (section Two sides of VCF); [Three perspectives on metrics](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/foundations/metric-perspectives.md); [project/tools/tags.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/tags.yaml) (pillar).
- Search 1: "Workload means the customers VM, not your infrastructure software."
- Search 2: diagram label "IT (VCF & Non-VCF Appliances )"
- Question:
  - (a) The text excludes infrastructure software from workload; the diagram lists IT appliances under Workloads. Are VCF appliances (vCenter, NSX Edge) workloads?
  - (b) Pillars differ across the book: this diagram has seven (availability, performance, security, compliance, capacity, configuration, inventory); Key Metrics has availability, performance, capacity, compliance; the `pillar` tag has availability, performance, security, capacity, value. Options: (A) keep the tag list; (B) add compliance, configuration and inventory to the tag; (C) another list.
- Written as now: workload = customer VMs, appliances also run as VMs; pillar tag unchanged.
- Answer: (a) Yes and No. They are technically workload, as they are VM that runs on vSphere Cluster. Operationally they are not owned by the business users. They are yours, so they are internal and hence have 0 SLA. They only have KPI. SLA is always between 2 parties.
  (b) Pillars follow the SP5 Framework diagram in Part 1 of the book.
  Applied 2026-11-08: purpose-driven-architecture (Two sides of VCF); pillar tag now availability, performance, compliance, capacity, cost (tags.yaml, 44 files); pillars-of-operations renamed sp5-framework. (a) Yes and No. They are technically workload, as they are VM that runs on vSphere Cluster. Operationally they are not owned by the business users. They are yours, so they are internal and hence have 0 SLA. They only have KPI. SLA is always between 2 parties.
  (b) Pillars follow the SP5 Framework diagram in Part 1 of the book.
  Applied 2026-11-08: purpose-driven-architecture (Two sides of VCF); pillar tag now availability, performance, compliance, capacity, cost (tags.yaml, 44 files); pillars-of-operations renamed sp5-framework.

### Q089 · Part 1 > Observability > Alert · Importance of alerts and the colours
- Files: [Alerts, symptoms and insights: why alert-driven operations stay reactive](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/alerts-and-insights.md) (sections Alert vs insight, Criticality).
- Search 1: "Hopefully not important issue"
- Search 2: "Urgent and important. However, it does not always mean you must drop everything you do and start firefighting in seconds."
- Search 3: "Symptom. Non urgent. Leading Indicators. Symptoms. Could be important, could also be false positive"
- Question:
  - (a) The alert vs insight table says alerts are hopefully not important and insights are important. The colour table says red alerts are urgent and important, and the diagram calls yellow low importance while the table says it could be important. Which wording should the knowledge base keep?
  - (b) Red: attend within 1-2 hours (table) vs review it today, the sooner the better (legend image). Keep 1-2 hours?
  - (c) Do the KPI colour bands (green, yellow, orange, red in the VCF Operations KPIs) carry the same response times: yellow next business day, orange today, red within 1-2 hours?
- Written as now: alerts urgent; red urgent and important, 1-2 hours; yellow possibly important or a false positive; (c) not stated.
- Answer: (a) Alerts should be minimized to issues that you cannot avoid, as each alert is reactive. When you react, you lose as time has started. So you hope that the alerts are not important. It's common for Enterprise IT to experience alerts storm and alerts fatigue. The root cause is the alerts are never defined properly. Red = urgent + important. Orange = urgent + not important. Yellow = not urgent, hence removed from the alerts definition and dealt as insights as part of proactive Health Check. Do this at the start of the day, or the start of your shift.
  (b) Red = ASAP, max within 1-2 hours. Orange = by end of day, do not differ until tomorrow. Any issue that can be deferred until tomorrow is not urgent. They are best dealt as a group as insight, so you can see the big picture.
  (c) No. The color in alert has a timeline as alert is reactive by nature. Time has started. The color in KPI is for proactive. They are not related.
  Applied 2026-11-08: alerts-and-insights (Alert vs insight, Criticality, Traps). (a) Alerts should be minimized to issues that you cannot avoid, as each alert is reactive. When you react, you lose as time has started. So you hope that the alerts are not important. It's common for Enterprise IT to experience alerts storm and alerts fatigue. The root cause is the alerts are never defined properly. Red = urgent + important. Orange = urgent + not important. Yellow = not urgent, hence removed from the alerts definition and dealt as insights as part of proactive Health Check. Do this at the start of the day, or the start of your shift.
  (b) Red = ASAP, max within 1-2 hours. Orange = by end of day, do not differ until tomorrow. Any issue that can be deferred until tomorrow is not urgent. They are best dealt as a group as insight, so you can see the big picture.
  (c) No. The color in alert has a timeline as alert is reactive by nature. Time has started. The color in KPI is for proactive. They are not related.
  Applied 2026-11-08: alerts-and-insights (Alert vs insight, Criticality, Traps).

### Q112 · Part 1 > Configuration Management > Review List · Facts to update for VCF 9.1
- Files: [Cluster configuration review: HA, DRS, DPM and cluster variants](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/configuration/cluster-configuration-review.md) (section DRS); [Storage configuration review: datastores, LUNs, NFS, arrays, queue depth](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/configuration/storage-configuration-review.md); [VM configuration review: VMware Tools, hardware, compute and storage settings](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/vm/configuration/vm-configuration-review.md) (sections Storage, VMware Tools).
- Search 1: "Since DRS calculates every five minutes" (DRS runs every minute since vSphere 7; [DRS migration levels](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/configuration/drs-migration-levels.md)).
- Search 2: "Is the usage following design best practice?" (vVols; deprecated in VCF 9.0, Broadcom KB 401070; Protection and Recovery 9.1 is its last release with vVols).
- Search 3: "Ensure that the snapshot is removed within one day" (the SP5 Process daily SOP says older than about 3 days).
- Search 4: "refer to KB 340" (VMware Tools benefits; KB number under Broadcom to confirm).
- Question: confirm (1) every minute; (2) keep vVol checks for existing estates, with the deprecation stated; (3) one day or three days; (4) the KB number.
- Written as now: every minute; vVols deprecated; one day in the VM review; KB 340 as cited.
- Answer: 1. Every minute 2. Yes 3. One day 4. Article 315382
- Applied 2026-11-08: vm-configuration-review (KB 315382, snapshot one day), proactive-operations (daily SOP: one day), review notes in the cluster and storage reviews.

### Q093 · Part 1 > Your Private Cloud · Book corrections for the next edition
- Files: none; the knowledge base already uses current names.
- Search 1: "something you can implement with the current version of Aria products" (now VCF Operations).
- Search 2: "Salesforce, VMware Skyline, Microsoft Office 365" (Skyline status under Broadcom to check).
- Search 3: "Typically, Windows 10 + End-User applications" (Windows 10 support ended October 2025).
- Search 4: "VMware Horizon Cloud, Microsoft Windows Cloud are cloud examples" (Horizon is now Omnissa; Microsoft's product is Windows 365).
- Search 5: "This is not so obvious as it’s the only product in this category." (Nutanix Cloud Platform and Azure Local are in the same category.)
- Search 6: "The creates a bigger problem" (typo: This).
- Question: confirm each for the next edition; (5) is a claim the knowledge base does not repeat.
- Written as now: not in the knowledge base.
- Answer (author, 2026-11-08, on Q107): the book edition does not matter to Agent E2; what matters is the knowledge. Closed without review: the knowledge base already holds the corrected facts and current names.

### Q107 · Part 1 > Your Private Cloud (Service Level Agreement to SP5 Framework: Process) · Book corrections for the next edition
- Files: none beyond those named; the knowledge base already uses the corrected wording.
- Search 1: "because it is charged at 200% more" (2x price is 100% more).
- Search 2: "It looks operationally visible" (viable).
- Search 3: "It took me years to vrealize the mistake"; "you vrealize that there are 3 sides of health" (realize, twice).
- Search 4: "Your ticket is also directly answered by Level 3" vs "Gold bypasses the first level help desk" (Level 2 in the service table).
- Search 5: "We covered both in-depth in Part 1 of the book" (this is Part 1).
- Search 6: "There are 3 techniques we can apply" (4 listed).
- Search 7: "Happy to discuss my documented analysis ." (stray space; the link target is missing).
- Search 8: "Buying 64 cores maximizes your vSphere license" (per-core licensing, Q099 d).
- Image text: "Aria Operations for Logs" in the Not Healthy diagram (now VCF Operations for logs); the RCA screenshot is VMware Log Insight from 2016.
- Search 9: "Since storage IO control configuration is not based on latency" (Storage I/O Control deprecated in VCF 9, Q080).
- Question: confirm each for the next edition.
- Written as now: corrected wording in the knowledge base.

### Q113 · Part 1 > Configuration Management · Book corrections for the next edition
- Files: none beyond those named; the knowledge base uses the corrected wording.
- Search 1: "You can categorizes check into 4" (two bullets follow; the four are value, consistency, compatibility, variance).
- Search 2: "You have 1 ESXi host while providing higher redundancy" (you save 1 host: 21 vs 20).
- Search 3: "Is the HBA configured for high availability?" under Network Related (NIC, not HBA).
- Search 4: "both NSX Controller and Manager" (the controller is part of the NSX Manager cluster since NSX-T).
- Search 5: "Use Log Insight to parse Windows events" (now VCF Operations for logs).
- Search 6: "addiitonal", "combile", "issueing", "imaging both VMs" (typos).
- Question: confirm each for the next edition.
- Written as now: corrected wording.
- Answer (author, 2026-11-08, on Q107): the book edition does not matter to Agent E2; what matters is the knowledge. Closed without review: the knowledge base already holds the corrected facts and current names.

### Q104 · Part 1 > SP5 Framework > Troubleshoot; SP5 Framework: Process · Three orders of checks
- Files: [Monitoring vs troubleshooting, root cause analysis and validating a log alert](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/monitoring-vs-troubleshooting.md) (section Troubleshooting); [Proactive operations: dual track, daily cadence, NOC screens and the VM life cycle](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/proactive-operations.md) (section Dual track); [Users say the VM is slow: triage](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/performance/troubleshooting/vm-slow-triage.md). Related: Q060.
- Search: image text only (not searchable): "4 possible areas. Check in this order: Contention, Configuration, Availability, Utilization"; reactive track "Configuration Issue? Availability Issue? Known Bugs? Consumption Issue?".
- Question: the Not Healthy diagram starts with contention; the reactive track starts with configuration and adds known bugs; the VM slow triage flow (draft) has no configuration or known-bug step. (a) Is the reactive track the order after a complaint, and Not Healthy the order after a health check? (b) Should vm-slow-triage add configuration (version incompatibility) and known bugs after contention?
- Written as now: each order in its file; vm-slow-triage unchanged.
- Answer: There is an overall daily health check runs each morning so VMware Admin can review. It should start with Availability then performance then security. Configuration issue can cause these 3 so they are checked as a drill down. Known bugs are typically caused by configuration issue, such as older version or incompatible settings. Contention is part of performance as it's the primary metric type for performance management. Performance flow such as VM slow triage should always check configuration.
  Reactive is after an alert, an incident (outage, breached), or human complain. Proactive focuses on insight, as system has not detected a known problem. Typically it's anomaly detection. While a monitoring system can detect anomaly mathematically it results in false positives as it lacks real world business context. What is abnormal can mean normal and vice versa.
- Applied 2026-11-08: monitoring-vs-troubleshooting (section Troubleshooting), proactive-operations (Dual track, Day-to-day order), vm-slow-triage (new step 5, Configuration), the three health checks (configuration step as drill-down), KNOWLEDGE-ENGINEERING.md section 10, both flow templates.

### Q083 · Part 1 > Noisy Neighbour > Network · Author's network limit and reservation
- Files: [Noisy neighbour: limit, reservation and share per resource](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/noisy-neighbour.md) (section Network).
- Search 1: "I think it should be 8 Gb/s."
- Search 2: "consider setting 100 Mb/s per VM"
- Question: these are the only network numbers per VM. 8 Gb/s × 25 VMs = 200 Gb on a 40 Gb host: the limit stops one villain, not many at once. Is 8 Gb/s a cap for one VM's peak and 100 Mb/s a floor? Should they go in the capacity threshold file as rules?
- Written as now: in the text, not in the threshold files.
- Answer: book was wrong. I do not encourage both VM limit and VM reservation as it complicates operations, especially in dynamic and large scale environment.

### Q084 · Knowledge base · ESXi CPU Demand: sum of VMs or not
- Files: [knowledge/vsphere/foundations/provider-consumer.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/provider-consumer.md) (sections ESXi CPU Demand, Provider metric types); [knowledge/glossary.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/glossary.md) (Confusable pairs, ESXi CPU Demand vs Usage).
- Search (Part 3): "Not the sum of all VM worlds + VMkernel worlds"
- Question: found while checking this chapter. One file says ESXi CPU Demand is not a sum of consumers, with a trap. The same file, in Provider metric types, gives it as a sum-of-consumer example. The glossary says it is the sum over the VMs. Which is right? Claude will make the three agree.
- Written as now: contradictory.
- Answer: In my Part 1 book, it stated that "If a host has no VM, Demand will likely show flat 0. Usage will not show 0 as it includes the kernel" . It was followed by a screenshot. I can't figure out the image in the images directory so I added one called esxi-cpu-demand-usage-without-vm.png. If you have the same thing, ignore it.

### Q085 · Follow-up to Q070 · Does the hypervisor count a full VMXNET3 receive ring
- Files: [VM Network Packets Dropped](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/network/metrics/virtual-motherboard/packets-dropped.md) (sections Known causes, Traps).
- Search: not from the book. Broadcom KB 1010071 (Claude's own knowledge, not fetched): esxtop shows dropped receive packets at the virtual switch port when the guest does not empty its receive ring fast enough; the fix is a larger ring in the Guest OS.
- Question: your answer says the ring-buffer drop is not visible to the hypervisor. As Claude reads it, the guest never receives the packet, so the drop is counted at the VM's port: VM Network Receive Packets Dropped in vCenter, %DRPRX in esxtop. Visible to the hypervisor, but caused and fixed in the guest. Your conclusion holds either way: outside the IaaS SLA, and receive drops are already left out of it. Which is right for the reason: (a) not visible, or (b) visible but not controllable?
- Written as now: guest-os layer, outside the IaaS SLA; the visibility claim left out.
- Answer: (b), visible but not controllable. The author's document Packet Lifecycle and Metric Accounting in Virtualized Networks (2026-11-07): ESXi counts the drop at the dvPort and the VM (%DRPRX, net.droppedRx); VMXNET3 also shares it with the guest. Applied in [Packet drop accounting: which layer counts a dropped packet](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/network/concepts/packet-drop-accounting.md).

### Q081 · Part 1 > Noisy Neighbour > Network · Host pool or uplink pool
- Files: [Noisy neighbour: limit, reservation and share per resource](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/noisy-neighbour.md) (section Network).
- Search 1: "Now, a single villain VM can hit 10 Gb."
- Search 2: "sustaining 5 Gb over 300 seconds period"
- Search 3: "The share should be larger for production VM network and development VM network."
- Question: (a) The calculation pools 2 × 25 Gb per host. With the default teaming (route based on originating virtual port) each vNIC uses one uplink. A 10 Gb villain fills 10 of one 25 Gb uplink and hurts only the VMs on that uplink. Compute per uplink? (b) The villain is 10 Gb in the calculation, 5 Gb sustained in the example: the 5-minute average hides the 10 Gb 20-second peak (the Interval rule)? (c) Read the share sentence as "larger for production VM traffic than development"?
- Written as now: per host, both figures, (c) as read.
- Answer: (a) Not per uplink, per group of uplinks assigned to the switch. With Load Based Teaming, the distributed switch tests the uplinks every 30 seconds, and if their load exceeds 75 percent of usage, the port ID of the virtual machine or vmkernel port with the highest I/O is moved to a different uplink. (b) my book was wrong. It should be sustaining 10 Gbps over 300 seconds period. (c) No. The main issue is the VM traffic is given a default share of 100 as a group, but each VMkernel traffic is given their own share. So the VM traffic is outnumbered. See the shares in this image https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/network/images/distributed-switch-network-share-allocation-by-traffic-type.png showing VM is 100 while VMkernel is up to 475 shares.

### Q082 · Part 1 > Noisy Neighbour > Memory and Solution · Gold 1:1 with memory tiering
- Files: [Noisy neighbour: limit, reservation and share per resource](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/noisy-neighbour.md) (sections Memory, Avoiding it); [knowledge/vsphere/technology/memory/concepts/memory-tiering.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/memory-tiering.md).
- Search 1: "Per-VM reservation becomes irrelevant when the entire cluster does not overcommit."
- Search 2: the table row Gold, overcommit "1 : 1", under "the following shows the SLA for memory"
- Question: vSphere 9 memory tiering adds NVMe memory beyond DRAM. For Gold 1:1: (a) is the ratio against DRAM only, so a Gold host has no tier, or against DRAM plus tier? (b) Does VM memory contention count time on pages in the NVMe tier? If not, Gold can read 0% while pages are in NVMe.
- Written as now: the book's table; no tiering note.
- Answer: (a) overcommit ratio for memory is only against DRAM portion only, because the whole point of adding an NVMe disk is to avoid overcommit. (b) I'm unsure if the memory latency or memory contention metric is modified to ignore it. I hope it should as NVMe is around 1000x slower, but logically the code that increments LAT_M may not be aware. I cannot confirm if the LAT_M polling logic was explicitly rewritten to inject tiering page faults into the latency aggregate. As a comparison, Linux and KVM do not explicitly report when a VM reads a page from NVMe instead of DIMM. No new KVM-specific counter was added, and existing KVM counters were not modified. vSphere introduces new counters in the vCenter UI for the NVMe tier:
•	Memory type read bandwidth 
•	Memory type read latency 
•	Memory type write bandwidth 
•	Memory type write latency
The consumed metric reflects the combined usage of both the DRAM and NVMe tiers. Because the VMkernel tiering algorithm explicitly tracks physical DRAM (Tier 0) and initiates migration to Tier 1 when Tier 0 consumption crosses the 80% threshold, total consumed memory can exceed the physical DRAM capacity once cold pages are migrated.

### Q065 · Part 1 > Performance Management > Utilization vs Demand · Absolute or relative performance
- Files: [Performance vs capacity: two readings of the same utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/performance-vs-capacity.md) (section Absolute vs relative); [KPI vs SLA: from complaint-based operations to a contract](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/performance/kpi-vs-sla.md) (section KPI vs SLA, Reference).
- Search 1: "Performance will be absolute (real value), Capacity will be relative"
- Search 2: "It tends to be absolute, as it’s reporting raw metrics"
- Question: the book says performance is absolute. In chat you said relative cluster performance is more meaningful than absolute, because no perfect formula exists. Relative to what: (a) other clusters and the same cluster last week, (b) the class-of-service threshold (a score in %), (c) the share of VMs served well (a count, not milliseconds)? Which sentence should the knowledge base hold?
- Written as now: performance absolute, against total capacity; capacity relative, against usable capacity. The paradigm in your chat message is not written yet.
- Answer:
(a). Performance is relative to other clusters, and relative to itself over time. Think of your stock market index like Nasdaq. The actual amount is basically irrelevant as it's just a combination of number. What you care is the relative movement.
(b) Gold Class Cluster should relatively high higher performance (%) score , lower consumption (%) score, and lower risk (%) score versus Bronze Class Cluster.

Capacity is relative because it's relative to Usable Capacity, not Total Capacity. The real, actual, cluster utilization is lower in reality. But since it's divided over Usable Capacity instead of Total Capacity, the score becomes artificially higher. 

### Q067 · Part 1 > Contention vs Consumption · Points A and B: 100% and queues
- Files: [Performance vs capacity: two readings of the same utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/performance-vs-capacity.md) (sections Contention vs consumption, Four points on the utilization scale).
- Search 1: "rarely happens here as utilization rarely exceeds 100% in real world"
- Search 2: "High utilization does not compromise performance, so long as there is no queue or contention"
- Question: (a) Point A: utilization cannot pass 100% of physical capacity; demand can. Write A as "demand above physical capacity", and add "utilization above physical capacity" to the Words to avoid table? (b) Point B: demand arrives in bursts. At 20-second resolution, a host at 100% CPU Usage almost always shows some VM Ready. Is 100% with 0 contention the best point for throughput (provider view), and acceptable for the VMs only while measured contention stays in the KPI? Or do you hold it as a target?
- Written as now: A worded as demand above physical capacity; B as the most work done.
- Answer: 
(a) Point A is above the physical capacity. Utilization cannot pass 100% of physical capacity as utilization measures reality; demand can exceed, as demand includes unmet demand. So there is no such thing as utilization above physical capacity as that's not possible.
(b) The English word "target" implies something you have yet to achieve. You aim at a target before you hit it. Once the arrow hits the mark, you have achieved or hit the target. KPI is closer to Baseline / Standard Expectation: What you currently or consistently maintain as standard performance, albeit with great effort. In the ideal world, which is not realistic, your ESXi reaches 100% utilization while non VM experience contention. Provider and Consumer have their own KPI metrics. 

### Q074 · Part 1 > KPIs in IaaS · How many SLAs per service; is there a Guest OS SLA
- Files: [KPI vs SLA: from complaint-based operations to a contract](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/performance/kpi-vs-sla.md) (section KPIs in VM as a Service).
- Search 1: "There is only 1 SLA per service."
- Search 2: "What happens inside the Guest OS is not even relevant to the VM SLA."
- Search 3: heading "The 4 SLAs of IaaS"
- Question: (a) One SLA per service, while the earlier section gives 4 SLAs of IaaS and the layer table gives availability, performance and compliance per SLA. Read as one SLA contract per service, holding several SLA metrics? (b) The VM as a Service diagram shows a Guest OS SLA. The table says Guest OS metrics stay out of the IaaS SLA. Does a Guest OS SLA exist only when IT owns Guest OS sizing, and then as a separate SLA?
- Written as now: one SLA per service; Guest OS outside the IaaS SLA.
- Answer:
- (a): Read as one SLA contract per service, holding several SLA metrics
- (b): When central IT Department owns Guest OS, they should provide Guest OS SLA. It should have its own Availability SLA, Performance SLA and Security SLA. These values can be combined with the VM SLA to ease reporting and aggregation.
- Use the word Security SLA, not Compliance SLA. Security is more than Compliance. Compliance management is mostly about comparing settings against secured configuration. Security management covers activity, such as undesirable activity which is potentially a security risk.

### Q075 · Part 1 > KPI | SLA > Differences · KPI timing words
- Files: [KPI vs SLA: from complaint-based operations to a contract](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/performance/kpi-vs-sla.md) (sections Three steps of maturity, KPI vs SLA).
- Search 1: "5-minute window. They are used as the starting point to troubleshoot"
- Search 2: "Based on day (e.g. last 1 hour), which is moving as time passes."
- Search 3: "Customers can track the SLA via self-service portal."
- Question: (a) The KPI is a 5-minute window with 20-second accuracy: computed every 5 minutes from 20-second peaks (Q048)? (b) "Based on day" means a moving window and "based on date" a calendar period? (c) The portal line is in the KPI step, where no SLA exists yet. Is it the KPI the customers track?
- Written as now: (a) and (b) as read; (c) written as "follow the numbers".
- Answer:
- (a) The KPI is a 5-minute window with 20-second accuracy: computed every 5 minutes from 20-second peaks? Yes.
- (b) KPI is based on day, not date. It's rolling continuously, like live operations. SLA is based on calendar date.
- (c) In the absence of SLA, yes, both application team and infrastructure team tracks KPI. SLA requires far more advanced cloud maturity model.

### Q076 · Part 1 > KPI step and Noisy Neighbour > Solution · How the SLA is computed; 99.99% at 5 minutes
- Files: [KPI vs SLA: from complaint-based operations to a contract](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/performance/kpi-vs-sla.md); [Noisy neighbour: limit, reservation and share per resource](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/noisy-neighbour.md) (memory class table); [knowledge/vcf-operations/kpis/cluster-sla-sli.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/kpis/cluster-sla-sli.md).
- Search 1: "SLA = 1 month average of SLI of that specific month."
- Search 2: "VM contention is <1% for 99.99% of the time in the entire month"
- Question: (a) Is the SLA the mean of the SLI values, or the share of 5-minute intervals that pass the threshold? They differ: one bad hour at 50% contention averages out in a mean, but fails 12 intervals. (b) A 30-day month has 8,640 five-minute intervals. One failed interval gives 99.988%. So 99.99% allows 0 failures, the same count as Gold's 100%; only the threshold differs (0% vs below 1%). Did you mean 99.9% (8 intervals, 40 minutes)? (c) Bronze has no threshold. Give one?
- Written as now: the table as the book gives it.
- Answer:
- (a) the mean value. The SLI itself is already computed based on pass or fail. So each 5 minute a micro SLA is computed, leading to the final SLA number at the end of the calendar month. SLI = SLA Leading Indicator. It is not Service Level Indicator. That's a trap as people think SLI and SLA are peers as they sound similar.
- (b) the table was wrong. 100% is unrealistic practically. Cost will escalate.
- (c) Recommended threshold for Performance SLA: 99.9% gold, 99.8% silver and 99.6% bronze

### Q077 · Part 1 > Noisy Neighbour > CPU · Shares of a busy vCPU beside an idle one
- Files: [Noisy neighbour: limit, reservation and share per resource](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/noisy-neighbour.md) (section CPU, Share); [knowledge/vsphere/foundations/resource-controls.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/resource-controls.md) (section Default CPU shares).
- Search: "the vCPU 1 of VM 2 does get 2x the share as it does not benefit from idleness of vCPU 2 of VM 2"
- Question: the sentence says both "does get 2x" and "does not benefit". As Claude reads the scheduler: default shares are set per vCPU (1,000 per vCPU at Normal; your screenshot shows 2,000 for a 2-vCPU VM). Under contention each vCPU is charged against its own part, and an idle sibling's part is not handed to the busy vCPU. So vCPU 1 of VM 2 gets the same as vCPU 1 of VM 1, not 2x. Is "does get" a typo for "does not get"? And "shares are per VM, not per vCPU": per VM in configuration, per vCPU in effect?
- Written as now: "the busy vCPU of a 2-vCPU VM does not gain from its idle sibling".
- Answer: that's a Level 400 trap. I think even VMware VCDX will fail for it. A larger VM has more overall CPU shares, the share is shareable among its vCPU. In the following example, the vCPU 1 of VM 2 does get 2x the share as it benefits from idleness of vCPU 2 of VM 2.

### Q078 · Part 1 > Noisy Neighbour > CPU and Disk · Two calculations
- Files: [Noisy neighbour: limit, reservation and share per resource](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/noisy-neighbour.md) (sections CPU, Reservation; Disk, Limit).
- Search 1: "At 8:1 overcommit against physical thread, you cannot guarantee more than 0.25 CPU thread worth of resource"
- Search 2: "then it only takes 5% of the VM population (40 VM in this case) to saturate your storage"
- Question: (a) 8 vCPU per thread gives 0.125 thread per vCPU. 0.25 is right for 8:1 per core (4:1 per thread). Which basis? (b) 5% of 2,000 VMs is 100, not 40; at 1% each, 100 VMs reach 100% of the array. Was it meant as 40 VMs at 2.5% each, or 100?
- Written as now: (a) left out; (b) 100 VMs.
- Answer:
- (a) a core typically has dual threads due to Hyper Threading. I meant to say a 4:1 overcommit against physical thread.
- (b) 2.5% limit per VM, not 1%. 

### Q079 · Part 1 > Solution > Maximum VM Size · Core or thread as the basis
- Files: [Noisy neighbour: limit, reservation and share per resource](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/noisy-neighbour.md) (section Maximum VM size).
- Search 1: "Maximum size = ESXi logical CPU."
- Search 2: "if your ESXi has 48 cores total, then avoid doing 12 vCPU VM"
- Question: the example states overcommit per core ("1 core is assigned to 4 vCPU"); the size table per logical CPU (thread). Mixed: (a) 1:1 allows 96 vCPU on 48 cores and 96 threads, which alone is 2:1 per core; (b) 8:1 gives 0.125 × 96 = 12 vCPU, and the same row says avoid 12 on 48 cores, keep 4-6; (c) 4:1 gives 24 vCPU, called a whole socket, which is one socket's cores, not its threads. Should the table state overcommit and size per physical core? Then 1:1 → 48, 2:1 → 24 (19 with headroom), 4:1 → 12, 8:1 → 6.
- Written as now: the table as the book gives it, flagged.
- Answer: the book is wrong as the overcommit was based on core, not thread. It should be based on CPU physical thread. So 8:1 on a thread means 4:1 on the core if the core has dual threads. 

### Q080 · Part 1 > Noisy Neighbour > Storage I/O Control · Deprecated in VCF 9
- Files: [Noisy neighbour: limit, reservation and share per resource](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/noisy-neighbour.md) (sections Disk, Storage I/O Control).
- Search: "SIOC provides 2 choices for congestion threshold"
- Source: vSphere 9.1 documentation, Manage Storage I/O Resources with vSphere (p. 1886): "With VCF 9.0, vSphere Storage I/O Control Components are deprecated." The datastore performance charts still list SIOC Normalized Latency and Aggregate IOPs.
- Question: (a) In 9.1, should the knowledge base mark SIOC as deprecated and keep only the per-disk limit and shares? Or does your field practice still enable it? (b) "There is no reservation for VM Disk." From vSphere 6.5, SIOC policy components also had an IOPS reservation, now deprecated with them (Claude's own knowledge). Keep the sentence as "none in the VM disk settings"?
- Written as now: SIOC as the book gives it; the deprecation in review notes only.
- Answer:
- (a) for product deprecation, follows the official manual as the book gets outdated. We can't practice what is officially deprecated.
- (b) Yes, keep as none. Do not include deprecated feature.

### Q066 · Part 1 > Contention vs Consumption · Point C: worst performance at 0% utilization
- Files: [Performance vs capacity: two readings of the same utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/performance-vs-capacity.md) (section Four points on the utilization scale).
- Search: "Worst performance actually happens when utilization = 0% as nothing gets done"
- Question: 0% utilization with 0 demand is an idle VM: no contention, nothing to serve. Only 0% with demand above 0 is bad: a VM frozen by a storage pause, as in your antivirus story. Is the rule "performance = demand served / demand", so that utilization alone cannot tell good from bad at either end?
- Written as now: "C, 0% while there is demand" (Claude's wording).
- Answer: Yes, utilization alone does not mean anything. 0% can be bad, 100% can be good. Hence my book said utilization is not something you manage. It's just an input, and one of the inputs to 2 things you care, which is performance and capacity. Utilization is used differently in capacity and performance. 

### Q068 · Part 1 > Utilization vs Demand · Highest host utilization in cluster performance
- Files: [Performance vs capacity: two readings of the same utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/performance-vs-capacity.md) (section Cluster: performance vs capacity); [knowledge/vcf-operations/kpis/cluster-performance.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/kpis/cluster-performance.md).
- Search 1: "you want to take the highest among the host as your primary counter for cluster utilization"
- Search 2: "Utilization is for troubleshooting, not monitoring." (table image, Cluster Performance column)
- Question: for cluster performance, the same chapter says utilization is for troubleshooting only, and the cluster KPI holds only the contention of running VMs. Where does the highest-host utilization belong: (a) a performance monitoring metric, (b) the first troubleshooting drill-down after the cluster KPI drops, (c) a capacity-risk early warning?
- Written as now: both statements, unreconciled.
- Answer: highest-host utilization belong cluster risk score. See https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/cluster-risk.md and https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/formula/cluster-risk.png. I thought I gave you these 2 already?
- BTW, typically risk hits both capacity and performance, as capacity and performance are 2 sides of the same coin. 
- I think you hallucinated here. I'm not able to find anything around "you want to take the highest among the host as your primary counter for cluster utilization" in the 2 files you refer. In future, cite something I can search.

On the file https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/kpis/cluster-performance.md. Why does vCommunity have to be part of the page title? What's the relevant to the local LLM? 
  

### Q069 · Part 1 > Pattern Difference · Where the cliff starts
- Files: [Performance vs capacity: two readings of the same utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/performance-vs-capacity.md) (section Pattern difference).
- Search: "You can’t forecast performance using capacity"
- Question: the chart marks the drop at "Overcommit >1". The noisy-neighbour example runs 4:1 vCPU to core with no cliff. Is the cliff where demand passes supply on a host (demand overcommit), not where the allocation ratio passes 1? And since each host is its own pool, does it start on the hottest host, before the cluster average reaches 100%?
- Written as now: "falls steeply once demand passes what the hosts supply".
- Answer: Is the cliff where the allocation ratio passes 1. And since each host is its own pool, does it start on the hottest host, before the cluster average reaches 100%? Yes, although in theory DRS is supposed to balance all the hosts. There is no such thing demand overcommit as you can only overcommit the allocation. Demand, Usage, Utilization, are not something you can control. 

### Q070 · Part 1 > IaaS Metric Types · Layer of the driver metrics
- Files: [Business, application and IaaS: layers, lost context and metric types](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/realms-and-layers.md) (section Consumer and provider metric types); [knowledge/vsphere/technology/network/metrics/virtual-motherboard/packets-dropped.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/network/metrics/virtual-motherboard/packets-dropped.md) (VMXNET3 buffer drops).
- Search: "One at the Windows/Linux layer, and one at the driver layer (e.g. PVSCSI, vmxnet)"
- Question: the book puts PVSCSI and vmxnet metrics in the Guest OS. The repository rule places a metric by the layer that produces it. The driver runs in the guest kernel, but it is VMware's virtual device. Is a VMXNET3 ring-buffer drop (a) guest-os layer, outside the IaaS SLA, or (b) virtual-motherboard layer, inside it? This decides the folder and who fixes it.
- Written as now: VMXNET3 drops sit in the VM (virtual-motherboard) file.
- Answer: VMXNET3 ring-buffer drop is a guest-os layer, outside the IaaS SLA as it's not visible to the hypervisor. You don't put SLA on something you cannot see, let alone control. The one covered by SLA is the vNIC as seen by the hypervisor. 

### Q071 · Part 1 > The 3 Realms · One word, two meanings: realm
- Files: [Business, application and IaaS: layers, lost context and metric types](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/sp5-framework/realms-and-layers.md); [knowledge/vsphere/foundations/vm-vs-guest-os.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/vm-vs-guest-os.md) (VM vs Guest OS: two realms); [knowledge/operations-management/performance/performance-kpi-design.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/performance/performance-kpi-design.md) ("one per realm").
- Search: "In the big picture, there are 3 realms of IT in business"
- Question: Part 1 uses realm for business, application and IaaS. Part 3 and the knowledge base use realm for VM and Guest OS. One word per concept. Keep realm for the 3 of Part 1 and call VM and Guest OS layers? Or the reverse?
- Written as now: both meanings.
- Answer: realm in this case means world with a boundary. It's not an IT operations management jargon. So use for both.

### Q073 · Part 1 > KPI | SLA > Differences · One KPI or two for VM and Guest OS
- Files: [KPI vs SLA: from complaint-based operations to a contract](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/performance/kpi-vs-sla.md) (section KPI vs SLA, Scope); [knowledge/operations-management/performance/performance-kpi-design.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/performance/performance-kpi-design.md) (section Two KPIs, not one).
- Search 1: "they are 1 logical entity due to 1:1 permanent relationship, hence they are combined in 1 KPI number"
- Search 2 (Part 3): "VM Performance (%) and Guest OS Performance (%)"
- Question: Part 1 combines VM and Guest OS in one KPI. Part 3, the KPIs in VCF Operations and the Part 1 diagram (Guest OS KPI, VM KPI) keep two. Is Part 1's sentence older? The knowledge base would then state: two KPIs, one logical entity, read together.
- Written as now: both, flagged.
- Answer: Yes, Part 1 is outdated. In operations, we may refer to it at VM GOS KPI, using average of the 2 as from the perspective of application team, these 2 objects are the same thing.

### Q045 · Chapter 3 Memory > VM · Swapped formula in the vSphere 9.1 documentation
- Files: [VM Memory Swapped](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/virtual-motherboard/swapped.md)
- Search: "This is why Swapped is not Swapped In – Swapped Out"
- Question: the vSphere 9.1 documentation (Virtual Machines > Memory (MB), p. 2103) defines VM Swapped = swapout – swapin, and adds that vMotion can make Swapped larger than swapout – swapin. Is the documentation wrong, or does its formula hold for cumulative counters (total swapped out minus total swapped in) while the book means the rates?
- Written as now: Swapped is not Swap in - Swap out: both run in parallel on different pages. Related to Q019 (host Swap Consumed).
- Answer: The vSphere 9.1 documentation is wrong. My book is correct. However, add  that vMotion can make Swapped larger than swapout – swapin if the VM comes with its memory already swapped.
BTW, the page is 2105, not 2103.
- Done 2026-11-06: VM Memory Swapped: vMotion line added; documentation formula recorded as wrong.

### Q046 · Provider Objects > esxtop · HTQ and DTYP still in the 9.1 documentation
- Files: [esxtop CPU, power and interrupt counters](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/tools/esxtop/cpu.md), [esxtop network counters](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/tools/esxtop/network.md)
- Search 1: "The column HTQ is no longer shown in ESXi 7.0"
- Search 2: "does not seem to be available anymore"
- Question: the vSphere 9.1 documentation still lists HTQ (CPU panel) and DTYP (network panel). Do they show on an ESXi 9.1 host?
- Written as now: both described as no longer shown, per the book.
- Answer: both no longer shown. My book is correct. Add this as a mistake in the manual.
- Done 2026-11-06: esxtop CPU and network files state HTQ and DTYP are not shown on ESXi 9.1 and the documentation is out of date.

### Q047 · The World of Metrics > Resource management · Untouched memory reservation
- Files: [Resource controls: reservation, limit, shares, entitlement](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/resource-controls.md)
- Search: "since ESXi has reserved the space, it is not available to other VMs"
- Question: the vSphere 9.1 documentation (vSphere Resource Management > Virtual Machine Memory, pp. 1833-1834) says that until a VM has touched all memory within its reservation, the VMkernel can allocate the untouched part to other VMs; only touched reserved memory is kept, even when idle. Does the book statement mean admission control (the reservation cannot be promised to another VM), while the physical pages can still be used by others until touched?
- Written as now: Consumed jumps to the reservation at power-on; the reserved space is not available to other VMs. The existing correction says RAM is backed on first use, then stays locked.
- Answer: Consumed does not jump to the reservation at power-on. Until a VM has touched all memory within its reservation, the VMkernel can allocate the untouched part to other VMs; only touched reserved memory is kept, even when idle. Correct my book.
- Done 2026-11-06: Resource controls (table and corrections) and VM Memory Consumed: Consumed does not jump to the reservation; untouched reserved memory can go to other VMs.

### Q048 · Thresholds · Interval and instance reading of every band
- Files: band tables in [VM Performance (%) (VCF Operations KPI)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/vm/kpis/vm-performance.md), [Cluster Performance (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/kpis/cluster-performance.md), [Cluster Consumption (%) (VCF Operations KPI)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-consumption.md), [Cluster Risk (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-risk.md), [Cluster SLA and SLI](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/kpis/cluster-sla-sli.md), [Guest OS Performance (%) (VCF Operations KPI)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/system/metrics/guest-os-performance.md); rows in [knowledge/catalog/thresholds-performance.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-performance.yaml) and [thresholds-capacity.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-capacity.yaml) (fields `interval`, `instance`).
- Search: not from the book. Follows the rule added to [Thresholds and interpretation](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/foundations/thresholds.md) (Interval rule, Instance rule).
- Question: for each band row, which sample interval was it set on (20-second peak, 5-minute, 1-day), and which reading (worst instance, object aggregate, percentile of objects)? Most rows say "peak" or "worst" but not the interval; utilization rows say neither.
- Written as now: interval and instance stated only where the row name says it (for example "Peak CPU Ready among any vCPU"); Compressed + Swapped at 5 minutes and Memory Contention at 20 seconds (Q026).
- Answer: In VCF Operations, when the metric name has the word peak, that means it's reporting the highest 20-second-average within the 300-second reporting period. There are 15 data points within each 5 minute, each is a 20-second average. It's taking the highest among these 15 instance. The metrics at VM level are:
Peak CPU Queue within collection cycle
Peak CPU Context Switch within collection cycle
Peak Guest OS Page-out Rate within collection cycle
Peak Disk Queue within collection cycle
Peak vCPU Ready within collection cycle
Peak vCPU Co-Stop within collection cycle
Peak Memory Contention within collection cycle
Peak Latency within collection cycle
Peak Usage Rate within collection cycle
Peak Network Packets/sec within collection cycle
Peak Transmitted Packet Dropped within collection cycle
All the KPI and SLI are always by 5 minute. SLA is a lagging indicator, reported at the end of the month for the whole month. KPI, SLA, SLI are covered in Part 1 of my book. These are not vSphere metrics. They are VCF Operations metrics.
- Done 2026-11-06: intervals set in both threshold files (peak metrics 20s, other KPI and SLI rows 5m); peak and reporting periods added to the 20-second peak metrics file.

### Q049 · vCenter API counters · clusterServices.cpufairness and memfairness (low priority)
- Files: [knowledge/catalog/vcenter-api-counters.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/vcenter-api-counters.yaml) (HostSystem rows); no knowledge file yet.
- Search: not from the book. vCenter 9.1.0 API summaries: cpufairness "Fairness of distributed CPU resource allocation"; memfairness "Aggregate available memory resources of all the hosts within a cluster" (looks copied from another counter).
- Question: what do the two host counters measure, and are they worth documenting for operations?
- Written as now: listed in the catalog only, no knowledge file.
- Answer: not worth documenting. They are internal counter. The Cluster Risk (%) metric in https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/c1c954d0fb284bb813fded0aeb4ebd299897edd2/docs/reference/metrics/cluster-risk.md is more applicable to VMware admin.
- Closed 2026-11-06: not documented (internal counters).

### Q050 · vCenter API counters · clusterServices.effectivecpu and effectivemem vs totalmhz and totalmb (low priority)
- Files: [knowledge/catalog/vcenter-api-counters.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/vcenter-api-counters.yaml) (ClusterComputeResource rows); candidate: [Capacity model: total, usable, buffer, projection](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/capacity-model.md).
- Search: not from the book. vCenter 9.1.0 API summaries: effectivecpu "Total available CPU resources of all hosts within a cluster"; effectivemem "Total amount of machine memory of all hosts in the cluster that is available for use for virtual machine memory and overhead".
- Question: Claude's own knowledge (the API's cluster summary) says effective capacity excludes hosts in maintenance mode or not responding, and virtualization overhead. Is that right, and should the knowledge base prefer it over totalmhz and totalmb for usable capacity?
- Written as now: listed in the catalog only.
- Answer: This is a good example of why jargon confuses people. In capacity, we have Total and Usable. Total is the raw and physical capacity. It typically does not change and remain static. Usable capacity  = Total - availability buffer - capacity buffer - overhead. I'm unsure if effective maps to total or usable. Anyway, this is low priority as there is no such word as Effective in the vCenter UI. The API is not fully documented, so focus on what the UI shows.
- Closed 2026-11-06: not documented (API only, not in the UI); Total vs Usable stays in the capacity model.

### Q051 · vCenter API counters · clusterServices.failover
- Files: [Admission control, expandable reservations and cluster state](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/concepts/admission-control-and-cluster-state.md).
- Search: not from the book. vCenter 9.1.0 API summary: "vSphere HA number of failures that can be tolerated".
- Question: how does the value behave under each HA admission control policy (slot, percentage of cluster resources, dedicated failover hosts, disabled)? Any trap in reading it?
- Written as now: the counter, its level and its summary; behaviour per policy left open.
- Answer: The trap comes when the hosts in the cluster is not identical. Regarding the counter, ignore it for now as it's low priority item.
- Done 2026-11-06: trap of non-identical hosts added to the admission control file; the counter itself left as low priority.

### Q052 · vCenter API counters · vmop counters: cumulative or per interval (low priority)
- Files: [Cluster VM operations event counts](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/metrics/vm-operations.md).
- Search: "Cumulative since the cluster was created"
- Question: vCenter stores the 20 vmop counters with rollup latest and stat type absolute, on the cluster and the datacenter. Your hypothesis: vCenter accumulates them while VCF Operations shows a rate. Confirm? Do the vCenter counts ever reset (vCenter restart, cluster re-creation)?
- Written as now: cumulative since cluster creation (book); VCF Operations converts them to rates (book).
- Answer: the counter is cumulative since the object creation. vCenter reset does not impact it. I'm unsure of re-creation but ignore it as we don't re-create cluster.
- Done 2026-11-06: VM operations counts are cumulative since object creation, not reset by a vCenter restart.

### Q057 · Benchmark · [Memory reservation vs CPU reservation](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-07-reservation-cpu-vs-memory.md): check with a vCenter CPU screenshot
- Files: [Memory reservation vs CPU reservation](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-07-reservation-cpu-vs-memory.md) (section Expected key points, CPU bullet); [Resource controls: reservation, limit, shares, entitlement](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/resource-controls.md) (section Reservation: CPU vs memory).
- Search: not from the book. The question comes from the book section The World of Metrics > Resource management (`source_path` of the question).
- Question: please validate the CPU key point with a screenshot of the vCenter UI: a VM with a 4 GHz CPU reservation, powered on and sitting at the BIOS screen. Do Run, Used, Demand and Usage stay at or near 0? The screenshot can then become the question's attachment (input type screenshot).
- Written as now: CPU reservation is on demand; the CPU counters stay at or near 0 while the VM sits at the BIOS screen.
- Answer: I was wrong. Memory is also on demand. So both are. I verified on a live vCenter.
- Done 2026-11-06: question L3-07 key and the resource controls file: memory reservation is also on demand.

### Q058 · Benchmark · Synthetic share and review of L4-14 to L4-50
- Files: https://github.com/e1-rahabok/agent-e2/tree/main/benchmark/questions (L4-14 to L4-50); [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md) (section 10, synthetic cap; section 12, status).
- Search: not from the book.
- Context: the Level 400 allocation (37 questions) is now drafted by Claude from the knowledge base. Synthetic questions are 63 of 90 (70%), against the cap of about 30% in section 10.
- Question:
  1. Keep the cap? If yes, which synthetic questions should be replaced by book, quiz or real-ticket questions, or should the cap rise?
  2. Review the 37: answer letters and key points per question (each `## Expected key points`), and the `## Input to supply` of the 24 awaiting-input questions (0066 to 0089).
  3. [Which VMs to reclaim memory from](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-39-memory-reclaim-from-300-vms.md), [Which datastores run out of space first](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-40-datastores-running-out-of-space.md), [Bad network packets: find the host and the cause](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-48-bad-packets-which-host.md), [Disk latency peak 40 times the average](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-49-disk-latency-peak-vs-average.md): the key names rows of the table you supply. Record the names in each question's Notes.
- Written as now: all 37 are `origin: synthetic`, status draft or awaiting-input; none counts until approved.
- Answer: no need to keep cap as I'm reviewing every question one by one. What is important is the allocation and distribution. The source (book versus Claude) is less important.
- Done 2026-11-06: synthetic cap removed from benchmark/design.md (sections 10 and 12).


### Q023 · Chapter 4 Storage > VM · Disk metric scope
- Files: [VM Disk (device level)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/metrics/virtual-motherboard/disk.md)
- Search: "if the value is per VM or per disk"
- Question: is the VM Disk (device-level) metric value for this VM only, or for the whole device shared by many VMs?
- Written as now: associated with the VM, flagged as unsure.
- Answer: it is for the VM, not the whole device or datastore.
- Done 2026-11-06: [VM Disk (device level)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/metrics/virtual-motherboard/disk.md), section Meaning, states the value is for the VM only.

### Q042 · Quiz > CPU > Q11 Reclamation · Option D, power off frees memory
- Files: [Reclaiming vCPUs from an idle VM](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-06-reclaiming-vcpus-from-an-idle-vm.md); [Why rightsizing matters for VMs](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/rightsizing.md), [Unused and idle vCPUs](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/concepts/idle-and-unused-vcpus.md), [Large VM with low utilization: build the case to downsize](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/health-check/oversized-vm-downsizing.md)
- Search (quiz): "Power off the VM, as this also frees the VM memory"
- Question: key is C,D. Frontier baseline chose C,D in 5 of 5; frontier classic chose C only in 5 of 5, citing that the knowledge base does not make the claim. Should the knowledge base state that powering off an idle VM frees its memory, as part of reclamation?
- Written as now: no file states that powering off an idle VM frees its memory. idle-and-unused-vcpus covers the CPU cost of idle vCPUs only.
- Answer: Yes, the knowledge base should state that powering off an idle VM frees its memory, as the consumed page tends to linger long after the VM has gone idle. The main reason is Windows and Linux tends to hold on to the memory. Powering off is a good best practice to claim this unused memory.
- Done 2026-11-06: [Why rightsizing matters for VMs](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/rightsizing.md), new section Idle VM: power it off, and a trap.

### Q043 · Quiz > Memory > Q2 VM vs Guest OS · Options A and D
- Files: [Relationship between VM and Guest OS memory metrics](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-13-relationship-between-vm-and-guest-os-memory-metrics.md); [Guest OS memory vs VM memory](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/guest-os-vs-vm-memory.md), [Ballooning](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/ballooning.md), [VM Memory Usage](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/virtual-motherboard/usage.md)
- Search 1 (quiz): "Neither layer considers the other"
- Search 2 (quiz): "the hypervisor cannot balloon the VM"
- Question: key is A,B,D,E. Frontier dropped A or D in every run (baseline and agentic B,D,E; classic A,B,E). Are A and D both correct? If yes, which statements should the knowledge base add?
- Written as now: guest-os-vs-vm-memory says neither the VMkernel nor the Guest OS has full visibility into the other (close to A, but not "managed independently"). No file states that ballooning requires VMware Tools running (D).
- Answer: Yes, A and D are correct. The architecture of virtualization in ESXi means Guest OS cannot see the underlying memory. As a result, Windows and Linux completely operate its given memory as if they are on physical server hardware. Unlike a Type 2 hypervisor, which executes as software applications on top of a conventional host operating system, ESXi access the Guest OS via VMware Tools. This is the only channel for ESXi to issue a malloc() request to Windows or Linux. Without this request, ESXi is blind and can swap used memory.
- Done 2026-11-06: [Guest OS memory vs VM memory](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/guest-os-vs-vm-memory.md), section No mapping (A); [Ballooning](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/ballooning.md), section Trigger and requirement and a trap (D).

### Q044 · Chapter 4 Storage > ESXi · Latency thresholds vs vSphere 9.1 documentation
- Files: [ESXi storage latency is high](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/troubleshooting/host-storage-latency.md), [vSphere documentation performance guidance](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/tools/vsphere-client/performance-guidance.md)
- Search 1: "the value should be within 0.5 ms"
- Search 2: "In a healthy environment, it should be well within 5 ms"
- Question: the vSphere 9.1 documentation (vSphere Monitoring and Performance > Solutions for Disk Performance Problems, p. 2121) says kernelLatency best 0-1 ms and a problem above 4 ms; deviceLatency above 15 ms indicates an array problem; queueLatency must be 0. Keep the book values as the knowledge-base thresholds, and the documentation values only as the vendor's published guidance?
- Written as now: diagnosis file uses the book values (KAVG 0.5 ms, DAVG well within 5 ms). The guidance file lists the documentation values, says the 15 ms value comes from spinning-disk arrays, and points to the book values.
- Answer: move all these threshold guidance from scattered over many files into a single small database, so it's quick for the Agent or Harness to check, and easy for human expert to review. You did create the database before. Where is it?
- Done 2026-11-06: all thresholds in one place, [knowledge/catalog/thresholds-performance.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-performance.yaml) and `thresholds-capacity.yaml` (YAML source, loaded into the harness catalog). The book values (KAVG 0.5 ms, DAVG within 5 ms) and the documentation values (kernelLatency above 4 ms, deviceLatency above 15 ms, queueLatency 0) are separate rows, each with its source.


### Q056 · Benchmark · Level of each existing question
- Files: the 28 files in https://github.com/e1-rahabok/agent-e2/tree/main/benchmark/questions (metadata `level`).
- Search: not from the book.
- Question: Claude assigned a draft level to each question (definitions: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 3.2). Which are wrong? None is at Level 100 or 200.
- Written as now:
  - [High CPU Wait](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-01-cpu-wait-includes-idle.md) (judged, text): 300
  - [CPU Latency without contention](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-01-cpu-latency-frequency.md) (judged, text): 400
  - [Hyper-Threading and two vantage points](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-02-hyperthreading-vm-vs-esxi.md) (judged, text): 400
  - [ESXi true utilization from Usage, Core Utilization and Utilization](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-03-esxi-true-utilization-from-usage-core-utilization-and-utilization.md) (deterministic, screenshot): 400
  - [Likely vCPU speed on a busy Hyper-Threaded cluster](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-04-likely-vcpu-speed-on-a-busy-hyper-threaded-cluster.md) (deterministic, text): 400
  - [ESXi CPU capacity: threads, not hertz](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-05-esxi-cpu-capacity-threads-not-hertz.md) (judged, screenshot): 400
  - [Reading an Intel Xeon specification: base, all-core Turbo, TDP](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-02-reading-an-intel-xeon-specification-base-all-core-turbo-tdp.md) (deterministic, screenshot): 300
  - [Which counter to size VM CPU](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-06-which-counter-to-size-vm-cpu.md) (deterministic, text): 400
  - [Counters where a vCPU cannot run at all](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-03-counters-where-a-vcpu-cannot-run-at-all.md) (deterministic, text): 300
  - [Guest OS run queue, context switch, Windows thread states](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-04-guest-os-run-queue-context-switch-windows-thread-states.md) (deterministic, text): 300
  - [CPU reservation behaviour](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-05-cpu-reservation-behaviour.md) (deterministic, text): 300
  - [Utilization 50% and Core Utilization 50%](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-07-utilization-50-and-core-utilization-50.md) (deterministic, text): 400
  - [Reclaiming vCPUs from an idle VM](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-06-reclaiming-vcpus-from-an-idle-vm.md) (deterministic, text): 300
  - [Memory reservation vs CPU reservation](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-07-reservation-cpu-vs-memory.md) (judged, text): 300
  - [VM availability](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-08-vm-availability.md) (judged, text): 300
  - [Provider vs consumer metrics](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-09-provider-consumer-ready-demand.md) (judged, text): 300
  - [What counts as overhead](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-10-overhead-classification.md) (judged, text): 300
  - [VM (virtual motherboard) vs Guest OS metrics](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-08-vm-is-a-virtual-motherboard.md) (deterministic, text): 400
  - [Performance vs capacity view of utilization](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-11-performance-vs-capacity-view-of-utilization.md) (deterministic, text): 300
  - [Memory usage: VM vs ESXi](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-09-usage-vm-vs-esxi.md) (judged, text): 400
  - [Which counter to size VM memory](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-12-which-counter-to-size-vm-memory.md) (deterministic, text): 300
  - [Relationship between VM and Guest OS memory metrics](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-13-relationship-between-vm-and-guest-os-memory-metrics.md) (deterministic, text): 300
  - [Actual vs potential memory contention](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-10-actual-vs-potential-memory-contention.md) (deterministic, text): 400
  - [Memory reservation behaviour](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-11-memory-reservation-behaviour.md) (deterministic, text): 300
  - [Balloon 0 while Swapped and Compressed are not 0](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-12-balloon-0-while-swapped-and-compressed-are-not-0.md) (deterministic, text): 400
  - [Guest queue invisible to the hypervisor](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-13-guest-queue-invisible.md) (judged, text): 400
  - [Setting a disk latency threshold](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-14-disk-latency-threshold.md) (judged, text): 400
  - [Latency and outstanding IO](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-15-latency-and-outstanding-io.md) (deterministic, text): 300
- Answer: Author (2026-11-05): reviewed all. [Memory reservation behaviour](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-11-memory-reservation-behaviour.md) is Level 400, not 300; [Setting a disk latency threshold](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-14-disk-latency-threshold.md) is Level 300, not 400. The others stand.
- Done 2026-11-05: both levels changed; the draft marks removed from all 28 questions.

### Q054 · Benchmark · Allocation of the 100 questions
- Files: https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md, sections 3.1 (tasks), 3.2 (levels), 3.3 (answer types), 3.4 (input types), 3.6 (allocation), 3.7 (coverage).
- Search: not from the book.
- Question: the blueprint is now top down. Are these shares right?
  - Tasks: read a metric 30, troubleshoot 25, decide capacity 20, explain a mechanism 15, judge a setting 10.
  - Levels: 100: 10, 200: 15, 300: 25, 400: 50.
  - Answer types: deterministic 70, judged 30.
  - Input types (questions that include them): text only 60, table at least 15, screenshot at least 25; at least 5 Level 400 questions with a table and a screenshot.
- Written as now: the shares above, as a proposal. Replaces the earlier 60 multiple choice, 20 screenshot, 20 conversation.
- Answer: Author (2026-11-05): agreed; replaces the old proposal.
- Done 2026-11-05: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 3.6 marked decided.

### Q041 · Quiz > CPU > Q8 Reservation · Options A and B
- Files: [CPU reservation behaviour](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-05-cpu-reservation-behaviour.md); [Resource controls: reservation, limit, shares, entitlement](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/resource-controls.md), [ESXi CPU Reserved Capacity](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/reserved-capacity.md), [Overhead: classification, hypervisor overhead and CPU virtualization overhead](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/overhead.md)
- Search 1 (quiz): "Total reservation at ESXi level is capped at the base nominal clock speed"
- Search 2 (quiz): "CPU reservation only comes into play during contention"
- Question: key is A,B,C,D. Frontier classic chose C,D in 5 of 5 runs and rejected A and B. Are A and B correct? If yes, which statements should the knowledge base add?
- Written as now: reservation in MHz/Hertz (supports D); CPU reservation not sticky, memory reservation sticky (supports C). No file states the cap at base nominal clock speed (A) or that the reservation only matters under contention (B).
- Note (2026-11-05): the text written here was about case [ESXi true utilization from Usage, Core Utilization and Utilization](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-03-esxi-true-utilization-from-usage-core-utilization-and-utilization.md) (image links missing). Done: the case and the other two cases with attachments now have an `## Attachments` section with image links. Options A and B are still open.
- Answer: A and B are correct.
- The justification for A was already in the key itself. ESXi CPU has 3 frequency (base or nominal, all core turbo, and single core turbo). Only the base frequency is used by ESXi logic to guarantee a reservation. This is a conservative design.
- The justification for A was already in the key itself. It's written "if there is enough for everyone, reservation is irrelevant. Think of a restaurant. If there is enough seat, does your reservation matter if you do not reserve a specific table?"
- Done 2026-11-05: [Resource controls: reservation, limit, shares, entitlement](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/resource-controls.md) (section Reservation: CPU vs memory) and [ESXi CPU Reserved Capacity](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/reserved-capacity.md) (Meaning, Traps). The second justification line is read as being about B.

### Q033 · MS Windows > CPU > Usage | Utilization | Time · VM CPU Run and Hyper-Threading
- Files: [Windows CPU scheduling and thread states](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/cpu/concepts/windows-cpu-scheduling.md), [VM CPU Run](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/run.md)
- Search 1 (MS Windows table): "Which VM counters can be used when you have no visibility into the Guest"
- Search 2 (Chapter 2, Run | Net Run): "counter not affected by CPU frequency scaling and hyper threading"
- Question: the MS Windows table marks VM CPU Run as Yes in the Hyperthreading column. Chapter 2 says Run is not affected by Hyper-Threading. Which is right?
- Written as now: the table as in the book, marked with the conflict; `run` keeps the Chapter 2 statement.
- Answer: Run and Net Run not affected by hyper threading
- Done 2026-11-05: [Windows CPU scheduling and thread states](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/cpu/concepts/windows-cpu-scheduling.md) table: Run and Net Run marked not affected by Hyper-Threading; Demand marked affected (Q035).

### Q038 · Auto Test > Prompt design · ONLY the knowledge base, or knowledge base first
- Files: [harness/modes.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/modes.py) (SYSTEM_KB, SYSTEM_AGENT); evidence in [benchmark/results/20261103-093742/report.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/results/20261103-093742/report.md), section Analysis.
- Search: not from the book. Finding from the frontier reference run 20261103-093742.
- Question: should the AI answer from the knowledge base only, or use the knowledge base first and its own knowledge where the knowledge base is silent?
- Written as now: prompt says answer using ONLY the knowledge base; if not covered, choose "Not covered by the knowledge base".
- Finding:
  - Frontier model: baseline (no knowledge base) 75%, classic 67%, agentic 67%.
  - The ONLY rule cost 3 questions where the knowledge base is silent: vendor-neutral-general-001 (5 of 5 to 0 of 5), [Reclaiming vCPUs from an idle VM](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-06-reclaiming-vcpus-from-an-idle-vm.md) (5 to 0), [Performance vs capacity view of utilization](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-11-performance-vs-capacity-view-of-utilization.md) (5 to 2).
  - The knowledge base cut the trap rate: 16% to 6-9%.
- Options:
  - Keep ONLY: fewer invented answers; no credit where the knowledge base is silent; every gap must be filled in the knowledge base.
  - Knowledge base first: knowledge base wins on conflict; own knowledge fills gaps; more coverage; more risk of invented answers.
  - Test both in one run and compare.
- Answer: In the auto test, we're testing 3 components as 1 expert (harness + model + knowledge base). So use the knowledge base first and its own knowledge where the knowledge base is silent.
- Done 2026-11-05: [harness/modes.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/modes.py) prompts: knowledge base first, it wins on conflict, own knowledge where it is silent and marked in the reason. The Not covered option is removed from the benchmark; docs updated ([benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), both benchmark READMEs, `ARCHITECTURE.md`).

### Q040 · Quiz > CPU > Q1 ESXi CPU Utilisation · Which counter is ESXi true utilization
- Files: [ESXi true utilization from Usage, Core Utilization and Utilization](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-03-esxi-true-utilization-from-usage-core-utilization-and-utilization.md); [ESXi CPU Core Utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/core-utilization.md), [ESXi CPU Utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/utilization.md), [ESXi CPU Usage](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/usage.md)
- Search 1 (quiz): "It is a balanced reporting"
- Search 2 (quiz): "Plenty of physical threads are idle"
- Question: key is C (Utilization, 40%). All models, frontier included, chose B (Core Utilization, 70%), with and without the knowledge base. Is C right? If yes, which statement should the knowledge base add?
- Written as now: core-utilization says Core Utilization is a capacity metric (ignores frequency). utilization says Utilization suits capacity management. No file says which one is the ESXi true utilization, or why Core Utilization overstates it.
- Answer: I think you got triggered with the word "true". Change it to "Three metrics show three values. What is the ESXi utilization, from capacity management perspective? Hint: capacity is about space, while performance is about speed. Capacity is about quantity, performance is about quality". Review https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/utilization.md and https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/core-utilization.md and update accordingly.
- Done 2026-11-05: case [ESXi true utilization from Usage, Core Utilization and Utilization](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-03-esxi-true-utilization-from-usage-core-utilization-and-utilization.md) prompt and hint reworded as given; [ESXi CPU Utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/utilization.md) (section The capacity reading, traps) and [ESXi CPU Core Utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/core-utilization.md) (not the capacity reading; traps) updated.

### Q055 · Follow-ups to Q027 and Q029
- Files: [VM footprint sizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/vm-footprint-sizing.md) (section CPU), [Guest OS sizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/system/concepts/guest-os-sizing.md) (section Memory).
- Search: not from the book; from your answers to Q027 and Q029.
- Question 1 (Q027): the formula ends with "/ 20000 * vCPU". The sum over all vCPUs divided by 20,000 already gives the footprint in vCPUs (2 vCPUs each fully busy: 40,000 / 20,000 = 2). Is the result meant in vCPUs, so "× vCPU" is not needed, or in % of the VM, so the division is by (20,000 × vCPU)?
- Question 2 (Q029): option 2 has four ranges, 0-75, 75-85, 85-95, 95-100%. The image shows grey, green, yellow, orange and red. Is it grey (waste) below 75, green 75-85, yellow 85-95, red 95-100?
- Written as now: Q027 formula as you wrote it, with this question in review_notes. Q029 boundaries only, no colours.
- Answer to Q1: From my book, which you missed: "The System counter is not available per vCPU. Reason is the underlying physical core that does the IO work on behalf of the VM may be doing it for more than 1 vCPU. There is no way to break it down for each vCPU.". Because of this, I need to sum all the per-vCPU counters one by one, then add CPU System. After that, we divide by 20000 x vCPU. Is it clear?
- Answer to Q2: Grey is the 5th region. Only applicable to Capacity. It's not applicable to Performance as there is no such thing as wastage performance. Grey symbolizes wastage. It's placed below green. For Guest OS Memory, the range is 0 - 75 - 85 - 90 - 95 - 100. Yes, green is 10 point wide. Add in to do to upload Part 1 of my book to complete the capacity and performance management knowledge.
- Done 2026-11-05: [VM footprint sizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/vm-footprint-sizing.md) (divisor 20,000 × vCPU, System reason, example); [Guest OS sizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/system/concepts/guest-os-sizing.md) (ranges 75-85-90-95-100, grey below 75 for capacity only). To-do added: upload Part 1 of the book.

### Q027 · Consumer Objects > Capacity · VM CPU Needed formula
- Files: [VM footprint sizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/vm-footprint-sizing.md)
- Search: "VM CPU Needed = (Used + Overlap + Co-stop + Ready + Other Wait) + System"
- Question: is the whole sum divided by 20,000, or only System? VM-level Used already includes System (Chapter 2 VM, Used formula). Is System counted twice?
- Written as now: formula copied as is, flagged.
- Answer: VM CPU Needed = (Sum of all vCPU (Used + Overlap + Co-stop + Ready + Other Wait) + System ) / 20000 * vCPU
Emphasize that this is a narrow use case, as it's about the footprint of the VM on the underlying ESXi. This is only useful in VM migration to a different ESXi. What's more relevant in the Guest OS (Windows or Linux) capacity sizing.
- Done 2026-11-05: [VM footprint sizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/vm-footprint-sizing.md) (formula grouping, narrow use case, pointer to Guest OS sizing). Follow-up on the unit of the result: Q055.

### Q028 · Consumer Objects > Capacity · Balloon in Guest OS memory sizing
- Files: [Guest OS sizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/system/concepts/guest-os-sizing.md)
- Search: "Exclude balloon"
- Question: the text excludes balloon, but the sizing table marks Ballooned in blue (include) with "The memory was taken by Tools". Include or exclude?
- Written as now: exclude, flagged.
- Answer: include. It is hard to know if the page used by balloon was a free page or not. 
If it’s from free page, then exclude. 
If it’s from non-free page, then include. 
To be conservative, I recommend include.
- Done 2026-11-05: [Guest OS sizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/system/concepts/guest-os-sizing.md), rule changed to Include balloon, with the reason.

### Q029 · Consumer Objects > Capacity · Memory utilization ranges
- Files: [Guest OS sizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/system/concepts/guest-os-sizing.md)
- Search: "The company is wasting money if the utilization falls below 50%"
- Question: the text gives waste below 50% and risk above 75%, which matches bar 1. You recommend bar 2, where green starts near 75%. What are the ranges for bar 2?
- Written as now: bar 2 recommended, no numbers stated.
- Answer: I’d recommend 0 - 75% - 85% – 95% - 100% as Windows and Linux tend to cache memory.
- Done 2026-11-05: [Guest OS sizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/system/concepts/guest-os-sizing.md), option 2 boundaries added. Follow-up on the colour of each range: Q055.

### Q030 · Provider Objects > Performance · vMotion in Cluster Performance (%)
- Files: [Cluster Performance (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/kpis/cluster-performance.md)
- Search 1: "vMotion is not included as it only becomes an issue"
- Search 2: "vMotion is included as it does impact the VM performance"
- Question: is vMotion part of the cluster KPI or not? The threshold table has no vMotion row.
- Written as now: vMotion described as a leading indicator, flagged.
- Answer: vMotion should not be included in actual performance as the metric counts the number of vmotion, not the length of the actual downtime. In a healthy environment, each vMotion down time is below 0.2 second and does not impact the Guest OS. Broadbase infrastructure capabilities like vMotion, NSX Edge, vSAN resync and general infrastructure (e.g. network) should be monitored separately. For example, track the maximum downtime for all vMotion across entire environment as a high downtime is a leading indicator of performance degradation.
- Done 2026-11-05: [Cluster Performance (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/kpis/cluster-performance.md), section vMotion is not part of the KPI; [Cluster Risk (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-risk.md), section Not used.

### Q031 · Provider Objects > Performance · Cluster KPI table vs text
- Files: [Cluster Performance (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/kpis/cluster-performance.md)
- Search 1: "Storage troubleshooting differs to compute troubleshooting" (disk latency listed as not used)
- Search 2: "That’s why it’s given 4x the threshold of zipped + swapped" (balloon thresholds)
- Search 3: "I did not set green = 0"
- Question: the table includes disk latency rows, has no balloon or swapped rows, and sets packet green to 0%. Is the table or the text current?
- Written as now: the table, with text reasons listed and the conflict flagged.
- Answer: both are outdated. The updated information is here https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/formula/cluster-performance.png and https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/cluster-performance.md Update the knowledge accordingly.
Also, update Cluster Risk in the knowledge base from https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/formula/cluster-risk.png and https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/cluster-risk.md
- Done 2026-11-05: [Cluster Performance (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/kpis/cluster-performance.md) and [Cluster Risk (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-risk.md) rewritten from the adapter documentation (thresholds, calculation, DRAM-only memory, scoring, Excluded rows, known limitation, missing data); both threshold images replaced with the current tables; shared scoring rule updated in [Performance KPI design: VM Performance (%) and Guest OS Performance (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/performance/performance-kpi-design.md).

### Q032 · Provider Objects > Other Metrics · Monster VM threshold
- Files: [Cluster Risk (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-risk.md), [vSphere cluster: operations complexity](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/concepts/cluster-operations.md)
- Search 1 (Overview): "If a VM vCPU > 45% of the ESXi count of threads"
- Search 2 (Monster VM): "if a VM vCPU size is > 40% of the ESXi count of threads"
- Search 3 (Cluster Risk): "the VM size needs to be at least half the ESXi"
- Search 4 (recommendation): "Monster VM > 50% of physical core, not thread"
- Question: which CPU threshold defines a monster VM?
- Written as now: the recommendation (above 50% of physical cores); the others flagged.
- Answer: The final and up to date answer at https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/cluster-risk.md#when-a-vm-is-a-monster  Update the
- Done 2026-11-05: [Cluster Risk (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-risk.md), section Monster VM; [vSphere cluster: operations complexity](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/concepts/cluster-operations.md) Monster VM row; [knowledge/catalog/thresholds-performance.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-performance.yaml) and [thresholds-capacity.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-capacity.yaml) rows monster-vm-cpu and monster-vm-memory.

### Q024 · Chapter 5 Network > Architecture · VM and ingress
- Files: [Network layers and observability](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/network/concepts/network-observability.md)
- Search: "That’s why a VM does not have ingress traffic"
- Question: if moving further inside is ingress, traffic arriving at a VM looks like ingress. What does "a VM does not have ingress traffic" mean? That VM metrics use receive/transmit instead?
- Written as now: definitions only; the VM statement is flagged.
- Answer: Diagram is wrong. Correct answer is RX / TX (Receive / Transmit): L1/L2 hardware and driver domain. Used by physical interface cards (NICs), hypervisor VMkernel drivers, and DMA ring buffers. RX measures frame processing at the lowest stack layer regardless of protocol payload.
Ingress / Egress: L3–L7 policy and control plane domain. Used by routing engines, distributed firewalls, and microsegmentation policies. Ingress evaluates stateful rule processing upon crossing a defined logical security or administrative boundary.
Incoming / Outgoing: Operational telemetry domain. Used in application dashboards, capacity planning, and generalized monitoring to describe directional bandwidth utilization without mapping to a specific hardware driver or firewall rule.
Here is a simple mermaid diagram. If you can add to the diagram, that's good.
flowchart LR
    Traffic["Network → VM Interface<br/><b>(100 Packets / 150 KB)</b>"]

    subgraph AbstractionLayers ["Operational Abstraction Layers"]
        direction TB
        L1["<b>L1/L2 Driver Layer</b><br/>RX Count: 100<br/><i>(DMA Ring Buffer)</i>"]
        L2["<b>L3/L7 Policy Layer</b><br/>Ingress Count: 100<br/><i>(Stateful Firewall Rule)</i>"]
        L3["<b>Telemetry Layer</b><br/>Incoming Count: 100<br/><i>(Monitoring Dashboard)</i>"]
    end

    Traffic --> L1
    L1 --> L2
    L2 --> L3

### Q025 · Chapter 5 Network > VM · Dropped packet volume
- Files: [VM Network Packets Dropped](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/network/metrics/virtual-motherboard/packets-dropped.md)
- Search: "1 thousand packets dropped = 1500 MB worth of packets within 300 seconds"
- Question: 1,000 × 1.5 KB = 1.5 MB. Should it be 1 million packets = 1,500 MB, or 1,000 packets = 1.5 MB?
- Written as now: flagged, no number stated.
- Answer: 1.5 MB. Book was wrong.

### Q026 · Consumer Objects > Performance · Compressed + Swapped threshold
- Files: [VM Performance (%) (VCF Operations KPI)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/vm/kpis/vm-performance.md)
- Search: "their threshold is 2x of memory contention"
- Question: the table gives Compressed + Swapped green at 0-0.25%, half of Memory Contention (0-0.5%), not 2x. Which is intended?
- Written as now: the table values, with the conflict flagged.
- Answer: Swapped and Compressed are combined as they are the result of the same action. Together they tell the complete picture. As they may not indicate actual problem, their threshold is higher. However, since we measure at 5 minute sample, while memory contention is measured at 20 second, I adjust the threshold.

### Q019 · Chapter 3 Memory > ESXi · Swap Consumed formula
- Files: [ESXi Memory Swap Used](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/host/swap-used.md)
- Search 1 (ESXi): "I think this is swapped out – swapped in"
- Search 2 (VM): "This is why Swapped is not Swapped In – Swapped Out"
- Question: is host Swap Consumed equal to swapped out minus swapped in?
- Written as now: both statements, flagged.
- Answer: Search 1 is wrong. Search 2 is correct.

### Q021 · Chapter 3 Memory > ESXi · Utilization formula
- Files: [ESXi Memory Utilization (VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/host/utilization.md)
- Search 1: "the sum of running VM Utilization metrics + the kernel reservation"
- Search 2: "Utilization. Machine Demand + ESX System Usage"
- Question: is the kernel part the kernel reservation or ESX System Usage? Are they the same thing?
- Written as now: both forms, flagged. Note: Provider Objects > Capacity says "Memory \\ ESX System Usage (KB)" is the kernel reservation (legacy name). If so, the two forms agree; please confirm.
- Answer: They are the same thing. See my book for Reservation. The metric name is Memory \ ESX System Usage (KB). It is a raw counter from vCenter. Just in case you’re wondering, the name ESX System Usage is a legacy name.

### Q022 · Chapter 4 Storage > Architecture · IP storage read and network direction
- Files: [VM Disk Latency](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/metrics/virtual-motherboard/disk-latency.md)
- Search: "Read and Write are both mapped to Transmit counter"
- Question: for a read, the data returns to ESXi as received traffic. Do reads show mostly as Receive (data) with only the command on Transmit?
- Written as now: both map to Transmit, as in the book.
- Answer: book was wrong. Answer is If you are using IP storage, take note that Read and Write in storage do not map 1:1 to Transmit (Tx) and Receive (Rx) in Networking metrics. This depends on the storage block size (normally 4K or 8K), network packet size (ideally 9000 MTU), and TCP/IP handshakes packets. Get detail from https://docs.google.com/document/d/1E7Or6rsJZ_P1MUZZfL1X3RSXPxhR2lW2fSp3wcaqnGo/edit?usp=sharing and add it accordingly.
- Done 2026-11-04: [IP storage: storage counters vs network counters](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/concepts/ip-storage-network-accounting.md) (from the linked note); disk-latency corrected, with a `corrections` entry until the book is updated.

### Q039 · Auto Test > Golden case vendor-neutral-general-001 · Hyperscaler cost not in the knowledge base
- Files: `benchmark/questions/vendor-neutral/general/general-001-hyperscaler-cost-of-1000-vms.md`
- Search: not from the book.
- Question: add hyperscaler cost content to the knowledge base, or score this case in baseline mode only?
- Written as now: the knowledge base has no cost content. In knowledge-base modes every model chose "Not covered" (frontier: 10 of 10 runs). Baseline frontier: correct 5 of 5.
- Answer: remove the case. Cost and price management is out of scope: the knowledge base is about performance troubleshooting (author, 2026-11-04). Case deleted; its id is not reused.
### Q001 · Chapter 2 CPU > VM · Linux Steal Time
- Files: [VM CPU Overlap](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/overlap.md), [VM CPU Latency](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/latency.md)
- Search 1 (Chapter 1): "Steal Time in Linux only includes CPU Ready"
- Search 2 (CPU > VM > Overlap): "Linux Guest OS tracks this as Stolen time"
- Question: does Linux Steal Time include Ready only, Overlap only, or both?
- Written as now: both statements, flagged.
- Answer: CPU Ready only. Because ESXi accounts for Overlap as active CPU Run time rather than wait time, it bypasses the hypervisor steal-time accumulator. The hypervisor does not report this interrupted time to the guest OS as stolen. The Linux OS Steal Time metric remains completely blind to vCPU Overlap. This ESXi accounting behavior necessitates the VCF Operations Net Run = Run - Overlap metric to determine actual execution time.

### Q002 · Chapter 2 CPU > VM · System charged to vCPU 0
- Files: [VM CPU System](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/system.md), [VM CPU Used](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/used.md)
- Search 1: "this is charged to the VM CPU 0"
- Search 2 (diagram text): "Charged at VM level, not at vCPU 1"
- Question: is System charged to vCPU 0 or to the VM level only? Chapter 1 says per-vCPU Used excludes System.
- Written as now: charged to vCPU 0, flagged.
- Answer: Charged at VM level, not vCPU 0 or 1. This results in Total VM cost > sum of all vCPU. This is not a problem for CPU scheduling. It’s just the way the kernel does the CPU accounting. 

### Q003 · Chapter 2 CPU > VM · Run for sizing
- Files: [VM CPU Run](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/run.md), [Controlled test: VM and ESXi CPU metrics under Hyper-Threading](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/comparisons/vm-vs-esxi-ht-ramp-test.md)
- Search 1: "suitable as input to size the Guest OS and not the VM"
- Search 2: "This counter is suitable for VM Capacity sizing"
- Question: is Run for Guest OS sizing, VM sizing, or both?
- Written as now: both statements, flagged.
- Answer: Guest OS. I've updated my document.

### Q004 · Chapter 2 CPU > VM · Contention formula condition
- Files: [VM CPU Contention (VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/contention.md)
- Search: "Other Wait (if less than 1%)"
- Question: what does the condition mean?
- Written as now: formula copied as is.
- Answer: The condition of < 1% is added to ensure no false positive. See https://knowledge.broadcom.com/external/article/338438/increased-vmwait-for-idle-vms-after-upgr.html

### Q005 · Chapter 2 CPU > VM · Contention and limit
- Files: [VM CPU Contention (VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/contention.md), [VM CPU Latency](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/latency.md)
- Search 1: "Unlike CPU Ready, it does not account for Limit"
- Search 2: "Why does the counter include Ready by Limit?"
- Question: is the first statement about the pre-July-2024 Contention, which mapped to Latency?
- Written as now: yes, pre-July-2024 Contention excludes limit; current Contention includes it.
- Answer: This is VCF Operations counter, not vSphere. vSphere does not have counter. vSphere has CPU Latency, also known as %LAT_C in esxtop. The formula for CPU Contention changed in VCF Operations 8.18

### Q006 · Chapter 2 CPU > VM · Used above Run
- Files: [VM CPU Run and Used differ](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/troubleshooting/run-vs-used-gap.md)
- Search: "Why is Used consistently 41% higher than Run?"
- Question: how does Ready make Used higher than Run?
- Written as now: the book's answer (Ready), without explanation.
- Answer: Book was wrong. Answer is CPU frequency. The VM run at a higher clock speed due to turbo boost.

### Q007 · Chapter 2 CPU > VM · Ready and VM size
- Files: [VM CPU Ready](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/ready.md), [States of a VM vCPU](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/concepts/vcpu-states.md)
- Search 1 (VM): "CPU Ready tends to be higher, ceteris paribus, in larger VMs"
- Search 2 (Architecture): "You can reduce Co-stop by reducing the VM size"
- Question: does downsizing reduce Ready too, or only Co-stop?
- Written as now: both statements, flagged.
- Answer: It should reduce both, as the VM can be slot more easily. On the other than, having smaller share can increase CPU Ready.

### Q008 · Chapter 2 CPU > VM · Ramp test
- Files: [Controlled test: VM and ESXi CPU metrics under Hyper-Threading](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/comparisons/vm-vs-esxi-ht-ramp-test.md)
- Search: "ESXi CPU Core Utilization (%) matches VM Run. Both went 2x."
- Question: Core Utilization stayed at 100%. Should this read Utilization (%)?
- Written as now: Utilization (%).
- Answer: Correct. Make it clearer by using Thread Utilization instead of just Utilization.

### Q009 · Chapter 2 CPU > ESXi · Demand: provider or consumer
- Files: [ESXi CPU Demand](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/demand.md)
- Search 1: "Demand is consumer-view, while Usage is provider view"
- Search 2: "The value you see at ESXi is the summation of all the VMs"
- Question: your correction (2026-11-02) says ESXi Demand is a provider metric. Which holds?
- Written as now: both, flagged.
- Answer: The providers have 2 types of counters:
•	Provider metric. This metric does not exist at consumer. For example, the physical network in ESXi.
•	Sum of Consumer metric. This metric aggregates the metric of consumers. For example, the sum of VM network in the ESXi.

### Q010 · Chapter 2 CPU > ESXi · Usage cap
- Files: [ESXi CPU Usage](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/usage.md)
- Search: "Usage no longer capped at 100% of total capacity at the nominal frequency"
- Question: your correction says capped at 100% (KB pending). Is the cap only in vCenter, removed in VCF Operations since Aria Operations 8.18?
- Written as now: vCenter capped; VCF Operations not capped since 8.18.
- Answer: Cap have been removed in both. Add the KBs https://knowledge.broadcom.com/external/article/417702/esxi-host-reporting-over-100-cpu-usage.html and https://knowledge.broadcom.com/external/article/431027/esxi-host-cpu-usage-appears-high-in-vcen.html

### Q011 · Chapter 2 CPU > ESXi · CPU Imbalance
- Files: [ESXi CPU Imbalance](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/imbalance.md)
- Search: "ESXi CPU Imbalance = Count of Running Threads / Count of Running Cores"
- Question: built-in VCF Operations metric, or your own?
- Written as now: product tagged vsphere and vcf-operations, flagged.
- Answer: my own metric, not built-in. Add reference to https://github.com/e1-rahabok/VCF-vCommunity-Adapter/tree/main/docs/reference/metrics

### Q012 · Chapter 3 Memory > Architecture · 3 levels
- Files: [Memory layers and page mapping](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/memory-layers.md)
- Search: "ESXi uses 3 levels to manage memory"
- Question: the list after it has 4 items (TPS, Tiered Memory, Balloon, Compress/Swap). Which are the 3 levels?
- Written as now: 4 mechanisms listed, no level count.
- Answer: 4 level. Book corrected.

### Q013 · Chapter 3 Memory > Architecture · Balloon and unmet demand
- Files: [Memory layers and page mapping](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/memory-layers.md), [VM Memory Ballooned](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/virtual-motherboard/ballooned.md)
- Search: "The first sign of unmet demand"
- Question: the next sentences say ballooning does not mean ESXi is unable to meet demand. Is balloon a sign of memory pressure rather than unmet demand?
- Written as now: proactive, not unmet demand.
- Answer: The first sign of memory pressure, not unmet demand. It's a grey matter as memory management has gradient as ESXi applies 4 different layers.
- Applied 2026-11-03.

### Q014 · Chapter 3 Memory > VM · Limit and balloon
- Files: [VM Memory Ballooned](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/virtual-motherboard/ballooned.md), [Ballooning](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/ballooning.md)
- Search 1: "Does limit result in Balloon?" (the book answers no)
- Search 2: "heavily ballooned as limit was imposed on it"
- Search 3: "Since the VM needed more, it experienced heavy ballooning"
- Search 4 (Memory > ESXi): "If you actually see balloon, that means there is limit imposed"
- Search 5 (Memory > ESXi): "It takes longer to realize, and is not affected by limit"
- Question: does a limit cause ballooning?
- Written as now: both, flagged.
- Answer: The answer is not directly. Why an in-between answer? Go back to the 4 layers of memory. They are at different level on memory management. Limit results in swapped or compressed is Consumed tries to grow beyond. Consumed grows because Guest OS uses more. These uses can come from balloon driver or other processes.

### Q015 · Chapter 3 Memory > VM · Memory Latency: space or time
- Files: [VM Memory Latency](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/virtual-motherboard/latency.md), [Memory as storage](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/memory-as-storage.md)
- Search 1 (Architecture): "percentage of memory space"
- Search 2 (VM): "the amount of time a vCPU spends waiting on the completion of a page fault"
- Question: is Memory Latency a share of space or a share of time?
- Written as now: both definitions, flagged. vCenter description says time.
- Answer: Search 1 is wrong. Book updated. The correct answer is Search 2. Memory Latency, aka "Page-fault latency" is tracking the amount of time a vCPU spends waiting on the completion of a page fault. Its value is mostly swap wait, with a bit of page decompression / copy-on-write-break. The counter is called %LAT_M in esxtop. The latency metric is highly corelated with the swap-in rate.

### Q016 · Chapter 3 Memory > VM · Meaning of Compressed and Swapped
- Files: [VM Memory Swapped](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/virtual-motherboard/swapped.md), [Memory layers and page mapping](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/memory-layers.md)
- Search 1 (VM): "indicates that the host is unable to satisfy the VM memory requirement"
- Search 2 (Architecture): "It does not mean VMs were contending for RAM"
- Question: which holds?
- Written as now: Architecture statement in the concept file; VM statement flagged.
- Answer: VM compressed happens when ESXi Consumed is very high or a particular VM hit its limit. That Consumed page of a VM can contain a lot of cache, so it does not always translate to VM hitting latency.

### Q017 · Chapter 3 Memory > VM · Sharing savings
- Files: [VM Memory Shared](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/virtual-motherboard/shared.md), [VM Memory Consumed](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/virtual-motherboard/consumed.md)
- Search: "Savings = 29.83 TB"
- Question: Consumed = Granted - Savings gives 23.7 TB of savings, not 6.13 TB. Which is right?
- Written as now: the book's calculation, flagged.
- Answer:

### Q018 · Chapter 3 Memory > VM · Utilization 5%
- Files: [VM Memory Utilization (VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/virtual-motherboard/utilization.md)
- Search: "We add 5% of Total, not Used"
- Question: where does the 5% enter the formula?
- Written as now: formula and the 5% statement, flagged.
- Answer:

### Q034 · Quiz > CPU > Q2 VM CPU Speed · 80% vs 62.5% Hyper-Threading charge
- Files: [Likely vCPU speed on a busy Hyper-Threaded cluster](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-04-likely-vcpu-speed-on-a-busy-hyper-threaded-cluster.md), [VM CPU Usage](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/usage.md), [VM CPU Used](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/used.md)
- Search 1 (quiz key): "3.0 (All Cores Turbo) x 80% (as HT delivers 1.25x total)"
- Search 2 (book): "37.5%"
- Question: the quiz key gives 3.0 GHz x 80% = 2.4 GHz. The knowledge base charges each thread 62.5% when both threads run, which gives 1.875 GHz. Which factor does VM CPU Usage apply?
- Written as now: case uses the key (2.4 GHz), flagged in Notes. KB unchanged.
- Answer: Author (2026-11-03): the key is correct (2.4 GHz). Added All-Core Turbo knowledge to [CPU frequency, Turbo and their impact on a VM](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/concepts/cpu-frequency.md).

### Q035 · Quiz > CPU > Q6 VM CPU Contention · Demand and Hyper-Threading
- Files: [Counters where a vCPU cannot run at all](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-03-counters-where-a-vcpu-cannot-run-at-all.md), [VM CPU Demand](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/demand.md)
- Search 1 (quiz key): "G is wrong as Demand is affected by hyper threading"
- Search 2 (book, MS Windows table): "| VM CPU Demand   | Yes               | No             | Yes           |"
- Question: the key says Demand is affected by Hyper-Threading. The MS Windows table marks Demand as not affected. Which is right?
- Written as now: case keeps the key's answer (G wrong); reason flagged.
- Answer: Author (2026-11-03): the key is correct. Guest OS and VM are 2 realms; the Guest OS does not see physical threads. Added to [VM vs Guest OS: two realms and their visibility layers](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/vm-vs-guest-os.md), [VM CPU Demand](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/demand.md), [Guest OS CPU vs VM CPU](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/concepts/guest-os-vs-vm-cpu.md).

### Q036 · Quiz > CPU > Q7 Guest OS CPU · Is F correct?
- Files: [Guest OS run queue, context switch, Windows thread states](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-04-guest-os-run-queue-context-switch-windows-thread-states.md)
- Search 1 (quiz key): "F is correct. Windows has 8 states."
- Question: the answer column says D, E. The explanation says F is correct. Is the answer D, E, F?
- Written as now: scored as D, E, F until answered.
- Answer: Author (2026-11-03): F is correct. Answer D, E, F.

### Q037 · Quiz > Cost and Price > Q1 VM Cost · Missing explanations
- Files: `benchmark/questions/vendor-neutral/general/general-001-...`
- Search 1 (quiz key): "C is correct. The VM costs around US$ 2000 per year."
- Question: the key has empty explanations for A, B and D. What is the reason each is wrong? Which pricing date and source should the case record?
- Written as now: answer C only; no reasons for the others.
- Answer: Author (2026-11-03): tracked as a to-do in project/todo.md. Closed 2026-11-04: case removed (see Q039).

- None yet. Earlier resolved questions are recorded in each file's `review_notes`.
