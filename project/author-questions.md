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

### Q166 · ARCHITECTURE.md, section Troubleshooting questions · Code evaluates flow branches

- Files: [harness/flows.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/flows.py), [project/design-thresholds.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/design-thresholds.md).
- What the knowledge base says now: the flow tool serves step text; the model compares values and picks the branch.
- Question: (a) executable steps: the model extracts values into a case state, code compares them with catalog thresholds and picks the branch, the model explains; (b) keep as is.
- Proposed answer: (a), for 1.0, starting with the VM slow flow.
- Answer: Yes, (a) for 1.0.
- Applied 2026-11-12: Recorded in project/plan.md, M1 open work: executable flow steps (the model extracts values into a case state, code compares them with catalog thresholds and picks the branch), starting with the VM slow flow.

### Q208 · Knowledge design · Product label and better model

- Files: [KNOWLEDGE-ENGINEERING.md](https://github.com/e1-rahabok/agent-e2/blob/main/KNOWLEDGE-ENGINEERING.md) (section Product label and better model); [knowledge/glossary.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/glossary.md); [knowledge/catalog/user-terms.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/user-terms.yaml); [project/tools/tags.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/tags.yaml) (misconception_type).
- Question: from your answer to [Q203](author-questions-resolved.md#q203--cpu--capacity--name-vspheres-ghz-total-capacity-as-a-throughput-figure), a general design: every product label Agent E2 improves on is kept verbatim and paired with what it computes, the decision it invites, the better model and the better name. Accept these parts, or change them: (A) glossary entries named by the product label, with new lines `Product label:` and `Better name:`; (B) term-map rows for those labels generated from the glossary, so the note reaches the model before it reasons; (C) the five-step teaching order in every answer that meets such a label; (D) misconception type `label-read-as-model`; (E) the better name for Total Capacity (GHz): your word (a throughput figure at base clock; "Nominal Throughput" is one option). Then: which other labels belong in the first list? Candidates from the knowledge base: ESXi CPU Usage (%), VM Memory Usage (%), ESXi Memory Usage (%), Consumed, CPU Latency, Contention (VCF Operations), Capacity Remaining (%).
- Written as now: the design is a proposal; [Q203](author-questions-resolved.md#q203--cpu--capacity--name-vspheres-ghz-total-capacity-as-a-throughput-figure) applied to the two CPU files only. Recommended: A-D as written; E and the list are yours.
- Answer:

### Q207 · Benchmark > Field set · Measure coverage on real questions

- Files: [benchmark/results/analysis-2026-11-13.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/archive/benchmark-results-before-2026-11-14/analysis-2026-11-13.md) (section 12); [benchmark/live-test.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/live-test.md) (step 9: 20 real questions); [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md) (section 7.5, held-out set).
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

- Files: [Capacity forecast](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/features/capacity-forecast.md); question [0235](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-76-capacity-forecast-averages-hide-month-end.md).
- Search 1: "The largest difference between usable capacity and projected utilization"
- Search 2: "follows the tightest point of the 3 days"
- Question: TechDocs 9.1 says Capacity Remaining (%) is the largest difference between usable capacity and projected utilization over the next 3 days; the same page sets it to 0 when any projection exceeds 100%. In the field, does the value follow the smallest remaining capacity (the highest projected point), as the key of 0235 says, or the largest gap, as the text literally reads?
- Written as now: the TechDocs wording kept, plus a reading that the 0 rule makes the value follow the tightest point (draft, review note).
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

### Q199 · Benchmark > Release gate · Confident-wrong limit on open answers

- Files: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md) (section 7.5); [benchmark/runner/judge.py](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/judge.py) (RUBRIC); [harness/modes.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/modes.py) (OPEN_FORMAT); [benchmark/results/analysis-2026-11-13.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/archive/benchmark-results-before-2026-11-14/analysis-2026-11-13.md) (sections 2 and 3).
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

## Future release

- None open.

