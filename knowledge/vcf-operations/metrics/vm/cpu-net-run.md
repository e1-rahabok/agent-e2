# VM CPU Net Run (VCF Operations)

## Meaning
- Run minus the time the vCPU was interrupted by the kernel.
- Added to VCF Operations in July 2024.

## Formula
```text
Net Run = Run - Overlap
```

## Why
- Run does not see Overlap, frequency or Hyper-Threading.
- Run is the input for Guest OS sizing. The interrupted portion (Overlap) must be removed.
- Net Run cannot exceed 100%.

## Net Run vs Usage
- Net Run can stay flat at 100% for 24 hours while Usage fluctuates widely.
- Usage can be higher or lower than Net Run. Usage moves with CPU speed and power management.
- High utilization: Usage (%) over-reports, due to Turbo Boost.
- Low utilization: Usage (%) under-reports, due to power saving.

## Traps
- "Usage above Net Run means more work than possible" → Turbo raises Usage. Net Run caps at 100%.

## Metadata
```yaml
id: vcf-operations/metrics/vm/cpu-net-run
retriever_guide: metric-meaning
scope: vcf-operations
technology:
- cpu
pillar:
- capacity
- performance
product:
- vcf-operations
object:
- VirtualMachine
layer:
- virtual-motherboard
metric_class: consumption
internal_derive:
- vsphere/technology/cpu/metrics/virtual-motherboard/run
- vsphere/technology/cpu/metrics/virtual-motherboard/overlap
same_name: []
same_meaning: []
related:
- vsphere/technology/cpu/metrics/virtual-motherboard/run
- vsphere/technology/cpu/metrics/virtual-motherboard/usage
- vsphere/technology/cpu/metrics/virtual-motherboard/overlap
source:
  document: PART 3 - Counters.docx
  path: CPU > VM (pp. 78-118) > Consumption Metrics > Run | Net Run; Usage vs Net Run
corrections: []
review_notes:
- 'Moved 2026-11-06 from vcf-operations/metrics/vm/cpu-net-run (architecture review 2026-11-06, section 5).'
status: draft
```
