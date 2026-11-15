# VM Memory Usage: vCenter vs VCF Operations

## Prompt
- Both vCenter and VCF Operations show Memory Usage (%) for a VM.
- For one Windows VM with VMware Tools running, the two tools show very different values for the same hour.

Which statements about VM Memory Usage (%) are correct?

- A. VM Memory Usage (%) has the same formula in vCenter and in VCF Operations.
- B. vCenter computes VM Memory Usage (%) from Active memory against the configured memory.
- C. VCF Operations computes VM Memory Usage (%) from the guest's Needed Memory against the VM's total memory.
- D. vCenter VM Memory Usage (%) reads the Windows In Use counter through VMware Tools.
- E. Every VM memory metric in VCF Operations has a formula of its own, unlike its vCenter counterpart.
- F. Cut the VM's memory to the vCenter Usage value, since that is what the guest uses.
- G. Guest Needed Memory includes part of the guest's cache.
- H. The gap between the tools comes from VCF Operations averaging 20-second samples into 5-minute points.

## Likely wrong answer
A: "Same name, same counter: one of the tools must be wrong." Or E, the reverse: every memory metric differs between the tools.

## Expected key points
- Answer: B, C, G.
- A false: one name, two formulas. vCenter reads an ESXi estimate; VCF Operations reads the guest.
- B true: vCenter VM Memory Usage (%) maps to Active, a sampled estimate of recently touched pages, against configured memory.
- C true: VCF Operations Usage (%) = Guest OS Needed Memory / VM Memory Total Capacity × 100, from VMware Tools data.
- D false: Active is an ESXi counter of pages read or written recently; it has no mapping to Windows In Use.
- E false: over-correction. Only some names hide different formulas; VCF Operations Memory Contention, for example, is the vCenter Latency counter.
- F false: the wrong action. Active is an internal kernel estimate and does not see how the guest uses its cache; size the guest from Needed Memory with headroom.
- G true: Needed Memory is derived by VMware Tools, not a Windows counter; it keeps part of the cache, plus a 5% buffer.
- H false: the tools use different formulas (B, C). Averaging cannot turn Active into Needed Memory, and vCenter's own past-day chart also holds 5-minute averages.

## Notes
- Paired with 0395 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item D2.
- Kept to the difference between the tools. The fallback to Active without guest data is the fact of pair D8 (0396, 0397). No option rests on memory Demand (open author question Q221) or on ESX System Usage (Q215, answered 2026-11-15: a VCF Operations metric, not a vCenter counter; no option names it).
- Review fixes 2026-11-15: the option that VCF Operations Memory Contention is the vCenter Latency counter was dropped: it was the counterexample of E (T2); E stays decidable from vm-memory-metrics. Key B, C, F, H → B, C, G (relettered).
- VCF Operations 9.1 metric list (TechDocs, Virtual Machine Metrics, updated 2026-11-12, https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/metric-property-and-alert-definitions/metrics-definitions-in-vrealize-operations-manager/metrics-for-vcenter-server-components/virtual-machine-metrics.html): Memory|Usage (%) (`mem|usage_average`) is among the metrics disabled by default and has no description there. The formula in C is the knowledge base's (virtual-motherboard/usage); the practical 0395 enables the metric before its capture and checks the formula on the screen.
- Written 2026-11-14 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after approval (design.md, section 6.2).

## Metadata
```yaml
id: "0394"
title: "VM Memory Usage: vCenter vs VCF Operations"
product: [vsphere, vcf-operations, windows]
technology: [memory]
task: explain-mechanism
level: 300
answer_type: deterministic
input: [text]
object: [vm]
tool: [vcenter, vcf-operations]
knowledge:
  - vsphere/technology/memory/metrics/virtual-motherboard/usage
  - vsphere/technology/memory/metrics/virtual-motherboard/active
  - vsphere/technology/memory/metrics/comparisons/vm-memory-metrics
  - guest-os/memory/windows-memory
  - guest-os/system/concepts/guest-os-sizing
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/usage
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D2"
answer: [B, C, G]
misconception: [A]
misconception_type: [tool-confusion, layer-confusion]
pair: "0395"
status: draft
```
