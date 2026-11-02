---
id: foundations/metric-perspectives
type: concept
scope: vendor-neutral
resources: [cpu, memory, storage, network]
related: [foundations/resource-nature]
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Documentation Challenge
corrections: []
review_notes:
  - "Document orders raw metrics per resource as contention first, then consumption. Left out: unclear if this is an analysis rule or only the book's layout. Confirm if it should be added as a rule."
status: draft
---

# Three perspectives on metrics

Any metric can be viewed from three perspectives. Full understanding requires all three.

## 1. Technology
- Computer architecture has not fundamentally changed since the mainframe: CPU, memory, disk, network.
- Variants exist (GPU, APU). Components become distributed and virtual.
- Metric behaviour changes when a component becomes distributed or virtual.
- Best suited to infrastructure metrics.

## 2. Pillars of operations
- Each pillar creates its own metrics.

| Pillar | Example metrics it creates |
|---|---|
| Capacity | Time Remaining, Recommended Size |
| Cost | Month-to-Date Cost |
| Performance | KPI (%) |
| Compliance | PCI-DSS Compliance Score (%) |

## 3. Product / object
- Each product (vSphere, NSX, Kubernetes, ...) brings its own object types.
- Each object type (VM, Kubernetes Pod, AWS S3, Oracle DB, ...) has its own metrics.
- Objects relate to other objects and are grouped under parents (e.g. Kubernetes cluster → nodes → pods).
- Result: multiple parallel or overlapping hierarchies.

## Raw vs derived metrics
- Raw metric: simple, narrow scope.
- Derived metric: combines multiple raw metrics. Often spans multiple areas.
- Raw metrics map best to the technology perspective.
- Derived metrics map best to the product/object perspective, then the pillar perspective.
