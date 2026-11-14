# Default CPU shares after a vCPU downsize

## Prompt
- A 12-vCPU VM has its CPU shares at Normal, the default. It runs on a host where most VMs show CPU Ready of 4-6% per vCPU at the busy hour.
- Its work at the busy hour is steady: about 5 vCPUs' worth.
- The team reduces it to 6 vCPUs in the vSphere Client. The work stays the same.

Which statements about the VM's CPU shares are correct?

- A. At Normal, default CPU shares are 1,000 per vCPU, so the VM held 12,000 shares before the change.
- B. After the resize in the vSphere Client, the VM holds 6,000 shares.
- C. Each remaining vCPU gets fewer shares than before, so every downsize makes each vCPU wait longer.
- D. For the same work, the VM now competes with half its shares, so at the busy hour it can get less CPU than it demands.
- E. Shares decide the split only when the host cannot meet the demand of every VM.
- F. A downsize always lowers a VM's Ready and Co-stop, because fewer vCPUs fit free threads more easily.
- G. If Ready rises and Usage falls below Demand after the change, add the 6 vCPUs back.
- H. Shares set by hand (Custom) keep their number when the VM is resized.
- I. Shares guarantee the VM a minimum amount of CPU, as a reservation does.

## Likely wrong answer
C: a smaller VM gets fewer shares per vCPU, so a downsize makes each vCPU wait longer. Or the reverse: shares belong to the VM and do not change with its size.

## Expected key points
- Answer: A, B, D, E, H.
- A true: Normal is 1,000 shares per vCPU; 12 vCPUs hold 12,000.
- B true: a resize in the vSphere Client recalculates default shares from the new vCPU count: 6 x 1,000.
- C false: the misconception. Each vCPU keeps 1,000 shares; what falls is the VM's total.
- D true: the total halves while the demand stays at about 5 vCPUs. A VM's shares are shared among its vCPUs, so before the change 12,000 shares covered 5 vCPUs of work; now 6,000 cover the same work. On a contended host its entitlement can fall below its demand: Ready rises and Usage falls below Demand, while the guest run queue stays the same.
- E true: without contention every VM gets its demand; shares act only when demand exceeds supply.
- F false: over-correction. Downsizing an oversized VM usually lowers Ready and Co-stop, but not when the same work now needs more per vCPU than the VM's shares give it on a contended host, as here.
- G false: the vCPU count was not the constraint. Raise the VM's shares or move it to a less busy host, then check that Ready falls and Usage meets Demand.
- H true: only default share levels are recalculated; a custom number stays as set.
- I false: shares are relative and act only on what reservations leave; a reservation is the guarantee.

## Notes
- Paired with the practical question 0236 (theory and practical; design.md, section 3.9). Situation numbers differ from 0236 on purpose.
- Vendor sources: VMware vSphere 9.1 product documentation (project/sources/vmware-vsphere-9-1.pdf), vSphere Resource Management > CPU Virtualization: "With the default resource allocation settings, all virtual machines associated with the same ESX host receive an equal share of CPU per virtual CPU." vSphere Automation API (developer.broadcom.com, latest), Shares, level NORMAL: "For CPU: Shares = 1000 * number of virtual CPUs" (https://developer.broadcom.com/xapis/vsphere-automation-api/latest/appliance/data-structures/Vcenter_Settings_V1_Config_Components_Managementcluster_Shares/); vSphere Resource Management, Resource Allocation Shares (Normal: 1,000 shares per virtual CPU).
- The knowledge base stated in one file that shares are per VM, not per vCPU; that line is being corrected in the same change set (project/question-pairing-2026-11-14.md, section 5). The key rests on resource-controls and ready.
- Drafted 2026-11-14 for the question pairing plan (item B12). Counts only after author approval.

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
answer: [A, B, D, E, H]
misconception: [C]
misconception_type: [unit-and-normalization]
pair: "0236"
status: draft
```
