# Threshold catalog: functional design

Proposal for the author, 2026-11-10. Not indexed. Replaces nothing yet: the current files stay until the author answers Q153-Q158.
Scope: the YAML files in `knowledge/catalog/` that hold thresholds, what each holds, how the harness reads them, and why.
Current state: `thresholds-performance.yaml` (47 rules, 31 band rows, 31 `levels` lines), `thresholds-capacity.yaml` (26 rules, 18 band rows).

## 1. Premises

Taken from the author's brief and the knowledge base. The design follows from them.

- Performance and capacity ask different questions, over different time spans. The same metric gets different thresholds.
- Alerts belong to performance (and availability). Capacity does not use alerts: it looks at weeks and months.
- Alert and KPI are different things. KPI is proactive; an alert is reactive, a guard rail when people ignore the KPI. An alert does not repeat a KPI band: it fires at a higher threshold, when the issue is urgent.
- An alert has a dimension the KPI does not have: wait cycle and cancel cycle. They remove one-off spikes and flapping.
- Performance has two uses: KPI and SLA. Different thresholds, even for the same metric.
- The reader is Agent E2: a 32B model, 16K context, and code in front of it (`ARCHITECTURE.md`, section No fast first-stage model). The author reads the files for QA only.

## 2. Use cases

What Agent E2 does with a threshold. Each use case names the files and the fields it needs. The design is checked against this list.

| # | Use case | Example question or job | Time span | Files | Who compares the number |
|---|---|---|---|---|---|
| U1 | Daily health check (automated) | Score every KPI and model; list objects in orange and red | Last 24 hours | performance, capacity, availability | Code |
| U2 | Troubleshooting a complaint | "Users say VM X is slow since 10:00" | Minutes to hours | performance (KPI, not SLA: author, 2026-11-09) | Code; model reads the verdict |
| U3 | Read a screenshot or CSV | "Is 6% Ready bad?" with a VCF Operations chart | One reading | performance, capacity | Code, after the model extracts value, metric, interval |
| U4 | Explain an alert | "Why did this alert fire? Is it real?" | One alert | alerts, performance | Code |
| U5 | Review alert design | "We get 500 alerts a day"; "Is 4% Ready a good alert threshold?" | Design | alerts, performance | Code compares with KPI; model writes the advice |
| U6 | SLA report or breach | "Did Gold VMs meet the SLA in October?" (forensic investigation) | Calendar month | performance (SLI, SLA) | Code |
| U7 | Capacity decision | "Can this cluster take 20 more VMs?"; close for business | 24 hours to months | capacity, performance (KPI as input) | Code |
| U8 | Rightsizing and reclamation | "Which VMs are oversized?" | 30 days or more | capacity (grey band, sizing bands) | Code |
| U9 | Explain a threshold | "Why is Ready 2.5% in the SLA and 8% in the alert?" | Concept | all files, one metric across uses | Model, from one tool result |
| U10 | Policy setting | "What do I set in the VCF Operations policy?" | Design | the file of the use asked | Model quotes the row |
| U11 | Availability SLA (after 1.0) | "Did we meet 99.95%?" | Calendar month | availability | Code |
| U12 | Security and compliance (after 1.0) | "How compliant is the cluster?" | Daily | security | Code |

- U2 and U3 are the 1.0 core. U1 is the automated path; it never passes raw metrics through the model.
- U9 is where a 32B model fails today: it receives five rows of the same metric and picks the wrong one. The tool must label each row with its use.
- Troubleshooting has no thresholds of its own. It reads KPI levels at the interval of the reading: 20s for the VCF Operations peak and the vSphere Client real-time chart, 2s for esxtop (Q152).

## 3. Why the same metric has different thresholds

Each use has its own time constant, its own spike filter and its own cost of a wrong call. These three set the number.

| Use | Question | Reading | Spike filter | Deadline | Cost of a false positive | Cost of a false negative |
|---|---|---|---|---|---|---|
| KPI | Is it performing now? | 20-second peak and 5-minute average, rolling window | None: the peak is wanted | None | Cheap: a yellow line read in the daily check | VMs suffer unseen until a complaint |
| SLI | Did this 5 minutes pass the contract? | 5-minute average | The 5-minute average | None | Penalty paid for nothing | Breach not reported |
| SLA | Did the month pass? | Mean of SLI passes, calendar month | The month | Lagging | Credit on the next bill | Contract dispute |
| Alert | Must someone act today? | 5-minute average, often with a 20s peak condition | Wait cycle, cancel cycle | Red 1-2 hours; orange end of day | Alert fatigue; real alerts ignored | Outage or slowness with no one acting |
| Capacity | Is there room for weeks to months? | 95th percentile over 24 hours; monthly trend | Percentile: the worst 5% ignored | Weeks | Hardware bought early | Contention for months; long lead time |

- Every use filters spikes, each in a different way. That is the core reason the numbers differ.
- Example, ESXi CPU thread utilization, same counter, three uses:

| Use | Reading | Threshold | File today |
|---|---|---|---|
| Capacity, Cluster Consumption | cluster-wide, p95 of 24 h | red from 85% | Cluster Consumption (model) |
| Capacity, Cluster Risk | worst host | red from 90% | Cluster Risk (model) |
| Alert (consumption, red only) | one host, 10 minutes, with core utilization above 80% | above 40% thread | `thresholds-capacity.yaml` row `alert-esxi-cpu-thread-utilization-red` |

- Example, VM CPU Ready:

| Use | Reading | Threshold |
|---|---|---|
| KPI | Peak CPU Ready among any vCPU, 20s | yellow 2, orange 4, red 8 |
| SLI | VM CPU Ready, VM aggregate, 5m | fail above 2.5% |
| Alert orange | VM CPU Ready 5m above 4%, with peak vCPU Ready above 32%, contention above 8%, usage above 1 GHz | all at once |
| Alert red | VM CPU Ready 5m above 8%, same conditions | all at once |

- The KPI and the alert are not on the same reading: one is the worst vCPU at 20s, the other the VM aggregate at 5m. Comparing their numbers without the reading is the classic mistake. The threshold key therefore has six parts:

```text
threshold key = (use, object, metric, instance, interval or window statistic, class of service)
```

- This extends `KNOWLEDGE-ENGINEERING.md`, section 9 (metric, object, instance, interval, window) with `use` and `class`.

## 4. Design rules for a 32B reader

- The model never reads the YAML. Code loads it into the catalog (SQLite) and a tool returns a short answer card. The YAML is shaped for code, lint and the author; the card is shaped for the model.
- The model never compares numbers. Code decides the band, the pass or fail, the trigger. The card states the verdict in words: "6.1% is orange (KPI, 20s, orange 4-8)". A 32B model is unreliable at ranges, open ends, and reversed direction (lower is worse).
- `use` is a required argument of the tool. Without it, the tool returns one line per use, each labelled with when it applies. The model cannot apply a KPI band to an SLA question by accident.
- Interval mismatch is refused by code: a 5m reading against a 20s band returns "not comparable: band is for 20-second peaks" (Interval rule, `observability/thresholds`). No silent 4x conversion.
- No null in a card. A missing value reads "no source value", so the model does not take it as 0.
- Every row is flat and complete: object, metric, unit, direction, interval on every row. No YAML anchors, no inheritance, no defaults hidden in code. Lint can check one row alone.
- One representation per fact. Today a KPI band exists twice (band row and `levels` line) plus the Markdown table. Proposed: the YAML holds edges once; the Markdown table stays for retrieval; lint checks the two match.
- Closed vocabularies for `use`, `pillar`, `interval`, `statistic`, `direction`, `class`, `instance`, `role`, in `project/tools/tags.yaml`.
- Card size: under 300 tokens per lookup. The 16K budget also carries retrieved files and screenshots.
- Each row keeps `kb` and `quote`: the model cites the file, and lint keeps the number tied to its text.

## 5. Files

Five files, one per pillar, plus alerts, as the author proposed. Names keep the `thresholds-` prefix: the harness loads one pattern and lint applies common checks.

| File | Holds | Uses inside | In 1.0 |
|---|---|---|---|
| `thresholds-performance.yaml` | KPI levels, SLI tests, SLA targets, performance rules | kpi, sli, sla, rule | Yes |
| `thresholds-capacity.yaml` | Capacity and risk models, decisions, planning and sizing rules | model, decision, rule | Yes |
| `thresholds-alerts.yaml` | Symptom definitions; thin alert definitions (Q158) | symptom, alert | Yes, the author's alerts from the book |
| `thresholds-availability.yaml` | Availability targets and SLA | kai or kpi (Q153), sla | Schema now; rows from sla-metrics (99.95%, 100%) |
| `thresholds-security.yaml` | Compliance and security targets and SLA | kci or kpi (Q153), sla | Schema now; no row until after 1.0 |

### 5.1 Common fields

Every row in every file.

| Field | Values | Why |
|---|---|---|
| `id` | unique across all five files | Stable reference from other files and from questions |
| `use` | kpi, sli, sla, model, decision, rule, symptom, alert (+ kai, kci per Q153) | The first filter of every lookup |
| `object` | managed object type, or `Guest OS` | Same metric, different object, different threshold |
| `metric` | name as the `kb` file writes it | Lookup by name |
| `counter` | VCF Operations metric key, when a source gives it | Exact match for U1 and for live integration after 1.0; fuzzy name matching picks wrong rows |
| `unit` | %, ms, count, ratio, MB/s, ... | Printed in the card |
| `direction` | above, below | Lower is worse for free memory, KPI scores, SLA |
| `instance` | aggregate, worst instance, worst child, p90 of children, cluster-wide | Worst vCPU is always at least the VM value |
| `interval` | 2s, 20s, 5m | Sample-level uses: kpi, sli, symptom |
| `window` and `statistic` | 24h p95; calendar month mean; 30d max | Window-level uses: sla, model, decision |
| `class` | all, gold, silver, bronze, production, non-production | Thresholds per class of service |
| `source`, `kb`, `quote` | as today | Traceability; lint |

- A row has `interval` or `window`, never both empty. That forces the author and Claude to state what the number applies to.

### 5.2 `thresholds-performance.yaml`

```yaml
meta: {...}
uses:            # one sentence each; the tool prints it as the card header
  kpi: 'Proactive. Is it performing now? Rolling window, 20-second accuracy, no deadline. Yellow is read in the daily check.'
  sli: 'Pass or fail of one 5-minute interval against the contract.'
  sla: 'Monthly mean of SLI passes, per class of service. Lagging.'
kpi:
- id: vm-kpi-peak-cpu-ready-any-vcpu
  object: VirtualMachine
  kpi: VM Performance (%)            # the score the row feeds
  group: contention
  metric: Peak CPU Ready among any vCPU
  unit: '%'
  direction: above
  instance: worst vCPU
  edges:                             # green start, yellow, orange, red, red end
    20s: [0, 2, 4, 8, 16]
    5m: null
    2s: null
  source: book
  kb: vsphere/object-types/vm/kpis/vm-performance
sli:
- id: vm-sli-cpu-ready
  object: VirtualMachine
  metric: CPU Ready
  instance: aggregate
  interval: 5m
  direction: above
  fail: 2.5
  unit: '%'
  class: all
  kb: sp5-framework/concepts/sla-metrics
  quote: '| CPU | Ready | above 2.5% |'
sla:
- id: performance-sla-gold
  object: VirtualMachine
  metric: Performance SLA
  window: calendar month
  statistic: mean of SLI passes
  direction: below
  fail: 99.9
  class: gold
  kb: sp5-framework/performance/noisy-neighbour
  quote: 'Performance SLA thresholds: Gold 99.9%, Silver 99.8%, Bronze 99.6%.'
rules:            # single-value statements that are neither KPI nor SLA (vm-cpu-ready-poor, documentation readings)
- ...
```

- `edges` replaces the band rows and the `levels` table: one copy. The red end is kept because KPI scoring places a value inside its band (`sp5-framework/performance/performance-kpi-design`).
- Boundary rule in code, once: a value on an edge belongs to the better band (as Close for Business does).
- KPI has no `class`: one policy for all (`kpi-vs-sla`). SLA always has `class`.
- The 9-value grid (5m, 20s, 2s) stays; Q152 fills it.
- Pros: KPI and SLA of one metric sit in one file; U9 is one query. Cons: two shapes (edges vs fail value) in one file; the tool must know both.

### 5.3 `thresholds-capacity.yaml`

Capacity is a model, not a list of metrics. The file mirrors the model: model, groups, input rows, then the decision built on the models.

```yaml
models:
- id: cluster-consumption
  use: model
  object: ClusterComputeResource
  kb: vsphere/object-types/cluster/models/cluster-consumption
  score: {direction: above, edges: [0, 25, 50, 75, 100]}
  inputs:
  - id: cluster-consumption-cpu-thread-utilization
    group: utilization
    metric: Cluster-wide ESXi CPU thread utilization
    counter: cpu|utilization_average
    instance: cluster-wide
    unit: '%'
    direction: above
    edges: [0, 55, 70, 85, 100]
    grey: null                       # wastage; Q110
    excluded_when_green: false
  - ...
- id: cluster-risk
  use: model
  object: ClusterComputeResource
  score: {direction: above, edges: [0, 25, 50, 75, 100]}
  inputs:
  - id: cluster-risk-highest-memory-consumed
    group: utilization
    metric: Highest ESXi memory consumed
    instance: worst host
    edges: [null, 80, 90, 95, 100]
    excluded_when_green: true
  - ...
decisions:
- id: close-for-business
  use: decision
  object: ClusterComputeResource
  inputs: [cluster-performance, cluster-consumption, cluster-risk]   # cluster-performance is a KPI id in the performance file
  window: 24h
  statistic: p95 (p5 for Cluster Performance), worst 5% ignored
  closed_when:
  - 'consumption red or performance red'
  - 'consumption orange and performance orange and risk orange or red'
  kb: vsphere/object-types/cluster/models/close-for-business
- id: book-closure-production
  use: decision
  class: production
  ...
rules:            # planning and sizing: overcommit per class, monster VM, idle VM, Guest OS sizing bands, unmap rate
- ...
```

- Two blocks per model, as the author described: consumption (utilization, saturation) and risk (utilization, saturation, reservation, allocation, monster VM). Each block is a list of metric rows.
- `instance` carries the key difference: Cluster Consumption reads cluster-wide; Cluster Risk reads the worst host. Same counter, different threshold.
- `window` and `statistic` sit on the decision, not on each input: the pack scores every 5 minutes, then the decision takes the percentile of the score.
- Five bands (grey, green, yellow, orange, red): grey stays capacity only (lint already checks it).
- A KPI used by a decision is referenced by id, never copied. One place.
- No alert rows in this file (section 5.4).
- Pros: the file reads like the model, so U7 can explain which input drove the decision. Cons: nested, unlike the flat performance rows; lint needs a second walker.

### 5.4 `thresholds-alerts.yaml`

Symptoms are the unit, as the author proposed: an alert definition reuses symptoms, so a symptom is stored once.

```yaml
uses:
  symptom: 'One test on one metric, with wait and cancel cycles. Not an alert by itself.'
  alert: 'Urgent. Red: act within 1-2 hours, pushed to phone. Orange: by end of day. No yellow alert.'
cycle: 5m        # VCF Operations collection cycle: wait 3 = 15 minutes
symptoms:
- id: sym-vm-cpu-ready-5m-above-8
  use: symptom
  pillar: performance
  type: contention                  # contention, consumption, availability
  role: issue                       # issue or gate
  object: VirtualMachine
  metric: CPU Ready
  instance: aggregate
  interval: 5m
  operator: '>'
  value: 8
  unit: '%'
  wait_cycles: 1
  cancel_cycles: null               # Q155
  class: all
  kb: vsphere/technology/cpu/configuration/cpu-alerts
  quote: VM CPU Ready above 8%;
- id: sym-vm-cpu-usage-above-1ghz
  role: gate                        # suppresses contention alerts on idle VMs; not a problem
  ...
alerts:          # thin; Q158
- id: alert-vm-cpu-contention-red
  object: VirtualMachine
  criticality: red                  # VCF Operations Critical; orange = Immediate
  match: all
  symptoms: [sym-vm-cpu-ready-5m-above-8, sym-vm-peak-vcpu-ready-20s-above-32, sym-vm-cpu-contention-above-8, sym-vm-cpu-usage-above-1ghz]
  wait_cycles: 1                    # alert level; sensitivity lives in the symptoms
  cancel_cycles: 1
  persona: infrastructure
  kb: vsphere/technology/cpu/configuration/cpu-alerts
```

- Wait and cancel cycles, mechanism (VCF Operations 9.x, TechDocs, Alert Definition Best Practices):
  - Counted in collection cycles, 5 minutes by default. Wait n: the test must be true n cycles in a row before the symptom triggers. Cancel m: false m cycles in a row before it clears.
  - The alert definition has its own wait and cancel cycles, applied after the symptom triggers. Broadcom advises sensitivity at the symptom level and alert-level cycles at 1. The design follows this: one place for the delay.
  - Time to fire is about n × 5 minutes plus collection delay. Time to clear is about m × 5 minutes.
- Wait cycle and interval are two separate filters:
  - The wait cycle filters across 5-minute cycles: persistence.
  - The 20-second peak brings spike sensitivity back inside one cycle: one 20-second burst fills the whole cycle's peak. A peak symptom with wait 1 fires on a 20-second spike.
  - The author's alerts pair a 20s peak symptom with a 5m average symptom under `all`: acute and sustained together. The file keeps both as separate symptoms so the pairing is visible.
- Cancel cycle is hysteresis: it stops an alert flapping open and closed when a metric hovers on the threshold, a known source of alert storms. Its cost: a stale alert stays open m cycles after recovery. The knowledge base gives no cancel value today (Q155).
- Gate symptoms (`role: gate`): CPU usage above 1 GHz is not a problem; it suppresses contention alerts on idle VMs (`sp5-framework/alerts/alert-design`, Performance). Without the role, a 32B model reads "usage above 1 GHz" as the cause.
- No yellow: lint refuses `criticality: yellow` and symptoms with Warning criticality. Yellow is insight (`alerts-and-insights`).
- No capacity alerts. The three alert rows in `thresholds-capacity.yaml` move here with a pillar (Q156):
  - ESXi CPU thread utilization, ESXi memory consumed with balloon: performance, consumption (host saturated now, intra-day).
  - Datastore used space above 90%: availability (a full datastore stops thin-disk writes and stuns VMs).
- Not duplicating the KPI, checked by lint: for a symptom and a KPI row with the same key (object, metric, instance, interval), the symptom value must be at or beyond the KPI red edge. Today one row fails it (Q157):
  - VM CPU Net Run alert above 95% (`alert-vm-cpu-net-run-red`); the KPI is yellow from 95, red from 99.
  - Its guard is the condition (Guest OS CPU queue above 4) and 15 minutes of wait, not the value. Either the value moves above 99, or the rule allows a lower value when a gate or a second issue symptom is required.
- Pros: symptoms reused, no duplicated tests; wait and cancel stored where VCF Operations applies them; matches the 1,951 symptoms of the alert overhaul for 1.2. Cons: without the thin `alerts` block, the `all` logic and the gates are lost, and U4 cannot answer "why did it fire".

### 5.5 `thresholds-availability.yaml` and `thresholds-security.yaml`

- Same shape as the performance file: an internal target block and an `sla` block, each with `class`.
- Availability rows that exist today: contract 99.95%, internal target 100%, maintenance window excluded (`sp5-framework/concepts/sla-metrics`, Q098). Window is a calendar period; statistic is uptime share.
- Security: after 1.0. "Is it secure?" covers security and compliance (Q102); compliance is drift against a secured configuration, measured daily; security is forensics. No rows until a source gives one.
- Recommendation: create the availability file now with its two rows, so the schema is tested; create the security file only with its first row. Lint rejects an empty catalog file.

## 6. Harness changes

- One loader for `thresholds-*.yaml`; one SQLite table per shape: `levels` (kpi edges), `tests` (sli, rule, symptom), `targets` (sla, kai), `models` and `model_inputs`, `decisions`, `alerts`, `alert_symptoms`.
- Tool `threshold(metric, object, use, class=None, interval=None, value=None)`:
  - With `value`: returns the band or pass/fail, the edges, the quote and the file.
  - Without `use`: one line per use, each with its `uses` sentence.
  - Interval or instance mismatch: "not comparable", with the reason.
- Tool `alert(id or metric)`: the alert, its symptoms with roles, total delay to fire and to clear in minutes (code adds the cycles), and the KPI row of the same metric for comparison.
- U1 (automated health check) reads the same tables. No second copy of a threshold in code.

## 7. Lint checks to add

- `use` present and in the closed list; `interval` or `window` present.
- Edges monotonic in the row's `direction`; 5 edges (performance) or 6 with grey (capacity).
- Ids unique across the five files; every id referenced by a decision or an alert exists.
- No `criticality: yellow`; alert-level cycles are 1 unless a review note explains.
- No alert row in the capacity file.
- Symptom at or beyond KPI red on the same key (section 5.4), or a gate in its alert.
- Every `kb` Markdown band table matches its edges, both ways (as today).

## 8. Alternatives considered

| Option | Pros | Cons | Verdict |
|---|---|---|---|
| A. One file for all thresholds | One join for U9; one loader | 2,000+ lines; author review hard; every change touches one file | No |
| B. One file per pillar plus alerts (the author's) | Matches the `pillar` tag and the SP5 model; KPI and SLA of a metric together; capacity keeps its model shape | Alerts span pillars; two shapes per file | Yes, with `use` on every row |
| C. One file per use (kpi, sla, models, symptoms) | Matches the engine exactly | KPI and SLA of one metric in two files; availability and security split across all files | No: `use` as a field gives the same query |
| D. A sixth file for metric identity (counter, unit, instance), rows refer to it | Metric spelled once | One more join; the 32B card needs the fields anyway | Later, if `counter` drift appears |
| E. Alerts as full definitions now | U4 complete | 1,193 definitions wait on the overhaul (1.2) | Thin block now, full catalog at 1.2 |

## 9. Risks

- Number of uses: kpi, sli, sla, model, decision, rule, symptom, alert, plus kai and kci. Ten values is the upper limit for a 32B model to keep apart. The tool output, not the model, carries them.
- Migration can break the 4 SLI rows, 31 band rows, 31 levels lines and 73 rule quotes. Migrate by script, then lint; no hand edits.
- Term clash on symptom (Q154): VCF Operations symptom definition (a test) vs SP5 symptom (a minor issue for the daily check). The file uses the product meaning; the glossary must split the two.
- `counter` keys are mostly unknown. Rows without one fall back to name matching, which is the current weakness.
- Retrieval: the catalog is not chunked, so the retrieval check should not move. Measure it before and after anyway (CLAUDE.md, Validation), and add 5 questions for U9 and U4 to M2.

## 10. Order of work

1. Author answers Q153-Q158.
2. Migrate the two current files to the new performance and capacity shape by script; lint; retrieval check before and after.
3. Move the 20 alert rows to `thresholds-alerts.yaml` as symptoms plus thin alerts; add the cycle values from Q155.
4. Harness: loader, `threshold` and `alert` tools, unit tests.
5. `thresholds-availability.yaml` with its two rows.
6. Update `KNOWLEDGE-ENGINEERING.md`, section 9, and the glossary.
7. At 1.2: full alert definitions from the overhaul repository, referencing symptom ids.

## Sources
- Broadcom TechDocs, VCF 9.0: [Alert Definition Best Practices](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-0/infrastructure-operations/configuring-alerts-and-actions/defining-alerts-best-practices.html) (alert wait cycle applies after the symptom wait cycle; set alert-level cycles to 1).
- Broadcom TechDocs, VCF 9.1: [Add a Virtual Machine CPU Usage Symptom to the Alert Definition](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/configuring-alerts-and-actions/create-a-problem-alert-definition/add-a-virtual-machine-cpu-usage-symptom-to-the-alert-definition.html) (wait cycle in collection cycles; default 1; wait 3 to skip short spikes).
- Knowledge base: `sp5-framework/performance/kpi-vs-sla`, `sp5-framework/alerts/alert-design`, `sp5-framework/alerts/alerts-and-insights`, `vcf-operations/alerts/alert-definitions`, the cluster models and `close-for-business`.
