# Questions for the author

Not indexed. One entry per question.

How to answer:

- Write your reply after `Answer:` under each question. Any length.
- Leave `Answer:` empty to skip a question for now.
- Then tell Claude the file is updated. Claude applies each answer to the knowledge base and moves the entry to [author-questions-resolved.md](author-questions-resolved.md).
- `Final answer:` (2026-11-12) is the answer proposed for your review. It replaces the drafts of 2026-11-10 and 2026-11-11 and the partly-settled notes: it is checked against the knowledge base as it is now, the decisions in project/plan.md and your answers up to [Q179](author-questions-resolved.md#q179--memory-tiering-rows-for-cluster-consumption-cluster-performance-and-cluster-risk--proposal-for-review). Its status says how it was reached: settled (by an earlier answer or decision, named), expert call, or needs you. `For you:` names what only you can give; "nothing" means accept or change. In `Answer:`, write accept, accept with changes, or your own answer.

Each entry has:

- Section: book chapter and Heading 3.
- Files: knowledge-base files affected.
- Search: verbatim strings to find in the book, only for a question about the book. A question about this repository links its files instead.
- Written as now: what the knowledge base currently says.

## Open

### Q210 · Terms · Agent, case, reading set, reading plan

- Files: [project/terms.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/terms.md); [harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md).
- Question: the new design needs four repository terms. Accept, or give your word: (A) agent now means the expert's procedure as code (was: the model plus the tool loop); (B) case: the agent's structured reading of one question (your word in [Q166](author-questions-resolved.md#q166--architecturemd-section-troubleshooting-questions--code-evaluates-flow-branches), case state; the benchmark keeps question); (C) reading set: the files and sections the model reads for one question; (D) reading plan: the code that builds it.
- Written as now: all four in project/terms.md as proposals; used in harness/AGENT.md and ARCHITECTURE.md.
- Answer:

### Q209 · Benchmark > Runs · What the next round runs

- Files: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md) (sections 8 and 16); [benchmark/RUN.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/RUN.md); [benchmark/runner/config.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/config.yaml) (`final_round`); [MISSION.md](https://github.com/e1-rahabok/agent-e2/blob/main/MISSION.md) (section 1).
- Question: under the rule that the benchmark is a proof (2026-11-14), two run choices change.
  - (1) The local model alone (baseline). It showed that the knowledge base lifts every model by 19-28 points; it proves nothing about the shipped product. (A) drop it from the rounds; (B) keep it, 1 run instead of 5, as the zero point.
  - (2) The next full round, decided on 2026-11-13 as the next run, on classic and agentic. (C) run it now as planned; (D) run it when the new agent is built ([harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md), section 7, step 5): Agent E2 on the candidates, and the frontier reference.
- Written as now: `final_round` runs baseline, classic and agentic for 3 candidates and the frontier reference in web mode, 5 runs.
- Recommended: A and D. A round on classic and agentic measures pipelines that will not ship (about US$ 73 and 2-4 hours); the retrieval check gives the new agent's retrieval number for free, and the round after step 5 is the proof.
- Answer:

### Q208 · Knowledge design · Product label and better model

- Files: [KNOWLEDGE-ENGINEERING.md](https://github.com/e1-rahabok/agent-e2/blob/main/KNOWLEDGE-ENGINEERING.md) (section Product label and better model); [knowledge/glossary.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/glossary.md); [knowledge/catalog/user-terms.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/user-terms.yaml); [project/tools/tags.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/tags.yaml) (misconception_type).
- Question: from your answer to [Q203](author-questions-resolved.md#q203--cpu--capacity--name-vspheres-ghz-total-capacity-as-a-throughput-figure), a general design: every product label Agent E2 improves on is kept verbatim and paired with what it computes, the decision it invites, the better model and the better name. Accept these parts, or change them: (A) glossary entries named by the product label, with new lines `Product label:` and `Better name:`; (B) term-map rows for those labels generated from the glossary, so the note reaches the model before it reasons; (C) the five-step teaching order in every answer that meets such a label; (D) misconception type `label-read-as-model`; (E) the better name for Total Capacity (GHz): your word (a throughput figure at base clock; "Nominal Throughput" is one option). Then: which other labels belong in the first list? Candidates from the knowledge base: ESXi CPU Usage (%), VM Memory Usage (%), ESXi Memory Usage (%), Consumed, CPU Latency, Contention (VCF Operations), Capacity Remaining (%).
- Written as now: the design is a proposal; [Q203](author-questions-resolved.md#q203--cpu--capacity--name-vspheres-ghz-total-capacity-as-a-throughput-figure) applied to the two CPU files only. Recommended: A-D as written; E and the list are yours.
- Answer:

### Q207 · Benchmark > Field set · Measure coverage on real questions

- Files: [benchmark/results/analysis-2026-11-13.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/results/analysis-2026-11-13.md) (section 12); [benchmark/live-test.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/live-test.md) (step 9: 20 real questions); [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md) (section 7.5, held-out set).
- Question: 159 of the 196 questions were drafted from the knowledge files they test, so the benchmark cannot show how often a real question falls outside the knowledge base. On your 37 questions Agent E2 leads the frontier model by 8-17 points; outside coverage the 30B model is far weaker than the frontier model. Proposal: a field set of about 100 real questions, collected, not written from the knowledge base (your tickets and consulting cases, customer questions, Broadcom community and forum threads). Two numbers from it: coverage (share settled by the knowledge base) and the score. Out-of-coverage answers must say so. (A) adopt it, collected now, kept out of the repository like the held-out set; (B) adopt it, collected at release only; (C) no: the live test's 20 questions are enough.
- Written as now: held-out set of 30 drawn from the same blueprint; 20 real questions in the live test. Recommended: A. You hold the real questions; Claude can collect public community threads.
- Answer:

### Q205 · Memory > Swap and compression > Example · Gap between Consumed and the effective limit

- Files: [Swap and compression](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/swap-and-compression.md) (section Example: limit, swap and compress in opposite directions).
- Search 1: "The small gap above the limit is VM overhead" (old line, removed)
- Question: The old line said the small gap above the limit is VM overhead. In the example data, Consumed sits just under Memory|Effective limit and Granted above it. Did the line mean the gap between Consumed and Granted? Is the effective limit the configured limit plus overhead?
- Written as now: Consumed stays a little below the effective limit because the effective limit includes overhead; Granted sits above it and ignores the limit (draft, review note).
- Answer:

### Q204 · VCF Operations > Capacity forecast · Capacity Remaining: largest gap or tightest point

- Files: [Capacity forecast](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/features/capacity-forecast.md); question 0235 (benchmark/questions).
- Search 1: "The largest difference between usable capacity and projected utilization"
- Search 2: "follows the tightest point of the 3 days"
- Question: TechDocs 9.1 says Capacity Remaining (%) is the largest difference between usable capacity and projected utilization over the next 3 days; the same page sets it to 0 when any projection exceeds 100%. In the field, does the value follow the smallest remaining capacity (the highest projected point), as the key of 0235 says, or the largest gap, as the text literally reads?
- Written as now: the TechDocs wording kept, plus a reading that the 0 rule makes the value follow the tightest point (draft, review note).
- Answer:

### Q202 · Memory > Overhead · Kernel memory reservation with vSAN and NSX

- Files: [Overhead](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/architecture/overhead.md) (section Memory metrics); question 0024, option E.
- Search 1: "Too low with vSAN and NSX, too high with ESXi only"
- Search 2: "Reservation stays steady even when kernel use drops"
- Question: The file says the kernel reservation is too low with vSAN and NSX (supports the key: E false), and later that the memory reservation stays steady even when kernel use drops 90% (supports E). On a busy host with vSAN and NSX, is the kernel memory reservation below actual kernel use? Should the second line be scoped to an idle or ESXi-only host?
- Written as now: both lines unchanged.
- Answer:

### Q201 · Memory > Reservation · 'Not available to VMs': admission or physical pages

- Files: [ESXi memory reservation](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/host/reservation.md); [Overhead](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/architecture/overhead.md); question 0024, option D.
- Search 1: "Kernel reservation means the amount is not available to VMs"
- Search 2: "reserved memory must be used first before it is held"
- Question: Option D of 0024 does not say which sense of available it means. For admission control the kernel reservation is withheld whether used or not, so D is true; for physical pages it is not withheld until touched, so D is false. Every model, Opus included, reads the first. Should D say (A) not available for VM reservations (true), (B) physically blocked before use (false), or (C) leave the misconception list?
- Written as now: an untouched reservation can serve other VMs; admission control counts the full reservation (draft, review note).
- Answer:

### Q199 · Benchmark > Release gate · Confident-wrong limit on open answers

- Files: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md) (section 7.5); [benchmark/runner/judge.py](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/judge.py) (RUBRIC); [harness/modes.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/modes.py) (OPEN_FORMAT); [benchmark/results/analysis-2026-11-13.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/results/analysis-2026-11-13.md) (sections 2 and 3).
- Question: the gate allows 3% confident-wrong over all answers. With consensus, multiple choice reaches 3-4%, but judged answers stay at 31-41% (Opus with web search: 23%). A judged answer of up to 250 words scores 0 when one sentence contradicts a key point. Which way? (A) keep one 3% limit, and change the answer shape: shorter answers that state only what the knowledge base supports, the rest marked as not settled; (B) the judge grades each claim, and a contradicted side claim lowers the score instead of zeroing it; (C) two limits: 3% for multiple choice, a separate limit for judged answers set from the next round; (D) A and C together.
- Written as now: one limit of 3% over all answers. Recommended: D. A is a harness change Claude can build and measure; C keeps the gate reachable while A is measured.
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
- Answer:

### Q149 · Term map · Wrong terms users write

- Files: [knowledge/catalog/user-terms.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/user-terms.yaml).
- Search: not from the book.
- Question: list the wrong terms VMware admins and architects write in tickets, forums and chats, each with what they mean (for example "steal time" means VM CPU Ready and Co-stop). Each becomes a row: the words, the knowledge-base terms, the file, the misconception.
- Written as now: 41 rows, none from real tickets. `sla-for-performance` was added on 2026-11-11.
- Final answer (2026-11-12; expert call for the seed rows; the real terms need you):
  - Ten seed rows, each backed by current knowledge-base text:
    - `latency-unqualified`: "latency" with no layer; answer the likely layer, name the others (clarify rule).
    - `network-latency`: a VM has no network latency counter; read transmitted dropped packets.
    - `host-ready`: "ESXi Ready" sums or averages its VMs; read the worst VM.
    - `ready-percent`: "Ready 5% / 10%" or "Ready 2000 ms": summed over vCPUs, read per vCPU and against Run (ready).
    - `vm-consumed`: "VM consumed memory high" or "memory leak": Consumed does not drop when the Guest OS frees memory (guest-os-vs-vm-memory).
    - `thin-provisioning`: provisioned space counts thin disks at full size.
    - `drs-score`: DRS Score is demand met per VM, not contention.
    - `load-average`: esxtop load average is a utilization level; confirm with VM contention.
    - `sioc`: Storage I/O Control is deprecated in VCF 9.0.
    - `memory-pressure`: three layers: Guest OS paging, VM memory contention, host memory state.
  - Reword three notes: `iowait` ("CPU wait" can also mean Ready); `overcommit` (per thread, not per core); `esxtop-cpu` (read %RDY against %RUN).
  - Change if accepted: user-terms.yaml (10 rows, 3 notes); retrieval check before and after.
  - For you: the wrong terms you see in real tickets.
- Answer:

### Q150 · URL questions · Pages with known Level 300 errors

- Files: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md) (section 3.4, URL questions); [L2-15, the first URL question](https://github.com/e1-rahabok/agent-e2/blob/main/project/archive/benchmark-questions/L2-15-vm-contention-dashboard-deprecated.md).
- Search: not from the book.
- Question: list 5-10 public pages (Broadcom KB or TechDocs, VMware blogs, community posts, third-party blogs) that you know are wrong, each with the error. Each becomes a URL question where a frontier model tends to agree with the page.
- Written as now: one URL question (L2-15, id 0091, the VM Contention dashboard page). Plan M2 lists the page list as yours to do.
- Final answer (2026-11-12; expert call for two pages; the rest needs you):
  - Two pages verified (fetched 2026-11-10):
    - Broadcom KB 419238, Troubleshooting VM performance (https://knowledge.broadcom.com/external/article/419238): %RDY ≥ 10 for a VM, with no per-vCPU normalisation and no Run; MCTLSZ, CACHEUSD, SWCUR ≥ 1 read as current problems (they are past tense); ZIP/s and UNZIP/s both read as overcommitment (only UNZIP/s and SWR/s mean the VM waits now); %DRPTX and %DRPRX above 0 read as high network utilization (received drops usually mean the Guest OS did not drain the ring); "Increase the amount of CPU and memory" (more vCPUs can raise Ready and Co-stop).
    - Broadcom KB 386180, CPU Ready Time issues in ESXi environments running high I/O workloads (https://knowledge.broadcom.com/external/article/386180): Ready baseline 5% and warning 10% from an esxtop batch capture, not per vCPU, not against Run; CPU Latency 5% and 10% read as contention (Latency also rises with lower frequency and Hyper-Threading, with no wait).
  - Checked and rejected: KB 306576 (right apart from "cores" for vCPUs); KB 431027 (matches core-utilization).
  - Re-fetch each page when the question is written: the date renders by script, so the question key records the fetch date and quotes the lines it relies on.
  - The frontier reference runs with web search on ([Q164](author-questions-resolved.md#q164--benchmarkdesignmd-sections-1-and-8--what-frontier-model-means-in-the-claim)), so URL questions test whether a model agrees with a page it reads. The benchmark runs after development ([Q163](author-questions-resolved.md#q163--plan-decisions-2026-11-06--benchmark-before-m1-and-m2-are-complete)), so the pages can still change.
  - Change if accepted: two URL questions (Level 300, troubleshoot).
  - For you: 3-8 more pages (blogs, community posts) you know to be wrong.
- Answer:

## Resolved index

Answered questions are in [author-questions-resolved.md](author-questions-resolved.md). Each key links to its entry there.

- [Q200](author-questions-resolved.md#q200--benchmark--mode--agentic-or-classic-as-the-shipped-mode) · Benchmark > Mode · Agentic or classic as the shipped mode
- [Q203](author-questions-resolved.md#q203--cpu--capacity--name-vspheres-ghz-total-capacity-as-a-throughput-figure) · CPU > Capacity · Name vSphere's GHz 'Total Capacity' as a throughput figure
- [Q206](author-questions-resolved.md#q206--benchmark--retrieval-check--restart-it-now) · Benchmark > Retrieval check · Restart it now
- [Q189](author-questions-resolved.md#q189--cpu--overlap--overlap-and-linux-steal-time) · CPU > Overlap · Overlap and Linux steal time
- [Q198](author-questions-resolved.md#q198--cpu--numa-settings--nps-1-default-or-the-setting-that-matches-the-silicon) · CPU > NUMA settings · NPS-1 default or the setting that matches the silicon?
- [Q197](author-questions-resolved.md#q197--repository-consistency--pillar-list-and-the-troubleshooting-check-order) · Repository consistency · Pillar list and the troubleshooting check order
- [Q196](author-questions-resolved.md#q196--mission--what-result-proves-that-agent-e2-works) · Mission · What result proves that Agent E2 works?
- [Q195](author-questions-resolved.md#q195--esxi-storage-io-path--where-does-a-paravirtual-scsi-queue-limit-show) · ESXi storage I/O path · Where does a Paravirtual SCSI queue limit show?
- [Q194](author-questions-resolved.md#q194--guest-os-disk-queue--above-the-driver-or-below-it) · Guest OS disk queue · Above the driver, or below it?
- [Q192](author-questions-resolved.md#q192--virtual-numa--numaautosizeonce-default-and-the-power-cycle) · Virtual NUMA · numa.autosize.once default and the power cycle
- [Q193](author-questions-resolved.md#q193--guest-os-sizing--lowering-sql-server-max-server-memory-in-steps) · Guest OS sizing · Lowering SQL Server max server memory in steps
- [Q191](author-questions-resolved.md#q191--field-checks-the-documents-do-not-settle) · Field checks the documents do not settle
- [Q182](author-questions-resolved.md#q182--chapter-3-memory--vm--limit-and-balloon-again-reopens-q014) · Chapter 3 Memory > VM · Limit and balloon, again (reopens Q014)
- [Q183](author-questions-resolved.md#q183--benchmark--thick-vms-in-the-datastore-ds01-export) · Benchmark · Thick VMs in the datastore DS01 export
- [Q184](author-questions-resolved.md#q184--benchmark--the-vm-contention-page-returns-404) · Benchmark · The VM Contention page returns 404
- [Q185](author-questions-resolved.md#q185--benchmark--keys-of-your-questions-that-a-reviewer-doubts) · Benchmark · Keys of your questions that a reviewer doubts
- [Q186](author-questions-resolved.md#q186--benchmark--keys-that-rest-on-your-definitions-fairness) · Benchmark · Keys that rest on your definitions (fairness)
- [Q187](author-questions-resolved.md#q187--cpu--demand--demand-under-a-cpu-limit) · CPU > Demand · Demand under a CPU limit
- [Q188](author-questions-resolved.md#q188--memory--esxi--high-state-and-large-pages) · Memory > ESXi · High state and large pages
- [Q190](author-questions-resolved.md#q190--windows-memory--500-mb-free-or-available) · Windows memory · 500 MB: Free or Available?
- [Q181](author-questions-resolved.md#q181--writing-rules--lint-for-titles-and-headings) · Writing rules · Lint for titles and headings
- [Q162](author-questions-resolved.md#q162--class-of-service--minimum-vm-performance--per-class) · Class of service · Minimum VM Performance (%) per class
- [Q165](author-questions-resolved.md#q165--benchmarkdesignmd--sealed-claim-set-and-knowledge_class-tag) · benchmark/design.md · Sealed claim set and knowledge_class tag
- [Q175](author-questions-resolved.md#q175--class-of-service--relative-value-per-class-vs-reservation-vm-size-and-sla) · Class of service · Relative value per class vs reservation, VM size and SLA
- [Q143](author-questions-resolved.md#q143--part-2--proactive-operations--alert--threshold-design--conditions--condition-vs-symptom) · Part 2 > Proactive Operations > Alert > Threshold Design > Conditions · Condition vs symptom
- [Q144](author-questions-resolved.md#q144--part-2--proactive-operations--alert--cpu-alerts--vm-contention--orange-values-and-the-missing-diagram) · Part 2 > Proactive Operations > Alert > CPU Alerts > VM Contention · Orange values and the missing diagram
- [Q145](author-questions-resolved.md#q145--part-2--proactive-operations--alert--memory-alerts--wait-example-and-instance) · Part 2 > Proactive Operations > Alert > Memory Alerts · Wait, example and instance
- [Q146](author-questions-resolved.md#q146--part-2--proactive-operations--alert--storage-alerts--vm-contention--80-ms-vs-class-of-service) · Part 2 > Proactive Operations > Alert > Storage Alerts > VM Contention · 80 ms vs class of service
- [Q147](author-questions-resolved.md#q147--part-2--proactive-operations--alert--network-alerts--vm-dropped-packets) · Part 2 > Proactive Operations > Alert > Network Alerts · VM dropped packets
- [Q142](author-questions-resolved.md#q142--part-2--proactive-operations--alert--design--alert-count-table-vs-the-alert-sections) · Part 2 > Proactive Operations > Alert > Design · Alert count table vs the alert sections
- [Q134](author-questions-resolved.md#q134--part-3--metric-mastery--triple-see-method--why-not-use-red-golden-signals) · Part 3 > Metric Mastery > Triple See Method · Why not USE, RED, Golden Signals
- [Q135](author-questions-resolved.md#q135--why-a-new-framework--complexity--itil-4-or-itil-5) · Why a New Framework? > Complexity · ITIL 4 or ITIL 5
- [Q136](author-questions-resolved.md#q136--part-3--modelling--calculation--kpi-colours-and-a-timeline) · Part 3 > Modelling > Calculation · KPI colours and a timeline
- [Q137](author-questions-resolved.md#q137--metric-mastery--aggregation--the-problem-with-average--esxi-cpu-ready-) · Metric Mastery > Aggregation > The Problem with Average · ESXi CPU Ready (%)
- [Q139](author-questions-resolved.md#q139--part-2--proactive-operations--business-applications--vsphere-folder-structure--diagram-label) · Part 2 > Proactive Operations > Business Applications > vSphere Folder Structure · Diagram label
- [Q140](author-questions-resolved.md#q140--part-2--proactive-operations--alert--threshold-design--red-vs-orange-scale) · Part 2 > Proactive Operations > Alert > Threshold Design · Red vs orange scale
- [Q141](author-questions-resolved.md#q141--part-2--proactive-operations--alert--class-of-service-the-what--class-names) · Part 2 > Proactive Operations > Alert > Class of Service: The What · Class names
- [Q132](author-questions-resolved.md#q132--vcf-vcommunity-adapter-vs-part-1--cluster-closure--which-closure-thresholds-does-agent-e2-apply) · VCF-vCommunity-Adapter vs Part 1 > Cluster Closure · Which closure thresholds does Agent E2 apply
- [Q131](author-questions-resolved.md#q131--vcf-vcommunity-adapter--kpi-is-performance-only-names-in-the-adapter-documentation) · VCF-vCommunity-Adapter · KPI is performance only: names in the adapter documentation
- [Q128](author-questions-resolved.md#q128--glossary--proposed-terms-from-capacity-management) · Glossary · Proposed terms from Capacity Management
- [Q125](author-questions-resolved.md#q125--part-1--rightsizing--best-practices--8-core-block-8-and-16-vcpu) · Part 1 > Rightsizing > Best Practices · 8-core block, 8 and 16 vCPU
- [Q111](author-questions-resolved.md#q111--part-1--configuration-management--compute-related-esxi--cores-or-threads-and-48-or-64-cores) · Part 1 > Configuration Management > Compute-related, ESXi · Cores or threads, and 48 or 64 cores
- [Q088](author-questions-resolved.md#q088--part-1--observability--symptom--alert--insight--thresholds-in-the-prevention-window-image) · Part 1 > Observability > Symptom | Alert | Insight · Thresholds in the prevention window image
- [Q130](author-questions-resolved.md#q130--benchmark--release-score-gap-to-the-frontier-model-retrieval-levels) · Benchmark · Release score, gap to the frontier model, retrieval levels
- [Q180](author-questions-resolved.md#q180--resource-controls--one-home-for-share-limit-and-reservation) · Resource controls · One home for share, limit and reservation
- [Q110](author-questions-resolved.md#q110--part-1--configuration-management--reservation-cluster-resource-pool--admission-control-slot-size-and-siblings) · Part 1 > Configuration Management > Reservation, Cluster, Resource Pool · Admission control, slot size and siblings
- [Q109](author-questions-resolved.md#q109--part-1--configuration-management--limit--is-there-a-network-limit) · Part 1 > Configuration Management > Limit · Is there a network limit
- [Q108](author-questions-resolved.md#q108--part-1--configuration-management--resource-management-share--memory-share-unit-and-the-share-example) · Part 1 > Configuration Management > Resource Management, Share · Memory share unit and the share example
- [Q096](author-questions-resolved.md#q096--part-1--service-level-agreement--availability-sla--the-database-restore-in-actual-availability) · Part 1 > Service Level Agreement > Availability SLA · The database restore in Actual Availability
- [Q064](author-questions-resolved.md#q064--review--which-files-to-review-first) · Review · Which files to review first
- [Q179](author-questions-resolved.md#q179--memory-tiering-rows-for-cluster-consumption-cluster-performance-and-cluster-risk--proposal-for-review) · Memory tiering rows for Cluster Consumption, Cluster Performance and Cluster Risk · Proposal for review
- [Q178](author-questions-resolved.md#q178--memory-tiering-in-the-capacity-and-performance-models--review-of-the-three-closure-conditions) · Memory tiering in the capacity and performance models · Review of the three closure conditions
- [Q176](author-questions-resolved.md#q176--part-1--service-level-agreement--size-limit--memory-cap-per-class-after-the-socket-rule) · Part 1 > Service Level Agreement > Size Limit · Memory cap per class after the socket rule
- [Q177](author-questions-resolved.md#q177--capacity-planning-stagexlsx--memory-tiering-on-top-of-the-memory-overcommit-ratio) · Capacity Planning Stage.xlsx · Memory tiering on top of the memory overcommit ratio
- [Q166](author-questions-resolved.md#q166--architecturemd-section-troubleshooting-questions--code-evaluates-flow-branches) · ARCHITECTURE.md, section Troubleshooting questions · Code evaluates flow branches
- [Q138](author-questions-resolved.md#q138--part-2--proactive-operations--system-engagement--good-for-row) · Part 2 > Proactive Operations > System Engagement · Good For row
- [Q087](author-questions-resolved.md#q087--part-1--purpose-driven-architecture--day-0--day-1--day-2--host-specification-example) · Part 1 > Purpose-Driven Architecture > Day 0 | Day 1 | Day 2 · Host specification example
- [Q099](author-questions-resolved.md#q099--part-1--service-level-agreement--price--sla--silver-ratios-notation-and-the-64-core-licence) · Part 1 > Service Level Agreement > Price & SLA · Silver ratios, notation and the 64-core licence
- [Q168](author-questions-resolved.md#q168--vcenter-api-counters--gpumemused-on-vsphere-8x) · vCenter API counters · gpu.mem.used on vSphere 8.x
- [Q172](author-questions-resolved.md#q172--guest-os--linux-pressure-stall-information-vs-no-memory-latency) · Guest OS · Linux pressure stall information vs "no memory latency"
- [Q173](author-questions-resolved.md#q173--class-of-service--price-and-reservation-after-bronze-31) · Class of service · Price and reservation after Bronze 3:1
- [Q174](author-questions-resolved.md#q174--capacity-planning-stagexlsx--conflicts-with-the-knowledge-base-and-four-formula-errors) · Capacity Planning Stage.xlsx · Conflicts with the knowledge base, and four formula errors
- [Q127](author-questions-resolved.md#q127--part-1--performance--capacity-vs-capacity-model--demand--reservation-supply-or-demand-side) · Part 1 > Performance | Capacity vs Capacity Model > Demand · Reservation: supply or demand side
- [Q062](author-questions-resolved.md#q062--operations-flows--is-this-host-or-cluster-healthy-right-now) · Operations flows · Is this host or cluster healthy right now
- [Q116](author-questions-resolved.md#q116--part-1--4-dimensions-of-capacity--utilization--zones-vs-cluster-consumption-bands) · Part 1 > 4 Dimensions of Capacity > Utilization · Zones vs Cluster Consumption bands
- [Q061](author-questions-resolved.md#q061--operations-flows--can-this-cluster-take-more-vms-your-order-of-checks) · Operations flows · Can this cluster take more VMs: your order of checks
- [Q060](author-questions-resolved.md#q060--operations-flows--users-say-the-vm-is-slow-your-order-of-checks) · Operations flows · Users say the VM is slow: your order of checks
- [Q171](author-questions-resolved.md#q171--scope--generic-public-cloud-in-the-sp5-framework) · Scope · Generic public cloud in the SP5 Framework
- [Q167](author-questions-resolved.md#q167--missionmd-section-1--mission-sentence-and-outcome-metric) · MISSION.md, section 1 · Mission sentence and outcome metric
- [Q164](author-questions-resolved.md#q164--benchmarkdesignmd-sections-1-and-8--what-frontier-model-means-in-the-claim) · benchmark/design.md, sections 1 and 8 · What "frontier model" means in the claim
- [Q163](author-questions-resolved.md#q163--plan-decisions-2026-11-06--benchmark-before-m1-and-m2-are-complete) · Plan, Decisions 2026-11-06 · Benchmark before M1 and M2 are complete
- [Q170](author-questions-resolved.md#q170--knowledge-engineeringmd-section-51--home-of-the-misreadings) · KNOWLEDGE-ENGINEERING.md, section 5.1 · Home of the misreadings
- [Q169](author-questions-resolved.md#q169--knowledge-engineeringmd-sections-5-and-10--single-pillar-flows-filed-as-health-checks) · KNOWLEDGE-ENGINEERING.md, sections 5 and 10 · Single-pillar flows filed as health checks
- [Q059](author-questions-resolved.md#q059--agent--core-rules-and-confusable-pairs-given-to-the-agent-up-front) · Agent · Core rules and confusable pairs given to the agent up front
- [Q095](author-questions-resolved.md#q095--part-1--service-level-agreement--sla-calculation--pass-scored-as-0-and-partial-vm-scores) · Part 1 > Service Level Agreement > SLA Calculation · Pass scored as 0%, and partial VM scores
- [Q020](author-questions-resolved.md#q020--chapter-3-memory--esxi--consumed-and-compressed) · Chapter 3 Memory > ESXi · Consumed and compressed
- [Q053](author-questions-resolved.md#q053--vcenter-api-counters--gpumemreserved-vs-gpumemused) · vCenter API counters · gpu.mem.reserved vs gpu.mem.used
- [Q161](author-questions-resolved.md#q161--kpi-vs-sla--the-daily-kpi-actual) · KPI vs SLA · The daily KPI actual
- [Q160](author-questions-resolved.md#q160--kpi-vs-sla--75-is-acceptable-and-the-class-kpi-targets) · KPI vs SLA · "75% is acceptable" and the class KPI targets
- [Q158](author-questions-resolved.md#q158--threshold-design--alert-definitions-in-10) · Threshold design · Alert definitions in 1.0
- [Q157](author-questions-resolved.md#q157--threshold-design--vm-cpu-net-run-alert-at-kpi-yellow) · Threshold design · VM CPU Net Run alert at KPI yellow
- [Q156](author-questions-resolved.md#q156--threshold-design--alert-rows-in-the-capacity-file) · Threshold design · Alert rows in the capacity file
- [Q155](author-questions-resolved.md#q155--threshold-design--cancel-cycle-values) · Threshold design · Cancel cycle values
- [Q154](author-questions-resolved.md#q154--threshold-design--symptom-two-meanings) · Threshold design · Symptom: two meanings
- [Q153](author-questions-resolved.md#q153--threshold-design--kpi-in-availability-and-security-files) · Threshold design · KPI in availability and security files
- [Q152](author-questions-resolved.md#q152--thresholds--levels--empty-cells-in-the-9-value-table) · Thresholds > levels · Empty cells in the 9-value table
- [Q159](author-questions-resolved.md#q159--repository-rules--who-said-it-tags) · Repository rules · Who-said-it tags
- [Q126](author-questions-resolved.md#q126--part-1--rightsizing--optimization-vs-the-big-picture--100-or-40) · Part 1 > Rightsizing > Optimization vs The Big Picture · 100% or 40%
- [Q123](author-questions-resolved.md#q123--part-1--capacity-management--reclamation--benefit-table-and-scope) · Part 1 > Capacity Management > Reclamation · Benefit table and scope
- [Q148](author-questions-resolved.md#q148--part-2--overall-design-approach--design-consideration--data-points-per-month-and-the-wastage-colour) · Part 2 > Overall Design Approach > Design Consideration · Data points per month and the wastage colour
- [Q151](author-questions-resolved.md#q151--cluster-risk---cpu-overcommit-per-core-or-per-thread) · Cluster Risk (%) · CPU overcommit per core or per thread
- [Q105](author-questions-resolved.md#q105--part-1--monitor--troubleshoot-sp5-framework-process--logs-in-monitoring-and-the-length-of-the-daily-check) · Part 1 > Monitor | Troubleshoot; SP5 Framework: Process · Logs in monitoring and the length of the daily check
- [Q101](author-questions-resolved.md#q101--part-1--sp5-framework-pillars--relationship-lines-and-what-is-troubleshot) · Part 1 > SP5 Framework: Pillars · Relationship lines and what is troubleshot
- [Q106](author-questions-resolved.md#q106--part-1--service-level-agreement--performance-sla--sla-counters-vs-the-prevention-window-alerts) · Part 1 > Service Level Agreement > Performance SLA · SLA counters vs the prevention window alerts
- [Q100](author-questions-resolved.md#q100--part-1--service-level-agreement--size-limit--socket-or-logical-cpus) · Part 1 > Service Level Agreement > Size Limit · Socket or logical CPUs
- [Q098](author-questions-resolved.md#q098--part-1--service-level-agreement--recommended-sla--compliance-9995-or-100) · Part 1 > Service Level Agreement > Recommended SLA · Compliance 99.95% or 100%
- [Q097](author-questions-resolved.md#q097--part-1--service-level-agreement--performance-sla--co-stop-exclusion-and-memory-contention-unit) · Part 1 > Service Level Agreement > Performance SLA · Co-stop exclusion and Memory Contention unit
- [Q122](author-questions-resolved.md#q122--part-1--cluster-closure-vs-planning-phase--performance--closure-values) · Part 1 > Cluster Closure vs Planning Phase · Performance (%) closure values
- [Q121](author-questions-resolved.md#q121--part-1--capacity-model--cluster-closure--logic--non-production-capacity-and-the-orange-case) · Part 1 > Capacity Model > Cluster Closure > Logic · Non-production capacity and the orange case
- [Q120](author-questions-resolved.md#q120--part-1--planning-phase-vs-cluster-risk--bronze-plan-scores-red) · Part 1 > Planning Phase vs Cluster Risk · Bronze plan scores red
- [Q119](author-questions-resolved.md#q119--part-1--capacity-model--planning-phase--is-the-gap-2x-everywhere) · Part 1 > Capacity Model > Planning Phase · Is the gap 2x everywhere
- [Q118](author-questions-resolved.md#q118--part-1--4-dimensions-of-capacity--reservation--share--unit-of-cpu-reservation) · Part 1 > 4 Dimensions of Capacity > Reservation | Share · Unit of CPU reservation
- [Q117](author-questions-resolved.md#q117--part-1--4-dimensions-of-capacity--allocation--memory-tiering-version) · Part 1 > 4 Dimensions of Capacity > Allocation · Memory tiering version
- [Q115](author-questions-resolved.md#q115--part-1--capacity-management--good-advice--why-each-statement-is-wrong) · Part 1 > Capacity Management > "Good" Advice · Why each statement is wrong
- [Q114](author-questions-resolved.md#q114--part-1--capacity-management--stages-and-capacity-model--book-text-fixes) · Part 1 > Capacity Management > Stages and Capacity Model · Book text fixes
- [Q102](author-questions-resolved.md#q102--part-1--sp5-framework--health--where-compliance-and-inventory-sit) · Part 1 > SP5 Framework > Health · Where compliance and inventory sit
- [Q133](author-questions-resolved.md#q133--health-check--decisions-still-open-from-the-2026-11-08-review) · Health check · Decisions still open from the 2026-11-08 review
- [Q103](author-questions-resolved.md#q103--part-1--sp5-framework--basic-terminology--alert-urgent-or-important-symptom) · Part 1 > SP5 Framework > Basic Terminology · Alert: urgent or important; symptom
- [Q092](author-questions-resolved.md#q092--part-1--begin-with-the-end-in-mind--the-crown-jewel--health-across-tiers) · Part 1 > Begin with The End in Mind > The Crown Jewel · Health across tiers
- [Q090](author-questions-resolved.md#q090--part-1--observability--input--output--property-types-the-second-event-row-drs-automation-level) · Part 1 > Observability > Input | Output · Property types, the second Event row, DRS automation level
- [Q086](author-questions-resolved.md#q086--part-1--your-private-cloud--overview--key-metrics--operational-availability-and-green-zone) · Part 1 > Your Private Cloud > Overview > Key Metrics · Operational Availability and green zone
- [Q072](author-questions-resolved.md#q072--part-1--the-layers-in-it-systems--apdex) · Part 1 > The Layers in IT Systems · Apdex
- [Q063](author-questions-resolved.md#q063--sources--book-part-1-and-the-vcf-operations-chapters) · Sources · Book Part 1 and the VCF Operations chapters
- [Q094](author-questions-resolved.md#q094--repository--where-cross-pillar-operations-files-go) · Repository · Where cross-pillar operations files go
- [Q091](author-questions-resolved.md#q091--part-1--purpose-driven-architecture--the-2-sides-of-vcf--workload-and-the-pillar-list) · Part 1 > Purpose-Driven Architecture > The 2 Sides of VCF · Workload and the pillar list
- [Q089](author-questions-resolved.md#q089--part-1--observability--alert--importance-of-alerts-and-the-colours) · Part 1 > Observability > Alert · Importance of alerts and the colours
- [Q112](author-questions-resolved.md#q112--part-1--configuration-management--review-list--facts-to-update-for-vcf-91) · Part 1 > Configuration Management > Review List · Facts to update for VCF 9.1
- [Q093](author-questions-resolved.md#q093--part-1--your-private-cloud--book-corrections-for-the-next-edition) · Part 1 > Your Private Cloud · Book corrections for the next edition
- [Q107](author-questions-resolved.md#q107--part-1--your-private-cloud-service-level-agreement-to-sp5-framework-process--book-corrections-for-the-next-edition) · Part 1 > Your Private Cloud (Service Level Agreement to SP5 Framework: Process) · Book corrections for the next edition
- [Q113](author-questions-resolved.md#q113--part-1--configuration-management--book-corrections-for-the-next-edition) · Part 1 > Configuration Management · Book corrections for the next edition
- [Q104](author-questions-resolved.md#q104--part-1--sp5-framework--troubleshoot-sp5-framework-process--three-orders-of-checks) · Part 1 > SP5 Framework > Troubleshoot; SP5 Framework: Process · Three orders of checks
- [Q083](author-questions-resolved.md#q083--part-1--noisy-neighbour--network--authors-network-limit-and-reservation) · Part 1 > Noisy Neighbour > Network · Author's network limit and reservation
- [Q084](author-questions-resolved.md#q084--knowledge-base--esxi-cpu-demand-sum-of-vms-or-not) · Knowledge base · ESXi CPU Demand: sum of VMs or not
- [Q085](author-questions-resolved.md#q085--follow-up-to-q070--does-the-hypervisor-count-a-full-vmxnet3-receive-ring) · Follow-up to Q070 · Does the hypervisor count a full VMXNET3 receive ring
- [Q081](author-questions-resolved.md#q081--part-1--noisy-neighbour--network--host-pool-or-uplink-pool) · Part 1 > Noisy Neighbour > Network · Host pool or uplink pool
- [Q082](author-questions-resolved.md#q082--part-1--noisy-neighbour--memory-and-solution--gold-11-with-memory-tiering) · Part 1 > Noisy Neighbour > Memory and Solution · Gold 1:1 with memory tiering
- [Q065](author-questions-resolved.md#q065--part-1--performance-management--utilization-vs-demand--absolute-or-relative-performance) · Part 1 > Performance Management > Utilization vs Demand · Absolute or relative performance
- [Q067](author-questions-resolved.md#q067--part-1--contention-vs-consumption--points-a-and-b-100-and-queues) · Part 1 > Contention vs Consumption · Points A and B: 100% and queues
- [Q074](author-questions-resolved.md#q074--part-1--kpis-in-iaas--how-many-slas-per-service-is-there-a-guest-os-sla) · Part 1 > KPIs in IaaS · How many SLAs per service; is there a Guest OS SLA
- [Q075](author-questions-resolved.md#q075--part-1--kpi--sla--differences--kpi-timing-words) · Part 1 > KPI | SLA > Differences · KPI timing words
- [Q076](author-questions-resolved.md#q076--part-1--kpi-step-and-noisy-neighbour--solution--how-the-sla-is-computed-9999-at-5-minutes) · Part 1 > KPI step and Noisy Neighbour > Solution · How the SLA is computed; 99.99% at 5 minutes
- [Q077](author-questions-resolved.md#q077--part-1--noisy-neighbour--cpu--shares-of-a-busy-vcpu-beside-an-idle-one) · Part 1 > Noisy Neighbour > CPU · Shares of a busy vCPU beside an idle one
- [Q078](author-questions-resolved.md#q078--part-1--noisy-neighbour--cpu-and-disk--two-calculations) · Part 1 > Noisy Neighbour > CPU and Disk · Two calculations
- [Q079](author-questions-resolved.md#q079--part-1--solution--maximum-vm-size--core-or-thread-as-the-basis) · Part 1 > Solution > Maximum VM Size · Core or thread as the basis
- [Q080](author-questions-resolved.md#q080--part-1--noisy-neighbour--storage-io-control--deprecated-in-vcf-9) · Part 1 > Noisy Neighbour > Storage I/O Control · Deprecated in VCF 9
- [Q066](author-questions-resolved.md#q066--part-1--contention-vs-consumption--point-c-worst-performance-at-0-utilization) · Part 1 > Contention vs Consumption · Point C: worst performance at 0% utilization
- [Q068](author-questions-resolved.md#q068--part-1--utilization-vs-demand--highest-host-utilization-in-cluster-performance) · Part 1 > Utilization vs Demand · Highest host utilization in cluster performance
- [Q069](author-questions-resolved.md#q069--part-1--pattern-difference--where-the-cliff-starts) · Part 1 > Pattern Difference · Where the cliff starts
- [Q070](author-questions-resolved.md#q070--part-1--iaas-metric-types--layer-of-the-driver-metrics) · Part 1 > IaaS Metric Types · Layer of the driver metrics
- [Q071](author-questions-resolved.md#q071--part-1--the-3-realms--one-word-two-meanings-realm) · Part 1 > The 3 Realms · One word, two meanings: realm
- [Q073](author-questions-resolved.md#q073--part-1--kpi--sla--differences--one-kpi-or-two-for-vm-and-guest-os) · Part 1 > KPI | SLA > Differences · One KPI or two for VM and Guest OS
- [Q045](author-questions-resolved.md#q045--chapter-3-memory--vm--swapped-formula-in-the-vsphere-91-documentation) · Chapter 3 Memory > VM · Swapped formula in the vSphere 9.1 documentation
- [Q046](author-questions-resolved.md#q046--provider-objects--esxtop--htq-and-dtyp-still-in-the-91-documentation) · Provider Objects > esxtop · HTQ and DTYP still in the 9.1 documentation
- [Q047](author-questions-resolved.md#q047--the-world-of-metrics--resource-management--untouched-memory-reservation) · The World of Metrics > Resource management · Untouched memory reservation
- [Q048](author-questions-resolved.md#q048--thresholds--interval-and-instance-reading-of-every-band) · Thresholds · Interval and instance reading of every band
- [Q049](author-questions-resolved.md#q049--vcenter-api-counters--clusterservicescpufairness-and-memfairness-low-priority) · vCenter API counters · clusterServices.cpufairness and memfairness (low priority)
- [Q050](author-questions-resolved.md#q050--vcenter-api-counters--clusterserviceseffectivecpu-and-effectivemem-vs-totalmhz-and-totalmb-low-priority) · vCenter API counters · clusterServices.effectivecpu and effectivemem vs totalmhz and totalmb (low priority)
- [Q051](author-questions-resolved.md#q051--vcenter-api-counters--clusterservicesfailover) · vCenter API counters · clusterServices.failover
- [Q052](author-questions-resolved.md#q052--vcenter-api-counters--vmop-counters-cumulative-or-per-interval-low-priority) · vCenter API counters · vmop counters: cumulative or per interval (low priority)
- [Q057](author-questions-resolved.md#q057--benchmark--memory-reservation-vs-cpu-reservationhttpsgithubcome1-rahabokagent-e2blobmainbenchmarkquestionsl3-07-reservation-cpu-vs-memorymd-check-with-a-vcenter-cpu-screenshot) · Benchmark · [Memory reservation vs CPU reservation](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-07-reservation-cpu-vs-memory.md): check with a vCenter CPU screenshot
- [Q058](author-questions-resolved.md#q058--benchmark--synthetic-share-and-review-of-l4-14-to-l4-42) · Benchmark · Synthetic share and review of L4-14 to L4-42
- [Q023](author-questions-resolved.md#q023--chapter-4-storage--vm--disk-metric-scope) · Chapter 4 Storage > VM · Disk metric scope
- [Q042](author-questions-resolved.md#q042--quiz--cpu--q11-reclamation--option-d-power-off-frees-memory) · Quiz > CPU > Q11 Reclamation · Option D, power off frees memory
- [Q043](author-questions-resolved.md#q043--quiz--memory--q2-vm-vs-guest-os--options-a-and-d) · Quiz > Memory > Q2 VM vs Guest OS · Options A and D
- [Q044](author-questions-resolved.md#q044--chapter-4-storage--esxi--latency-thresholds-vs-vsphere-91-documentation) · Chapter 4 Storage > ESXi · Latency thresholds vs vSphere 9.1 documentation
- [Q056](author-questions-resolved.md#q056--benchmark--level-of-each-existing-question) · Benchmark · Level of each existing question
- [Q054](author-questions-resolved.md#q054--benchmark--allocation-of-the-100-questions) · Benchmark · Allocation of the 100 questions
- [Q041](author-questions-resolved.md#q041--quiz--cpu--q8-reservation--options-a-and-b) · Quiz > CPU > Q8 Reservation · Options A and B
- [Q033](author-questions-resolved.md#q033--ms-windows--cpu--usage--utilization--time--vm-cpu-run-and-hyper-threading) · MS Windows > CPU > Usage | Utilization | Time · VM CPU Run and Hyper-Threading
- [Q038](author-questions-resolved.md#q038--auto-test--prompt-design--only-the-knowledge-base-or-knowledge-base-first) · Auto Test > Prompt design · ONLY the knowledge base, or knowledge base first
- [Q040](author-questions-resolved.md#q040--quiz--cpu--q1-esxi-cpu-utilisation--which-counter-is-esxi-true-utilization) · Quiz > CPU > Q1 ESXi CPU Utilisation · Which counter is ESXi true utilization
- [Q055](author-questions-resolved.md#q055--follow-ups-to-q027-and-q029) · Follow-ups to Q027 and Q029
- [Q027](author-questions-resolved.md#q027--consumer-objects--capacity--vm-cpu-needed-formula) · Consumer Objects > Capacity · VM CPU Needed formula
- [Q028](author-questions-resolved.md#q028--consumer-objects--capacity--balloon-in-guest-os-memory-sizing) · Consumer Objects > Capacity · Balloon in Guest OS memory sizing
- [Q029](author-questions-resolved.md#q029--consumer-objects--capacity--memory-utilization-ranges) · Consumer Objects > Capacity · Memory utilization ranges
- [Q030](author-questions-resolved.md#q030--provider-objects--performance--vmotion-in-cluster-performance-) · Provider Objects > Performance · vMotion in Cluster Performance (%)
- [Q031](author-questions-resolved.md#q031--provider-objects--performance--cluster-kpi-table-vs-text) · Provider Objects > Performance · Cluster KPI table vs text
- [Q032](author-questions-resolved.md#q032--provider-objects--other-metrics--monster-vm-threshold) · Provider Objects > Other Metrics · Monster VM threshold
- [Q024](author-questions-resolved.md#q024--chapter-5-network--architecture--vm-and-ingress) · Chapter 5 Network > Architecture · VM and ingress
- [Q025](author-questions-resolved.md#q025--chapter-5-network--vm--dropped-packet-volume) · Chapter 5 Network > VM · Dropped packet volume
- [Q026](author-questions-resolved.md#q026--consumer-objects--performance--compressed--swapped-threshold) · Consumer Objects > Performance · Compressed + Swapped threshold
- [Q019](author-questions-resolved.md#q019--chapter-3-memory--esxi--swap-consumed-formula) · Chapter 3 Memory > ESXi · Swap Consumed formula
- [Q021](author-questions-resolved.md#q021--chapter-3-memory--esxi--utilization-formula) · Chapter 3 Memory > ESXi · Utilization formula
- [Q022](author-questions-resolved.md#q022--chapter-4-storage--architecture--ip-storage-read-and-network-direction) · Chapter 4 Storage > Architecture · IP storage read and network direction
- [Q039](author-questions-resolved.md#q039--auto-test--golden-case-vendor-neutral-general-001--hyperscaler-cost-not-in-the-knowledge-base) · Auto Test > Golden case vendor-neutral-general-001 · Hyperscaler cost not in the knowledge base
- [Q001](author-questions-resolved.md#q001--chapter-2-cpu--vm--linux-steal-time) · Chapter 2 CPU > VM · Linux Steal Time
- [Q002](author-questions-resolved.md#q002--chapter-2-cpu--vm--system-charged-to-vcpu-0) · Chapter 2 CPU > VM · System charged to vCPU 0
- [Q003](author-questions-resolved.md#q003--chapter-2-cpu--vm--run-for-sizing) · Chapter 2 CPU > VM · Run for sizing
- [Q004](author-questions-resolved.md#q004--chapter-2-cpu--vm--contention-formula-condition) · Chapter 2 CPU > VM · Contention formula condition
- [Q005](author-questions-resolved.md#q005--chapter-2-cpu--vm--contention-and-limit) · Chapter 2 CPU > VM · Contention and limit
- [Q006](author-questions-resolved.md#q006--chapter-2-cpu--vm--used-above-run) · Chapter 2 CPU > VM · Used above Run
- [Q007](author-questions-resolved.md#q007--chapter-2-cpu--vm--ready-and-vm-size) · Chapter 2 CPU > VM · Ready and VM size
- [Q008](author-questions-resolved.md#q008--chapter-2-cpu--vm--ramp-test) · Chapter 2 CPU > VM · Ramp test
- [Q009](author-questions-resolved.md#q009--chapter-2-cpu--esxi--demand-provider-or-consumer) · Chapter 2 CPU > ESXi · Demand: provider or consumer
- [Q010](author-questions-resolved.md#q010--chapter-2-cpu--esxi--usage-cap) · Chapter 2 CPU > ESXi · Usage cap
- [Q011](author-questions-resolved.md#q011--chapter-2-cpu--esxi--cpu-imbalance) · Chapter 2 CPU > ESXi · CPU Imbalance
- [Q012](author-questions-resolved.md#q012--chapter-3-memory--architecture--3-levels) · Chapter 3 Memory > Architecture · 3 levels
- [Q013](author-questions-resolved.md#q013--chapter-3-memory--architecture--balloon-and-unmet-demand) · Chapter 3 Memory > Architecture · Balloon and unmet demand
- [Q014](author-questions-resolved.md#q014--chapter-3-memory--vm--limit-and-balloon) · Chapter 3 Memory > VM · Limit and balloon
- [Q015](author-questions-resolved.md#q015--chapter-3-memory--vm--memory-latency-space-or-time) · Chapter 3 Memory > VM · Memory Latency: space or time
- [Q016](author-questions-resolved.md#q016--chapter-3-memory--vm--meaning-of-compressed-and-swapped) · Chapter 3 Memory > VM · Meaning of Compressed and Swapped
- [Q017](author-questions-resolved.md#q017--chapter-3-memory--vm--sharing-savings) · Chapter 3 Memory > VM · Sharing savings
- [Q018](author-questions-resolved.md#q018--chapter-3-memory--vm--utilization-5) · Chapter 3 Memory > VM · Utilization 5%
- [Q034](author-questions-resolved.md#q034--quiz--cpu--q2-vm-cpu-speed--80-vs-625-hyper-threading-charge) · Quiz > CPU > Q2 VM CPU Speed · 80% vs 62.5% Hyper-Threading charge
- [Q035](author-questions-resolved.md#q035--quiz--cpu--q6-vm-cpu-contention--demand-and-hyper-threading) · Quiz > CPU > Q6 VM CPU Contention · Demand and Hyper-Threading
- [Q036](author-questions-resolved.md#q036--quiz--cpu--q7-guest-os-cpu--is-f-correct) · Quiz > CPU > Q7 Guest OS CPU · Is F correct?
- [Q037](author-questions-resolved.md#q037--quiz--cost-and-price--q1-vm-cost--missing-explanations) · Quiz > Cost and Price > Q1 VM Cost · Missing explanations
