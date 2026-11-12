# Service level agreement (SLA)

## SLA in the contract
- An SLA is one section of a business contract between a consuming entity (pays) and a providing entity (supplies). The contract also holds clauses, context and other agreements (confidentiality, payment terms, non-compete, marketing).
- The SLA section holds the metrics and their numbers. A financial penalty makes the provider accountable; certifications and architecture claims do not.
- The SLA (what is delivered) comes before the process and architecture (how it is delivered).
- An SLA is always between two parties. Internal objects (management cluster, vCenter, NSX Edge) have no SLA.
- Operations do not run on the SLA. Performance monitoring and troubleshooting use the KPI only: no performance SLA, no SLI, no SLO ([`sp5-framework/performance/kpi-vs-sla`](../performance/kpi-vs-sla.md)). Availability is monitored with KAI, security with KSI.

## Customer claims of an SLA
- Common: VMware customers say they have an SLA. Probed for the metrics that define it, they state a wrong metric, or they have none.
- Probe with five questions: which metric, on which object, which target, over which window, with which penalty. No metric and no number: it is an intention, not an SLA. Work from the KPI.
- The object must be one the consumer owns. Application teams care about their own VMs and Kubernetes pods, not the infrastructure under them.
- Typical wrong metric: Cluster Availability. The cluster is the provider's object. A cluster that stays up while one VM is down is a failure for that VM's owner; a host failure whose VMs restart elsewhere is a short outage for those VMs, and the cluster number hides it.
- The Kubernetes node is often owned by the SRE team, not the developers; developers may not care about it either. Their object is the pod.
- Provider objects (cluster, ESXi host, Kubernetes node, datastore, NSX Edge) carry a KPI and a KAI, never an SLA.

## IaaS contract contents
- Public providers commit to availability only: it is binary and the easiest to measure.
- Each SLA measures time in a bad state and expresses the month as 0-100%, 100% being perfect against the contract.

| SLA | Question | Measures |
|---|---|---|
| Availability | Is it up? | Downtime of the VM or Guest OS |
| Compliance | Is it secure? | Unsecured time |
| Service | Is the human and portal service delivered? | Response, provisioning, support |

- Performance has no SLA in this knowledge base. Fast is defined by the KPI: it shows how bad, at 20-second resolution, daily; a contract can only count pass or fail, monthly.
- Availability is largely a given: whatever the agreed number, a down VM is restored at once.
- The Compliance SLA is also called Security SLA (preferred term: `knowledge/glossary.md`). Customers and providers assume 100%; promising 100% without a contract number leads to disappointment.

## VM and Guest OS scope
- VM and Guest OS are two objects with a permanent 1:1 relationship. An IaaS provider often covers both. If the Guest OS is in scope, Windows or Linux is in the SLA.
- **Availability**
  - VM: powered on, BIOS running. The Guest OS is not in the VM SLA.
  - Guest OS: Windows or Linux running, including basic services such as security agents. The application is not in the SLA.
- **Security**
  - VM: protected per the vSphere hardening guide or industry regulation.
  - Guest OS: protected per its vendor or industry regulation.

## Availability SLA
- Definition: the Guest OS answers ping. A VM that runs but is isolated fails.
- The ping source is set by the IaaS provider, not the customer. It pings the VM, not a process: IaaS is not web server as a service.
- Uptime covers the Guest OS only. Application start-up (loading files, starting services) is not counted.
- Included: crashes caused by VMware Tools or by drivers and agents the infrastructure team owns.
- Excluded:
  - unscheduled downtime caused by the customer, such as an application crash;
  - reboots by the VM owner, after a software install or to fix a problem. Windows does not fully trap this event, so tracking it is hard;
  - work inside the scheduled downtime: Guest OS upgrade, patch reboot, VMware Tools and VM hardware upgrade.
- The cause of a downtime takes time to find, so the metric must be recalculable after the month.
- Recovery time counts: Windows or Linux may boot in 1 minute and then run fsck before the application can start. That time is downtime.
- Two metrics, because vendors exclude scheduled downtime and can claim 99.999% while users see less:
  - Actual Availability (%): down is down, whatever the time, owner or cause. Easy to measure.
  - Operational Availability (%): excludes scheduled downtime and customer-caused downtime. Harder to measure. The SLA uses it.
  - Scheduled downtime is downtime inside the green zone: the change window (also maintenance window, authorized execution window), the agreed time when approved changes, deployments, patches and infrastructure changes may enter production. Downtime outside it counts, even when planned.

```text
Actual Availability (%)      = (minutes in month - all downtime minutes) / minutes in month × 100
Operational Availability (%) = (minutes in month - downtime minutes counted by the SLA) / minutes in month × 100
```
- Example: weekly patch window Sunday 00:00-02:00. In June (30 days, 720 hours) a database VM is patched 3 times inside the window: each time the Guest OS is down 15 minutes and the database takes 45 minutes to be fully restored.
  - Operational Availability: 100%. All three are inside the scheduled window.
  - IaaS Actual Availability counts the Guest OS only: 3 × 15 = 45 minutes, 99.90%. This is the value of the Availability SLA.
  - Counting until the database is restored gives 3 × 60 minutes = 3 hours, 717 / 720 = 99.58%. That is the application owner's view, outside the IaaS SLA: database recovery is the application layer, like application start-up. It belongs to the application team's KAI or an application SLA.
  - Actual and Operational Availability share one scope, the Guest OS answering; they differ only in which downtime counts.
- Example on a 10-host cluster with 1 HA host (usable 9 hosts). Actual Availability counts running hosts against all hosts; Operational Availability counts them against usable hosts, capped at 100%. DPM is intentional and desired: it lowers total capacity, not availability. Maintenance mode is intentional but not desired: it lowers usable capacity ([`sp5-framework/capacity/supply`](../capacity/supply.md), section Total vs usable after host loss).

| Hosts out | Event | Actual Availability | Operational Availability |
|---|---|---|---|
| 1 | DPM | 9/9 = 100% | 9/8 → 100% (capped) |
| 1 | Maintenance mode | 9/10 = 90% | 9/9 = 100% |
| 2 | DPM | 8/8 = 100% | 8/7 → 100% (capped) |
| 2 | Maintenance mode | 8/10 = 80% | 8/9 = 89% |

- Supporting offers that justify a higher class: application-level backup and self-service file restore; application-level HA monitoring, boot order, VM-host affinity; lower RPO and RTO with a yearly real DR test; longer and larger snapshots; patch deferral and custom patch sets; deferral of VMware Tools and VM hardware updates.

## Compliance SLA
- Percentage of compliance against an agreed security policy or benchmark.
- Compliance is binary: compliant or not.
- The SLA is a formal contract between two entities: do not put 100% in it; the contract value is 99.95%. The internal KSI is 100%: a non-compliant setting can be a door for an attack.
- The maintenance window is always excluded from the SLA: it is an agreed period of change.
- Calculated from the infrastructure team's point of view.
- Included:
  - internal standards, usually adapted from VMware best practices and security hardening guides;
  - regulatory benchmarks: CIS, ISO, DISA, FISMA, PCI DSS, HIPAA. VCF Operations manages vSphere compliance against these and custom benchmarks;
  - the VM's surroundings: if its ESXi host, vSAN, distributed switch or storage is not secure, the VM's score reflects it.
- Excluded: what the provider does not control.
  - Guest OS in the service: compliance is managed in the guest (Group Policy, configuration management, security agents), and availability is measured by Guest OS ping.
  - Guest OS not in the service: no guest compliance, and availability is measured by VM power state.

## Service SLA
- IaaS is commodity hardware sold as a utility; the class of service is where providers differ.
- Provisioning time: matters where churn is high. Define provisioned: a bare OS, or the application and database loaded.
- Provisioning success: complex multi-tier applications with many VMs and integrations fail from time to time.
- Support: response time and escalation path. Do not promise resolution time unless it is fully in your control. Example: Gold alerted by email and messaging within 10 minutes.
- Technical account manager: one contact who represents the customer inside the provider.
- Monitoring: Gold VMs monitored proactively, not only by alerts; Gold sees lower-level metrics (vMotion stun time, VMkernel latency); self-service monitoring portal where customers can start their own scheduled downtime.
- Leave out metrics that serve no business purpose. Portal availability is one: the provider's office is open 24 x 7 x 365.

## Time window
- The SLA is monthly, on the calendar month.
- Yearly: customers reject it; a year allows long outages. Daily: providers reject it; no room for error.
- Allowable downtime per period:

| SLA | 1 week | 1 month | 1 quarter | 1 year |
|---|---|---|---|---|
| 99.999% | 0.1 min | 0.4 min | 1.3 min | 5.3 min |
| 99.99% | 1.0 min | 4.3 min | 13.1 min | 52.6 min |
| 99.95% | 5.0 min | 21.6 min | 65.5 min | 263.0 min |
| 99.9% | 10.1 min | 43.2 min | 131.0 min | 526.0 min |

- 99.999% a year (5.3 min) allows more downtime than 99.95% a week (5.0 min).
- Each extra nine shrinks the window 10x and can call for a different architecture: 99.99% leaves 4.0-4.5 minutes a month to detect and remediate.
- Window by month length:

| SLA | Relative window | 28-day month | 30-day month | 31-day month |
|---|---|---|---|---|
| 99.999% | 1x | 0.4 min | 0.4 min | 0.4 min |
| 99.995% | 5x | 2.0 min | 2.2 min | 2.2 min |
| 99.990% | 10x | 4.0 min | 4.3 min | 4.5 min |
| 99.950% | 50x | 20.2 min | 21.6 min | 22.3 min |
| 99.900% | 100x | 40.3 min | 43.2 min | 44.6 min |

## Promise and reality
- Promise: what is sold. Several numbers, one per class of service: a higher price buys a higher SLA.
- Reality: what is delivered, calculated at month end. One number per VM, whatever its class. A Gold VM can fail its SLA while a Bronze VM passes.

## Same benchmark for every class
- Every class is measured against the same benchmark; the classes differ in how often they may miss it.
  - Availability: against no downtime.
  - Compliance: against perfect compliance.
  - Service: against the best possible service.
- A different benchmark per class cannot be explained by price, and lets a lower class score better than a higher one. Numbers per class: [`sp5-framework/concepts/class-of-service`](class-of-service.md).

## Misconceptions
- "Our SLA is Cluster Availability 99.95%" → wrong object. The application team cares about its own VMs and pods; a cluster can be up while their VM is down. Measure the consumer's object.
- "Our Kubernetes SLA is node availability" → the node is often the SRE team's object; developers own the pod.
- "We have a performance SLA" → ask for the metric, object, target and window. Usually there is none, or the metric is wrong. Operations use the KPI.
- "Track an SLI or SLO for performance" → neither is used. The KPI covers performance; the SLA is the contract.
- "Alert on the SLA" → alerts are based on the KPI. The SLA is monthly and lagging.
- "Write 100% compliance into the contract" → the SLA is 99.95%; 100% is the internal KSI.
- "Our availability SLA is 99.999%, so users had 5 minutes of downtime a year" → the SLA excludes scheduled and customer-caused downtime. Actual Availability counts everything and is lower.
- "Application start-up after a reboot counts against the IaaS availability SLA" → IaaS uptime covers the Guest OS answering ping. fsck counts; application loading does not.
- "A yearly SLA is easier on the customer" → a yearly window allows the longest single outage; 99.999% a year is more downtime than 99.95% a week.
- "vCenter and NSX Edge get the same SLA as customer VMs" → they are internal: KPI and KAI only. An SLA needs two parties.

## Metadata
```yaml
id: sp5-framework/concepts/sla-metrics
retriever_guide: how-it-works
scope: sp5-framework
technology:
- system
pillar:
- availability
- compliance
product:
- vsphere
- vcf-operations
- windows
- linux
object:
- VirtualMachine
internal_derive:
- sp5-framework/performance/kpi-vs-sla
related:
- sp5-framework/capacity/supply
- sp5-framework/concepts/class-of-service
- sp5-framework/concepts/iaas-business
- vsphere/architecture/vm-vs-guest-os
- sp5-framework/observability/thresholds
images: []
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Your Private Cloud > Service Level Agreement (The 4 SLAs of IaaS, VM vs Guest OS, Availability SLA, Performance SLA, Compliance SLA, Service SLA, The Metrics of SLAs, The Time Window, The 2 Sides of an SLA, SLA Calculation, Performance Quantification, Penalty Quantification, The Benchmark to Rule Them All)'
corrections:
- 'Performance SLA, SLI and SLO removed (2026-11-11): the SLA is a business contract; performance is managed by the KPI only. The book''s Performance SLA, SLA calculation and Performance Quantification sections are not used.'
review_notes:
- 'To check: Section ''Availability SLA'', Operational Availability formula: derived from the definition; the book has a Formula heading with no formula.'
- 'Section ''Time window'': tables transcribed from the book images. The book table has 99.95% quarter 65.5 min (91-day quarter) and year 263.0 min (rounded); kept as the book gives them.'
status: draft
```
