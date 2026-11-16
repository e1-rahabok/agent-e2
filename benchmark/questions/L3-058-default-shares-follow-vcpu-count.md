# Default CPU shares after a vCPU downsize

## Prompt
- A 12-vCPU VM has its CPU shares at Normal, the default. It runs on a host where most VMs show CPU Ready of 4-6% per vCPU at the busy hour.
- Its work at the busy hour is steady: about 5 vCPUs' worth.
- The team reduces it to 6 vCPUs in the vSphere Client. The work stays the same.

Which statements about the VM's CPU shares are correct?

- A. At Normal, default CPU shares are 1,000 per vCPU, so the VM held 12,000 shares before the change.
- B. After the resize in the vSphere Client, the VM holds 6,000 CPU shares in total.
- C. Each remaining vCPU gets fewer shares than before, so a downsize makes each vCPU wait longer.
- D. For the same work, the VM now competes with half its shares, so at the busy hour it can get less CPU than it demands.
- E. Shares decide the split only when the host cannot meet the demand of every VM.
- F. After the downsize, Ready and Co-stop should fall: 6 vCPUs find free threads at once more easily than 12.
- G. If Ready rises and Usage falls below Demand after the change, add the 6 vCPUs back.
- H. Shares set by hand (Custom) keep their number when the VM is resized.
- I. If other VMs reserve 80% of the host and use it at the busy hour, this VM's shares still divide the whole host.

## Answers
A, B, D, E, H

## Explanation
- A is correct: Normal is 1,000 shares per vCPU; 12 vCPUs hold 12,000.
- B is correct: a resize in the vSphere Client recalculates default shares from the new vCPU count: 6 x 1,000.
- C is wrong: the misconception. Each vCPU keeps 1,000 shares; what falls is the VM's total.
- D is correct: the total halves while the demand stays at about 5 vCPUs. A VM's shares are shared among its vCPUs, so before the change 12,000 shares covered 5 vCPUs of work; now 6,000 cover the same work. On a contended host its entitlement can fall below its demand: Ready rises and Usage falls below Demand. The guest cannot see that wait, so its run queue need not move.
- E is correct: without contention every VM gets its demand; shares act only when demand exceeds supply.
- F is wrong: over-correction. Downsizing an oversized VM usually lowers Ready and Co-stop, but not when the same work now needs more per vCPU than the VM's shares give it on a contended host.
- G is wrong: the vCPU count was not the constraint. Raise the VM's shares or move it to a less busy host, then check that Ready falls and Usage meets Demand.
- H is correct: only default share levels are recalculated; a custom number stays as set.
- I is wrong: shares divide only what reservations leave; with 80% of the host reserved and in use, shares divide the other 20%.
- Misconception: C: a smaller VM gets fewer shares per vCPU, so a downsize makes each vCPU wait longer. Or the reverse: shares belong to the VM and do not change with its size.

## Notes
- Paired with the practical question 0236 (theory and practical; design.md, section 3.9). Situation numbers differ from 0236 on purpose.
- Vendor sources: VMware vSphere 9.1 product documentation (project/sources/vmware-vsphere-9-1.pdf), vSphere Resource Management > CPU Virtualization: "With the default resource allocation settings, all virtual machines associated with the same ESX host receive an equal share of CPU per virtual CPU." vSphere Automation API (developer.broadcom.com, latest), Shares, level NORMAL: "For CPU: Shares = 1000 * number of virtual CPUs" (https://developer.broadcom.com/xapis/vsphere-automation-api/latest/appliance/data-structures/Vcenter_Settings_V1_Config_Components_Managementcluster_Shares/); vSphere Resource Management, Resource Allocation Shares (Normal: 1,000 shares per virtual CPU).
- Drafted 2026-11-14 for the question pairing plan (item B12). Counts only after the author's approval.
- Changed in the 2026-11-15 audit: F reworded without "always" and "because" (still false); I replaced ("shares guarantee CPU", weak at Level 300) by shares dividing only what reservations leave, with the reserving VMs using their reservations (breaker: a CPU reservation applies only on demand); stale note on the per-VM shares line removed (ready.md is corrected).
- Changed in the 2026-11-16 re-review: C "every downsize" -> "a downsize" and F "will fall" -> "should fall", so the hedge no longer sits only in a true option and the absolutes only in false ones. Truth values unchanged.

## Metadata
```yaml
id: "0365"
title: "Default CPU shares after a vCPU downsize"
product: [vsphere]
technology: [cpu, system]
task: explain-mechanism
level: 300
answer_type: deterministic
input: [text]
object: [vm, esxi]
tool: [vcenter]
knowledge:
  - vsphere/architecture/resource-controls
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - sp5-framework/capacity/rightsizing
knowledge_main: vsphere/architecture/resource-controls
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item B12"
misconception: [C]
misconception_type: [unit-and-normalization]
pair: "0236"
status: draft
```
