# Purpose-driven architecture

## Goals come from what is sold
- Architecture goals are business results, as seen by whoever pays for the platform and whoever pays for the service. Availability and performance practice come after.
- The goals depend on what is sold: an application or infrastructure.
- **SaaS**: no on-premises install. ISVs use it so customers do not run outdated versions.
- **DBaaS**: two variants.
  - Shared binary: one patch updates every instance; all share one maintenance window.
  - Dedicated binary: each customer has its own version, patch level and downtime schedule.
- **PaaS**: common services for business applications (login, payment).
- **DaaS**: desktops at a low price per user.
  - All desktops run the same software, so one software change hits every desktop at once. A 10% CPU increase in the browser, on a heavily overcommitted host, can breach the Performance SLA. Application teams must be involved.
- **K8aaS**: Kubernetes, on a dedicated or a shared cluster.
- **IaaS**: three variants (VM, resource pool, hardware): `sp5-framework/concepts/iaas-business`.

## Plan from Day 2
- Day 0: plan. Business plan, high-level architecture, operations model.
- Day 1: design and build. Low-level architecture, deployment, commissioning.
- Day 2: operate. It starts at go-live and lasts the life of the platform.
- Think in the order Day 2, Day 0, Day 1. How the platform will be sold and operated decides the plan, and the plan decides the architecture.
- A major upgrade or migration starts the cycle again from Day 2.
![Day 2 Operate → Day 0 Plan (high-level architecture and operations model) → Day 1 Design (low-level architecture and deployment); a major upgrade or migration loops back to Day 2](images/day2-day0-day1-sequence-diagram.png)
- Example 1: the class of service and the average VM profile fix the ESXi host specification (`sp5-framework/capacity/host-spec-from-class-of-service`).
- Example 2: business continuity caps cluster size.
  - Policy: one cluster failure may affect at most N production VMs. Book example: 300.
  - Size the cluster so its VMs stay under N. A larger cluster cannot be filled without breaking the policy.
  - Seen in the field: 32-node production clusters running 1,000-2,000 VMs.
  - Gold adds availability zones, because it hosts mission-critical services.

## Reflect the business in the platform
- The infrastructure team must know which business application each object serves, and what its failure costs.
- CIO view: live information on how IT serves each business unit and its critical applications. The platform must map business units and applications to their VMs.
- Tenant view: customers check their own VM health and how the platform serves their VMs. The platform must associate each tenant with its VMs; at least a structure to browse or find applications and VMs.
- One model fits every application: the infrastructure metrics are the same for all of them (`sp5-framework/concepts/realms-and-layers`).

## Crown jewels
- Mission-critical business applications: a small share of the VMs, essential to revenue, profit or image. Bank: internet banking. E-commerce: the online portal.
- Check them several times a day. The application team watches its system all day; a morning check is too late.
- The question to answer is whether the infrastructure causes the application's problem. Usually performance; sometimes availability or security.

## Health of an application tier
- A tier scales out: web and application servers behind load balancers; microservices as pods per function (payments, shipping).
- Tier health is the average of its members, not the worst one. Members serve requests in parallel, so one slow member slows only its share. A good load balancer spreads both load and failures.
- Spare members (4 or 5 web servers where 3 carry the load):
  - Availability: count the spare. One member down does not reduce tier availability while the remaining members carry the load.
  - Performance: average all members, spare included. Every member serves requests, so a slow one slows its share of them.

## Automation after operations
- Design only what the team can troubleshoot. Problems show on Day 2, under revenue workload.
- Plan the roles and skills that will run the platform. Each component needs monitoring and a definition of healthy.
- Automation is a feature of the design, like fly-by-wire in a plane; operations is flying the passengers safely and on time.
- Automate only what is already operated well. Automating an ungoverned process repeats its mistakes faster. Automation comes last.
- Maturity: reactive and manual (remediating issues not seen coming) → predictive and proactive (the system warns, fewer alerts, more insights) → intelligent and automated (the system is trusted to fix; the team works on improvement).

## Two sides of VCF
- VCF is a software-defined data center: software on commodity hardware that builds an on-premises private cloud.
- Platform side: VCF as the customer's IaaS. The application team cares about it.
- Product side: VCF as a Broadcom software product. The infrastructure team cares about it. Two forms:
  - virtual appliances: vCenter, NSX Edge;
  - kernel software: ESXi VMkernel, vSAN and NSX kernel modules.
- VCF appliances (vCenter, NSX Edge) and other infrastructure appliances are workload in the technical sense: VMs on a vSphere cluster.
- Operationally they are not workload: no business user owns them; the infrastructure team does. They are internal, so they have a KPI and no SLA. An SLA is always between two parties.
- Product-side work: compatibility, patch and upgrade; configuration maximums; templates; users and roles; certificates; licenses; log analysis.
- Pillars across both sides: availability, performance, security, compliance, capacity, configuration, inventory.
- The two sides depend on each other and are managed together. Example: an expired vCenter certificate (product) stops vCenter; DRS stops balancing while vCenter is down, so VM contention can rise (platform). vSphere HA keeps working without vCenter.
![Platform (VCF as an IaaS platform of the customer): workloads (business; IT, VCF and non-VCF appliances) above the virtual infrastructure. Product (VCF as a software product of Broadcom): compatibility, patch, upgrade, configuration maximums, template, users and roles, certificate, license, log analysis. A dependency arrow joins them; pillars across: availability, performance, security, compliance, capacity, configuration, inventory](images/vcf-platform-vs-product-pillars-diagram.png)
- Two layers: consumer and provider.
  - Consumer: where VMs and containers run. Three sublayers: application, Guest OS, VM.
  - Provider: the virtualized platform: compute, storage, network.
- VCF scope ends at the VM (virtual motherboard and BIOS) and VMware Tools. The Guest OS is largely outside VCF's influence (`vsphere/architecture/vm-vs-guest-os`).

## Traps
- "Plan first, then design, then work out how to operate it" → Day 2 drives Day 0, which drives Day 1. The class of service and the operations model fix the hardware and cluster design.
- "Automate first; automation is the transformation" → automation is a feature of the architecture. Automating operations that are not governed speeds up the problem.
- "Tier health is the worst member" → work in a tier runs in parallel; tier health is the average of its members.
- "Tier performance can leave out the spare node, since N+1 covers it" → the spare counts for availability only. For performance every member serves requests and is averaged.
- "A larger cluster is always more efficient" → a cap on VMs affected by one cluster failure caps the cluster size.
- "The application team needs the latest VCF version" → the VCF version is a product-side decision. The application team sees the platform side: its VMs and their service level.
- "vCenter and NSX Edge VMs get the same SLA as customer VMs" → they are internal: KPI only. An SLA needs two parties.
- "VCF is responsible for the Guest OS" → VCF scope ends at the VM and VMware Tools.
- "vCenter certificates are an infrastructure matter with no effect on VMs" → product-side failures reach the platform side: without vCenter, DRS stops balancing.

## Metadata
```yaml
id: sp5-framework/concepts/purpose-driven-architecture
retriever_guide: how-it-works
scope: sp5-framework
technology:
- system
pillar:
- availability
- performance
- capacity
- compliance
product:
- vsphere
- vsan
- nsx
- vcf-operations
- kubernetes
object:
- VirtualMachine
- ClusterComputeResource
internal_derive:
- sp5-framework/concepts/iaas-business
related:
- sp5-framework/capacity/host-spec-from-class-of-service
- sp5-framework/alerts/alerts-and-insights
- sp5-framework/concepts/realms-and-layers
- vsphere/architecture/vm-vs-guest-os
- vsphere/object-types/cluster/concepts/drs-overview
images:
  - path: images/day2-day0-day1-sequence-diagram.png
    product: [vsphere]
    object: [HostSystem, ClusterComputeResource]
    topic: 'Day 2 (operate) drives Day 0 (plan), which drives Day 1 (design)'
    image_type: diagram
  - path: images/vcf-platform-vs-product-pillars-diagram.png
    product: [vsphere, vsan, nsx]
    object: [VirtualMachine, VCenterServer, HostSystem]
    topic: 'Two sides of VCF: IaaS platform of the customer and software product of Broadcom, across seven pillars'
    image_type: diagram
source:
  document: PART 1 - Concepts of Operations Management.docx
  path: 'Your Private Cloud > Purpose-Driven Architecture (Begin with The End in Mind: The Crown Jewel, Day 0 | Day 1 | Day 2; Automate | Operate; The 2 Sides of VCF) (pp. 11-22)'
corrections: []
review_notes:
- 'Section ''Two sides of VCF'': appliances are workload technically, internal operationally: KPI, no SLA (author, Q091, 2026-11-08).'
- 'Section ''Goals come from what is sold'', DaaS: reason (same software on every desktop moves together) added by Claude.'
- 'Section ''Day 2 → Day 0 → Day 1'', Example 2: the book does not say whether 32-node clusters with 1,000-2,000 VMs are a counter-example to the cap (Q087 d).'
- 'Section ''Health of an application tier'': the reason in the performance bullet (each member serves its share of requests) is Claude''s. Health across tiers (in sequence) and of an active/passive database tier: Q092.'
- 'Section ''Two sides of VCF'': the book text says workload means the customers'' VMs; its diagram lists IT appliances under Workloads (Q091). Pillar list differs from the pillar tag values (Q091).'
- 'Section ''Two sides of VCF'', certificate example (DRS needs vCenter, vSphere HA does not): Claude''s own knowledge, vSphere 9.1 availability documentation.'
- 'Not copied: the application tier diagram (three-tier vs microservices pods) and the maturity diagram; their content is in the text.'
status: draft
```
