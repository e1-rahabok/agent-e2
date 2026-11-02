---
id: foundations/metrics-as-accounting
retriever_guide: how-it-works
scope: vendor-neutral
technology:
- cpu
- memory
- storage
- network
pillar:
- performance
- capacity
product: []
internal_derive: []
related:
- foundations/naming-patterns
- foundations/thresholds
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances
corrections: []
review_notes: []
status: draft
---

# Metrics as accounting

## Definition
- A metric is an accounting of a system in operation.
- A counter records what the system did, using the system's own accounting rules.

## Consequences for metrics
- Interpreting a counter correctly requires knowing how the whole system works.
- Without the mechanism, interpretation falls back to memorising definitions. Memorised definitions fail on cases not covered by the definition.
- A threshold can only be judged once it is known how the value is calculated.
- To explain a counter value, explain the mechanism that produced it first.
