# Guest OS Performance (%) (VCF Operations KPI)

## Layer
- Guest OS layer: Windows or Linux, running on the VM. The VM is a virtual motherboard; it cannot see inside the Guest OS.
- VMware Tools collects this counter inside the Guest OS and vCenter and VCF Operations store it on the VirtualMachine object. That is a data path, not ownership: the counter belongs to the Guest OS.

## Thresholds (book)
- Colour levels (yellow, orange, red for 5 minutes, 20 seconds and 2 seconds): `catalog/thresholds-performance`, section `kpi`. They are shown with this file; this file holds the reasons.

## Reasons
- Guest OS metrics with no VM equivalent, which change the course of troubleshooting.
- The run queue threshold is set higher than normal to reduce false positives.
- Linux and Windows track memory space, throughput and IOPS, but not memory latency. A Guest OS memory performance metric is still missing.
- Utilization metrics are included because the Guest OS has only 4 metrics: combining keeps it simple.

## Traps
- "Guest OS memory latency is in the KPI" → Windows and Linux do not track it.

## Metadata
```yaml
id: guest-os/system/metrics/guest-os-performance
retriever_guide: metric-meaning
scope: guest-os
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
- windows
- linux
layer:
- guest-os
metric_class: contention
internal_derive:
- sp5-framework/performance/performance-kpi-design
same_name: []
same_meaning: []
related:
- vsphere/object-types/vm/kpis/vm-performance
images:
source:
  document: PART 3 - Counters.docx
  path: 'Consumer Objects > Performance: VM & Guest OS > Guest OS Performance (%)'
corrections: []
review_notes: []
status: draft
```
