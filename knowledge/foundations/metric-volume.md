---
id: foundations/metric-volume
type: concept
scope: vendor-neutral
resources: [cpu, memory]
objects: [vm, vcpu]
related: [vsphere/cpu/distinctions]
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Other Nuances
corrections: []
review_notes: []
status: draft
---

# Metric volume

## Choice problem
- Several metrics measure similar things. Two watches showing different times leave you unsure which is right.
- vSphere example: 5 VM CPU "consumption" metrics and 7 ESXi CPU "consumption" metrics. See `vsphere/cpu/distinctions`.

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
