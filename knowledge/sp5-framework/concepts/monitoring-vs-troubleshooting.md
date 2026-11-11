# Monitoring vs troubleshooting

| Item | Monitoring | Troubleshooting |
|---|---|---|
| Question | What is the problem? | Why does it happen? What is the root cause?|
| Nature | Proactive | Reactive |
| Expertise | Low: repetitive, with dashboards and alerts | High: varied steps, needs the environment's context |
| Metrics | Usually one, the KPI: primary, checked by SOP | Many, in layers: secondary, read when the primary nears its threshold |
| Duration | A few minutes, about 5, when there is no problem | Can take days across teams |
| Frequency | Daily; Gold more often than Bronze | Rarely; On demand |
| Timeline | Now and future: anticipate load | Now: put out the fire |
| Logs | Required: logs stream continuously, not in 5-minute samples | Almost always; NetFlow for network |
| KPI | KPIs, not single metrics | Starting point, then raw supporting metrics |

- What is monitored decides the data. Logs stream continuously; metrics arrive per reporting interval.
- Performance monitoring reports the 20-second peak within each 5-minute reporting interval. Exception: a mission-critical system, where 20-second visibility is worth the cost of monitoring.


## Primary and secondary metrics
- Monitoring reads the primary metric, the what; troubleshooting reads the secondary metrics, the why. Definitions and examples: `sp5-framework/observability/triple-see-method`, section Primary and secondary metrics.

## Monitoring
- Monitoring compares plan with actual. The goal must be defined; if reality differs from what the architecture should deliver, adjust the plan. Plan and monitor form a loop.
  - Example: VDI planned for 10,000 users. At 1,000 users they consume more than planned: scale down the rollout or add resources.
- Act when reality is worse than plan, not when a complaint arrives. Troubleshooting done proactively has time and no one rushing it.


## Troubleshooting
- There are only 2 types of troubleshooting, as a system is either down or slow. 
- An incident means something is dead, slow or breached. You perform availability troubleshooting, performance troubleshooting, or security forensic investigation. Capacity and cost are not considered troubleshooting.
- Troubleshooting should not be the centre of operations. What can be troubleshot, and how, should be planned as part of the architecture. Document what can go wrong, how it is detected, how it is remediated. Unplanned incident gets added to the architecture.
- An expert team troubleshoots. The same team sets the thresholds the Level 1 team uses.
- Logs are needed: many systems emit incomplete metrics, and one common problem has many causes. The root cause can be far from the symptom.
- Troubleshooting may need per-second data, but not every counter: if the remediation is the same, the extra detail adds nothing.
- Root Cause Analysis is mandatory to ensure future problem is detected promptly. Ideally it comes with a fix that prevents the next incident, not only setting up alerts to detect.
- Order of checks, the same in the daily health check and in troubleshooting: availability, performance, security, capacity; inside each, configuration and known bugs as the drill-down (`sp5-framework/concepts/health-check`, section Order of checks).
- Availability is read from soft errors, vMotion stun time and lock-ups, mostly in logs (VCF Operations for logs).
- Utilization comes last. Even at 100% it does not matter if availability, performance and configuration are good.
- Every performance flow checks configuration, the VM slow flow included.
![The book's earlier order for an object that is not healthy: contention; configuration (version incompatibility); availability (soft errors, vMotion stun time, lock up; needs the log tool); utilization (check last; even 100% does not matter if 1-3 are good). Replaced by the order above](images/not-healthy-check-order-contention-configuration-availability-utilization-diagram.png)
- VM-level flow: `sp5-framework/performance/troubleshooting/vm-slow`.

### First incident: forgivable once
- The first time an issue happens: troubleshoot, write the RCA, set up an alert.
- The second time: the same problem is known within minutes; a similar one is understood within an hour.
- Process maturity:
  - manual: blamestorming with all hands on deck, ping-pong between teams, time lost, no RCA;
  - optimized: KPI red or complaint → big picture on a shared dashboard → joint analysis with shared tools → RCA report → alert set up in VCF Operations;
  - ideal: early warning → preventive action → optimization.

### Root cause analysis
- The most important content of an RCA report is the corrective action that prevents a repeat, above all the alerts that flag signs of recurrence. Without them the issue cannot be caught before it returns.
- The root cause often differs from the symptom: another object, a message that looks unrelated. It usually starts as a log message that never became an alarm in the UI.
- An alert from a log message must not give false positives. Validate it before setting it up.

### Validating a log message before alerting on it
- Example: VDI mass disconnect, more than 100 users at the same moment.
  - vmware.log: GuestRpc to the VDI agent timed out; second ping timeout, app assumed down.
  - vmkernel log, 0.4 s earlier: resuming traffic on DV port.
  - Analysis: the VM was briefly unavailable and then resumed transmitting; the fault was on the server side, not the client. With the GuestRpc timeouts, the Guest OS was unresponsive and then recovered.
  - Proposal: alert on the vmkernel message.
- Check: search the message across the whole environment in the log tool (VCF Operations for logs), above all on healthy, unaffected objects, over a full week, not only the incident window.
- Result: more than 1,000 occurrences in 5 working days, on many hosts, with a pattern that follows office hours. The message is routine; an alert on it would be a false positive.
- Rule: a message is a valid alert trigger only if it is rare on healthy objects and appears with the incident.

## Misconceptions
- "Monitoring needs per-second data" → performance monitoring reports the 20-second peak of each 5-minute interval; 20-second visibility only for mission-critical systems. Per-second data is for troubleshooting, and only when it changes the remediation.
- "Monitoring needs no logs" → logs are monitored too: they stream continuously.
- "Configuration is a separate check after performance" → it is the drill-down under availability, performance and security.
- "Utilization is 100%, so that is the root cause" → check contention, configuration and availability first. High utilization with none of them is not a problem.
- "Troubleshoot capacity" → capacity and cost are planned and monitored; incidents (dead, slow, breached) are troubleshot.
- "The RCA is done once the root cause is named" → it is done when the alert that detects a recurrence is set up.
- "Vendor support found the log message; set the alert" → check how often it appears on healthy objects over a week. A message seen 1,000 times in 5 days on healthy hosts is noise.
- "The error message names the failing object" → the root cause often sits on another object with a message that looks unrelated.
- "Give Level 1 raw counters such as VM Disk IOPS" → Level 1 needs 0-100% metrics that can be colour coded; raw counters need context.

## Metadata
```yaml
id: sp5-framework/concepts/monitoring-vs-troubleshooting
retriever_guide: how-it-works
scope: sp5-framework
technology:
- system
- network
pillar:
- availability
- performance
- compliance
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
- sp5-framework/outputs/alerts-and-insights
- sp5-framework/performance/kpi-vs-sla
related:
- sp5-framework/performance/performance-management
- sp5-framework/performance/troubleshooting/vm-slow
- sp5-framework/concepts/proactive-operations
- sp5-framework/concepts/health-risk-efficiency
- sp5-framework/observability/input-types
- vsphere/object-types/vm/metrics/vmotion
images:
  - path: images/not-healthy-check-order-contention-configuration-availability-utilization-diagram.png
    product: [vsphere, vcf-operations]
    object: [VirtualMachine, ClusterComputeResource]
    topic: 'Order of areas to check when an object is not healthy'
    image_type: diagram
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Your Private Cloud > SP5 Framework > Monitor | Troubleshoot; Troubleshoot; Root Cause Analysis'
corrections:
- 'Section ''Troubleshooting'', order: daily health check availability, performance, security; configuration as drill-down; known bugs are configuration; every performance flow checks configuration. The book diagram (contention, configuration, availability, utilization) is replaced.'
- 'Monitoring table, row Logs, and the interval bullets: monitoring needs logs; performance monitoring reports the 20-second peak within the 5-minute interval; 20-second visibility for mission-critical systems.'
review_notes:
- 'To check: Section ''Troubleshooting'': the order differs between files: the book diagram gives contention, configuration, availability, utilization; the reactive track diagram in SP5 Framework: Process uses configuration, availability, known bugs, consumption; vm-slow has its own order (Q060).'
- 'Section ''Troubleshooting'': the diagram says Aria Operations for Logs; written as VCF Operations for logs (current name).'
- 'Section ''Validating a log message'': log lines from the book image (2016 example); the Log Insight screenshot is not copied. ''0.4 s earlier'' computed from the timestamps (23:42:14.842 vs 23:42:15.266).'
- 'To check: Section ''Validating a log message'', rule: a generalization of the example; not stated in the book.'
status: draft
```
