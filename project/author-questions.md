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
- Files: `vsphere/technology/memory/metrics/host/consumed`
- Search 1: "It only includes the resultant zipped, not the amount subjected to compression"
- Search 2: "Consumed does not include compressed"
- Question: does host Consumed include the compressed result in DIMM?
- Written as now: includes the result, flagged. Your diagram (physical view) also shows it inside Consumed.
- Answer:

### Q023 · Chapter 4 Storage > VM · Disk metric scope
- Files: `vsphere/technology/storage/metrics/virtual-motherboard/disk`
- Search: "if the value is per VM or per disk"
- Question: is the VM Disk (device-level) metric value for this VM only, or for the whole device shared by many VMs?
- Written as now: associated with the VM, flagged as unsure.
- Answer:

### Q027 · Consumer Objects > Capacity · VM CPU Needed formula
- Files: `operations-management/capacity/vm-footprint-sizing`
- Search: "VM CPU Needed = (Used + Overlap + Co-stop + Ready + Other Wait) + System"
- Question: is the whole sum divided by 20,000, or only System? VM-level Used already includes System (Chapter 2 VM, Used formula). Is System counted twice?
- Written as now: formula copied as is, flagged.
- Answer: VM CPU Needed = (Sum of all vCPU (Used + Overlap + Co-stop + Ready + Other Wait) + System ) / 20000 * vCPU
Emphasize that this is a narrow use case, as it's about the footprint of the VM on the underlying ESXi. This is only useful in VM migration to a different ESXi. What's more relevant in the Guest OS (Windows or Linux) capacity sizing. 


### Q028 · Consumer Objects > Capacity · Balloon in Guest OS memory sizing
- Files: `guest-os/system/concepts/guest-os-sizing`
- Search: "Exclude balloon"
- Question: the text excludes balloon, but the sizing table marks Ballooned in blue (include) with "The memory was taken by Tools". Include or exclude?
- Written as now: exclude, flagged.
- Answer: include. It is hard to know if the page used by balloon was a free page or not. 
If it’s from free page, then exclude. 
If it’s from non-free page, then include. 
To be conservative, I recommend include.


### Q029 · Consumer Objects > Capacity · Memory utilization ranges
- Files: `guest-os/system/concepts/guest-os-sizing`
- Search: "The company is wasting money if the utilization falls below 50%"
- Question: the text gives waste below 50% and risk above 75%, which matches bar 1. You recommend bar 2, where green starts near 75%. What are the ranges for bar 2?
- Written as now: bar 2 recommended, no numbers stated.
- Answer: I’d recommend 0 - 75% - 85% – 95% - 100% as Windows and Linux tend to cache memory.

### Q030 · Provider Objects > Performance · vMotion in Cluster Performance (%)
- Files: `vsphere/object-types/cluster/metrics/cluster-performance`
- Search 1: "vMotion is not included as it only becomes an issue"
- Search 2: "vMotion is included as it does impact the VM performance"
- Question: is vMotion part of the cluster KPI or not? The threshold table has no vMotion row.
- Written as now: vMotion described as a leading indicator, flagged.
- Answer: vMotion should not be included in actual performance as the metric counts the number of vmotion, not the length of the actual downtime. In a healthy environment, each vMotion down time is below 0.2 second and does not impact the Guest OS. Broadbase infrastructure capabilities like vMotion, NSX Edge, vSAN resync and general infrastructure (e.g. network) should be monitored separately. For example, track the maximum downtime for all vMotion across entire environment as a high downtime is a leading indicator of performance degradation.

### Q031 · Provider Objects > Performance · Cluster KPI table vs text
- Files: `vsphere/object-types/cluster/metrics/cluster-performance`
- Search 1: "Storage troubleshooting differs to compute troubleshooting" (disk latency listed as not used)
- Search 2: "That’s why it’s given 4x the threshold of zipped + swapped" (balloon thresholds)
- Search 3: "I did not set green = 0"
- Question: the table includes disk latency rows, has no balloon or swapped rows, and sets packet green to 0%. Is the table or the text current?
- Written as now: the table, with text reasons listed and the conflict flagged.
- Answer: both are outdated. The updated information is here https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/formula/cluster-performance.png and https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/cluster-performance.md Update the knowledge accordingly.
Also, update Cluster Risk in the knowledge base from https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/formula/cluster-risk.png and https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/cluster-risk.md

### Q032 · Provider Objects > Other Metrics · Monster VM threshold
- Files: `vsphere/object-types/cluster/metrics/cluster-risk`, `vsphere/object-types/cluster/concepts/cluster-operations`
- Search 1 (Overview): "If a VM vCPU > 45% of the ESXi count of threads"
- Search 2 (Monster VM): "if a VM vCPU size is > 40% of the ESXi count of threads"
- Search 3 (Cluster Risk): "the VM size needs to be at least half the ESXi"
- Search 4 (recommendation): "Monster VM > 50% of physical core, not thread"
- Question: which CPU threshold defines a monster VM?
- Written as now: the recommendation (above 50% of physical cores); the others flagged.
- Answer: The final and up to date answer at https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/cluster-risk.md#when-a-vm-is-a-monster  Update the 

### Q033 · MS Windows > CPU > Usage | Utilization | Time · VM CPU Run and Hyper-Threading
- Files: `guest-os/cpu/concepts/windows-cpu-scheduling`, `vsphere/technology/cpu/metrics/virtual-motherboard/run`
- Search 1 (MS Windows table): "Which VM counters can be used when you have no visibility into the Guest"
- Search 2 (Chapter 2, Run | Net Run): "counter not affected by CPU frequency scaling and hyper threading"
- Question: the MS Windows table marks VM CPU Run as Yes in the Hyperthreading column. Chapter 2 says Run is not affected by Hyper-Threading. Which is right?
- Written as now: the table as in the book, marked with the conflict; `run` keeps the Chapter 2 statement.
- Answer:

### Q038 · Auto Test > Prompt design · ONLY the knowledge base, or knowledge base first
- Files: `harness/modes.py` (SYSTEM_KB, SYSTEM_AGENT); evidence in `benchmark/results/autotest/20261103-093742/report.md`, section Analysis.
- Search: not from the book. Finding from the frontier reference run 20261103-093742.
- Question: should the AI answer from the knowledge base only, or use the knowledge base first and its own knowledge where the knowledge base is silent?
- Written as now: prompt says answer using ONLY the knowledge base; if not covered, choose "Not covered by the knowledge base".
- Finding:
  - Frontier model: baseline (no knowledge base) 75%, classic 67%, agentic 67%.
  - The ONLY rule cost 3 questions where the knowledge base is silent: vendor-neutral-general-001 (5 of 5 to 0 of 5), vsphere-cpu-013 (5 to 0), vsphere-general-001 (5 to 2).
  - The knowledge base cut the trap rate: 16% to 6-9%.
- Options:
  - Keep ONLY: fewer invented answers; no credit where the knowledge base is silent; every gap must be filled in the knowledge base.
  - Knowledge base first: knowledge base wins on conflict; own knowledge fills gaps; more coverage; more risk of invented answers.
  - Test both in one run and compare.
- Answer:

### Q040 · Quiz > CPU > Q1 ESXi CPU Utilisation · Which counter is ESXi true utilization
- Files: `benchmark/cases/vsphere-cpu-004-esxi-true-utilization-from-usage-core-utilization-and-utilization.md`; `vsphere/technology/cpu/metrics/host/core-utilization`, `vsphere/technology/cpu/metrics/host/utilization`, `vsphere/technology/cpu/metrics/host/usage`
- Search 1 (quiz): "It is a balanced reporting"
- Search 2 (quiz): "Plenty of physical threads are idle"
- Question: key is C (Utilization, 40%). All models, frontier included, chose B (Core Utilization, 70%), with and without the knowledge base. Is C right? If yes, which statement should the knowledge base add?
- Written as now: core-utilization says Core Utilization is a capacity metric (ignores frequency). utilization says Utilization suits capacity management. No file says which one is the ESXi true utilization, or why Core Utilization overstates it.
- Answer:

### Q041 · Quiz > CPU > Q8 Reservation · Options A and B
- Files: `benchmark/cases/vsphere-cpu-011-cpu-reservation-behaviour.md`; `vsphere/foundations/resource-controls`, `vsphere/technology/cpu/metrics/host/reserved-capacity`, `vsphere/foundations/overhead`
- Search 1 (quiz): "Total reservation at ESXi level is capped at the base nominal clock speed"
- Search 2 (quiz): "CPU reservation only comes into play during contention"
- Question: key is A,B,C,D. Frontier classic chose C,D in 5 of 5 runs and rejected A and B. Are A and B correct? If yes, which statements should the knowledge base add?
- Written as now: reservation in MHz/Hertz (supports D); CPU reservation not sticky, memory reservation sticky (supports C). No file states the cap at base nominal clock speed (A) or that the reservation only matters under contention (B).
- Answer:

### Q042 · Quiz > CPU > Q11 Reclamation · Option D, power off frees memory
- Files: `benchmark/cases/vsphere-cpu-013-reclaiming-vcpus-from-an-idle-vm.md`; `operations-management/capacity/rightsizing`, `vsphere/technology/cpu/concepts/idle-and-unused-vcpus`, `vsphere/technology/cpu/diagnosis/oversized-vm-downsizing`
- Search (quiz): "Power off the VM, as this also frees the VM memory"
- Question: key is C,D. Frontier baseline chose C,D in 5 of 5; frontier classic chose C only in 5 of 5, citing that the knowledge base does not make the claim. Should the knowledge base state that powering off an idle VM frees its memory, as part of reclamation?
- Written as now: no file states that powering off an idle VM frees its memory. idle-and-unused-vcpus covers the CPU cost of idle vCPUs only.
- Answer:

### Q043 · Quiz > Memory > Q2 VM vs Guest OS · Options A and D
- Files: `benchmark/cases/vsphere-memory-003-relationship-between-vm-and-guest-os-memory-metrics.md`; `vsphere/technology/memory/concepts/guest-os-vs-vm-memory`, `vsphere/technology/memory/concepts/ballooning`, `vsphere/technology/memory/metrics/virtual-motherboard/usage`
- Search 1 (quiz): "Neither layer considers the other"
- Search 2 (quiz): "the hypervisor cannot balloon the VM"
- Question: key is A,B,D,E. Frontier dropped A or D in every run (baseline and agentic B,D,E; classic A,B,E). Are A and D both correct? If yes, which statements should the knowledge base add?
- Written as now: guest-os-vs-vm-memory says neither the VMkernel nor the Guest OS has full visibility into the other (close to A, but not "managed independently"). No file states that ballooning requires VMware Tools running (D).
- Answer:

### Q044 · Chapter 4 Storage > ESXi · Latency thresholds vs vSphere 9.1 documentation
- Files: `vsphere/technology/storage/diagnosis/host-storage-latency`, `vsphere/foundations/vsphere-client-performance-guidance`
- Search 1: "the value should be within 0.5 ms"
- Search 2: "In a healthy environment, it should be well within 5 ms"
- Question: the vSphere 9.1 documentation (vSphere Monitoring and Performance > Solutions for Disk Performance Problems, p. 2121) says kernelLatency best 0-1 ms and a problem above 4 ms; deviceLatency above 15 ms indicates an array problem; queueLatency must be 0. Keep the book values as the knowledge-base thresholds, and the documentation values only as the vendor's published guidance?
- Written as now: diagnosis file uses the book values (KAVG 0.5 ms, DAVG well within 5 ms). The guidance file lists the documentation values, says the 15 ms value comes from spinning-disk arrays, and points to the book values.
- Answer:

### Q045 · Chapter 3 Memory > VM · Swapped formula in the vSphere 9.1 documentation
- Files: `vsphere/technology/memory/metrics/virtual-motherboard/swapped`
- Search: "This is why Swapped is not Swapped In – Swapped Out"
- Question: the vSphere 9.1 documentation (Virtual Machines > Memory (MB), p. 2103) defines VM Swapped = swapout – swapin, and adds that vMotion can make Swapped larger than swapout – swapin. Is the documentation wrong, or does its formula hold for cumulative counters (total swapped out minus total swapped in) while the book means the rates?
- Written as now: Swapped is not Swap in - Swap out: both run in parallel on different pages. Related to Q019 (host Swap Consumed).
- Answer:

### Q046 · Provider Objects > esxtop · HTQ and DTYP still in the 9.1 documentation
- Files: `vsphere/technology/cpu/metrics/comparisons/esxtop-cpu`, `vsphere/technology/network/metrics/comparisons/esxtop-network`
- Search 1: "The column HTQ is no longer shown in ESXi 7.0"
- Search 2: "does not seem to be available anymore"
- Question: the vSphere 9.1 documentation still lists HTQ (CPU panel) and DTYP (network panel). Do they show on an ESXi 9.1 host?
- Written as now: both described as no longer shown, per the book.
- Answer:

### Q047 · The World of Metrics > Resource management · Untouched memory reservation
- Files: `vsphere/foundations/resource-controls`
- Search: "since ESXi has reserved the space, it is not available to other VMs"
- Question: the vSphere 9.1 documentation (vSphere Resource Management > Virtual Machine Memory, pp. 1833-1834) says that until a VM has touched all memory within its reservation, the VMkernel can allocate the untouched part to other VMs; only touched reserved memory is kept, even when idle. Does the book statement mean admission control (the reservation cannot be promised to another VM), while the physical pages can still be used by others until touched?
- Written as now: Consumed jumps to the reservation at power-on; the reserved space is not available to other VMs. The existing correction says RAM is backed on first use, then stays locked.
- Answer:

### Q048 · Thresholds · Interval and instance reading of every band
- Files: band tables in `vsphere/object-types/vm/metrics/vm-performance`, `vsphere/object-types/cluster/metrics/cluster-performance`, `cluster-consumption`, `cluster-risk`, `cluster-sla-sli`, `guest-os/system/metrics/guest-os-performance`; rows in `knowledge/catalog/thresholds.yaml` (fields `interval`, `instance`).
- Search: not from the book. Follows the rule added to `foundations/thresholds` (Interval rule, Instance rule).
- Question: for each band row, which sample interval was it set on (20-second peak, 5-minute, 1-day), and which reading (worst instance, object aggregate, percentile of objects)? Most rows say "peak" or "worst" but not the interval; utilization rows say neither.
- Written as now: interval and instance stated only where the row name says it (for example "Peak CPU Ready among any vCPU"); Compressed + Swapped at 5 minutes and Memory Contention at 20 seconds (Q026).
- Answer:

### Q049 · vCenter API counters · clusterServices.cpufairness and memfairness (low priority)
- Files: `knowledge/catalog/vcenter-api-counters.yaml` (HostSystem rows); no knowledge file yet.
- Search: not from the book. vCenter 9.1.0 API summaries: cpufairness "Fairness of distributed CPU resource allocation"; memfairness "Aggregate available memory resources of all the hosts within a cluster" (looks copied from another counter).
- Question: what do the two host counters measure, and are they worth documenting for operations?
- Written as now: listed in the catalog only, no knowledge file.
- Answer:

### Q050 · vCenter API counters · clusterServices.effectivecpu and effectivemem vs totalmhz and totalmb (low priority)
- Files: `knowledge/catalog/vcenter-api-counters.yaml` (ClusterComputeResource rows); candidate: `operations-management/capacity/capacity-model`.
- Search: not from the book. vCenter 9.1.0 API summaries: effectivecpu "Total available CPU resources of all hosts within a cluster"; effectivemem "Total amount of machine memory of all hosts in the cluster that is available for use for virtual machine memory and overhead".
- Question: Claude's own knowledge (the API's cluster summary) says effective capacity excludes hosts in maintenance mode or not responding, and virtualization overhead. Is that right, and should the knowledge base prefer it over totalmhz and totalmb for usable capacity?
- Written as now: listed in the catalog only.
- Answer:

### Q051 · vCenter API counters · clusterServices.failover
- Files: `vsphere/object-types/cluster/concepts/admission-control-and-cluster-state`.
- Search: not from the book. vCenter 9.1.0 API summary: "vSphere HA number of failures that can be tolerated".
- Question: how does the value behave under each HA admission control policy (slot, percentage of cluster resources, dedicated failover hosts, disabled)? Any trap in reading it?
- Written as now: the counter, its level and its summary; behaviour per policy left open.
- Answer:

### Q052 · vCenter API counters · vmop counters: cumulative or per interval (low priority)
- Files: `vsphere/object-types/cluster/metrics/vm-operations`.
- Search: "Cumulative since the cluster was created"
- Question: vCenter stores the 20 vmop counters with rollup latest and stat type absolute, on the cluster and the datacenter. Your hypothesis: vCenter accumulates them while VCF Operations shows a rate. Confirm? Do the vCenter counts ever reset (vCenter restart, cluster re-creation)?
- Written as now: cumulative since cluster creation (book); VCF Operations converts them to rates (book).
- Answer:

### Q053 · vCenter API counters · gpu.mem.reserved vs gpu.mem.used
- Files: `vsphere/technology/gpu/concepts/gpu-monitoring` (sections Counters, Reading the counters, vGPU capacity).
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

### Q054 · Benchmark · Mix of the 100 cases by kind
- Files: `benchmark/test-design.md`, sections 3.2.1, 3.3, 7.4, 13 (https://github.com/e1-rahabok/isvara-2/blob/main/benchmark/test-design.md).
- Search: not from the book.
- Question: the final score weighs every case the same, so the mix of kinds sets the weight of each sub-score. Is 60 multiple choice, 20 screenshot, 20 conversation the right mix for the 100 cases? Are the screenshot minimums right (5 each from esxtop, vCenter UI, VCF Operations UI; 5 with 2 or more images)?
- Written as now: the proposal above. Today: 15 multiple choice, 3 screenshot, 10 conversation.
- Answer:

## Resolved

### Q024 · Chapter 5 Network > Architecture · VM and ingress
- Files: `vsphere/technology/network/concepts/network-observability`
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
- Files: `vsphere/technology/network/metrics/virtual-motherboard/packets-dropped`
- Search: "1 thousand packets dropped = 1500 MB worth of packets within 300 seconds"
- Question: 1,000 × 1.5 KB = 1.5 MB. Should it be 1 million packets = 1,500 MB, or 1,000 packets = 1.5 MB?
- Written as now: flagged, no number stated.
- Answer: 1.5 MB. Book was wrong.

### Q026 · Consumer Objects > Performance · Compressed + Swapped threshold
- Files: `vsphere/object-types/vm/metrics/vm-performance`
- Search: "their threshold is 2x of memory contention"
- Question: the table gives Compressed + Swapped green at 0-0.25%, half of Memory Contention (0-0.5%), not 2x. Which is intended?
- Written as now: the table values, with the conflict flagged.
- Answer: Swapped and Compressed are combined as they are the result of the same action. Together they tell the complete picture. As they may not indicate actual problem, their threshold is higher. However, since we measure at 5 minute sample, while memory contention is measured at 20 second, I adjust the threshold.

### Q019 · Chapter 3 Memory > ESXi · Swap Consumed formula
- Files: `vsphere/technology/memory/metrics/host/swap-used`
- Search 1 (ESXi): "I think this is swapped out – swapped in"
- Search 2 (VM): "This is why Swapped is not Swapped In – Swapped Out"
- Question: is host Swap Consumed equal to swapped out minus swapped in?
- Written as now: both statements, flagged.
- Answer: Search 1 is wrong. Search 2 is correct.

### Q021 · Chapter 3 Memory > ESXi · Utilization formula
- Files: `vsphere/technology/memory/metrics/host/utilization`
- Search 1: "the sum of running VM Utilization metrics + the kernel reservation"
- Search 2: "Utilization. Machine Demand + ESX System Usage"
- Question: is the kernel part the kernel reservation or ESX System Usage? Are they the same thing?
- Written as now: both forms, flagged. Note: Provider Objects > Capacity says "Memory \\ ESX System Usage (KB)" is the kernel reservation (legacy name). If so, the two forms agree; please confirm.
- Answer: They are the same thing. See my book for Reservation. The metric name is Memory \ ESX System Usage (KB). It is a raw counter from vCenter. Just in case you’re wondering, the name ESX System Usage is a legacy name.

### Q022 · Chapter 4 Storage > Architecture · IP storage read and network direction
- Files: `vsphere/technology/storage/metrics/virtual-motherboard/disk-latency`
- Search: "Read and Write are both mapped to Transmit counter"
- Question: for a read, the data returns to ESXi as received traffic. Do reads show mostly as Receive (data) with only the command on Transmit?
- Written as now: both map to Transmit, as in the book.
- Answer: book was wrong. Answer is If you are using IP storage, take note that Read and Write in storage do not map 1:1 to Transmit (Tx) and Receive (Rx) in Networking metrics. This depends on the storage block size (normally 4K or 8K), network packet size (ideally 9000 MTU), and TCP/IP handshakes packets. Get detail from https://docs.google.com/document/d/1E7Or6rsJZ_P1MUZZfL1X3RSXPxhR2lW2fSp3wcaqnGo/edit?usp=sharing and add it accordingly.
- Done 2026-11-04: `vsphere/technology/storage/concepts/ip-storage-network-accounting` (from the linked note); disk-latency corrected, with a `corrections` entry until the book is updated.

### Q039 · Auto Test > Golden case vendor-neutral-general-001 · Hyperscaler cost not in the knowledge base
- Files: `benchmark/cases/vendor-neutral/general/general-001-hyperscaler-cost-of-1000-vms.md`
- Search: not from the book.
- Question: add hyperscaler cost content to the knowledge base, or score this case in baseline mode only?
- Written as now: the knowledge base has no cost content. In knowledge-base modes every model chose "Not covered" (frontier: 10 of 10 runs). Baseline frontier: correct 5 of 5.
- Answer: remove the case. Cost and price management is out of scope: the knowledge base is about performance troubleshooting (author, 2026-11-04). Case deleted; its id is not reused.
### Q001 · Chapter 2 CPU > VM · Linux Steal Time
- Files: `vsphere/technology/cpu/metrics/virtual-motherboard/overlap`, `vsphere/technology/cpu/metrics/virtual-motherboard/latency`
- Search 1 (Chapter 1): "Steal Time in Linux only includes CPU Ready"
- Search 2 (CPU > VM > Overlap): "Linux Guest OS tracks this as Stolen time"
- Question: does Linux Steal Time include Ready only, Overlap only, or both?
- Written as now: both statements, flagged.
- Answer: CPU Ready only. Because ESXi accounts for Overlap as active CPU Run time rather than wait time, it bypasses the hypervisor steal-time accumulator. The hypervisor does not report this interrupted time to the guest OS as stolen. The Linux OS Steal Time metric remains completely blind to vCPU Overlap. This ESXi accounting behavior necessitates the VCF Operations Net Run = Run - Overlap metric to determine actual execution time.

### Q002 · Chapter 2 CPU > VM · System charged to vCPU 0
- Files: `vsphere/technology/cpu/metrics/virtual-motherboard/system`, `vsphere/technology/cpu/metrics/virtual-motherboard/used`
- Search 1: "this is charged to the VM CPU 0"
- Search 2 (diagram text): "Charged at VM level, not at vCPU 1"
- Question: is System charged to vCPU 0 or to the VM level only? Chapter 1 says per-vCPU Used excludes System.
- Written as now: charged to vCPU 0, flagged.
- Answer: Charged at VM level, not vCPU 0 or 1. This results in Total VM cost > sum of all vCPU. This is not a problem for CPU scheduling. It’s just the way the kernel does the CPU accounting. 

### Q003 · Chapter 2 CPU > VM · Run for sizing
- Files: `vsphere/technology/cpu/metrics/virtual-motherboard/run`, `vsphere/technology/cpu/metrics/comparisons/vm-vs-esxi-ht-ramp-test`
- Search 1: "suitable as input to size the Guest OS and not the VM"
- Search 2: "This counter is suitable for VM Capacity sizing"
- Question: is Run for Guest OS sizing, VM sizing, or both?
- Written as now: both statements, flagged.
- Answer: Guest OS. I've updated my document.

### Q004 · Chapter 2 CPU > VM · Contention formula condition
- Files: `vsphere/technology/cpu/metrics/virtual-motherboard/contention`
- Search: "Other Wait (if less than 1%)"
- Question: what does the condition mean?
- Written as now: formula copied as is.
- Answer: The condition of < 1% is added to ensure no false positive. See https://knowledge.broadcom.com/external/article/338438/increased-vmwait-for-idle-vms-after-upgr.html

### Q005 · Chapter 2 CPU > VM · Contention and limit
- Files: `vsphere/technology/cpu/metrics/virtual-motherboard/contention`, `vsphere/technology/cpu/metrics/virtual-motherboard/latency`
- Search 1: "Unlike CPU Ready, it does not account for Limit"
- Search 2: "Why does the counter include Ready by Limit?"
- Question: is the first statement about the pre-July-2024 Contention, which mapped to Latency?
- Written as now: yes, pre-July-2024 Contention excludes limit; current Contention includes it.
- Answer: This is VCF Operations counter, not vSphere. vSphere does not have counter. vSphere has CPU Latency, also known as %LAT_C in esxtop. The formula for CPU Contention changed in VCF Operations 8.18

### Q006 · Chapter 2 CPU > VM · Used above Run
- Files: `vsphere/technology/cpu/diagnosis/run-vs-used-gap`
- Search: "Why is Used consistently 41% higher than Run?"
- Question: how does Ready make Used higher than Run?
- Written as now: the book's answer (Ready), without explanation.
- Answer: Book was wrong. Answer is CPU frequency. The VM run at a higher clock speed due to turbo boost.

### Q007 · Chapter 2 CPU > VM · Ready and VM size
- Files: `vsphere/technology/cpu/metrics/virtual-motherboard/ready`, `vsphere/technology/cpu/concepts/vcpu-states`
- Search 1 (VM): "CPU Ready tends to be higher, ceteris paribus, in larger VMs"
- Search 2 (Architecture): "You can reduce Co-stop by reducing the VM size"
- Question: does downsizing reduce Ready too, or only Co-stop?
- Written as now: both statements, flagged.
- Answer: It should reduce both, as the VM can be slot more easily. On the other than, having smaller share can increase CPU Ready.

### Q008 · Chapter 2 CPU > VM · Ramp test
- Files: `vsphere/technology/cpu/metrics/comparisons/vm-vs-esxi-ht-ramp-test`
- Search: "ESXi CPU Core Utilization (%) matches VM Run. Both went 2x."
- Question: Core Utilization stayed at 100%. Should this read Utilization (%)?
- Written as now: Utilization (%).
- Answer: Correct. Make it clearer by using Thread Utilization instead of just Utilization.

### Q009 · Chapter 2 CPU > ESXi · Demand: provider or consumer
- Files: `vsphere/technology/cpu/metrics/host/demand`
- Search 1: "Demand is consumer-view, while Usage is provider view"
- Search 2: "The value you see at ESXi is the summation of all the VMs"
- Question: your correction (2026-11-02) says ESXi Demand is a provider metric. Which holds?
- Written as now: both, flagged.
- Answer: The providers have 2 types of counters:
•	Provider metric. This metric does not exist at consumer. For example, the physical network in ESXi.
•	Sum of Consumer metric. This metric aggregates the metric of consumers. For example, the sum of VM network in the ESXi.

### Q010 · Chapter 2 CPU > ESXi · Usage cap
- Files: `vsphere/technology/cpu/metrics/host/usage`
- Search: "Usage no longer capped at 100% of total capacity at the nominal frequency"
- Question: your correction says capped at 100% (KB pending). Is the cap only in vCenter, removed in VCF Operations since Aria Operations 8.18?
- Written as now: vCenter capped; VCF Operations not capped since 8.18.
- Answer: Cap have been removed in both. Add the KBs https://knowledge.broadcom.com/external/article/417702/esxi-host-reporting-over-100-cpu-usage.html and https://knowledge.broadcom.com/external/article/431027/esxi-host-cpu-usage-appears-high-in-vcen.html

### Q011 · Chapter 2 CPU > ESXi · CPU Imbalance
- Files: `vsphere/technology/cpu/metrics/host/imbalance`
- Search: "ESXi CPU Imbalance = Count of Running Threads / Count of Running Cores"
- Question: built-in VCF Operations metric, or your own?
- Written as now: product tagged vsphere and vcf-operations, flagged.
- Answer: my own metric, not built-in. Add reference to https://github.com/e1-rahabok/VCF-vCommunity-Adapter/tree/main/docs/reference/metrics

### Q012 · Chapter 3 Memory > Architecture · 3 levels
- Files: `vsphere/technology/memory/concepts/memory-layers`
- Search: "ESXi uses 3 levels to manage memory"
- Question: the list after it has 4 items (TPS, Tiered Memory, Balloon, Compress/Swap). Which are the 3 levels?
- Written as now: 4 mechanisms listed, no level count.
- Answer: 4 level. Book corrected.

### Q013 · Chapter 3 Memory > Architecture · Balloon and unmet demand
- Files: `vsphere/technology/memory/concepts/memory-layers`, `vsphere/technology/memory/metrics/virtual-motherboard/ballooned`
- Search: "The first sign of unmet demand"
- Question: the next sentences say ballooning does not mean ESXi is unable to meet demand. Is balloon a sign of memory pressure rather than unmet demand?
- Written as now: proactive, not unmet demand.
- Answer: The first sign of memory pressure, not unmet demand. It's a grey matter as memory management has gradient as ESXi applies 4 different layers.
- Applied 2026-11-03.

### Q014 · Chapter 3 Memory > VM · Limit and balloon
- Files: `vsphere/technology/memory/metrics/virtual-motherboard/ballooned`, `vsphere/technology/memory/concepts/ballooning`
- Search 1: "Does limit result in Balloon?" (the book answers no)
- Search 2: "heavily ballooned as limit was imposed on it"
- Search 3: "Since the VM needed more, it experienced heavy ballooning"
- Search 4 (Memory > ESXi): "If you actually see balloon, that means there is limit imposed"
- Search 5 (Memory > ESXi): "It takes longer to realize, and is not affected by limit"
- Question: does a limit cause ballooning?
- Written as now: both, flagged.
- Answer: The answer is not directly. Why an in-between answer? Go back to the 4 layers of memory. They are at different level on memory management. Limit results in swapped or compressed is Consumed tries to grow beyond. Consumed grows because Guest OS uses more. These uses can come from balloon driver or other processes.

### Q015 · Chapter 3 Memory > VM · Memory Latency: space or time
- Files: `vsphere/technology/memory/metrics/virtual-motherboard/latency`, `vsphere/technology/memory/concepts/memory-as-storage`
- Search 1 (Architecture): "percentage of memory space"
- Search 2 (VM): "the amount of time a vCPU spends waiting on the completion of a page fault"
- Question: is Memory Latency a share of space or a share of time?
- Written as now: both definitions, flagged. vCenter description says time.
- Answer: Search 1 is wrong. Book updated. The correct answer is Search 2. Memory Latency, aka "Page-fault latency" is tracking the amount of time a vCPU spends waiting on the completion of a page fault. Its value is mostly swap wait, with a bit of page decompression / copy-on-write-break. The counter is called %LAT_M in esxtop. The latency metric is highly corelated with the swap-in rate.

### Q016 · Chapter 3 Memory > VM · Meaning of Compressed and Swapped
- Files: `vsphere/technology/memory/metrics/virtual-motherboard/swapped`, `vsphere/technology/memory/concepts/memory-layers`
- Search 1 (VM): "indicates that the host is unable to satisfy the VM memory requirement"
- Search 2 (Architecture): "It does not mean VMs were contending for RAM"
- Question: which holds?
- Written as now: Architecture statement in the concept file; VM statement flagged.
- Answer: VM compressed happens when ESXi Consumed is very high or a particular VM hit its limit. That Consumed page of a VM can contain a lot of cache, so it does not always translate to VM hitting latency.

### Q017 · Chapter 3 Memory > VM · Sharing savings
- Files: `vsphere/technology/memory/metrics/virtual-motherboard/shared`, `vsphere/technology/memory/metrics/virtual-motherboard/consumed`
- Search: "Savings = 29.83 TB"
- Question: Consumed = Granted - Savings gives 23.7 TB of savings, not 6.13 TB. Which is right?
- Written as now: the book's calculation, flagged.
- Answer:

### Q018 · Chapter 3 Memory > VM · Utilization 5%
- Files: `vsphere/technology/memory/metrics/virtual-motherboard/utilization`
- Search: "We add 5% of Total, not Used"
- Question: where does the 5% enter the formula?
- Written as now: formula and the 5% statement, flagged.
- Answer:

### Q034 · Quiz > CPU > Q2 VM CPU Speed · 80% vs 62.5% Hyper-Threading charge
- Files: `benchmark/cases/vsphere-cpu-005-likely-vcpu-speed-on-a-busy-hyper-threaded-cluster.md`, `vsphere/technology/cpu/metrics/virtual-motherboard/usage`, `vsphere/technology/cpu/metrics/virtual-motherboard/used`
- Search 1 (quiz key): "3.0 (All Cores Turbo) x 80% (as HT delivers 1.25x total)"
- Search 2 (book): "37.5%"
- Question: the quiz key gives 3.0 GHz x 80% = 2.4 GHz. The knowledge base charges each thread 62.5% when both threads run, which gives 1.875 GHz. Which factor does VM CPU Usage apply?
- Written as now: case uses the key (2.4 GHz), flagged in Notes. KB unchanged.
- Answer: Author (2026-11-03): the key is correct (2.4 GHz). Added All-Core Turbo knowledge to `vsphere/technology/cpu/concepts/cpu-frequency`.

### Q035 · Quiz > CPU > Q6 VM CPU Contention · Demand and Hyper-Threading
- Files: `benchmark/cases/vsphere-cpu-009-counters-where-a-vcpu-cannot-run-at-all.md`, `vsphere/technology/cpu/metrics/virtual-motherboard/demand`
- Search 1 (quiz key): "G is wrong as Demand is affected by hyper threading"
- Search 2 (book, MS Windows table): "| VM CPU Demand   | Yes               | No             | Yes           |"
- Question: the key says Demand is affected by Hyper-Threading. The MS Windows table marks Demand as not affected. Which is right?
- Written as now: case keeps the key's answer (G wrong); reason flagged.
- Answer: Author (2026-11-03): the key is correct. Guest OS and VM are 2 realms; the Guest OS does not see physical threads. Added to `vsphere/foundations/vm-vs-guest-os`, `vsphere/technology/cpu/metrics/virtual-motherboard/demand`, `vsphere/technology/cpu/concepts/guest-os-vs-vm-cpu`.

### Q036 · Quiz > CPU > Q7 Guest OS CPU · Is F correct?
- Files: `benchmark/cases/vsphere-cpu-010-guest-os-run-queue-context-switch-windows-thread-states.md`
- Search 1 (quiz key): "F is correct. Windows has 8 states."
- Question: the answer column says D, E. The explanation says F is correct. Is the answer D, E, F?
- Written as now: scored as D, E, F until answered.
- Answer: Author (2026-11-03): F is correct. Answer D, E, F.

### Q037 · Quiz > Cost and Price > Q1 VM Cost · Missing explanations
- Files: `benchmark/cases/vendor-neutral/general/general-001-...`
- Search 1 (quiz key): "C is correct. The VM costs around US$ 2000 per year."
- Question: the key has empty explanations for A, B and D. What is the reason each is wrong? Which pricing date and source should the case record?
- Written as now: answer C only; no reasons for the others.
- Answer: Author (2026-11-03): tracked as a to-do in project/todo.md. Closed 2026-11-04: case removed (see Q039).

- None yet. Earlier resolved questions are recorded in each file's `review_notes`.
