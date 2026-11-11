# IaaS as a service

## System vs service
- VCF is the system the infrastructure team designs and buys (SDDC). IaaS is the service it sells to application teams.
- A system is judged by its architecture. A service is judged by its service level.
- It is a service with or without chargeback. VM owners no longer own the hardware, so they judge only the service level, not the architecture.
- The architecture is judged by its result in production: firefighting and blame between teams, or alerts that are meaningful and actionable.
- Moving from SDDC to IaaS is an operations change: complaint-based to KPI-based, alert-driven to insight-driven. The maturity steps: `sp5-framework/performance/kpi-vs-sla`. Alerts and insights: `sp5-framework/outputs/alerts-and-insights`.

## Three variants of IaaS
The variants differ in what is sold, how it is priced, and which SLA is offered.
- **VM**
  - Sold: a VM of a given size in a given tier. Example: 1 VM, 4 vCPU, 16 GB RAM, 200 GB disk, Gold.
  - Price rises with size and with tier.
  - Availability SLA: per VM, by tier.
  - Performance: per VM, by tier, through overcommit and maximum VM size; read with the VM KPI.
- **Resource pool**
  - Sold: GHz, GB of RAM, TB of disk. Example: 100 GHz CPU, 1 TB RAM, 80 TB disk.
  - Reservation: 100% (guaranteed) or partial. Burst is best effort, through an expandable resource pool.
  - A limit, when set, is above what is paid. Example: 1 TB RAM paid, 0.5 TB reserved, 2 TB limit.
  - Availability SLA: per VM, with limited tiering.
  - Performance: the tenant's own. The tenant may overcommit inside its own pool; the service definition does not impose it.
- **Hardware**
  - Sold: ESXi hosts. Example: 8 hosts. The tenant decides how many VMs to place. HA is provided by the vendor. Example provider: Azure VMware Solution.
  - Availability SLA: on the host or cluster, not the VM.
  - Performance: the tenant's own. The tenant can place as many VMs as it likes.
- Class of service is harder to run in the resource pool variant: nested resource pools add moving parts.
- In the resource pool variant, contention caused by the pool's own limit or by the tenant's overcommit inside the pool is the tenant's. VM CPU Ready includes time held back by a limit (`vsphere/technology/cpu/metrics/virtual-motherboard/ready`).

## VM as a Service
- The most common variant. Buy wholesale, sell retail: hardware, software and data-centre space are bought in bulk and committed for years; VMs and Kubernetes pods are sold in small units.
- Margin per unit: the provider pays roughly 5x less per GHz than it sells for.
- Cost target: cheaper than public cloud. Customers usually aim at half the public cloud price or lower, not a small saving.
- Workloads are grouped by tenant and by business application.
- Cost is known: hardware, software, services, salaries. Running well is the unknown, and the source of disputes between application teams and the infrastructure team.
- The VM profile is unknown at design time: size (vCPU, RAM, disk), intensity (CPU and RAM utilization, disk IOPS, network throughput) and pattern (daily, weekly, monthly, none). Application teams and their vendors do not know it either; some applications are not written yet.
- So the platform cannot promise to serve every VM well in absolute terms. It promises price/performance per class of service: cheap is not fast, fast is not cheap.
- Each class of service has its own availability, security and service SLA, written in the contract with numbers. Performance per class follows from overcommit and size limits and is read with the KPI.
- Class of service parameters (overcommit ratio, maximum VM size): `sp5-framework/performance/noisy-neighbour`. Host specification per class: `sp5-framework/capacity/host-spec-from-class-of-service`.
- Provisioning has an SLA too, delivered through self-service with workflows and electronic approval.

## Metrics per pillar
| Pillar | Metric | Reading |
|---|---|---|
| Availability | Operational Availability (%) | Relative: against the availability architecture and the green zone (change window) |
| Availability | Actual Availability (%) | Absolute: as it happened; usually lower |
| Performance | KPI (%) | Absolute: as it happened |
| Capacity | Capacity Remaining (%) | Relative to usable capacity, not total |
| Capacity | Time Remaining (days) | Days until Capacity Remaining reaches 0 |
| Compliance | Benchmark compliance (%) | One metric per benchmark, such as PCI-DSS |

- Performance has no SLA and no SLI: the KPI is enough (`sp5-framework/performance/kpi-vs-sla`).
- Definitions, formulas and the time window of each SLA: `sp5-framework/concepts/sla-metrics`. Numbers per class: `sp5-framework/concepts/class-of-service`.
- Usable capacity: `sp5-framework/capacity/capacity-model`.

## A complete, correct and accurate SLA
- Complete: compliance as well as availability; performance through the KPI.
- Correct: measured on each paying VM, not at the infrastructure level, with the right metrics.
- Accurate: measured every 5 minutes. A longer interval averages a breach away.
- Why per VM: a cluster average hides the VM in breach. Why 5 minutes: the interval rule in `sp5-framework/observability/thresholds`.

## Signs of complaint-based operations
- Customers blame the IaaS. Complaints are the only signal because performance is not defined or measured.
- Troubleshooting pulls in every team (network, storage, server, OS, application). No shared process ends in a root cause analysis (RCA).
- An RCA closes only when an alert is set up that detects the same issue earlier next time.
- Many oversized VMs. The team works as a system builder: it sizes each application and argues with its owners, who are its customers.
- A service provider does not block a purchase. It prices so that the right behaviour pays. Why rightsizing still matters: `sp5-framework/capacity/rightsizing`.
- New hardware cannot be justified while utilization is low. Capacity is measured on utilization and performance: a cluster is full when it cannot serve its VMs well. Hardware takes time to buy, so contention must give early warning (`sp5-framework/concepts/performance-vs-capacity`).

## Common mistakes
- Private cloud run as an automation project. Automation, workflow and the self-service portal support it. Its core is SLAs and class of service: it is operations-centric.
- VCF designed with a server-consolidation mindset: no awareness of IaaS and SLAs; classes of service mixed in one cluster or datastore.
- Class of service exists, but names of clusters and datastores do not show it.
- Performance never defined: the design benchmark does not match what is sold; often no KPI.
- The infrastructure has no awareness of business units, applications or application tiers.

## Consumer layer and provider layer
- Consumer layer: the customers' VMs. In public cloud it is all the customer can see.
- Provider layer: the infrastructure, VCF and hardware.
- The line between them is clear. The VM owner does not choose the VCF version or the hardware brand and specification.
- Public cloud is part of the provider layer. Not owning the infrastructure does not remove the infrastructure team's accountability.
- Customers first: if the VMs are served well and paid for, a problem inside the provider layer is internal.
- What each layer checks:
  - Consumer, performance: is this VM served well by the platform? Other VMs do not matter to its owner.
  - Consumer, capacity: is the VM right-sized? Too small: increase it. Too big: reduce it, for better performance.
  - Provider, performance: is the IaaS serving every VM well? No contention among all VMs.
  - Provider, capacity: utilization. Too low: too much was spent on hardware. Too high: buy hardware.
  - Provider, configuration: compliance and configuration drift.
  - Provider, availability: alerts on hardware faults, before the software stops working.
![Consumer layer (many VMs) above a line, provider layer (IaaS with security, network, storage) below. Consumer checks: 1 performance of one VM, other VMs irrelevant; 2 capacity, right-sizing. Provider checks: 1 performance of every VM, no contention; 2 capacity, utilization too low or too high; 3 configuration (compliance, drift) and availability (hardware faults)](images/consumer-provider-layer-what-each-checks-diagram.png)
- In a class with guaranteed performance, a VM is not affected by any other VM: it performs as if it were the only VM on its ESXi host.
- In a lower class, the application team accepts a performance hit for a lower price.
- Talk with application teams regularly: running well on VCF (performance, availability, security, cost); how to see that the platform serves them as promised; Windows and Linux performance practice; why right-sized beats oversized.
- VM owners differ in expectation and knowledge, more so in large environments.
- The provider side is changing too. The server, Windows or Linux team became the platform team; HCI brought storage into it; network virtualization blurred the line with the network team (firewalls, load balancers); Kubernetes added containers, with DevOps or SRE teams between platform and application teams.

## Misconceptions
- "Cluster average CPU Ready is low, so no paying VM is slow" → a cluster average hides the VM with contention. Check the VM KPI and the worst VM.
- "Utilization is low, so the cluster has capacity" → a cluster is full when it cannot serve its VMs well. Limits, imbalance and configuration cause contention at low utilization.
- "A VM in a tenant's resource pool shows contention, so the provider is at fault" → in the resource pool variant performance is the tenant's own. Check the pool limit and the tenant's overcommit first.
- "In the hardware variant the provider answers for VM uptime" → its availability SLA is on the host or cluster. The tenant places the VMs.
- "Actual Availability below Operational Availability means a data error" → Actual is absolute; Operational is relative to the availability architecture. Actual is usually lower.
- "Capacity Remaining 20% means 20% of the cluster's total capacity is free" → it is relative to usable capacity: total minus HA, buffer and overhead.
- "Block oversized VM requests" → a service provider prices; it does not block. Show owners why right-sized performs better.
- "A daily-average SLA report proves the service level" → an SLA is accurate only at 5-minute measurement; longer intervals hide breaches.

## Metadata
```yaml
id: sp5-framework/concepts/iaas-business
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
- vcf-operations
object:
- VirtualMachine
- ClusterComputeResource
- ResourcePool
- HostSystem
internal_derive:
- sp5-framework/performance/kpi-vs-sla
- sp5-framework/performance/noisy-neighbour
related:
- sp5-framework/concepts/sla-metrics
- sp5-framework/concepts/class-of-service
- sp5-framework/concepts/purpose-driven-architecture
- sp5-framework/outputs/alerts-and-insights
- sp5-framework/capacity/host-spec-from-class-of-service
- sp5-framework/capacity/capacity-model
- sp5-framework/capacity/rightsizing
- sp5-framework/concepts/performance-vs-capacity
- sp5-framework/concepts/realms-and-layers
- sp5-framework/observability/thresholds
images:
  - path: images/consumer-provider-layer-what-each-checks-diagram.png
    product: [vsphere]
    object: [VirtualMachine, ClusterComputeResource]
    topic: 'What the consumer layer and the provider layer each check, per pillar'
    image_type: diagram
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Your Private Cloud > Overview > Complaint-based Operations (The Litmus Test, Common Mistakes); The Business of IaaS (VM as a Service, Capabilities, Key Metrics, The Restaurant Analogy)'
corrections: []
review_notes:
- 'To check: Section ''Three variants of IaaS'', last bullet: contention from the pool limit or tenant overcommit is the tenant''s, and Ready includes limit time; derived from the book''s resource pool row and the VM CPU Ready file.'
- 'To check: Section ''A complete, correct and accurate SLA'', last bullet: the reason, taken from sp5-framework/observability/thresholds; not in the book.'
- 'Not copied (human reference only): the teams diagram (silos to platform team) is in the text; the restaurant analogy wording is kept out.'
- 'Book naming is older (Aria products); the knowledge base uses VCF Operations.'
status: draft
```
