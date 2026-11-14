# Slow every morning in a DPM cluster

## Prompt
- Cluster vdi-operations-02: 10 hosts, DRS fully automated, Distributed Power Management (DPM) automatic at the default threshold.
- Users complain every weekday between about 07:45 and 08:45. After 09:00 there are no complaints.
- Cluster CPU demand over 24 hours averages 35%.
- A typical weekday, from vCenter and VCF Operations:

| Time | Hosts powered on | CPU demand, % of the powered-on hosts | Highest VM CPU Ready (%) | VMs with CPU Ready above 5% |
|---|---|---|---|---|
| 06:00 | 4 | 41 | 0.9 | 0 |
| 07:30 | 4 | 78 | 5.8 | 37 |
| 08:00 | 4 | 93 | 14.2 | 214 |
| 08:20 | 6 | 71 | 8.7 | 96 |
| 08:45 | 8 | 57 | 3.1 | 12 |
| 09:30 | 10 | 47 | 1.1 | 0 |

- The service owner proposes buying two more hosts.

Which statements are correct?

- A. The cluster runs out of CPU every weekday morning, so two more hosts are the lasting fix for the slowness.
- B. Overnight DPM put 6 of 10 hosts in standby; the load rises faster than they return, so the 4 hosts left on contend.
- C. Without predictions, DPM powers a host on only after demand passes its target, and boot plus vMotion then take minutes.
- D. DPM learns the weekday ramp from its demand history and wakes the standby hosts before 07:30 without any help.
- E. With all 10 hosts on, demand is 47% and Ready is normal, so the cluster is not short of capacity.
- F. Two added hosts would also be put in standby overnight, so they would not remove the morning wait.
- G. A 24-hour average of 35% shows the cluster has ample headroom, so the morning complaints point outside vSphere.
- H. A Scheduled Task that deactivates DPM before 07:00 on weekdays powers on all standby hosts ahead of the ramp.
- I. A higher value of the DPM option MinPoweredOnCpuCapacity keeps more CPU capacity powered on through the night.
- J. Predictive DRS with VCF Operations as its data provider lets DPM bring hosts out of standby before the predicted demand.
- K. The fix is proven only when VM CPU Ready stays low across the whole 07:30-09:00 ramp, not in an hourly average.

## Likely wrong answer
- A: "The cluster runs out of CPU in the morning: buy two more hosts."
- D: "DPM knows the daily pattern and wakes the hosts in time."

## Expected key points
- Answer: B, C, E, F, H, I, J, K.
- A false: the contention appears only while the powered-on host count climbs; with all hosts on, Ready is normal. It is power-on lag, not a shortage.
- B true: 4 hosts at 93% at 08:00 with 214 VMs above 5% Ready; the count rises to 10 only by 09:30.
- C true: DPM is reactive without predictions: power on through IPMI, iLO or Wake-on-LAN, boot ESXi, reconnect, HA agent, then DRS vMotion. Here about an hour until all 10 hosts carry load.
- D false: the historical demand DPM considers sizes the spare capacity it keeps; it does not forecast a daily ramp unless Predictive DRS feeds it predictions.
- E true: the signature of power-on lag: normal VM CPU Ready once all hosts are on.
- F true: DPM puts new hosts in standby during the quiet hours as well.
- G false: the daily average hides the morning hour; Ready of the VMs at 08:00 shows the wait.
- H true: deactivating DPM with Scheduled Tasks powers on all standby hosts; reactivate it in the evening.
- I true: MinPoweredOnCpuCapacity (default 1 MHz) sets the minimum CPU capacity DPM keeps powered on.
- J true: with Predictive DRS on and VCF Operations registered as the data provider, DPM can bring hosts back before demand rises.
- K true: the proof that the fix works is low Ready across the ramp window; an hourly or daily average would hide a remaining wait.

## Notes
- DPM: vSphere 9.1 Resource Management, Managing Power Resources (DPM consolidates VMs and puts hosts in standby; powers hosts on when demand rises).
- The other fixes of the old key (a more conservative DPM threshold, no DPM on this cluster) are left out to keep the option count moderate; both stay valid.
- Converted from judged to multiple choice (Q199 F, 2026-11-14).

## Metadata
```yaml
id: "0238"
title: "Slow every morning in a DPM cluster"
product: [vsphere, vcf-operations]
technology: [system, cpu]
task: troubleshoot
level: 400
answer_type: deterministic
answer: [B, C, E, F, H, I, J, K]
misconception: [A, D]
input: [text]
object: [cluster, esxi, vm]
tool: [vcenter, vcf-operations]
knowledge:
  - vsphere/object-types/cluster/concepts/dpm
  - vsphere/object-types/cluster/concepts/cluster-operations
  - vsphere/object-types/cluster/concepts/cluster-utilization-vs-contention
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
knowledge_main: vsphere/object-types/cluster/concepts/dpm
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
misconception_type: [average-hides-worst, provider-vs-consumer]
status: reviewed
```
