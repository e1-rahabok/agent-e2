# VM memory usage at 100% after an agent install

## Prompt
- A Windows Server domain controller VM with 4 GB of memory. Light load. VMware Tools is running and current.
- At 10:00 the team installed a monitoring agent in the guest. It collects Windows counters every 5 minutes.
- Soon after, the vCenter alarm "Virtual machine memory usage" fired on the VM.
- [The attached vSphere Client export](0151/vm-memory-past-day.csv) is the VM's Past Day memory chart (5-minute samples).
- Inside Windows, sampled at 15:00 and at 20:00: In Use about 1.6 GB, Available about 2.3 GB, hard page faults near 0 per second.
- The VM owner asks for 4 GB more memory "because vCenter shows the VM at 100% for half a day".

Which statements are correct?

- A. Usage has sat at 100% for half a day and the alarm fired, so the VM is out of memory and needs the 4 GB.
- B. Windows has about 2.3 GB available and almost no hard page faults, so the guest is not short of memory.
- C. In vCenter, a VM's memory Usage (%) follows Active, a sampled estimate of recently touched pages.
- D. Active can stay near 100% for hours after an agent starts, without the guest needing any more memory.
- E. Consumed stayed flat through the day, so the guest took no more memory from the host after 10:00.
- F. Consumed close to the configured 4 GB all day shows the VM was already short of memory before the agent.
- G. The alarm is built on the same Usage counter, so it fired on the Active estimate, not on a shortage.
- H. Size this VM, and alert on it, with Guest OS counters such as available memory and paging.
- I. VCF Operations computes VM memory Usage (%) from Active as well, so it would also show 100%.
- J. The Usage (%) in this vCenter chart is computed from Windows In Use, which VMware Tools reports.

## Likely wrong answer
- A: "Memory usage has been at 100% for 12 hours and the alarm fired: the VM is out of memory. Add the 4 GB."

## Expected key points
- Answer: B, C, D, E, G, H.
- A is false: the guest counters show no shortage; the 100% is the Active estimate.
- B is true: 2.3 GB available and no hard paging mean Windows does not need more memory.
- C is true: vCenter UI Usage (%) = Active / configured memory; in the export Usage and Active move together.
- D is true: Active is sampled; the sampling can go wrong, or the agent touched memory widely. It jumped at 10:05 and stayed near 100% until 22:30, while Windows showed about 1.6 GB In Use at 15:00 and 20:00.
- E is true: Consumed sits at about 3.9 GB before and after 10:00.
- F is false: Consumed holds every page the guest has touched, cache included, and does not drop when the guest frees memory; it is not the guest's need.
- G is true: the default alarm "Virtual machine memory usage" reads the VM memory Usage counter.
- H is true: size and alert the Guest OS on its own counters; VM counters describe what ESXi does.
- I is false: VCF Operations VM memory Usage (%) is Guest OS Needed Memory divided by configured memory; it falls back to Active only when guest data is missing, and VMware Tools is running here.
- J is false: vCenter Usage (%) is Active, an ESXi estimate; it does not use Windows counters.

## Notes
- From the knowledge base, Guest OS memory vs VM memory, section Example: Guest OS more accurate (an Active Directory server, a Telegraf-based agent every 5 minutes, VM Active at 100% for more than 12 hours, a vCenter alarm).
- The vCenter alarm "Virtual machine memory usage" reads the VM memory Usage counter (VMware vSphere 9.1 documentation, project/sources/vmware-vsphere-9-1.pdf: Preconfigured vSphere Alarms, Table 474, p. 2140, "Monitors virtual machine memory usage"; the VM counter Usage, Table 444, p. 2101).
- Prompt sharpened: VMware Tools is running, so the option on VCF Operations Usage (%) is decidable.
- Converted from judged to multiple choice (Q199 F, 2026-11-14).

## Metadata
```yaml
id: "0151"
title: "VM memory usage at 100% after an agent install"
product: [vsphere, windows]
technology: [memory]
task: troubleshoot
level: 300
answer_type: deterministic
answer: [B, C, D, E, G, H]
misconception: [A]
input: [table]
object: [vm, guest-os]
tool: [vcenter, guest-os-tools]
knowledge:
  - vsphere/technology/memory/concepts/guest-os-vs-vm-memory
  - vsphere/technology/memory/metrics/virtual-motherboard/active
  - vsphere/technology/memory/metrics/virtual-motherboard/usage
  - vsphere/technology/memory/metrics/virtual-motherboard/consumed
knowledge_main: vsphere/technology/memory/concepts/guest-os-vs-vm-memory
attachments:
  - 0151/vm-memory-past-day.csv
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
misconception_type: [layer-confusion, consumption-as-contention]
status: draft
```
