# Alerts, symptoms and insights

## Why alert storms happen
- Operations that start from alerts are reactive by construction.
- IT operations commonly carry more than 1,000 alert definitions across all monitored systems.
- Thresholds are set conservatively to be warned early. The result is an alert storm.
- Alerts are set to close automatically when the symptom disappears. Then no alert is read as no problem: lazy operations.
- Root cause: alerts used as a to-do list or a reminder, so that nothing is missed.

## Observability is built in
- Observability is built into the architecture, not added later: every component can be monitored, down to the smallest. A system that cannot be monitored does not go into production.
- Many applications, software and hardware leave no trail for post-mortem analysis.
- Observability is a property of the system. Monitoring is an action by an actor.
- Peers: observability with debuggability; monitoring with troubleshooting.
  - A system that emits metrics and logs is not necessarily debuggable: it may give no way to step through it or intervene.
  - An administrator who can monitor a system cannot necessarily fix it.
- Debuggability is the property that matters for fixing. Modern debugging can include in-line analytics while the code runs; the system must be built for it.
- Experts should explore data (metrics, logs, events, traces, NetFlow) on a regular cadence. Low-level metrics often behave differently from their documentation, which is rarely deep; metric bugs from several vendors were found this way.
- Input types: [`sp5-framework/observability/input-types`](../observability/input-types.md).

## Symptom, alert, insight
- Symptom: a minor, non-urgent issue. Caught in the proactive daily health check.
- A mild symptom that does not go away becomes an alert: it is now urgent.
- Alert: bottom up. One object crossed a threshold.
- Insight: top down. Derived from a set of alerts and symptoms plus context, using many more metrics, above all the supporting ones.
- An insight needs technology expertise and experience of the environment. It deals with hints, not issues.
- Insights complement alerts; they do not replace them. An insight has no automatic close: it opens no help-desk ticket.
- A proactive alert is a contradiction. Proactive means acting before something forces a reaction. Reacting to an alert is reactive, even when the business is not yet hit.
  - Example: vSAN shows high disk latency at Sunday midnight; it is fixed before Monday. Still reactive: an alert forced the action. The same alert in business hours with business impact is no more reactive.
- A threshold sees only objects above it. For each object that crosses it, many sit just below: the alert is the tip of an iceberg.
- Questions insights answer, too fuzzy to define as alerts:
  - Are we being attacked? Are there events and activities where they should not happen?
  - Is performance degrading? Is there a common pattern and cause?
  - Is the environment behaving differently from what we expect?
- An insight is useless to someone who does not know the environment. Example: total IOPS is low. Meaningless unless high throughput is expected that day, such as the day before Christmas at a retailer; then sales are not happening.
- Limits of proactive work: false positives, and the daily discipline it takes.

## Finding, issue, alert, notification
- Finding: the result of troubleshooting or analysis, from logs, events, metrics and tasks. Good or bad. The sources report the negative, so an empty result is usually a good day (example: no login to a confidential cluster).
- Positive findings feed insight. Deriving an insight from findings takes someone who knows the technology and the environment.
- Negative findings are issues. An issue is a negative finding: something was found to be bad. It has one or more symptoms; no symptom, no issue.
- Symptoms left untreated can degenerate over time and become urgent: that is when an issue becomes an alert.
- Issue types: availability (hard failure, soft failure), configuration (drift, insecure), performance, capacity, security.
- Every issue also feeds insight, which is read in the daily check at the start and end of the day. Insight is not urgent and needs a subject matter expert.
- Alert: an urgent issue. The NOC team watches alerts several times a day. A non-urgent issue is not an alert: it goes to the daily check.
- Notification: the way VCF Operations pushes an alert to a person at once: mobile or email. Only an important alert is pushed (red: urgent and important). An alert that is urgent but not important (orange) stays in the NOC's alert list.
- Admins want urgent issues fast; important but not urgent issues are analysed after the time-sensitive ones.
![Information (logs, events, metrics, tasks) → analysis → Finding. Positive findings → Insight (not urgent, requires SME) → Daily Check (start of day + end of day). Negative findings → Issue (with its symptoms). All issues → Insight; non-urgent issues → Daily Check; urgent issues → Alert (NOC team watch multiple times daily) → important → Notification (immediately pushed to mobile or email)](images/finding-issue-alert-insight-notification-flow-diagram.png)
- Monitoring and troubleshooting with these terms: [`sp5-framework/concepts/monitoring-vs-troubleshooting`](../concepts/monitoring-vs-troubleshooting.md).

## Alert vs insight
| Item | Alert | Insight |
|---|---|---|
| Goal | Fix: something is ill | Prevent: nothing is ill yet |
| Record | Formal event with a ticket; may have an incident | Not a formal event; no incident |
| Impact | Business or operations may be impacted | None |
| Problem | Known; root cause may be unknown | None known |
| Urgency | Today: red as soon as possible (at most 1-2 hours), orange by the end of the day | Not urgent: read as a group in the daily health check |
| Nature | Reactive, unpredictable; the system tells you | Proactive, regular (daily, weekly, monthly); you start it |
| Response | Mandatory | Not applicable: you initiate it |
| Person | Low expertise; follows an SOP | Deep expertise; no steps to follow |
| Context | Overall environment not needed | Environment and recent operations needed |
| Metrics | Primary metrics: the what | Primary and secondary: why the primary is bad |
| Interface | Email or phone notification; one alert, bottom up | Large dashboard; whole environment, top down |

## Prevention window
- Two points in time: when the operations team knows there is a problem (insight), and when customers would know if nothing were done (alert). The time between is the prevention window.
- Insight types: secondary metrics, while consumers are not yet affected; primary metrics at a low grade, or rare with no pattern; total consumption rising above what was expected; undesirable security events above what was expected.
- Alert types: a primary metric at its urgent threshold; a lagging indicator above its threshold; an availability event (for example a VM reset).
- Alert examples: VM CPU Ready and VM disk latency on each VM; on a cluster, the share of its VMs above a per-VM value (25% of VMs for the infrastructure CPU alert), not a cluster average, which hides the victim. Values: the alert rows of the threshold catalog.
- Insight examples: anomaly metrics; VM CPU Co-stop; VM CPU Other Wait; read latency of an individual virtual disk; the maximum vMotion stun time across the environment (healthy below 0.2 second); the queue time of an ESXi device (QAVG). An insight reads the KPI levels early; it does not need a lower number than the alert, only an earlier signal.
- Insights use finer metrics and supporting metrics. Example: the alert watches the VM's disk latency; the insight watches each virtual disk, whose worst instance is always at least the VM value (instance rule, [`sp5-framework/observability/thresholds`](../observability/thresholds.md)).
![Timeline: Insight (green) → Prevention Window (yellow to orange) → Alert (red). Insight starts at the point when you know it is a problem; Alert starts at the point when your customers know it is a problem if you do nothing. Insight types: secondary metrics, consumers not yet affected; primary metrics, but low grade or infrequent with no pattern; rising total consumption, higher than expected; higher than expected undesirable security events. Alert examples: primary metric at an urgent threshold; lagging indicator threshold breached; availability event (for example VM reset)](images/insight-prevention-window-alert-types-examples-diagram.png)
- Metric files: [`vsphere/technology/cpu/metrics/virtual-motherboard/co-stop`](../../vsphere/technology/cpu/metrics/virtual-motherboard/co-stop.md), [`vsphere/technology/cpu/metrics/virtual-motherboard/other-wait`](../../vsphere/technology/cpu/metrics/virtual-motherboard/other-wait.md), [`vsphere/technology/storage/metrics/virtual-motherboard/virtual-disk`](../../vsphere/technology/storage/metrics/virtual-motherboard/virtual-disk.md), [`vsphere/object-types/vm/metrics/vmotion`](../../vsphere/object-types/vm/metrics/vmotion.md), [`vsphere/technology/storage/concepts/esxi-storage-latency-stack`](../../vsphere/technology/storage/concepts/esxi-storage-latency-stack.md).

## Lagging and leading indicators
| Item | Lagging indicator | Leading indicator |
|---|---|---|
| Used in | Alerts: the fallback when proactive work missed it | Insights |
| Focus | Metrics that hit customers (consumer layer) | Underlying metrics that drive the primary ones (provider layer) |
| Technicality | Meaning simple, formula maybe not | Low level; deep technical knowledge |
| Persona | Level 1 and help desk | Subject matter expert who knows the environment |

- The KPI serves both: the insight reads it early, the alert at red ([`sp5-framework/performance/kpi-vs-sla`](../performance/kpi-vs-sla.md)).

## What an alert is: rapid, real, rare
- Rapid: the issue is urgent, so it must be known at once.
  - If time does not matter, a daily SOP with a dashboard works better: it shows the big picture.
  - Long-term work such as capacity management belongs on a dashboard.
  - Do not send alerts to people outside day-to-day operations.
  - An alert is not a to-do list and not a reminder.
- Real: something is wrong. A symptom is not an alert.
  - No alert on inventory changes as a rule: inventory is an account of something, not a fault.
- Rare: frequent alerts numb the reader.
  - An alert is about exceptions, not the big picture. If the whole house is on fire, an alert is too late.

## Criticality: yellow, orange, red
- Something happened to an object: a metric crossed a threshold, its configuration changed, or its state changed.
- First question: urgent? Must it be acted on today?
  - No → not an alert. It becomes an insight, read with others as a group in the proactive health check at the start of the day or shift. Seen as a group, it shows the big picture.
  - Yes → acknowledge, then: when to act?
    - By the end of the day → orange: urgent, not important.
    - As soon as possible, at most 1-2 hours → red: urgent and important.
- The wider the impact, the higher the importance.
- Alerts are reactive: when one fires, time has already started. Define as few as possible: only issues that cannot be prevented.
- Alert storms and alert fatigue in enterprise IT come from alerts that were never defined properly.
- In daily operations:
  - Red: urgent and important. As soon as possible, at most 1-2 hours; not drop-everything.
  - Orange: urgent, not important. By the end of the day; do not defer to tomorrow.
  - Yellow: not urgent, so not an alert. An issue that can wait until tomorrow is not urgent: handle it as an insight in the health check.
  - Emergency: a small subset of red. Act that minute, even at 02:00, because each minute matters. Rare. VCF has no alert defined for it yet.
  - Green: nothing to do.
![Decision flow: something happened or changed on an object → urgent (act today)? No → low importance (yellow), next business day, seen as a group in the daily health check. Yes → acknowledge, when to act? As soon as possible → high importance (red); sometime today → medium importance (orange). The wider the impact, the higher the importance](images/alert-criticality-urgency-importance-diagram.png)

## Misconceptions
- "Yellow alert: deal with it tomorrow" → yellow is not an alert. Not urgent means it belongs in the daily health check as an insight.
- "Alert colours and KPI colours mean the same" → an alert colour is a deadline, because time has started. A KPI colour band is proactive and carries no deadline. They are not related.
- "We have proactive alerts" → reacting to an alert is reactive, even before business impact. Proactive work is insight from the daily health check.
- "No open alerts, so no problem" → alerts close themselves when the symptom fades, and a threshold sees only objects above it. Many objects sit just below.
- "Lower the thresholds to catch problems earlier" → conservative thresholds cause alert storms. Early warning comes from leading indicators read as insights.
- "Yellow is a problem to fix now" → yellow is a symptom, possibly a false positive. Review it the next business day in the daily health check.
- "Red means drop everything" → red is attended within 1-2 hours. Only the rare emergency subset is acted on that minute.
- "Alert on every inventory change" → inventory is an account, not a fault: an alert must be real.
- "Alert on capacity running low months ahead" → not urgent; long-term actions such as capacity belong on a dashboard.
- "The cluster average is fine, so no VM needs attention" → alerts on averages miss individual objects. Insights read per instance: each VM, each virtual disk.
- "An empty findings report means the check did not run" → the sources report the negative; no finding is usually a good day.
- "Every alert must reach someone's phone" → only urgent alerts are notified at once; others go to the daily check.
- "Observability tooling replaces monitoring and troubleshooting" → observability is a property of the system; monitoring and troubleshooting are actions on it.

## Metadata
```yaml
id: sp5-framework/outputs/alerts-and-insights
retriever_guide: how-it-works
scope: sp5-framework
technology:
- system
pillar:
- availability
- performance
- compliance
- capacity
product:
- vsphere
- vsan
- vcf-operations
object:
- VirtualMachine
- ClusterComputeResource
- HostSystem
internal_derive:
- sp5-framework/observability/input-types
- sp5-framework/observability/thresholds
related:
- sp5-framework/performance/kpi-vs-sla
- sp5-framework/outputs/alert-design
- sp5-framework/concepts/iaas-business
- sp5-framework/concepts/purpose-driven-architecture
- vsphere/technology/cpu/metrics/virtual-motherboard/co-stop
- vsphere/technology/cpu/metrics/virtual-motherboard/other-wait
- vsphere/technology/storage/metrics/virtual-motherboard/virtual-disk
- vsphere/object-types/vm/metrics/vmotion
- vsphere/technology/storage/concepts/esxi-storage-latency-stack
images:
  - path: images/insight-prevention-window-alert-types-examples-diagram.png
    product: [vsphere, vcf-operations]
    object: [VirtualMachine, ClusterComputeResource, HostSystem]
    topic: 'Insight, prevention window and alert on one timeline: insight types and alert examples'
    image_type: diagram
  - path: images/finding-issue-alert-insight-notification-flow-diagram.png
    product: [vcf-operations]
    object: [VirtualMachine, ClusterComputeResource]
    topic: 'Finding, issue, insight, alert, daily check and notification flow'
    image_type: diagram
  - path: images/alert-criticality-urgency-importance-diagram.png
    product: [vcf-operations]
    object: [VirtualMachine, HostSystem, ClusterComputeResource]
    topic: 'Alert criticality from urgency and importance: yellow, orange, red'
    image_type: diagram
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Your Private Cloud > Overview (alert storms, lazy operations); Purpose-Driven Architecture > Observability (Symptom | Alert | Insight; Lagging Indicator | Leading Indicator; Alert); SP5 Framework > Basic Terminology'
corrections: []
review_notes:
- 'To check: Section ''Prevention window'', last bullet before the image: the instance-rule example (not in the source).'
- 'Section ''Criticality'': the book''s alert vs insight table calls alerts hopefully not important and insights important; its colour table calls red urgent and important.'
- 'Not copied: the iceberg picture (decorative) and the colour legend (red: review today, the sooner the better; orange: review today; yellow: review tomorrow, could be a false positive; green: great), whose content is in the text.'
status: draft
```
