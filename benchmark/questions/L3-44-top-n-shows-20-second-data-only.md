# Top N in real time analysis shows 20-second data only

## Prompt
- VCF Operations 9.1 with the Real-Time Metrics component deployed.
- In the policy, the Real time metrics tile has ESX Top activated for the object type Host System, and 2-second data shows in the Overview tab for a host.
- An administrator suspects CPU ready bursts of 1 to 3 seconds on some of the 200 VMs in a cluster. In Troubleshooting Workbench, Real Time Analysis, they open the Top N tab to list the VMs with the highest CPU ready.

What data does the Top N tab show?

- A. 2-second data, because ESX Top is activated in the policy.
- B. 20-second data only; 2-second data is not available in Top N.
- C. 2-second data when the time range is 6 hours or less, otherwise 20-second data.
- D. 5-minute data only, as in the dashboards.
- E. 2-second data for VMs and 20-second data for hosts.

## Likely wrong answer
A or C: activating ESX Top in the policy is read as switching the whole Real Time Analysis page to 2-second data.

## Expected key points
- Answer: B.
- Top N always shows 20-second granularity; 2-second metrics are not available in the Top N tab.
- Each 20-second point is an average over 20 seconds, so a burst of 1 to 3 seconds is flattened.
- To see 2-second data, select the ESX Top view in the Overview tab for the host or VM (time range 6 hours or less), or run a Custom Query filtered on the ESX Top feature.

## Notes
- Public source: Broadcom TechDocs, VCF Operations 9.1, "Real-time Data in Troubleshooting Workbench": "Data in the Top N view is always displayed at 20-second granularity" and 2-second interval metrics are not available in the Top N sub-tab. https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/troubleshooting-workbench-home-page/real-time-data-in-troubleshooting-workbench.html (page last updated 2026-11-12).
- Why one answer: the vendor page states the Top N granularity as fixed; the 6-hour limit applies to the ESX Top view of the Overview tab only.
- Debatable risk: none. The prompt does not claim the 20-second tier is real time.

## Metadata
```yaml
id: "0276"
title: "Top N in real time analysis shows 20-second data only"
product: [vcf-operations, vsphere]
technology: [cpu]
task: read-metric
level: 300
answer_type: deterministic
input: [text]
object: [vm, esxi, cluster]
tool: [vcf-operations]
knowledge:
  - vcf-operations/features/real-time-metrics
knowledge_main: vcf-operations/features/real-time-metrics
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
answer: [B]
misconception: [A, C]
misconception_type: [rollup-and-interval]
status: draft
```
