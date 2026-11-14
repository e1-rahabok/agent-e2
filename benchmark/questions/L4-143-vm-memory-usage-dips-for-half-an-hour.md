# VM memory usage dips for half an hour in VCF Operations

## Prompt
See [the VCF Operations memory charts of the VM](0397/vcf-operations-vm-memory-guest-data-gap-2h.png).

- A Windows Server VM runs a file and print service; nothing changed in the application that day.
- The capacity team sees its Memory Usage (%) drop sharply for about half an hour and then come back. They propose to downsize the VM to the low value.

Which statements are correct?

- A. During the dip, Usage (%) matches Active as a share of the VM's total memory.
- B. During the dip, Workload (%) rises to match Consumed as a share of the VM's total memory.
- C. Guest Needed Memory has no values in the minutes of the dip.
- D. The application freed memory during the dip and took it back afterwards.
- E. The VM's memory history in VCF Operations is unreliable for the whole day.
- F. Downsize the VM to the Usage (%) value of the dip.
- G. ESXi took memory from the VM during the dip, which lowered its Usage (%).

## Input to supply
- Product: VCF Operations 9.1; a Windows Server VM with VMware Tools, 8 GB or more, whose guest uses much of its memory as cache (Needed Memory well above Active).
- Lab step: stop the VMware Tools service in the guest (`net stop vmtools`) for 25-35 minutes, then start it again. Change nothing else on the VM.
- Screen: VCF Operations > the VM > Metrics, a 2-hour window around the stop, six charts stacked: Memory|Usage (%), Memory|Workload (%), Guest|Needed Memory (KB), Memory|Non Zero Active (KB), Memory|Consumed (KB), Memory|Total Capacity (KB). Save as `benchmark/questions/0397/vcf-operations-vm-memory-guest-data-gap-2h.png`.
- Condition the key depends on, in the points of the stop:
  - Guest|Needed Memory has no data points;
  - Usage (%) within 2 points of Non Zero Active / Total Capacity × 100, and at least 20 points below its value before the stop;
  - Workload (%) within 3 points of Consumed / Total Capacity × 100, and above its value before the stop;
  - Consumed flat (within 5%) across the whole window.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
D: "Memory usage fell, so the application released memory for half an hour." Or F: downsizing on the dip.

## Expected key points
- Answer: A, B, C.
- A true: without guest data, VCF Operations Usage (%) falls back to Active; the dip equals Active against total memory.
- B true: without guest data, Workload (%) falls back to Consumed; it rises to Consumed against total memory while Usage falls.
- C true: the gap in Needed Memory is the missing guest data that triggers both fallbacks; VMware Tools derives Needed Memory inside the guest.
- D false: the guest did not change; the source of the metric changed. Needed Memory has no values, and Usage returns as soon as guest data does.
- E false: over-correction. Only the points without guest data use the fallback; before and after, the metrics read the guest as usual.
- F false: the wrong action. Without guest data there is no Needed Memory and so no sizing; the dip shows Active, which does not stand in for the guest's need.
- G false: Consumed stays flat through the dip, so ESXi reclaimed nothing; Usage moved because its source moved.

## Notes
- Paired with 0396 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item D8.
- The stem does not name the stopped service: the gap in Needed Memory on the screen is the evidence to read.
- Never attach the knowledge-base image of the same fallback (vcf-operations-vm-memory-usage-falls-back-to-active.png); the capture must be new.
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
misconception: [D]
misconception_type: [layer-confusion, tool-confusion]
pair: "0396"
status: awaiting-input
```
