# Role of VCF Operations

## Role
- VCF Operations is monitoring and operations management software. It does not run workloads.
- It collects from source systems: vSphere, vSAN, NSX, Windows, Linux, VKS.
- Every metric it shows is derived from a source system. Two kinds:
  - passed through: the source counter, possibly with a different rollup or interval;
  - computed: a formula over source metrics (KPIs, capacity, super metrics).
- It is a thin layer. The meaning of a passed-through metric is set by the source, not by VCF Operations.

## vCenter vs VCF Operations
- vCenter is the administrative tool of vSphere: create VMs, configure switches, set reservations and limits.
- Capacity planning and performance troubleshooting are done in VCF Operations, not in vCenter.
- Admins often treat the two as interchangeable because VCF Operations is the main monitoring tool for vCenter. They are different tools with different jobs.
- vCenter performance charts keep a short history and roll peaks away. See [`vsphere/tools/vsphere-client/vcenter-statistics`](../vsphere/tools/vsphere-client/vcenter-statistics.md).

## Knowledge placement
- VCF Operations is an observability tool. Without a system to manage it has nothing to show, so it is not a peer of vSphere, vSAN, NSX or the Guest OS.
- A metric about a managed object is documented with that object, even when VCF Operations computes it:
  - VM CPU Contention: [`vsphere/technology/cpu/metrics/virtual-motherboard/contention`](../vsphere/technology/cpu/metrics/virtual-motherboard/contention.md), beside VM CPU Ready;
  - VM Performance (%): [`vsphere/object-types/vm/vm-performance`](../vsphere/object-types/vm/vm-performance.md);
  - Cluster Risk (%): [`vsphere/object-types/cluster/models/cluster-risk`](../vsphere/object-types/cluster/models/cluster-risk.md);
  - 20-second peaks, how VCF Operations shows a counter: [`vcf-operations/features/peak-20-second-metrics`](features/peak-20-second-metrics.md).
- This folder holds VCF Operations itself, in five folders:
  - `concepts/`: what the product is for and how it reaches people (this file, [`sp5-framework/outputs/system-engagement`](../sp5-framework/outputs/system-engagement.md));
  - `features/`: product features as implemented, such as [`vcf-operations/features/real-time-metrics`](features/real-time-metrics.md);
  - `dashboards/`: dashboard design and the shipped dashboard suites, such as [`sp5-framework/outputs/dashboard-design`](../sp5-framework/outputs/dashboard-design.md);
  - `reports/`: report design and the report suite, such as [`sp5-framework/outputs/report-design`](../sp5-framework/outputs/report-design.md);
  - `alerts/`: how alert definitions are built (bottom up), [`vcf-operations/alert-definitions`](alert-definitions.md).
- Later: its own sizing, health and performance troubleshooting.
- Alert architecture across products (top down): [`sp5-framework/outputs/alert-design`](../sp5-framework/outputs/alert-design.md). The recommended alerts live with the object type they fire on, such as [`vsphere/object-types/vm/vm-alerts`](../vsphere/object-types/vm/vm-alerts.md); their values are in the threshold catalog.

## Misconceptions
- "vCenter and VCF Operations show the same counter name, so the values match" → rollup and interval can differ. Check the source file and [`vsphere/tools/vsphere-client/vcenter-statistics`](../vsphere/tools/vsphere-client/vcenter-statistics.md).
- "Plan capacity from vCenter charts" → vCenter is an administrative tool; its history is short and averaged.
- "A VCF Operations metric needs its own definition" → only computed metrics do. A passed-through metric means what its source means.

## Metadata
```yaml
id: vcf-operations/vcf-operations-role
retriever_guide: how-it-works
scope: vcf-operations
technology:
- system
pillar:
- performance
- capacity
product:
- vcf-operations
- vsphere
internal_derive:
- vsphere/architecture/metric-sources
related:
- vsphere/tools/vsphere-client/vcenter-statistics
- vsphere/architecture/provider-consumer
- vcf-operations/features/peak-20-second-metrics
source:
  document: Knowledge base
  path: Conversation on VCF Operations and vCenter roles
corrections: []
review_notes:
- 'Section ''vCenter vs VCF Operations'': short history and rolled-up peaks follow vsphere/tools/vsphere-client/vcenter-statistics.'
status: draft
```
