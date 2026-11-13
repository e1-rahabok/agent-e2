# Keeping a business application current without manual edits

## Prompt
- In VCF Operations 9.1 the business application "Shop" was created manually (Define Manually). Its Web tier holds the web VMs added one by one.
- Automation deploys web VMs every week into the vSphere folder Shop/Web, on two vCenter instances (two vCenter adapter instances in VCF Operations). Production names are shop-web- plus three digits, for example shop-web-017.
- Test VMs for the same application are deployed by the same automation into the folder Shop/Web-Test of the same vCenter instances. Their names are shop-web-test- plus three digits. They must not appear in the business application.
- Both kinds of VM carry the same vSphere tags. The automation team will not change the tags or the names.
- Retired VMs are deleted by the automation.
- The application owner is tired of asking the operations team to edit the business application each time.

What can the operations team change in VCF Operations so that new production web VMs show in the business application, and the test VMs do not, without a manual edit? State the mechanism, the criteria and what limits apply.

## Likely wrong answer
"Tiers are dynamic; the VM appears once vCenter reports it." Or: a custom group with the rule "Object Name starts with shop-web-", which also takes the test VMs. Or: only a script against the API can do this.

## Expected key points
- Tier members of a manually created business application are static, so adding or removing VMs by hand does not scale; folder, tag and name do not move a VM into a tier.
- A custom group can be added to the business application directly, or nested, without being placed in a tier. A dynamic custom group has membership rules; VCF Operations finds the matching objects and updates the group members from the search results.
- So: create a dynamic custom group of object type Virtual Machine and add it to the business application (in place of the single VMs, which can then be removed).
- The trap: "Object Name starts with shop-web-" also matches shop-web-test-NNN. The rule must be tighter. The group workspace offers the operator "matches regular expression" (for example the digits after shop-web-), "does not contain" or "does not start with" on the name, or the list "Objects to Always Exclude". Tags can not separate the two kinds, because both carry the same tags.
- The group spans both vCenter instances, because the rules apply to objects of the object type across adapter instances. Use Preview in the group workspace to check the list of matching objects before saving.
- The refresh time of a dynamic group is not documented: a new VM may not show at the next collection, and the answer should not promise it.
- Optional, not required: an application created by VCF Operations itself reflects changes of the real application without manual edits; it depends on what VCF Operations discovers, not on names.

## Notes
- Public source: Broadcom TechDocs, VCF 9.1, "Add Business Application" (page last updated 2026-11-12): tier objects are static if the application is created manually; custom groups can be dragged onto the application without a tier, nested, or added to applications. https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/workload-monitoring-and-observability/configuring-business-applications/add-business-application.html
- Public source: Broadcom TechDocs, VCF Operations 9.0, "Custom Object Groups Workspace to Create a New Group" (page last updated 2026-11-09): criteria types Metrics, Relationship, Properties, Object Name, Tag; operators is, is not, contains, does not contain, starts with, ends with, does not start with, does not end with, matches regular expression, does not match regular expression; Preview; "Objects to Always Include" and "Objects to Always Exclude"; "Keep group membership up to date". https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-0/infrastructure-operations/inventory-management/configuring-objects/object-discovery/managing-custom-object-groups/custom-groups-workspace/custom-groups-workspace-create-new-group.html
- Public source: Broadcom TechDocs, VCF Operations 9.1, "Managing Custom Object Groups in VCF Operations" (updated 2026-11-12): dynamic, mixed, manual and adapter-managed membership.
- Why one answer: the mechanism (dynamic custom group added to the application) is the product's own way. The test-VM trap follows from the prefix: shop-web-test-017 starts with shop-web-. The key accepts any documented operator that separates the two names.
- Debatable risk: the criteria page is the 9.0 page; no 9.1 page for it was found, but the 9.1 group page links the same workspace. How several criteria combine (Any or All) is not described on the page, so the key asks for a tighter name rule, not for a combination. That the object-type rule spans adapter instances is a consequence of rules running on the inventory; the docs do not say it in one sentence, so the judge should not require it. A tag rule on a tag the automation does not set is not possible here, as the prompt says.
- Rewritten 2026-11-13 to raise difficulty: a second set of VMs whose names share the prefix (test VMs) removes the easy prefix rule, tags can not separate them, and the reader must choose an operator and note the undocumented refresh time.

## Metadata
```yaml
id: "0279"
title: "Keeping a business application current without manual edits"
product: [vcf-operations, vsphere]
technology: [system]
task: judge-setting
level: 400
answer_type: judged
input: [text]
object: [vm]
tool: [vcf-operations]
knowledge:
  - vcf-operations/dashboards/business-applications
knowledge_main: vcf-operations/dashboards/business-applications
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
misconception_type: [same-name-other-object]
status: draft
```
