# Performance dashboards

## Goals and users
- Goals: monitor performance; troubleshoot performance.
- Questions they answer:
  - Are the VMs performing well? If not, which are hit, by which resource (CPU, memory, disk, network)?
  - Is a VM slow because the infrastructure does not serve it, or because of contention inside the Guest OS?
  - Are VMs running at high utilization? Which, how high, on which resource?
  - Is that high relative to the infrastructure capacity, enough to strain the shared platform?
- Users: VMware administrators and architects. The dashboards serve proactive daily monitoring and ad hoc troubleshooting, so they are advanced; not for Level 1.
- Frequency:
  - daily for monitoring. What happened more than 24 hours ago rarely matters for troubleshooting, so the views show the last 8-24 hours;
  - ad hoc for troubleshooting, the same day as the issue or the next day at most.
- The dashboards of the suite share one design, so they read as one set. The VM Performance dashboard is the reference; read it first.

## Consumer vs provider troubleshooting
- Consumer: one VM, container or application. Other consumers have no problem, or are independent.
- Provider: the shared infrastructure, because the problem hits many consumers, possibly at random: different VMs at different times.
- Clear the infrastructure first. If it struggles to serve most VMs, troubleshooting one VM is pointless. Only when the infrastructure is free of contention, troubleshoot the VM.
- Infrastructure health is judged from its VMs, not from infrastructure metrics: does it serve every VM well? Flow: [`sp5-framework/performance/troubleshooting/vm-slow`](../performance/troubleshooting/vm-slow.md).

## Three parts: contention, consumption, configuration
- Contention: first and most visible. It is the primary counter for performance, and the only part that is colour coded.
- Consumption: once contention is found, check whether very high utilization causes it. Above 100%, performance can suffer, above all when a queue builds inside Windows or Linux.
  - VCF Operations collects every 5 minutes. A spike of a few seconds disappears when the rest of the 300 seconds is low ([`vcf-operations/features/peak-20-second-metrics`](../../vcf-operations/features/peak-20-second-metrics.md)).
- Configuration: only the settings that can affect performance.
- The split keeps each dashboard simple and puts contention first.
- Utilization is not colour coded. A health chart does not suit metrics without a ceiling, where 100% is hard to define, such as disk IOPS and CPU context switches. If operations sets a utilization limit, draw it as a line on the chart, so less technical teams can compare.

## Colour from best practice, or from a profile
- Each counter's colours follow its best practice.
- Unsure of the right values for your environment? Profile the metrics: the Guest OS Performance Profiling dashboard shows how.
- Design for the trend and for going back to any point in time: by the time someone looks, 5 minutes have passed or the problem is gone.

## Grouping in large environments
- Group VMs by clusters of the same class of service (for example Gold) to see the profile of each class.
- The vSphere Datacenter is a good boundary: storage, network and compute rarely extend beyond it.
- Performance problems tend to stay in one physical site, unless the WAN link between sites is the cause. A problem in country A rarely causes one in country B when they share little.

## Misconceptions
- "Troubleshoot the slow VM first" → clear the infrastructure first; if it fails most VMs, one VM is not the problem.
- "Infrastructure health from host metrics" → judge it by how well it serves its VMs.
- "High utilization is red" → contention is coloured; utilization is not, and a busy VM with no contention is healthy.
- "The 5-minute average shows the spike" → a few seconds of spike vanish in 300 seconds; use the 20-second peak.
- "Colour disk IOPS and context switches like contention" → they have no ceiling; draw an agreed limit line instead.
- "Keep a month of data in the performance view" → the views show 8-24 hours; older data rarely matters for troubleshooting.
- "Group the whole estate in one view" → group by class of service and by Datacenter.

## Metadata
```yaml
id: sp5-framework/outputs/performance-dashboards
retriever_guide: how-it-works
scope: sp5-framework
technology:
- cpu
- memory
- storage
- network
pillar:
- performance
product:
- vcf-operations
- vsphere
object:
- VirtualMachine
- ClusterComputeResource
- Datacenter
internal_derive:
- sp5-framework/outputs/dashboard-design
- sp5-framework/performance/troubleshooting/vm-slow
related:
- vcf-operations/features/peak-20-second-metrics
- vsphere/object-types/vm/kpis/vm-performance
- sp5-framework/concepts/class-of-service
- sp5-framework/outputs/capacity-dashboards
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Overall Design Approach > Overall Design: Performance Dashboards'
corrections: []
review_notes:
- 'Section ''Colour from best practice, or from a profile'': the source points to the Baseline Profiling section of the book for the profiling steps; not in this document.'
- 'To check: Section ''Consumer vs provider troubleshooting'': the link to vm-slow is not in the source.'
- 'Section ''Goals and users'': the source says which pods are affected; written as which VMs, as the question is about VMs.'
status: draft
```
