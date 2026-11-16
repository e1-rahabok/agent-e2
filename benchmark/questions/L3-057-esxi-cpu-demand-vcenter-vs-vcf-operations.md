# ESXi CPU Demand and Usage: vCenter vs VCF Operations

## Prompt
Both vCenter and VCF Operations show ESXi CPU Demand (MHz) and ESXi CPU Usage (MHz) for a host.

Which statements are correct?

- A. A counter with the same name in vCenter and in VCF Operations has the same formula.
- B. On a quiet host, ESXi CPU Demand (MHz) in vCenter sits below ESXi CPU Usage (MHz).
- C. ESXi CPU Demand (MHz) in VCF Operations includes the host's CPU System Resource Reservation.
- D. ESXi CPU Demand (MHz) in vCenter includes the kernel's CPU reservation.
- E. VM CPU Demand does not include the VM's own CPU reservation, in vCenter or in VCF Operations.
- F. On a quiet host, ESXi CPU Demand in VCF Operations can sit far above Usage with no CPU contention.
- G. In VCF Operations, ESXi CPU Demand far above Usage calls for another host in the cluster.
- H. ESXi CPU Usage includes the CPU the kernel uses, for example for vSAN and NSX work.
- I. ESXi CPU Usage (MHz) in VCF Operations also adds the kernel's CPU reservation.
- J. ESXi CPU Demand (MHz) in VCF Operations adds each running VM's CPU reservation to that VM's demand.

## Answers
B, C, E, F, H

## Explanation
- A false: ESXi CPU Demand has one name and two formulas.
- B true: vCenter Demand sums what the VMs ask for, while Usage also holds the kernel's own work, so on a quiet host Demand sits below Usage.
- C true: VCF Operations takes the operations view (what the host must be able to deliver), so it adds the kernel's reservation.
- D false: vCenter shows what the scheduler wants now and leaves the kernel reservation out. A host with no VMs shows vCenter Demand flat at 0.
- E true: VM CPU Demand is what the VM would use with no contention or limit; its reservation is not in it in either tool. The reservation enters only the host Demand of VCF Operations.
- F true: the gap is reserved capacity, not unmet demand.
- G false: in VCF Operations the gap can be reservation alone, which no added host changes. Contention is Ready and Co-stop.
- H true: Usage is actual use by VMs and the kernel; a host with no VMs has Usage above 0.
- I false: Usage is the same counter in both tools; only Demand counts reservations.
- J false: per running VM, VCF Operations counts the higher of the VM's demand and its CPU reservation, not the sum. A VM demanding 4 GHz with a 5 GHz reservation counts 5 GHz, not 9 GHz.
- Misconception: A: the same name means the same counter, so ESXi CPU Demand matches between the tools. Or the reverse, I: both counters differ. Only Demand differs.

## Notes
- Paired with the screenshot question 0363 (theory and practical; author, 2026-11-14). Reading the pair: design.md, section 3.9.
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): C one fact (its clause on vCenter negated D); old G (a reading) is now the wrong action; old I (Usage leaves out kernel work) negated H and is now the over-correction (Usage also counts reservations). Key unchanged.
- The author's answer to Q218 (2026-11-14): vCenter Demand excludes the hypervisor reservation; VCF Operations Demand includes it and, per VM, takes the higher of demand and reservation. The split goes back to vRealize Operations.
- Changed in the 2026-11-15 audit: B (the 5-minute average of Usage, a fact tested in many questions) replaced by vCenter Demand below Usage on a quiet host; E (higher of demand and reservation) replaced by the VM Demand fact, since E and J were the two sides of one rule; J stays as the unit-trap. Level stays 300 (author-set).
- Synthetic, 2026-11-14, from the author's sample. Counts only after author approval.

## Metadata
```yaml
id: "0362"
title: "ESXi CPU Demand and Usage: vCenter vs VCF Operations"
product: [vsphere, vcf-operations]
technology: [cpu]
task: explain-mechanism
level: 300   # author 2026-11-14
answer_type: deterministic
input: [text]
object: [esxi]
tool: [vcenter, vcf-operations]
knowledge:
  - vsphere/technology/cpu/metrics/host/demand
  - vsphere/technology/cpu/metrics/host/usage
knowledge_main: vsphere/technology/cpu/metrics/host/demand
attachments: []
origin: synthetic
source_path: "Author's sample, 2026-11-14 (Q218)"
misconception: [A, G, I]
misconception_type: [tool-confusion, consumption-as-contention]
pair: "0363"
status: draft
```
