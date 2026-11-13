# Ballooning on a host with free memory

## Prompt
- A Linux VM has 16 GB of configured memory. Its memory reservation is 0 and its memory limit is 8 GB, set by a former administrator.
- The ESX host has 512 GB of memory and about 40% of it is consumed. No other VM on the host shows ballooning or swapping.
- In vCenter this VM shows Balloon of about 5 GB and Swapped of about 2 GB, and the application on it is slow.
- Inside the VM, the Linux tools report 16 GB of total memory.

Why does this VM balloon and swap on a host with this much free memory? What do you change?

## Likely wrong answer
"Ballooning and swapping happen only when the host is short of memory, so the host or the VM tools are misreporting." Or: "The memory limit is applied only under contention, like shares, so the cause must be somewhere else."

## Expected key points
- The memory limit is an upper bound on the physical RAM the host allocates to the VM. The host enforces it at all times, also when unused memory exists (shares act only under contention; a limit does not).
- The Guest OS does not know the limit. It sees 16 GB, uses it for cache and applications, and touches pages beyond the 8 GB the VM may hold.
- When the VM needs more than its limit, the VMkernel treats it like a VM under contention and reclaims from it: the balloon driver inflates, the guest pages out, and the VMkernel compresses and swaps pages. This explains Balloon and Swapped on a host with free memory.
- Fix: set the memory limit to Unlimited (the effective limit is then the configured 16 GB). If the VM does not need 16 GB, right-size the configured memory instead of capping it.
- Swapped pages come back only when the guest touches them again, so the slowness can last for a while after the limit is removed.

## Notes
- Public source: Broadcom KB 326270, "Impact of virtual machine memory and CPU resource limits" (covers ESXi 7.0 and 8.0; the "Updated On" field is empty). vSphere 9.1 documentation, vSphere Resource Management, "Resource Allocation Limit": "can never allocate more than the limit, even if there are unused resources on the system" (VMware vSphere 9.1 PDF, build of 2026-11-02).
- Why one answer: the documentation states that the limit holds even with unused resources, and the KB states that the guest is unaware and that the VMkernel balloons and swaps. No other cause is consistent with a 40% consumed host.
- Debatable risk: the KB covers ESXi 7 and 8, not 9.1 by name; the 9.1 limit page agrees. The fix has two valid forms (remove the limit, or right-size), and the key points accept both.

## Metadata
```yaml
id: "0291"
title: Ballooning on a host with free memory
product: [vsphere]
technology: [memory]
task: troubleshoot
level: 300
answer_type: judged
input: [text]
object: [vm, esxi]
tool: [vcenter]
knowledge:
  - vsphere/object-types/vm/configuration/resource-settings-guidance
  - vsphere/architecture/resource-controls
  - vsphere/technology/memory/concepts/ballooning
knowledge_main: vsphere/object-types/vm/configuration/resource-settings-guidance
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
misconception_type: [reclamation-as-contention, consumption-as-contention]
status: draft
```
