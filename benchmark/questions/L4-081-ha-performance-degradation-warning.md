# HA warning about performance after a failure

## Prompt
- Cluster prod-cl05: 6 identical hosts, DRS fully automated.
- vSphere HA admission control: cluster resource percentage, failover capacity of one host.
- "Performance degradation VMs tolerate" is set to 0%.
- Most VMs have no reservations. Cluster CPU usage is about 90%.
- The cluster shows a configuration warning about failover performance. New VMs still power on.

Which statements are correct?

- A. The warning means the five hosts left after a failure would need about 108% of their CPU for today's load.
- B. With the setting at 0%, HA admission control blocks new power-ons until usage falls back below the failover capacity.
- C. At 100%, the default, this setting stays silent however high the cluster's CPU usage climbs.
- D. At a threshold of 20% instead of 0%, the same cluster at 90% usage would still raise the warning.

## Likely wrong answer
B: reading the warning as a block on power-ons.

## Expected key points
- Answer: A, C.
- A is correct: 90% of 6 hosts is 5.4 hosts of load; on the 5 hosts left that is 108%. The VMs restart after a failure, then contend.
- B is wrong: the degradation setting only raises a configuration warning; it does not block power-ons, migrations or reservation changes.
- C is correct: the default 100% tolerates any reduction, so it never warns.
- D is wrong: at 20% the tolerated reduction is 20% of the current usage: 5.4 x 0.8 = 4.32 hosts of load, below the 5 hosts left, so no warning.

## Notes
- Synthetic, 2026-11-12. The setting is in admission-control-and-cluster-state, section HA performance degradation threshold (vSphere 9.1 Availability, vSphere HA Admission Control, https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-1/vsphere-availability/creating-and-using-vsphere-ha-clusters/vsphere-ha-admission-control.html).
- 2026-11-15 audit: old C (the failover capacity counts reservations, not usage) dropped, as that fact is kept by 0290 and 0355; old E (needs DRS) replaced by D, the 20% case, which only the reduction formula decides. Letters: A, B unchanged; D -> C; E -> D (new text).

## Metadata
```yaml
id: "0240"
title: "HA warning about performance after a failure"
product: [vsphere]
technology: [system, cpu]
task: decide-capacity
level: 400
answer_type: deterministic
input: [text]
object: [cluster, esxi]
tool: [vcenter]
knowledge:
  - vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
knowledge_main: vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-12"
answer: [A, C]
misconception: [B]
misconception_type: [consumption-as-contention]
status: draft
```
