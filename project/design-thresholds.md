# Thresholds in Agent E2: design and implementation

Status: design. Section 3 describes what is built today; sections 4-13 describe the target; section 14 lists the work. No catalog file or harness change is made until the design is approved and Q153-Q158 are answered.
Not indexed.

## 1. Goal

- Agent E2 knows every threshold it needs, applies the right one to the reading in front of it, explains why that number sits there, and never mixes the uses.
- Agent E2 is one program: a 32B LLM, the Harness and the Agent loop working together. This document says what Agent E2 does. It names a part (LLM, Harness, catalog, verifier) only where the design depends on where the work happens.

## 2. Domain premises

- Performance and capacity ask different questions over different time spans, so the same metric has different thresholds.
- Alerts are for the intra-day timeline: performance, availability, configuration, compliance, security, inventory (for example too many large VMs on one host). Capacity has no alerts: it looks at weeks and months.
- Alert and KPI are different things. KPI is proactive; an alert is reactive, a guard rail when people ignore the KPI. An alert fires when the issue has become urgent, so it does not repeat a KPI band.
- An alert has a dimension the KPI does not have: wait cycle and cancel cycle. They remove one-off spikes and flapping.
- Performance has two uses, KPI and SLA, with different thresholds for the same metric.

## 3. As built today

### 3.1 Files
| File | Content |
|---|---|
| `knowledge/catalog/thresholds-performance.yaml` | 47 rule rows (one value: above X means Y), 31 band rows (green, yellow, orange, red as ranges), 31 `levels` lines (yellow, orange, red for 5m, 20s, 2s; filled from the band rows) |
| `knowledge/catalog/thresholds-capacity.yaml` | 26 rule rows, 18 band rows with a grey (wastage) band |
| Knowledge files | Each KPI and model file keeps its colour-band table in Markdown; each rule row quotes a sentence of its file |

- Alert thresholds are rule rows with the wait time inside the `condition` text ("for 15 minutes"). Three of them sit in the capacity file.
- Rows are joined by the metric's English name; no key.

### 3.2 How Agent E2 uses them
1. Start-up: `harness/catalog.py` loads both files into an in-memory SQLite catalog: tables `thresholds` (rules), `bands`, `levels`.
2. Term map (`harness/terms.py`, `knowledge/catalog/user-terms.yaml`): the user's words pull the metric's knowledge files into the context. No threshold is fetched here.
3. Classic mode: `Catalog.facts_for(ids)` adds up to 14 "Catalog facts (exact)" lines for the files in the context: counters and rule rows. Band rows are not included.
4. Agentic mode: the LLM may call the `catalog` tool with a name. `Catalog.lookup` scores every counter, esxtop field, metric file and threshold row against the name (word overlap, `_score`) and returns the 8 best of each.
5. The LLM reads the rows, picks one, compares the value itself and writes the answer.
6. Prompt rules (`harness/modes.py`, `harness/primer.py`): "Quote a threshold only when the knowledge base states it"; "For a threshold, call catalog. Its values are exact."
7. Verifier (`harness/verify.py`): a number with a unit in the reason line that is not in the question or the context is recorded as "ungrounded" in the trace. Soft: it does not trigger a repair.
8. Clarifying (`harness/clarify.py`, shipped conversation only): one round of up to 3 questions when the question is odd, the text and an attachment disagree, or one missing fact (object, layer, interval, version) changes the answer.
9. Quality checks: lint checks every row (fields, allowed values, quote still in its file), band rows against the Markdown tables both ways, and `levels` against the band rows. `project/tools/threshold_inventory.py` lists thresholds written in prose without a row. `harness/test_tools.py` checks that lookups return sourced thresholds.

### 3.3 Gaps in what is built
| # | Gap | Effect on an answer |
|---|---|---|
| G1 | Lookup by fuzzy name | "Ready" returns VM, ESXi and cluster rows mixed; the LLM picks |
| G2 | Rule results leave out `interval` and `instance` | The LLM cannot tell a 20s peak threshold from a 5-minute one |
| G3 | No use label on a row | A KPI band, an SLI test and an alert threshold look alike |
| G4 | The LLM compares the value | Errors on ranges, open ends and lower-is-worse metrics |
| G5 | `levels` is loaded but no lookup returns it | The 9-value grid is invisible to Agent E2 |
| G6 | Classic mode sends rules, not bands | KPI colours reach the LLM only inside the Markdown file, if it was retrieved |
| G7 | Wait cycles are free text inside `condition` | Agent E2 cannot compute when an alert fires or clears |
| G8 | No signal that the answer depends on a missing fact | Asking is left to the LLM's judgment |
| G9 | Ungrounded-number check is soft and reason-line only | A wrong threshold in the answer body passes |
| G10 | Three copies of each KPI band (band row, `levels` line, Markdown table) | Drift; lint has to hold them together |

## 4. Use cases

| # | Use case | Example | Time span | Files | Release |
|---|---|---|---|---|---|
| U1 | Daily health check over many objects | Score every KPI and model; list objects in orange and red | Last 24 hours | performance, capacity, availability | Needs data: exports (1.2) or live VCF Operations (after 1.0) |
| U2 | Troubleshooting a complaint | "Users say VM X is slow since 10:00" | Minutes to hours | performance (KPI, not SLA) | 1.0 |
| U3 | Read a screenshot | "Is 6% Ready bad?" with a chart | One reading | performance, capacity | 1.0 |
| U4 | Explain an alert | "Why did this alert fire? Is it real?" | One alert | alerts, performance | 1.0 |
| U5 | Review alert design | "We get 500 alerts a day"; "Is 4% Ready a good alert threshold?" | Design | alerts, performance | 1.0 |
| U6 | SLA report or breach | "Did Gold VMs meet the SLA in October?" (forensic investigation) | Calendar month | performance (SLI, SLA) | 1.0 |
| U7 | Capacity decision | "Can this cluster take 20 more VMs?"; close for business | 24 hours to months | capacity, performance (KPI as input) | 1.0 |
| U8 | Rightsizing and reclamation | "Which VMs are oversized?" | 30 days or more | capacity (grey band, sizing bands) | 1.0 |
| U9 | Explain a threshold | "Why is Ready 2.5% in the SLA and 8% in the alert?" | Concept | all files, one reading across uses | 1.0 |
| U10 | Policy setting | "What do I set in the VCF Operations policy?" | Design | the file of the use asked | 1.0 |
| U11 | Availability SLA | "Did we meet 99.95%?" | Calendar month | availability | After 1.0 |
| U12 | Security and compliance | "How compliant is the cluster?" | Daily | security | After 1.0 |

- U2, U3 and U9 are the 1.0 core.
- In U1, raw metrics never pass through the LLM: Agent E2 scores them in the Harness, and the LLM reads only the findings (`ARCHITECTURE.md`, section No fast first-stage model).
- Troubleshooting has no thresholds of its own. It reads the KPI levels at the interval of the reading: 20s for the VCF Operations peak and the vSphere Client real-time chart, 2s for esxtop (Q152).

## 5. Why the same metric has different thresholds

Each use has its own time span, spike filter and cost of a wrong call.

| Use | Question | Reading | Spike filter | Deadline | Cost of a false positive | Cost of a false negative |
|---|---|---|---|---|---|---|
| KPI | Is it performing now? | 20-second peak and 5-minute average, rolling window | None: the peak is wanted | None | A line read in the daily check | VMs suffer unseen until a complaint |
| SLI | Did these 5 minutes pass the contract? | 5-minute average | The 5-minute average | None | Penalty paid for nothing | Breach not reported |
| SLA | Did the month pass? | Mean of SLI passes, calendar month | The month | Lagging | Credit on the next bill | Contract dispute |
| Alert | Must someone act today? | 5-minute average, often with a 20s peak condition | Wait cycle, cancel cycle | Red 1-2 hours; orange end of day | Alert fatigue; real alerts ignored | Outage or slowness with no one acting |
| Capacity | Is there room for weeks to months? | 95th percentile over 24 hours; monthly trend | Percentile: the worst 5% ignored | Weeks | Hardware bought early | Contention for months; long lead time |

- ESXi CPU thread utilization: Cluster Consumption red from 85% (cluster-wide, p95 of 24 h); Cluster Risk red from 90% (worst host); alert above 40% thread with core utilization above 80% for 10 minutes (one host).
- VM CPU Ready: KPI on the worst vCPU at 20s (yellow 2, orange 4, red 8); SLI on the VM total at 5m (fail above 2.5%); alert on the VM total at 5m (orange above 4%, red above 8%) with peak vCPU Ready, contention and a usage gate.
- A threshold therefore has six parts:

```text
threshold   = (use, reading key, class of service) -> values, spike filter, source
reading key = (object, metric, instance, interval or window statistic)
```

## 6. Proactive and reactive: consistency

### 6.1 Two dominance rules
- Peak dominates average: the 20-second peak of an interval is at least its 5-minute average.
- Worst instance dominates aggregate: the worst vCPU or virtual disk is at least the VM value (`observability/thresholds`, Instance rule).
- The KPI reads the dominant reading; the SLI and the alert read the dominated one.

### 6.2 Nesting
```text
alert red  ⊂  alert orange  ⊂  SLI fail  ⊂  KPI not green
```
- VM CPU Ready: alert red (total, 5m, above 8) means the worst vCPU at 20s is above 8: KPI red. Alert orange (above 4) means KPI at least orange and the SLI (above 2.5) already failed. An SLI fail means KPI at least yellow.
- VM memory contention: SLI fail (above 1%, 5m) means KPI peak at least orange (from 1); alert orange (above 3%) means KPI red (from 2).
- An alert fires only on an object whose KPI was already at that colour or worse. The KPI warned first; the time between is the prevention window (`sp5-framework/alerts/alerts-and-insights`).

### 6.3 Rules
- C1. When an alert of colour C fires, the KPI of the same object and resource is at C or worse. Lint checks it where the readings are linked by `dominates` (section 7.3).
- C2. KPI red without an alert is normal: wait cycles, cancel cycles and gates keep the alert for what persists and matters.
- C3. Every metric alert has a parent KPI or model on the same object and resource.
- C4. Every KPI resource on every object has an alert or a stated reason why not (the "Not yet" and "N/A" cells of `sp5-framework/alerts/alert-design`).
- C5. KPI colour means how bad, with no deadline. Alert colour means by when. Every answer names which.
- C6. A KPI edge and an alert never share the same reading and number. Today VM CPU Net Run breaks C1 and C6: red alert above 95% on the reading whose KPI yellow edge is 95 (Q157).

## 7. The reading key

### 7.1 What Agent E2 receives
| Input | Shows | Key visible |
|---|---|---|
| VCF Operations screenshot | Display name, sometimes localized: "CPU \| Ready (%)" | None |
| vSphere Client chart | Label: "Readiness", "Ready" | None |
| esxtop | Field: `%RDY` | Field name |
| VCF Operations export (1.2) | Display name; sometimes the metric key | Sometimes |
| vCenter export (1.2) | Label | None |
| Live VCF Operations (after 1.0) | API | VCF Operations key, `cpu\|readyPct` |
| Live vCenter (after 1.0) | API | vCenter counter, `cpu.ready.summation` |
| User's words | "steal time", "CPU wait" | None |

- No external key covers all inputs. The VCF Operations key has no esxtop field and no book metric, and changes with product renames. The vCenter key has no VCF Operations derived metric (peak among vCPUs, KPIs) and several rollups per counter.
- So Agent E2 has its own key, one per reading, with a mapping to every external name and key.

### 7.2 Format
- Readable slug from closed lists: `object.resource.measure.instance.statistic`.
  - `vm.cpu.ready.vcpu-max.peak20s`: Peak CPU Ready among any vCPU.
  - `vm.cpu.ready.total.avg5m`: VM CPU Ready, 5-minute average.
  - `cluster.mem.consumed.host-max.avg5m`: Cluster Risk input.
- A 32B LLM copies and matches a slug more reliably than a number or a hash; the slug also shows instance and interval.
- Product renames change the mapping, never the key.
- Unit is not in the key: a VCF Operations % and a vCenter summation in ms are one reading; the calculator converts.

### 7.3 `knowledge/catalog/readings.yaml`
```yaml
- key: vm.cpu.ready.vcpu-max.peak20s
  object: VirtualMachine
  resource: cpu
  measure: ready
  instance: worst vCPU
  statistic: highest 20-second value in the 5-minute cycle
  unit: '%'
  names: ['Peak CPU Ready among any vCPU', 'Peak vCPU Ready']
  vcf_operations: null
  vcenter: null
  esxtop: null
  dominates: [vm.cpu.ready.total.avg5m]
  same_name: [esxi.cpu.ready.total.avg5m]
  hints: ['"Peak" in a VCF Operations metric name means the 20-second peak', '"among any vCPU" means the worst vCPU']
  kb: vsphere/technology/cpu/metrics/virtual-motherboard/ready
```
- Threshold rows hold only the key and the threshold; names, units and external keys live here once.
- `names` lets Agent E2 map a screen label to a key; `hints` let it infer instance and interval from an attachment (section 10).
- `dominates` makes section 6 checkable; `same_name` carries the existing trap guard (same label, other object).

## 8. Threshold files

| File | Holds | 1.0 |
|---|---|---|
| `readings.yaml` | Reading keys and mapping | Yes |
| `thresholds-performance.yaml` | KPI edges, SLI tests, SLA targets, performance rules | Yes |
| `thresholds-capacity.yaml` | Capacity and risk models, decisions, planning and sizing rules | Yes |
| `thresholds-alerts.yaml` | Symptom definitions; thin alert definitions (Q158) | Yes |
| `thresholds-availability.yaml` | Internal target and SLA | Two rows (99.95%, 100%); rest open to contributors |
| `thresholds-security.yaml` | Compliance and security targets and SLA | Open to contributors |

### 8.1 Common fields
| Field | Values | Why |
|---|---|---|
| `id` | unique across all files | Reference from other files and from questions |
| `use` | kpi, sli, sla, model, decision, rule, symptom, alert (+ kai, kci per Q153) | First filter of every lookup |
| `reading` | key from `readings.yaml` | The join across files and uses |
| `direction` | above, below | Lower is worse for free memory, KPI scores, SLA |
| `window` + `statistic` | 24h p95; calendar month mean | Window-level uses (sla, model, decision); sample-level uses take the interval from the reading key |
| `class` | all, gold, silver, bronze, production, non-production | Thresholds per class of service |
| `source` | `knowledge-base`, or a vendor document with its version | Which source wins: version-bound vendor facts can go stale (Q159) |
| `kb`, `quote` | knowledge file id; sentence copied from it | Citation; lint keeps the number tied to its text |

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
  why: null                        # one sentence copied from the kb file; the VM KPI file has none per row yet
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
- The interval is in the reading key, so the 5m, 20s, 2s grid becomes up to three KPI rows (Q152).
- `edges` replaces the band rows and the `levels` table (G10). The red end stays: KPI scoring places a value inside its band.
- `why` is one sentence copied from the knowledge file and returned with the number. Most KPI files have no such sentence per row yet: to write, then lint checks the copy.
- One boundary rule: a value on an edge belongs to the better band (as Close for Business does).
- KPI has no `class`; SLA always has one.

### 8.3 `thresholds-capacity.yaml`
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
- The reading key carries the difference: Cluster Consumption reads cluster-wide, Cluster Risk the worst host.
- A KPI used by a decision is referenced by id, never copied.
- Five bands with grey; no alert rows.
- 1.0: Agent E2 reads the scores the vCommunity pack publishes; the parameters serve explanation. Recomputing is after 1.0 (section 14.3).

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
  role: gate                        # not a problem: keeps contention alerts off idle VMs
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
- Symptom types: metric (a reading against a value), property (a setting or a count), event (a fault or message). Wait and cancel cycles apply to metric and property symptoms.
- One reading can be a capacity input and an alert symptom: monster VM concentration is a Cluster Risk input (daily planning) and an inventory alert (a placement that cannot wait).
- Wait and cancel cycles (Broadcom TechDocs, Alert Definition Best Practices):
  - counted in collection cycles, 5 minutes by default. Wait n: true n cycles in a row before the symptom triggers. Cancel m: false m cycles in a row before it clears;
  - the alert definition has its own cycles, applied after the symptom triggers; Broadcom advises the delay in the symptom and alert-level cycles at 1;
  - time to fire about n × 5 minutes; time to clear about m × 5 minutes.
- The wait cycle filters across cycles (persistence). A 20-second peak puts spike sensitivity back inside one cycle: a peak symptom with wait 1 fires on one 20-second burst. The alerts pair a peak symptom with a 5-minute average symptom under `all`.
- The cancel cycle stops an alert flapping on its threshold, at the cost of staying open m cycles after recovery.
- The three alert rows now in the capacity file move here (Q156).

### 8.5 `thresholds-availability.yaml` and `thresholds-security.yaml`
- Same shape as the performance file: an internal target block and an `sla` block, each with `class`.
- Availability, 1.0: contract 99.95%, internal 100%, maintenance window excluded (`sp5-framework/concepts/sla-metrics`).

## 9. How Agent E2 answers a threshold question (target)

Example: "Is 6% CPU Ready bad?" with a VCF Operations screenshot of a VM.

| Step | What Agent E2 does | Where it happens |
|---|---|---|
| 1 | Maps the words: "CPU Ready" gives the readings `vm.cpu.ready.*` and their files | Term map (Harness) |
| 2 | Reads the screenshot: label "Peak vCPU Ready", value 6.1, object VM, chart "Last 6 hours". Shows back what it read | LLM |
| 3 | Resolves the label to `vm.cpu.ready.vcpu-max.peak20s` through `names` | Catalog (Harness) |
| 4 | Looks up all uses of that reading and the readings it dominates, and places 6.1 in each | Catalog (Harness) |
| 5 | Receives the result (below): verdict per use, why, what the verdict depends on | Tool result |
| 6 | Nothing is missing (the name says peak and worst vCPU), so no question. Writes the answer: KPI orange, why, next check (Co-stop, vCPU count, host contention) | LLM |
| 7 | Checks that every threshold number in the answer matches a returned row | Verifier (Harness) |

Lookup result, about 120 tokens (the `why` text is illustrative until the files carry it):
```text
Reading: vm.cpu.ready.vcpu-max.peak20s (Peak CPU Ready among any vCPU, VM, 20-second peak). Value 6.1 %.
- KPI (proactive, no deadline): ORANGE. Edges yellow 2, orange 4, red 8. Why: one waiting vCPU stalls a multi-threaded job. [vsphere/object-types/vm/kpis/vm-performance]
- SLI: not comparable. The SLI reads vm.cpu.ready.total.avg5m (VM total, 5-minute). Fail above 2.5. [sp5-framework/concepts/sla-metrics]
- Alert: not comparable. Alerts read vm.cpu.ready.total.avg5m: orange above 4, red above 8, with gates. [vsphere/technology/cpu/configuration/cpu-alerts]
Values: recommended (Agent E2). Depends on: nothing missing.
```

If the screenshot had shown "CPU Ready, 6%" without "Peak":
```text
Depends on: interval and instance. 20-second peak of the worst vCPU: KPI orange. 5-minute VM total: SLI fail; alert orange if it lasts.
Hint: VCF Operations names the 20-second metric "Peak". The vSphere Client real-time chart is 20 seconds; "Past day" is 5 minutes.
```
Agent E2 then infers from the chart, answers both branches, or asks (section 10).

## 10. When Agent E2 asks

A question rarely gives all six parts of a threshold, and the customer's VCF Operations may use its own thresholds. Agent E2 must not guess.

### 10.1 Today
- One round, up to 3 questions, then it answers. Triggers: an odd question, text and attachment that disagree, one missing fact (object, layer, interval, version) that changes the answer. It never asks what an attachment already answers; otherwise it states its assumption first.
- Gaps: instance, use, class and the customer's own setting are not triggers (G8); the decision to ask is the LLM's judgment; answers do not carry to the next question; the benchmark is single turn, so asking is not measured.

### 10.2 Target
- The lookup states what the verdict depends on (section 9). That is exact, not a judgment.
- Then Agent E2:
  1. infers the part from the attachment with the reading's `hints` (chart title, metric name, breadcrumb);
  2. answers both branches when they are at most two and lead to the same next step;
  3. otherwise asks, with the reason ("because the 20-second peak and the 5-minute average have different thresholds").
- New triggers in the clarifying rule: instance, use, class of service, the customer's own setting.
- Recommended vs configured: every threshold in an answer is labelled "recommended (Agent E2)" or "configured (your VCF Operations)". For a question about the user's own alert or policy, Agent E2 asks for the alert definition (symptoms, thresholds, wait and cancel cycles), or answers with the recommended set and says so. At 1.2 the shipped VCF Operations alert definitions are in the catalog, so a default alert is recognised by name.
- Class of service: asked once when it changes the answer; all classes shown when there are three or fewer rows.
- Answers given (class, interval, configured thresholds) carry to later questions in the same conversation.

## 11. What Agent E2 always knows

- An up-front prompt block, about 200 tokens, generated from the `uses` sentences of the files (as `harness/primer.py` generates its blocks), states the frame before any lookup:
  - the uses and their question, time span, spike filter, deadline;
  - a threshold applies to one reading: object, metric, instance, interval;
  - KPI colour means how bad; alert colour means by when; yellow is never an alert;
  - capacity has no alerts; alerts are intra-day;
  - every number comes from a lookup; recommended and configured are labelled.
- Each lookup result carries the `why` sentence and the knowledge file. Agent E2 reads the file when the question asks why (U9) or when it judges a customer's own threshold (U5).

## 12. Target implementation

| Part | Today | Target |
|---|---|---|
| `knowledge/catalog/` | 2 threshold files, joined by name | 6 files (section 8), joined by reading key |
| Catalog load (`harness/catalog.py`) | Tables `thresholds`, `bands`, `levels` | Tables `readings`, `reading_names`, `kpi_edges`, `tests` (sli, rule, symptom), `targets` (sla, kai, kci), `models`, `model_inputs`, `decisions`, `alerts`, `alert_symptoms` |
| Name to reading | Fuzzy score on English names | Exact match on `names` and external keys first; fuzzy only as fallback, marked as a guess |
| Lookup | Returns rows | Extends the existing `catalog` tool with `value`, `use`, `class`: returns the verdict per use, `why`, "not comparable" for other readings, "depends on" for missing parts. One tool, not a new one: each tool costs prompt tokens and choice errors for a 32B LLM |
| Comparison | By the LLM | In the catalog: edges, direction, the boundary rule, dominance |
| Alert timing | Free text | Computed: time to fire and to clear from wait and cancel cycles |
| Classic mode (`Catalog.facts_for`) | Counters and rules of the files in context | Results of section 9 for every reading of the files in context, bands included |
| Term map (`user-terms.yaml`) | Files | Files and reading keys, so the lookup starts before the LLM asks |
| Up-front block (`harness/primer.py`) | Tool advice | The threshold frame of section 11 |
| Clarifying rule (`harness/clarify.py`) | Object, layer, interval, version | Adds instance, use, class, the customer's own setting; reads "depends on" |
| Verifier (`harness/verify.py`) | Soft check on numbers in the reason line | Every number with a unit in the whole answer checked against the returned rows; a threshold not returned triggers the repair turn after the benchmark shows it helps |
| Lint (`project/tools/lint.py`) | Fields, quotes, bands vs Markdown, `levels` vs bands | Plus: `use` and `reading` on every row; reading exists; edges monotonic; ids unique; no yellow alert; no capacity alert; rules C1 and C6; Markdown band tables vs edges |
| Tools | `levels_csv.py`, `threshold_inventory.py` | Both on the new files; a migration script from the 2 files to the 6 |
| Tests (`harness/test_tools.py`) | Lookups return sourced rows | Verdicts per use, not-comparable cases, depends-on cases, alert timing, dominance |

## 13. Alternatives considered

| Option | Pros | Cons | Verdict |
|---|---|---|---|
| A. One file for all thresholds | One join for U9 | 2,000+ lines; review hard | No |
| B. One file per pillar plus alerts | Matches the `pillar` tag and the SP5 model; KPI and SLA of a reading together | Alerts span pillars; two shapes per file | Yes, with `use` and `reading` on every row |
| C. One file per use | Matches the scoring | KPI and SLA of one reading in two files | No: `use` as a field gives the same query |
| D. External key (VCF Operations or vCenter) | No mapping file | Neither covers esxtop, book metrics and derived metrics; renames break rows | No: own key plus mapping |
| E. Full alert definitions now | U4 complete | 1,193 definitions wait on the overhaul (1.2) | Thin block now, full catalog at 1.2 |
| F. A separate threshold tool | Clear purpose | One more tool for a 32B LLM to choose | No: extend `catalog` |

## 14. Work list

### 14.1 1.0, in order
1. Answers to Q153-Q158.
2. `readings.yaml` for every reading that has a threshold today.
3. Migration script: the 2 files to the performance, capacity and alerts files; lint; retrieval check before and after.
4. Catalog tables, lookup with verdicts, `catalog` tool arguments, classic facts, unit tests.
5. Up-front block, clarifying triggers, verifier check.
6. `thresholds-availability.yaml` with its two rows.
7. `KNOWLEDGE-ENGINEERING.md`, section 9, and the glossary (symptom definition vs symptom).
8. Benchmark: questions for U4, U5, U9, and a clarifying set (asked when it should, did not ask when it should not).

### 14.2 Open to contributors
- `thresholds-availability.yaml`: availability SLA and internal target per class; source: the vCommunity adapter's Operational Availability page.
- `thresholds-security.yaml`: compliance and security targets and SLA; "is it secure?" covers security and compliance.
- `readings.yaml`: VCF Operations keys from the 9.1 metric reference; vCenter and esxtop columns from `vcenter-counters.yaml` and `esxtop-fields.yaml`.
- Alert symptoms for configuration, compliance and inventory.

### 14.3 After 1.0
- Capacity: Agent E2 recomputes Cluster Consumption, Cluster Risk and Close for Business from their inputs, for what-if questions and for clusters without the vCommunity pack.
- Full alert definition catalog from the overhaul (1.2), referencing symptom ids.
- Live VCF Operations: configured thresholds and alert definitions read directly; U1 on live data.

## 15. Risks

- Ten `use` values is the upper limit for a 32B LLM to keep apart; every result names its use.
- Migration touches 4 SLI rows, 31 band rows, 31 `levels` lines and 73 rule quotes: by script, then lint.
- Symptom has two meanings (Q154): the VCF Operations symptom definition (a test) and the SP5 symptom (a minor issue for the daily check).
- Most VCF Operations keys are unknown; until filled, screen names map to keys through `names`.
- The catalog is not chunked, so retrieval should not move; the retrieval check runs before and after anyway.

## Sources
- Broadcom TechDocs, VCF 9.0: [Alert Definition Best Practices](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-0/infrastructure-operations/configuring-alerts-and-actions/defining-alerts-best-practices.html).
- Broadcom TechDocs, VCF 9.1: [Add a Virtual Machine CPU Usage Symptom to the Alert Definition](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/configuring-alerts-and-actions/create-a-problem-alert-definition/add-a-virtual-machine-cpu-usage-symptom-to-the-alert-definition.html).
- Knowledge base: `sp5-framework/performance/kpi-vs-sla`, `sp5-framework/alerts/alert-design`, `sp5-framework/alerts/alerts-and-insights`, `vcf-operations/alerts/alert-definitions`, the cluster models, `close-for-business`, `observability/thresholds`.
- Harness: `harness/catalog.py`, `harness/agent.py`, `harness/modes.py`, `harness/primer.py`, `harness/clarify.py`, `harness/verify.py`, `project/tools/lint.py`.
