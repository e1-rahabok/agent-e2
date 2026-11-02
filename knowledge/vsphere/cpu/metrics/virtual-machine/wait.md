---
id: vsphere/cpu/metrics/virtual-machine/wait
retriever_guide: metric-meaning
scope: vsphere
technology:
- cpu
pillar:
- performance
product:
- vsphere
object:
- VirtualMachine
metric_class: context
internal_derive:
- vsphere/foundations/provider-consumer
same_name: []
same_meaning: []
related: []
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity
corrections: []
review_notes:
- metric_class set to context. The book groups Wait separately from contention and consumption. Author to confirm.
status: draft
---

# VM CPU Wait

## Meaning
- Includes idle time.
- Most VMs do not run at 100%, so CPU Wait is naturally high.

## Why the name is still correct
- From the kernel scheduler's vantage point, an idle vCPU is waiting to be used.

## Traps
- "High CPU Wait means the VM waits for disk or memory" → wrong. Mostly idle time.
