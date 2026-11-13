# A manually created business application does not follow new VMs

## Prompt
- In VCF Operations 9.1 the business application "Shop" was created manually (Add Applications, Define Manually).
- Its Web tier holds web-01 to web-04, added by drag and drop from the inventory. The four VMs sit in the vSphere VM folder Shop/Web and carry the vSphere tag app=shop.
- A custom group "Shop-DB" was dragged onto the application canvas without a tier. It is a dynamic group with one rule: object type Virtual Machine, Object Name starts with "shopdb-". When it was created it matched shopdb-01 and shopdb-02.
- After that, with nobody opening the business application:
  - automation deploys web-05 into the folder Shop/Web, with the tag app=shop;
  - automation deploys shopdb-03;
  - an administrator renames shopdb-02 to old-shopdb-02 in vCenter.
- The vCenter adapter has collected the new names and VMs, and VCF Operations has re-evaluated the membership of the custom group.

Which statement describes the members of the business application?

- A. Web tier: web-01 to web-05, because folder and tag match. Shop-DB: shopdb-01 and shopdb-03.
- B. Web tier: web-01 to web-04. Shop-DB: shopdb-01 and shopdb-03.
- C. Web tier: web-01 to web-04. Shop-DB: shopdb-01 and shopdb-02, because a group dropped onto a manually created application is copied at that moment.
- D. Web tier: web-01 to web-04. Shop-DB: shopdb-01, shopdb-02 and shopdb-03, because a group never removes members.
- E. Web tier: web-01 to web-05, because the adapter adds new VMs of the same folder to every tier. Shop-DB: shopdb-01, shopdb-02 and shopdb-03.

## Likely wrong answer
A or E: the tier is assumed to behave like a folder, a tag filter or a dynamic group. Or C: the dynamic group is assumed to be frozen once it is placed in a manually created application.

## Expected key points
- Answer: B.
- Objects in a tier are static when the business application is created manually: web-05 is not in the tier until someone edits the application. Folder, tag and name do not move a VM into a tier. A and E are wrong.
- A custom group can be added to a business application directly, without a tier. A dynamic group has membership rules; VCF Operations finds the objects that match and updates the group members. So shopdb-03 joins and old-shopdb-02 (no longer starts with "shopdb-") leaves. C and D are wrong.
- Static membership does not mean a tier is frozen in every way: the Web tier keeps its four VMs.
- To make the Web tier follow new VMs, the VMs have to come from a dynamic custom group, or the application has to be created by VCF Operations itself, whose changes in the actual application are reflected without a manual edit.

## Notes
- Public source: Broadcom TechDocs, VCF 9.1, "Add Business Application" (page last updated 2026-11-12): tier objects are static if the application is created manually, so edit it when the set of objects changes; applications created by VCF Operations reflect changes without manual edits; custom groups can be dragged onto the application without a tier, nested, or added to applications. https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/workload-monitoring-and-observability/configuring-business-applications/add-business-application.html
- Public source: Broadcom TechDocs, VCF Operations 9.0, "Custom Object Groups Workspace to Create a New Group" (page last updated 2026-11-09): criteria types Metrics, Relationship, Properties, Object Name, Tag; operators include "starts with"; section "Keep group membership up to date": for dynamic groups VCF Operations discovers objects that match the rules and updates the group members from the search results. https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-0/infrastructure-operations/inventory-management/configuring-objects/object-discovery/managing-custom-object-groups/custom-groups-workspace/custom-groups-workspace-create-new-group.html
- Why one answer: the vendor page states the static rule for manual tiers; the group page states that dynamic groups are updated from the search results. B is the only option that applies both. The prompt says the re-evaluation has happened, so no timing has to be guessed.
- Debatable risk: no page states in one sentence that a dynamic group placed in a manually created application keeps following its rules; this follows from the group being updated and the application holding the group, not a copy of its members. The refresh interval of a dynamic group is not documented and is not asked.
- Rewritten 2026-11-13 to raise difficulty: two mechanisms in one application (static tier and dynamic group), a leaving member (rename), and folder and tag that match the tier VMs to tempt the reader.

## Metadata
```yaml
id: "0278"
title: "A manually created business application does not follow new VMs"
product: [vcf-operations, vsphere]
technology: [system]
task: explain-mechanism
level: 400
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
misconception: [A, C]
misconception_type: [same-name-other-object]
status: draft
```
