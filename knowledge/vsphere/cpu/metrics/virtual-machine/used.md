---
id: vsphere/cpu/metrics/virtual-machine/used
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
instance:
- aggregate
- per-vcpu
metric_class: consumption
internal_derive:
- vsphere/foundations/kernel-worlds
same_name:
- vsphere/cpu/metrics/host/used
same_meaning: []
related:
- vsphere/cpu/metrics/comparisons/consumption-metrics
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity
corrections:
- '2026-11-02: Author states the CPU Used metric is buggy. The row ''VM Used HT penalty 37.5% vs ESXi Used 50%'' was removed (section: Notes).'
review_notes: []
status: draft
---

# VM CPU Used

## Meaning by instance
- Per-vCPU instance: excludes System time.
- VM aggregate: includes System time.
- Pattern: same name, same object, different formula.

## Why
- System time is charged at VM level. It does not exist at vCPU level.
- See `vsphere/foundations/kernel-worlds` for work charged to the VM rather than to a vCPU.

## Notes
- The author states CPU Used is buggy. Do not build conclusions on it alone.

## Traps
- "Sum of per-vCPU Used equals VM Used" → the VM value includes System time; the per-vCPU values do not.
