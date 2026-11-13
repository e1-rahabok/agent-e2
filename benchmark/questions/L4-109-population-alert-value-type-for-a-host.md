# Population alert: both symptoms on the same VM

## Prompt
- VCF Operations. An alert definition has the ESXi host as its base object. The VMs running on the host are the child object type of the host.
- Requirement: generate the alert when more than 25% of the VMs on the host suffer a CPU problem and a memory problem at the same time, on the same VM: CPU Contention (%) above 3 and Memory Contention (%) above 2. One struggling VM must not generate it, and a CPU problem on some VMs plus a memory problem on other VMs must not generate it.
- Hosts run between 20 and 400 VMs, and DRS moves VMs between hosts.
- A first version used two symptom sets. Set 1 is Defined on Child (Virtual Machine), value type Percent, operator ">", value 25, with the CPU Contention condition. Set 2 is the same with the Memory Contention condition. The two sets must both be true (All).
- That version raised an alert on host esx-07, and the infrastructure team judged it a false alarm. At that moment esx-07 ran 40 VMs. 14 of them had CPU Contention above 3%, 15 had Memory Contention above 2%, 5 had both, and 16 had neither.

Which definition implements the requirement, stays silent on esx-07 and keeps working on every host size?

- A. One symptom set Defined on Child (Virtual Machine), value type Percent, operator ">", value 25, with both conditions in the set and the conditions combined with All.
- B. The same two symptom sets as the first version, but with the sets combined with Any instead of All.
- C. One symptom set Defined on Child (Virtual Machine), value type Percent, operator ">", value 25, with both conditions in the set and the conditions combined with Any.
- D. One symptom set Defined on Child (Virtual Machine), value type Count, operator ">", value 10, with both conditions in the set and the conditions combined with All.
- E. One symptom set Defined on Child (Virtual Machine), value type All, with both conditions in the set and the conditions combined with All.

## Likely wrong answer
B or the first version itself (two sets, each with its own population): each set counts its own VMs, so 14 of 40 (35%) and 15 of 40 (37.5%) both pass and the sets are true together although only 5 VMs (12.5%) have both problems. Or D (a fixed count that does not follow the host size).

## Expected key points
- Answer: A.
- Percent is the share of the related objects that meet the criteria of the symptom set. With both conditions in one set and All inside the set, a VM counts only if it meets both. On esx-07: 5 of 40 = 12.5%, not over 25%, so the alert stays silent.
- Two separate sets each build their own population. The first version passed on 35% and 37.5%, which are different VMs. All between the sets only requires both sets to be true (B and the first version are wrong).
- Any inside the set counts a VM with either problem: at least 15 and up to 24 of 40 VMs on esx-07, so it fires (C is wrong). Any between sets fires too.
- Count is an exact number of VMs. More than 10 is 27.5% on a 40-VM host, 55% on a 20-VM host and 2.5% on a 400-VM host, so it does not follow host size or DRS moves (D is wrong).
- Value type All needs every VM on the host to meet the set, far stricter than 25%; the alert would almost never fire (E is wrong).

## Notes
- Public source: VMware Aria Operations 8.18, "Creating Alert Definitions" (https://techdocs.broadcom.com/us/en/vmware-cis/aria/aria-operations/8-18/vmware-aria-operations-configuration-guide-8-18/configuring-alerts-and-actions/alert-definitions/creating-alert-definitions.html), last updated 2026-05-20: Child is "an object type that is one level below the base object type"; value types Count ("exact number of related objects meet the symptom/condition set criteria"), Percent ("percentage of total related objects meet the symptom/condition set criteria"), Any, All; All and Any inside a set are a Boolean AND and OR; several sets combine with their own All or Any. The condition names CPU Contention (%) and Memory Contention (%) are the VM metrics of VCF Operations.
- Knowledge file logic: the ESXi, resource pool and cluster contention alerts read a share of the member VMs (relation child, population over 25%), with both symptoms in one set and match All inside the set, so one VM must show both the acute and the sustained symptom (catalog thresholds-alerts.yaml, alerts alert-esxi-cpu-contention-red and the memory twins).
- Why one answer: the vendor text defines Percent over the criteria of one set, so the same-VM requirement can only be met by putting both conditions into one set with All; the other options are excluded by esx-07 or by the 20 to 400 VM range.
- Debatable risk: the 9.1 pages do not repeat the value type definitions; the 8.18 page is the verbatim source. The prompt says the VMs are a child type of the host (as the 8.18 page says), so Descendant is not offered. Powered-off VMs in the denominator are not part of the question.
- Rewritten 2026-11-13 to raise difficulty: the old question asked for the value type of one condition. The new one adds a second condition, a failed first version with numbers, and a requirement (same VM) that only the set structure can meet, besides the host-size variation.

## Metadata
```yaml
id: "0314"
title: "Population alert: both symptoms on the same VM"
product: [vcf-operations, vsphere]
technology: [cpu, memory, system]
task: judge-setting
level: 400
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
answer: [A]
misconception: [B, D]
misconception_type: [average-hides-worst]
status: draft
```
