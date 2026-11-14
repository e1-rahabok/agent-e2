# VCF Operations VM memory without guest data

## Prompt
- The VMware Tools service of a Windows VM stops for about an hour and then starts again.
- VCF Operations keeps collecting from vCenter for the VM during that hour.

Which statements about the VM's memory metrics during that hour are correct?

- A. VCF Operations computes VM Memory Usage (%) from Active memory while guest data is missing.
- B. VCF Operations computes VM Memory Workload (%) from Consumed memory while guest data is missing.
- C. Guest Needed Memory has no values for that hour.
- D. A drop in VM Memory Usage (%) during that hour shows that the application freed memory.
- E. The VM's memory history in VCF Operations becomes unreliable for the whole day, before and after the hour.
- F. Downsize the VM to the Memory Usage (%) value seen during that hour.
- G. vCenter VM Memory Usage (%) also changes its source while VMware Tools is stopped.

## Likely wrong answer
D: "Memory usage dropped, so the application released memory." Or F: sizing on the low value.

## Expected key points
- Answer: A, B, C.
- A true: VCF Operations VM Memory Usage (%) comes from Guest Needed Memory and falls back to Active when guest data is not available, so it usually drops.
- B true: VCF Operations VM Memory Workload (%) falls back to Consumed when guest data is missing, so it usually jumps up: Consumed holds every page the VM has touched and ESXi still backs.
- C true: Needed Memory is derived by VMware Tools inside the guest; with the service stopped there is nothing to collect.
- D false: the drop is the change of source from the guest to an ESXi estimate, not a change in the guest.
- E false: over-correction. Only the points without guest data use the fallback source; the points before and after read the guest as usual.
- F false: the wrong action. Without guest data there is no Needed Memory and so no sizing; Active and Consumed do not stand in for it. Restore the data first.
- G false: vCenter VM Memory Usage (%) is always Active; VMware Tools plays no part in it.

## Notes
- Paired with 0397 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item D8.
- Kept to the two metrics (Usage and Workload). The sizing fallback is in 0022 option E; F here rests on guest-os-sizing (no guest data, no sizing), not on the VCF Operations sizing engine.
- Written 2026-11-14 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after approval (design.md, section 6.2).

## Metadata
```yaml
id: "0396"
title: "VCF Operations VM memory without guest data"
product: [vcf-operations, vsphere, windows]
technology: [memory]
task: explain-mechanism
level: 300
answer_type: deterministic
input: [text]
object: [vm]
tool: [vcf-operations, vcenter]
knowledge:
  - vsphere/technology/memory/metrics/virtual-motherboard/usage
  - vsphere/technology/memory/metrics/virtual-motherboard/utilization
  - vsphere/technology/memory/metrics/virtual-motherboard/active
  - guest-os/system/concepts/guest-os-sizing
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/usage
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D8"
answer: [A, B, C]
misconception: [D]
misconception_type: [layer-confusion, tool-confusion]
pair: "0397"
status: draft
```
