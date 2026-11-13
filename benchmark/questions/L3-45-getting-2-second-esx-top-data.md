# Getting 2-second ESX Top data in VCF Operations 9.1

## Prompt
- VCF Operations 9.1. A host shows a smooth CPU ready line in Troubleshooting Workbench, Real Time Analysis, Overview, over the last 12 hours.
- The application team reports freezes of 1 to 3 seconds at about 03:00 last night on VMs of this host.
- The Real-Time Metrics component is deployed. ESX Top has not been touched in the policy.

What must the administrator do to look at the 3 AM event with 2-second data, and what limits apply? Name each step and limit.

## Likely wrong answer
"Open the Overview chart and zoom in on 03:00; the 20-second real-time data shows the burst." Or: use Top N for the 2-second values.

## Expected key points
- The 20-second data averages the burst away; only the 2-second (ESX Top) data can show a freeze of 1 to 3 seconds.
- In the policy that applies to the host, in the Real time metrics tile, set ESX Top to Activated for the object type Host System. The Real-Time Metrics component must be deployed first.
- In Overview, select the ESX Top view explicitly in the view dropdown; it does not show by default.
- A time range above 6 hours in the ESX Top view gives an error: select a range of 6 hours or less around 03:00.
- 2-second data exists for Host System and Virtual Machine objects. Top N never shows it (20-second only).
- Alternative: Custom Query returns both tiers as two lines; filter on feature ESX_TOP for the 2-second line.
- Data exists only from the time ESX Top was activated, so activation now cannot show last night's event; it can catch the next one.

## Notes
- Public source: Broadcom TechDocs, VCF Operations 9.1, "Real-time Data in Troubleshooting Workbench" (page last updated 2026-11-12): ESX Top view must be selected explicitly and needs the ESX Top category activated in the policy; a range above 6 hours in that view errors; Host System and Virtual Machine objects; Top N 20-second only; Custom Query feature='ESX_TOP' and feature='TROUBLESHOOTING'. https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/troubleshooting-workbench-home-page/real-time-data-in-troubleshooting-workbench.html
- Public source: Broadcom TechDocs, VCF Operations 9.1, "Real-Time Metrics Details" (policy workspace, page last updated 2026-11-12): ESX Top state Activated, object type Host System, 2-second interval. https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/configuring-policies/using-the-monitoring-policy-workspace/policy-workspace/real-time-metrics-policy-workspace.html
- Public source: Broadcom TechDocs, "Deploy Real-Time Metrics" (9.1): Real-Time Metrics must be deployed and enabled before ESX Top can be activated.
- Why one answer: the steps and limits are listed on the vendor pages. The last key point (no history before activation) follows from the data being collected only after activation; it is a consequence, not a documented sentence, so the judge should not require it.
- Debatable risk: the docs differ on whether the policy page names Host System only or also Virtual Machine for the ESX Top view; the key points follow the Workbench page and ask only for Host System in the policy.

## Metadata
```yaml
id: "0277"
title: "Getting 2-second ESX Top data in VCF Operations 9.1"
product: [vcf-operations, vsphere]
technology: [cpu, system]
task: troubleshoot
level: 300
answer_type: judged
input: [text]
object: [esxi, vm]
tool: [vcf-operations]
knowledge:
  - vcf-operations/features/real-time-metrics
knowledge_main: vcf-operations/features/real-time-metrics
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
misconception_type: [average-hides-worst, rollup-and-interval]
status: draft
```
