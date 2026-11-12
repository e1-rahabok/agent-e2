# KPI vs SLA

## KPI only
- Performance monitoring and troubleshooting use the KPI only. No performance SLA, no SLI, no SLO.
- The SLA is a business contract between two parties ([`sp5-framework/concepts/sla-metrics`](../concepts/sla-metrics.md)). It is not an operations metric.
- A contract counts pass or fail against one agreed line, monthly. Operations need to know how bad, now, and on which object. The KPI gives both: a 0-100 score per object, at 20-second resolution, read daily.
- A performance SLA is rarely defined with a number. Customers who say they have one, probed for the metric, state the wrong one or none (section Misconceptions).

## Two steps of maturity
| Step | How it works |
|---|---|
| Complaint | Reactive, alert-driven, tickets passed between teams, blame between teams |
| KPI | Modelled, measured, agreed; one policy for all; SOPs from insight; an RCA closes with an alert set up |

- The KPI step:
  - uses both the 20-second and the 5-minute average;
  - quantifies consumer and provider objects;
  - includes the Guest OS when IT owns VM sizing;
  - has no class of service; the expectation is set by production;
  - both the application team and the infrastructure team track the KPI, through a self-service portal.
- Start with KPIs: they need no class of service. With different expectations for production and non-production, make one group per environment and a super metric that averages each group's KPI. Production should score better.

## KPI vs SLA
- Owner and purpose:
  - KPI: operations, internal. How did the object perform, and how bad was it?
  - SLA: business, between provider and consumer. Did we keep the promise? A penalty, usually a credit on the next bill.
- Scope:
  - KPI: one metric for one object: VM, Guest OS, ESXi, cluster, pod. VM and Guest OS each have a KPI. For the application team they are one entity (permanent 1:1), so operations can report the average of the two as a VM GOS KPI ([`sp5-framework/performance/performance-kpi-design`](performance-kpi-design.md)).
  - SLA: only on the consumer's object, the VM or the pod. Never on a cluster or a Kubernetes node.
- Reference:
  - KPI: reality, the absolute value: how bad. A score of 75% for one 5-minute interval on a development VM is acceptable; it is not a contract with a penalty.
  - SLA: relative to an agreed number, near 100%.
- Target and actual, and how a daily actual is read: [`sp5-framework/performance/performance-kpi-design`](performance-kpi-design.md), section Reading a KPI over time.
- Cadence: KPI daily, in a technical meeting; a month is far too late. SLA monthly, in a business meeting.
- Timing: KPI is a leading indicator, 5-minute window, 20-second accuracy, more metrics and events: the start of troubleshooting, before a complaint. An SLA is lagging, 30 days back.
- Period: KPI is based on day, not date: a rolling window (last 1 hour), like live operations. An SLA uses a fixed calendar month.
- KPIs fit when the infrastructure team owns VM sizing. Sizing the VM is sizing the Guest OS, so the team answers for Windows and Linux metrics too.
- A KPI is colour coded (green, yellow, orange, red) so the reader reacts before the situation degrades. What a KPI is, its design and scoring: [`sp5-framework/performance/performance-kpi-design`](performance-kpi-design.md).
- KPIs per layer:
  - business (line of business): business metrics (transaction volume, concurrent customers) and IT metrics (page response time, error rate);
  - application (IT developers): custom code and packaged ISV software, such as web server, application server and database KPIs;
  - infrastructure (IT administrators): consumer layer VM KPI and Kubernetes pod KPI; provider layer vSphere cluster, vSAN and NSX Edge KPIs.

## KPIs in VM as a Service
- VM KPI: stops at Windows or Linux. The application or service inside the Guest OS is excluded: the infrastructure team stops at the OS.
- Guest OS KPI: when central IT owns the Guest OS.
- Business application KPI: three levels. The business transaction first (user login). Below expectation → the application software KPI (Apache web server) and the infrastructure KPI (the VM KPI).
- vSphere cluster KPI: only the contention metrics of the running VMs. Utilization is excluded: it has no direct link to cluster performance. A vSAN cluster adds vSAN performance metrics. Implementation: [`vsphere/object-types/cluster/cluster-performance`](../../vsphere/object-types/cluster/cluster-performance.md).
- vSAN KPI: disk latency of every VM using the vSAN datastore, from the same or another cluster.
- NSX KPI: many-to-many with vSphere clusters, so not tied to one cluster.

## Misconceptions
- "Our performance SLA is met, so there is no performance problem" → ask which metric, object, target and window. Usually there is none, or it is on the wrong object. Read the KPI.
- "Our SLA is Cluster Availability" → the application team cares about its VMs and pods, not the cluster. A cluster number hides the VM that was down.
- "Track an SLI or SLO as the leading indicator" → the KPI is the leading indicator: 20-second accuracy, colour levels, alerts on it.
- "Cluster performance KPI includes host utilization" → it includes only the contention of the running VMs.

## Metadata

```yaml
id: sp5-framework/performance/kpi-vs-sla
retriever_guide: how-it-works
scope: sp5-framework
technology:
- system
pillar:
- performance
- availability
product:
- vsphere
- vsan
- nsx
- vcf-operations
object:
- VirtualMachine
- ClusterComputeResource
internal_derive:
- sp5-framework/performance/performance-kpi-design
related:
- sp5-framework/performance/performance-management
- sp5-framework/concepts/sla-metrics
- vsphere/object-types/cluster/cluster-performance
- vsphere/object-types/vm/vm-performance
- sp5-framework/concepts/performance-vs-capacity
- sp5-framework/concepts/realms-and-layers
images: []
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Performance Management > Key Performance Indicator > KPIs as a Stepping Stone; KPI | SLA > Differences; KPIs in IaaS'
corrections:
- 'Section ''KPI vs SLA'', Scope: Part 1 combines VM and Guest OS in one KPI; outdated. Two KPIs; the VM GOS KPI is their average, for the application team.'
- 'Section ''KPI means performance'': a KPI is a baseline, not a target.'
- 'Sections ''Two steps of maturity'', ''KPI vs SLA'': KPI timing confirmed; both teams track the KPI.'
- 'Section ''KPI only'' (2026-11-11): the book''s third maturity step (SLA), the SLI and the Performance SLA are removed. The SLA is a business contract; performance is managed by the KPI only.'
review_notes: []
status: draft
```
