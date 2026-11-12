# HA warning about performance after a failure

## Prompt
- Cluster prod-cl05: 6 identical hosts, DRS fully automated.
- vSphere HA admission control: cluster resource percentage, failover capacity of one host.
- "Performance degradation VMs tolerate" is set to 0%.
- Most VMs have no reservations. Cluster CPU usage is about 90%.
- The cluster shows a configuration warning about failover performance. New VMs still power on.

Which statements are correct?

- A. The warning says that if a host fails, the five that remain could not carry the current usage without the VMs slowing down: about 108% of their CPU.
- B. With the setting at 0%, HA admission control blocks new power-ons until usage falls back below the failover capacity.
- C. The failover capacity of one host counts reservations, so on its own it does not warn about usage; the degradation setting is the check that compares usage with what survives a failure.
- D. At 100%, the default, this setting gives no warning at all.
- E. The setting also works with DRS turned off: HA computes it from the hosts' usage.

## Likely wrong answer
B: reading the warning as a block on power-ons.

## Expected key points
- Answer: A, C, D.
- A: 90% of 6 hosts is 5.4 hosts' worth of load; on 5 hosts that is 108%. VMs restart after a failure, but then contend.
- B is wrong: the setting raises a warning; it does not stop power-ons.
- C: the percentage policy checks reservations (plus overhead) against the capacity left after the failover hosts; VMs without reservations fill the cluster past what survives a failure. The degradation threshold is the setting that looks at usage.
- D: 100% turns the warning off; 0% warns when the usage would exceed the capacity left after a failure.
- E is wrong: the setting needs vSphere DRS to be on.

## Notes
- Drafted 2026-11-12 for the System slots (question set 1.0, plan M2). Outside the knowledge base: the knowledge base has HA admission control but not this setting. Keyed from the vendor documents.
- vSphere HA Admission Control, Performance degradation VMs tolerate: not available unless DRS is on; default 100% gives no warnings; at 0% a warning is generated when cluster usage exceeds the available capacity (vSphere 9.1 Availability, vSphere HA Admission Control, https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-1/vsphere-availability/creating-and-using-vsphere-ha-clusters/vsphere-ha-admission-control.html).

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
source_path: "Drafted by Claude 2026-11-12 for the System slots, outside the knowledge base (question set 1.0)"
answer: [A, C, D]
misconception: [B]
misconception_type: [consumption-as-contention]
status: draft
```
