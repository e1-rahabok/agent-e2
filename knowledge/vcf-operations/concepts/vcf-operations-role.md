# Role of VCF Operations

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
- vCenter performance charts keep a short history and roll peaks away. See `vsphere/tools/vsphere-client/vcenter-statistics`.

## Where its knowledge lives
- VCF Operations is an observability tool. Without a system to manage it has nothing to show, so it is not a peer of vSphere, vSAN, NSX or the Guest OS.
- A metric about a managed object is documented with that object, even when VCF Operations computes it:
  - VM CPU Contention: `vsphere/technology/cpu/metrics/virtual-motherboard/contention`, beside VM CPU Ready;
  - VM Performance (%): `vsphere/object-types/vm/kpis/vm-performance`;
  - Cluster Risk (%): `vsphere/object-types/cluster/models/cluster-risk`;
  - 20-second peaks, how VCF Operations shows a counter: `vcf-operations/features/peak-20-second-metrics`.
- This folder holds VCF Operations itself, in five folders:
  - `concepts/`: what the product is for and how it reaches people (this file, `vcf-operations/concepts/system-engagement`);
  - `features/`: product features as implemented, such as `vcf-operations/features/real-time-metrics`;
  - `dashboards/`: dashboard design and the shipped dashboard suites, such as `vcf-operations/dashboards/dashboard-design`;
  - `reports/`: report design and the report suite, such as `vcf-operations/reports/report-design`;
  - `alerts/`: how alert definitions are built (bottom up), `vcf-operations/alerts/alert-definitions`.
- Later: its own sizing, health and performance troubleshooting.
- Alert architecture across products (top down): `sp5-framework/alerts/alert-design`. Alert thresholds live with the resource they watch, such as `vsphere/technology/cpu/configuration/cpu-alerts`.

## Traps
- "vCenter and VCF Operations show the same counter name, so the values match" → rollup and interval can differ. Check the source file and `vsphere/tools/vsphere-client/vcenter-statistics`.
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
- vsphere/architecture/metric-sources
related:
- vsphere/tools/vsphere-client/vcenter-statistics
- vsphere/architecture/provider-consumer
- vcf-operations/features/peak-20-second-metrics
source:
  document: Author's answer (2026-11-04)
  path: Conversation with the author on VCF Operations and vCenter roles
corrections: []
review_notes:
- 'Section ''Where its knowledge lives'': folders concepts, features, dashboards, reports, alerts (author, 2026-11-09: a file that documents an actual implementation is not a concept). VCF Operations is not a peer of the managed systems; vcf-operations/ holds only content about itself (author, 2026-11-08).'
- 'Whole file: from the author''s statement of 2026-11-04 (VCF Operations is monitoring software; all its metrics are derived; thin layer above vSphere, vSAN, NSX, Windows, Linux, VKS; vCenter is an administrative tool, not used for capacity planning or performance troubleshooting).'
- 'Section ''vCenter is not the operations tool'': short history and rolled-up peaks follow vsphere/tools/vsphere-client/vcenter-statistics.'
status: draft
```
