# Metrics as accounting

## Definition
- A metric is an accounting of a system in operation.
- A counter records what the system did, using the system's own accounting rules.

## Consequences for metrics
- Interpreting a counter correctly requires knowing how the whole system works.
- Without the mechanism, interpretation falls back to memorising definitions. Memorised definitions fail on cases not covered by the definition.
- A threshold can only be judged once it is known how the value is calculated.
- To explain a counter value, explain the mechanism that produced it first.

## Metadata
```yaml
id: sp5-framework/observability/metrics-as-accounting
retriever_guide: how-it-works
scope: sp5-framework
technology:
- cpu
- memory
- storage
- network
pillar:
- performance
- capacity
product:
- vsphere
- vcf-operations
internal_derive: []
related:
- sp5-framework/observability/naming-patterns
- sp5-framework/observability/thresholds
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: The World of Metrics > Metrics Nuances
corrections: []
review_notes: []
status: draft
```
