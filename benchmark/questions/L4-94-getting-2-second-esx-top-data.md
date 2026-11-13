# Getting 2-second ESX Top data in VCF Operations 9.1

## Prompt
- VCF Operations 9.1 with the Real-Time Metrics component deployed. Host H7 runs 40 VMs, among them the web VMs of one application.
- The application team reports freezes of 1 to 3 seconds at about 03:00 last night and again at about 10:15 this morning, on VMs of H7.
- It is now 14:30. In Troubleshooting Workbench, Real Time Analysis, Overview, the CPU Ready chart of H7 over the last 12 hours is smooth, with no peak at either time.
- The monitoring policy that applies to H7 had no ESX Top setting until a colleague activated ESX Top for the object type Host System at 09:00 this morning.
- Cluster C2, which holds H7 and 7 other hosts, also shows nothing in its charts at either time.
- The administrator tried the Top N tab for the VMs of H7 at 10:00 to 10:30 and the values look the same as in the Overview.

For each of the two freezes, can the administrator look at 2-second data of H7, how, and what limits apply? Name each step and limit.

## Likely wrong answer
"Select the ESX Top view in the Overview, set a range around 03:00 and around 10:15, and read the 2-second values." Or: use the Top N tab or the cluster chart for the 2-second values. Or: activate ESX Top (it is already activated) and zoom in on 03:00.

## Expected key points
- The 03:00 freeze: 2-second data of H7 can not be shown. ESX Top was activated at 09:00, and 2-second data exists only for the time after activation. The 20-second data of that night, as far as it is kept, averages a freeze of 1 to 3 seconds away, and the 5-minute data does so even more. So the 03:00 event can not be shown at 2 seconds, and the smooth chart gives no proof that it did not happen.
- The 10:15 freeze: the 2-second data exists, because ESX Top was active (Real-Time Metrics deployed, policy with ESX Top Activated for object type Host System applying to H7).
- In Overview, select the ESX Top view explicitly in the view dropdown; it is not the default, and the default chart is 20-second data. This is why the Overview looked smooth.
- Time range: 6 hours or less in the ESX Top view, otherwise an error. Use a short range around 10:15. The range 09:00 to 14:30 is 5.5 hours and works, but 08:00 to 14:30 would error (and has no 2-second data before 09:00).
- Top N shows 20-second data only, even with ESX Top activated, so its values matching the Overview is expected; it cannot show the freeze at 2 seconds.
- Cluster C2 has 60-second and 5-minute data only; a 1 to 3 second burst can not show there. Read the host (and VM) objects.
- Alternative: Custom Query (PromQL) cpu.ready.HOST{feature='ESX_TOP'} returns the 2-second line; without the filter the chart shows two lines (2-second and 20-second) for the metric.
- To catch a repeat of the 03:00 freeze: leave ESX Top activated for the hosts concerned (2-second data is 10 times the volume of 20-second data, so limit it to the hosts under investigation) and look within 6-hour ranges after the next event.

## Notes
- Public source: Broadcom TechDocs, VCF Operations 9.1, "Real-time Data in the Workbench" (page last updated 2026-11-12): ESX Top view must be selected explicitly and needs ESX Top activated in the policy; a range above 6 hours in that view gives an error; Host System and VM objects; Top N always 20-second even when ESX Top is enabled; Cluster and Datacenter 60 s and 5 min; Custom Query feature='ESX_TOP' and feature='TROUBLESHOOTING', two lines when a metric has both tiers. https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/troubleshooting-workbench-home-page/real-time-data-in-troubleshooting-workbench.html
- Public source: Broadcom TechDocs, VCF Operations 9.1, "Real-Time Metrics Details" (policy workspace, updated 2026-11-12): ESX Top, 2 seconds, object type Host System, Activated or Deactivated; Real-Time Metrics must be deployed first. https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/configuring-policies/using-the-monitoring-policy-workspace/policy-workspace/real-time-metrics-policy-workspace.html
- Why one answer: the 10:15 steps and limits are listed on the vendor pages. That no 2-second data exists for 03:00 follows from the setting: ESX Top is a collection setting with the states Activated and Deactivated, and the data is produced while it is Activated. The pages do not state this in one sentence; the judge should treat the 03:00 point as the main trap but accept an answer that says "no 2-second data before the activation" in any wording, and an answer that says "only if the data was collected, which it was not".
- Debatable risk: if the product kept 2-second data without the setting, the 03:00 point would be wrong. The page says the ESX Top policy "must be activated for the hosts" for the view, and the policy is a collection setting, so the data is taken to start at activation. The docs give no retention period for either tier, so the question does not ask for one. The docs differ on whether the policy page names Host System only or also Virtual Machine for the ESX Top view; the key follows the Workbench page and the policy for Host System.
- Rewritten 2026-11-13 to raise difficulty: two incidents, one before and one after a known activation time, a smooth 12-hour chart, a Top N check and a cluster chart; the generic procedure fails for 03:00 and the 6-hour limit and the explicit view selection decide 10:15.

## Metadata
```yaml
id: "0277"
title: "Getting 2-second ESX Top data in VCF Operations 9.1"
product: [vcf-operations, vsphere]
technology: [cpu, system]
task: troubleshoot
level: 400
answer_type: judged
input: [text]
object: [esxi, vm, cluster]
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
