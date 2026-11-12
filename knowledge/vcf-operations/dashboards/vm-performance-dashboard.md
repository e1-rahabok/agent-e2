# VM Performance dashboard

## Dashboard choice
- In VCF Operations 9.1, the VM Performance dashboard is the dashboard for VM performance monitoring and troubleshooting.
- It supersedes the VM Contention dashboard. In 9.1 the old dashboard is renamed with the suffix (DEP): deprecated, kept for a transition period.
- The VCF Operations 9.1 documentation still describes VM Contention as current. The documentation was not updated; the product was. When the two differ, the product is the newer source.

## Dashboard content
- Performance means contention: the VM did not get the CPU, memory, disk or network service it demanded. VM Performance (%) is a KPI built from contention counters ([`vsphere/object-types/vm/vm-performance`](../../vsphere/object-types/vm/vm-performance.md), [`sp5-framework/performance/performance-kpi-design`](../../sp5-framework/performance/performance-kpi-design.md)).
- Contention first and colour coded; utilization second, as context, not colour coded; then the configuration that can affect performance ([`sp5-framework/outputs/performance-dashboards`](../../sp5-framework/outputs/performance-dashboards.md)).
- Counters are VCF Operations metrics on the VM object (VM CPU Ready, Co-stop, Memory Contention, Disk Latency), reported every 5 minutes as an average and as the 20-second peak ([`vcf-operations/features/peak-20-second-metrics`](../features/peak-20-second-metrics.md)). They are not esxtop fields.
- Widget detail: to be written after the dashboard overhaul.

## Misconceptions
- "VM Contention is the dashboard for VM contention" → it is deprecated in 9.1; VM Performance supersedes it. The documentation lags the product.
- "VM Contention shows supply, VM Performance shows demand" → there is no such split. Performance is contention; demand and utilization are consumption, read as context on the same dashboard.
- "The dashboard shows %RDY and %CSTP" → those are esxtop fields, sampled every 2-5 seconds per world. VCF Operations shows VM CPU Ready (%) and Co-stop (%) per 5 minutes, with 20-second peaks; the values are not comparable.
- "Active Memory is a performance metric" → Active is an estimate of recently touched pages, with no operational use ([`vsphere/technology/memory/metrics/virtual-motherboard/active`](../../vsphere/technology/memory/metrics/virtual-motherboard/active.md)).
- "No contention and CPU at 100%: add vCPUs" → a batch job runs at 100% by design. Add vCPUs only when the Guest OS run queue shows a bottleneck ([`vsphere/object-types/vm/vm-alerts`](../../vsphere/object-types/vm/vm-alerts.md), section VM CPU consumption).
- "The official page is current, so follow it" → for VCF Operations 9.1 dashboards, the documentation is out of date in places; the product names (DEP) dashboards.

## Metadata
```yaml
id: vcf-operations/dashboards/vm-performance-dashboard
retriever_guide: how-it-works
scope: vcf-operations
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
internal_derive:
- vsphere/object-types/vm/vm-performance
- sp5-framework/outputs/performance-dashboards
related:
- sp5-framework/performance/performance-kpi-design
- vcf-operations/features/peak-20-second-metrics
- vsphere/technology/memory/metrics/virtual-motherboard/active
- vsphere/object-types/vm/vm-alerts
- sp5-framework/performance/vm-slow
source:
  document: Knowledge base
  path: 'Conversation on the VM Contention dashboard: VM Performance supersedes VM Contention, which is marked (DEP) in VCF Operations 9.1; the 9.1 documentation was not updated'
corrections:
- 'Section ''Dashboard choice'': VM Contention deprecated, superseded by VM Performance. The VCF Operations 9.1 documentation (TechDocs, Performance Dashboards > VM Contention Dashboard) still describes it as current.'
review_notes:
- 'To check: Section ''Dashboard content'': widget detail, after the dashboard overhaul; the layout follows sp5-framework/outputs/performance-dashboards (Part 2).'
- 'To check: Section ''Misconceptions'': written from a Gemini answer of 2026-11-09 (benchmark question 0091); check each misconception.'
status: draft
```
