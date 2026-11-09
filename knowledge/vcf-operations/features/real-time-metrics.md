# Real-time metrics (VCF Operations 9.1)

## What it adds
- The purpose and the three implementations (esxtop, VCF Operations 2 seconds, 20-second data labelled real time): `observability/real-time-metrics`. This file is the VCF Operations 9.1 feature.
- New in VCF Operations 9.1: live performance data, streamed from vCenter, ESX, NSX and vSAN into a real-time metrics store.
- Two tiers on ESX hosts and VMs: 20-second (standard real-time interval) and 2-second (high-resolution, an esxtop subset of about 21 metrics).
- Purpose of 2-second data: micro bursts of 1-3 seconds that a 20-second average flattens (`sp5-framework/capacity/rightsizing`, section Micro burst).
- Designed for programmatic consumption: data is queried with PromQL (Prometheus Query Language), so scripts can detect short anomalies.

## Intervals per object
| Object | Intervals |
|---|---|
| Host System, Virtual Machine | 2 s (esxtop subset), 20 s, 5 min |
| Cluster, Datacenter | 60 s, 5 min |
| NSX transport node | 60 s, 5 min |

- Cluster and datacenter have no 2-second or 20-second data: a micro burst is read on the host or VM.

## Enable it
1. Deploy the Real-Time Metrics component: Build > Lifecycle > VCF Management > Add Components > Real-Time Metrics, per VCF instance. Requires HTTPS (443) from VCF Operations to vCenter and ESX hosts.
2. 2-second data: in the policy, tile Real time metrics, object type Host System, ESX Top state Activated.
- 20-second standard tier: Large deployments only, activated on the vCenter object type. Essentials metrics are always on.
- Without the component, dashboard charts that use real-time aggregates show empty values.

## Where to read it
- Troubleshooting Workbench > Real Time Analysis: Overview, Top N, Custom Query.
- Overview: select the ESX Top view explicitly to see 2-second data. A time range above 6 hours in that view gives an error.
- Top N: always 20-second data, never 2-second.
- Custom Query: PromQL. A metric with both tiers shows two lines; filter by feature.

```text
cpu.ready.HOST{feature='ESX_TOP'}         2-second
cpu.ready.HOST{feature='TROUBLESHOOTING'} 20-second
```

## Cost
- 2-second data is 10x the volume of 20-second data. Limit collection (book: about 1,000 data points) so the monitored system is not loaded.

## Traps
- "The 20-second tier is real time" → the UI calls it real time; each point is a 20-second average. Only the 2-second tier sees a burst of 1-3 seconds (`observability/real-time-metrics`).
- "The cluster chart shows the 2-second peak" → cluster and datacenter stop at 60 seconds; read hosts and VMs.
- "Top N lists the 2-second spikes" → Top N uses 20-second data only.
- "No 2-second data, so no burst happened" → ESX Top must be activated in the policy, and the ESX Top view selected.
- "Query cpu.ready.HOST and read one line" → both tiers return; filter feature='ESX_TOP'.
- "2-second Ready compares with 20-second thresholds" → shorter samples read higher; bands set on 20-second peaks do not apply (`observability/thresholds`).

## Metadata
```yaml
id: vcf-operations/features/real-time-metrics
retriever_guide: how-it-works
scope: vcf-operations
technology:
- cpu
- memory
- system
pillar:
- performance
- capacity
product:
- vcf-operations
- vsphere
object:
- HostSystem
- VirtualMachine
internal_derive:
- observability/real-time-metrics
related:
- sp5-framework/capacity/rightsizing
- vcf-operations/features/peak-20-second-metrics
- observability/thresholds
- vsphere/tools/esxtop/overview
source:
  document: VCF Operations 9.1 documentation (TechDocs, VCF 9.1.x), Real-time Data in the Workbench (updated 2026-10-29); Real-Time Metrics Details and Deploy Real-Time Metrics (updated 2026-11-05)
  path: https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/troubleshooting-workbench-home-page/real-time-data-in-troubleshooting-workbench.html; .../configuring-policies/using-the-monitoring-policy-workspace/policy-workspace/real-time-metrics-policy-workspace.html; .../deploying-vcf-operations-for-real-time-data-service.html
corrections:
- 'Section ''What it adds'': designed for programmatic consumption, Prometheus compatibility for scripts (author, 2026-11-07).'
review_notes:
- 'Section ''What it adds'': the docs show PromQL only in the Custom Query sub-tab; no Prometheus endpoint or API route for external scripts is described. To confirm with the author (Q129).'
- 'Docs conflict: the policy page says ESX Top view is for Virtual Machine types; the Workbench page says Host System and VM.'
- 'The list of the ~21 2-second metrics is in VODAP-9.1-Metrics-List-Per-Provider.xlsx (not read).'
- 'Section ''Cost'': 1,000 data points from the book; 10x volume is arithmetic.'
status: draft
```
