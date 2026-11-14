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
  - For you: accept (1)-(3), or keep VM slow first.
- Answer:

### Q212 · Mission > Release gate · Is beating the frontier model a 1.0 requirement?

- Files: [project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md) (Mission: "1.0 minimum"); [MISSION.md](https://github.com/e1-rahabok/agent-e2/blob/main/MISSION.md) (section 1, "A proof that Agent E2 works"); [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md) (sections 1, 7.5 and 15); [benchmark/runner/report.py](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/report.py) (`gate`, `mcnemar`).
- Question: three statements disagree. The plan's Mission: "1.0 minimum: ... higher score than frontier models on monitoring and troubleshooting". MISSION.md: "A proof that Agent E2 works is the benchmark result show it scored higher than frontier models". Your decision of 2026-11-13 ("beating anyone is not a goal; it is an outcome") took the 15-point gap of Q130 out of the gate; design.md section 7.5: "The gap to the frontier model is not a gate". Which holds for release 1.0? (A) Not a gate: the plan line and the MISSION.md line say "the release gate; the gap to the frontier model reported with its paired test". (B) A gate: Agent E2's final score above the frontier reference's, the one-sided McNemar test significant at α 0.05. (C) Non-inferiority as the gate: Agent E2 not significantly below the frontier reference (one-sided McNemar at α 0.05); a win is claimed only when B holds.
- Written as now: the gate is final score at least 85%, Level 400 at least 80%, confident-wrong at most 3%, no up-front misconception stated as true, held-out set at most 11 points below; the frontier gap is an outcome row in the report. Last measured (previous generation, archived): the frontier reference with web search at 81%, no local configuration above it.
- Final answer (review 2026-11-14; expert call): C. The mission is a comparison, and a release that loses clearly to the frontier model contradicts the reason the product exists: the customer compares, and the frontier model needs no GPU. B as a gate fails by noise when both sit near 85%: a real 5-point win has low power at about 200 questions (design.md, section 4). C protects the claim without gating on luck; the README and MISSION.md claim a win only when B holds.
  - Change if accepted: plan Mission and gate line; MISSION.md section 1 (the line, and its grammar); design.md sections 1, 7.5 and 15; report.py (`gate`: one non-inferiority row); project/terms.md (release gate).
  - For you: A, B or C.
- Answer:

### Q208 · Knowledge design · Product label and better model

- Files: [KNOWLEDGE-ENGINEERING.md](https://github.com/e1-rahabok/agent-e2/blob/main/KNOWLEDGE-ENGINEERING.md) (section Product label and better model); [knowledge/glossary.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/glossary.md); [knowledge/catalog/user-terms.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/user-terms.yaml); [project/tools/tags.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/tags.yaml) (misconception_type).
- Question: from your answer to [Q203](author-questions-resolved.md#q203--cpu--capacity--name-vspheres-ghz-total-capacity-as-a-throughput-figure), a general design: every product label Agent E2 improves on is kept verbatim and paired with what it computes, the decision it invites, the better model and the better name. Accept these parts, or change them: (A) glossary entries named by the product label, with new lines `Product label:` and `Better name:`; (B) term-map rows for those labels generated from the glossary, so the note reaches the model before it reasons; (C) the five-step teaching order in every answer that meets such a label; (D) misconception type `label-read-as-model`; (E) the better name for Total Capacity (GHz): your word (a throughput figure at base clock; "Nominal Throughput" is one option). Then: which other labels belong in the first list? Candidates from the knowledge base: ESXi CPU Usage (%), VM Memory Usage (%), ESXi Memory Usage (%), Consumed, CPU Latency, Contention (VCF Operations), Capacity Remaining (%).
- Written as now: the design is a proposal; [Q203](author-questions-resolved.md#q203--cpu--capacity--name-vspheres-ghz-total-capacity-as-a-throughput-figure) applied to the two CPU files only. Not applied: no glossary entry has `Product label:` or `Better name:` lines; tags.yaml has no `label-read-as-model`; no prompt carries the teaching order. AGENT.md (section 4.5) described the teaching order as part of the answer shape: corrected in the review of 2026-11-14 to "proposed, not built".
- Final answer (review 2026-11-14; expert call for A-D and the list; E is yours):
  - A, B, D as written. B by a small generator (glossary pair → term-map row) checked by lint, so the row is never edited by hand.
  - C, narrowed: the teaching order only when the case or a term-map row names a listed label, and inside the answer length, not added to it. Five steps in every answer that meets a label conflict with Q199 (A: shorter answers): a 250-word judged answer with four key points has no room for them. Steps 1, 3 and 4 carry the correction; steps 2 and 5 fold into the mechanism and what to check next.
  - The list, by the test of the design (the label invites a decision its computed model does not support): ESXi CPU Usage (%) (counts frequency and Hyper-Threading; read as busy time); VM Memory Usage (%) (vCenter: Active over configured; read as "the VM needs more memory"); ESXi Memory Usage (%) (Consumed over total; read as pressure); Consumed (read as in use by the Guest OS); CPU Latency (counts frequency and Hyper-Threading; read as waiting); Capacity Remaining (%) (a projection's tightest point; read as space left now). Contention (VCF Operations) needs you: whether its 9.x formula still differs from what the label invites (Q144).
  - For you: E (the better name for Total Capacity (GHz)); accept or change the list.
- Answer:

### Q207 · Benchmark > Field set · Measure coverage on real questions

- Files: [analysis-2026-11-13.md, archived](https://github.com/e1-rahabok/agent-e2/blob/main/project/archive/benchmark-results-before-2026-11-14/analysis-2026-11-13.md) (section 12); [harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md) (section 4.6, coverage boundary); [benchmark/live-test.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/live-test.md) (step 9: 20 real questions); [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md) (section 7.5, held-out set).
- Question: 159 of the 196 questions were drafted from the knowledge files they test, so the benchmark cannot show how often a real question falls outside the knowledge base. In the round of 2026-11-13 (previous generation, archived), on your 37 questions the local configuration led the frontier model by 8-17 points; outside coverage the 30B model was far weaker than the frontier model. Proposal: a field set of about 100 real questions, collected, not written from the knowledge base (your tickets and consulting cases, customer questions, Broadcom community and forum threads). Two numbers from it: coverage (share settled by the knowledge base) and the score. Out-of-coverage answers must say so. (A) adopt it, collected now, kept out of the repository like the held-out set; (B) adopt it, collected at release only; (C) no: the live test's 20 questions are enough.
- Written as now: held-out set of 30 drawn at release in the proportions of the run set, from real questions where you have them; 20 real questions in the live test. The blueprint (target counts) was removed on 2026-11-14: the real test is the field. Built 2026-11-14: the coverage boundary (when nothing in the reading set came from a flow or a file the question names, the answer prompt says the question may be outside the knowledge base, and to say so); AGENT.md sets its search-score limit on this field set, so the field set also tunes that boundary. Recommended: A. You hold the real questions; Claude can collect public community threads (titles and questions only, no customer data).
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

### Q199 · Benchmark > Release gate · Confident-wrong limit on open answers

- Files: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md) (sections 7.5 and 14); [benchmark/runner/judge.py](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/runner/judge.py) (RUBRIC); [harness/agent.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/agent.py) (`OPEN_SHAPE`); [harness/modes.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/modes.py) (`OPEN_FORMAT`); [project/archive/benchmark-results-before-2026-11-14/analysis-2026-11-13.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/archive/benchmark-results-before-2026-11-14/analysis-2026-11-13.md) (sections 2 and 3).
- Question: the gate allows 3% confident-wrong over all answers. In the round of 2026-11-13 (previous generation, archived; the numbers are not compared, only the shape of the problem carries over), consensus brought multiple choice to 3-4% (projected), but judged answers stayed at 31-41% (Opus with web search: 23%). Judged answers are 77 of the 196 questions (39%): even at 8% confident-wrong on them, the overall rate is above 3%. A judged answer of up to 250 words scores 0 when one sentence contradicts a key point. Which way? (A) keep one 3% limit, and change the answer shape: shorter answers that state only what the knowledge base supports, the rest marked as not settled; (B) the judge grades each claim, and a contradicted side claim lowers the score instead of zeroing it; (C) two limits: 3% for multiple choice, a separate limit for judged answers set from the next round; (D) A and C together.
- Written as now (review 2026-11-14): one limit of 3% over all answers. Part of A is already built, ahead of your answer: Agent E2's open-answer prompt asks for a last line "Not settled by the knowledge base:" holding every claim with no file (`agent.OPEN_SHAPE`, 2026-11-14). Not measured. The 250-word cap is unchanged. The judge has no rule for that line: its rubric scores "says the question cannot be settled" as 0 and unsure, and caps at 0 on any statement that contradicts a key point. A judge can read the line either way, so an answer with the right conclusion and one doubtful side claim under the line can score 0.
- Final answer (review 2026-11-14; expert call; replaces the recommendation above): D, plus a judge rule (E) that the next round needs whatever you choose.
  - E: one rule in the judge's rubric: "Text under 'Not settled by the knowledge base:' is not stated as fact: it earns no credit and does not cap the score. The answer is unsure only when its conclusion is there." Without it, the shape built for A is scored by chance.
  - A: keep the shape; set the answer length by the number of key points, not one 250-word cap (plan M2 already lists a per-question length: 250 words is long for 2 key points and short for 10).
  - C: confident-wrong at most 3% on multiple choice; for judged answers a separate limit, set from the first round on Agent E2 and lowered with each release (proposal for 1.0: at most 10%).
  - Not B: grading each claim rewards long answers that hedge; a statement that contradicts a key point is one an operator acts on, so the cap at 0 stays.
  - Change if accepted: judge.py RUBRIC (rule E) with a unit test; design.md sections 7.5 (two limits) and 14 (rule E); report.py `GATE` (two confident-wrong rows); summarize.py; the per-question answer length (a question field, M2).
  - For you: accept or change; the judged limit for 1.0.
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

