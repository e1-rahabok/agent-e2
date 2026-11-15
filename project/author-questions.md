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

### Q236 · Terms · Better names for six product labels

- Files: [glossary](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/glossary.md) (entries with `Better name:`); [KNOWLEDGE-ENGINEERING.md](https://github.com/e1-rahabok/agent-e2/blob/main/KNOWLEDGE-ENGINEERING.md) (Product label and better model).
- Now: Q208 is built. Agent E2 quotes the product label as it is, then gives the better model and a better name. Six names are new terms, so they need your OK:
  - Total Capacity (GHz) → Nominal CPU Throughput
  - ESXi CPU Usage (%) → CPU Throughput (% of nominal)
  - VM CPU Latency → CPU Throughput Loss
  - ESXi Memory Usage (%) → ESXi Memory Claimed (%)
  - VM Memory Consumed → VM Memory Claimed
  - Capacity Remaining (%) → 3-Day Forecast Remaining (%)
- Question: accept all, or change some? For a change, write the label and your name.
- Recommended: accept. The CPU names form one family with CPU Throughput (your Q203 answer); "Nominal" is the glossary's word for base clock. "Claimed" says pages held, not pages in use, and pairs with reclamation.
- Answer:

### Q207 · Benchmark > Field set · Real questions from you

- Files: [benchmark/live-test.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/live-test.md) (step 9); [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md) (7.5, held-out set); [harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md) (4.6, coverage boundary).
- Now: every benchmark question was written from the knowledge files, in their words. Only real operator questions show how often a question falls outside the knowledge base, and how search copes with an operator's words. Stems alone already lose much: recall 83% to 72% (retrieval check, 2026-11-15).
- Question: can you give real questions? Tickets, consulting cases, customer emails, chats. Text only, as asked; no answer needed; kept out of the repository.
  - A. Yes, now. About how many?
  - B. At release only.
  - C. None. The 20 of the live test are enough.
- Recommended: A.
- Answer:

## Future release

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
