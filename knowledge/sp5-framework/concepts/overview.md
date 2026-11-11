# SP5 framework

## SP5 framework

- A private cloud on VCF needs its own IT operations management framework. The SP5 Framework implements the IT private cloud business strategy using the five P: policy, pillars, process, people, platform.
- Strategy: an SLA-backed enterprise private cloud.
- Policy (business and IT) and process (Day 2 → Day 0 → Day 1) are set along one timeline with people (users, application teams, infrastructure team, leadership).
- Pillars: the disciplines a CIO cares about. People are organized around pillars; policies and processes. A full set of policies and SOPs answers who does what, when, where and how.
- Platform: the system architecture (compute, storage, network, security, management and portal), implemented with a product such as VCF.
  ![Business layer: Strategy (SLA-backed enterprise private cloud); Policy (business, IT), People (users, IT apps, IT infra, leadership), Process (Day 2 → Day 0 → Day 1) on one timeline. Operations layer: 5 pillars (availability, performance, compliance, capacity, cost + price) over inventory and configuration. Architecture layer: platform (management + portal; compute, storage, network; security)](images/sp5-framework-strategy-policy-pillars-process-people-platform-diagram.png)
- The SP5 Framework is documented in the book Private Cloud Management by Iwan Rahabok, free to download at https://isvara.io/download. Cite it by that title when a user asks where the framework comes from.
- Why a new framework instead of ITIL or COBIT: `sp5-framework/concepts/why-a-new-framework`.
- Metric types per pillar (contention, consumption, context): `sp5-framework/observability/triple-see-method`.
- Modelling a pillar into one number (KPI, risk): `sp5-framework/concepts/modelling`.
- Day 2 → Day 0 → Day 1: `sp5-framework/concepts/purpose-driven-architecture`, section Begin with the end in mind.

## What a private cloud manages

- Consumer side: tenants consume and pay for IaaS through a self-service portal and API: KPI and SLA reports, inventory, projects, troubleshooting, security, team, bill.
- Provider side:
  - IaaS management: the services above the platform (Kubernetes, database, desktop, private AI, VM), each managed by its persona (SRE, DBA, VDI team);
  - private cloud operations: day-to-day running (NOC live screen, alerts and symptoms, tasks, events, health check, KPI), operations management (availability, capacity, performance, cost and price, configuration, sustainability), inventory management (inventory, tags, groups, folders);
  - cloud platform management: VCF as a Broadcom product: identity (users, passwords, roles, single sign-on) and platform (licenses, certificates, life cycle, appliances);
  - security operations: threat, compliance, audit, events.
- Virtualization: the virtualization manager over servers, storage and network, integrated with hardware management (top-of-rack switches, racks, backup, arrays).
- Order of work: inventory first (visibility of thousands of related objects), then health of what is known, then risk (potential problems), then optimization.
- Acid test of operations management: the lead can take a long holiday with no escalation call for information or decisions only they hold.

## The five pillars

- Availability, performance, compliance, capacity, value. Each is a unit of management with its own discipline. The `pillar` tag of the knowledge base uses these five.
- Value management keeps three things apart: the cost of the infrastructure IT spends, the price IT charges each tenant (line of business), and the business value of the investment. The SP5 diagram labels the pillar Cost + Price.
- Inventory and configuration are not pillars: they sit under all five.
- Security is part of the platform (architecture layer), not a pillar.
- CIO order: availability first (a system that is down has neither a performance nor a security problem; nobody can log in to a vCenter that is down); then performance (so slow it is as good as down); then security and compliance (up and fast is not secure).
- The complexity of a pillar depends on the technology: vSAN capacity is more dynamic than a traditional SAN; a storage policy change can raise consumption at once.

## Relationships

- Symptom and root cause sit in different pillars: a performance problem can come from configuration (outdated settings, incompatible versions).
- Arrows mean impact:
  - Availability raises cost: extra resources with no capacity benefit.
  - Compliance raises cost: more requirements, more overhead to manage and measure them.
  - Cost and price drive capacity and performance.
  - Capacity → performance is non-linear: as capacity remaining falls, performance holds; below 0% it drops suddenly.
  - Availability impacts capacity: an availability problem, such as a host down, reduces the capacity available. The planned part (the HA host) is already taken out of usable capacity (`sp5-framework/capacity/supply`); an outage beyond the design takes more.
  - Availability impacts performance, above all when it is intermittent: an object flapping between on and off, or a cluster flapping between its passive and active nodes.
- A line without an arrow means a relationship without impact: inventory and configuration do not impact each other.
- Below the pillars: the pillars feed inventory, configuration and sustainability; configuration impacts sustainability.
- Security and compliance sit outside the core group: usually another department, with a scope beyond the data centre (building security, work-from-home).
  ![Capacity → Performance (red, non-linear); Cost & Price → Performance and → Capacity; Availability → Performance, → Capacity and → Cost & Price; Security + Compliance → Cost & Price. Below, fed by the pillars: Inventory — Configuration (no arrow); Configuration → Sustainability](images/pillars-of-operations-relationships-diagram.png)

## Availability

- Solutions span snapshots, backup, redundancy, fault tolerance, clustering and site recovery. Most consume resources (load balancers, replication), so they go into capacity planning; then they do not hurt performance.
- Include the load of a DR event in capacity planning.
- Two metrics: Actual Availability (%) ignores HA design and scheduled downtime; Operational Availability (%) accounts for them, is higher, and is the SLA number (`sp5-framework/concepts/sla-metrics`).
- Each extra nine shrinks the margin of error 10x. The book puts five nines at 10x the cost of four nines.

## Performance

- The most important pillar in day-to-day operations. With HA designed in, part of the system can be down with no impact on performance or capacity.
- Often confused with capacity: more work done is read as good performance. That reading makes idle look like poor performance.
- The primary metric is contention. No contention, no performance problem. A common cause of contention: utilization reaching capacity or a limit. Details: `sp5-framework/concepts/performance-vs-capacity`.
- Its boundary with the peer pillars, its two processes (monitoring with KPIs, troubleshooting), its KPIs and where each question is answered: `sp5-framework/performance/performance-management`.

## Capacity

- Quantity: is there enough supply for the demand to come? Its two stages (planning, running), its horizons (short term: stop provisioning; long term: buy hardware), its boundary with the peer pillars and where each question is answered: `sp5-framework/capacity/capacity-management`.
- Short-term capacity and performance depend on each other, which is why they are confused. A cluster that cannot serve its current demand is full, whatever its utilization: stop adding workload until the cause is known.
- How reservation, commitment, allocation, share and utilization feed the pillars:
  - share → contention (quality of service); utilization causes contention; contention → performance;
  - utilization → capacity; reservation and commitment → capacity; allocation → capacity only in plan;
  - allocation, reservation, commitment and share justify cost and price;
  - Reservation in the planning stage becomes share in the running stage.
    ![Inputs (share, reservation, commitment, contention, utilization, allocation) and what is managed (performance, capacity, cost & price): share → contention (QoS); utilization causes contention; contention → performance; utilization, reservation, commitment → capacity; allocation → capacity only in plan; allocation, reservation, commitment, share justify cost & price; reservation becomes share](images/share-reservation-commitment-allocation-to-performance-capacity-cost-diagram.png)

## Security and compliance

- The question "is it secure?" covers both. They differ in urgency and in nature:
  - Security management is operational, proactive and dynamic. It keeps the confidentiality, integrity and availability (the CIA triad) of hosts, storage fabrics and workloads against zero-day exploits, unauthorized access and runtime threats.
  - Compliance management is structural, declarative and driven by governance. It enforces verifiable configuration baselines against internal policy, industry benchmarks (CIS Benchmarks, VMware security configuration guides) and regulation (PCI DSS, MAS Technology Risk Management, ISO 27001).
- A security issue is more urgent: a non-compliant setting is being exploited, or it is exposed on a public network. That is present health.
- Not every non-compliant setting raises a security alert: that would flood the team. A non-compliant setting is risk (future health) until it is exploited or exposed.
- Security covers attacks, by insiders or outsiders: track malicious activity such as misuse of administrator accounts or denial of service.
- Compliance covers settings that expose loopholes or must meet a standard. It is close to configuration: you comply by controlling configuration values.
- Compliance is measured continuously, against internal and industry standards.
- Compliance is binary and unaffected by contention or performance. So the provider guarantees 100% compliance with its own benchmark for every class.
- Guarantee only what you manage: no Guest OS in the service, no Guest OS compliance and no SLA on it. With the Guest OS in the service, manage its configuration (for example with Active Directory Group Policy).

## Value: cost, price and business value

- Needed to become a real service provider.
- Price: hardware is a commodity and the price per VM is similar across providers; SLAs are the way to differentiate. Price must exceed cost but can be set independently of it. Discounts and progressive pricing set the terms and stop oversized VMs before production. Per VM, less overcommit (less contention) earns a higher price: price/performance.
- Cost: at platform level it moves with capacity. Higher utilization, lower cost per VM.
- Cost and capacity can move independently: a technology refresh adds capacity at the same cost; cheaper service rates cut cost with the same capacity.

## Non-pillars

- Inventory: what you have, where, and how it changes. A by-product: capacity and cost decisions shape it.
- Configuration: a means to an end. It matters only through security, capacity, performance and availability; it is both the cause of and the fix for problems in all of them.
- Sustainability: covered by capacity and cost. Only the power source is new; it is the same data from another angle.
- Reliability: a characteristic, not a discipline. Unstable performance or uptime is troubleshot as a performance or availability problem. Making it a pillar creates overlap.
- Recoverability: a property of availability. Debuggability: of performance and availability. Manageability: of configuration.

## Inventory vs configuration


| Item | Inventory | Configuration |
|---|---|---|
| What | An account of what is where: location, movement, count | Properties of the inventory; location is one property |
| Properties used | A small subset: counting objects | The full set, set by choice or accepted |
| Drift | Not relevant | Important |
| Movement | Important | Not relevant |
| Stocktake | Yes, physical or virtual | No |
| Goal | Distribution: keep it balanced (VMs per cluster) | Variance: keep it minimal (VM hardware versions) |

- Configuration maximum is in fact an inventory maximum.
- VMs in a cluster: inventory. ESXi hosts in a cluster: inventory, and configuration as well, because the host count is the cluster design; a deviation must be explained in the design document.
- High churn is an inventory problem: how many VMs were added, deleted and changed last month.
- Volume of change covers a longer period (5 minutes, 1 hour, 1 day); rate of change a shorter one (per second, per minute).
- Group inventory by function:
  - consumer layers: business application (spans pods or VMs), software (such as SQL Server), container or pod, VM (on premises or in a cloud);
  - provider layers: cloud services, Kubernetes, vSphere with vSAN and NSX, physical (network, arrays, servers, UPS, racks).

## Misconceptions
- "Availability and performance are separate, so an outage that HA covers has no performance cost" → flapping on and off, or between passive and active nodes, hurts performance.
- "Capacity is computed after HA, so availability cannot touch capacity" → an outage beyond the design reduces the capacity available.

- "Treat availability, performance and security as one health score" → they are separate pillars with separate metrics. Up is not fast; fast is not secure.
- "Utilization is low, so capacity is fine" → short-term capacity is full when current demand is not served. Stop provisioning until contention is explained.
- "More work done means better performance" → performance is contention. Idle is not poor performance.
- "Capacity remaining is falling, so performance is degrading now" → performance holds until capacity remaining passes 0%, then drops suddenly.
- "A host failure is a performance event" → with HA in the design, usable capacity already excludes the failover host.
- "Count HA spare as capacity" → availability and capacity do not overlap; capacity is calculated after availability.
- "Add hardware for the annual sale day" → burst, borrow hosts, or limit, power off or move other workloads for that day.
- "The infrastructure team should make developers shrink their VMs" → show the CFO the cost of waste; budget control makes the line of business optimize.
- "Compliance is lower in the cheaper class" → compliance is binary and guaranteed at 100% for every class.
- "Offer a compliance SLA for the Guest OS though the customer manages it" → guarantee only what you manage.
- "VM count per cluster is a configuration setting" → it is inventory. Configuration maximums are inventory maximums.
- "Reliability needs its own team and metrics" → it is a characteristic of performance and availability; a separate pillar overlaps them.
- "Sustainability is a sixth pillar" → it reads capacity and cost data from another angle.

## Metadata

```yaml
id: sp5-framework/concepts/overview
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
- vsan
- nsx
- vcf-operations
object:
- ClusterComputeResource
- VirtualMachine
- HostSystem
internal_derive:
- sp5-framework/concepts/sla-metrics
- sp5-framework/concepts/performance-vs-capacity
- sp5-framework/capacity/supply
related:
- sp5-framework/performance/performance-management
- sp5-framework/capacity/capacity-management
- sp5-framework/concepts/modelling
- sp5-framework/concepts/why-a-new-framework
- sp5-framework/observability/triple-see-method
- sp5-framework/concepts/purpose-driven-architecture
- sp5-framework/concepts/health-risk-efficiency
- sp5-framework/concepts/proactive-operations
- sp5-framework/concepts/class-of-service
- sp5-framework/observability/input-types
- vsphere/architecture/resource-controls
images:
  - path: images/sp5-framework-strategy-policy-pillars-process-people-platform-diagram.png
    product: [vsphere, vcf-operations]
    object: [ClusterComputeResource]
    topic: 'SP5 framework: strategy, policy, people, process, five pillars, platform'
    image_type: diagram
  - path: images/pillars-of-operations-relationships-diagram.png
    product: [vsphere]
    object: [ClusterComputeResource]
    topic: 'Relationships among the pillars of operations'
    image_type: diagram
  - path: images/share-reservation-commitment-allocation-to-performance-capacity-cost-diagram.png
    product: [vsphere]
    object: [ClusterComputeResource, VirtualMachine]
    topic: 'Share, reservation, commitment, allocation, utilization, contention as inputs to performance, capacity, cost and price'
    image_type: diagram
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Your Private Cloud > SP5 Framework (opening, capabilities); SP5 Framework: Pillars (Availability, Performance, Capacity, Reclamation, Compliance and Security, Cost and Price, Non-Pillars)'
corrections: []
review_notes:
- 'Section ''The five pillars'': pillar names differ between the SP5 diagram (compliance; cost + price) and the text (security and compliance; value).'
- 'Section ''What a private cloud manages'': text twin of the capabilities diagram (book p. 44), not copied: the text carries its content.'
- 'Section ''Availability'': five nines at 10x the cost of four nines is the book''s rule of thumb, not a measured figure.'
- 'Not copied: detailed pillar relationship diagram (p. 53), private cloud capabilities diagram.'
status: draft
```
