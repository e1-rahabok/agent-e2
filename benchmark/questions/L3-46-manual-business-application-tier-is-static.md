# A manually created business application does not follow new VMs

## Prompt
- In VCF Operations 9.1 a business application was created manually (Add, Define Manually). Its Web tier holds 4 VMs added by drag and drop.
- An automation job deploys a fifth web VM into the same vSphere VM folder as the other four, with the same naming pattern.
- Nobody edits the business application.

After the next collection, which statement about the Web tier is correct?

- A. The new VM joins the tier automatically, because it is in the same vSphere folder as the other four.
- B. The new VM is not in the tier until someone edits the business application; tier members of a manually created application are static.
- C. The new VM joins the tier after the next scheduled discovery of the vCenter adapter.
- D. The new VM joins the tier automatically, because its name matches the pattern of the other four.
- E. The new VM joins the tier only if it carries the same vSphere tags as the other four.

## Likely wrong answer
A or D: the tier is assumed to behave like a folder or a dynamic group.

## Expected key points
- Answer: B.
- Objects in a tier are static when the business application is created manually and not by VCF Operations. If the set of objects changes, the application must be edited by hand.
- Folder, name or tag do not move a VM into the tier; only a person (or a custom group, see below) does.
- A custom group can be added to the business application directly or nested under it; a custom group can have dynamic membership criteria.

## Notes
- Public source: Broadcom TechDocs, VCF 9.1, "Add Business Application": the objects in a tier are static if the Business Application is created manually and not by VCF Operations; if the set of objects in a tier changes, you must manually edit the Business Application; if created by VCF Operations, changes in the actual application are reflected without manual edit. https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/workload-monitoring-and-observability/configuring-business-applications/add-business-application.html (page last updated 2026-11-12).
- Why one answer: the vendor page states the rule in one sentence for this exact creation path.
- Debatable risk: a business application that VCF Operations discovers itself behaves differently; the prompt says the application was created manually.

## Metadata
```yaml
id: "0278"
title: "A manually created business application does not follow new VMs"
product: [vcf-operations, vsphere]
technology: [system]
task: explain-mechanism
level: 300
answer_type: deterministic
input: [text]
object: [vm]
tool: [vcf-operations]
knowledge:
  - vcf-operations/dashboards/business-applications
knowledge_main: vcf-operations/dashboards/business-applications
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
answer: [B]
misconception: [A, D]
misconception_type: [same-name-other-object]
status: draft
```
