# Three perspectives on metrics

Any metric can be viewed from three perspectives. Full understanding requires all three.

## 1. Technology
- Computer architecture has not fundamentally changed since the mainframe: CPU, memory, disk, network.
- Variants exist (GPU, APU). Components become distributed and virtual.
- Metric behaviour changes when a component becomes distributed or virtual.
- Best suited to infrastructure metrics.
- Technology values used in this knowledge base: CPU, memory, storage, network, system.
- System: the box as a whole, such as the OS, the BIOS, or a whole device. Example: overall chassis availability (%) of a physical storage array.

## 2. Pillars of operations
- Each pillar creates its own metrics.

| Pillar | Example metrics it creates |
|---|---|
| Availability | Not given in the source. |
| Performance | KPI (%) |
| Security | PCI-DSS Compliance Score (%) |
| Capacity | Time Remaining, Recommended Size |
| Value | Month-to-Date Cost |

## 3. Product / object
- Each product (vSphere, NSX, Kubernetes, ...) brings its own object types.
- Each object type (VM, Kubernetes pod, datastore, Oracle DB, ...) has its own metrics.
- Objects relate to other objects and are grouped under parents (e.g. Kubernetes cluster → nodes → pods).
- Result: multiple parallel or overlapping hierarchies.

## Raw vs derived metrics
- Raw metric: simple, narrow scope.
- Derived metric: combines multiple raw metrics. Often spans multiple areas.
- Raw metrics map best to the technology perspective.
- Derived metrics map best to the product/object perspective, then the pillar perspective.

## Analysis order per resource
- Look at contention metrics first, then consumption metrics.

## Metadata
```yaml
id: sp5-framework/observability/metric-perspectives
retriever_guide: how-it-works
scope: sp5-framework
technology:
- cpu
- memory
- storage
- network
- system
pillar:
- availability
- performance
- security
- capacity
- value
product:
- vsphere
- vcf-operations
internal_derive: []
related:
- sp5-framework/observability/resource-nature
source:
  document: Knowledge base
  path: The World of Metrics > Metrics Nuances > Complexity > Documentation Challenge
corrections:
- '2026-11-02: Contention first, then consumption, is an analysis rule (not only document layout).'
- '2026-11-02: Pillars are availability, performance, security, capacity, value (section: 2. Pillars of operations). Uploaded document lists capacity, cost, performance, compliance.'
- '2026-11-02: Technology includes system: OS, BIOS, or whole device (section: 1. Technology).'
review_notes: []
status: draft
```
