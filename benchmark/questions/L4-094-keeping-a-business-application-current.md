# Keeping a business application current without manual edits

## Prompt
- In VCF Operations 9.1 the business application "Shop" was created manually (Define Manually). Its Web tier holds the web VMs added one by one.
- Automation deploys web VMs every week into the vSphere folder Shop/Web, on two vCenter instances (two vCenter adapter instances in VCF Operations). Production names are shop-web- plus three digits, for example shop-web-017.
- Test VMs for the same application are deployed by the same automation into the folder Shop/Web-Test of the same vCenter instances. Their names are shop-web-test- plus three digits. They must not appear in the business application.
- Both kinds of VM carry the same vSphere tags. The automation team will not change the tags or the names.
- Retired VMs are deleted by the automation.
- The application owner is tired of asking the operations team to edit the business application each time.

The operations team wants new production web VMs to show in the business application, and the test VMs not, without a manual edit. Which statements are correct?

- A. With Define Manually, a new VM never enters a tier by itself, whatever its folder, tags or name.
- B. Tiers update themselves: a new VM in the folder Shop/Web joins the Web tier once vCenter reports it.
- C. A dynamic custom group of Virtual Machine objects can be attached to the application directly, outside any tier.
- D. A dynamic group rule "Object Name starts with shop-web-" selects the production web VMs and leaves the test VMs out.
- E. A name rule "matches regular expression", such as shop-web- followed by exactly three digits, keeps the test VMs out.
- F. A rule on the vSphere tags of the VMs can separate the production web VMs from the test VMs of the same application.
- G. A single dynamic group can collect VMs from both vCenter adapter instances; its rules are not tied to one of them.
- H. The group workspace can show which objects the rules match before the group is saved.
- I. Keeping a manually created business application current needs a script against the VCF Operations API.
- J. The owner can be promised that a new VM shows in the group within one 5-minute collection cycle of its creation.
- K. A custom group can be nested in a business application, but a business application cannot be nested in a custom group.

## Likely wrong answer
- B: "Tiers are dynamic; the VM appears once vCenter reports it."
- D: "A custom group with the rule Object Name starts with shop-web-."
- I: "This needs a script against the API."

## Expected key points
- Answer: A, C, E, G, H.
- A is correct: tier objects are static when the application is created manually; a VM added later needs a manual edit.
- B is wrong: tiers are added and filled by hand; they have no dynamic membership, unlike a custom group.
- C is correct: a custom group can be dropped on the application directly, or nested; VCF Operations finds the objects that match its rules and updates the members, so the application follows the group.
- D is wrong: shop-web-test-017 also starts with shop-web-, so the prefix rule takes the test VMs too.
- E is correct: a regular expression on the name separates the two schemes (the documented name operators include matches regular expression).
- F is wrong: both kinds carry the same tags; a tag rule separates two sets only when their tags differ.
- G is correct: a group rule runs on the inventory of the object type, so it matches VMs of every vCenter adapter instance.
- H is correct: Preview in the group workspace lists the objects the rules match, before the group is saved.
- I is wrong: a dynamic custom group added to the application does it without a script.
- J is wrong: how soon a dynamic group picks up a new VM is not documented, so no collection-cycle delay can be promised.
- K is wrong: custom groups and business applications can be nested in each other, in both directions.

## Notes
- Public source: Broadcom TechDocs, VCF 9.1, "Add Business Application" (page last updated 2026-11-12): tier objects are static if the application is created manually; custom groups can be dragged onto the application without a tier, nested, or added to applications. https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/workload-monitoring-and-observability/configuring-business-applications/add-business-application.html
- Public source: Broadcom TechDocs, VCF Operations 9.0, "Custom Object Groups Workspace to Create a New Group" (page last updated 2026-11-09): criteria types Metrics, Relationship, Properties, Object Name, Tag; operators is, is not, contains, does not contain, starts with, ends with, does not start with, does not end with, matches regular expression, does not match regular expression; Preview; "Objects to Always Include" and "Objects to Always Exclude"; "Keep group membership up to date". https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-0/infrastructure-operations/inventory-management/configuring-objects/object-discovery/managing-custom-object-groups/custom-groups-workspace/custom-groups-workspace-create-new-group.html
- Public source: Broadcom TechDocs, VCF Operations 9.1, "Managing Custom Object Groups in VCF Operations" (updated 2026-11-12): dynamic, mixed, manual and adapter-managed membership.
- Debatable risk: the criteria page is the 9.0 page; no 9.1 page for it was found, but the 9.1 group page links the same workspace. How several criteria combine (Any or All) is not described on the page, so no option combines a prefix rule with a negative rule. The exclude list is left out of the options: each new test VM would need a manual entry. A Relationship rule on the folder is left out too: the knowledge base does not say whether it separates Shop/Web from Shop/Web-Test.
- Key point not made an option: an application created by VCF Operations itself also follows changes without manual edits (optional in the old key).
- G rests on a line of vcf-operations/dashboards/business-applications that still has an open review note (one custom group rule matching VMs of several vCenter adapter instances). If a live 9.1 instance shows a rule per adapter instance, G flips.
- Changed in the 2026-11-15 audit: level 400 to 300 (product behaviour, no metric mechanism); A, C, G, H paraphrased away from the knowledge-file sentences; I, J, K reworded without the only/must/because cues (J is now a promise the knowledge base says not to make); misconception_type same-name-other-object removed (no label has two meanings here).
- Changed 2026-11-16: K replaced. The old K (group inside the Web tier; the application reads its VMs from its tiers) was not decidable: the knowledge base never says a group cannot sit in a tier, and its second clause was true as written. The new K tests the nesting of groups and applications, false as before.

## Metadata
```yaml
id: "0279"
title: "Keeping a business application current without manual edits"
product: [vcf-operations, vsphere]
technology: [system]
task: judge-setting
level: 300
answer_type: deterministic
answer: [A, C, E, G, H]
misconception: [B, D, I]
input: [text]
object: [vm]
tool: [vcf-operations]
knowledge:
  - vcf-operations/dashboards/business-applications
knowledge_main: vcf-operations/dashboards/business-applications
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
misconception_type: []
status: draft
```
