# ESXi CPU Demand and Usage: vCenter vs VCF Operations

## Prompt
Both vCenter and VCF Operations show ESXi CPU Demand (MHz) and ESXi CPU Usage (MHz) for a host.

Which statements about these counters are correct?

- A. A counter with the same name in vCenter and in VCF Operations has the same formula.
- B. ESXi CPU Usage (MHz) in VCF Operations is the vCenter counter, averaged over the 5-minute collection cycle.
- C. ESXi CPU Demand (MHz) in VCF Operations includes the host's CPU System Resource Reservation; the vCenter counter does not.
- D. ESXi CPU Demand (MHz) in vCenter includes the kernel's CPU reservation.
- E. ESXi CPU Demand (MHz) in VCF Operations includes the CPU reservations of running VMs.
- F. On a quiet host, ESXi CPU Demand in VCF Operations can sit far above Usage with no CPU contention.
- G. In VCF Operations, ESXi CPU Demand above Usage means VMs are waiting for CPU.
- H. ESXi CPU Usage includes the CPU the kernel uses, for example for vSAN and NSX work.
- I. ESXi CPU Usage (MHz) in VCF Operations leaves out the kernel's work.
- J. ESXi CPU Demand (MHz) in VCF Operations adds each running VM's CPU reservation on top of that VM's demand.

## Likely wrong answer
A: the same name means the same counter, so ESXi CPU Demand matches between the tools. Or the reverse: both counters differ. Only Demand differs.

## Expected key points
- Answer: B, C, E, F, H.
- A false: ESXi CPU Demand has one name and two formulas.
- B true: Usage is one counter; VCF Operations collects the 20-second vCenter samples and stores their 5-minute average.
- C true: VCF Operations takes the operations view (what the host must be able to deliver), so it adds the kernel's reservation; vCenter shows what the scheduler wants now.
- D false: vCenter Demand leaves the kernel reservation out. A host with no VMs shows vCenter Demand flat at 0.
- E true: per running VM, VCF Operations counts the higher of its demand and its reservation, so a reservation above demand shows in host Demand.
- F true: the gap is reserved capacity, not unmet demand.
- G false: in VCF Operations the gap can be reservation alone. Contention is Ready and Co-stop.
- H true: Usage is actual use by VMs and the kernel; a host with no VMs has Usage above 0.
- I false: Usage is the same counter in both tools and includes kernel work.
- J false: per VM it is the higher of the two, not the sum. A VM demanding 4 GHz with a 5 GHz reservation counts 5 GHz, not 9 GHz.

## Notes
- Paired with the screenshot question 0363 (Type 1 know, Type 2 explain; author, 2026-11-14). Wrong here and wrong there: knowledge gap. Right here and wrong there: reading failure.
- The author's answer to Q218 (2026-11-14): vCenter Demand excludes the hypervisor reservation; VCF Operations Demand includes it and, per VM, takes the higher of demand and reservation. The split goes back to vRealize Operations.
- Drafted by Claude 2026-11-14 from the author's sample (origin: synthetic). Counts only after author approval.

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
answer: [B, C, E, F, H]
misconception: [A, G]
misconception_type: [tool-confusion, consumption-as-contention]
pair: "0363"
status: draft
```
