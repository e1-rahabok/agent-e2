---
id: vsphere/cpu/metrics/virtual-machine/usage
retriever_guide: metric-meaning
scope: vsphere
technology:
- cpu
pillar:
- performance
- capacity
product:
- vsphere
object:
- VirtualMachine
metric_class: consumption
internal_derive:
- vsphere/cpu/concepts/hyper-threading
- vsphere/foundations/provider-consumer
same_name:
- vsphere/cpu/metrics/host/usage
same_meaning: []
related:
- vsphere/cpu/metrics/comparisons/consumption-metrics
- vsphere/cpu/metrics/host/core-utilization
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity
corrections:
- '2026-11-02: Hyper-Threading scenario (section: Hyper-Threading) rewritten from the author. The uploaded document sentence is truncated.'
review_notes:
- The 37.5% penalty is from the author. Not found in Performance Best Practices for vSphere 9.1.
status: draft
---

# VM CPU Usage

## Hyper-Threading
- Scenario: two vCPUs run on the two threads of the same physical core at the same time.
- VM Usage is HT-aware. When both threads run, the VM is charged a 37.5% penalty, so it shows about 62.5%.
- The VM cannot see the core or its two threads. ESXi can.
- The host view of the same core: see `vsphere/cpu/metrics/host/usage`.

## Cap
- VM CPU Usage (MHz) is not capped.

## Reservation
- CPU reservation is on demand. It is not included in Usage.

## Traps
- "VM shows 62.5%, so the metric is wrong" → wrong. Different vantage point from the host.
- "Each VM gets only 62.5% of what it demands" → the 62.5% is an accounting charge for sharing a core.
