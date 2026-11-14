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

What causes the morning slowness? Is more hardware the answer? What do you change?

## Likely wrong answer
"The cluster runs out of CPU in the morning: buy two more hosts."

## Expected key points
- The cause is DPM: overnight it put 6 of the 10 hosts in standby. The morning load rises faster than the hosts come back, so the 4 hosts left on run at 93% and the VMs wait (CPU Ready).
- A host in standby takes minutes to come back (power on, boot, reconnect, HA agent), and DRS then moves VMs to it: here about an hour until all 10 hosts carry load.
- DPM powers hosts on only after demand rises above its target; with boot and migration time the hosts arrive after the ramp. It does not anticipate a daily ramp unless Predictive DRS gives it a VCF Operations forecast.
- Not a capacity shortage: with all 10 hosts on, demand is 47% and Ready is normal. The 24-hour average (35%) hides the morning hour. More hosts would also be put in standby overnight.
- Fix: have the hosts on before the ramp, for example a scheduled task that turns DPM off before 07:00 on weekdays (this powers on all standby hosts) and back on in the evening; or Predictive DRS with VCF Operations; or a minimum powered-on capacity (the DPM option MinPoweredOnCpuCapacity); or a more conservative DPM threshold; or no DPM on this cluster.
- Then check that Ready stays low from 07:30 to 09:00.

## Notes
- DPM: vSphere 9.1 Resource Management, Managing Power Resources (DPM consolidates VMs and puts hosts in standby; powers hosts on when demand rises).

## Metadata
```yaml
id: "0238"
title: "Slow every morning in a DPM cluster"
product: [vsphere, vcf-operations]
technology: [system, cpu]
task: troubleshoot
level: 400
answer_type: judged
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
