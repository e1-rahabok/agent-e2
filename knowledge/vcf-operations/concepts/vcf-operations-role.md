# VCF Operations: a derived layer above the source systems

## Role
- VCF Operations is monitoring and operations management software. It does not run workloads.
- It collects from source systems: vSphere, vSAN, NSX, Windows, Linux, VKS.
- Every metric it shows is derived from a source system. Two kinds:
  - passed through: the source counter, possibly with a different rollup or interval;
  - computed: a formula over source metrics (KPIs, capacity, super metrics).
- It is a thin layer. The meaning of a passed-through metric is set by the source, not by VCF Operations.

## vCenter is not the operations tool
- vCenter is the administrative tool of vSphere: create VMs, configure switches, set reservations and limits.
- Capacity planning and performance troubleshooting are done in VCF Operations, not in vCenter.
- Admins often treat the two as interchangeable because VCF Operations is the main monitoring tool for vCenter. They are different tools with different jobs.
- vCenter performance charts keep a short history and roll peaks away. See `vsphere/foundations/vcenter-statistics`.

## Where its knowledge lives
- A metric about a source object is documented once, at the source object. Example: VM CPU Ready lives in `vsphere/technology/cpu/metrics/virtual-motherboard/ready`.
- This folder holds only what VCF Operations itself adds:
  - computed metrics and KPIs, with their formula, linking each input to its source file;
  - its own mechanisms: capacity engine, policies, symptoms and alerts, super metrics, KPI calculation;
  - where a VCF Operations value differs from its source value (rollup, interval, peak handling).
- Each file here links to the source files it derives from (`internal_derive`), so nothing is written twice.

## Traps
- "vCenter and VCF Operations show the same counter name, so the values match" → rollup and interval can differ. Check the source file and `vsphere/foundations/vcenter-statistics`.
- "Plan capacity from vCenter charts" → vCenter is an administrative tool; its history is short and averaged.
- "A VCF Operations metric needs its own definition" → only computed metrics do. A passed-through metric means what its source means.

## Metadata
```yaml
id: vcf-operations/concepts/vcf-operations-role
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
- vsphere/foundations/metric-sources
related:
- vsphere/foundations/vcenter-statistics
- vsphere/foundations/provider-consumer
- vsphere/object-types/vm/metrics/comparisons/peak-20-second-metrics
source:
  document: Author's answer (2026-11-04)
  path: Conversation with the author on VCF Operations and vCenter roles
corrections: []
review_notes:
- 'Whole file: from the author''s statement of 2026-11-04 (VCF Operations is monitoring software; all its metrics are derived; thin layer above vSphere, vSAN, NSX, Windows, Linux, VKS; vCenter is an administrative tool, not used for capacity planning or performance troubleshooting).'
- 'Section ''vCenter is not the operations tool'': short history and rolled-up peaks follow vsphere/foundations/vcenter-statistics.'
status: draft
```
