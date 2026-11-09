# Real-time metrics

## Purpose
- Real-time metrics show what a 5-minute average flattens: a micro burst of 1-3 seconds, or a spike of under a minute.
- Use cases: troubleshooting a burst on a known host or VM while it happens or soon after; checking whether a short spike, not a sustained load, causes a complaint; rightsizing for bursty workloads (`sp5-framework/capacity/rightsizing`, section Micro burst).
- They add to 5-minute metrics; they do not replace them. 5-minute data stays the base for monitoring, capacity, KPIs and SLAs: it is kept for months or years and is cheap to store and query.
- Cost: each step finer multiplies the data. 2-second data is 10x the volume of 20-second data, and 150x that of 5-minute data. Retention is short, and collection is limited to a subset of metrics and objects so the monitored system is not loaded.

## Three implementations
| Interval | Where | Real time? |
|---|---|---|
| 2-5 seconds | esxtop on one ESXi host (default 5, minimum 2) | Yes |
| 2 seconds | VCF Operations 9.1, ESX Top tier (about 21 metrics, hosts and VMs) | Yes |
| 20 seconds | vCenter (vSphere Client chart named Real-time); VCF Operations 9.1 standard real-time tier | No: labelled real time by the UI |

- esxtop: one host at a time, nothing kept unless batch mode is used. See `vsphere/tools/esxtop/overview`.
- VCF Operations 2-second tier: across hosts and VMs, queried with PromQL in the Troubleshooting Workbench. See `vcf-operations/features/real-time-metrics`.
- 20-second data: each point is the average of 20 seconds. vCenter keeps it for about an hour before rolling it into 5-minute points (`vsphere/tools/vsphere-client/vcenter-statistics`). VCF Operations reports the highest 20-second value of each 5-minute cycle as a peak metric (`vcf-operations/features/peak-20-second-metrics`).

## Reading across intervals
- The same workload reads higher at 2 seconds than at 20 seconds, and higher at 20 seconds than at 5 minutes. A band set on one interval does not apply to another (`observability/thresholds`, Interval rule).
- A spike seen at 2 seconds and absent at 20 seconds lasted less than 20 seconds.

## Traps
- "The vSphere Client Real-time chart is real time" → it shows 20-second averages; the label is the UI's.
- "Real-time data replaces 5-minute data" → it adds to it; 5-minute data carries monitoring, capacity and SLAs over months.
- "Collect 2-second data on everything" → 10x the volume of 20-second data; limit it to the metrics and objects being troubleshot.
- "Compare 2-second CPU Ready with the 20-second bands" → shorter samples read higher; each interval has its own band.
- "No spike in the Real-time chart, so no burst" → a burst under 20 seconds is averaged away; use esxtop or the 2-second tier.

## Metadata
```yaml
id: observability/real-time-metrics
retriever_guide: how-it-works
scope: vendor-neutral
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
- observability/collection-interval
- observability/thresholds
related:
- vcf-operations/features/real-time-metrics
- vsphere/tools/esxtop/overview
- vsphere/tools/vsphere-client/vcenter-statistics
- vcf-operations/features/peak-20-second-metrics
- sp5-framework/capacity/rightsizing
source:
  document: Author's answer (2026-11-09)
  path: 'Conversation on the vcf-operations folder: real-time metrics as concept and implementation (esxtop 2-5 s; VCF Operations 9.1 2 s; vCenter and VCF Operations 9.1 20 s, labelled real time but not real time)'
corrections: []
review_notes:
- 'Section ''Purpose'': the use cases, the 150x volume (300 s / 2 s) and the short retention are Claude''s, from the intervals; the 10x is from vcf-operations/features/real-time-metrics.'
- 'Section ''Three implementations'': esxtop default 5 s, minimum 2 s from vsphere/tools/esxtop/overview; about 21 metrics from the VCF Operations 9.1 documentation (vcf-operations/features/real-time-metrics); vCenter keeps 20-second data about an hour (Claude''s knowledge of the vCenter real-time interval).'
status: draft
```
