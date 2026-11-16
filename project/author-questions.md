# Questions for the author

Not indexed. One entry per question.

How to answer:

- Write your reply after `Answer:`. Any length; a letter is enough where there are options.
- Leave `Answer:` empty to skip a question for now.
- Tell Claude the file is updated. Claude applies each answer and moves the entry to [author-questions-resolved.md](author-questions-resolved.md).
- Two sections: Release 1.0 (answer before release 1.0) and Future release.

Each entry:

- Files: the files the answer changes.
- Search: verbatim strings, only for a question about the book.
- Now: what the knowledge base says today.
- Question: what Claude needs from you, with options where they help.
- Recommended: Claude's choice and the reason.
- Answer: for you.

## Release 1.0

### Q244 · Cluster > HA admission control · Three vendor facts for the percentage policy

- Files: [Admission control and cluster state](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/concepts/admission-control-and-cluster-state.md); question [0330](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-100-ha-failover-percentage-uneven-hosts.md) (deferred until answered).
- Now: the file has none of: the 32 MHz CPU (0 MB memory) default that a powered-on VM without a reservation counts in the percentage policy; the Insufficient Failover Resources warning when a manual percentage is below the share of the largest hosts; the power-on test against the configured percentage. Its line "A VM with no reservation passes CPU and memory admission control" leads a reader away from the key of 0330.
- Research (2026-11-16): confirmed in the vSphere 9.1 PDF, p. 1971: a powered-on VM with no reservation counts 32 MHz CPU (`das.vmcpuminmhz`) and 0 MB memory; admission control disallows the operation when the Current CPU or Memory Failover Capacity is below the Configured Failover Capacity (step 4). Not confirmed: the Insufficient Failover Resources warning for a manual percentage below the share of the N largest hosts. No vSphere 9.1 PDF page, no TechDocs 8.0 or 9.0 page has it. The vendor fault is named "Insufficient Resources to Satisfy Configured Failover Level for HA" (p. 1949); Broadcom KB 424373 describes "Insufficient configured resources to satisfy the desired vSphere HA failover level" for the opposite case (percentage above current capacity); a 2018 post by Duncan Epping (not official) covers one host's share, not N hosts.
- Source to check: vSphere 9.1 documentation, vSphere Availability, Cluster Resources Percentage Admission Control, Computing the Current Available Capacity (project/sources/vmware-vsphere-9-1.pdf, p. 1971).
- Question: add the two confirmed facts, and rewrite 0330 without the warning half?
  - A. Yes: add the 32 MHz / 0 MB default and the power-on test against the configured percentage; 0330 asks only the power-on result (the warning options go).
  - B. No: retire 0330.
- Recommended: A. Both facts are in the vendor text; the warning is not, so no file or key states it.
- Answer:

### Q246 · Storage > Adapter Highest latency · Plain or command-weighted mean of read and write

- Files: [Storage adapter and path](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/metrics/host/adapter-and-path.md), [VM disk latency](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/metrics/virtual-motherboard/disk-latency.md); question [0072](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-025-vcenter-adapter-highest-latency.md).
- Now: adapter-and-path says Highest latency averages read and write per adapter first; disk-latency says a total latency is a command-weighted average, "not (read latency + write latency) / 2". If the adapter counter is command-weighted, options A, C and E of 0072 flip.
- Source to check: vSphere Web Services API 9.1, storage adapter counters (`storageAdapter.maxTotalLatency`); a lab export with unequal read and write rates settles it.
- Research (2026-11-16): the vSphere Web Services API 9.1 (and 9.0, 8.0) defines `storageAdapter.maxTotalLatency`, label Highest latency, only as "Highest latency value across all storage adapters used by the host" (statistics level 3, rollup latest, host aggregate). No vendor text says how one adapter combines read and write. The adapter group has no per-adapter total latency counter; the disk group defines total latency as kernel plus device latency per command. The author's own screenshot note shows the value below the read latency, which fits both readings. The files disagree: adapter-and-path says averaged per adapter, disk-latency (a different counter) says command-weighted, datastore says "a normalized average".
- Question: which is it for the adapter's Highest latency?
  - A. Plain mean of read and write latency per adapter.
  - B. Weighted by commands.
  - C. Not documented: all three files say "blends read and write per adapter"; 0072 depends only on its CSV.
- Recommended: C. Write one phrase in the three files (the vendor definition, then "blends read and write per adapter; the weights are not documented"). Rewrite 0072 A, C and E so that they hold under both readings (read and write command counts about equal in its CSV, or the options read the CSV numbers only); key unchanged. A lab check (90/10 and 50/50 read/write mix, compare with both formulas) settles it later: Future release.
- Answer:

### Q248 · Network > Port group drops · Option A of 0345 and the drop formula

- Files: [Distributed switch packets dropped](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/network/metrics/distributed-switch/packets-dropped.md); question [0345](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-107-port-group-drops-received-or-transmitted.md).
- Now: the knowledge base does not define the VCF Operations port group drop percentage (dropped / packets, or dropped / (dropped + delivered)). A first reviewer read option A of 0345 as false; an independent blind checker read it as true (the key). The audit reworded A and the stem ("of which ... were dropped") so A is true as keyed; the disagreement is recorded here as the safety rule asks.
- Research (2026-11-16): VCF Operations 9.1 TechDocs (updated 2026-11-12), Distributed Virtual Port Group Metrics and VMware Distributed Virtual Switch Metrics: one percentage metric, Percentage of Dropped Packets (`network|port_statistics|dropped_pkts_pct`, "Percentage of dropped packets"), no split by direction and no denominator; the rates Egress and Ingress Dropped Packets per second (`dropped_tx_pkts`, `dropped_rx_pkts`), Total Dropped Packets per second, and Total Ingress and Egress Packets per second (`rx_pkts`, `tx_pkts`). The vSphere API has no percentage counter. Host and VM `net|droppedPct` are also undefined. So the vendor gives no formula, and the question's 0.5% is plain arithmetic on its own numbers (0.19 of 38.0 million).
- Source to check: VCF Operations 9.1 metric definitions, port group network metrics.
- Question: confirm the key of 0345 (A) as now worded, and add a formula?
- Recommended: confirm A (it uses no vendor metric); add no formula. Add the vendor metric names to the file, say the denominator is not documented, and say a per-direction share is computed from the rate metrics (`dropped_tx_pkts` over `tx_pkts`), not a vendor metric. A lab check (compare `dropped_pkts_pct` with dropped / (rx + tx) and dropped / (rx + tx + dropped)) can come later.
- Answer:

### Q249 · Memory > Tiering · Two pairs of lines disagree

- Files: [Memory tiering](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/memory-tiering.md); question [0384](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-068-vm-wait-on-the-nvme-memory-tier.md) (option H), coverage gaps left unwritten.
- Now: section "Touching a page on NVMe" says one fetch at a high latency on an idle device does not slow the VM; a misconception line says otherwise. Section Interactions says a reservation splits between DRAM and NVMe only when the reserved VMs exceed DRAM, and elsewhere that a tiered VM is not kept in DRAM. 0384 H depends on the first pair.
- Research (2026-11-16): the vSphere 9.1 PDF says nothing about an idle NVMe device or a wake-up delay, so pair 1 is the author's lab fact. Pair 2: p. 1969 (and 1872 of the memory tiering chapter) says a tiered VM's "configured memory reservation is served from NVMe" and its overhead stays in DRAM, and that memory reservations (not pinned memory) "can be split between DRAM and the NVMe tiers" when the reserved VMs' consumed memory exceeds DRAM. That is an example, not a condition.
- Question: which line of each pair holds on 9.1?
  - Pair 1: A. "one fetch ... does not slow the VM"; B. "the VM that touched the page waited 900 µs".
  - Pair 2: A. a reservation splits only when the reserved VMs exceed DRAM; B. a tiered VM's reservation can be served from NVMe in any case.
- Recommended: pair 1 B (the touching vCPU waits for the fetch; reword the first line to "delays the vCPU once; a few fetches cost little, not nothing"); pair 2 B (drop "only when": keep the vendor example as an example). 0384 H stays false; key A, C unchanged.
- Answer:

### Q250 · Overhead · VM logging as overhead

- Files: [Overhead](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/architecture/overhead.md); question [0017](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-010-overhead-classification.md).
- Now: the file counts VM log files as overhead; vSphere 9.1 (p. 1024, Enable logging) makes VM logging a setting. 0017 B rests on the file's definition. The vSAN half of this question moved to Future release (Q254, author, 2026-11-16); 0017 no longer tests vSAN.
- Research (2026-11-16): the vSphere 9.1 PDF, p. 228, advanced configuration parameters: the `logging` option disables all VM logging and "Do not use this setting, because disabling virtual machine logging makes it difficult or impossible to get support for virtual machine problems." So logging is on by default and the vendor says to keep it on.
- Question: keep VM log files as overhead (0017 B stays)?
- Recommended: yes. Add one line to overhead.md: logging can be switched off but the vendor says not to (p. 228), so it is mandatory in practice and costs disk space and IO.
- Answer:

### Q253 · Network > esxtop units · The misconception line points the wrong way

- Files: [esxtop network units against the vSphere Client](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/tools/esxtop/network-units-vs-vsphere-client.md) (section Misconceptions); question 0412 (option K).
- Now: the line reads "esxtop shows 125 times more traffic than vCenter, so one tool is wrong". The same file's conversion (esxtop Mbps ≈ vSphere Client KBps × 8 / 1,000) makes the vCenter number about 125 times larger than the esxtop number, so the observation in the quote is reversed. A reader who trusts the line picks 0412 K.
- Research (2026-11-16): checked. 1,000 Mbps is 125,000 KBps, so the vCenter number is 125 times larger than the esxtop number; the file's own conversion and 0412's key point K say the same.
- Question: reword the quote to "vCenter shows 125 times more traffic than esxtop, so one tool is wrong"?
- Recommended: yes.
- Answer:

## Future release

### Q245 · VCF Operations > Alerts · Alert-level wait and cancel cycles, criticality, Child and Descendant

- Moved to Future release by the author, 2026-11-16. Impact: 0274, 0275 and 0340 are deferred (status `deferred`); their keys are unchanged and wait for the alert definitions content (plan.md, After 1.0).

- Files: [Alert definitions](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/alert-definitions.md); questions [0274](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-086-alert-wait-cycles-symptom-and-alert-level.md), [0275](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-053-one-alert-warning-and-critical-symptoms.md), [0340](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-102-resource-pool-alert-nested-pool.md).
- Now: the body states the symptom wait and cancel cycles only; it does not state the alert-level Wait Cycle and Cancel Cycle, how they stack on the symptom cycles, Symptom Based criticality (the most critical triggered symptom), or the Child (one level below) and Descendant relationships. The keys of 0274, 0275 and 0340 rest on these vendor facts.
- Source to check: VCF Operations 9.1 TechDocs, Alert Definition Best Practices and Defining Alerts (techdocs.broadcom.com).
- Question: add these facts to the file?
- Recommended: yes; until then the three keys rest on vendor documents cited in their Notes.
- Answer:

### Q247 · Guest OS > Linux memory · A Linux memory file

- Moved to Future release by the author, 2026-11-16. Impact: no file is written. 0272 stays in the run set as an outside-the-knowledge-base question (design.md 3.5), 0387 stays (its Linux facts are in linux-os-slow), 0079 has no Linux option; keys unchanged.

- Files: none yet (proposed guest-os/memory/linux-memory); [Guest OS sizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/system/guest-os-sizing.md); questions [0272](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-085-linux-oom-kill-from-a-cgroup-limit.md), [0387](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-070-linux-guest-free-memory-low-all-week.md), [0079](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-027-memory-reclaim-from-40-vms.md).
- Now: no knowledge file states Linux available against free memory, the page cache, cgroup v2 memory.max and memory.high, the OOM kill text, that /proc/vmstat swap counters count since boot, the meaning of /proc/pressure/memory, or how VCF Operations derives Guest Needed Memory on Linux. 0272 rests on the Linux kernel documentation (an outside-the-knowledge-base question, design.md 3.5); 0387 C and D rest on PSI and vmstat semantics.
- Question: write a Linux memory file for 1.0 (Claude drafts from kernel.org documentation on your accept), or keep Linux after 1.0 (plan.md, After 1.0)?
- Recommended: a short file now; three running questions lean on it.
- Answer:

### Q252 · Guest OS sizing · "VM Active shows the limit" for applications that manage their own memory

- Moved to Future release by the author, 2026-11-16. Impact: guest-os-sizing keeps its line for now. 0079 L stays keyed on active.md and sql-server-memory.md (VM Active shows what was touched); a model that reads only the guest-os-sizing line can answer L false. Fixing the line is a one-line change.

- Files: [Guest OS sizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/system/guest-os-sizing.md) (section Applications that manage their own memory), [SQL Server memory](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/memory/sql-server-memory.md), [VM Active](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/virtual-motherboard/active.md); question [0079](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-027-memory-reclaim-from-40-vms.md) (option L).
- Now: guest-os-sizing says VM Active "shows the limit" of an application that manages its own memory; sql-server-memory and active say Active shows what was touched, not the configured limit. 0079 L is keyed on the second reading.
- Question: correct the guest-os-sizing line?
- Recommended: yes, to "Active shows what the application touched, not its configured limit".
- Answer:

### Q254 · Overhead · vSAN as overhead (after 1.0)

- Moved to Future release by the author, 2026-11-16 (from Q250). Impact: 0017 no longer tests vSAN (E and K replaced; key A, B, F, K unchanged).
- Files: [Overhead](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/architecture/overhead.md) (vSAN processes, FTT policy, the Misconceptions line on FTT).
- Now: the file counts vSAN processes as overhead and the FTT copy as not overhead. Other questions lean on vSAN too and still run: 0390 (vSAN host Consumed in maintenance mode), 0056 (host Consumed with no VMs), 0080 (datastores running out of space: four options on vSAN space), 0215, 0217, 0296, 0409, 0069. They are not changed: Q250 named 0017 only.
- Question: when vSAN content is written, check the overhead lines against it, and decide for the questions above whether they move to after 1.0 too (0390 and 0080 are the most vSAN-keyed).
- Recommended: move 0390 and 0080 to after 1.0 if vSAN is out of 1.0 as a whole; keep the others, where vSAN is the setting and not the fact tested.
- Answer:

### Q241 · CPU > VM Demand · Demand under a limit (lab check)

- Files: [VM CPU Demand](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/demand.md) (section Not unmet demand, two misconceptions).
- Now: the file's lab test shows VM CPU Demand equal to Usage under a limit, so Demand is not unmet demand. The vSphere Web Services API 9.1 defines `cpu.demand` as the CPU a VM would use with no CPU contention or CPU limit, which says the opposite.
- Question: repeat the limit test on a 9.1 host (a VM with a CPU limit below its load; read Demand, Usage, Ready, Max Limited)?
  - A. Demand stays at Usage: keep the text and record a correction against the API definition.
  - B. Demand rises above Usage: follow the API and rewrite the section and the misconceptions.
- Recommended: run the test; until then the text stays with a review note.
- Answer:

### Q242 · Storage > esxtop · QAVG above KAVG

- Files: [ESXi storage latency stack](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/concepts/esxi-storage-latency-stack.md) (section Counters, one misconception).
- Now: "QAVG can exceed KAVG: QAVG covers VM IO and kernel IO; KAVG covers VM IO only", and the misconception "QAVG cannot exceed KAVG" → QAVG includes kernel IO. The ESXi disk queue note in project/sources gives KAVG = QAVG + VMkernel processing, so QAVG would never exceed KAVG.
- Question:
  - A. Keep the line: you have seen QAVG above KAVG in esxtop.
  - B. Follow the source note: KAVG includes QAVG; drop the misconception.
- Recommended: A only with field evidence, else B.
- Answer:

### Q222 · SP5 > Availability · Does a host in maintenance mode lower availability?

- Files: [IaaS SLAs](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/sla-metrics.md) (Availability SLA); [Cluster availability](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/metrics/availability.md).
- Now:
  - sla-metrics: the maintenance window is always excluded (your Q098 answer). One host in maintenance: Operational Availability 100%.
  - Cluster availability: the ESXi state score takes 25% off a host in maintenance mode.
- Question: which availability is the cluster score?
  - A. Actual Availability. Maintenance counts.
  - B. Operational Availability. Maintenance does not count; the 25% row goes.
  - C. A third score. The file gives it its own name.
- Recommended: C. The state score measures operations maturity (a host left in maintenance too long is a finding); the SLA measures the service. Two purposes, two names.
- Answer:

### Q226 · SP5 > Availability · Usable hosts during maintenance: 8 or 9 of 10?

- Files: [IaaS SLAs](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/sla-metrics.md) (the 10-host example); [Supply](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/supply.md) (Total vs usable after host loss).
- Search: "Example on a 10-host cluster with 1 HA host (usable 9 hosts)".
- Now:
  - 10 hosts, 1 HA host, 1 host in maintenance.
  - supply: usable 8. HA admission control leaves a host in maintenance out and keeps its reserve among the other 9 (vSphere 9.1).
  - sla-metrics: Operational Availability divides by usable 9.
- Question: which divisor does Operational Availability use?
  - A. Planned usable (9), whatever the maintenance. Availability measures the planned service; usable capacity is what is safe now.
  - B. Usable during the event (8). Maintenance never lowers availability.
  - C. Your design lets the HA host cover maintenance. supply then shows two views: protected (8) and unprotected (9).
- Recommended: A.
- Answer:

### Q235 · Sizing > VM CPU sizing note · Levels and units of the decision matrix

- Files: [VM CPU Sizing Best Practices](https://github.com/e1-rahabok/agent-e2/blob/main/project/sources/vm_cpu_sizing_best_practices.md) (Sizing Decision Matrix, Post-Resize Verification); [rightsizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/rightsizing.md) (Before vs after).
- Now: no number from the note is in the knowledge base. rightsizing has the verification step only.
- Questions:
  1. Queue unit. The matrix reads a total (10, 11-25, above 25 threads). The verification table reads per vCPU (2-3, above 10). Which one?
  2. Ready above 5% and Co-stop above 3% keep the VM at 10 vCPUs. A: use the KPI levels instead (yellow at 2% Ready, 1% Co-stop, 20-second peak). B: a separate sizing rule.
  3. N%L above 90% healthy, below 85% a red flag. Give a source, or drop it.
  4. 14 or 15 vCPUs on a 16-core node, to leave room for hypervisor interrupts. Field experience or a document?
- Recommended: 1 per vCPU (VCF Operations shows the queue per vCPU, Q217). 2 A (one place per number). 3 drop. 4 yours.
- Answer:

### Q216 · CPU > NUMA > Virtual NUMA · Topology rebuild and `numa.autosize.once` (lab checks)

- Files: [Virtual NUMA](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/concepts/virtual-numa.md) (Topology initialization, Misconceptions); [NUMA sizing guide](https://github.com/e1-rahabok/agent-e2/blob/main/project/sources/vmware_vsphere_numa_architecture_and_sizing_guide.md) (section 4).
- Now: the guide says ESXi rebuilds the vNUMA topology at every power cycle. vSphere 9.1 says it stays until the vCPU count changes, and lists `numa.autosize.once` (default TRUE). Both stay unverified in the file.
- Lab checks, text output only:
  - (a) `numa.allowHotadd`: hardware 20 or later, 12+ vCPUs, CPU Hot Add on. Power on without the option, then with it. Each time paste `lscpu | grep -i numa` (Linux) or `coreinfo -n` (Windows), and `grep -i numa <vm>.vmx` on the host.
  - (b) Persistence: a VM wider than one NUMA node (24 vCPU). Paste the guest NUMA output and the vmx lines. Power off, vMotion to a host with another node size, power on, paste again.
  - (c) `numa.autosize.once`: is it in the vmx after the first power-on? Add it as FALSE, repeat (b).
- Answer:

### Q124 · Storage > Unmap · Unmap counters per datastore

- Files: [ESXi Datastore metrics](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/metrics/host/datastore.md) (section Unmap); [esxtop storage](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/tools/esxtop/storage.md).
- Search: "but you can’t aggregate them per datastore".
- Now: unmap counters live on the ESXi host, one instance per datastore. No datastore total across hosts. Counter keys only in a review note.
- Proposed from vendor sources (Claude applies on your accept):
  - Keys `datastore.unmapIOs.summation` (count) and `datastore.unmapSize.summation` (MB), per host and datastore. Not in the 9.1 API pages; seen in live vCenter 7 and 8 lists.
  - Datastore total: sum the hosts that mount it. Complete, since each unmap comes from one host.
  - Per 20 seconds. A VCF Operations 5-minute point is the mean of 15: MB in 5 minutes = value × 15.
  - The vsish counters reset at reboot and when no VM on the host uses the datastore (Broadcom KB 374191).
- For you, in VCF Operations 9.1: does the Datastore object have an unmap metric? What are the Host System metric keys?
- Answer:

### Q129 · VCF Operations 9.1 · Real-time metrics API for scripts

- Files: [Real-time metrics](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/features/real-time-metrics.md).
- Now: "data is queried with PromQL"; no API section.
- Proposed from the Broadcom API reference (https://developer.broadcom.com/xapis/realtime-metrics-api/latest/; Claude applies on your accept):
  - Prometheus-style endpoints: GET `/api/v1/query`, `/api/v1/query_range`, `/api/v1/metadata`; PUT `/api/v1/vcenters/{vcId}/metrics_config`.
  - `sourceId` (vCenter UUID) required from API 9.1.1. Paged responses.
  - Auth: OpsToken from `/suite-api/api/auth/token/acquire`, exchanged for a JWT with the VCF_VODAP service key.
- For you, one call in your lab: which host answers the API (VCF Operations or the real-time component)? Does the esxtop feature return 2-second data through it?
- Answer:

### Q149 · Term map · Wrong terms users write

- Files: [user-terms.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/user-terms.yaml).
- Now: rows written from the knowledge base; none from real tickets.
- Question: which wrong terms do admins write in tickets and chats, and what do they mean? Example: "steal time" means VM CPU Ready and Co-stop. A list of term → meaning is enough.
- Ready to add on your accept, from the knowledge base: "latency" with no layer; VM network latency; "ESXi Ready"; "Ready 5%" or "2000 ms"; "VM consumed memory high"; thin provisioning; DRS Score; esxtop load average; SIOC shares (ignored from VCF 9.0); "memory pressure".
- Answer:

### Q150 · URL questions · Public pages with known errors

- Files: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md) (section 3.4).
- Now: no URL question in the run set.
- Candidates, still published with the error (fetched 2026-11-14):
  - Broadcom KB 419238, Troubleshooting VM performance: %RDY ≥ 10 with no per-vCPU reading; %DRPTX above 0 read as high utilization.
  - Broadcom KB 386180, CPU Ready with high I/O: fixed Ready and Co-stop levels; its capture runs 112.5 minutes, not 15.
  - TechDocs 9.1, Solutions for Memory Performance Problems: "94% or greater" usage and "6% or less" free read as pressure.
  - TechDocs 9.1, Solutions for Poor Network Performance: dropped packets read as a network bottleneck.
  - Broadcom KB 326296: strict co-scheduling; %CSTP above 3 with no per-vCPU reading.
  - Broadcom KB 415396: "focus on active memory".
- Question: accept these, drop some, or add pages you know are wrong?
- Answer:
