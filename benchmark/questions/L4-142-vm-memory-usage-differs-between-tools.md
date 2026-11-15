# VM Memory Usage differs between vCenter and VCF Operations

## Prompt
See [the vCenter memory chart of the VM](0395/vcenter-vm-memory-usage-active-consumed-past-day.png) and [the VCF Operations memory charts of the same VM](0395/vcf-operations-vm-memory-usage-needed-24h.png).

- A Windows Server VM with VMware Tools running.
- The owner's capacity report, from VCF Operations, shows the VM's memory usage far higher than the vCenter chart the vSphere team reads. The owner asks which tool is wrong.
- The vSphere team proposes to cut the VM's memory to what vCenter shows it uses.

Which statements are correct?

- A. On the vCenter chart, the Usage line moves with the Active line, not with Consumed.
- B. Dividing the Needed Memory values by Total Capacity gives the VCF Operations Usage (%) line within about two points.
- C. Consumed on the vCenter chart sits below half of the VM's memory.
- D. The two Usage lines read so differently that one of the tools must be reporting wrongly.
- E. VCF Operations shows the higher value because it turns 20-second samples into 5-minute averages.
- F. ESXi did not make the VM wait for memory at any point of the day.
- G. Shrink the VM to about the Active value on the vCenter chart.
- H. The guest is sized on the day's highest Guest Needed Memory, plus headroom.
- I. Consumed close to the VM's memory shows that Windows is using all of it.
- J. Both Usage lines are built from ESXi counters, so neither says what Windows needs.

## Input to supply
- Product: vSphere Client 9.1 and VCF Operations 9.1; a Windows Server VM with VMware Tools, 8 GB or more, running a workload that keeps a large cache (a database or a file server).
- Before the capture: VM Memory|Usage (%) (`mem|usage_average`) is disabled by default in the VCF Operations 9.1 metric list; enable it in the policy at least a day before the 24 hours captured.
- Screen 1: vSphere Client > the VM > Monitor > Performance > Advanced > Memory. Chart Options: timespan Past day; counters Usage (%), Active (KB) and Consumed (KB); target the VM. Save as `benchmark/questions/0395/vcenter-vm-memory-usage-active-consumed-past-day.png`.
- Screen 2: VCF Operations > the VM > Metrics, the same 24 hours, four charts stacked: Memory|Usage (%), Guest|Needed Memory, Mem|Total Capacity (KB), Mem|Contention (%). Save as `benchmark/questions/0395/vcf-operations-vm-memory-usage-needed-24h.png`.
- Condition the key depends on, at every point of the day:
  - vCenter Usage (%) at 15% or less, and within 2 points of Active / configured memory;
  - Consumed at 85% or more of the configured memory;
  - VCF Operations Memory|Usage (%) at 60% or more, and within 2 points of Guest|Needed Memory / Mem|Total Capacity;
  - Mem|Contention (%) 0.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
D: "The same counter cannot read so differently on the same day: one tool is wrong." Or G: Active taken as what Windows uses.

## Expected key points
- Answer: A, B, F, H.
- A true: the vCenter Usage line follows Active against configured memory; Consumed stays high and flat.
- B true: Needed Memory over Total Capacity matches the VCF Operations line within two points: VCF Operations VM Memory Usage (%) = Guest OS Needed Memory / VM Memory Total Capacity × 100.
- C false: Consumed sits at 85% or more of the VM's memory.
- D false: one name, two formulas. Both tools report correctly; they read different layers.
- E false: vCenter's past-day chart holds 5-minute averages too, and averaging cannot turn Active into Needed Memory.
- F true: Memory Contention, the share of time a vCPU waits on page faults ESXi resolves, is 0 at every point.
- G false: the wrong action. Active is a sampled kernel estimate of recently touched pages; a cut to it removes the cache Windows works from.
- H true: Guest OS sizing uses the peak of Needed Memory over the business cycle plus headroom, so the result lands below 100%.
- I false: Consumed counts pages the VM has touched since power-on and ESXi still backs; it is not what Windows uses now.
- J false: over-correction. VCF Operations Usage (%) reads Guest Needed Memory, which VMware Tools collects inside the guest.

## Notes
- Paired with 0394 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item D2.
- Kept to the difference between the tools; the fallback without guest data is pair D8 (0396, 0397). No option rests on memory Demand (Q221, settled 2026-11-15).
- VCF Operations 9.1 metric list (TechDocs, Virtual Machine Metrics, updated 2026-11-12): https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/metric-property-and-alert-definitions/metrics-definitions-in-vrealize-operations-manager/metrics-for-vcenter-server-components/virtual-machine-metrics.html. Guest|Needed Memory, Mem|Total Capacity (KB) and Mem|Contention (%) are enabled; Memory|Usage (%) is disabled by default and has no description there, so the condition checks the formula on the screen.
- Review fixes 2026-11-15: options reworded away from 0394 and turned into screen readings (A, B, F true; C false); Contention 0 at every point. Key A, B, E, G → A, B, F, H.
- The key holds whenever the condition of `## Input to supply` holds.
- Written 2026-11-14 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after approval (design.md, section 6.2).

## Metadata
```yaml
id: "0395"
title: "VM Memory Usage differs between vCenter and VCF Operations"
product: [vsphere, vcf-operations, windows]
technology: [memory]
task: read-metric
level: 400
answer_type: deterministic
input: [screenshot]
object: [vm]
tool: [vcenter, vcf-operations]
knowledge:
  - vsphere/technology/memory/metrics/virtual-motherboard/usage
  - vsphere/technology/memory/metrics/virtual-motherboard/active
  - vsphere/technology/memory/metrics/virtual-motherboard/consumed
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
  - guest-os/system/concepts/guest-os-sizing
  - sp5-framework/observability/collection-interval
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/usage
attachments:
  - 0395/vcenter-vm-memory-usage-active-consumed-past-day.png
  - 0395/vcf-operations-vm-memory-usage-needed-24h.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D2"
answer: [A, B, F, H]
misconception: [D]
misconception_type: [tool-confusion, rollup-and-interval]
pair: "0394"
status: awaiting-input
```
