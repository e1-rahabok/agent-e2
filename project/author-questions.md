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
- Source to check: vSphere 9.1 documentation, vSphere Availability, Cluster Resources Percentage Admission Control, Computing the Current Available Capacity (project/sources/vmware-vsphere-9-1.pdf, p. 1971).
- Question: add the three facts to the file (Claude drafts them from the vSphere 9.1 pages on your accept)?
  - A. Yes: add them; 0330 runs again.
  - B. No: retire 0330.
- Recommended: A; percentage admission control is the default policy and 0330 tests the reading most operators get wrong.
- Answer:

### Q245 · VCF Operations > Alerts · Alert-level wait and cancel cycles, criticality, Child and Descendant

- Files: [Alert definitions](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/alert-definitions.md); questions [0274](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-086-alert-wait-cycles-symptom-and-alert-level.md), [0275](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-045-one-alert-warning-and-critical-symptoms.md), [0340](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-102-resource-pool-alert-nested-pool.md).
- Now: the body states the symptom wait and cancel cycles only; it does not state the alert-level Wait Cycle and Cancel Cycle, how they stack on the symptom cycles, Symptom Based criticality (the most critical triggered symptom), or the Child (one level below) and Descendant relationships. The keys of 0274, 0275 and 0340 rest on these vendor facts.
- Source to check: VCF Operations 9.1 TechDocs, Alert Definition Best Practices and Defining Alerts (techdocs.broadcom.com).
- Question: add these facts to the file?
- Recommended: yes; until then the three keys rest on vendor documents cited in their Notes.
- Answer:

### Q246 · Storage > Adapter Highest latency · Plain or command-weighted mean of read and write

- Files: [Storage adapter and path](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/metrics/host/adapter-and-path.md), [VM disk latency](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/metrics/virtual-motherboard/disk-latency.md); question [0072](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-025-vcenter-adapter-highest-latency.md).
- Now: adapter-and-path says Highest latency averages read and write per adapter first; disk-latency says a total latency is a command-weighted average, "not (read latency + write latency) / 2". If the adapter counter is command-weighted, options A, C and E of 0072 flip.
- Source to check: vSphere Web Services API 9.1, storage adapter counters (`storageAdapter.maxTotalLatency`); a lab export with unequal read and write rates settles it.
- Question: which is it for the adapter's Highest latency?
  - A. Plain mean of read and write latency per adapter.
  - B. Weighted by commands.
- Recommended: a lab check; 0072 keeps its key (A) until then.
- Answer:

### Q247 · Guest OS > Linux memory · A Linux memory file

- Files: none yet (proposed guest-os/memory/linux-memory); [Guest OS sizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/system/guest-os-sizing.md); questions [0272](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-085-linux-oom-kill-from-a-cgroup-limit.md), [0387](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-063-linux-guest-free-memory-low-all-week.md), [0079](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-027-memory-reclaim-from-40-vms.md).
- Now: no knowledge file states Linux available against free memory, the page cache, cgroup v2 memory.max and memory.high, the OOM kill text, that /proc/vmstat swap counters count since boot, the meaning of /proc/pressure/memory, or how VCF Operations derives Guest Needed Memory on Linux. 0272 rests on the Linux kernel documentation (an outside-the-knowledge-base question, design.md 3.5); 0387 C and D rest on PSI and vmstat semantics.
- Question: write a Linux memory file for 1.0 (Claude drafts from kernel.org documentation on your accept), or keep Linux after 1.0 (plan.md, After 1.0)?
- Recommended: a short file now; three running questions lean on it.
- Answer:

### Q248 · Network > Port group drops · Option A of 0345 and the drop formula

- Files: [Distributed switch packets dropped](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/network/metrics/distributed-switch/packets-dropped.md); question [0345](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-107-port-group-drops-received-or-transmitted.md).
- Now: the knowledge base does not define the VCF Operations port group drop percentage (dropped / packets, or dropped / (dropped + delivered)). A first reviewer read option A of 0345 as false; an independent blind checker read it as true (the key). The audit reworded A and the stem ("of which ... were dropped") so A is true as keyed; the disagreement is recorded here as the safety rule asks.
- Source to check: VCF Operations 9.1 metric definitions, port group network metrics.
- Question: confirm the key of 0345 (A) as now worded, and the formula?
- Recommended: confirm; add the formula to the file.
- Answer:

### Q249 · Memory > Tiering · Two pairs of lines disagree

- Files: [Memory tiering](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/memory-tiering.md); question [0384](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-061-vm-wait-on-the-nvme-memory-tier.md) (option H), coverage gaps left unwritten.
- Now: section "Touching a page on NVMe" says one fetch at a high latency on an idle device does not slow the VM; a misconception line says otherwise. Section Interactions says a reservation splits between DRAM and NVMe only when the reserved VMs exceed DRAM, and elsewhere that a tiered VM is not kept in DRAM. 0384 H depends on the first pair.
- Question: which line of each pair holds on 9.1?
- Recommended: settle both from the vSphere 9.1 memory tiering pages (pp. 1848-1872 of project/sources/vmware-vsphere-9-1.pdf) or a lab check.
- Answer:

### Q250 · Overhead · VM logging and vSAN as overhead

- Files: [Overhead](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/architecture/overhead.md); question [0017](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-010-overhead-classification.md).
- Now: the file counts VM log files and vSAN space as overhead; vSphere 9.1 (p. 1024, Enable logging) makes VM logging optional, and vSAN protection is a chosen capability. 0017 B and K rest on the file's definition.
- Question: keep the definition (0017 stays), or narrow it (0017 B and K are rewritten)?
- Recommended: keep it with one line on why optional items still count as overhead in capacity planning.
- Answer:

### Q251 · Benchmark levels · Relabels that conflict with the pairing plan or your earlier labels

- Files: question files below; [project/question-pairing-2026-11-14.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/question-pairing-2026-11-14.md) (items C20, C26).
- Now: the audit kept your labels and the pairing plan's levels where reviewers disagreed, and changed others on the merits. Kept against a reviewer: [0420](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-088-vm-receive-drops-linux-shows-none.md) at 300 (reviewer: 400), [0415](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-134-small-packets-telemetry-vm.md) at 400 (reviewer: 300), [0364](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-050-ready-read-against-run.md) at 300 (reviewer: 400; it is the Level 400 example in KNOWLEDGE-ENGINEERING.md section 4), [0362](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-049-esxi-cpu-demand-vcenter-vs-vcf-operations.md) at 300 (yours), [0025](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-010-balloon-0-while-swapped-and-compressed-are-not-0.md) at 400 (yours, Q056). Changed against the pairing plan: [0390](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-064-vsan-host-consumed-in-maintenance-mode.md) and [0403](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-074-one-vm-waits-while-host-latency-stays-low.md) 400 to 300 (practical halves). Kept as the Level 100-200 basics guard (your decision for this audit), although the reviewers judged them Level 300 as written: 0187 (100), 0039, 0041, 0043, 0045, 0049, 0271, 0273 (200).
- Question: accept, or name the ones to set back?
- Recommended: accept; set 0364 to 400; for the eight guard questions, either keep the label and simplify the question, or relabel it 300 and write a new basic question in its place.
- Answer:

### Q252 · Guest OS sizing · "VM Active shows the limit" for applications that manage their own memory

- Files: [Guest OS sizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/system/guest-os-sizing.md) (section Applications that manage their own memory), [SQL Server memory](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/memory/sql-server-memory.md), [VM Active](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/virtual-motherboard/active.md); question [0079](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-027-memory-reclaim-from-40-vms.md) (option L).
- Now: guest-os-sizing says VM Active "shows the limit" of an application that manages its own memory; sql-server-memory and active say Active shows what was touched, not the configured limit. 0079 L is keyed on the second reading.
- Question: correct the guest-os-sizing line?
- Recommended: yes, to "Active shows what the application touched, not its configured limit".
- Answer:

### Q253 · Network > esxtop units · The misconception line points the wrong way

- Files: [esxtop network units against the vSphere Client](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/tools/esxtop/network-units-vs-vsphere-client.md) (section Misconceptions); question 0412 (option K).
- Now: the line reads "esxtop shows 125 times more traffic than vCenter, so one tool is wrong". The same file's conversion (esxtop Mbps ≈ vSphere Client KBps × 8 / 1,000) makes the vCenter number about 125 times larger than the esxtop number, so the observation in the quote is reversed. A reader who trusts the line picks 0412 K.
- Question: reword the quote to "vCenter shows 125 times more traffic than esxtop, so one tool is wrong"?
- Recommended: yes.
- Answer:

## Future release

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
