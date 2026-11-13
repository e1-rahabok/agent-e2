# Population alert: value type for a host

## Prompt
- VCF Operations. An alert definition has the ESXi host as its base object.
- The alert must be generated when more than 30% of the VMs running on the host meet a VM CPU Ready condition. One struggling VM must not generate it.
- Hosts run between 20 and 400 VMs, and VMs move between hosts with DRS.
- The symptom set is defined on the VMs, which are a child object type of a host.

Which setting of the symptom set implements this?

- A. Defined on Child (Virtual Machine), value type Any.
- B. Defined on Child (Virtual Machine), value type All.
- C. Defined on Child (Virtual Machine), value type Count, operator ">", value 30.
- D. Defined on Child (Virtual Machine), value type Percent, operator ">", value 30.
- E. Defined on Self, value type Percent, operator ">", value 30.

## Likely wrong answer
A (Any, which fires on a single VM) or C (a count of 30 VMs, which is a different share on every host size).

## Expected key points
- Answer: D.
- Any means one or more related objects meet the condition: one VM is enough, which the requirement excludes.
- All means every related object meets it: far stricter than 30%.
- Count is an exact number of related objects. 30 VMs is 150% of a 20-VM host (it can never fire) and 7.5% of a 400-VM host. The count does not follow the host size.
- Percent is the share of the related objects that meet the condition, so it follows host size and VM moves.
- Self is the base object itself (the host), not its VMs.

## Notes
- Public source: VMware Aria Operations 8.18, "Creating Alert Definitions" (https://techdocs.broadcom.com/us/en/vmware-cis/aria/aria-operations/8-18/vmware-aria-operations-configuration-guide-8-18/configuring-alerts-and-actions/alert-definitions/creating-alert-definitions.html), last updated 2026-05-20: Self, Child ("a virtual machine is a child of a host system"), Descendant, and the value types Count (exact number), Percent (percentage of total related objects), Any (one or more) and All. VCF Operations 9.1, "Add a Virtual Machine CPU Usage Symptom to the Alert Definition" (last updated 2026-11-12), uses Child with Percent and operator ">" for a share of VMs.
- Why one answer: the definitions of the four value types are in the vendor text; only Percent with ">" gives a share that follows a varying VM count.
- Debatable risk: Descendant would also reach the VMs of a host, so the options use Child only. The 9.1 pages did not repeat the definitions of the value types; the 8.18 page is the verbatim source.

## Metadata
```yaml
id: "0314"
title: "Population alert: value type for a host"
product: [vcf-operations, vsphere]
technology: [cpu, system]
task: judge-setting
level: 300
answer_type: deterministic
input: [text]
object: [esxi, vm]
tool: [vcf-operations]
knowledge:
  - vcf-operations/alert-definitions
  - vsphere/object-types/esxi/esxi-alerts
  - vsphere/object-types/cluster/cluster-alerts
knowledge_main: vcf-operations/alert-definitions
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
answer: [D]
misconception: [A, C]
misconception_type: [average-hides-worst]
status: draft
```
