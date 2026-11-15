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

### Q236 · Terms · Better name for ESXi CPU Usage (%)

- Files: [glossary](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/glossary.md) (entry ESXi CPU Usage (%)).
- Now: your answer of 2026-11-15 settled five names (resolved file). One is left: ESXi CPU Usage (%) → CPU Throughput (% of nominal). It is activity (work done against the base clock), so it fits your rule that throughput is activity.
- Question: accept, keep the label as it is, or give your name?
- Recommended: accept. It pairs with CPU Throughput, your Q203 name for Usage (MHz).
- Answer: Accepted

### Q237 · Catalog > KPI · Interval of three cluster KPI rows

- Files: [thresholds-performance.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-performance.yaml) (`kpi`, ClusterComputeResource); [cluster-performance](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/cluster-performance.md); [esxi-performance](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/esxi/esxi-performance.md).
- Now: three cluster rows carry their levels under `5m`: Worst memory wait among all VMs [0, 1, 2, 4, 8], 90th percentile memory wait among VMs [0, 0.5, 1, 2, 4], 90th percentile read/write latency among VM virtual disks [0, 20, 40, 60, 80]. Their ESXi twins carry the same levels under `20s`, and performance-kpi-design reads VM stats at their 20-second peak (`mem|20_sec_peak_host_contentionPct`, `virtualDisk|20_sec_peak_totalLatency_average`).
- Question: which interval do the three cluster rows use?
  - A. 20s, as the ESXi rows: move the levels.
  - B. 5m on purpose: the cluster reads a 5-minute value; cluster-performance states why.
  - C. Other.
- Recommended: A. Same metric source and same levels as the ESXi rows; under 5m the agent compares a 20-second peak with a 5-minute band.
- Answer: A

### Q238 · Capacity > Overhead · Static memory for ESXi, vSAN and NSX

- Files: [overhead](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/architecture/overhead.md) (section Recommended static values).
- Now: the table gives 64 GB of host memory for ESXi + vSAN + NSX and about 20 GB for ESXi only. Broadcom KB 420935 (ESXi 8.x and 9.x, https://knowledge.broadcom.com/external/article/420935), as read on 2026-11-15, sets aside host RAM by socket count: 64-256 GB for 2 sockets (default 128 GB), 128-384 GB for 4, 256-768 GB for 8; its examples give 64 GB per TB of installed memory.
- Question: which value does usable capacity subtract?
  - A. Keep 64 GB: your field value for the full stack.
  - B. The KB default (128 GB on 2 sockets).
  - C. Both: the KB by host size, with 64 GB as the field value for a given host size.
- Recommended: C. The KB scales with installed memory; one static number fits one host size.
- Answer: A. The KB is outdated. You should know as there is no more 4 socket ESXi. 2 socket are rare. Most are single socket.

### Q239 · CPU > Frequency · Likely vCPU speed on a busy cluster

- Files: [cpu-frequency](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/concepts/cpu-frequency.md) (section Likely vCPU speed on a busy cluster).
- Search: "likely vCPU speed = All-Core Turbo × 0.8".
- Now: the formula uses 0.8. Your Q225 answer and Broadcom KB 335065 give 0.625 of the core to a vCPU whose sibling thread runs and 1.0 when the sibling is halted, so 0.8 holds when the sibling runs about half the time. The file also says most cores run 2 threads on a busy cluster, which points below 0.8.
- Question:
  - A. Keep 0.8 as the field figure for a busy cluster, and state the assumption (sibling busy about half the time).
  - B. A range, 0.625 to 1.0 × All-Core Turbo, by how busy the sibling threads are.
- Recommended: B, unless your field data supports 0.8.
- Answer: A. You're confusing Turbo with HyperThreading. 

### Q240 · Capacity > Models · Memory row of Cluster Consumption and Cluster Risk

- Files: [cluster-consumption](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-consumption.md), [cluster-risk](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-risk.md); [ESXi Memory Utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/host/utilization.md) (section Reason).
- Now: this review settled the capacity counter of a host from Q221 and Q178: capacity reads ESXi Memory Utilization; Consumed is the capacity counter only on a host that runs with no ballooning by design, because Consumed holds guest cache. The two cluster models read `mem|consumed_average` as their utilization row, with ballooned, compressed, swapped and the NVMe tier as saturation rows (Q178 d).
- Question: keep Consumed in the models?
  - A. Keep Consumed and say why: the models assume a performance-first cluster that should not balloon, and the saturation rows catch the overflow.
  - B. Switch the utilization row to ESXi Memory Utilization (`mem|total_need`).
  - C. Consumed for classes that must not balloon, Utilization for the others.
- Recommended: A for 1.0 (the models describe the pack as built); B or C with the pack fixes after 1.0.
- Answer: A. Utilization is mixing realm as it includes Guest OS counters. Consumed is a conservative counter. Most clusters with no memory tiering should have balloon as the risk of actual contention is operationally negligible.

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

### Q243 · CPU > Used · "CPU Used is buggy"

- Files: [ESXi CPU Used](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/used.md), [VM CPU Used](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/used.md).
- Search: "CPU Used is buggy".
- Now: both files say "CPU Used is buggy. Do not build conclusions on it alone." No bug is named, so the model cannot say what is wrong or what to read instead.
- Question:
  - A. Name the mechanism: the two Hyper-Threading rules (VM CPU Used 62.5% per vCPU with a busy sibling, ESXi CPU Used 50% per thread; Q225) and Turbo make it hard to read; read Run and Ready with it.
  - B. A specific defect: give the KB or the case.
  - C. Delete the line.
- Recommended: A.
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
