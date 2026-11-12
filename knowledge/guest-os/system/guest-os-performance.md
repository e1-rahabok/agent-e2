# Guest OS Performance (%) (vCommunity management pack KPI for VCF Operations)

## Layer
- Guest OS layer: Windows or Linux, running on the VM. The VM is a virtual motherboard; it cannot see inside the Guest OS.
- VMware Tools collects these counters inside the Guest OS, and vCenter and VCF Operations store them on the VirtualMachine object. That is a data path, not ownership: the counters belong to the Guest OS.

## What it is
- One 0-100% score for the operating system inside a VM. 100 is perfect. It answers: is the Guest OS getting the CPU, disk and memory it needs?
- VM Performance (%) scores the virtual motherboard; this KPI scores what runs on it ([`vsphere/object-types/vm/vm-performance`](../../vsphere/object-types/vm/vm-performance.md)). Their average is the VM Guest OS KPI, one score per VM for the application team.
- Published on every powered-on VM with VMware Tools as `vCommunity|Guest OS Performance|Guest OS Performance Score`. Without VMware Tools there is no score.

## Sub-metrics
| Group | Sub-metric | Source | Unit | Scores 100 at |
|---|---|---|---|---|
| Guest OS contention | CPU run queue per vCPU | `guest\|20_sec_peak_cpu_queue` | threads | 0 |
| Guest OS contention | Disk queue | `guest\|20_sec_peak_disk_queue` | IOs | 0 |
| Guest OS utilization | Free memory | `guest\|mem.free_latest` ÷ 1024 (KB to MB) | MB | 1,024 or more |
| Guest OS utilization | Page-out rate | `guest\|page.outRate_latest` | pages/s | 0 |

- Colour levels: `catalog/thresholds-performance`, section `kpi`, rows with this file as `kb`.
- Free memory is higher-is-better, so its limits go down: 1 GB or more free scores 100; the green range ends at 512 MB.
- The run queue stat is already per vCPU.
- Free memory uses the latest value, not the lowest 20-second value: it measures space, and the latest value matters.

## Reasons
- Guest OS metrics with no VM equivalent, which change the course of troubleshooting.
- The run queue threshold is set higher than normal to reduce false positives.
- Linux and Windows track memory space, throughput and IOPS, but not memory latency. A Guest OS memory performance metric is still missing.
- Utilization metrics are included because the Guest OS has only 4 metrics: combining keeps it simple.

## Scoring
- The scoring shared by every KPI: [`sp5-framework/performance/performance-kpi-design`](../../sp5-framework/performance/performance-kpi-design.md), section Scoring.
- Nothing wrong: all 4 score 100. KPI = 100.
- CPU run queue of 3 per vCPU: halfway through yellow (2 to 4) scores 62.5, weight 2.83. KPI = (3 × 100 + 62.5 × 2.83) / (3 + 2.83) ≈ 81.8.
- 192 MB free memory: halfway through orange (256 down to 128) scores 37.5, weight 5.66. KPI ≈ 59.16.
- Missing data: a sub-metric with no data, or a stat older than 10 minutes, is left out, never counted as perfect.

## Misconceptions
- "Guest OS memory latency is in the KPI" → Windows and Linux do not track it.
- "Guest OS Performance is low, so the host is overloaded" → the Guest OS is a separate realm; read VM Performance (%) for what the host gives the VM.
- "512 MB free memory scores 100" → 1 GB or more scores 100; 512 MB is the end of green.
- "Guest OS Performance covers every VM" → only VMs with VMware Tools; the others have no score.

## Metadata
```yaml
id: guest-os/system/guest-os-performance
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
- vsphere/object-types/vm/vm-performance
- guest-os/system/troubleshooting/ms-windows-slow
- guest-os/system/troubleshooting/linux-os-slow
- sp5-framework/performance/performance-management
images:
source:
  document: VCF-vCommunity-Adapter documentation, Guest OS Performance KPI (read 2026-11-11); Private Cloud Management by Iwan Rahabok (https://isvara.io/download) for the reasons
  path: 'https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/guest-os-performance.md; Consumer Objects > Performance: VM & Guest OS > Guest OS Performance (%)'
corrections:
- 'Section ''Sub-metrics'': from the adapter documentation. Free memory scores 100 from 1 GB (the earlier text: above 512 MB).'
review_notes: []
status: draft
```
