# Questions for the author

Not indexed. One entry per question.

How to answer:

- Write your reply after `Answer:` under each question. Any length.
- Leave `Answer:` empty to skip a question for now.
- Then tell Claude the file is updated. Claude applies each answer and moves the entry to [author-questions-resolved.md](author-questions-resolved.md): resolved means done, kept as history.
- Two files: this one holds every open question, in two sections, Release 1.0 (answered before release 1.0) and Future release (a later release); [author-questions-resolved.md](author-questions-resolved.md) holds the answered ones.
- `Final answer:` (2026-11-12) is the answer proposed for your review. It replaces the drafts of 2026-11-10 and 2026-11-11 and the partly-settled notes: it is checked against the knowledge base as it is now, the decisions in project/plan.md and your answers up to [Q179](author-questions-resolved.md#q179--memory-tiering-rows-for-cluster-consumption-cluster-performance-and-cluster-risk--proposal-for-review). Its status says how it was reached: settled (by an earlier answer or decision, named), expert call, or needs you. `For you:` names what only you can give; "nothing" means accept or change. In `Answer:`, write accept, accept with changes, or your own answer.

Each entry has:

- Section: book chapter and Heading 3.
- Files: knowledge-base files affected.
- Search: verbatim strings to find in the book, only for a question about the book. A question about this repository links its files instead.
- Written as now: what the knowledge base currently says.

## Release 1.0

### Q166 · ARCHITECTURE.md, section Flow questions · Code evaluates flow branches

- Files: [harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md) (sections 4.3 and 6); [harness/flows.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/flows.py); [harness/agent.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/agent.py) (stage 3); [project/knowledge-rules/flows.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/knowledge-rules/flows.md); [VM slow](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/vm-slow.md); [VM CPU Contention or Latency is high](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high.md); [project/design-thresholds.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/design-thresholds.md).
- What the knowledge base says now (review 2026-11-14): the agent puts the best flow of the question's kind first in the reading set (tier 1) and the model follows its numbered steps and picks the branch. `flows.py` parses every flow into steps, but only lint and the unit tests call it; stage 3 (compute) has no flow step yet. The tool-loop `flow` tool this question was written against is removed.
- Question: (a) executable steps: the model extracts values into a case state, code compares them with catalog thresholds and picks the branch, the model explains; (b) keep as is.
- Proposed answer: (a), for 1.0, starting with the VM slow flow.
- Answer (2026-11-12): Yes, (a) for 1.0.
- Applied 2026-11-12: Recorded in project/plan.md, M1 open work: executable flow steps (the model extracts values into a case state, code compares them with catalog thresholds and picks the branch), starting with the VM slow flow.
- Still open, three design points before the build (review 2026-11-14; expert call):
  - (1) First flow: [VM CPU Contention or Latency is high](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high.md), not VM slow. VM slow has one numeric test (step 4, the VM Performance (%) band); its other steps are Guest OS quantification by the application team, breadth, configuration, known bugs and logs, which code cannot compare. The CPU flow has numeric tests in steps 1 (Ready, Co-stop and Overlap 20-second peaks against the KPI levels; CPU Latency), 3 (vCPUs against physical threads), 4 (vCPU count against the NUMA node) and 6 (vCPUs against cores), and the case already reads these values (`cpu.ready.summation` in ms, the vCPU count). VM slow follows as the router: step 4 picks the sub-flow from the counter that pulls VM Performance (%) down.
  - (2) Step format, one home: the numbered step stays the text the model reads; a `steps` list in the flow file's `## Metadata` holds what code needs per step: `step`, `object`, `metric` (a metric file title, so it resolves through the catalog), `test` (a catalog row by metric, object, interval and use; never a number typed in the flow), and `then` (band or outcome → next step). Lint checks that every `steps` entry matches its numbered step (metric named, targets equal to the `→ step N` arrows), as it already matches `kpi` rows to the KPI tables. The path goes to the model as computed facts: "Flow path (exact): step 1 VM CPU Ready 12% per vCPU at the 20-second peak, orange (row ...) → step 2".
  - (3) A value the case lacks: in a conversation, the agent asks for it (stage 4, one round). In a single-turn answer (the benchmark, a question with no reply) code stops at that step and the model states both branches with what to read. AGENT.md (stops at the first missing value) and ARCHITECTURE.md (ask, or state both branches) say this in parts; the build makes it one rule.
  - Change if accepted: AGENT.md sections 4.3, 4.4 and 6.4 (first flow, format, missing value); flows.md (the `steps` list); lint; `flows.py` and stage 3 of `agent.py` with unit tests on worked examples; the retrieval check before and after.
  - (4) Thresholds the flows need, with no catalog row (review of 2026-11-14, M1): the catalog admits a row only for a KPI, alert, capacity model or decision; a flow test is none of these, so these numbers sit in prose. Proposal: a `flow` section in thresholds-performance.yaml, rows by metric, object, interval and source, each named by a flow step. Candidates: KAVG and DAVG (values: Q195); memory tiering, active memory against DRAM and NVMe read latency and bandwidth (vSphere 9.1 documentation; memory-tiering, section Performance thresholds); vMotion stun time (vm/vmotion: under 200 ms, investigate above 1 second; no source named); Guest OS context switch per processor (guest-os/cpu/metrics/context-switch: 2K, 4K, 8K; knowledge base); the high and low host of inter-host imbalance (cpu/metrics/cluster/inter-host-imbalance; no model uses it yet, so no row until one does). Fixed in the same review without a question: the Guest OS run queue table and the Windows free memory guidance now point to their KPI rows.
  - For you: accept (1)-(4), or keep VM slow first; for (4), a source for the vMotion stun values.
- Re-checked 2026-11-14: still the first build step for the real world (guided troubleshooting is a 1.0 requirement, MISSION.md, Ways to ask, 4). In the field a question arrives without options, so the flow tier and the computed path carry more of the answer than in the benchmark.
- Answer:

### Q214 · Memory > Balloon · Does a memory limit cause ballooning?

- Files: [VM Ballooned](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/virtual-motherboard/ballooned.md) (section Behaviour); [Host memory states](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/host-memory-states.md).
- Search 1: "Does limit result in Balloon?"
- Question: your earlier answer ("not directly": a limit results in swapped or compressed when Consumed tries to grow beyond it) is in the files. Two sources point the other way. The vSphere 9.1 documentation, memory performance table (p. 2037): "If free memory is available on the hosts and the virtual machines are experiencing high swap or balloon memory, the virtual machine (or resource pool) has reached its resource limit." And the file's own example: an 8 GB VM with a 2 GB limit "was heavily ballooned". A limit caps the VM's memory target, and ESXi reclaims from a VM above its target with the balloon first when the driver runs. (A) keep: under a limit the direct result is Compressed or Swapped, not Balloon; (B) a limit lowers the VM's target; ESXi reclaims above it with the balloon first, then compression and swap, even with free host memory; (C) other.
- Written as now: (A) in both files. The review of 2026-11-14 changed only the balloon maximum in the example: Mem.CtlMaxPercent, default 65% (vSphere 9.1 documentation, p. 600; was "around 63%").
- Final answer (review 2026-11-14; expert call): B. The four layers still explain why Consumed grows under a limit; they do not stop the balloon, which is how ESXi enforces the target when the driver runs.
  - Change if accepted: ballooned.md (Behaviour, a misconception line "A limit cannot cause ballooning"), host-memory-states.md. No question key depends on the line (grep, 2026-11-14).
  - For you: A, B or C.
- Answer:

### Q215 · Memory > ESXi > Utilization · ESX System Usage: vCenter counter or VCF Operations metric?

- Files: [ESXi memory utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/host/utilization.md); [Overhead](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/architecture/overhead.md) (section Memory metrics); [Memory capacity](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/memory-capacity.md); [ESXi Consumed](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/host/consumed.md); [ESXi memory metrics compared](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/comparisons/host-memory-metrics.md).
- Search 1: "ESX System Usage"
- Question: your earlier answer ("Memory \ ESX System Usage (KB). It is a raw counter from vCenter ... a legacy name") is in the files, which call it the kernel reservation. The VCF Operations 9.1 Host System metrics page (TechDocs, updated 2026-11-12) lists "Mem|ESX System Usage: Memory usage by the VMkernel and ESX user-level services", key `mem|host_systemUsage`, a key VCF Operations computes, and separately "Mem|VM kernel Usage (KB)", key `mem|sysUsage_average`, which is vCenter `mem.sysUsage` (API 9.1: "Used by VMkernel", without VMs and vSphere services). consumed.md records ESX System Usage at 57 GB on a host with no VMs while host Consumed read 17.5 GB: a reservation, not current use. (A) keep as written; (B) ESX System Usage is a VCF Operations metric (`mem|host_systemUsage`) that behaves as the kernel reservation; vCenter `mem.sysUsage` is current VMkernel use, shown in VCF Operations as VM kernel Usage; (C) other.
- Written as now: "ESX System Usage is the kernel reservation. Raw vCenter counter: Memory \ ESX System Usage (KB). The name is legacy." The same in overhead.md, memory-capacity.md, host/consumed.md and host-memory-metrics.md.
- Final answer (review 2026-11-14; expert call on the names, the reservation reading is yours): B. Sources: https://techdocs.broadcom.com (VCF Operations 9.1, Host System metrics); https://developer.broadcom.com/xapis/vsphere-web-services-api/9.1/memory_counters.html.
  - Change if accepted: the five files; a review note "To check: the formula of `mem|host_systemUsage` (not published)".
  - For you: A, B or C; and whether any vCenter 9.1 screen shows ESX System Usage.
- Answer:

### Q216 · CPU > NUMA > Virtual NUMA · `numa.*` options and the topology rebuild in vSphere 9.1

- Files: [Virtual NUMA](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/concepts/virtual-numa.md); [project/sources/vmware_vsphere_numa_architecture_and_sizing_guide.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/sources/vmware_vsphere_numa_architecture_and_sizing_guide.md) (section 4); [project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md) (After 1.0, the manual reminder on `numa.autosize.once`).
- Search: not from the book; the uploaded NUMA sizing guide, section 4.
- Question: three lines of virtual-numa come from the uploaded guide, and the vSphere 9.1 documentation says otherwise. (1) "Do not add `numa.*` attributes in the VM's Advanced Parameters: they are no longer offered there or supported" vs vSphere 9.1 (p. 1940, and TechDocs Virtual NUMA Controls, updated 2026-11-09): "You can add these advanced options"; p. 1028 uses `numa.allowHotadd` to keep vNUMA with CPU Hot Add on hardware version 20. (2) "ESXi rebuilds the topology at every power cycle" vs TechDocs 9.1, Using Virtual NUMA: the topology "does not change unless the number of vCPUs ... is changed". (3) Your decision of 2026-11-13 that the 9.1 UI no longer offers `numa.autosize.once` (the UI wins) vs p. 1945, which lists it with default TRUE. Which holds in your 9.1 lab? (A) the guide and the UI: the 9.1 manual is out of date (add these to the manual reminder); (B) the manual: `numa.*` options stay valid as VMX options, and the topology persists unless the vCPU count changes; (C) mixed: name which.
- Written as now: the guide's three statements. The review of 2026-11-14 added the CPU Hot Add rule with `numa.allowHotadd` (vSphere 9.1 p. 1028; Broadcom KB 313375), itself a `numa.*` option, so line 13 now contradicts the file's own Hot Add line.
- Final answer (review 2026-11-14): needs you (a lab check). Expert reading: B at least for `numa.allowHotadd` (documented with hardware 20 and a KB), so line 13 must allow it; (2) and (3) need the lab.
- Answer:

### Q217 · Guest OS > CPU > Run queue · Peak CPU Queue: per vCPU or total?

- Files: [Guest OS Performance (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/system/guest-os-performance.md); [Processor queue](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/cpu/metrics/run-queue.md); [Guest OS alerts](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/guest-os-alerts.md); [thresholds-performance.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-performance.yaml) (kpi row); [thresholds-alerts.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-alerts.yaml) (the queue symptom).
- Search: not from the book.
- Question: one VCF Operations metric, `guest|20_sec_peak_cpu_queue`, feeds the Guest OS Performance (%) KPI, which reads it per vCPU ("The run queue stat is already per vCPU"; zero at 16), and an alert symptom above 20 count, which run-queue.md and guest-os-alerts read as a total ("Queue 53 on 8 vCPUs"). Both cannot hold: per vCPU, 20 is past the KPI's zero. (A) per vCPU: the alert value is wrong; (B) a total: the KPI divides by the vCPU count first; (C) other.
- Written as now: both readings, in different files.
- Final answer (review 2026-11-14): needs the VCF Operations 9.1 metric definition of Guest|Peak CPU Queue, or your lab. Expert reading: B; Windows Processor Queue Length is one queue for all processors, and the alert's example reads it as a total.
- Answer:

### Q220 · CPU > Hyper-Threading · Thread Utilization with both threads busy: 100% or 200%?

- Files: [ESXi CPU Usage](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/usage.md); [Core Utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/core-utilization.md); [Hyper-Threading](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/concepts/hyper-threading.md).
- Search: not from the book.
- Question: usage.md gives Thread Utilization 100% when both threads are busy; core-utilization.md gives "200% for a core (esxtop)"; hyper-threading.md says per thread, never summed. Is the 200% an esxtop sum of the two threads of one core, or a different counter?
- Written as now: both.
- Final answer (expert call): per thread at most 100%; an esxtop core view that adds two threads reads 200%. One home: hyper-threading, section Thread Utilization; core-utilization explains the 200% as two threads at 100%. For you: confirm against the esxtop PCPU panel.
- Answer:

### Q221 · Memory > Capacity · Memory Demand: kernel Consumed or kernel reservation?

- Files: [Memory capacity](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/memory-capacity.md) (lines on Demand); [ESXi memory utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/host/utilization.md); [Demand (capacity)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/demand.md).
- Search: not from the book.
- Question: memory-capacity gives host memory Demand as kernel Consumed plus the sum of VM Demand, and a few lines later as the kernel reservation plus guest needed memory and page-in; host/utilization and sp5 capacity demand give other forms. Three models share the word Demand. Which is the capacity model, and which are the VCF Operations formulas?
- Written as now: three forms in three files.
- Final answer (expert call on the placement): the method's model goes in sp5 capacity demand; the VCF Operations formulas stay in host and VM utilization; memory-capacity points to both. The formula itself needs you.
- Answer:

### Q222 · SP5 > SLA > Availability · Does a host in maintenance mode lower Operational Availability?

- Files: [IaaS SLAs](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/sla-metrics.md) (Availability SLA); [Cluster availability](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/metrics/availability.md).
- Search: not from the book.
- Question: sla-metrics excludes scheduled downtime from Operational Availability (your Q098 answer: the maintenance window is always excluded), so one host in maintenance gives 100%; cluster availability scores a host in maintenance mode as 25% lost. Is the cluster metric (A) Actual Availability, so it may count maintenance; (B) Operational, so it should not; (C) a different score that the file should name as such?
- Written as now: both, unreconciled.
- Answer:

### Q198 · CPU > NUMA settings · NPS-1 default or the setting that matches the silicon?

- Files: [NUMA settings](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/configuration/numa-settings.md) (section AMD EPYC); [CPU topology](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/concepts/cpu-topology.md) (section NUMA); source: project/sources/vmware_vsphere_numa_architecture_and_sizing_guide.md, section 2.
- Search 1: "From vSphere 7.0 Update 2, the defaults are NPS-1"
- Search 2: "Optimal Setting: NPS4 (Nodes Per Socket 4)"
- Question: Performance Best Practices for vSphere 9.1 (revision 20260624, pp. 29-30) says NPS-1 with CCX as NUMA Domain off gives the best performance in nearly all cases, and NPS-4 is worth testing only for bandwidth-hungry, NUMA-optimized, pinned workloads. Your source gives NPS4 as the optimal setting for EPYC 9005 and NPS2 for EPYC 9006. Which does Agent E2 recommend for a general-purpose cluster: (A) NPS-1 unless the workload meets the four conditions; (B) the setting that matches the silicon (NPS4 on 9005, NPS2 on 9006); (C) B for monster VMs only?
- Written as now: both stated; cpu-topology gives the per-processor setting, numa-settings keeps the vendor default and points to this question.
- Moved back from the resolved file in the review of 2026-11-14: it had no answer.
- Answer:

### Q195 · ESXi storage I/O path · Where does a Paravirtual SCSI queue limit show?

- Files: [ESXi storage I/O path](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/concepts/esxi-storage-io-path.md) (section Queues on the path); [ESXi storage latency stack](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/concepts/esxi-storage-latency-stack.md); question [0361](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-129-two-queue-limits-on-one-virtual-disk.md) (Two queue limits on one virtual disk).
- Search 1: "pvscsi queue depth"
- Search 2: "The hypervisor software queues are throttling requests"
- Question: the ESXi source file says high KAVG and QAVG (above 2 to 5 ms) with low DAVG usually occur when the concurrent requests of a VM exceed the configured queue depths, and names the pvscsi queue depth and Disk.SchedNumReqOutstanding. The knowledge file reads the two limits apart: a request that exceeds the Paravirtual SCSI queue depth (64 per device, 254 per adapter) waits in the Guest OS, before the virtual device takes it, and shows in the Guest OS counters, not in KAVG or QAVG; a request that exceeds the VMkernel device queue depth (DQLEN) waits in the VMkernel and shows as QUED and QAVG. Which holds? And what does Disk.SchedNumReqOutstanding limit, with what default, and when?
- Also: the thresholds differ by source for KAVG and DAVG (the source file: KAVG under 1 ms ideal, high at 2 to 5 ms, DAVG high above 10 to 15 ms; Broadcom KB 344099: 10 ms for DAVG, KAVG and GAVG when sustained; the latency stack file from the book: KAVG within 0.5 ms, DAVG within 5 ms). Which values go in the threshold catalog?
- Written as now: the two limits are read apart; no number for DSNRO; no threshold repeated; flagged in review_notes of the file.
- Moved back from the resolved file in the review of 2026-11-14: it had no answer.
- Answer:

### Q193 · Guest OS sizing · Lowering SQL Server max server memory in steps

- Files: [Guest OS sizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/system/concepts/guest-os-sizing.md) (section Applications that manage their own memory); [SQL Server holds its memory](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-89-sql-server-holds-its-memory.md).
- Search: "Finding the size: lower"
- Question: the section says to lower max server memory (MB) in steps, watch the SQL Server memory counters and the query times over a full business cycle, and resize the VM after that. The Microsoft page does not say it. Is this your method? Which counters do you watch, and how large is a step?
- Written as now: the method, with no counter names and no step size; flagged in review_notes.
- Moved back from the resolved file in the review of 2026-11-14: it had no answer.
- Answer:

### Q208 · Knowledge design · Product label and better model

- Files: [KNOWLEDGE-ENGINEERING.md](https://github.com/e1-rahabok/agent-e2/blob/main/KNOWLEDGE-ENGINEERING.md) (section Product label and better model); [knowledge/glossary.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/glossary.md); [knowledge/catalog/user-terms.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/user-terms.yaml); [project/tools/tags.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/tags.yaml) (misconception_type).
- Question: from your answer to [Q203](author-questions-resolved.md#q203--cpu--capacity--name-vspheres-ghz-total-capacity-as-a-throughput-figure), a general design: every product label Agent E2 improves on is kept verbatim and paired with what it computes, the decision it invites, the better model and the better name. Accept these parts, or change them: (A) glossary entries named by the product label, with new lines `Product label:` and `Better name:`; (B) term-map rows for those labels generated from the glossary, so the note reaches the model before it reasons; (C) the five-step teaching order in every answer that meets such a label; (D) misconception type `label-read-as-model`; (E) the better name for Total Capacity (GHz): your word (a throughput figure at base clock; "Nominal Throughput" is one option). Then: which other labels belong in the first list? Candidates from the knowledge base: ESXi CPU Usage (%), VM Memory Usage (%), ESXi Memory Usage (%), Consumed, CPU Latency, Contention (VCF Operations), Capacity Remaining (%).
- Written as now: the design is a proposal; [Q203](author-questions-resolved.md#q203--cpu--capacity--name-vspheres-ghz-total-capacity-as-a-throughput-figure) applied to the two CPU files only. Not applied: no glossary entry has `Product label:` or `Better name:` lines; tags.yaml has no `label-read-as-model`; no prompt carries the teaching order. AGENT.md (section 4.5) described the teaching order as part of the answer shape: corrected in the review of 2026-11-14 to "proposed, not built".
- Final answer (review 2026-11-14; expert call for A-D and the list; E is yours):
  - A, B, D as written. B by a small generator (glossary pair → term-map row) checked by lint, so the row is never edited by hand.
  - C, narrowed: the teaching order only when the case or a term-map row names a listed label, and inside the answer length, not added to it: an operator reads a short answer, and 250 words with four key points leave no room for five extra steps (the benchmark is multiple choice since Q199, so this shapes the product's open answers, judged by you in the live test). Steps 1, 3 and 4 carry the correction; steps 2 and 5 fold into the mechanism and what to check next.
  - The list, by the test of the design (the label invites a decision its computed model does not support): ESXi CPU Usage (%) (counts frequency and Hyper-Threading; read as busy time); VM Memory Usage (%) (vCenter: Active over configured; read as "the VM needs more memory"); ESXi Memory Usage (%) (Consumed over total; read as pressure); Consumed (read as in use by the Guest OS); CPU Latency (counts frequency and Hyper-Threading; read as waiting); Capacity Remaining (%) (a projection's tightest point; read as space left now). Contention (VCF Operations) needs you: whether its 9.x formula still differs from what the label invites (Q144).
  - For you: E (the better name for Total Capacity (GHz)); accept or change the list.
- Answer:

### Q207 · Benchmark > Field set · Measure coverage on real questions

- Files: [analysis-2026-11-13.md, archived](https://github.com/e1-rahabok/agent-e2/blob/main/project/archive/benchmark-results-before-2026-11-14/analysis-2026-11-13.md) (section 12); [harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md) (section 4.6, coverage boundary); [benchmark/live-test.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/live-test.md) (step 9: 20 real questions); [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md) (section 7.5, held-out set).
- Question: 159 of the 196 questions were drafted from the knowledge files they test, so the benchmark cannot show how often a real question falls outside the knowledge base. In the round of 2026-11-13 (previous generation, archived), on your 37 questions the local configuration led the frontier model by 8-17 points; outside coverage the 30B model was far weaker than the frontier model. Proposal: a field set of about 100 real questions, collected, not written from the knowledge base (your tickets and consulting cases, customer questions, Broadcom community and forum threads). Two numbers from it: coverage (share settled by the knowledge base) and the score. Out-of-coverage answers must say so. (A) adopt it, collected now, kept out of the repository like the held-out set; (B) adopt it, collected at release only; (C) no: the live test's 20 questions are enough.
- Written as now: held-out set of 30 drawn at release in the proportions of the run set, from real questions where you have them; 20 real questions in the live test. The blueprint (target counts) was removed on 2026-11-14: the real test is the field. Built 2026-11-14: the coverage boundary (when nothing in the reading set came from a flow or a file the question names, the answer prompt says the question may be outside the knowledge base, and to say so); AGENT.md sets its search-score limit on this field set, so the field set also tunes that boundary. Recommended: A. You hold the real questions; Claude can collect public community threads (titles and questions only, no customer data).
- Re-checked 2026-11-14, after your direction "focus on Agent E2 in the real world": A matters more now. Every benchmark question is multiple choice (Q199), and its options help retrieval: the reading plan searches each option. With the options removed, as an operator asks, the retrieval check falls from 78% to 67% recall, from 116 to 85 of 196 questions with every needed file, and the main file is missing on 32 instead of 20 (`retrieval_eval.py --no-options`). Only real questions show the field number. Recommended: A, and the field set scored on open answers (judged by you), with the retrieval check run on its questions as written.
- Answer:

### Q205 · Memory > Swap and compression > Example · Gap between Consumed and the effective limit

- Files: [Swap and compression](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/swap-and-compression.md) (section Example: limit, swap and compress in opposite directions).
- Search 1: "The small gap above the limit is VM overhead" (old line, removed)
- Question: The old line said the small gap above the limit is VM overhead. In the example data, Consumed sits just under Memory|Effective limit and Granted above it. Did the line mean the gap between Consumed and Granted? Is the effective limit the configured limit plus overhead?
- Written as now: Consumed stays a little below the effective limit because the effective limit includes overhead; Granted sits above it and ignores the limit (draft, review note).
- Answer:

### Q202 · Memory > Overhead · Kernel memory reservation with vSAN and NSX

- Files: [Overhead](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/architecture/overhead.md) (section Memory metrics); question [0024](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-11-memory-reservation-behaviour.md), option E.
- Search 1: "Too low with vSAN and NSX, too high with ESXi only"
- Search 2: "Reservation stays steady even when kernel use drops"
- Question: The file says the kernel reservation is too low with vSAN and NSX (supports the key: E false), and later that the memory reservation stays steady even when kernel use drops 90% (supports E). On a busy host with vSAN and NSX, is the kernel memory reservation below actual kernel use? Should the second line be scoped to an idle or ESXi-only host?
- Written as now: both lines unchanged.
- Answer:

### Q201 · Memory > Reservation · 'Not available to VMs': admission or physical pages

- Files: [ESXi memory reservation](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/host/reservation.md); [Overhead](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/architecture/overhead.md); question [0024](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-11-memory-reservation-behaviour.md), option D.
- Search 1: "Kernel reservation means the amount is not available to VMs"
- Search 2: "reserved memory must be used first before it is held"
- Question: Option D of 0024 does not say which sense of available it means. For admission control the kernel reservation is withheld whether used or not, so D is true; for physical pages it is not withheld until touched, so D is false. Every model, Opus included, reads the first. Should D say (A) not available for VM reservations (true), (B) physically blocked before use (false), or (C) leave the misconception list?
- Written as now: an untouched reservation can serve other VMs; admission control counts the full reservation (draft, review note).
- Answer:

### Q124 · Part 1 > Reclamation > TRIM and Unmap · Per datastore

- Files: [ESXi Datastore metrics (host view)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/metrics/host/datastore.md) (section Unmap); [esxtop storage counters](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/tools/esxtop/storage.md).
- Search: "but you can’t aggregate them per datastore"
- Question: the knowledge base reads this as: the metrics are on the ESXi host with one instance per datastore, and no datastore-wide total across hosts exists. Correct?
- Written as now: "Two metrics on the ESXi host, one instance per datastore"; "Per host and datastore only: a datastore total across hosts is not available. Sum the hosts that mount it." Counter keys only in a review note ("likely datastore.unmapIOs and datastore.unmapSize"). esxtop storage lists the VAAI unmap fields (DELETE, DELETE_F, MBDEL/s), not linked from the Unmap section.
- Final answer (2026-11-12; expert call; one live check):
  - Correct, with four precisions.
  - Keys: vCenter `datastore.unmapIOs.summation` (count) and `datastore.unmapSize.summation` (MB), per host, one instance per datastore. They are not in the 9.1 API counter pages or the chart tables. ESXi keeps the same counts per volume (vsish) and per device (esxtop VAAI: DELETE, DELETE_F); both reset at reboot.
  - Total: the datastore object has no unmap counter. Sum the hosts that mount it, same interval. The sum is complete: each unmap command comes from exactly one host. The space reclamation hosts setting limits how many hosts send automatic unmap, so most hosts read 0.
  - Units: one value per 20 seconds. VCF Operations averages the 15 values of a 5-minute point: MB released in 5 minutes = value × 15; MB/s = value / 20.
  - Scope: VMFS6, and NFS through the VAAI unmap primitive.
  - Sources: vSphere 9.1 documentation (Space Reclamation); https://developer.broadcom.com/xapis/vsphere-web-services-api/9.1/datastore_counters.html (no unmap counter); Broadcom KB 374191.
  - Change if accepted: host datastore, Unmap (keys, conversions, reclamation hosts, link to the esxtop fields); close the plan item on the unmap keys (M1, VCF Operations line).
  - For you: in a live VCF Operations 9.1, confirm the Datastore object has no unmap metric, and give the Host System metric keys.
- Re-checked in the review of 2026-11-14: no unmap counter on the 9.1, 9.1.1 or latest API counter pages (datastore, disk, storage adapter, storage path, virtual disk); the vSphere 9.1 PDF has no "unmapIOs". The keys `datastore.unmapIOs.summation` (num) and `datastore.unmapSize.summation` (MB) appear only in third-party counter lists built from live vCenter 7.0 and 8.0 dumps (virten.net), not yet for 9.1. One precision for the Units bullet: Broadcom KB 374191 says the vsish counters also reset when no VM on that host runs on the datastore (the datastore is no longer monitored), not only at reboot. The live check stays yours.
- Answer:

### Q129 · VCF Operations 9.1 · Prometheus access for scripts

- Files: [Real-time metrics](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/features/real-time-metrics.md).
- Search: not from the book. TechDocs "Real-time Data in the Workbench": "Use the Add Query input field to enter and run your PromQL query."
- Question: you say 2-second metrics are for programmatic use, with native Prometheus compatibility. The 9.1 docs show PromQL only in the Workbench Custom Query sub-tab. How do scripts reach it (endpoint, auth, doc link)?
- Written as now: "Designed for programmatic consumption: data is queried with PromQL"; "Custom Query: PromQL". No API section; sources are TechDocs pages only.
- Final answer (2026-11-12; settled by vendor documentation; one live check):
  - The statement holds. Broadcom publishes Real-Time Metrics APIs for VCF 9.1 and 9.1.1: Prometheus-compatible APIs for real-time metrics from vCenter (https://developer.broadcom.com/xapis/realtime-metrics-api/latest/). Usable as a Grafana data source, down to 2-second granularity.
  - Endpoints: GET `/api/v1/query`; GET `/api/v1/query_range` (start, end, step); GET `/api/v1/metadata`; PUT `/api/v1/vcenters/{vcId}/metrics_config` (STANDARD or VERBOSE profile; the ESXi hosts for esxtop collection). Responses in Prometheus format.
  - Not stock Prometheus: `sourceId` (vCenter instance UUID, NSX id) is required; `externalTagsFilter` is optional.
  - Auth: POST `/suite-api/api/auth/token/acquire` → OpsToken; read the integration services list and take the service of type VCF_VODAP; POST `/suite-api/api/auth/token/exchange` → JWT, sent as Bearer.
  - Change if accepted: real-time-metrics, new section API for scripts (endpoints, sourceId, auth, URL); delete the review note; keep the corrections entry (the Workbench page still omits the API).
  - For you: one call in your lab: which host answers `{api_host}` (the VCF Operations FQDN or the real-time metrics component), and whether the esxtop feature returns 2-second data through the API.
- Re-checked in the review of 2026-11-14 (developer.broadcom.com, versions 9.1 and 9.1.1): the endpoints and the auth flow hold. Two corrections: `sourceId` is required only from API 9.1.1 (query and query_range; the 9.1.1 changelog: "Parameter sourceId changed required from false to true"), optional in 9.1 and on metadata; the token exchange takes a service key (`{"serviceKeys": ["<key>"]}`, the key of the integration service whose type is VCF_VODAP). Also not stock Prometheus: responses carry `pageInfo` (`nextPageToken`, `pageSize`) and a `limit` parameter. Grafana and 2-second granularity are in the VMware blog of 2026-05-25, not on the API pages.
- Answer:

### Q149 · Term map · Wrong terms users write

- Files: [knowledge/catalog/user-terms.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/user-terms.yaml).
- Search: not from the book.
- Question: list the wrong terms VMware admins and architects write in tickets, forums and chats, each with what they mean (for example "steal time" means VM CPU Ready and Co-stop). Each becomes a row: the words, the knowledge-base terms, the file, the misconception.
- Written as now: 41 rows, none from real tickets. `sla-for-performance` was added on 2026-11-11. Re-checked 2026-11-14: none of the ten seed rows is in the file yet.
- Final answer (2026-11-12; expert call for the seed rows; the real terms need you):
  - Ten seed rows, each backed by current knowledge-base text:
    - `latency-unqualified`: "latency" with no layer; answer the likely layer, name the others (clarify rule).
    - `network-latency`: a VM has no network latency counter; read transmitted dropped packets.
    - `host-ready`: "ESXi Ready" sums or averages its VMs; read the worst VM.
    - `ready-percent`: "Ready 5% / 10%" or "Ready 2000 ms": summed over vCPUs, read per vCPU and against Run (ready).
    - `vm-consumed`: "VM consumed memory high" or "memory leak": Consumed does not drop when the Guest OS frees memory (guest-os-vs-vm-memory).
    - `thin-provisioning`: provisioned space counts thin disks at full size.
    - `drs-score`: DRS Score is execution efficiency (VM happiness) per VM, not contention (vSphere 9.1 documentation; the cluster files now say the same, review of 2026-11-14).
    - `load-average`: esxtop load average is a utilization level; confirm with VM contention.
    - `sioc`: Storage I/O Control components are deprecated in VCF 9.0 (vSphere 9.1 documentation), and from VCF 9.0 SIOC keeps only IOPS limits: shares and reservations are ignored (Broadcom KB 385396). "Give the VM High disk shares" no longer protects it.
    - `memory-pressure`: three layers: Guest OS paging, VM memory contention, host memory state.
  - Reword three notes: `iowait` ("CPU wait" can also mean Ready); `overcommit` (per thread, not per core); `esxtop-cpu` (read %RDY against %RUN). Done in the review of 2026-11-14, outside this list: `steal-time` now says Linux shows steal only with the VM's steal clock on (Broadcom KB 434983).
  - With Q208 (B): rows for product labels are generated from the glossary, so the seed rows above stay for user words, not labels.
  - Change if accepted: user-terms.yaml (10 rows, 3 notes); retrieval check before and after.
  - For you: the wrong terms you see in real tickets.
- Re-checked 2026-11-14: more useful now. Without options (the field case) retrieval rests on the question's own words (recall 67% against 78% with options); a term-map row brings the right file when the user's words do not name it.
- Answer:

### Q150 · URL questions · Pages with known Level 300 errors

- Files: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md) (section 3.4, URL questions); [L2-15, the first URL question, retired](https://github.com/e1-rahabok/agent-e2/blob/main/project/archive/benchmark-questions/L2-15-vm-contention-dashboard-deprecated.md).
- Search: not from the book.
- Question: list 5-10 public pages (Broadcom KB or TechDocs, VMware blogs, community posts, third-party blogs) that you know are wrong, each with the error. Each becomes a URL question where a frontier model tends to agree with the page.
- Written as now (review 2026-11-14): no URL question in the run set. The first one (L2-15, id 0091) was retired on 2026-11-12 after the official page was fixed ([Q184](author-questions-resolved.md#q184--benchmark--the-vm-contention-page-returns-404)). Plan M2 lists the page list as yours to do.
- Final answer (review 2026-11-14; expert call for the pages; replaces the answer of 2026-11-12):
  - Re-fetched 2026-11-14, still published with the same error lines:
    - Broadcom KB 419238, Troubleshooting VM performance (https://knowledge.broadcom.com/external/article/419238, modified 2026-02-17): %RDY ≥ 10 for a VM with no per-vCPU normalisation and no Run; MCTLSZ, CACHEUSD, SWCUR ≥ 1 read as current problems; ZIP/s and UNZIP/s both read as overcommitment; %DRPTX and %DRPRX above 0 read as high network utilization; "Increase the amount of CPU and memory".
    - Broadcom KB 386180, CPU Ready Time issues in ESXi environments running high I/O workloads (https://knowledge.broadcom.com/external/article/386180, modified 2026-02-11): Ready baseline 5% and warning 10%, Co-stop under 1% and 5%, CPU Latency 5% and 10% read as contention. New: its capture command runs 112.5 minutes, not the 15 it states (`-d 15 -n $(expr ${minutes} \* 30)`: 450 samples of 15 seconds).
  - More pages the knowledge base corrects with a mechanism (fetched 2026-11-14):
    1. TechDocs vSphere 9.1, Solutions for Memory Performance Problems (https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-1/vsphere-monitoring-and-performance/monitoring-inventory-objects/troubleshoot-and-enhance-performance/memory-performance-solutions.html): "Memory usage is constantly high (94% or greater)", "Free memory consistently is 6% or less", host memory "at least slightly larger than the combined active memory". Host Usage is Consumed, mostly cache; minFree is a sliding scale, about 1% on a large host; Active is not a sizing counter.
    2. TechDocs vSphere 9.1, Solutions for Poor Network Performance (same path, `network-performance.html`): "Dropped network packets indicate a bottleneck in the network". A receive drop on a VM is usually the guest's full receive ring.
    3. Broadcom KB 326296, Determining if multiple virtual CPUs are causing performance issues (https://knowledge.broadcom.com/external/article/326296): strict co-scheduling ("has to wait until all, even the currently unused virtual cores, can be run"), and %CSTP above 3 with no per-vCPU reading.
    4. Broadcom KB 415396, High memory utilization alarms despite low active memory (https://knowledge.broadcom.com/external/article/415396): "Focus on active memory trends rather than total allocated memory". Active is a sampled estimate for the kernel, not a performance or capacity counter.
    5. Third party, if you want one: Yellow Bricks esxtop (%DRPRX "hardware overworked"), copied by KB 308290 and KB 419238.
  - Not proposed yet: TechDocs 9.1 Solutions for Disk Performance Problems (kernelLatency above 4 ms, deviceLatency above 15 ms) and Broadcom KB 344099 (https://knowledge.broadcom.com/external/article/344099: DAVG, KAVG and GAVG "should not exceed 10 ms"). The knowledge base's own KAVG and DAVG values have no catalog row yet (review of 2026-11-14), so a key would rest on an unsourced number; they qualify once the rows exist.
  - Recommended for 1.0: the two KBs and pages 1-4. Each question records the fetch date (`dateModified`; the visible date renders by script) and quotes the lines it relies on, and is re-checked before scoring.
  - The frontier reference runs in mode `web` (search available, the model decides; [Q164](author-questions-resolved.md#q164--benchmarkdesignmd-sections-1-and-8--what-frontier-model-means-in-the-claim), Q209), so a URL question tests whether a model agrees with a page it reads.
  - Change if accepted: one URL question per accepted page, multiple choice like every question since Q199 (options: the page's claims and the corrections, each true or false; Level 300); design.md section 3.4.
  - For you: accept or pick from the list; add pages you know to be wrong.
- Answer:

## Future release

- None open.

