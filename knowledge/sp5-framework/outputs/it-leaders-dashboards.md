# Dashboards for IT leaders

## Layers of management
- In a large organisation there are several layers between the operations team and the CIO, and each has its own needs. Find the need behind each request: the questions, the answers expected, the actions taken on them.
- Decide what you want from them as well: they hold budget and resources. Live data proves a hardware request, and shows where wastage is and how large.
- Show what supports the approval you need, without burying them in detail.

## General requirements
- Summary first:
  - the big picture, then drill-down;
  - the trend of the last few months, ideally with a projection, averaged so a 5-minute spike does not show;
  - exceptions that need their attention. Complete means nothing more can be taken out.
- Offline:
  - they prefer email, to read anywhere without logging in to VCF Operations;
  - they are mobile; some ask for one phone screen or one screenshot. Check the screen size: a 7-inch screen shows much less than a 14-inch one.
- Simple:
  - minimal interaction (clicks, zoom, sort); larger fonts; round numbers (significant figures);
  - one specific question per dashboard;
  - the 5-second test: understood in 5 seconds buys a few more minutes;
  - business terms, not IT terms: replace datastore or distributed switch with words the organisation uses;
  - few widgets and little scrolling.
- A self-service portal for them must be easy to reach and should not need a password: they forget it.

## Sample analysis: two layers
- Middle IT management (two named managers in the example):
  - read on their laptop; log in to VCF Operations only occasionally;
  - know the environment well;
  - focus: keeping the lights on; availability, performance, security;
  - authority: medium changes, with a budget limit.
- Senior IT leadership (three named leaders in the example):
  - expect a 15-minute live presentation and a PDF copy in their inbox;
  - need explanation;
  - focus: last month against plan and SLA, next month's plan; capacity and cost, lowering cost while adding capacity;
  - authority: strategic, long-term IT decisions; represent IT to business leaders.
- Approach that follows:

| Channel | Middle IT management | Senior IT leadership |
|---|---|---|
| Mobile | Daily, first thing; forward looking; 1 screen | Weekly on Monday; 1-week outlook; 1 screen |
| Desktop | Weekly; 2 pages, all read | Monthly; 4 pages, presented in the operations review |
| Other | Log in on demand for detail | A wall screen near their office; no interaction |

## Business applications report
- Likely the most important view for both sides: it proves the infrastructure does its part.
- A summary of all mission-critical business applications, grouped by business unit, since they are equally important.
- Fields:
  - Name: as the business calls it. Applications span tiers, VMs and Kubernetes pods, so build the structure in VCF Operations first ([`vcf-operations/dashboards/business-applications`](../../vcf-operations/dashboards/business-applications.md)).
  - Availability: average uptime in the period, as Actual Availability (%), not Operational Availability (%). End customers, often external, do not care about scheduled downtime, and most websites are expected up 24x7 all year ([`sp5-framework/concepts/sla-metrics`](../concepts/sla-metrics.md)).
  - Performance: average over the period. The average can hide poor moments, so they may ask for the worst too; with many applications, the average of all, possibly over time like a stock chart.
  - Compliance: configuration compliant with security and with the master template.
- An infrastructure-centric report is the other common request. A request for basic facts usually means they do not know the environment.

## Operations overview report
- Summarizes how operations went: was the week or month busy and volatile? Were availability and compliance within SLA, and performance within the KPI levels?
- Fields:
  - inventory: key items, absolute or relative; items added or removed; settings changed;
  - configuration: what they care about, or what you want them to see;
  - capacity: enough? If not, when to act? What changed?
  - performance: against the KPI.

## Sample dashboards in VCF Operations
- VCF Operations ships two sample dashboards for presenting live information to senior management: Inventory Summary and Capacity Summary. The operations team presents them; they are not for self-service.
- Capacity Summary as built (World summary, compute and storage heat maps, why network and World-level capacity remaining are left out): [`vcf-operations/dashboards/capacity-summary-dashboard`](../../vcf-operations/dashboards/capacity-summary-dashboard.md).

## Misconceptions
- "Executives want detail" → summary and trend first, exceptions only; drill-down on request.
- "One leadership dashboard fits all layers" → middle managers and senior leaders differ in channel, frequency, focus and authority.
- "Report Operational Availability to the business" → end customers count scheduled downtime too; report Actual Availability.
- "Use technical terms on executive dashboards" → use the organisation's business terms.

## Metadata
```yaml
id: sp5-framework/outputs/it-leaders-dashboards
retriever_guide: how-it-works
scope: sp5-framework
technology:
- system
pillar:
- availability
- performance
- security
- capacity
- value
product:
- vcf-operations
- vsphere
object:
- ClusterComputeResource
- Datastore
- VirtualMachine
internal_derive:
- sp5-framework/outputs/dashboard-design
- vcf-operations/dashboards/business-applications
related:
- sp5-framework/concepts/sla-metrics
- sp5-framework/outputs/capacity-dashboards
- sp5-framework/capacity/supply
- sp5-framework/outputs/system-engagement
- vcf-operations/dashboards/capacity-summary-dashboard
source:
  document: Knowledge base
  path: 'Overall Design Approach > Overall Design: IT Leaders Dashboard (General Requirements, Sample Requirements Analysis: Business Applications, Operations Overview; Sample Dashboards: Capacity Summary, How to Use, Points to Note)'
corrections: []
review_notes: []
status: draft
```
