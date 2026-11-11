# VM Performance (%) (VCF Operations KPI)

## Thresholds (book)
- Colour levels (yellow, orange, red for 5 minutes, 20 seconds and 2 seconds): `catalog/thresholds-performance`, section `kpi`. They are shown with this file; this file holds the reasons.

## Reasons
- CPU uses 4 metrics (Co-stop, Ready, Overlap, Net Run). They do not peak in the same 20-second period, so they cannot be combined. Known limitation: CPU weight is larger.
- Ready, Co-stop and Overlap have different thresholds: different sensitivity. Ready tends to be 2x Co-stop.
- High CPU utilization threshold: high utilization means work is done.
- Memory Contention is the only counter that shows a VM memory problem. VM and Guest OS can have memory problems independently.
- Ballooned and Compressed + Swapped are leading indicators, not real performance problems.
- Compressed and Swapped are combined: both result from the same action (reclaiming a page), so together they tell the complete picture.
- Their band is tighter than Memory Contention (green 0-0.25% vs 0-0.5%) although they are less serious: they are measured on 5-minute samples, Memory Contention on 20-second peaks. A 5-minute average reads lower than a 20-second peak, so its band must be lower too.
- Ballooned and Compressed + Swapped are divided by Guest OS used memory, not configured memory. Configured would under-report the risk.
- Network: vCenter has no latency or retransmit, so transmit dropped packets are used. Threshold not low: drops are retransmitted and often unnoticed.
- Known limitation: dropped packets use the 20-second peak, but packets transmitted uses the period average (which of the 15 points to take is unknown).

## Misconceptions
- "CPU Run 70% lowers the score" → below 95% is green; below 60% scores 100.

## Metadata
```yaml
id: vsphere/object-types/vm/kpis/vm-performance
retriever_guide: metric-meaning
scope: vsphere
technology:
- cpu
- memory
- storage
- network
- system
pillar:
- performance
product:
- vcf-operations
object:
- VirtualMachine
layer:
- virtual-motherboard
metric_class: contention
internal_derive:
- sp5-framework/performance/performance-kpi-design
same_name: []
same_meaning: []
related:
- guest-os/system/metrics/guest-os-performance
- vcf-operations/features/peak-20-second-metrics
images:
source:
  document: PART 3 - Counters.docx
  path: 'Consumer Objects > Performance: VM & Guest OS > VM Performance (%)'
corrections:
- 'Section ''Reasons'': the book says the Compressed + Swapped threshold is 2x memory contention. The table (half) is correct; the text is superseded. Keep until the book is updated.'
review_notes: []
status: draft
```
