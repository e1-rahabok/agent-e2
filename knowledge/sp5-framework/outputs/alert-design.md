# Alert design

## Managing vs minimizing alerts
- Managing alerts deals with alerts already triggered. Minimizing alerts prevents them from firing.
- Use insight to keep alert definitions few: an alert is reserved for urgent and important issues.
- Goal: the broadest coverage with the fewest alert storms. That takes planning of each definition, its conditions and its thresholds.
- What an alert is (rapid, real, rare) and its colours: [`sp5-framework/outputs/alerts-and-insights`](alerts-and-insights.md).

## One question per alert
- For each alert: what action must the person who sees it take, today?
  - Nothing: do not disturb them today. A dashboard shows the issue better, together with objects not yet at the threshold.
  - Something that can be automated: automate the response instead of alerting. Automation has no common sense; logic that is not fool-proof can cause a disaster.
  - Escalate to Level 2 with context and a first analysis: depends on urgency. Level 2 works on longer timelines and reads the big picture, so Level 1 can group related alerts into one escalation. A dashboard shows that picture better.

## Persona: who receives it
- Design each alert for a persona. What matters to one is noise to another.
- Three main personas:
  - application team;
  - infrastructure team, the main persona, with sub-personas such as the network team and the storage team;
  - security team, which looks at both, from the security side only.

### Application team vs infrastructure team
- Guest OS alerts go to the application team, not the infrastructure team.
- In an overcommitted environment a VM can see contention. Let the infrastructure team act before the application team is alerted; this reduces blame:
  - give the application team red only; keep orange for the infrastructure team as a heads-up;
  - give the application team a higher per-VM threshold: its VM alert fires at a higher CPU Ready than the per-VM values of the ESXi, resource pool and cluster alerts, which watch a share of the same VMs.
- Infrastructure-level alerts, such as on ESXi, are not relevant to the application team.
- Shared infrastructure alerts look at the population, not a few VMs: use 25% of the VM population as the overall threshold, with a lower per-VM threshold because 25% can mean hundreds of VMs. Applies to ESXi, resource pool and cluster; not Datacenter, whose clusters can serve different purposes.

## Class of service: which workload
- Workloads are not equal: a mission-critical application matters more than its development copy.
- Use the 3 classes of service: Gold (mission critical), Silver (standard production and DR), Bronze (test and development, non-production). More than 3 complicates operations.
- A class belongs to the data centre infrastructure the VM runs on (a Gold cluster with its storage and network), not to the application. The colour names are short words, not application labels.
- The more critical the class, the lower the threshold. Example for VM disk latency:

| Class | VM Disk Latency above | For |
|---|---|---|
| Gold | 30 ms | 5 minutes |
| Silver | 60 ms | 10 minutes |
| Bronze | 120 ms | 10 minutes |

- The table is an example of the step between classes (each 2x the one above), not values of the recommended set. The recommended set is one policy for every VM; a site with classes makes one VCF Operations policy per class and sets each class's values.
- An alert threshold per class is allowed: an alert colour is urgency plus importance, and a Gold VM is more important. The KPI has no class, and there is no performance SLA ([`sp5-framework/performance/kpi-vs-sla`](../performance/kpi-vs-sla.md)).

- Classes of service: [`sp5-framework/concepts/class-of-service`](../concepts/class-of-service.md).

## What to alert, by pillar
- Define the problem types of each pillar; for each type, decide whether it gets an alert.
- Availability:
  - Replace hardware before its manufacturing limit. Example: an SSD has a write endurance limit, as each write wears it. With thousands of disks, track the limit on a weekly dashboard and schedule replacement; no alert.
  - Watch hardware temperature: heat is the main enemy of electronics.
  - Keep the software stack compatible: version incompatibility is a known cause of outages.
  - Design redundancy, so an unplanned failure within the design allowance raises a non-critical alert. With N+1, one host down is not a red alert.
  - Treat soft errors as insight: they are non-critical events that warn early.
- Performance:
  - Do not reduce reactive work with lower thresholds: that creates noise. Track early-warning metrics as insight.
  - Consumption alerts: red only. The orange level belongs to the daily dashboard.
  - Contention alerts: suppress at low utilization, where the application likely feels no impact. CPU usage is the proxy for application activity.
  - Sustained high utilization, above all when trending up: daily check.
  - Keep the alert (customers would notice) apart from the insight (early, internal); both read the KPI. See [`sp5-framework/performance/kpi-vs-sla`](../performance/kpi-vs-sla.md).
- Security: a live attack (pair the alert with the NOC screen); undesirable events.
- Configuration: only high-risk settings that cause urgent problems such as slowness, outage or a breach. Non-urgent configuration goes to the daily health check.
- Compliance: only what cannot wait until tomorrow.
- Capacity: a principle, not a rule. Capacity management takes the long view (weeks and months), so done properly it raises no alert. A capacity alert means something is amiss: a software bug or a hardware availability issue (a failed host taking capacity away).
- An alert does not replace operations practice. Outdated VMware Tools is not urgent: a daily SOP lists the VMs with outdated Tools and the list is kept empty. An alert would make the team reactive and noisy.
- Trigger the alert on every affected object, victims and cause. A failure at the bottom ripples up. Example: a physical disk fails in a vSAN cluster; the disk group can go down; a host with one disk group loses its storage.

## What not to alert
- Anything that can be reviewed the next day: a daily dashboard shows it with the big picture.
- Availability: one failed backup. With 1,000 VMs backed up nightly and 1 failure, last night's backup still exists; no reason to troubleshoot at night. Many failures are the exception.
- Value: nothing in cost is urgent.
- Inventory: the NOC screen tracks inventory changes. Inventory is an account of what exists, not good or bad.
- Capacity: reclamation and downsizing belong on the daily dashboard. High utilization is often mistaken for a performance problem.
- Configuration: non-urgent issues, such as outdated VMware Tools.
- Compliance: non-urgent issues, such as non-security deviation from a corporate standard.
- Important but not urgent, so no alert:
  - A host in maintenance mode for 72 hours or more: not urgent after 3 days down; important because it is not normal.
  - A recoverable memory error on a host: recovered, so not urgent; important because it can spread. Schedule a hardware scan, which may require downtime.
  - vMotion taking 3x as long over 12 hours (0.2 s to 0.6 s) in 10 large clusters running 10,000 production VMs, unnoticed by application owners: not urgent; important because it can grow into a large problem.
  - A performance problem that hits random VMs for under 5 minutes, a few times a day for days: each owner is rarely hit and does not complain; adding VMs is now risky.

## Design the alerts as a set
- Start from the 4 resources: CPU, memory, disk, network. Each behaves differently.
- For each resource, design top down over every monitored object, consumers and providers together.
- For each object, cover both metric types: contention and consumption.
- Then validate:
  - consistency: walk each object type through all 4 resources;
  - bottom-up scenarios: check every case is caught.
- Result: an alert set per object type. For each object type, what it alerts on, and for each resource left out, why: not yet in the set, or the daily check or the NOC screen serves better. Some objects have 2 alerts for one resource because the problems differ, such as read and write latency.
- The recommended set, one file per object type, values in [`catalog/thresholds-alerts.yaml`](../../catalog/thresholds-alerts.yaml):
  - consumers: [`guest-os/guest-os-alerts`](../../guest-os/guest-os-alerts.md), [`vsphere/object-types/vm/vm-alerts`](../../vsphere/object-types/vm/vm-alerts.md);
  - compute providers: [`vsphere/object-types/esxi/esxi-alerts`](../../vsphere/object-types/esxi/esxi-alerts.md), [`vsphere/object-types/resource-pool/resource-pool-alerts`](../../vsphere/object-types/resource-pool/resource-pool-alerts.md), [`vsphere/object-types/cluster/cluster-alerts`](../../vsphere/object-types/cluster/cluster-alerts.md);
  - storage and network providers: [`vsphere/object-types/datastore/datastore-alerts`](../../vsphere/object-types/datastore/datastore-alerts.md), [`vsphere/object-types/datastore-cluster/datastore-cluster-alerts`](../../vsphere/object-types/datastore-cluster/datastore-cluster-alerts.md), [`vsphere/object-types/distributed-switch/distributed-switch-alerts`](../../vsphere/object-types/distributed-switch/distributed-switch-alerts.md), [`vsphere/object-types/distributed-port-group/distributed-port-group-alerts`](../../vsphere/object-types/distributed-port-group/distributed-port-group-alerts.md).
- An object type with no alert in the set still has its file, which says why.

## Generic vs specific alerts
- Generic alert: symptom oriented; many possible causes. Example: a VM did not get the CPU time it asked for.
- Specific alert: cause oriented. Examples: VM CPU contention from Co-stop caused by snapshots; VM CPU contention from Co-stop caused by too many vCPUs.
- Generic strengths: simpler names; fewer definitions.
- Generic weaknesses:
  - The alert does not tell the actual problem, such as read or write latency. The alert is the tip of the iceberg; the detail can come from insight dashboards.
  - The recommendation becomes a long list. Put conditions inside the recommendation so only the relevant advice shows, with live, clickable data rather than plain text.
- Specific strengths: a precise name; a clear action.
- Specific weaknesses:
  - Complex to design, and it misses unknown causes, so a generic catch-all stays.
  - Most causes cannot be proven. A snapshot cannot be proven to cause CPU contention or disk latency; only a probable cause is known.
  - Many known causes are misconfiguration, which a regular health check finds before any alert.
  - Mostly useful to the infrastructure team. A VM owner does not and should not care about the infrastructure cause.

## Threshold design
- Follow industry standards; for compliance, the relevant regulation.
- Alerts read KPI metrics with their own values; KPI levels and alert values are set apart.
- Review complaints, formal (tickets) and informal (through management).
- Use several conditions instead of one: each added condition narrows the alert.
- Contention: the issue must be both acute and sustained.
  - Acute: severe for one 20-second sample.
  - Sustained: the average over 300 seconds.
  - Set the acute threshold near 4x the sustained one, because a spike does not last 300 seconds ([`sp5-framework/observability/thresholds`](../observability/thresholds.md)). 4x is a guide, not a formula: it depends on the metric. A flat metric needs less than 4x, a volatile one more.
- Do not raise a contention alert at very low utilization, where there may be no real business workload.
- Keep a consistent scale between colours, so red stays the same step worse than orange. In the recommended set red is 2x orange on every threshold ([`catalog/thresholds-alerts.yaml`](../../catalog/thresholds-alerts.yaml)). Doubling the peak and the average together is one factor: an episode twice as bad crosses both. Red can be made worse than orange in three ways:
  - 2x the threshold: orange at 10 ms latency, red at 20 ms;
  - 2x the population: orange when 10% of VMs are hit, red at 20%;
  - 2x the time: orange for 5 minutes, red for 10 minutes. Not recommended.
- Wait time before the alert fires: contention 5 minutes, 10 minutes for metrics with false positives; consumption 10-15 minutes. The wait of each recommended alert is in its catalog row. VCF Operations setting: [`vcf-operations/alert-definitions`](../../vcf-operations/alert-definitions.md).

## Recommendation vs remediation
- A recommendation is advice; it changes nothing. A remediation runs a change in the environment. A recommendation is safer because it is not automated.
- A complete yet short recommendation, or a sound remediation, is hard to build: the root cause usually sits far from the triggered alert, in many combinations.
- IT systems have poor observability. A slow browser on a fast, lightly used laptop is hard to troubleshoot; a private cloud is harder. Products expose few meaningful metrics, often without an API, and some metrics are unreliable.
- A good recommendation is clear, lists its assumptions and gives the reason.
- Root cause analysis today is mostly elimination and requires human knowledge of the architecture. Example: troubleshooting VKS requires knowledge of Kubernetes, vSphere and the VKS implementation.
- Elimination is the method because a lower layer does not carry the identity of the upper layer: ESXi SCSI commands cannot be traced to a VM.

## Misconceptions
- "Alert on everything so nothing is missed" → an alert nobody must act on today is noise. Use the daily dashboard.
- "Lower thresholds catch problems earlier" → they create noise. Early warning comes from insight metrics.
- "Orange consumption alerts give early warning" → consumption alerts are red only; orange belongs to the daily dashboard.
- "High CPU Ready with idle CPU is urgent" → suppress contention alerts at low utilization; the application may feel nothing.
- "One host down in an N+1 cluster is red" → it is within the design allowance; non-critical.
- "Alert on outdated VMware Tools" → not urgent; a daily SOP keeps the list empty.
- "A specific alert names the root cause" → most causes cannot be proven; keep a generic catch-all.
- "Make red worse by waiting longer" → doubling the threshold or the population keeps the response time; doubling the wait delays it.
- "Red is always 4x orange" → red is 2x orange in the recommended set. About 4x is the guide between the 20-second peak and the 5-minute average inside one colour, and it varies with how volatile the metric is.
- "The same CPU Ready threshold for VM owners and infrastructure" → a higher threshold for application teams lets infrastructure act first.
- "A cluster alert fires when one VM suffers" → infrastructure alerts look at the population, such as 25% of VMs.

## Metadata
```yaml
id: sp5-framework/outputs/alert-design
retriever_guide: how-it-works
scope: sp5-framework
technology:
- cpu
- memory
- storage
- network
- system
pillar:
- availability
- performance
- compliance
- capacity
- value
product:
- vsphere
- vsan
- vcf-operations
object:
- VirtualMachine
- HostSystem
- ClusterComputeResource
- ResourcePool
- Datastore
internal_derive:
- sp5-framework/outputs/alerts-and-insights
- sp5-framework/observability/thresholds
related:
- sp5-framework/concepts/class-of-service
- sp5-framework/performance/kpi-vs-sla
- vcf-operations/alert-definitions
- guest-os/guest-os-alerts
- vsphere/object-types/vm/vm-alerts
- vsphere/object-types/esxi/esxi-alerts
- vsphere/object-types/resource-pool/resource-pool-alerts
- vsphere/object-types/cluster/cluster-alerts
- vsphere/object-types/datastore/datastore-alerts
- vsphere/object-types/distributed-switch/distributed-switch-alerts
- vsphere/object-types/datastore-cluster/datastore-cluster-alerts
- vsphere/object-types/distributed-port-group/distributed-port-group-alerts
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Proactive Operations > Alert > Alerts Planning (Target Persona, Class of Service, What to Alert, What not to Alert, Design: Alert Definition, Threshold Design, Wait Cycle, Recommendation | Remediation); Application Team; VM Alerts; CPU Alerts > Contention Alerts'
corrections: []
review_notes:
- 'To check: Section ''Recommendation vs remediation'': VKS (vSphere Kubernetes Service) as the current name for the source''s Tanzu and K8.'
- 'To check: Section ''Threshold design'': the wait-time link to the VCF Operations setting (not in the source).'
status: draft
```
