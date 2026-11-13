# Top N in real time analysis shows 20-second data only

## Prompt
- VCF Operations 9.1 with the Real-Time Metrics component deployed.
- Cluster C1 has 8 hosts and 200 VMs. The policy applied to all 8 hosts has, in the Real time metrics tile, ESX Top activated for the object type Host System. It was activated at 09:00 today.
- The default 5-minute dashboards show CPU Ready of 0.4% on a 4-vCPU web VM, with no alert.
- At 13:40 several web VMs of C1 froze for 1 to 3 seconds. It is now 15:30.
- The administrator selects cluster C1 in Troubleshooting Workbench, Real Time Analysis. They want to find which VMs were hit, using 2-second CPU Ready for the window 13:30 to 14:00.

Which statement is correct?

- A. The Top N tab ranks the VMs of C1 by 2-second CPU Ready for 13:30 to 14:00, because ESX Top has been active since 09:00 and the range is under 6 hours.
- B. The Top N tab ranks VMs on 20-second data only; 2-second CPU Ready for 13:30 to 14:00 comes from the ESX Top view in the Overview of a host or VM, or from a Custom Query filtered on ESX_TOP.
- C. The Top N tab ranks VMs on 20-second data only; the ESX Top view in the Overview of a host can show 2-second CPU Ready for the whole period from 09:00 to 15:30.
- D. A Custom Query on cpu.ready.HOST returns a single 2-second line, because ESX Top is activated; 20-second data is returned only after the activation is removed.
- E. The Overview of cluster C1 with the ESX Top view shows 2-second CPU Ready for 13:30 to 14:00, with the hosts of the cluster added together.

## Likely wrong answer
A: activating ESX Top in the policy is read as switching the whole Real Time Analysis page, Top N included, to 2-second data. Or E: the cluster is the object that was selected, so its chart is assumed to have the same tiers as a host.

## Expected key points
- Answer: B.
- Top N always shows 20-second granularity, even when ESX Top is activated. A is wrong.
- 2-second data (an esxtop subset of about 21 metrics) exists for Host System and Virtual Machine objects. It is shown in the Overview tab, in the ESX Top view that must be selected explicitly in the view dropdown, or by a Custom Query.
- C is wrong: in the ESX Top view a time range above 6 hours gives an error. 09:00 to 15:30 is 6.5 hours; 13:30 to 14:00 is fine.
- D is wrong: for a metric that has both tiers the Custom Query chart shows two lines, 2 seconds and 20 seconds. The filter feature='ESX_TOP' (or Feature equal to ESX_TOP) leaves only the 2-second line.
- E is wrong: cluster and datacenter objects have 60-second and 5-minute data only. A cluster chart cannot show a burst of 1 to 3 seconds; read hosts and VMs.
- The 5-minute 0.4% is an average over 300 seconds, and a 20-second point averages 20 seconds, so both flatten a 1 to 3 second freeze.
- 2-second data exists only for the period after ESX Top was activated (09:00). The incident at 13:40 is inside it.

## Notes
- Public source: Broadcom TechDocs, VCF Operations 9.1, "Real-time Data in the Workbench" (page last updated 2026-11-12): reporting intervals per resource type (Host System and VM 2 s for about 21 metrics, 20 s, 5 min; Cluster and Datacenter 60 s, 5 min); Top N always uses 20-second granularity even when ESX Top is enabled; ESX Top view must be selected explicitly, needs the ESX Top policy activated, and a range above 6 hours gives an error; Custom Query samples cpu.ready.HOST{feature='ESX_TOP'} and {feature='TROUBLESHOOTING'}, two lines when a metric has both tiers. https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/troubleshooting-workbench-home-page/real-time-data-in-troubleshooting-workbench.html
- Public source: Broadcom TechDocs, VCF Operations 9.1, "Real-Time Metrics Details" (policy workspace, updated 2026-11-12): ESX Top, 2 seconds, object type Host System, state Activated. https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/configuring-policies/using-the-monitoring-policy-workspace/policy-workspace/real-time-metrics-policy-workspace.html
- Why one answer: each wrong option contradicts one sentence of the Workbench page: Top N (A), 6-hour limit (C), two lines in Custom Query (D), cluster intervals (E). 09:00 to 15:30 is 6.5 hours, so C fails by arithmetic.
- Debatable risk: the Workbench page's introduction says both Overview and Top N offer 2-second data, but its Top N section says Top N is always 20-second, even when ESX Top is enabled; the question follows the explicit sentence. The policy page names the ESX Top view for Virtual Machine types and the Workbench page names Host System and VM; B says "host or VM", which the Workbench page supports. The metric name cpu.ready.HOST is documented for hosts only, so B does not name a VM metric.
- Rewritten 2026-11-13 to raise difficulty: the Top N fact now sits in a cluster scenario with an activation time, an incident time and a 6.5-hour range, so four documented limits (Top N, 6 hours, two lines, cluster intervals) each carry one wrong option.

## Metadata
```yaml
id: "0276"
title: "Top N in real time analysis shows 20-second data only"
product: [vcf-operations, vsphere]
technology: [cpu]
task: read-metric
level: 400
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
misconception: [A, E]
misconception_type: [rollup-and-interval]
status: draft
```
