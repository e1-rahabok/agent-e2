# Monitoring vs troubleshooting, root cause analysis and validating a log alert

## Monitor: what; troubleshoot: why
- Monitoring compares plan with actual. The goal must be defined; if reality differs from what the architecture should deliver, adjust the plan. Plan and monitor form a loop.
  - Example: VDI planned for 10,000 users. At 1,000 users they consume more than planned: scale down the rollout or add resources.
- Act when reality is worse than plan, not when a complaint arrives. Troubleshooting done proactively has time and no one rushing it.
- Troubleshooting is not the centre of operations. What can be troubleshot, and how, is planned in the architecture: what can go wrong, how it is detected, how it is remediated. Unplanned, each incident costs more than it should.

| Item | Monitoring | Troubleshooting |
|---|---|---|
| Question | What is the problem? | Why does it happen? |
| Nature | Proactive | Reactive |
| Expertise | Low: repetitive, with dashboards and alerts | High: varied steps, needs the environment's context |
| Metrics | Usually one, the SLA metric: primary, checked by SOP | Many, in layers: secondary, read when the primary nears its threshold |
| Duration | About 5 minutes | Can take days across teams |
| Frequency | Daily; Gold more often than Bronze | On demand |
| Timeline | Now and future: anticipate load | Now: put out the fire |
| Logs | Not required: metrics, properties, events | Almost always; NetFlow for network |
| SLA | Applies | Urgent once the SLA is breached |
| KPI | KPIs, not single metrics | Starting point, then raw supporting metrics |

- Interval: monitor at 5 minutes; 1 bad minute may have no business impact. Troubleshooting may need per-second data, but not every counter: if the remediation is the same, the extra detail adds nothing.

## Troubleshooting
- An expert team troubleshoots. The same team sets the thresholds the Level 1 team uses.
- Logs are needed: many systems emit incomplete metrics, and one common problem has many causes. The root cause can be far from the symptom.
- An incident means something is dead, slow or breached. Availability, performance and security are troubleshot. Capacity and cost are not.
- The aim is why, and a fix that prevents the next incident, not only the facts.
- When an object is not healthy, four areas, in this order:
  1. Contention: the primary indicator.
  2. Configuration: version incompatibility.
  3. Availability: soft errors, vMotion stun time, lock-ups. Usually needs VCF Operations for logs.
  4. Utilization: last. Even at 100% it does not matter if the first three are good.
![Not healthy → four areas, in this order: contention (primary indicator); configuration (version incompatibility); availability (soft errors, vMotion stun time, lock up; needs the log tool); utilization (check last; even 100% does not matter if 1-3 are good)](images/not-healthy-check-order-contention-configuration-availability-utilization-diagram.png)
- VM-level flow: `operations-management/performance/troubleshooting/vm-slow-triage`.

## Primary and secondary metrics
- Layer the troubleshooting metrics, events and properties so a less technical team can use them.
- Primary metric: defines performance; the what. Always 0-100%, usually a hybrid of several metrics. Example: Kubernetes Cluster Performance (%).
- Secondary metrics: explain the primary; the why. Aim for 0-100% too. Example: highest ESXi Memory Consumed (%) in a cluster.
- A metric that cannot be colour coded, such as VM Disk IOPS, is hard for Level 1: its meaning depends on context.

## First incident: forgivable once
- The first time an issue happens: troubleshoot, write the RCA, set up an alert.
- The second time: the same problem is known within minutes; a similar one is understood within an hour.
- Process maturity:
  - manual: blamestorming with all hands on deck, ping-pong between teams, time lost, no RCA;
  - optimized: SLA breach → big picture on a shared dashboard → joint analysis with shared tools → RCA report → alert set up in VCF Operations;
  - ideal: early warning → preventive action → optimization.

## Root cause analysis
- The most important content of an RCA report is the corrective action that prevents a repeat, above all the alerts that flag signs of recurrence. Without them the issue cannot be caught before it returns.
- The root cause often differs from the symptom: another object, a message that looks unrelated. It usually starts as a log message that never became an alarm in the UI.
- An alert from a log message must not give false positives. Validate it before setting it up.

## Validating a log message before alerting on it
- Example: VDI mass disconnect, more than 100 users at the same moment.
  - vmware.log: GuestRpc to the VDI agent timed out; second ping timeout, app assumed down.
  - vmkernel log, 0.4 s earlier: resuming traffic on DV port.
  - Analysis: the VM was briefly unavailable and then resumed transmitting; the fault was on the server side, not the client. With the GuestRpc timeouts, the Guest OS was unresponsive and then recovered.
  - Proposal: alert on the vmkernel message.
- Check: search the message across the whole environment in the log tool (VCF Operations for logs), above all on healthy, unaffected objects, over a full week, not only the incident window.
- Result: more than 1,000 occurrences in 5 working days, on many hosts, with a pattern that follows office hours. The message is routine; an alert on it would be a false positive.
- Rule: a message is a valid alert trigger only if it is rare on healthy objects and appears with the incident.

## Traps
- "Monitoring needs per-second data" → monitor at 5 minutes; per-second data is for troubleshooting, and only when it changes the remediation.
- "Utilization is 100%, so that is the root cause" → check contention, configuration and availability first. High utilization with none of them is not a problem.
- "Troubleshoot capacity" → capacity and cost are planned and monitored; incidents (dead, slow, breached) are troubleshot.
- "The RCA is done once the root cause is named" → it is done when the alert that detects a recurrence is set up.
- "Vendor support found the log message; set the alert" → check how often it appears on healthy objects over a week. A message seen 1,000 times in 5 days on healthy hosts is noise.
- "The error message names the failing object" → the root cause often sits on another object with a message that looks unrelated.
- "Give Level 1 raw counters such as VM Disk IOPS" → Level 1 needs 0-100% metrics that can be colour coded; raw counters need context.

## Metadata
```yaml
id: operations-management/performance/monitoring-vs-troubleshooting
retriever_guide: how-it-works
scope: operations-management
technology:
- system
- network
pillar:
- availability
- performance
- security
product:
- vsphere
- vcf-operations
- kubernetes
object:
- VirtualMachine
- HostSystem
- ClusterComputeResource
- VmwareDistributedVirtualSwitch
internal_derive:
- operations-management/performance/alerts-and-insights
- operations-management/performance/kpi-vs-sla
related:
- operations-management/performance/troubleshooting/vm-slow-triage
- operations-management/performance/proactive-operations
- operations-management/performance/health-risk-efficiency
- foundations/input-types
- vsphere/object-types/vm/metrics/vmotion
images:
  - path: images/not-healthy-check-order-contention-configuration-availability-utilization-diagram.png
    product: [vsphere, vcf-operations]
    object: [VirtualMachine, ClusterComputeResource]
    topic: 'Order of areas to check when an object is not healthy'
    image_type: diagram
source:
  document: PART 1 - Concepts of Operations Management.docx
  path: 'Your Private Cloud > SP5 Framework > Monitor | Troubleshoot; Troubleshoot; Root Cause Analysis (pp. 46-50)'
corrections: []
review_notes:
- 'Section ''Troubleshooting'', order: contention, configuration, availability, utilization (book diagram). The reactive track diagram in SP5 Framework: Process uses configuration, availability, known bugs, consumption; vm-slow-triage has its own order (Q060). Q104.'
- 'Section ''Troubleshooting'': the diagram says Aria Operations for Logs; written as VCF Operations for logs (current name, Q107).'
- 'Monitoring table: logs not required for monitoring, while availability data comes mostly from logs (health section) and the daily SOP reads logs for soft errors. Duration 5 minutes vs the daily check of about 1 minute and 10 minutes elsewhere. Q105.'
- 'Section ''Validating a log message'': log lines from the book image (2016 example); the Log Insight screenshot is not copied. ''0.4 s earlier'' computed by Claude from the timestamps (23:42:14.842 vs 23:42:15.266).'
- 'Section ''Validating a log message'', rule: Claude''s generalization of the example.'
status: draft
```
