# VM memory usage dips for half an hour in VCF Operations

## Prompt
See [the VCF Operations memory charts of the VM](0397/vcf-operations-vm-memory-guest-data-gap-2h.png).

- A Windows Server VM runs a file and print service; nothing changed in the application that day.
- The capacity team sees its Memory Usage (%) drop sharply for about half an hour and then come back. They propose to downsize the VM to the low value.

Which statements are correct?

- A. The Needed Memory chart has no points where the dip is.
- B. During the dip, the Usage (%) line sits at the level of the active memory line.
- C. While Usage (%) dips, Utilization rises to about the level of Consumed.
- D. Consumed falls during the dip.
- E. The guest needed less memory for half an hour and then needed it again.
- F. Every Usage (%) value on these charts, before and after the dip too, comes from active memory.
- G. Size the VM down to the lowest Usage (%) on these charts.

## Input to supply
- Product: VCF Operations 9.1; a Windows Server VM with VMware Tools, 8 GB or more, whose guest uses much of its memory as cache (Guest|Needed Memory well above active memory).
- Before the capture: VM Memory|Usage (%) (`mem|usage_average`) is disabled by default in the VCF Operations 9.1 metric list; enable it in the policy at least a day before.
- Lab step: stop the VMware Tools service in the guest (`net stop vmtools`) for 25-35 minutes, then start it again. Change nothing else on the VM.
- Screen: VCF Operations > the VM > Metrics, a 2-hour window around the stop, six charts stacked: Memory|Usage (%), Mem|Guest Active Memory (%), Guest|Needed Memory, Mem|Utilization (KB), Mem|Consumed (KB), Mem|Total Capacity (KB). Save as `benchmark/questions/0397/vcf-operations-vm-memory-guest-data-gap-2h.png`.
- Condition the key depends on:
  - Guest|Needed Memory has no data points during the stop;
  - during the stop, Memory|Usage (%) within 2 points of Mem|Guest Active Memory (%), and at least 20 points below its value before the stop;
  - before and after the stop, Memory|Usage (%) within 2 points of Guest|Needed Memory / Mem|Total Capacity × 100;
  - during the stop, Mem|Utilization (KB) within 5% of Mem|Consumed (KB), and above its value before the stop;
  - Mem|Consumed (KB) flat (within 5%) at every point of the window.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
E: "Memory usage fell, so the application needed less memory for half an hour." Or G: downsizing on the dip.

## Expected key points
- Answer: A, B, C.
- A true: Needed Memory comes from VMware Tools inside the guest; the chart has a gap where the dip is.
- B true: without guest data, VCF Operations Usage (%) falls back to active memory, and the dip sits on the active line.
- C true: without guest data, VM memory Utilization falls back to Consumed, so it rises while Usage falls.
- D false: Consumed is level through the whole window.
- E false: the guest did not change; the source of the metric changed. Usage comes back as soon as guest data does.
- F false: over-correction. Only the points without guest data use the fallback; before and after the dip, Usage matches Needed Memory against Total Capacity.
- G false: the wrong action. Without guest data there is no Needed Memory and so no sizing; the dip shows active memory, which does not stand in for the guest's need.

## Notes
- Paired with 0396 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item D8.
- The stem does not name the stopped service: the gap in Needed Memory on the screen is the evidence to read.
- Never attach the knowledge-base image of the same fallback (vcf-operations-vm-memory-usage-falls-back-to-active.png); the capture must be new.
- Metric names from the VCF Operations 9.1 Virtual Machine metric list (TechDocs, updated 2026-11-12): https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/metric-property-and-alert-definitions/metrics-definitions-in-vrealize-operations-manager/metrics-for-vcenter-server-components/virtual-machine-metrics.html. It has no VM Memory|Workload (%), so the Consumed fallback is read on Mem|Utilization (KB), whose fallback is in virtual-motherboard/utilization.
- Review fixes 2026-11-15: options rewritten as screen readings (A, B, C true; D false), away from the wording of 0396; Workload (%) replaced by Utilization (KB). Key A, B, C → A, B, C.
- The key holds whenever the condition of `## Input to supply` holds.
- Written 2026-11-14 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after approval (design.md, section 6.2).

## Metadata
```yaml
id: "0397"
title: "VM memory usage dips for half an hour in VCF Operations"
product: [vcf-operations, vsphere, windows]
technology: [memory]
task: read-metric
level: 400
answer_type: deterministic
input: [screenshot]
object: [vm]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/memory/metrics/virtual-motherboard/usage
  - vsphere/technology/memory/metrics/virtual-motherboard/utilization
  - vsphere/technology/memory/metrics/virtual-motherboard/active
  - vsphere/technology/memory/metrics/virtual-motherboard/consumed
  - guest-os/system/concepts/guest-os-sizing
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/usage
attachments:
  - 0397/vcf-operations-vm-memory-guest-data-gap-2h.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D8"
answer: [A, B, C]
misconception: [E]
misconception_type: [layer-confusion, tool-confusion]
pair: "0396"
status: awaiting-input
```
