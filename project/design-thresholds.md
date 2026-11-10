# Threshold catalog: functional design

Proposal for the author. Not indexed. Design only: no catalog file and no harness code changes until the author approves it and answers Q153-Q158.
Scope: what Agent E2 must know about thresholds, the use cases, the YAML files and their content, and the weaknesses with their mitigations.
Current state: `thresholds-performance.yaml` (47 rules, 31 band rows, 31 `levels` lines), `thresholds-capacity.yaml` (26 rules, 18 band rows).

## 1. Premises

From the author's brief and the knowledge base.

- Performance and capacity ask different questions, over different time spans. The same metric gets different thresholds.
- Alerts are for the intra-day timeline: performance, availability, configuration, compliance, security, inventory (for example too many large VMs on one host). Capacity has no alerts: it looks at weeks and months.
- Alert and KPI are different things. KPI is proactive; an alert is reactive, a guard rail when people ignore the KPI. An alert does not repeat a KPI band: it fires when the issue is urgent.
- An alert has a dimension the KPI does not have: wait cycle and cancel cycle. They remove one-off spikes and flapping.
- Performance has two uses: KPI and SLA. Different thresholds, even for the same metric.
- Agent E2 is one program: the 32B LLM, the Harness and the Agent loop working together. The design says what Agent E2 does; it names a part only where the design depends on where the work happens.

## 2. How Agent E2 handles a threshold question

Example: "Is 6% CPU Ready bad?" with a VCF Operations screenshot.

1. Agent E2 maps the user's words to its terms (term map) and pulls the metric's knowledge files into the context.
2. Agent E2 reads the screenshot: metric label, value, object, interval, time range. It shows back what it read.
3. Agent E2 looks up the thresholds of that reading in the catalog, by key (section 6).
4. When the reading is ambiguous (section 9), Agent E2 infers what it can from the attachment, then asks the user once, or answers both branches.
5. Agent E2 places the value in a band for each use that applies. The comparison is exact (catalog and calculator), not a judgment of the LLM: a 32B LLM is unreliable with ranges, open ends and lower-is-worse metrics.
6. Agent E2 explains: which use, which band, why the number sits there (from the knowledge file), what to check next.
7. Agent E2 checks its answer: every number in it must come from the context.

- What exists today: steps 1, 2, 7; one clarifying round of up to 3 questions (`harness/clarify.py`); a catalog lookup by name that returns rows without comparing them.
- What this design adds: lookup by key, the exact comparison, the use label on every result, the ambiguity signal of section 9.

## 3. Use cases

| # | Use case | Example | Time span | Files |
|---|---|---|---|---|
| U1 | Daily health check (automated) | Score every KPI and model; list objects in orange and red | Last 24 hours | performance, capacity, availability |
| U2 | Troubleshooting a complaint | "Users say VM X is slow since 10:00" | Minutes to hours | performance (KPI, not SLA: author, 2026-11-09) |
| U3 | Read a screenshot or data file | "Is 6% Ready bad?" with a chart | One reading | performance, capacity |
| U4 | Explain an alert | "Why did this alert fire? Is it real?" | One alert | alerts, performance |
| U5 | Review alert design | "We get 500 alerts a day"; "Is 4% Ready a good alert threshold?" | Design | alerts, performance |
| U6 | SLA report or breach | "Did Gold VMs meet the SLA in October?" (forensic investigation) | Calendar month | performance (SLI, SLA) |
| U7 | Capacity decision | "Can this cluster take 20 more VMs?"; close for business | 24 hours to months | capacity, performance (KPI as input) |
| U8 | Rightsizing and reclamation | "Which VMs are oversized?" | 30 days or more | capacity (grey band, sizing bands) |
| U9 | Explain a threshold | "Why is Ready 2.5% in the SLA and 8% in the alert?" | Concept | all files, one reading across uses |
| U10 | Policy setting | "What do I set in the VCF Operations policy?" | Design | the file of the use asked |
| U11 | Availability SLA (after 1.0) | "Did we meet 99.95%?" | Calendar month | availability |
| U12 | Security and compliance (after 1.0) | "How compliant is the cluster?" | Daily | security |

- U2 and U3 are the 1.0 core. U1 never passes raw metrics through the LLM: Agent E2 scores them in the Harness and the LLM reads only the findings (`ARCHITECTURE.md`, section No fast first-stage model).
- Troubleshooting has no thresholds of its own. It reads KPI levels at the interval of the reading: 20s for the VCF Operations peak and the vSphere Client real-time chart, 2s for esxtop (Q152).

## 4. Why the same metric has different thresholds

Each use has its own time span, its own spike filter and its own cost of a wrong call.

| Use | Question | Reading | Spike filter | Deadline | Cost of a false positive | Cost of a false negative |
|---|---|---|---|---|---|---|
| KPI | Is it performing now? | 20-second peak and 5-minute average, rolling window | None: the peak is wanted | None | Cheap: a line read in the daily check | VMs suffer unseen until a complaint |
| SLI | Did these 5 minutes pass the contract? | 5-minute average | The 5-minute average | None | Penalty paid for nothing | Breach not reported |
| SLA | Did the month pass? | Mean of SLI passes, calendar month | The month | Lagging | Credit on the next bill | Contract dispute |
| Alert | Must someone act today? | 5-minute average, often with a 20s peak condition | Wait cycle, cancel cycle | Red 1-2 hours; orange end of day | Alert fatigue; real alerts ignored | Outage or slowness with no one acting |
| Capacity | Is there room for weeks to months? | 95th percentile over 24 hours; monthly trend | Percentile: the worst 5% ignored | Weeks | Hardware bought early | Contention for months; long lead time |

- Example, ESXi CPU thread utilization: Cluster Consumption red from 85% (cluster-wide, p95 of 24 h); Cluster Risk red from 90% (worst host); alert above 40% thread with core utilization above 80% for 10 minutes (one host).
- Example, VM CPU Ready: KPI on the worst vCPU at 20s (yellow 2, orange 4, red 8); SLI on the VM total at 5m (fail above 2.5%); alert on the VM total at 5m (orange above 4%, red above 8%) with peak vCPU Ready, contention and a usage gate.
- A threshold therefore has six parts:

```text
threshold = (use, reading key, class of service) -> values, spike filter, source
reading key = (object, metric, instance, interval or window statistic)
```

## 5. Proactive and reactive: consistency

KPI (proactive), SLI (contract) and alert (reactive) watch the same resources. They must not contradict each other, and the alert must not repeat the KPI.

### 5.1 Two dominance rules
- Peak dominates average: the 20-second peak of an interval is at least its 5-minute average.
- Worst instance dominates aggregate: the worst vCPU or virtual disk is at least the VM value (`observability/thresholds`, Instance rule).
- So a reading on the worst instance at 20s is never below the same metric on the VM total at 5m. The KPI reads the dominant reading; the SLI and the alert read the dominated one.

### 5.2 Nesting
- With those rules, each later stage is a subset of the earlier one:

```text
alert red  ⊂  alert orange  ⊂  SLI fail  ⊂  KPI not green
```

- VM CPU Ready: alert red (total, 5m, above 8) means the worst vCPU at 20s is above 8: KPI red. Alert orange (above 4) means KPI at least orange and the SLI (above 2.5) already failed. An SLI fail means KPI at least yellow (from 2).
- VM memory contention: SLI fail (above 1%, 5m) means KPI peak at least orange (from 1); alert orange (above 3%) means KPI red (from 2).
- Every alert therefore fires on an object whose KPI was already at that colour or worse. The KPI warned first; the time between is the prevention window (`sp5-framework/alerts/alerts-and-insights`).

### 5.3 Rules
- C1. When an alert of colour C fires, the KPI of the same object and resource is at C or worse. Checked by lint where the alert reading is dominated by the KPI reading.
- C2. KPI red without an alert is normal. The wait cycle, the cancel cycle and the gates (section 8.3) keep the alert for what persists and matters. This gap is the point of the design, not a defect.
- C3. Every metric alert has a parent KPI or model on the same object and resource: no alert without a proactive view.
- C4. Every KPI resource on every object has an alert or a stated reason why not (the "Not yet" and "N/A" cells of `sp5-framework/alerts/alert-design`).
- C5. Colours mean different things. KPI colour: how bad, no deadline. Alert colour: by when (red 1-2 hours, orange end of day). Same word, different scale; the answer always names which.
- C6. Never the same reading and the same number in a KPI edge and an alert. Today one alert breaks C1 and C6: VM CPU Net Run above 95% (red alert, 5m) on the same reading as the KPI's yellow edge (95) (Q157).

## 6. The reading key

Every row in every file uses a key, never an English name.

### 6.1 What Agent E2 needs
| Where the reading comes from | What it shows | Key it carries |
|---|---|---|
| VCF Operations screenshot | Display name, often localized: "CPU \| Ready (%)" | None visible |
| vSphere Client chart | Label: "Readiness", "Ready" | None visible |
| esxtop | Field: `%RDY` | Field name |
| VCF Operations export (1.2) | Display name; sometimes the metric key | VCF Operations key, sometimes |
| vCenter export (1.2) | Label | None |
| Live VCF Operations (after 1.0) | API | VCF Operations key, `cpu\|readyPct` |
| Live vCenter (after 1.0) | API | vCenter counter, `cpu.ready.summation` |
| User's words | "steal time", "CPU wait" | None |

- No external key covers all of these.
  - VCF Operations key: no esxtop field; no book metric outside the product; renamed across vRealize, Aria and VCF Operations releases; the same name on VM and host means different things.
  - vCenter key: no VCF Operations derived metric (peak among vCPUs, KPIs, vCommunity pack); a counter carries several rollups.
- Design call: Agent E2 has its own key, one per reading, and a mapping from each key to every external name and key.

### 6.2 Key format
- Readable slug, lowercase, dot-separated parts from closed lists: `object.resource.measure.instance.statistic`.
  - `vm.cpu.ready.vcpu-max.peak20s`: Peak CPU Ready among any vCPU.
  - `vm.cpu.ready.total.avg5m`: VM CPU Ready, 5-minute average (SLI and alert).
  - `esxi.mem.consumed.total.avg5m`; `cluster.mem.consumed.host-max.avg5m` (Cluster Risk input).
- Readable, not opaque: a 32B LLM copies and matches a slug far more reliably than a number or a hash, and the slug shows the instance and interval to the author.
- Stable: product renames change the mapping, never the key.
- Unit is not in the key: a VCF Operations % and a vCenter summation in ms are the same reading; the mapping holds the conversion (calculator).

### 6.3 Mapping file
- A sixth file, `knowledge/catalog/readings.yaml`, one row per key:

```yaml
- key: vm.cpu.ready.vcpu-max.peak20s
  object: VirtualMachine
  resource: cpu
  measure: ready
  instance: worst vCPU
  statistic: highest 20-second value in the 5-minute cycle
  unit: '%'
  names: ['Peak CPU Ready among any vCPU', 'Peak vCPU Ready']   # how screens, books and users write it
  vcf_operations: null            # metric key, when the 9.1 metric reference gives it
  vcenter: null                   # no vCenter counter: VCF Operations derives it
  esxtop: null
  dominates: [vm.cpu.ready.total.avg5m]   # section 5.1; used by lint for rule C1
  same_name: [esxi.cpu.ready.total.avg5m]  # confusable reading on another object
  kb: vsphere/technology/cpu/metrics/virtual-motherboard/ready
```

- The threshold files hold only the key and the threshold. Names, units and external keys live once, here.
- `dominates` makes the nesting of section 5 checkable.
- To do: fill `vcf_operations` from the VCF Operations 9.1 metric reference (already open under M1), `vcenter` from `vcenter-counters.yaml`, `esxtop` from `esxtop-fields.yaml`.

## 7. Design rules for a 32B LLM

- The LLM reads lookup results, not the YAML. A result is short (under 300 tokens: the 16K context also carries files and screenshots), names the use, the reading, the band and the source file.
- The comparison of a value against a threshold is exact (section 2, step 5).
- `use` is part of every result. A lookup without a use returns one line per use, each saying when it applies, so a KPI band is never read as an SLA test.
- A value on a different reading is not compared: "not comparable: this band is for 20-second peaks" (Interval rule). No silent 4x conversion.
- No null in a result: "no source value", so the LLM does not read it as 0.
- One copy of each number. Today a KPI band exists as a band row, a `levels` line and a Markdown table; the YAML keeps one copy, the Markdown table stays for retrieval, lint checks they match.
- Closed lists for `use`, `pillar`, `interval`, `statistic`, `direction`, `class`, `instance`, `role` and the key parts, in `project/tools/tags.yaml`.
- Every row keeps `kb` and `quote`: Agent E2 cites the file, and lint keeps the number tied to its text.
- The why comes with the number. Each result carries the reason in one line and the `kb` file id, and Agent E2 reads the file when the question asks why (U9) or when it must judge a customer's own threshold (U5).
- A short up-front block states the threshold model (uses, reading key, spike filter per use, colours), like `harness/misreadings.md`: Agent E2 knows the frame before any lookup.

## 8. Files

Six files: four pillars, alerts, and the reading keys.

| File | Holds | In 1.0 |
|---|---|---|
| `readings.yaml` | Reading keys and their mapping (section 6.3) | Yes |
| `thresholds-performance.yaml` | KPI edges, SLI tests, SLA targets, performance rules | Yes |
| `thresholds-capacity.yaml` | Capacity and risk models, decisions, planning and sizing rules | Yes |
| `thresholds-alerts.yaml` | Symptom definitions; thin alert definitions (Q158) | Yes, the author's alerts from the book |
| `thresholds-availability.yaml` | Internal target and SLA | Two rows (99.95%, 100%); rest to do |
| `thresholds-security.yaml` | Compliance and security targets and SLA | To do |

### 8.1 Common fields
| Field | Values | Why |
|---|---|---|
| `id` | unique across all files | Reference from other files and from questions |
| `use` | kpi, sli, sla, model, decision, rule, symptom, alert (+ kai, kci per Q153) | First filter of every lookup |
| `reading` | key from `readings.yaml` | The join across files and uses |
| `direction` | above, below | Lower is worse for free memory, KPI scores, SLA |
| `interval` or `window` + `statistic` | 2s, 20s, 5m; 24h p95; calendar month mean | What the number applies to; one of them always present |
| `class` | all, gold, silver, bronze, production, non-production | Thresholds per class of service |
| `source`, `kb`, `quote` | as today | Traceability; lint |

### 8.2 `thresholds-performance.yaml`
```yaml
uses:
  kpi: 'Proactive. Is it performing now? Rolling window, 20-second accuracy, no deadline. Yellow is read in the daily check.'
  sli: 'Pass or fail of one 5-minute interval against the contract.'
  sla: 'Monthly mean of SLI passes, per class of service. Lagging.'
kpi:
- id: vm-kpi-peak-cpu-ready-any-vcpu
  reading: vm.cpu.ready.vcpu-max.peak20s
  kpi: VM Performance (%)
  group: contention
  direction: above
  edges: [0, 2, 4, 8, 16]          # green start, yellow, orange, red, red end
  source: book
  kb: vsphere/object-types/vm/kpis/vm-performance
sli:
- id: vm-sli-cpu-ready
  reading: vm.cpu.ready.total.avg5m
  direction: above
  fail: 2.5
  class: all
  kb: sp5-framework/concepts/sla-metrics
  quote: '| CPU | Ready | above 2.5% |'
sla:
- id: performance-sla-gold
  reading: vm.performance.sla.total.month-mean
  direction: below
  fail: 99.9
  class: gold
  kb: sp5-framework/performance/noisy-neighbour
  quote: 'Performance SLA thresholds: Gold 99.9%, Silver 99.8%, Bronze 99.6%.'
rules: []
```
- The interval is in the reading key, so the 9-value grid (5m, 20s, 2s) becomes up to three KPI rows, one per reading (Q152).
- `edges` replaces the band rows and the `levels` table. The red end stays: KPI scoring places a value inside its band.
- One boundary rule: a value on an edge belongs to the better band (as Close for Business does).
- KPI has no `class` (one policy for all); SLA always has one.

### 8.3 `thresholds-capacity.yaml`
Capacity is a model, so the file mirrors the model: models, groups, input rows, then decisions.
```yaml
models:
- id: cluster-consumption
  use: model
  object: ClusterComputeResource
  score: {direction: above, edges: [0, 25, 50, 75, 100]}
  inputs:
  - id: cluster-consumption-cpu-thread-utilization
    group: utilization
    reading: cluster.cpu.thread-utilization.total.avg5m
    direction: above
    edges: [0, 55, 70, 85, 100]
    grey: null                       # wastage; Q110
    excluded_when_green: false
- id: cluster-risk
  use: model
  inputs:
  - id: cluster-risk-highest-memory-consumed
    group: utilization
    reading: cluster.mem.consumed.host-max.avg5m
    edges: [null, 80, 90, 95, 100]
    excluded_when_green: true
decisions:
- id: close-for-business
  inputs: [cluster-performance, cluster-consumption, cluster-risk]
  window: 24h
  statistic: p95 (p5 for Cluster Performance), worst 5% ignored
  closed_when:
  - consumption red or performance red
  - consumption orange and performance orange and risk orange or red
rules: []          # overcommit per class, monster VM, idle VM, Guest OS sizing bands, unmap rate
```
- Consumption block: utilization, saturation. Risk block: utilization, saturation, reservation, allocation, monster VM.
- The reading key carries the key difference: Cluster Consumption reads cluster-wide, Cluster Risk the worst host.
- A KPI used by a decision is referenced by id, never copied.
- Five bands with grey (capacity only). No alert rows.
- 1.0: Agent E2 reads the scores the vCommunity pack publishes; the file holds their parameters for explanation. Recomputing a model is to do (section 12).

### 8.4 `thresholds-alerts.yaml`
```yaml
cycle: 5m        # VCF Operations collection cycle: wait 3 = 15 minutes
symptoms:
- id: sym-vm-cpu-ready-above-8
  pillar: performance
  type: metric                      # metric, property, event
  role: issue                       # issue or gate
  reading: vm.cpu.ready.total.avg5m
  operator: '>'
  value: 8
  wait_cycles: 1
  cancel_cycles: null               # Q155
  class: all
  kb: vsphere/technology/cpu/configuration/cpu-alerts
  quote: VM CPU Ready above 8%;
- id: sym-vm-cpu-usage-above-1ghz
  role: gate                        # not a problem: it keeps contention alerts off idle VMs
- id: sym-host-monster-vm-count-above-n
  pillar: inventory
  type: property
alerts:          # thin (Q158)
- id: alert-vm-cpu-contention-red
  criticality: red                  # VCF Operations Critical; orange is Immediate; no yellow
  match: all
  symptoms: [sym-vm-cpu-ready-above-8, sym-vm-peak-vcpu-ready-above-32, sym-vm-cpu-contention-above-8, sym-vm-cpu-usage-above-1ghz]
  wait_cycles: 1
  cancel_cycles: 1
  persona: infrastructure
```
- Pillars: performance (contention, consumption), availability, configuration, compliance, security, inventory. Never capacity.
- Symptom types: metric (a reading against a value), property (a setting or a count: hardware version, too many monster VMs on one host), event (a fault or message). Wait and cancel cycles apply to metric and property symptoms.
- The same reading can be a capacity input and an alert symptom: monster VM concentration is a Cluster Risk input (planning, daily) and an inventory alert (a placement today that cannot wait). Different uses, different thresholds, one reading key.
- Wait and cancel cycles (Broadcom TechDocs, Alert Definition Best Practices):
  - counted in collection cycles, 5 minutes by default. Wait n: true n cycles in a row before the symptom triggers. Cancel m: false m cycles in a row before it clears;
  - the alert definition has its own cycles, applied after the symptom triggers. Broadcom advises the delay in the symptom and alert-level cycles at 1; the design follows it;
  - time to fire about n × 5 minutes; time to clear about m × 5 minutes.
- Wait cycle and interval are separate filters. The wait cycle filters across cycles (persistence). A 20-second peak puts spike sensitivity back inside one cycle: one burst fills the cycle's peak, so a peak symptom with wait 1 fires on a 20-second spike. The author's alerts pair a peak symptom with a 5-minute average symptom under `all`.
- The cancel cycle stops an alert flapping when a metric hovers on its threshold. Its cost: the alert stays open m cycles after recovery.
- Gate symptoms keep contention alerts off idle VMs (`sp5-framework/alerts/alert-design`). Without the role, Agent E2 could read "usage above 1 GHz" as the cause.
- The three alert rows in the capacity file move here (Q156): the ESXi CPU and memory rows to performance consumption, the datastore row to availability.

### 8.5 `thresholds-availability.yaml` and `thresholds-security.yaml`
- Same shape as the performance file: an internal target block and an `sla` block, each with `class`.
- Availability, 1.0: contract 99.95%, internal 100%, maintenance window excluded (`sp5-framework/concepts/sla-metrics`, Q098).
- Both files are open for contributors (section 12).

## 9. Ambiguity: when Agent E2 asks

A question rarely gives all six parts of the threshold. A screenshot shows one number; the user's own VCF Operations may use its own thresholds. Agent E2 must not guess.

### 9.1 What Agent E2 does today
- One clarifying round per question, at most 3 questions, then it answers (`harness/clarify.py`; MISSION.md, section 5).
- Asks when the question is odd, when the text and an attachment disagree, or when one missing fact changes the answer: object, layer, interval, version.
- Never asks what the knowledge base or an attachment already answers; otherwise answers and states its assumption first.
- Gaps for thresholds:
  - the list of missing facts lacks instance, class of service, use, and the customer's own setting;
  - the decision to ask is a judgment of the LLM: nothing tells it that the thresholds differ for the missing part;
  - the round covers one question; an answer given (class, interval) is not carried to the next question;
  - the benchmark is single turn, so asking is not measured (open under M2).

### 9.2 Proposed
- The threshold lookup reports which key parts change the verdict: "depends on interval: 20s peak orange (KPI); 5m average fails the SLI". That is an exact signal, not a guess.
- Then Agent E2, in this order:
  1. infers the part from the attachment: chart title (Real-time is 20s; Past day is 5m), metric name (Peak means 20s peak; "among any vCPU" means worst instance), object in the breadcrumb;
  2. answers both branches when they are at most two and lead to the same next step;
  3. otherwise asks, naming why the part matters ("because the 20-second peak and the 5-minute average have different thresholds").
- Missing facts that trigger a question, added to the clarifying rule: instance, use, class of service, the customer's own setting.
- Recommended vs configured: every threshold in an answer is labelled "recommended (Agent E2)" or "configured (your VCF Operations)". When the question is about the user's own alert or policy ("why did this alert fire"), Agent E2 asks for the alert definition (symptoms, thresholds, wait and cancel cycles), or answers with the recommended set and says so. At 1.2 the shipped VCF Operations alert definitions are in the catalog, so Agent E2 can recognise a default alert by its name.
- Class of service: ask once when it changes the answer; show all classes when there are three or fewer rows.
- Carry the user's answers (class, interval, configured thresholds) to later questions in the same conversation.

## 10. Lint checks to add

- `use` and `reading` on every row; the reading exists in `readings.yaml`; `interval` or `window` present.
- Edges monotonic in the row's `direction`; 5 edges (performance) or 6 with grey (capacity).
- Ids unique across files; every id a decision or an alert names exists.
- No `criticality: yellow`; alert-level cycles are 1 unless a review note explains.
- No alert row in the capacity file; no capacity pillar in the alerts file.
- Rules C1 and C6 (section 5.3) where the readings are linked by `dominates` or are the same.
- Every `kb` Markdown band table matches its edges, both ways.

## 11. Alternatives considered

| Option | Pros | Cons | Verdict |
|---|---|---|---|
| A. One file for all thresholds | One join for U9 | 2,000+ lines; author review hard | No |
| B. One file per pillar plus alerts (the author's) | Matches the `pillar` tag and the SP5 model; KPI and SLA of a reading together | Alerts span pillars; two shapes per file | Yes, with `use` and `reading` on every row |
| C. One file per use | Matches the scoring exactly | KPI and SLA of one reading in two files | No: `use` as a field gives the same query |
| D. External key (VCF Operations or vCenter) instead of an own key | No mapping file | Neither covers esxtop, book metrics and derived metrics; product renames break rows | No: own key plus mapping |
| E. Alerts as full definitions now | U4 complete | 1,193 definitions wait on the overhaul (1.2) | Thin block now, full catalog at 1.2 |

## 12. To do

### For contributors
- `thresholds-availability.yaml`: availability SLA and internal target per class; the source named in the plan is the vCommunity adapter's Operational Availability page.
- `thresholds-security.yaml`: compliance and security targets (KCI per Q153), SLA; "is it secure?" covers security and compliance (Q102).
- `readings.yaml`: VCF Operations keys from the 9.1 metric reference; vCenter and esxtop columns from the existing catalog files.
- Alert symptoms for configuration, compliance and inventory, as the author defines them.

### After 1.0
- Capacity: Agent E2 recomputes Cluster Consumption, Cluster Risk and Close for Business from the inputs, for what-if questions ("what if I add 20 VMs?") and for clusters without the vCommunity pack. In 1.0 it reads the published scores.
- Full alert definition catalog from the overhaul (1.2), referencing symptom ids.
- Live VCF Operations: read the configured thresholds and alert definitions, so the recommended vs configured comparison needs no screenshot.

## 13. Risks

- Ten `use` values is the upper limit for a 32B LLM to keep apart. Every result names its use.
- Migration touches 4 SLI rows, 31 band rows, 31 levels lines and 73 rule quotes. By script, then lint.
- Symptom has two meanings (Q154): the VCF Operations symptom definition (a test) and the SP5 symptom (a minor issue for the daily check).
- Most VCF Operations keys are unknown today; until filled, screen names map to keys through the `names` list.
- The catalog is not chunked, so retrieval should not move; the retrieval check is run before and after anyway. New questions for U4, U5 and U9 go to M2.

## Sources
- Broadcom TechDocs, VCF 9.0: [Alert Definition Best Practices](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-0/infrastructure-operations/configuring-alerts-and-actions/defining-alerts-best-practices.html).
- Broadcom TechDocs, VCF 9.1: [Add a Virtual Machine CPU Usage Symptom to the Alert Definition](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/configuring-alerts-and-actions/create-a-problem-alert-definition/add-a-virtual-machine-cpu-usage-symptom-to-the-alert-definition.html).
- Knowledge base: `sp5-framework/performance/kpi-vs-sla`, `sp5-framework/alerts/alert-design`, `sp5-framework/alerts/alerts-and-insights`, `vcf-operations/alerts/alert-definitions`, the cluster models, `close-for-business`, `observability/thresholds`.
