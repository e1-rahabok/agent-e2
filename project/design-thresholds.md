# Thresholds in Agent E2: design and implementation

Status: design, with Q152-Q158 answered (2026-11-10). Built: one copy of the KPI levels (2026-11-10); sections named by use and alerts in their own file (2026-11-11) (section 3). Section 3 describes what is built; sections 4-14 the target; section 15 the work.
Not indexed.

2026-11-11: the performance SLA and the SLI are removed from operations (author: the SLA is a business contract; the KPI is enough). The `sla` and `sli` sections of `thresholds-performance.yaml` and their 7 rows are gone; the Harness, lint and tests no longer know the uses. Rows and sections below that still show `sla` or `sli` for performance are the earlier design, kept for the record; the availability and security SLA (contract) rows of the future files stay.

## 1. Goal

- Agent E2 knows every threshold it needs, applies the right one to the reading in front of it, explains why that number sits there, and never mixes the uses.
- Agent E2 is one program: a 32B LLM, the Harness and the Agent loop working together. This document says what Agent E2 does. It names a part (LLM, Harness, catalog, verifier) only where the design depends on where the work happens.

## 2. Domain premises

- Performance and capacity ask different questions over different time spans, so the same metric has different thresholds.
- Alerts are for the intra-day timeline: performance, availability, configuration, compliance, security, inventory (for example too many large VMs on one host).
- Capacity principle: capacity management takes the long view, weeks and months, so done properly it raises no alert. A capacity alert means something is amiss: a software bug, or a hardware availability issue that took capacity away.
- Alert and KPI are independent: different purpose, set separately. KPI is proactive, an internal target; an alert is reactive, a guard rail when people ignore the KPI, and fires when the issue has become urgent.
- An alert has a dimension the KPI does not have: wait cycle and cancel cycle. They remove one-off spikes and flapping.
- Performance has one use, the KPI (internal baseline). No performance SLA or SLI (2026-11-11). Alerts read the KPI metrics with their own values.
- KPI is performance only: the P is performance. Availability has KAI (key availability indicator); security, compliance included, has KSI (key security indicator). Users say availability KPI or business KPI in daily speech; Agent E2 translates by the pillar measured (term map row `kpi-other-pillar`).
- Symptom and condition are one thing in VCF Operations: a test on a metric, property or event. A symptom definition is reusable across alert definitions; a condition is written inside one.

## 3. As built today

### 3.1 Files
| File | Content |
|---|---|
| [`knowledge/catalog/thresholds-performance.yaml`](../knowledge/catalog/thresholds-performance.yaml) | `kpi`: 31 lines (2026-11-11: `sla` and `sli` removed), green, yellow, orange, red, zero for 5m, 20s and 2s (2026-11-12: green and zero added), entered by hand, with `group`, `kb`, `excluded_when_green` (2026-11-10: one place; 20 rows that served no use case went back to prose; 2 capacity rows moved) |
| [`knowledge/catalog/thresholds-capacity.yaml`](../knowledge/catalog/thresholds-capacity.yaml) | `models`: 18 rows with a grey (wastage) band. `decisions`: 6 close-for-business rows. `rules`: 12 planning and sizing rows (2026-11-10: 7 vendor and default rows went back to prose) |
| [`knowledge/catalog/thresholds-alerts.yaml`](../knowledge/catalog/thresholds-alerts.yaml) | `symptoms`: 40, one test each; `alerts`: 33 definitions, one object type each (2026-11-12; were 24 with object lists, and before that 20 rows with a free-text `condition`), each with `criticality`, `pillar`, `match`, symptom `sets` (self or children with a population) and `wait_cycles` |
| Knowledge files | No colour-band table: the file holds the reasons; Agent E2 shows the catalog values with it. Alert files hold no values (2026-11-12): one file per object type, each alert explained under a heading with its catalog name. Capacity flow steps still carry their numbers (marked by `quote` in the row) until they move |

- The section name is the use (2026-11-11): rows carry no `kind` or `use` field; the Harness stores the use as a column and puts it first in every result.
- Alert rows hold the main test, with the other tests and the wait time inside the `condition` text ("for 15 minutes"). Splitting them into symptoms is still to do (section 8.4).
- Rows are joined by the metric's English name; no key.

### 3.2 How Agent E2 uses them
1. Start-up: [`harness/catalog.py`](../harness/catalog.py) loads the three files into an in-memory SQLite catalog: tables `thresholds` (one-value tests with `use`: alert, decision, rule; plus `criticality`, `class`, `pillar`, `interval`, `instance`), `kpi`, and `bands` (capacity model rows).
2. Term map ([`harness/terms.py`](../harness/terms.py), [`knowledge/catalog/user-terms.yaml`](../knowledge/catalog/user-terms.yaml)): the user's words pull the metric's knowledge files into the context. No threshold is fetched here.
3. Agent E2's reading set: `Catalog.facts_for(ids)` adds up to 20 "Catalog facts (exact)" lines for the files in the reading set: counters, rule rows, and the KPI levels of a KPI file (all three intervals, "no value" where empty).
4. The agent's code calls `Catalog.lookup` with each metric name of the case (harness/AGENT.md, stage 1; the model calls no tool since 2026-11-14). It scores every counter, esxtop field, metric file and threshold row against the name (word overlap, `_score`) and returns the 8 best of each, with the KPI levels of each matched band.
5. The LLM reads the rows, picks one, compares the value itself and writes the answer.
6. Prompt rules ([`harness/modes.py`](../harness/modes.py), [`harness/primer.py`](../harness/primer.py)): "Quote a threshold only when the knowledge base states it"; "For a threshold, call catalog. Its values are exact."
7. Verifier ([`harness/verify.py`](../harness/verify.py)): a number with a unit in the reason line that is not in the question or the context is recorded as "ungrounded" in the trace. Soft: it does not trigger a repair.
8. Clarifying ([`harness/clarify.py`](../harness/clarify.py), shipped conversation only): one round of up to 3 questions when the question is odd, the text and an attachment disagree, or one missing fact (object, layer, interval, version) changes the answer.
9. Quality checks: lint checks every catalog row (parses, fields, allowed values), a `quote` where one remains, and that no knowledge file carries a colour-band table. [`harness/test_tools.py`](../harness/test_tools.py) checks that lookups and the reading set show the catalog values.

### 3.3 Gaps in what is built
| # | Gap | Effect on an answer |
|---|---|---|
| G1 | Lookup by fuzzy name | "Ready" returns VM, ESXi and cluster rows mixed; the LLM picks |
| G2 | Fixed 2026-11-11: results and reading-set facts carry `interval` and `instance` where a row has them | - |
| G3 | Fixed 2026-11-11: every value is labelled with its use ("Alert, red: VM CPU Ready > 8", "Capacity decision: ...") | - |
| G4 | The LLM compares the value | Errors on ranges, open ends and lower-is-worse metrics |
| G5 | Fixed 2026-11-10: lookups and reading-set facts return the KPI levels (`kpi`) | - |
| G6 | Fixed 2026-11-10: reading-set facts include the KPI levels of a KPI file in the context | - |
| G7 | Wait cycles are free text inside `condition` | Agent E2 cannot compute when an alert fires or clears |
| G8 | No signal that the answer depends on a missing fact | Asking is left to the LLM's judgment |
| G9 | Ungrounded-number check is soft and reason-line only | A wrong threshold in the answer body passes |
| G10 | Fixed 2026-11-10: `kpi` is the one catalog copy; the Markdown table stays for retrieval, checked by lint | - |

## 4. Use cases

| # | Use case | Example | Time span | Files | Release |
|---|---|---|---|---|---|
| U1 | Daily health check over many objects | Score every KPI and model; list objects in orange and red | Last 24 hours | performance, capacity, availability | Needs data: exports (1.2) or live VCF Operations (after 1.0) |
| U2 | Troubleshooting a complaint | "Users say VM X is slow since 10:00" | Minutes to hours | performance (KPI) | 1.0 |
| U3 | Read a screenshot | "Is 6% Ready bad?" with a chart | One reading | performance, capacity | 1.0 |
| U4 | Explain an alert | "Why did this alert fire? Is it real?" | One alert | alerts, performance | 1.0 |
| U5 | Review alert design | "We get 500 alerts a day"; "Is 4% Ready a good alert threshold?" | Design | alerts, performance | 1.0 |
| U6 | "Our SLA" claim | "Did Gold VMs meet the SLA in October?"; "Our SLA is Cluster Availability" | Concept | none: probe the metric and object; performance reads the KPI | 1.0 |
| U7 | Capacity decision | "Can this cluster take 20 more VMs?"; close for business | 24 hours to months | capacity, performance (KPI as input) | 1.0 |
| U8 | Rightsizing and reclamation | "Which VMs are oversized?" | 30 days or more | capacity (grey band, sizing bands) | 1.0 |
| U9 | Explain a threshold | "Why is Ready 2 in the KPI and 8 in the alert?" | Concept | all files, one reading across uses | 1.0 |
| U10 | Policy setting | "What do I set in the VCF Operations policy?" | Design | the file of the use asked | 1.0 |
| U11 | Availability SLA | "Did we meet 99.95%?" | Calendar month | availability | After 1.0 |
| U12 | Security and compliance | "How compliant is the cluster?" | Daily | security | After 1.0 |

- U2, U3 and U9 are the 1.0 core.
- In U1, raw metrics never pass through the LLM: Agent E2 scores them in the Harness, and the LLM reads only the findings ([`ARCHITECTURE.md`](../ARCHITECTURE.md), section No fast first-stage model).
- Troubleshooting has no thresholds of its own. It reads the KPI levels at the interval of the reading: 20s for the VCF Operations peak and the vSphere Client real-time chart, 2s for esxtop. Each interval has its own yellow, orange, red, entered by hand.

## 5. Why the same metric has different thresholds

Each use has its own time span, spike filter and cost of a wrong call.

| Use | Question | Reading | Spike filter | Deadline | Cost of a false positive | Cost of a false negative |
|---|---|---|---|---|---|---|
| KPI | Is it performing now? | 20-second peak and 5-minute average, rolling window | None: the peak is wanted | None | A line read in the daily check | VMs suffer unseen until a complaint |
| Alert | Must someone act today? | 5-minute average, often with a 20s peak condition | Wait cycle, cancel cycle | Red 1-2 hours; orange end of day | Alert fatigue; real alerts ignored | Outage or slowness with no one acting |
| Capacity | Is there room for weeks to months? | 95th percentile over 24 hours; monthly trend | Percentile: the worst 5% ignored | Weeks | Hardware bought early | Contention for months; long lead time |

- ESXi CPU thread utilization: Cluster Consumption red from 85% (cluster-wide, p95 of 24 h); Cluster Risk red from 90% (worst host); alert above 40% thread with core utilization above 80% for 10 minutes (one host).
- VM CPU Ready: KPI on the worst vCPU at 20s (yellow 2, orange 4, red 8); alert on the VM total at 5m (orange above 4%, red above 8%) with peak vCPU Ready, contention and a usage gate.
- A threshold therefore has six parts:

```text
threshold   = (use, reading key, class of service) -> values, spike filter, source
reading key = (object, metric, instance, interval or window statistic)
```

## 6. KPI and alert: independent

- KPI and alert have different purposes and are set separately. Neither is derived from the other, and lint does not link their numbers.
  - KPI: proactive, an internal target, read in the daily health check; colour means how bad, with no deadline.
  - Alert: reactive, a guard rail when people ignore the KPI; colour means by when (red 1-2 hours, orange end of day). Its spike filter is the wait cycle and cancel cycle (section 9), which the KPI does not have.
- Reading them together still needs two rules about readings, used when Agent E2 explains why an alert fired while the KPI looks better, or the reverse:
  - peak dominates average: the 20-second peak of an interval is at least its 5-minute average;
  - worst instance dominates aggregate: the worst vCPU or virtual disk is at least the VM value ([`sp5-framework/observability/thresholds`](../knowledge/sp5-framework/observability/thresholds.md), Instance rule).
- Example: the VM KPI reads the worst vCPU at 20 seconds; the VM CPU contention alert reads the VM total at 5 minutes with a usage gate. A VM can be KPI red with no alert (short or gated bursts), and the answer says why.
- KPI colour and alert colour are never compared as if one scale.

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
- Readable slug from closed lists: `object.resource.measure.instance`. The interval is not in the key: one reading is seen at 5m, 20s and 2s, as the `kpi` columns show; a rule row names its interval.
  - `vm.cpu.ready.vcpu-max`: CPU Ready of the worst vCPU (VCF Operations "Peak CPU Ready among any vCPU" is its 20s value).
  - `vm.cpu.ready.total`: VM CPU Ready.
  - `cluster.mem.consumed.host-max`: Cluster Risk input.
- A 32B LLM copies and matches a slug more reliably than a number or a hash; the slug also shows the instance.
- Product renames change the mapping, never the key.
- Unit is not in the key: a VCF Operations % and a vCenter summation in ms are one reading; the calculator converts.

### 7.3 `knowledge/catalog/readings.yaml`
```yaml
- key: vm.cpu.ready.vcpu-max
  object: VirtualMachine
  resource: cpu
  measure: ready
  instance: worst vCPU
  unit: '%'
  names: {20s: ['Peak CPU Ready among any vCPU', 'Peak vCPU Ready'], 2s: ['%RDY (per vCPU, esxtop expanded)']}
  vcf_operations: null
  vcenter: null
  esxtop: null
  dominates: [vm.cpu.ready.total]
  same_name: [esxi.cpu.ready.total]
  hints: ['"Peak" in a VCF Operations metric name means the 20-second peak', '"among any vCPU" means the worst vCPU']
  kb: vsphere/technology/cpu/metrics/virtual-motherboard/ready
```
- Threshold rows hold only the key and the threshold; names, units and external keys live here once.
- `names` maps a screen label to a key and an interval; `hints` let Agent E2 infer instance and interval from an attachment (section 11).
- `dominates` records section 6's reading rules for explanations; `same_name` carries the existing misconception guard (same label, other object).

## 8. Threshold files

| File | Holds | 1.0 |
|---|---|---|
| `readings.yaml` | Reading keys and mapping | Yes |
| `thresholds-performance.yaml` | KPI levels (9 values per metric), SLI tests, SLA targets, performance rules | Yes |
| `thresholds-capacity.yaml` | Capacity and risk models, decisions, planning and sizing rules | Yes |
| `thresholds-alerts.yaml` | Symptoms (one test each) and alert definitions (built 2026-11-12); cancel cycles to do (section 9) | Yes |
| `thresholds-availability.yaml` | KAI (internal target) and SLA (contract) | Two rows (99.95%, 100%); rest open to contributors |
| `thresholds-security.yaml` | KSI (security and compliance internal target) and SLA | Open to contributors |

### 8.1 Common fields
| Field | Values | Why |
|---|---|---|
| `id` | unique across all files | Reference from other files and from questions |
| `use` | kpi, sli, sla, kai, ksi, model, decision, rule, symptom, alert | First filter of every lookup. Not a row field: the section name is the use (built 2026-11-11), so it cannot disagree with where the row sits |
| `reading` | key from `readings.yaml` | The join across files and uses |
| `direction` | above, below | Lower is worse for free memory, KPI scores, SLA |
| `interval` or `window` + `statistic` | 2s, 20s, 5m; 24h p95; calendar month mean | What the number applies to; KPI rows carry all three intervals as `kpi` columns |
| `class` | all, gold, silver, bronze, production, non-production | Thresholds per class of service |
| `source` | `knowledge-base`, or a vendor document with its version | Which source wins: version-bound vendor facts can go stale |
| `kb`, `quote` | knowledge file id; sentence copied from it | Citation; lint keeps the number tied to its text |

### 8.2 `thresholds-performance.yaml`
```yaml
meta:
  sections:      # what each use means, for the author; the Harness labels values by section
    kpi: 'Proactive. Is it performing now? Rolling window, 20-second accuracy, no deadline. Yellow is read in the daily check.'
    sli: 'Pass or fail of one 5-minute interval against the contract.'
    sla: 'Monthly mean of SLI passes, per class of service. Lagging.'
kpi:             # the one copy (built 2026-11-10, renamed from levels 2026-11-11, without reading keys yet)
- {object: VirtualMachine, metric: "Peak CPU Ready among any vCPU (%)", direction: above, 5m: null, 20s: [2, 4, 8], 2s: null}
# target: reading: vm.cpu.ready.vcpu-max replaces object and metric
sli:
- id: vm-sli-cpu-ready
  reading: vm.cpu.ready.total
  direction: above
  fail: 2.5
  class: all
  kb: sp5-framework/concepts/sla-metrics
  quote: '| CPU | Ready | above 2.5% |'
sla:
- id: performance-sla-gold
  reading: vm.performance.sla.total
  direction: below
  fail: 99.9
  class: gold
  kb: sp5-framework/performance/noisy-neighbour
  quote: 'Performance SLA thresholds: Gold 99.9%, Silver 99.8%, Bronze 99.6%.'
rules: []
```
- Fifteen values per metric (nine until 2026-11-12): green, yellow, orange, red, zero for 5m, 20s and 2s, entered by hand; the 4x rule is a guide for choosing a 20-second value from a 5-minute one (a spike rarely lasts 300 seconds), not a formula: it never fills a cell.
- The green start and the red end stay in the KPI file's Markdown table; Agent E2 reads the published score in 1.0 and does not recompute it.
- The why comes from the KPI file, which the lookup names.
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
    reading: cluster.cpu.thread-utilization.total
    direction: above
    edges: [0, 55, 70, 85, 100]
    grey: null                       # wastage; Q110
    excluded_when_green: false
- id: cluster-risk
  use: model
  inputs:
  - id: cluster-risk-highest-memory-consumed
    group: utilization
    reading: cluster.mem.consumed.host-max
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
- 1.0: Agent E2 reads the published scores; the parameters serve explanation. Recomputing is after 1.0 (section 15.3).

### 8.4 `thresholds-alerts.yaml`
Built 2026-11-12. As built, it differs from the proposal below in three points:
- Wait cycles are on the alert (`wait_cycles`), as the knowledge files state them ("for 15 minutes, all of"). A shared symptom (VM CPU Usage above 1 GHz, in 10 alerts) is used with different waits; on the symptom it would need one copy per wait. Broadcom's advice (delay on the symptom) stays a review note.
- Symptom sets: `sets`, each with `relation` (self, or child with `object` and `population`), `match` and `symptoms`; the alert's `match` combines the sets. Covers "cluster when more than 25% of hosts". The key is not `on`: YAML reads `on` as true.
- No `type`, `reading`, `class`, `persona` or cancel cycles yet: no row needs them, and section 9 is not approved.
- Fixes found during the migration: VM disk latency is four alerts (read and write separate, as storage-alerts says), not two; infrastructure contention alerts are on ESXi, resource pool and cluster, not on the cluster only; the 3 capacity alerts carry their population.
- Lint: every symptom used, every reference exists, a symptom is defined on the alert's object, no two symptoms with the same test, no `condition` anywhere.
- Restructured 2026-11-12 (author: an alert fires on one object type, not on a technology): one alert definition per object type (the infrastructure contention rows split into ESXi, resource pool and cluster; ESXi dropped packets into virtual and physical network, as the source counts 2). Alert `kb` is the object type's alert file (`vsphere/object-types/<object>/<object>-alerts`, [`guest-os/guest-os-alerts`](../knowledge/guest-os/guest-os-alerts.md); one file per VCF Operations object type, no `alerts/` folder), which explains each alert under a `##` heading carrying its `name`; a symptom's `kb` is the file of the metric it tests. No `quote`: the alert files hold no values, and lint rejects a value in an alert's section or a misconception's correction. The harness shows an alert with its own file only (not with every metric file it tests). CPU contention on ESXi, resource pool and cluster now reads a share of the member VMs (child VirtualMachine, > 25%), as the source states; memory contention the same since Q145 (c). VM CPU contention without the Contention symptom and orange halved (Q144); VM dropped packets gated by VM CPU Usage (Q147).

Proposal (2026-11-10):
```yaml
cycle: 5m        # VCF Operations collection cycle: wait 3 = 15 minutes
symptoms:
- id: sym-vm-cpu-ready-above-8
  pillar: performance
  type: metric                      # metric, property, event
  role: issue                       # issue or gate
  reading: vm.cpu.ready.total
  operator: '>'
  value: 8
  wait_cycles: 1
  cancel_cycles: 3                  # contention: section 9
  class: all
  kb: vsphere/technology/cpu/configuration/cpu-alerts
  quote: VM CPU Ready above 8%;
- id: sym-vm-cpu-usage-above-1ghz
  role: gate                        # not a problem: keeps contention alerts off idle VMs
- id: sym-host-monster-vm-count-above-n
  pillar: inventory
  type: property
alerts:          # to do (section 15): without it, "why did this alert fire" cannot be answered
- id: alert-vm-cpu-contention-red
  criticality: red                  # VCF Operations Critical; orange is Immediate; no yellow
  match: all
  symptoms: [sym-vm-cpu-ready-above-8, sym-vm-peak-vcpu-ready-above-32, sym-vm-cpu-contention-above-8, sym-vm-cpu-usage-above-1ghz]
  wait_cycles: 1
  cancel_cycles: 1
  persona: infrastructure
```
- Pillars: performance (contention, consumption), availability, configuration, compliance, security, inventory, and capacity under the principle of section 2: a capacity alert means a bug or a hardware availability issue.
- Symptom types: metric (a reading against a value), property (a setting or a count), event (a fault or message). Wait and cancel cycles apply to metric and property symptoms.
- One reading can be a capacity input and an alert symptom: monster VM concentration is a Cluster Risk input (daily planning) and an inventory alert (a placement that cannot wait).
- Wait and cancel cycles (Broadcom TechDocs, Alert Definition Best Practices):
  - counted in collection cycles, 5 minutes by default. Wait n: true n cycles in a row before the symptom triggers. Cancel m: false m cycles in a row before it clears;
  - the alert definition has its own cycles, applied after the symptom triggers; Broadcom advises the delay in the symptom and alert-level cycles at 1;
  - time to fire about n × 5 minutes; time to clear about m × 5 minutes.
- The wait cycle filters across cycles (persistence). A 20-second peak puts spike sensitivity back inside one cycle: a peak symptom with wait 1 fires on one 20-second burst. The alerts pair a peak symptom with a 5-minute average symptom under `all`.
- Cancel cycles: section 9.
- The three alert rows now in the capacity file move here with the other alerts; they keep their pillar.

### 8.5 `thresholds-availability.yaml` and `thresholds-security.yaml`
- Same shape as the performance file: a `kai` (availability) or `ksi` (security) block for the internal target and an `sla` block for the contract, each with `class`.
- Availability, 1.0: contract 99.95%, internal 100%, maintenance window excluded ([`sp5-framework/concepts/sla-metrics`](../knowledge/sp5-framework/concepts/sla-metrics.md)).

## 9. Alert cancel cycle

Proposal. Values are design values for the recommended alert set, to tune from each site's alert history; they are not knowledge-base thresholds.

### 9.1 Three states, kept apart
| State | Owner | Question | Set by |
|---|---|---|---|
| Symptom or condition | VCF Operations | Is the test true now? | Wait cycle and cancel cycle on the symptom or condition |
| Alert | VCF Operations | Is the issue still urgent? | The symptom set (all or any); alert-level cycles at 1 |
| Incident | Event engine or ITSM (ServiceNow and the like) | Has a person dealt with it? | People and the event engine, never the metric |

- The cancel cycle belongs to the symptom or condition. Its only job: stop the alert flapping open and closed while the metric hovers near the threshold.
- It is not a cooldown to keep an alert visible, and not the incident's closure. Closing a ticket is a human or event-engine decision.

### 9.2 Why VCF Operations needs a cancel cycle above 1
- A VCF Operations symptom or condition has one threshold: no separate clear threshold (state hysteresis). The cancel cycle is the only hysteresis it offers, in time instead of in value. Check against the VCF Operations 9.1 symptom definition page.
- Contention metrics are bursty. An episode that lasts an hour often dips below the threshold for one 5-minute cycle. With cancel 1, it becomes several alerts, each with its own notification: an alert storm made of one problem.
- While an alert is open, VCF Operations does not raise it again for the same object. A long cancel cycle therefore hides a new episode behind an old alert: the suppression trap. That sets the upper limit.

### 9.3 Rules
- R1. Cancel cycles live on symptoms or conditions (a condition has its own waitCycles, cancelCycles and severity: VCF Operations API 9.1.1, alert-condition); alert-level wait and cancel cycles stay at 1 (Broadcom advice). Build an alert's tests as conditions (Q143).
- R2. By symptom type:

| Symptom type | Behaviour | Cancel cycles | Time to clear |
|---|---|---|---|
| Contention metric (Ready, Co-stop, memory contention, disk latency, dropped packets) | Bursty, oscillates around the threshold | 3 | about 15 minutes |
| Consumption metric (Net Run, utilization, consumed memory, datastore space) | Moves slowly; a drop is real | 1-2 | 5-10 minutes |
| 20-second peak symptom paired with a 5-minute one | The most volatile member of its set | At least the cancel of its 5-minute partner | - |
| Gate (usage above 1 GHz) | Severe contention can push usage down | At least the cancel of the issue symptoms | - |
| Property (setting, version, count) | Changes only by a change | 1 | one cycle |
| Event or fault | Cleared by a matching event, or by a person | Per fault definition; never by time alone | - |

- R3. Under `all`, the alert lives as long as its shortest-living symptom: give the most volatile member the longest cancel. Under `any`, the alert lives as long as its longest-living symptom: keep every cancel short.
- R4. Upper limit: wait + cancel of a red alert must fit well inside its 1-2 hour deadline, and cancel never above 3 cycles (15 minutes), so the suppression trap stays short.
- R5. The gate case: severe CPU contention can lower CPU usage below the 1 GHz gate, so the gate turns false exactly when the VM is worst. A longer gate cancel keeps the alert open through it. Better still, gate on demand rather than usage (to check).
- R6. Red and orange on one metric are separate alert definitions. When red clears and orange still holds, the orange alert stays; the cancel cycle of the red symptom does not hold red for orange's sake.

### 9.4 Incident layer
- Red (urgent and important, pushed to the phone): the alert cancelling does not close the ticket. The ticket records the recovery; a person closes it with the cause. This matches the misconception in [`sp5-framework/outputs/alerts-and-insights`](../knowledge/sp5-framework/outputs/alerts-and-insights.md): alerts that close themselves breed "no open alert means no problem".
- Orange (urgent, not important): the ticket may close with the alert, with the recovery recorded; the end-of-day review reads the closed ones.
- Re-trigger within a debounce window (proposal: 30 minutes) appends to the open ticket and sends no new page.
- Two topologies:
  - with an event engine: debounce there; symptom cancel cycles can stay at the low end of R2;
  - VCF Operations sending straight to email or ITSM: the cancel cycle is the only debounce; use the values of R2 as they are.

### 9.5 Review of [`project/sources/alert_close_cycle_design_best_practices.md`](sources/alert_close_cycle_design_best_practices.md)
| Point in the note | Verdict | Reason |
|---|---|---|
| Separate telemetry, event and ITSM states | Agree | Section 9.1 |
| Hysteresis by value (trigger 20 ms, clear 10 ms) | Agree in principle; not available in a VCF Operations symptom | One threshold per symptom; the cancel cycle is the hysteresis there |
| Cancel immediately, no time-based delay | Disagree for VCF Operations | Without an event engine, cancel 1 turns one bursty episode into many alerts and notifications; the cancel cycle is count-based hysteresis, not a cooldown |
| Debounce in the event engine | Agree where one exists | Many VCF sites have none; then the cancel cycle does it |
| Human-gated closure for critical | Agree | Section 9.4, red |
| Auto-close for low priority performance and capacity alerts routed to daily dashboards | Disagree | A daily-dashboard item is not an alert: yellow is not an alert. Capacity raises no alert when managed properly (section 2) |

### 9.6 What Agent E2 does with it
- Computes when an alert fires and clears: wait × 5 minutes, cancel × 5 minutes, per symptom, under `all` or `any` (R3).
- Explains an alert that fires, clears and fires again as cancel-cycle flapping, and proposes the cancel value of R2.
- Reviews a customer's alert definition against R1-R6.

## 10. How Agent E2 answers a threshold question (target)

Example: "Is 6% CPU Ready bad?" with a VCF Operations screenshot of a VM.

| Step | What Agent E2 does | Where it happens |
|---|---|---|
| 1 | Maps the words: "CPU Ready" gives the readings `vm.cpu.ready.*` and their files | Term map (Harness) |
| 2 | Reads the screenshot: label "Peak vCPU Ready", value 6.1, object VM, chart "Last 6 hours". Shows back what it read | LLM |
| 3 | Resolves the label to `vm.cpu.ready.vcpu-max` through `names` | Catalog (Harness) |
| 4 | Looks up all uses of that reading and the readings it dominates, and places 6.1 in each | Catalog (Harness) |
| 5 | Receives the result (below): verdict per use, why, what the verdict depends on | Tool result |
| 6 | Nothing is missing (the name says peak and worst vCPU), so no question. Writes the answer: KPI orange, why, next check (Co-stop, vCPU count, host contention) | LLM |
| 7 | Checks that every threshold number in the answer matches a returned row | Verifier (Harness) |

Lookup result, about 120 tokens (the `why` text is illustrative until the files carry it):
```text
Reading: vm.cpu.ready.vcpu-max (Peak CPU Ready among any vCPU, VM, 20-second peak). Value 6.1 %.
- KPI (proactive, no deadline): ORANGE. Edges yellow 2, orange 4, red 8. Why: one waiting vCPU stalls a multi-threaded job. [vsphere/object-types/vm/vm-performance]
- SLI: not comparable. The SLI reads vm.cpu.ready.total (VM total, 5-minute). Fail above 2.5. [sp5-framework/concepts/sla-metrics]
- Alert: not comparable. Alerts read vm.cpu.ready.total: orange above 4, red above 8, with gates. [vsphere/object-types/vm/vm-alerts]
Values: recommended (Agent E2). Depends on: nothing missing.
```

If the screenshot had shown "CPU Ready, 6%" without "Peak":
```text
Depends on: interval and instance. 20-second peak of the worst vCPU: KPI orange. 5-minute VM total: SLI fail; alert orange if it lasts.
Hint: VCF Operations names the 20-second metric "Peak". The vSphere Client real-time chart is 20 seconds; "Past day" is 5 minutes.
```
Agent E2 then infers from the chart, answers both branches, or asks (section 11).

## 11. When Agent E2 asks

A question rarely gives all six parts of a threshold, and the customer's VCF Operations may use its own thresholds. Agent E2 must not guess.

### 11.1 Today
- One round, up to 3 questions, then it answers. Triggers: an odd question, text and attachment that disagree, one missing fact (object, layer, interval, version) that changes the answer. It never asks what an attachment already answers; otherwise it states its assumption first.
- Gaps: instance, use, class and the customer's own setting are not triggers (G8); the decision to ask is the LLM's judgment; answers do not carry to the next question; the benchmark is single turn, so asking is not measured.

### 11.2 Target
- The lookup states what the verdict depends on (section 10). That is exact, not a judgment.
- Then Agent E2:
  1. infers the part from the attachment with the reading's `hints` (chart title, metric name, breadcrumb);
  2. answers both branches when they are at most two and lead to the same next step;
  3. otherwise asks, with the reason ("because the 20-second peak and the 5-minute average have different thresholds").
- New triggers in the clarifying rule: instance, use, class of service, the customer's own setting.
- Recommended vs configured: every threshold in an answer is labelled "recommended (Agent E2)" or "configured (your VCF Operations)". For a question about the user's own alert or policy, Agent E2 asks for the alert definition (symptoms, thresholds, wait and cancel cycles), or answers with the recommended set and says so. At 1.2 the shipped VCF Operations alert definitions are in the catalog, so a default alert is recognised by name.
- Class of service: asked once when it changes the answer; all classes shown when there are three or fewer rows.
- Answers given (class, interval, configured thresholds) carry to later questions in the same conversation.

## 12. What Agent E2 always knows

- An up-front prompt block, about 200 tokens, generated from the `uses` sentences of the files (as [`harness/primer.py`](../harness/primer.py) generates its blocks), states the frame before any lookup:
  - the uses and their question, time span, spike filter, deadline;
  - a threshold applies to one reading: object, metric, instance, interval;
  - KPI colour means how bad; alert colour means by when; yellow is never an alert;
  - alerts are intra-day; a capacity alert means a bug or a hardware availability issue;
  - KPI is performance only; availability is KAI, security KSI; symptom and condition are one test;
  - every number comes from a lookup; recommended and configured are labelled.
- Each lookup result carries the `why` sentence and the knowledge file. Agent E2 reads the file when the question asks why (U9) or when it judges a customer's own threshold (U5).

## 13. Target implementation

| Part | Today | Target |
|---|---|---|
| [`knowledge/catalog/`](../knowledge/catalog) | 2 threshold files, joined by name | 6 files (section 8), joined by reading key |
| Catalog load ([`harness/catalog.py`](../harness/catalog.py)) | Tables `thresholds` (with `use`), `kpi`, `bands` (capacity model rows) | Tables `readings`, `reading_names`, `kpi`, `tests` (sli, rule, symptom), `targets` (sla, kai, ksi), `models`, `model_inputs`, `decisions`, `alerts`, `alert_symptoms` |
| Name to reading | Fuzzy score on English names | Exact match on `names` and external keys first; fuzzy only as fallback, marked as a guess |
| Lookup | Returns rows | Extends the existing `catalog` tool with `value`, `use`, `class`: returns the verdict per use, `why`, "not comparable" for other readings, "depends on" for missing parts. One tool, not a new one: each tool costs prompt tokens and choice errors for a 32B LLM |
| Comparison | By the LLM | In the catalog: levels and bands, direction, the boundary rule |
| Alert timing | Free text | Computed: time to fire and to clear from wait and cancel cycles |
| Reading set (`Catalog.facts_for`) | Counters and rules of the files in the reading set | Results of section 10 for every reading of the files in context, bands included |
| Term map (`user-terms.yaml`) | Files | Files and reading keys, so the lookup starts before the LLM asks |
| Up-front block ([`harness/primer.py`](../harness/primer.py)) | Tool advice | The threshold frame of section 12 |
| Clarifying rule ([`harness/clarify.py`](../harness/clarify.py)) | Object, layer, interval, version | Adds instance, use, class, the customer's own setting; reads "depends on" |
| Verifier ([`harness/verify.py`](../harness/verify.py)) | Soft check on numbers in the reason line | Every number with a unit in the whole answer checked against the returned rows; a threshold not returned triggers the repair turn after the benchmark shows it helps |
| Lint ([`project/tools/lint.py`](tools/lint.py)) | Sections by use, no other section; `class` on SLA rows; `criticality` red or orange on alert rows; fields, quotes; `kpi` one copy, values worsen yellow to red, each line matched to its Markdown band table by metric name, both ways; capacity band rows vs Markdown | Plus: `use` and `reading` on every row; reading exists; ids unique; no yellow alert; cancel cycles within R1-R6 (section 9) |
| Tools | `kpi_csv.py` | `kpi_csv.py` on the new files; a migration script to the 6 files |
| Tests ([`harness/test_tools.py`](../harness/test_tools.py)) | Lookups return sourced rows | Verdicts per use, not-comparable cases, depends-on cases, alert timing, dominance |

## 14. Alternatives considered

| Option | Pros | Cons | Verdict |
|---|---|---|---|
| A. One file for all thresholds | One join for U9 | 2,000+ lines; review hard | No |
| B. One file per pillar plus alerts | Matches the `pillar` tag and the SP5 model; KPI and SLA of a reading together | Alerts span pillars; two shapes per file | Yes, with `use` from the section name and `reading` on every row |
| C. One file per use | Matches the scoring | KPI and SLA of one reading in two files | No: `use` as a field gives the same query |
| D. External key (VCF Operations or vCenter) | No mapping file | Neither covers esxtop, book metrics and derived metrics; renames break rows | No: own key plus mapping |
| E. Full alert definitions now | U4 complete | 1,193 definitions wait on the overhaul (1.2) | Thin block now, full catalog at 1.2 |
| F. A separate threshold tool | Clear purpose | One more tool for a 32B LLM to choose | No: extend `catalog` |

## 15. Work list

### 15.1 1.0, in order
1. Done 2026-11-10: answers to Q152-Q158; `levels` as the one copy of the KPI levels; lookups and reading-set facts return them.
2. `readings.yaml` for every reading that has a threshold today.
3. Migration to the performance, capacity and alerts files. Done 2026-11-11: sections by use (`sla`, `sli`, `kpi`; `models`, `decisions`, `rules`; `alerts`), `class` and `criticality` as fields, use labels in every result. Alert rows into symptoms and alert definitions: done 2026-11-12 (section 8.4). Still to do: cancel cycles (step 10); reading keys (step 2).
4. Catalog tables, lookup with verdicts, the case's metric names, reading-set facts, unit tests.
5. Up-front block, clarifying triggers, verifier check.
6. `thresholds-availability.yaml` with its two rows.
7. [`project/knowledge-rules/thresholds.md`](knowledge-rules/thresholds.md): the threshold files of this design.
8. Benchmark: questions for U4, U5, U9, and a clarifying set (asked when it should, did not ask when it should not).
9. Done 2026-11-12: alert definitions (id, name, criticality, pillar, match, symptom sets, wait cycles) for the recommended alerts; persona not added.
10. Cancel cycles of the recommended alerts set by section 9, once approved.

### 15.2 Open to contributors
- `thresholds-availability.yaml`: availability SLA and internal target per class; source: the vCommunity adapter's Operational Availability page.
- `thresholds-security.yaml`: compliance and security targets and SLA; "is it secure?" covers security and compliance.
- `readings.yaml`: VCF Operations keys from the 9.1 metric reference; vCenter and esxtop columns from `vcenter-counters.yaml` and `esxtop-fields.yaml`.
- Alert symptoms for configuration, compliance and inventory.

### 15.3 After 1.0
- Capacity: Agent E2 recomputes Cluster Consumption, Cluster Risk and Close for Business from their inputs, for what-if questions and for clusters where the scores are not published.
- Full alert definition catalog from the overhaul (1.2), referencing symptom ids.
- Live VCF Operations: configured thresholds and alert definitions read directly; U1 on live data.

## 16. Risks

- Ten `use` values is the upper limit for a 32B LLM to keep apart; every result names its use.
- Migration touches 4 SLI rows, 31 `kpi` lines and 72 rule quotes: by script, then lint.
- Most VCF Operations keys are unknown; until filled, screen names map to keys through `names`.
- The catalog is not chunked, so retrieval should not move; the retrieval check runs before and after anyway.

## Sources
- Broadcom TechDocs, VCF 9.0: [Alert Definition Best Practices](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-0/infrastructure-operations/configuring-alerts-and-actions/defining-alerts-best-practices.html).
- Broadcom TechDocs, VCF 9.1: [Add a Virtual Machine CPU Usage Symptom to the Alert Definition](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/configuring-alerts-and-actions/create-a-problem-alert-definition/add-a-virtual-machine-cpu-usage-symptom-to-the-alert-definition.html).
- Knowledge base: [`sp5-framework/performance/kpi-vs-sla`](../knowledge/sp5-framework/performance/kpi-vs-sla.md), [`sp5-framework/outputs/alert-design`](../knowledge/sp5-framework/outputs/alert-design.md), [`sp5-framework/outputs/alerts-and-insights`](../knowledge/sp5-framework/outputs/alerts-and-insights.md), [`vcf-operations/alert-definitions`](../knowledge/vcf-operations/alert-definitions.md), the cluster models, `close-for-business`, [`sp5-framework/observability/thresholds`](../knowledge/sp5-framework/observability/thresholds.md).
- Harness: [`harness/catalog.py`](../harness/catalog.py), [`harness/agent.py`](../harness/agent.py), [`harness/modes.py`](../harness/modes.py), [`harness/primer.py`](../harness/primer.py), [`harness/clarify.py`](../harness/clarify.py), [`harness/verify.py`](../harness/verify.py), [`project/tools/lint.py`](tools/lint.py).
