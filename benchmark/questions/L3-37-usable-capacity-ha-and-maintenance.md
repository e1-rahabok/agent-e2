# Usable capacity with HA and a maintenance host

## Prompt
- A new cluster: 8 identical hosts. vSphere HA admission control: cluster resource percentage, failover capacity of one host (12.5% of CPU and memory).
- The design also requires that one host can be in maintenance mode at any time without losing the HA failover capacity.
- Most VMs have no reservations.

Which statements are correct for the capacity plan?

- A. Usable capacity is 6 hosts' worth: one host for HA failover and one for maintenance.
- B. Usable capacity is 7 hosts' worth: the HA host also covers maintenance, because both are spare capacity.
- C. Above about 75% of the 8-host total load, a host in maintenance leaves the 7 others without a spare host's worth of capacity: a host failure in the window would leave VMs short.
- D. The 12.5% is held back on every host: each host keeps one eighth of its CPU and memory idle.
- E. Usable capacity is 7 hosts' worth most of the month and 6 only during maintenance windows, so the plan can be set at 7.

## Likely wrong answer
B: counting the HA host as the maintenance host. Or E: letting usable capacity move with the calendar.

## Expected key points
- Answer: A, C.
- A: 8 − 1 (failover) − 1 (maintenance) = 6 hosts' worth, about 75% of total.
- B is wrong: with one host in maintenance, HA still needs a host's worth of failover among the 7 left; the same host cannot be both.
- C: 75% of 8 hosts is 6 hosts' worth of load; during maintenance 7 hosts carry it, which leaves exactly one spare host's worth. With more load, a host failure during maintenance leaves VMs short.
- D is wrong: the failover capacity is cluster-wide accounting, not an idle slice on each host.
- E is wrong: usable capacity is a chosen constant. VMs placed in the 7th host's worth have nowhere to go when a maintenance window comes.
- HA admission control does not hold the plan by itself: it counts reservations, and most VMs have none. The capacity process holds it.

## Notes
- Drafted 2026-11-12 for the System slots (question set 1.0, plan M2). The design rule (one maintenance host on top of HA) is stated in the prompt (benchmark/design.md, section 6.1, F3).
- HA admission control: vSphere 9.1 Availability, Cluster Resources Percentage Admission Control (https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-1/vsphere-availability/creating-and-using-vsphere-ha-clusters/vsphere-ha-admission-control.html).

## Metadata
```yaml
id: "0233"
title: "Usable capacity with HA and a maintenance host"
product: [vsphere]
technology: [system, cpu, memory]
task: decide-capacity
level: 300
answer_type: deterministic
input: [text]
object: [cluster, esxi]
tool: [none]
knowledge:
  - sp5-framework/capacity/supply
  - vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
  - vsphere/object-types/cluster/decision-tree/can-cluster-take-a-host-out
knowledge_main: sp5-framework/capacity/supply
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12 for the System slots (question set 1.0)"
answer: [A, C]
misconception: [B, E]
misconception_type: [threshold-transplanted]
status: draft
```
