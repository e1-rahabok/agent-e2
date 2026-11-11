# Why SP5 and not ITIL

## Scope
- IT management frameworks exist: ITSM, IT4IT, ITIL, COBIT, Microsoft Operations Framework. eTOM and BIAN are domain-specific (telecom, banking) and do not suit VCF.
- SP5 covers Day 2 operations of a VCF private cloud only.

## Tickets
- The frameworks reflect ticket- and incident-based operations. A ticket as a unit of work is fine; most implementations disappoint users, though the help desk exists to help them.
- SP5 aims to remove tickets and incidents, not only reduce them.
- Proactive, insight-based operations require a small team of seasoned engineers with deep technical skill and knowledge of the business. They do not work with many teams across departments, each following rigid, siloed policies.

## Complexity
- ITIL 4 has 34 management practices: 17 service management, 3 technical management, 14 general management. With 34 practices, the team ends up managing the management.
- ITIL merges capacity and performance into one practice. In a VCF private cloud they are separate disciplines, with different personas and processes (`sp5-framework/concepts/performance-vs-capacity`).

## Terms that are not peers
| Pair in frameworks | SP5 reading |
|---|---|
| Monitoring and alerting | Alerting is one of three outputs of monitoring, with dashboards and reports |
| Changing vs optimizing | Optimizing is a kind of change |
| Operating vs supporting | Support is part of daily operations: inquiries, incidents, insights |
| Automation and orchestration | Orchestration is one technique of automation: it chains scripts |
| Measurement and reporting | Call it monitoring. Reporting is one output, with alerts and dashboards |
| Monitoring and event management | Monitoring is an activity, not a managed thing. An event is an input |
| Operations and governance | The same: operations are managed through governance |

- A monitoring result is one of three: troubleshoot (broken or wrong), optimize (not broken, but cost or performance can improve), or nothing to do.
- Events can be neutral or positive, unlike alerts. An event accounts for an activity, as a metric accounts for utilization or contention.
- Metrics, properties, events, logs and network flows are inputs, not things managed: their meaning comes from the pillar that reads them (`observability/input-types`).
- Governance covers risk (availability, capacity, security) and control (compliance with approved configuration, clear accountability per role, cost kept within budget).

## Practices that are not pillars
| Practice | Why not a pillar |
|---|---|
| Service level management | An SLA is a by-product of managing availability, performance and compliance |
| Service continuity | Part of the architecture: a living design that takes updates without breaking the SLA |
| Demand management | Part of capacity: just enough supply for demand |
| Continuity management | Part of availability: snapshots, HA, DR, replication, active/active, backup |
| Incident and problem management | Manage the impact (availability, performance) and reduce the causes, instead of accepting incidents and investing in managing them |
| Service request management, service desk | A technique designed in the monitoring strategy; the team is managed, but it is not a pillar |
| Continual improvement | A culture (Kaizen), realized as processes, policies and structures |

- Incidents (the website is down) come from problems (a rare bug in the core routers, incompatible configuration). Fewer availability, performance, compliance, configuration and capacity problems means fewer incidents.
- Pillars of SP5: `sp5-framework/concepts/overview`, section The five pillars.

## Misconceptions
- "Adopt ITIL capacity and performance management as one practice" → in VCF they are two disciplines with different teams, metrics and time frames.
- "Manage the SLA" → manage availability, performance and compliance; the SLA follows.
- "Alerting is a discipline next to monitoring" → alerts are one way monitoring talks to people, with dashboards and reports.
- "More tickets closed means better operations" → SP5 aims for fewer incidents, found as insights before they become tickets.

## Metadata
```yaml
id: sp5-framework/concepts/why-a-new-framework
retriever_guide: how-it-works
scope: sp5-framework
technology:
- system
pillar:
- availability
- performance
- compliance
- capacity
- value
product: []
internal_derive:
- sp5-framework/concepts/overview
related:
- sp5-framework/alerts/alerts-and-insights
- sp5-framework/concepts/monitoring-vs-troubleshooting
- observability/input-types
source:
  document: '"Why a New Framework?" (Word document, deleted after use)'
  path: Why a New Framework?; Complexity; Duplication; Clarity
corrections: []
review_notes:
- 'To check: Section ''Complexity'': the source says "ITIL 5 has 34 management practices" and links the ITIL 4 list. ITIL 4 has 34 practices; written as ITIL 4 (Q135).'
- 'Section ''Practices that are not pillars'': the source gives no reason for service request management and problem management in their own rows; grouped with service desk and incident management.'
status: draft
```
