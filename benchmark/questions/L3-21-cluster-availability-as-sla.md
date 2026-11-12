# Cluster Availability as the SLA

## Prompt
Our private cloud has an SLA: Cluster Availability 99.95% per month, and we met it every month this year. Yet the application teams still complain about outages and slowness. Should we raise the SLA to 99.99%, and what else should we add to it?

## Likely wrong answer
Accepts Cluster Availability as the SLA metric and answers with nines: raise the target, add host availability, add a performance SLA or an SLI such as CPU Ready 2.5% per 5 minutes.

## Expected key points
- Names the premise: Cluster Availability is the wrong metric. An SLA is a business contract, measured on the consumer's object. The application team cares about its own VMs and Kubernetes pods, not the infrastructure under them.
- A cluster can stay up while a VM is down; a host failure whose VMs restart elsewhere is an outage for those VMs that the cluster number hides. Raising the cluster target changes nothing the application team sees.
- The Kubernetes node is often owned by the SRE team, not the developers; the developers' object is the pod.
- Availability of the consumer's object: VM or Guest OS (ping), Actual Availability vs Operational Availability (scheduled downtime excluded).
- Slowness is not an SLA matter: performance is managed with the KPI (VM Performance, pod KPI), read daily at 20-second resolution. No performance SLA, no SLI, no SLO.
- Probe any claimed SLA: which metric, on which object, which target, which window, which penalty.

## Notes
- From the author's field experience, 2026-11-11: customers claim an SLA; probed for the metric, they state the wrong one (Cluster Availability) or none.
- Drafted by Claude 2026-11-11 from the knowledge files listed in `knowledge`. Counts only after author approval.

## Metadata
```yaml
id: "0096"
title: "Cluster Availability as the SLA"
product: [vsphere, vcf-operations, kubernetes]
technology: [system]
input: [text]
task: judge-setting
knowledge:
  - sp5-framework/concepts/sla-metrics
  - sp5-framework/performance/kpi-vs-sla
attachments: []
origin: synthetic
source_path: "Author's statement on SLA and KPI, 2026-11-11"
answer_type: judged
level: 300
status: draft
```
