# Metric volume

## Choice problem
- Several metrics measure similar things. Two watches showing different times leave you unsure which is right.
- vSphere example: 5 VM CPU "consumption" metrics and 7 ESXi CPU "consumption" metrics. See `vsphere/technology/cpu/metrics/comparisons/consumption-metrics`.

## Volume problem (vCenter example)
- Per VM: 17 CPU metrics at VM level. 12 of them also exist per vCPU. 28 memory metrics.
```text
metrics per VM = 17 + (vCPUs × 12) + 28
4-vCPU VM      = 17 + 48 + 28 = 93
```
- 1,000 VMs, average 4 vCPU:
```text
per collection        ≈ 93,000 metrics
every minute, per day ≈ 134 million metrics
6 months retention    ≈ 24+ billion metrics
```

## Consequence
- The business value per collected metric becomes a valid concern at this volume.
- This is a reason not every available metric is collected or retained.

## "Collect everything"
- "Collect everything" means two dimensions at once: more metrics and more often.
- 2x the metrics at 20 seconds instead of 5 minutes = 2 × 15 = 30x the data points. A jump of that size has to justify its benefit.
- Begin with the end in mind. For each piece of hardware and software, each product and service that can go wrong (down or slow), list the metrics needed to tell it. Work backwards from there: the list is far shorter, and every metric collected serves a purpose.
- Input, Process, Output: a metric is an input. If no output (alert, dashboard, report, troubleshooting step) needs it in its processing, collecting it wastes resources.
- 20-second visibility does not need 20-second collection: VCF Operations keeps the 20-second peak of each 5-minute cycle as its own metric (`vcf-operations/features/peak-20-second-metrics`).
- Answering "why" after an incident depends on the right data, not all data: the metrics of the component that can fail, at the resolution that shows it, plus events, tasks and logs.

## Traps
- "Collect every metric, at 20 seconds, so any incident can be explained" → 30x the data for metrics no output uses. Work backwards from what can go down or slow; take 20-second peaks where bursts matter.

## Metadata
```yaml
id: observability/metric-volume
retriever_guide: how-it-works
scope: vendor-neutral
technology:
- cpu
- memory
pillar:
- value
product: []
object:
- VirtualMachine
internal_derive: []
related:
- vsphere/technology/cpu/metrics/comparisons/consumption-metrics
- vcf-operations/features/peak-20-second-metrics
- observability/collection-interval
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Other Nuances
corrections: []
review_notes: []
status: draft
```
