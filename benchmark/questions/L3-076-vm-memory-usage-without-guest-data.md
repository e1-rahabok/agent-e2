# VCF Operations VM memory without guest data

## Prompt
- A Windows VM with 32 GB of memory. VM Memory|Usage (%) is enabled in the VCF Operations policy and reads about 68% in the hours before.
- The VMware Tools service of the VM stops for about an hour and then starts again.
- VCF Operations keeps collecting from vCenter for the VM during that hour.

Which statements about the VM's memory metrics during that hour are correct?

- A. VCF Operations computes VM Memory Usage (%) from Active memory while guest data is missing.
- B. VCF Operations computes VM memory Utilization (KB) from Consumed memory while guest data is missing.
- C. Guest Needed Memory has no values for that hour.
- D. A drop in VM Memory Usage (%) during that hour shows that the application freed memory.
- E. Every VM metric that VCF Operations shows for that hour falls back to an ESXi counter.
- F. Downsize the VM to the Memory Usage (%) value seen during that hour.
- G. vCenter VM Memory Usage (%) also changes its source while VMware Tools is stopped.

## Answers
A, B, C

## Explanation
- A true: VCF Operations VM Memory Usage (%) comes from Guest Needed Memory and falls back to Active when guest data is not available, so it usually drops.
- B true: VCF Operations VM memory Utilization starts from Guest Needed Memory and falls back to Consumed when guest data is missing, so it usually jumps up: Consumed holds every page the VM has touched and ESXi still backs.
- C true: Needed Memory is derived by VMware Tools inside the guest; with the service stopped there is nothing to collect.
- D false: the drop is the change of source from the guest to an ESXi estimate, not a change in the guest.
- E false: over-correction. Only the metrics built on guest data change source, and only for the points without it: Needed Memory itself has no values (C), and metrics that already come from ESXi keep their source.
- F false: the wrong action. Without guest data there is no Needed Memory and so no sizing; Active and Consumed do not stand in for it. Restore the data first.
- G false: vCenter VM Memory Usage (%) is always Active; VMware Tools plays no part in it.
- Misconception: D: "Memory usage dropped, so the application released memory." Or F: sizing on the low value.

## Notes
- Paired with 0397 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item D8.
- Kept to the two metrics (Usage (%) and Utilization (KB)). Broadcom KB 390432 states both fallbacks without VMware Tools running: Memory|Utilization (KB) = Memory|Consumed (KB) (B), and Memory|Usage (%) prefers Memory|Non Zero Active (KB) (A). F rests on guest-os-sizing (no guest data, no sizing), not on the VCF Operations sizing engine.
- Review fixes 2026-11-15: B moved from Workload (%) to Utilization (KB). The VCF Operations 9.1 metric list (TechDocs, Virtual Machine Metrics, updated 2026-11-12, https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/metric-property-and-alert-definitions/metrics-definitions-in-vrealize-operations-manager/metrics-for-vcenter-server-components/virtual-machine-metrics.html) has no VM Memory|Workload (%); it lists Mem|Utilization (KB) (`mem|vmMemoryDemand`) as the guest OS memory required or the VM's consumption. The fallback to Consumed is in virtual-motherboard/utilization. Key unchanged: A, B, C.
- Changed in the 2026-11-15 audit: stem gives the VM size, the value before the stop and that the metric is enabled in the policy (9.1 has it disabled by default); E reworded to a plausible over-correction (every metric falls back).
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
  - guest-os/system/guest-os-sizing
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/usage
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D8"
misconception: [D]
misconception_type: [layer-confusion, tool-confusion]
pair: "0397"
status: draft
```
