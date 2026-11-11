# Measurement precision and sampling

## Sampling error
- Counters are sampled.
- Expect small rounding and timing drift.
- Do not expect values that sum to exactly 100.000% on every sample.

## Sampling drift in a busy system
- Example: target sample interval is 20 seconds.
- If collecting and processing a sample takes a few seconds (large data volume, busy system), samples drift against the wall clock over time.
- Correct collection logic accounts for the time taken to collect and process.

## Observer slower than the observed
- CPU operates in nanoseconds. Observability code operates in milliseconds.
- Values describing fast CPU activity are approximations.
- Example: thread counts per thread state in Windows or Linux can vary by ~5%.

## Past tense metrics
- Some metric names are in past tense because the value reflects what happened in the past, not current activity.
- See `vsphere/technology/memory/metrics/virtual-motherboard/ballooned`.

## Metadata
```yaml
id: sp5-framework/observability/measurement-precision
retriever_guide: how-it-works
scope: sp5-framework
technology:
- cpu
- memory
- storage
- network
pillar:
- performance
product:
- vsphere
- vcf-operations
internal_derive: []
related:
- sp5-framework/observability/resource-nature
- sp5-framework/observability/units
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: The World of Metrics > Metrics Nuances > Complexity > Other Nuances
corrections: []
review_notes: []
status: draft
```
