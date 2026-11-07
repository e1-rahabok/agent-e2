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
- Files: [Core rules of vSphere metrics](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/core-rules.md) (section Rules); [Terminology](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/glossary.md) (section Confusable pairs); design: [harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md), section 3.
- Search: not from the book. Each rule and pair summarises the knowledge file it points to.
- Question:
  1. Are these the 12 rules an expert would give a new colleague first? Which would you drop, add or reword?
  2. Are the 8 confusable pairs right, and is any pair missing?
- Written as now: drafted by Claude 2026-11-06, status draft. The agent receives them only when the switches are on (all off by default).
- Answer: 

### Q060 · Operations flows · Users say the VM is slow: your order of checks
- Files: [Users say the VM is slow: triage](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/performance/diagnosis/vm-slow-triage.md) (sections Checks, in order; Why this order). Review: [project/review-2026-11-06.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/review-2026-11-06.md), section 3.3.
- Search: not from the book. Drafted from the VM overview file and the per-resource flows.
- Question:
  1. Is this the order you follow in the field: time window, breadth (many VMs?), VM contention per resource, Guest OS queues, then context (limits, snapshots, vMotion)?
  2. What do you check that is missing, for example the application team's own evidence, or a recent change?
  3. Is the SLI bar (Ready 2.5%, memory contention 1%, disk latency 10 ms, transmit dropped 0%) the right first bar for one VM, or do you use other values?
- Written as now: 5 steps, status draft. It hands over to the existing CPU, memory, storage, network and cluster flows.
- Answer:

### Q061 · Operations flows · Can this cluster take more VMs: your order of checks
- Files: [Can this cluster take more VMs?](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/diagnosis/can-cluster-take-more-vms.md) (sections Checks, in order; Why this order).
- Search: not from the book. Drafted from the capacity model, Cluster Performance, Cluster Risk, Cluster Consumption, admission control and host memory states.
- Question:
  1. Is this your order: cluster state and HA, contention today, Cluster Risk, room after HA and buffer, fit of the new VMs (reservations, overcommit, monster size), balance?
  2. Which resource do you find fills first in practice, and does that change the order?
  3. How do you state the answer to the requester: a yes/no, a number of VMs, or a date?
- Written as now: 6 steps, status draft.
- Answer:

### Q062 · Operations flows · Is this host or cluster healthy right now
- Files: [ESXi: what to monitor, in priority order](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/esxi/overview-what-to-monitor.md); [vSphere cluster: what to monitor, in priority order](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/overview-what-to-monitor.md).
- Search: not from the book.
- Question: what is your daily health check of an ESXi host and of a cluster, in order? The overview files list what to monitor, but not the order of checks with a stop at each step. With your order, a health-check flow can be written for each.
- Written as now: overview files only; no flow.
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
| 8 | 4 | [Cluster SLA and SLI](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/kpis/cluster-sla-sli.md) |
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
| 19 | 3 | [vNIC receive drops: find the reason with vsish](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/network/diagnosis/vnic-rx-drops.md) |
| 20 | 3 | [ESXi storage latency stack: GAVG, KAVG, QAVG, DAVG](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/concepts/esxi-storage-latency-stack.md) |
| 21 | 3 | [Cluster Performance (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/kpis/cluster-performance.md) |
| 22 | 3 | [Cluster Risk (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/kpis/cluster-risk.md) |
| 23 | 3 | [Why rightsizing matters for VMs](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/rightsizing.md) |
| 24 | 3 | [ESXi storage latency is high](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/diagnosis/host-storage-latency.md) |
| 25 | 3 | [Admission control, expandable reservations and cluster state](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/concepts/admission-control-and-cluster-state.md) |

- Written as now: all files draft.
- Answer:

### Q072 · Part 1 > The Layers in IT Systems · Book corrections and Apdex
- Files: [Business, application and IaaS: layers, lost context and metric types](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/performance/realms-and-layers.md) (image troubleshooting-layers-loss-of-context-example-table.png).
- Search 1: "Johnny’s transaction was the worst at 20.1 seconds"
- Search 2: "I like the principle behind apdex, but not its implementation"
- Question: (a) GetBankDetail 5.2 s plus the other 7 functions 15.1 s = 20.3 s, not 20.1 s. (b) Image text: "None of the counters are AWS shows any signs of performance counters". (c) The book offers an improved Apdex formula. Give it to the knowledge base, or leave it out, since it is not IaaS?
- Written as now: no number from the image in the text; no Apdex.
- Answer:

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
- Answer: (a) overcommit ratio for memory is only against DRAM portion only, because the whole point of adding an NVMe disk is to avoid overcommit. (b) the memory latency or memory contention metric 

### Q083 · Part 1 > Noisy Neighbour > Network · Author's network limit and reservation
- Files: [Noisy neighbour: limit, reservation and share per resource](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/noisy-neighbour.md) (section Network).
- Search 1: "I think it should be 8 Gb/s."
- Search 2: "consider setting 100 Mb/s per VM"
- Question: these are the only network numbers per VM. 8 Gb/s × 25 VMs = 200 Gb on a 40 Gb host: the limit stops one villain, not many at once. Is 8 Gb/s a cap for one VM's peak and 100 Mb/s a floor? Should they go in the capacity threshold file as rules?
- Written as now: in the text, not in the threshold files.
- Answer:

### Q084 · Knowledge base · ESXi CPU Demand: sum of VMs or not
- Files: [knowledge/vsphere/foundations/provider-consumer.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/provider-consumer.md) (sections ESXi CPU Demand, Provider metric types); [knowledge/glossary.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/glossary.md) (Confusable pairs, ESXi CPU Demand vs Usage).
- Search (Part 3): "Not the sum of all VM worlds + VMkernel worlds"
- Question: found while checking this chapter. One file says ESXi CPU Demand is not a sum of consumers, with a trap. The same file, in Provider metric types, gives it as a sum-of-consumer example. The glossary says it is the sum over the VMs. Which is right? Claude will make the three agree.
- Written as now: contradictory.
- Answer:

### Q085 · Follow-up to Q070 · Does the hypervisor count a full VMXNET3 receive ring
- Files: [VM Network Packets Dropped](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/network/metrics/virtual-motherboard/packets-dropped.md) (sections Known causes, Traps).
- Search: not from the book. Broadcom KB 1010071 (Claude's own knowledge, not fetched): esxtop shows dropped receive packets at the virtual switch port when the guest does not empty its receive ring fast enough; the fix is a larger ring in the Guest OS.
- Question: your answer says the ring-buffer drop is not visible to the hypervisor. As Claude reads it, the guest never receives the packet, so the drop is counted at the VM's port: VM Network Receive Packets Dropped in vCenter, %DRPRX in esxtop. Visible to the hypervisor, but caused and fixed in the guest. Your conclusion holds either way: outside the IaaS SLA, and receive drops are already left out of it. Which is right for the reason: (a) not visible, or (b) visible but not controllable?
- Written as now: guest-os layer, outside the IaaS SLA; the visibility claim left out.
- Answer:

## Resolved

### Q065 · Part 1 > Performance Management > Utilization vs Demand · Absolute or relative performance
- Files: [Performance vs capacity: two readings of the same utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/performance/performance-vs-capacity.md) (section Absolute vs relative); [KPI vs SLA: from complaint-based operations to a contract](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/performance/kpi-vs-sla.md) (section KPI vs SLA, Reference).
- Search 1: "Performance will be absolute (real value), Capacity will be relative"
- Search 2: "It tends to be absolute, as it’s reporting raw metrics"
- Question: the book says performance is absolute. In chat you said relative cluster performance is more meaningful than absolute, because no perfect formula exists. Relative to what: (a) other clusters and the same cluster last week, (b) the class-of-service threshold (a score in %), (c) the share of VMs served well (a count, not milliseconds)? Which sentence should the knowledge base hold?
- Written as now: performance absolute, against total capacity; capacity relative, against usable capacity. The paradigm in your chat message is not written yet.
- Answer:
(a). Performance is relative to other clusters, and relative to itself over time. Think of your stock market index like Nasdaq. The actual amount is basically irrelevant as it's just a combination of number. What you care is the relative movement.
(b) Gold Class Cluster should relatively high higher performance (%) score , lower consumption (%) score, and lower risk (%) score versus Bronze Class Cluster.

Capacity is relative because it's relative to Usable Capacity, not Total Capacity. The real, actual, cluster utilization is lower in reality. But since it's divided over Usable Capacity instead of Total Capacity, the score becomes artificially higher. 

### Q067 · Part 1 > Contention vs Consumption · Points A and B: 100% and queues
- Files: [Performance vs capacity: two readings of the same utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/performance/performance-vs-capacity.md) (sections Contention vs consumption, Four points on the utilization scale).
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
- Files: [KPI vs SLA: from complaint-based operations to a contract](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/performance/kpi-vs-sla.md); [Noisy neighbour: limit, reservation and share per resource](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/noisy-neighbour.md) (memory class table); [knowledge/vcf-operations/kpis/cluster-sla-sli.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/kpis/cluster-sla-sli.md).
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
- Files: [Performance vs capacity: two readings of the same utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/performance/performance-vs-capacity.md) (section Four points on the utilization scale).
- Search: "Worst performance actually happens when utilization = 0% as nothing gets done"
- Question: 0% utilization with 0 demand is an idle VM: no contention, nothing to serve. Only 0% with demand above 0 is bad: a VM frozen by a storage pause, as in your antivirus story. Is the rule "performance = demand served / demand", so that utilization alone cannot tell good from bad at either end?
- Written as now: "C, 0% while there is demand" (Claude's wording).
- Answer: Yes, utilization alone does not mean anything. 0% can be bad, 100% can be good. Hence my book said utilization is not something you manage. It's just an input, and one of the inputs to 2 things you care, which is performance and capacity. Utilization is used differently in capacity and performance. 

### Q068 · Part 1 > Utilization vs Demand · Highest host utilization in cluster performance
- Files: [Performance vs capacity: two readings of the same utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/performance/performance-vs-capacity.md) (section Cluster: performance vs capacity); [knowledge/vcf-operations/kpis/cluster-performance.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/kpis/cluster-performance.md).
- Search 1: "you want to take the highest among the host as your primary counter for cluster utilization"
- Search 2: "Utilization is for troubleshooting, not monitoring." (table image, Cluster Performance column)
- Question: for cluster performance, the same chapter says utilization is for troubleshooting only, and the cluster KPI holds only the contention of running VMs. Where does the highest-host utilization belong: (a) a performance monitoring metric, (b) the first troubleshooting drill-down after the cluster KPI drops, (c) a capacity-risk early warning?
- Written as now: both statements, unreconciled.
- Answer: highest-host utilization belong cluster risk score. See https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/cluster-risk.md and https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/formula/cluster-risk.png. I thought I gave you these 2 already?
- BTW, typically risk hits both capacity and performance, as capacity and performance are 2 sides of the same coin. 
- I think you hallucinated here. I'm not able to find anything around "you want to take the highest among the host as your primary counter for cluster utilization" in the 2 files you refer. In future, cite something I can search.

On the file https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/kpis/cluster-performance.md. Why does vCommunity have to be part of the page title? What's the relevant to the local LLM? 
  

### Q069 · Part 1 > Pattern Difference · Where the cliff starts
- Files: [Performance vs capacity: two readings of the same utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/performance/performance-vs-capacity.md) (section Pattern difference).
- Search: "You can’t forecast performance using capacity"
- Question: the chart marks the drop at "Overcommit >1". The noisy-neighbour example runs 4:1 vCPU to core with no cliff. Is the cliff where demand passes supply on a host (demand overcommit), not where the allocation ratio passes 1? And since each host is its own pool, does it start on the hottest host, before the cluster average reaches 100%?
- Written as now: "falls steeply once demand passes what the hosts supply".
- Answer: Is the cliff where the allocation ratio passes 1. And since each host is its own pool, does it start on the hottest host, before the cluster average reaches 100%? Yes, although in theory DRS is supposed to balance all the hosts. There is no such thing demand overcommit as you can only overcommit the allocation. Demand, Usage, Utilization, are not something you can control. 

### Q070 · Part 1 > IaaS Metric Types · Layer of the driver metrics
- Files: [Business, application and IaaS: layers, lost context and metric types](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/performance/realms-and-layers.md) (section Consumer and provider metric types); [knowledge/vsphere/technology/network/metrics/virtual-motherboard/packets-dropped.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/network/metrics/virtual-motherboard/packets-dropped.md) (VMXNET3 buffer drops).
- Search: "One at the Windows/Linux layer, and one at the driver layer (e.g. PVSCSI, vmxnet)"
- Question: the book puts PVSCSI and vmxnet metrics in the Guest OS. The repository rule places a metric by the layer that produces it. The driver runs in the guest kernel, but it is VMware's virtual device. Is a VMXNET3 ring-buffer drop (a) guest-os layer, outside the IaaS SLA, or (b) virtual-motherboard layer, inside it? This decides the folder and who fixes it.
- Written as now: VMXNET3 drops sit in the VM (virtual-motherboard) file.
- Answer: VMXNET3 ring-buffer drop is a guest-os layer, outside the IaaS SLA as it's not visible to the hypervisor. You don't put SLA on something you cannot see, let alone control. The one covered by SLA is the vNIC as seen by the hypervisor. 

### Q071 · Part 1 > The 3 Realms · One word, two meanings: realm
- Files: [Business, application and IaaS: layers, lost context and metric types](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/performance/realms-and-layers.md); [knowledge/vsphere/foundations/vm-vs-guest-os.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/foundations/vm-vs-guest-os.md) (VM vs Guest OS: two realms); [knowledge/operations-management/performance/performance-kpi-design.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/performance/performance-kpi-design.md) ("one per realm").
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
- Files: band tables in [VM Performance (%) (VCF Operations KPI)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/kpis/vm-performance.md), [Cluster Performance (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/kpis/cluster-performance.md), [Cluster Consumption (%) (VCF Operations KPI)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/kpis/cluster-consumption.md), [Cluster Risk (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/kpis/cluster-risk.md), [Cluster SLA and SLI](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/kpis/cluster-sla-sli.md), [Guest OS Performance (%) (VCF Operations KPI)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/system/metrics/guest-os-performance.md); rows in [knowledge/catalog/thresholds-performance.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-performance.yaml) and [thresholds-capacity.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-capacity.yaml) (fields `interval`, `instance`).
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
- Files: [Reclaiming vCPUs from an idle VM](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-06-reclaiming-vcpus-from-an-idle-vm.md); [Why rightsizing matters for VMs](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/capacity/rightsizing.md), [Unused and idle vCPUs](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/concepts/idle-and-unused-vcpus.md), [Large VM with low utilization: build the case to downsize](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/diagnosis/oversized-vm-downsizing.md)
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
- Files: [ESXi storage latency is high](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/diagnosis/host-storage-latency.md), [vSphere documentation performance guidance](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/tools/vsphere-client/performance-guidance.md)
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
- Files: [Cluster Performance (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/kpis/cluster-performance.md)
- Search 1: "vMotion is not included as it only becomes an issue"
- Search 2: "vMotion is included as it does impact the VM performance"
- Question: is vMotion part of the cluster KPI or not? The threshold table has no vMotion row.
- Written as now: vMotion described as a leading indicator, flagged.
- Answer: vMotion should not be included in actual performance as the metric counts the number of vmotion, not the length of the actual downtime. In a healthy environment, each vMotion down time is below 0.2 second and does not impact the Guest OS. Broadbase infrastructure capabilities like vMotion, NSX Edge, vSAN resync and general infrastructure (e.g. network) should be monitored separately. For example, track the maximum downtime for all vMotion across entire environment as a high downtime is a leading indicator of performance degradation.
- Done 2026-11-05: [Cluster Performance (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/kpis/cluster-performance.md), section vMotion is not part of the KPI; [Cluster Risk (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/kpis/cluster-risk.md), section Not used.

### Q031 · Provider Objects > Performance · Cluster KPI table vs text
- Files: [Cluster Performance (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/kpis/cluster-performance.md)
- Search 1: "Storage troubleshooting differs to compute troubleshooting" (disk latency listed as not used)
- Search 2: "That’s why it’s given 4x the threshold of zipped + swapped" (balloon thresholds)
- Search 3: "I did not set green = 0"
- Question: the table includes disk latency rows, has no balloon or swapped rows, and sets packet green to 0%. Is the table or the text current?
- Written as now: the table, with text reasons listed and the conflict flagged.
- Answer: both are outdated. The updated information is here https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/formula/cluster-performance.png and https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/cluster-performance.md Update the knowledge accordingly.
Also, update Cluster Risk in the knowledge base from https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/formula/cluster-risk.png and https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/cluster-risk.md
- Done 2026-11-05: [Cluster Performance (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/kpis/cluster-performance.md) and [Cluster Risk (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/kpis/cluster-risk.md) rewritten from the adapter documentation (thresholds, calculation, DRAM-only memory, scoring, Excluded rows, known limitation, missing data); both threshold images replaced with the current tables; shared scoring rule updated in [Performance KPI design: VM Performance (%) and Guest OS Performance (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/operations-management/performance/performance-kpi-design.md).

### Q032 · Provider Objects > Other Metrics · Monster VM threshold
- Files: [Cluster Risk (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/kpis/cluster-risk.md), [vSphere cluster: operations complexity](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/concepts/cluster-operations.md)
- Search 1 (Overview): "If a VM vCPU > 45% of the ESXi count of threads"
- Search 2 (Monster VM): "if a VM vCPU size is > 40% of the ESXi count of threads"
- Search 3 (Cluster Risk): "the VM size needs to be at least half the ESXi"
- Search 4 (recommendation): "Monster VM > 50% of physical core, not thread"
- Question: which CPU threshold defines a monster VM?
- Written as now: the recommendation (above 50% of physical cores); the others flagged.
- Answer: The final and up to date answer at https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/cluster-risk.md#when-a-vm-is-a-monster  Update the
- Done 2026-11-05: [Cluster Risk (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/kpis/cluster-risk.md), section Monster VM; [vSphere cluster: operations complexity](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/concepts/cluster-operations.md) Monster VM row; [knowledge/catalog/thresholds-performance.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-performance.yaml) and [thresholds-capacity.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-capacity.yaml) rows monster-vm-cpu and monster-vm-memory.

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
- Files: [VM Performance (%) (VCF Operations KPI)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/kpis/vm-performance.md)
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
- Files: [ESXi Memory Utilization (VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/metrics/esxi/memory-utilization.md)
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
- Files: [VM CPU Contention (VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/metrics/vm/cpu-contention.md)
- Search: "Other Wait (if less than 1%)"
- Question: what does the condition mean?
- Written as now: formula copied as is.
- Answer: The condition of < 1% is added to ensure no false positive. See https://knowledge.broadcom.com/external/article/338438/increased-vmwait-for-idle-vms-after-upgr.html

### Q005 · Chapter 2 CPU > VM · Contention and limit
- Files: [VM CPU Contention (VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/metrics/vm/cpu-contention.md), [VM CPU Latency](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/latency.md)
- Search 1: "Unlike CPU Ready, it does not account for Limit"
- Search 2: "Why does the counter include Ready by Limit?"
- Question: is the first statement about the pre-July-2024 Contention, which mapped to Latency?
- Written as now: yes, pre-July-2024 Contention excludes limit; current Contention includes it.
- Answer: This is VCF Operations counter, not vSphere. vSphere does not have counter. vSphere has CPU Latency, also known as %LAT_C in esxtop. The formula for CPU Contention changed in VCF Operations 8.18

### Q006 · Chapter 2 CPU > VM · Used above Run
- Files: [VM CPU Run and Used differ](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/diagnosis/run-vs-used-gap.md)
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
- Files: [VM Memory Utilization (VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/metrics/vm/memory-utilization.md)
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
