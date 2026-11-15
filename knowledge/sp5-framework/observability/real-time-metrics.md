# Real-time metrics

## Purpose
- Real-time metrics show what a 5-minute average flattens: a micro burst of 1-3 seconds, or a spike of under a minute.
- Use cases: troubleshooting a burst on a known host or VM while it happens or soon after; checking whether a short spike, not a sustained load, causes a complaint; rightsizing for bursty workloads ([`sp5-framework/capacity/rightsizing`](../capacity/rightsizing.md), section Micro burst).
- They add to 5-minute metrics; they do not replace them. 5-minute data stays the base for monitoring, capacity and KPIs: it is kept for months or years and is cheap to store and query.
- Cost: each step finer multiplies the data. 2-second data is 10x the volume of 20-second data, and 150x that of 5-minute data. Retention is short, and collection is limited to a subset of metrics and objects so the monitored system is not loaded.

## Three implementations
| Interval | Where | Real time? |
|---|---|---|
| 2-5 seconds | esxtop on one ESXi host (default 5, minimum 2) | Yes |
| 2 seconds | VCF Operations 9.1, ESX Top tier (about 21 metrics, hosts and VMs) | Yes |
| 20 seconds | vCenter (vSphere Client chart named Real-time); VCF Operations 9.1 standard real-time tier | No: labelled real time by the UI |

- esxtop: one host at a time, nothing kept unless batch mode is used. See [`vsphere/tools/esxtop/overview`](../../vsphere/tools/esxtop/overview.md).
- VCF Operations 2-second tier: across hosts and VMs, queried with PromQL in the Troubleshooting Workbench. See [`vcf-operations/features/real-time-metrics`](../../vcf-operations/features/real-time-metrics.md).
- 20-second data: each point is the average of 20 seconds. vCenter keeps it for about an hour before rolling it into 5-minute points ([`vsphere/tools/vsphere-client/vcenter-statistics`](../../vsphere/tools/vsphere-client/vcenter-statistics.md)). VCF Operations reports the highest 20-second value of each 5-minute cycle as a peak metric ([`vcf-operations/features/peak-20-second-metrics`](../../vcf-operations/features/peak-20-second-metrics.md)).

## Reading across intervals
- The same workload reads higher at 2 seconds than at 20 seconds, and higher at 20 seconds than at 5 minutes. A band set on one interval does not apply to another ([`sp5-framework/observability/thresholds`](thresholds.md), Interval rule).
- A spike seen at 2 seconds and absent at 20 seconds lasted less than 20 seconds.

## Misconceptions
- "The vSphere Client Real-time chart is real time" → it shows 20-second averages; the label is the UI's.
- "Real-time data replaces 5-minute data" → it adds to it; 5-minute data carries monitoring, capacity and KPI history over months.
- "Collect 2-second data on everything" → 10x the volume of 20-second data; limit it to the metrics and objects being troubleshot.
- "Compare 2-second CPU Ready with the 20-second bands" → shorter samples read higher; each interval has its own band.
- "No spike in the Real-time chart, so no burst" → a burst under 20 seconds is averaged away; use esxtop or the 2-second tier.

## Metadata
```yaml
id: sp5-framework/observability/real-time-metrics
retriever_guide: how-it-works
scope: sp5-framework
technology:
- cpu
- memory
- storage
- network
- system
pillar:
- performance
- capacity
product:
- vsphere
- vcf-operations
object:
- HostSystem
- VirtualMachine
internal_derive:
- sp5-framework/observability/collection-interval
- sp5-framework/observability/thresholds
related:
- vcf-operations/features/real-time-metrics
- vsphere/tools/esxtop/overview
- vsphere/tools/vsphere-client/vcenter-statistics
- vcf-operations/features/peak-20-second-metrics
- sp5-framework/capacity/rightsizing
source:
  document: Knowledge base; Broadcom KB 444403, Understanding "Peak" or "Worst" Performance Metrics in VMware VCF / Aria Operations (VCF Operations 9.x)
  path: 'Real-time metrics as concept; implementations from vsphere/tools/esxtop/overview (default 5 s, minimum 2 s), vcf-operations/features/real-time-metrics (2-second tier, about 21 metrics, 10x the volume of 20-second data) and vsphere/tools/vsphere-client/vcenter-statistics (Real-time chart, 1 hour). KB 444403: vCenter keeps 20-second data typically 1 hour'
corrections: []
review_notes: []
status: draft
```
