# Keeping a business application current without manual edits

## Prompt
- In VCF Operations 9.1 a business application was created manually, with a Web tier of VMs added one by one.
- New web VMs are deployed every week by automation. Their names all start with the same prefix and they all sit in one vSphere VM folder.
- The application owner is tired of asking the operations team to edit the business application each time.

What can the operations team change in VCF Operations so that new web VMs show in the business application without a manual edit? State the mechanism and what it rests on.

## Likely wrong answer
"Tiers are dynamic; the VM appears once vCenter reports it." Or: only a script against the API can do this.

## Expected key points
- Tier members of a manually created business application are static, so adding more VMs one by one does not scale.
- A custom group can be added to the business application directly, or nested under it, without being placed in a tier.
- A custom group can be dynamic: its membership criteria (for example object type, object name matching a prefix, properties, tags or relationships) are re-evaluated by VCF Operations and the members updated from the search results.
- So: create a custom group of VMs with membership criteria that match the web VMs (for example a name that starts with the prefix), and add that group to the business application in place of the single VMs.
- Optional, not required: a business application created by VCF Operations itself follows the real application without manual edit.

## Notes
- Public source: Broadcom TechDocs, VCF 9.1, "Add Business Application": custom groups can be dragged to the business application without a tier, nested, and tier objects are static if created manually. https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-0/workload-monitoring-and-observability/configuring-business-applications/add-business-application.html (9.0 and 9.1 pages last updated 2026-11-09 and 2026-11-12).
- Public source: Broadcom TechDocs, VCF Operations 9.1, "Managing Custom Object Groups in VCF Operations" and "Custom Object Groups Workspace": dynamic groups use membership criteria (object type, metrics, relationships, properties, name, tags); VCF Operations discovers matching objects and updates the group members. https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/inventory-management/configuring-objects/object-discovery/managing-custom-object-groups.html
- Why one answer: the documented combination (dynamic custom group, added to the application) is the product's own way; the key points do not ask for an exact criterion.
- Debatable risk: the exact refresh time of a dynamic group was not found in the docs and is not asked. An answer that suggests the discovered-application route is accepted as an extra, not required. Not verified: a page that states in one sentence that a dynamic group inside a business application follows its membership; this follows from the two documented facts.

## Metadata
```yaml
id: "0279"
title: "Keeping a business application current without manual edits"
product: [vcf-operations, vsphere]
technology: [system]
task: judge-setting
level: 300
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
misconception_type: []
status: draft
```
