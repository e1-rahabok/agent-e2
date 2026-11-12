# VM memory usage at 100% after an agent install

## Prompt
- A Windows Server domain controller VM with 4 GB of memory. Light load.
- At 10:00 the team installed a monitoring agent in the guest. It collects Windows counters every 5 minutes.
- Soon after, the vCenter alarm "Virtual machine memory usage" fired on the VM.
- [The attached vSphere Client export](0151/vm-memory-past-day.csv) is the VM's Past Day memory chart (5-minute samples).
- Inside Windows, sampled at 15:00 and at 20:00: In Use about 1.6 GB, Available about 2.3 GB, hard page faults near 0 per second.
- The VM owner asks for 4 GB more memory "because vCenter shows the VM at 100% for half a day".

What do you tell the owner, and why?

## Likely wrong answer
"Memory usage has been at 100% for 12 hours and the alarm fired: the VM is out of memory. Add the 4 GB."

## Expected key points
- Do not add memory: Windows has about 2.3 GB available and does not page. The guest is not short.
- The chart's Usage follows Active, a sampled estimate of recently touched pages. It jumped to about 100% when the agent started and stayed there until 22:30: the sampling can go wrong, or the agent touched memory widely. Either way, it is not what Windows needs.
- Consumed did not change: the guest did not take more memory.
- The alarm is built on that same Usage counter, so it fired on the sampling, not on a shortage. Size and alert on the Guest OS counters (available memory, page faults) instead.

## Notes
- From the knowledge base, Guest OS memory vs VM memory, section Example: Guest OS more accurate (an Active Directory server, a Telegraf-based agent every 5 minutes, VM Active at 100% for more than 12 hours, a vCenter alarm).
- The vCenter alarm "Virtual machine memory usage" reads the VM memory Usage counter (vSphere Monitoring and Performance, default alarms).

## Metadata
```yaml
id: "0151"
title: "VM memory usage at 100% after an agent install"
product: [vsphere, windows]
technology: [memory]
task: troubleshoot
level: 300
answer_type: judged
input: [table]
object: [vm, guest-os]
tool: [vcenter, guest-os-tools]
knowledge:
  - vsphere/technology/memory/concepts/guest-os-vs-vm-memory
  - vsphere/technology/memory/metrics/virtual-motherboard/active
  - vsphere/technology/memory/metrics/virtual-motherboard/usage
knowledge_main: vsphere/technology/memory/concepts/guest-os-vs-vm-memory
attachments:
  - 0151/vm-memory-past-day.csv
origin: synthetic
source_path: "Drafted by Claude 2026-11-12 for the memory slots (project/plan.md, M2)"
misconception_type: [layer-confusion, consumption-as-contention]
status: draft
```
