# Getting 2-second ESX Top data in VCF Operations 9.1

## Prompt
- VCF Operations 9.1 with the Real-Time Metrics component deployed. Host H7 runs 40 VMs, among them the web VMs of one application.
- The application team reports freezes of 1 to 3 seconds at about 03:00 last night and again at about 10:15 this morning, on VMs of H7.
- It is now 14:30. In Troubleshooting Workbench, Real Time Analysis, Overview, the CPU Ready chart of H7 over the last 12 hours is smooth, with no peak at either time.
- The monitoring policy that applies to H7 had no ESX Top setting until a colleague activated ESX Top for the object types Host System and Virtual Machine at 09:00 this morning.
- The 20-second data of last night is still kept in VCF Operations.
- Cluster C2, which holds H7 and 7 other hosts, also shows nothing in its charts at either time.
- The administrator has opened the Top N tab for the VMs of H7, for 10:00 to 10:30.

Which statements are correct?

- A. Now that ESX Top is activated, the ESX Top view set around 03:00 shows the 2-second values of the night freeze.
- B. The smooth 12-hour Ready chart proves that no Ready burst happened on H7 at 03:00 or at 10:15.
- C. For the 10:15 freeze, 2-second data of H7 exists, because ESX Top had been activated at 09:00.
- D. The Overview shows 20-second data unless the ESX Top view is selected, which is why the chart looked smooth.
- E. In the ESX Top view a range longer than 6 hours gives an error, so 08:00 to 14:30 fails while 09:00 to 14:30 works.
- F. Once ESX Top is activated, the Top N tab lists the 2-second spikes of the VMs on H7 for any time after 09:00.
- G. The charts of cluster C2 can show the 1-3 second burst once ESX Top is activated on the hosts of the cluster.
- H. A Custom Query on `cpu.ready.HOST{feature='ESX_TOP'}` returns the 2-second line; unfiltered, both tiers return.
- I. 2-second data is about 10 times the volume of 20-second data, so keep ESX Top to the hosts under investigation.
- J. Last night's 20-second data in VCF Operations averages a freeze of 1 to 3 seconds away in each point.
- K. A 2-second Ready value can be judged against the alert bands that were set on 20-second Ready peaks of the same VMs.
- L. The 2-second tier carries every metric of the 20-second tier for hosts and VMs, at ten times the resolution.

## Answers
C, D, E, H, I, J

## Explanation
- A is wrong: ESX Top is a collection setting; 2-second data exists only from its activation at 09:00. The 03:00 freeze cannot be shown at 2 seconds.
- B is wrong: the chart was 20-second data; a burst of 1-3 seconds averages away. No 2-second data is not proof that no burst happened.
- C is correct: Real-Time Metrics is deployed and the policy for H7 had ESX Top Activated, for hosts and VMs, from 09:00.
- D is correct: the ESX Top view must be selected in the view dropdown; it is not the default.
- E is correct: 6.5 hours errors (and has no 2-second data before 09:00); 5.5 hours works. A short range around 10:15 is best.
- F is wrong: Top N always uses 20-second data, even with ESX Top activated, so its values for 10:00 to 10:30 match the Overview.
- G is wrong: cluster and datacenter have 60-second and 5-minute data only; read the host and VM objects.
- H is correct: a metric with both tiers returns two lines; filter by feature.
- I is correct: limit collection so the monitored system is not loaded.
- J is correct: each 20-second point is an average; 5-minute data averages the burst away even more.
- K is wrong: shorter samples read higher; bands set on 20-second peaks do not apply to 2-second values.
- L is wrong: the 2-second tier is an esxtop subset of about 21 metrics.
- Misconception: A: "Select the ESX Top view in the Overview, set a range around 03:00, and read the 2-second values." - F: "Use the Top N tab for the 2-second values." - G: "Read the cluster chart for the 2-second values."

## Notes
- Public source: Broadcom TechDocs, VCF Operations 9.1, "Real-time Data in the Workbench" (page last updated 2026-11-12): ESX Top view must be selected explicitly and needs ESX Top activated in the policy; a range above 6 hours in that view gives an error; Host System and VM objects; Top N always 20-second even when ESX Top is enabled; Cluster and Datacenter 60 s and 5 min; Custom Query feature='ESX_TOP' and feature='TROUBLESHOOTING', two lines when a metric has both tiers. https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/troubleshooting-workbench-home-page/real-time-data-in-troubleshooting-workbench.html
- Public source: Broadcom TechDocs, VCF Operations 9.1, "Real-Time Metrics Details" (policy workspace, updated 2026-11-12): ESX Top, 2 seconds, object type Host System, Activated or Deactivated; Real-Time Metrics must be deployed first. https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/configuring-policies/using-the-monitoring-policy-workspace/policy-workspace/real-time-metrics-policy-workspace.html
- Why A is false: ESX Top is a collection setting with the states Activated and Deactivated, and the data is produced while it is Activated. The pages do not state this in one sentence.
- Debatable risk: if the product kept 2-second data without the setting, A would be true. The page says the ESX Top policy "must be activated for the hosts" for the view, and the policy is a collection setting, so the data is taken to start at activation. The docs give no retention period for either tier, so no option asks for one. The docs differ on whether the policy page names Host System only or also Virtual Machine for the ESX Top view; the stem activates both object types, so C holds under either page.
- Rewritten 2026-11-13 to raise difficulty: two incidents, one before and one after a known activation time, a smooth 12-hour chart, a Top N check and a cluster chart; the generic procedure fails for 03:00 and the 6-hour limit and the explicit view selection decide 10:15.
- Key point dropped as an option: "to catch a repeat of the 03:00 freeze, leave ESX Top activated and look within 6-hour ranges after the next event" (a follow-up step; I and E cover its facts).
- Changed in the 2026-11-15 audit: the stem activates ESX Top for Host System and Virtual Machine (C no longer rests on the open object-type note in vcf-operations/features/real-time-metrics); the 20-second data of the night is a case fact, so J lost its hedge.
- Changed 2026-11-16: the Top N stem line no longer says the values look the same as in the Overview (it interpreted the evidence toward F being false); it states only that the tab is open for 10:00 to 10:30.

## Metadata
```yaml
id: "0277"
title: "Getting 2-second ESX Top data in VCF Operations 9.1"
product: [vcf-operations, vsphere]
technology: [cpu, system]
task: troubleshoot
level: 400
answer_type: deterministic
misconception: [A, F, G]
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
