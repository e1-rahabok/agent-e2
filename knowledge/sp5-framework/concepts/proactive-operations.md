# Proactive operations

## Day 0, 1 and 2 owners
- Day 0 (plan) and Day 1 (design and build) belong to the architecture team; Day 2 (operate) to the operations team.
- In a large estate Day 1 never stops. 6,000 ESXi hosts on a 5-year depreciation means about 100 hosts replaced a month, 25 a week.
- Pillars per phase:

| Phase | Yes | Partial | Not applicable |
|---|---|---|---|
| Day 0: planning | All five | - | - |
| Day 1: design and build | Availability, performance, compliance, capacity | Cost | - |
| Day 2: monitoring | All five | - | - |
| Day 2: troubleshooting | Availability, performance | - | Security (forensic investigation), compliance (drift against the desired configuration), capacity, cost |
| Day 2: optimizing | Performance, capacity, cost | Availability | Compliance |

- A major technology upgrade needs planning and redesign: the cycle starts again.

## Dual track: proactive and reactive
- Two processes: reactive and proactive.
- Reactive: starts from a complaint or an alert. A manual process for three types of problem, each with its own order of checks, the what before the why:
  - Down: log, saturation, configuration, known bug.
  - Slow: contention, consumption, configuration, known bug, log. Read the KPI.
  - Breached (compromised): configuration, known bug, log.
- Down and slow are troubleshooting. Breached is a forensic investigation, not troubleshooting.
- The three orders are the same as the availability, performance and security steps of the health check: reactive enters one pillar directly; proactive walks all four.
- Proactive: the health check (its four questions in order: availability, performance, security, capacity). It is a superset of reactive, because nobody knows yet whether there is a problem.
  - Daily: a morning health check of configuration and state, with remediation by rules IT sets; important but not urgent symptoms, reviewed top down by someone who knows the environment.
  - Weekly: deeper analysis over a longer data range.
  - Monthly: overall performance analysis and baselining, covering consumer and provider.
- Proactive findings go to a human expert, who decides the remediation; reactive findings go straight to remediation. Remediation examples: vMotion a VM, reboot Windows, restart a pod.
- Known bugs are mostly configuration issues: an older version or incompatible settings.
- Anomaly detection by mathematics alone gives false positives: it lacks the real-world business context. What looks abnormal can be normal, and the reverse (a month-end batch, a planned migration).
![Reactive: complaint or alert → manual process: Down (log → saturation → configuration → known bug), Slow (contention → consumption → configuration → known bug → log), Breached (configuration → known bug → log) → remediation. Proactive: Daily (morning health check of configuration and state with rule-based remediation; important-but-not-urgent symptoms reviewed top down), Weekly (deeper analysis across longer data), Monthly (overall performance analysis and baselining of consumer and provider) → human expert → remediation](images/reactive-vs-proactive-operations-dual-track-diagram.png)
- Troubleshooting cannot be eliminated; regular health checks with automatic remediation reduce it.
- The checks must cover every manual check done today: automate the whole checklist.
- The rules are finite and known: the logic experts use to troubleshoot performance can be automated. Most remediation is moving VMs out of a cluster, which needs no AI and can be automated too.
- Daily check plus remediation, verified by a human, leaves the team free for corner cases.
- The check is short, a few minutes when there is no problem, so it runs twice a day: start and end of the day. A problem it finds turns into troubleshooting, which takes as long as the problem needs.

## Day-to-day order
1. Availability: a system that is down has no performance problem.
2. Performance: a system so slow it is as good as down.
3. Security: third, not first, in day-to-day operations.
4. Capacity: will it be enough; efficiency is read here.
- Configuration is checked as a drill-down under each of the four: a configuration issue can cause any of them.
- Assess all four on both sides of VCF, platform and product ([`sp5-framework/concepts/purpose-driven-architecture`](purpose-driven-architecture.md)).

## A 24-hour day
- Alerts arrive at random times, day and night: reactive.
- Proactive work:
  - NOC live screen: always on;
  - daily check at 09:00: about 5 minutes when there is no problem; a problem found makes it longer, as long as that problem needs;
  - weekly check: about 1 hour;
  - monthly review: about 1 day.
![00:00-24:00 timeline. Reactive: alerts at random times. Proactive: NOC live screen always on; daily check at 09:00 (the image says 10 minutes; it takes about 5 minutes when there is no problem); weekly check (1 hour); monthly review (1 day)](images/operations-24-hour-reactive-vs-proactive-timeline.png)
- Morning sequence:
  - 08:00-09:00: an automatic health optimization script runs and flags VCF components it cannot remediate.
  - 09:00-09:30: a human expert reviews the script outcome and the daily dashboard, including the alert trend.
  - 09:30-10:00: the team prepares the environment for the day's expected load, for example by approving rebalancing between clusters.
- Cadence by item: critical business applications twice daily (minimum), tracked by both the application and infrastructure teams; daily check twice daily; NOC screens now; log analysis daily; alerts as they come.
- Week-to-year: deep analysis and long-term planning by the Level 2 team, covering capacity, performance and configuration.

## NOC live screen and daily check
- Live screen: real-time data on the NOC wall, always on, auto-refreshing. With clear SOPs it gives Level 1 fewer, better escalations. It covers the hours after the morning check.
- Daily check: insight, not alerts. Insight and alerts complement each other: open both pages side by side.
- Both complement alerts. An alert is bottom up and shows only the tip of the iceberg.
- Real-time screen per pillar (minutes, so capacity rarely matters):
  - availability: undesirable events that do not match what is happening. Many VMs deleted while no deletion is planned means something is wrong;
  - performance: overall performance; check that fluctuation stays within expectation;
  - security: suspicious activity such as firewall rules loosened or administrator accounts used.
- The aim is early warning before any alert fires, to buy time.

## Alerts as guard rails
- An alert is a guard rail: it catches what humans forget and failures that give no warning.
- Operations does not start from alerts. Well-run operations have few alerts.
- Too many alerts overwhelm; too few give no early warning. Insight leads; alerts play a secondary role.
- Proactive operations reduce alerts in count and intensity. Most alerts are yellow (lower threshold); insight from the daily health check replaces them.
- Weekly, review the alerts that slipped through the daily check and NOC screens, and improve the dashboards. Repeated over months, fewer alerts slip through.
- Colours and urgency: [`sp5-framework/outputs/alerts-and-insights`](../outputs/alerts-and-insights.md).

## Deeper analysis
- Daily check and NOC screens cover at most one day. A quarterly workload pattern is invisible to them.
- Major improvements need monthly or longer analysis with interactive dashboards, such as performance baseline profiling. It has time to run and suits larger, complex and political problems.

## Daily SOP per pillar
- The daily SOP looks ahead, using history and business context.
- Availability:
  - soft errors, which usually need each vendor's logs (vSphere Proactive HA reads hardware health);
  - backups done. Example: snapshots taken on 1,549 VMs and removed on 1,518 means 31 backups likely failed to consolidate their snapshot.
- Performance: insight analysis over the environment; mission-critical VM performance for the next day, from the pattern of the last week and the expected load agreed with the business owner.
- Compliance: non-compliance remediated.
- Security: signs of attack, such as firewall rules loosened or administrator accounts used.
- Configuration: misconfigurations that can cause issues; urgent patches after validation.
- Capacity:
  - VM provisioning, ideally automated through the day; check that the aggregate load does not overwhelm the shared environment;
  - snapshot deletion by policy: older than one day, with agreed exclusions honoured;
  - powered-off VMs deleted once past the powered-off definition, without waiting another week (backups exist);
  - idle VMs shut down gracefully once past the idle definition.

## Optimization
- Monitoring that finds nothing to fix can still find something to improve.
- Lower cost: reclaim orphaned, powered-off, idle and oversized VMs and snapshots; a smaller data-centre footprint saves software, hardware, rack space, cooling and UPS; move burst capacity from owned to on-demand.
- Better performance: profiling with real baselines; a performance KPI beside the availability SLA; NOC dashboards (insight, then alerts); self-service with approval workflows.
- Lower complexity: standard architecture; simpler business and security policy; SOPs; automation against human error; replace ageing hardware and outdated software.
- Customer satisfaction: reputation with application teams (internal IT); repeat business (service provider); price/performance that justifies the price.
- Compliance: internal and industry benchmarks such as VMware hardening guides, CIS, ISO, FISMA, DISA, PCI DSS, HIPAA.

## VM life cycle
- Back each stage with an approval system: every change request and action recorded, which ends finger-pointing and supports audit (who changed which object, when).
- Request: if the VM is free, business justification and IT policy decide; the policy sets the criteria per class. The application team requests the size, approved by its management; IT reviews above a size or count threshold.
- Creation: deployment in vCenter, ideally automated. It sets the VM name, creates folders and places the VM in the right one. Once VCF Operations registers the VM, add it to custom groups and set custom properties.
- Changes: size changes need approval, because they affect capacity and performance. Update shares and reservations to match.
- Retire: delete the VM and remove it from inventory.

## Misconceptions
- "Proactive operations means proactive alerts" → reacting to an alert is reactive. Proactive is the scheduled health check, insight, modelling and baselining.
- "An anomaly is a problem" → anomaly detection lacks business context: what looks abnormal can be normal, and the reverse.
- "Troubleshooting automation needs AI" → the rules are finite and the usual remediation is moving VMs out of a cluster; rules and automation do it.
- "The morning check covers the whole day" → the NOC live screen covers the rest of the day; the weekly review catches what both missed.
- "The daily check takes 10 minutes" → about 5 minutes when there is no problem; a problem found makes it longer, as long as the problem needs.
- "The daily check shows every problem" → it covers at most a day; quarterly patterns need monthly baselining.
- "Security comes first in daily operations" → availability, then performance, then security.
- "A snapshot count that differs from the VM count is cosmetic" → snapshots taken but not removed point to failed backup consolidation.
- "Wait a week before deleting powered-off VMs" → once past the definition, delete; backups exist.
- "Day 1 is a project phase that ends" → at thousands of hosts, hardware replacement runs every week.
- "Capacity belongs on the NOC live screen" → live screens span minutes; capacity is a daily and long-term view.

## Metadata
```yaml
id: sp5-framework/concepts/proactive-operations
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
product:
- vsphere
- vcf-operations
- kubernetes
- windows
object:
- VirtualMachine
- ClusterComputeResource
- HostSystem
internal_derive:
- sp5-framework/outputs/alerts-and-insights
- sp5-framework/concepts/monitoring-vs-troubleshooting
- sp5-framework/concepts/purpose-driven-architecture
related:
- sp5-framework/concepts/overview
- sp5-framework/concepts/health-risk-efficiency
- sp5-framework/capacity/rightsizing
- vsphere/technology/storage/concepts/snapshot-impact
images:
  - path: images/reactive-vs-proactive-operations-dual-track-diagram.png
    product: [vsphere, vcf-operations, kubernetes]
    object: [VirtualMachine]
    topic: 'Reactive manual track vs proactive automated, insight, modelling and baselining track'
    image_type: diagram
  - path: images/operations-24-hour-reactive-vs-proactive-timeline.png
    product: [vcf-operations]
    object: [ClusterComputeResource]
    topic: 'Alerts, NOC live screen, daily, weekly and monthly checks over 24 hours'
    image_type: timeline
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Your Private Cloud > SP5 Framework: Process (Proactive Operations, Day-to-day Operations, Real Time, Daily, Optimize, VM Life Cycle); SP5 Framework: Pillars (pillar per phase table)'
corrections:
- 'Daily SOP per pillar, Capacity: snapshots older than one day; the book example said 3 days.'
- 'Daily check length: about 5 minutes when there is no problem; a problem makes it longer.'
- 'Sections ''Dual track'' and ''Day-to-day order'': reactive starts after an alert, an incident or a complaint; proactive is insight, typically anomaly detection, which gives false positives without business context; configuration is a drill-down; known bugs are configuration. The example in brackets (month-end batch, planned migration) is not from the source.'
review_notes:
- 'Section ''NOC live screen and daily check'': the book says insight and alerts were covered in Part 1; this is Part 1.'
- 'Section ''Daily SOP per pillar'', 31 backups: subtraction (1,549 - 1,518).'
- 'To check: Section ''Daily SOP per pillar'', Proactive HA reading hardware health: vSphere Proactive HA uses hardware vendor health providers; not in the book.'
- 'Not copied: day-to-day operations cadence image (text in A 24-hour day), day-to-day order image (text in Day-to-day order).'
status: draft
```
