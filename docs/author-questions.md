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

### Q001 · Chapter 2 CPU > VM · Linux Steal Time
- Files: `vsphere/cpu/metrics/virtual-machine/overlap`, `vsphere/cpu/metrics/virtual-machine/latency`
- Search 1 (Chapter 1): "Steal Time in Linux only includes CPU Ready"
- Search 2 (CPU > VM > Overlap): "Linux Guest OS tracks this as Stolen time"
- Question: does Linux Steal Time include Ready only, Overlap only, or both?
- Written as now: both statements, flagged.
- Answer:

### Q002 · Chapter 2 CPU > VM · System charged to vCPU 0
- Files: `vsphere/cpu/metrics/virtual-machine/system`, `vsphere/cpu/metrics/virtual-machine/used`
- Search 1: "this is charged to the VM CPU 0"
- Search 2 (diagram text): "Charged at VM level, not at vCPU 1"
- Question: is System charged to vCPU 0 or to the VM level only? Chapter 1 says per-vCPU Used excludes System.
- Written as now: charged to vCPU 0, flagged.
- Answer:

### Q003 · Chapter 2 CPU > VM · Run for sizing
- Files: `vsphere/cpu/metrics/virtual-machine/run`, `vsphere/cpu/metrics/comparisons/vm-vs-esxi-ht-ramp-test`
- Search 1: "suitable as input to size the Guest OS and not the VM"
- Search 2: "This counter is suitable for VM Capacity sizing"
- Question: is Run for Guest OS sizing, VM sizing, or both?
- Written as now: both statements, flagged.
- Answer:

### Q004 · Chapter 2 CPU > VM · Contention formula condition
- Files: `vsphere/cpu/metrics/virtual-machine/contention`
- Search: "Other Wait (if less than 1%)"
- Question: what does the condition mean?
- Written as now: formula copied as is.
- Answer:

### Q005 · Chapter 2 CPU > VM · Contention and limit
- Files: `vsphere/cpu/metrics/virtual-machine/contention`, `vsphere/cpu/metrics/virtual-machine/latency`
- Search 1: "Unlike CPU Ready, it does not account for Limit"
- Search 2: "Why does the counter include Ready by Limit?"
- Question: is the first statement about the pre-July-2024 Contention, which mapped to Latency?
- Written as now: yes, pre-July-2024 Contention excludes limit; current Contention includes it.
- Answer:

### Q006 · Chapter 2 CPU > VM · Used above Run
- Files: `vsphere/cpu/diagnosis/run-vs-used-gap`
- Search: "Why is Used consistently 41% higher than Run?"
- Question: how does Ready make Used higher than Run?
- Written as now: the book's answer (Ready), without explanation.
- Answer:

### Q007 · Chapter 2 CPU > VM · Ready and VM size
- Files: `vsphere/cpu/metrics/virtual-machine/ready`, `vsphere/cpu/concepts/vcpu-states`
- Search 1 (VM): "CPU Ready tends to be higher, ceteris paribus, in larger VMs"
- Search 2 (Architecture): "You can reduce Co-stop by reducing the VM size"
- Question: does downsizing reduce Ready too, or only Co-stop?
- Written as now: both statements, flagged.
- Answer:

### Q008 · Chapter 2 CPU > VM · Ramp test
- Files: `vsphere/cpu/metrics/comparisons/vm-vs-esxi-ht-ramp-test`
- Search: "ESXi CPU Core Utilization (%) matches VM Run. Both went 2x."
- Question: Core Utilization stayed at 100%. Should this read Utilization (%)?
- Written as now: Utilization (%).
- Answer:

### Q009 · Chapter 2 CPU > ESXi · Demand: provider or consumer
- Files: `vsphere/cpu/metrics/host/demand`
- Search 1: "Demand is consumer-view, while Usage is provider view"
- Search 2: "The value you see at ESXi is the summation of all the VMs"
- Question: your correction (2026-11-02) says ESXi Demand is a provider metric. Which holds?
- Written as now: both, flagged.
- Answer:

### Q010 · Chapter 2 CPU > ESXi · Usage cap
- Files: `vsphere/cpu/metrics/host/usage`
- Search: "Usage no longer capped at 100% of total capacity at the nominal frequency"
- Question: your correction says capped at 100% (KB pending). Is the cap only in vCenter, removed in VCF Operations since Aria Operations 8.18?
- Written as now: vCenter capped; VCF Operations not capped since 8.18.
- Answer:

### Q011 · Chapter 2 CPU > ESXi · CPU Imbalance
- Files: `vsphere/cpu/metrics/host/imbalance`
- Search: "ESXi CPU Imbalance = Count of Running Threads / Count of Running Cores"
- Question: built-in VCF Operations metric, or your own?
- Written as now: product tagged vsphere and vcf-operations, flagged.
- Answer:

### Q012 · Chapter 3 Memory > Architecture · 3 levels
- Files: `vsphere/memory/concepts/memory-layers`
- Search: "ESXi uses 3 levels to manage memory"
- Question: the list after it has 4 items (TPS, Tiered Memory, Balloon, Compress/Swap). Which are the 3 levels?
- Written as now: 4 mechanisms listed, no level count.
- Answer:

### Q013 · Chapter 3 Memory > Architecture · Balloon and unmet demand
- Files: `vsphere/memory/concepts/memory-layers`, `vsphere/memory/metrics/virtual-machine/ballooned`
- Search: "The first sign of unmet demand"
- Question: the next sentences say ballooning does not mean ESXi is unable to meet demand. Is balloon a sign of memory pressure rather than unmet demand?
- Written as now: proactive, not unmet demand.
- Answer:

### Q014 · Chapter 3 Memory > VM · Limit and balloon
- Files: `vsphere/memory/metrics/virtual-machine/ballooned`, `vsphere/memory/concepts/ballooning`
- Search 1: "Does limit result in Balloon?" (the book answers no)
- Search 2: "heavily ballooned as limit was imposed on it"
- Search 3: "Since the VM needed more, it experienced heavy ballooning"
- Search 4 (Memory > ESXi): "If you actually see balloon, that means there is limit imposed"
- Search 5 (Memory > ESXi): "It takes longer to realize, and is not affected by limit"
- Question: does a limit cause ballooning?
- Written as now: both, flagged.
- Answer:

### Q015 · Chapter 3 Memory > VM · Memory Latency: space or time
- Files: `vsphere/memory/metrics/virtual-machine/latency`, `vsphere/memory/concepts/memory-as-storage`
- Search 1 (Architecture): "percentage of memory space"
- Search 2 (VM): "the amount of time a vCPU spends waiting on the completion of a page fault"
- Question: is Memory Latency a share of space or a share of time?
- Written as now: both definitions, flagged. vCenter description says time.
- Answer:

### Q016 · Chapter 3 Memory > VM · Meaning of Compressed and Swapped
- Files: `vsphere/memory/metrics/virtual-machine/swapped`, `vsphere/memory/concepts/memory-layers`
- Search 1 (VM): "indicates that the host is unable to satisfy the VM memory requirement"
- Search 2 (Architecture): "It does not mean VMs were contending for RAM"
- Question: which holds?
- Written as now: Architecture statement in the concept file; VM statement flagged.
- Answer:

### Q017 · Chapter 3 Memory > VM · Sharing savings
- Files: `vsphere/memory/metrics/virtual-machine/shared`, `vsphere/memory/metrics/virtual-machine/consumed`
- Search: "Savings = 29.83 TB"
- Question: Consumed = Granted - Savings gives 23.7 TB of savings, not 6.13 TB. Which is right?
- Written as now: the book's calculation, flagged.
- Answer:

### Q018 · Chapter 3 Memory > VM · Utilization 5%
- Files: `vsphere/memory/metrics/virtual-machine/utilization`
- Search: "We add 5% of Total, not Used"
- Question: where does the 5% enter the formula?
- Written as now: formula and the 5% statement, flagged.
- Answer:

### Q019 · Chapter 3 Memory > ESXi · Swap Consumed formula
- Files: `vsphere/memory/metrics/host/swap-used`
- Search 1 (ESXi): "I think this is swapped out – swapped in"
- Search 2 (VM): "This is why Swapped is not Swapped In – Swapped Out"
- Question: is host Swap Consumed equal to swapped out minus swapped in?
- Written as now: both statements, flagged.
- Answer:

### Q020 · Chapter 3 Memory > ESXi · Consumed and compressed
- Files: `vsphere/memory/metrics/host/consumed`
- Search 1: "It only includes the resultant zipped, not the amount subjected to compression"
- Search 2: "Consumed does not include compressed"
- Question: does host Consumed include the compressed result in DIMM?
- Written as now: includes the result, flagged. Your diagram (physical view) also shows it inside Consumed.
- Answer:

### Q021 · Chapter 3 Memory > ESXi · Utilization formula
- Files: `vsphere/memory/metrics/host/utilization`
- Search 1: "the sum of running VM Utilization metrics + the kernel reservation"
- Search 2: "Utilization. Machine Demand + ESX System Usage"
- Question: is the kernel part the kernel reservation or ESX System Usage? Are they the same thing?
- Written as now: both forms, flagged. Note: Provider Objects > Capacity says "Memory \\ ESX System Usage (KB)" is the kernel reservation (legacy name). If so, the two forms agree; please confirm.
- Answer:

### Q022 · Chapter 4 Storage > Architecture · IP storage read and network direction
- Files: `vsphere/storage/metrics/virtual-machine/disk-latency`
- Search: "Read and Write are both mapped to Transmit counter"
- Question: for a read, the data returns to ESXi as received traffic. Do reads show mostly as Receive (data) with only the command on Transmit?
- Written as now: both map to Transmit, as in the book.
- Answer:

### Q023 · Chapter 4 Storage > VM · Disk metric scope
- Files: `vsphere/storage/metrics/virtual-machine/disk`
- Search: "if the value is per VM or per disk"
- Question: is the VM Disk (device-level) metric value for this VM only, or for the whole device shared by many VMs?
- Written as now: associated with the VM, flagged as unsure.
- Answer:

### Q024 · Chapter 5 Network > Architecture · VM and ingress
- Files: `vsphere/network/concepts/network-observability`
- Search: "That’s why a VM does not have ingress traffic"
- Question: if moving further inside is ingress, traffic arriving at a VM looks like ingress. What does "a VM does not have ingress traffic" mean? That VM metrics use receive/transmit instead?
- Written as now: definitions only; the VM statement is flagged.
- Answer:

### Q025 · Chapter 5 Network > VM · Dropped packet volume
- Files: `vsphere/network/metrics/virtual-machine/packets-dropped`
- Search: "1 thousand packets dropped = 1500 MB worth of packets within 300 seconds"
- Question: 1,000 × 1.5 KB = 1.5 MB. Should it be 1 million packets = 1,500 MB, or 1,000 packets = 1.5 MB?
- Written as now: flagged, no number stated.
- Answer:

### Q026 · Consumer Objects > Performance · Compressed + Swapped threshold
- Files: `vsphere/system/metrics/virtual-machine/vm-performance`
- Search: "their threshold is 2x of memory contention"
- Question: the table gives Compressed + Swapped green at 0-0.25%, half of Memory Contention (0-0.5%), not 2x. Which is intended?
- Written as now: the table values, with the conflict flagged.
- Answer:

### Q027 · Consumer Objects > Capacity · VM CPU Needed formula
- Files: `vsphere/system/concepts/vm-footprint-sizing`
- Search: "VM CPU Needed = (Used + Overlap + Co-stop + Ready + Other Wait) + System"
- Question: is the whole sum divided by 20,000, or only System? VM-level Used already includes System (Chapter 2 VM, Used formula). Is System counted twice?
- Written as now: formula copied as is, flagged.
- Answer:

### Q028 · Consumer Objects > Capacity · Balloon in Guest OS memory sizing
- Files: `vsphere/system/concepts/guest-os-sizing`
- Search: "Exclude balloon"
- Question: the text excludes balloon, but the sizing table marks Ballooned in blue (include) with "The memory was taken by Tools". Include or exclude?
- Written as now: exclude, flagged.
- Answer:

### Q029 · Consumer Objects > Capacity · Memory utilization ranges
- Files: `vsphere/system/concepts/guest-os-sizing`
- Search: "The company is wasting money if the utilization falls below 50%"
- Question: the text gives waste below 50% and risk above 75%, which matches bar 1. You recommend bar 2, where green starts near 75%. What are the ranges for bar 2?
- Written as now: bar 2 recommended, no numbers stated.
- Answer:

### Q030 · Provider Objects > Performance · vMotion in Cluster Performance (%)
- Files: `vsphere/system/metrics/cluster/cluster-performance`
- Search 1: "vMotion is not included as it only becomes an issue"
- Search 2: "vMotion is included as it does impact the VM performance"
- Question: is vMotion part of the cluster KPI or not? The threshold table has no vMotion row.
- Written as now: vMotion described as a leading indicator, flagged.
- Answer:

### Q031 · Provider Objects > Performance · Cluster KPI table vs text
- Files: `vsphere/system/metrics/cluster/cluster-performance`
- Search 1: "Storage troubleshooting differs to compute troubleshooting" (disk latency listed as not used)
- Search 2: "That’s why it’s given 4x the threshold of zipped + swapped" (balloon thresholds)
- Search 3: "I did not set green = 0"
- Question: the table includes disk latency rows, has no balloon or swapped rows, and sets packet green to 0%. Is the table or the text current?
- Written as now: the table, with text reasons listed and the conflict flagged.
- Answer:

### Q032 · Provider Objects > Other Metrics · Monster VM threshold
- Files: `vsphere/system/metrics/cluster/cluster-risk`, `vsphere/system/concepts/cluster-operations`
- Search 1 (Overview): "If a VM vCPU > 45% of the ESXi count of threads"
- Search 2 (Monster VM): "if a VM vCPU size is > 40% of the ESXi count of threads"
- Search 3 (Cluster Risk): "the VM size needs to be at least half the ESXi"
- Search 4 (recommendation): "Monster VM > 50% of physical core, not thread"
- Question: which CPU threshold defines a monster VM?
- Written as now: the recommendation (above 50% of physical cores); the others flagged.
- Answer:

### Q033 · MS Windows > CPU > Usage | Utilization | Time · VM CPU Run and Hyper-Threading
- Files: `vsphere/cpu/concepts/windows-cpu-scheduling`, `vsphere/cpu/metrics/virtual-machine/run`
- Search 1 (MS Windows table): "Which VM counters can be used when you have no visibility into the Guest"
- Search 2 (Chapter 2, Run | Net Run): "counter not affected by CPU frequency scaling and hyper threading"
- Question: the MS Windows table marks VM CPU Run as Yes in the Hyperthreading column. Chapter 2 says Run is not affected by Hyper-Threading. Which is right?
- Written as now: the table as in the book, marked with the conflict; `run` keeps the Chapter 2 statement.
- Answer:

## Resolved
- None yet. Earlier resolved questions are recorded in each file's `review_notes`.
