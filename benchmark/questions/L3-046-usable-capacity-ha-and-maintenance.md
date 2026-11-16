# Usable capacity with HA and a maintenance host

## Prompt
- A new cluster: 8 identical hosts. vSphere HA admission control: cluster resource percentage, failover capacity of one host (12.5% of CPU and memory).
- The design also requires that one host can be in maintenance mode at any time without losing the HA failover capacity.
- Most VMs have no reservations.

Which statements are correct for the capacity plan?

- A. Usable capacity is 6 hosts' worth: one host for HA failover and one for maintenance.
- B. Usable capacity is 7 hosts' worth: the HA host's spare capacity also absorbs a host in maintenance.
- C. With load above about 75% of the 8 hosts' total, a host failure during a maintenance window leaves VMs short of capacity.
- D. HA admission control stops new power-ons once cluster CPU usage passes 87.5%.
- E. Usable capacity is 7 hosts' worth most of the month and 6 only during maintenance windows, so the plan can be set at 7.

## Answers
A, C

## Explanation
- A is correct: 8 − 1 (failover) − 1 (maintenance) = 6 hosts' worth, about 75% of total. HA admission control leaves a host in maintenance out and keeps its failover capacity among the hosts left.
- B is wrong: with one host in maintenance, HA still needs a host's worth of failover among the 7 left; the same host cannot be both.
- C is correct: 75% of 8 hosts is 6 hosts' worth of load; during maintenance 7 hosts carry it, which leaves exactly one spare host's worth. With more load, a host failure during maintenance leaves VMs short.
- D is wrong: HA admission control counts reservations (plus overhead) against the failover capacity, not usage; most VMs here have no reservation, so usage can pass 87.5% with no power-on refused. The capacity process, not admission control, holds the plan.
- E is wrong: usable capacity is a chosen constant. VMs placed in the 7th host's worth have nowhere to go when a maintenance window comes.
- Misconception: B: counting the HA host as the maintenance host. Or E: letting usable capacity move with the calendar.

## Notes
- Synthetic, 2026-11-12. The design rule (one maintenance host on top of HA) is stated in the prompt (benchmark/design.md, section 6.1, F3).
- HA admission control: vSphere 9.1 Availability, Cluster Resources Percentage Admission Control (https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-1/vsphere-availability/creating-and-using-vsphere-ha-clusters/vsphere-ha-admission-control.html).
- Changed in the 2026-11-15 audit: B without its reason clause and C shorter (length and "because" cues); key points one bullet per option.

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
source_path: "Synthetic, 2026-11-12"
misconception: [B, E]
misconception_type: [threshold-transplanted]
status: draft
```
