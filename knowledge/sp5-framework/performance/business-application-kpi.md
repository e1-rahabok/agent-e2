# Business application KPI

## Why the infrastructure layer measures it
- A Level 300 view: the business application is the application team's job, measured by transaction monitoring; the infrastructure team measures VMs, hosts and clusters. That leaves the most important question unanswered.
- The question the infrastructure team must answer is per application: is the infrastructure serving application X? A business owner complains about internet banking, not about a cluster.
- Troubleshooting eliminates layers (`sp5-framework/concepts/realms-and-layers`). Each layer needs a KPI for the application, so the infrastructure layer needs the infrastructure slice of the application, not only a cluster KPI.
- Infrastructure metrics are horizontal: one KPI works for every application, with no agent and no per-software design. Transaction monitoring covers few applications and is built per application.
- vSphere objects do not map to applications. An application spans tiers, VMs, pods and clusters; a cluster serves many applications.
- Business leaders read IT by application: `sp5-framework/outputs/it-leaders-dashboards`.

## Crown jewels
- Crown jewels: the critical business applications, strategic to the core business. They contribute directly to revenue, to reputation, or both. A small share of the VMs.
- Examples: an airline's ticketing and frequent flyer systems; a bank's internet banking and core banking; an online retailer's portal.
- Check them several times a day, at least twice. The application team watches its system all day; a morning check is too late (`sp5-framework/concepts/proactive-operations`).
- The question is whether the infrastructure causes the application's problem. Usually performance; sometimes availability or security.
- They always run in the Gold class of service (`sp5-framework/concepts/class-of-service`).

## How the KPI is built
- Structure: application → tiers (web, application, database; or microservices, one pod set per function) → members (VMs, pods). In VCF Operations: `vcf-operations/dashboards/business-applications`.
- Member: its own KPI, VM Performance (%) for a VM (`vsphere/object-types/vm/kpis/vm-performance`).
- Tier: the average of its members. Members serve requests in parallel behind a load balancer, so one slow member slows only its share; a good load balancer spreads both load and failures.
- Spare members (4 or 5 web servers where 3 carry the load):
  - availability: count the spare; one member down does not reduce tier availability while the others carry the load;
  - performance: average all members, spare included; each serves its share of requests.
- Active and passive members (a database cluster): performance counts the active node only. The passive node serves no requests, so its good score would pull the tier up and hide a slow active node.
- Application: the worst of its tiers. Tiers work in sequence, like a convoy: a request passes web, application and database, so the slowest tier sets the pace.

## Not yet in VCF Operations
- VCF Operations cannot tell an active node from a passive one, so it averages both. Until it can, read the active node alone, or exclude the passive node from the tier by hand.

## Misconceptions
- "Business applications are the application team's job; infrastructure measures clusters" → the infrastructure layer must prove, per application, that it serves it. A cluster KPI cannot say that.
- "The tier is as slow as its worst VM" → members work in parallel; the tier is the average. The worst rule applies across tiers, not inside one.
- "Average the tiers into one application score" → tiers are in sequence; one slow tier makes the application slow. Take the worst tier.
- "The database tier is healthy: the average of both nodes is green" → the passive node serves nothing and is idle; count the active node only.
- "Transaction monitoring covers it" → it covers few applications and has no infrastructure context; the infrastructure KPI works for all of them.

## Metadata
```yaml
id: sp5-framework/performance/business-application-kpi
retriever_guide: how-it-works
scope: sp5-framework
technology:
- system
pillar:
- performance
- availability
product:
- vsphere
- vcf-operations
- kubernetes
object:
- VirtualMachine
internal_derive:
- sp5-framework/concepts/realms-and-layers
- vsphere/object-types/vm/kpis/vm-performance
related:
- sp5-framework/concepts/purpose-driven-architecture
- sp5-framework/performance/kpi-vs-sla
- sp5-framework/concepts/proactive-operations
- sp5-framework/concepts/class-of-service
- vcf-operations/dashboards/business-applications
- sp5-framework/outputs/it-leaders-dashboards
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download); Knowledge base
  path: 'Your Private Cloud > Purpose-Driven Architecture > Begin with The End in Mind: The Crown Jewel'
corrections:
- 'Section ''How the KPI is built'': across tiers the application takes the worst tier; active/passive counts the active node only.'
- 'Section ''Not yet in VCF Operations'': VCF Operations cannot tell active from passive.'
- 'Section ''Why the infrastructure layer measures it'': not measuring business applications at the infrastructure layer is a Level 300 mistake.'
review_notes:
- 'To check: Section ''How the KPI is built'': the reasons (the passive node pulls the average up; the convoy) and the workaround (read the active node, exclude the passive by hand); not in the source.'
status: draft
```
