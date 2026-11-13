# A request for a distributed switch alert

## Prompt
- One vSphere Distributed Switch (version 9.0, MTU 9000) connects 24 ESXi hosts and has 30 distributed port groups.
- VCF Operations has a red alert on every distributed port group: the share of packets dropped on the port group is above 10%, wait cycle 1. Every ESXi host has its own alert on dropped packets of the physical network, and the infrastructure team and the network team receive them.
- The network team asks for one more alert on the distributed switch itself: the share of packets dropped on the whole switch (all drops divided by all packets of its port groups) above 10%, "so that one alert shows a network problem on the switch".
- In the last 5-minute cycle:
  - The port group PG-Backup carries 2% of all packets of the switch. 15% of its packets were dropped (a misconfigured upstream switch port).
  - The other 29 port groups carry 98% of the packets and dropped 0.05% of them.
  - All 24 hosts show normal values on their physical network.

What would the switch-level alert show in this cycle, and is the alert worth building?

- A. About 0.35%, so it stays silent while the red alert on PG-Backup is already on. It dilutes a fault of one port group, and the port groups and hosts it groups have their own alerts, so it adds nothing.
- B. 15%, the value of the worst port group, so it goes red together with the alert of PG-Backup. It is worth building because it gives the team a single place to look.
- C. About 0.55%, the plain average of the 30 port groups, so it stays silent at 10% but would give early warning if its value were set at 0.5%.
- D. About 0.35%, so it stays silent, but it is still worth building with a value of 0.3%, because the switch is the object the network team owns and it should be alerted at the level it manages.
- E. About 7.5%, because the drops are shared by the 24 hosts, so it stays silent now but is the only alert that shows a fault which spreads over several hosts.

## Likely wrong answer
B or D: a switch is assumed to need its own alert because the network team owns the switch. The share is a weighted figure, so the faulty port group is diluted.

## Expected key points
- Answer: A.
- A share of packets is weighted by traffic: 2% x 15% + 98% x 0.05% = 0.30% + 0.049% = about 0.35%. The faulty port group is a small part of the packets, so the switch-level value stays far below 10% (B and C are wrong; C is a plain average that does not weight by traffic).
- The red alert on PG-Backup already fires at 15%, so the network team has the fault where it is.
- A distributed switch is a group of ESXi hosts and port groups, and both already have alerts. A switch alert would duplicate them, or hide the fault in the average. To catch the case it would need a value so low (0.3%) that normal background drops of the other 29 port groups (0.05%) come close to it, and that makes false alarms.
- A network has no clear 100%, so no consumption alert is set either. Contention (dropped packets) is alerted on the objects that own the packets.

## Notes
- Public source: no vendor page defines this design. The arithmetic (a ratio of totals is weighted by packets) is mathematics. A distributed switch is the set of hosts and distributed port groups it connects (vSphere Networking, "vSphere Distributed Switch Architecture", Broadcom TechDocs, vSphere 9.0).
- Knowledge file logic: vsphere/object-types/distributed-switch/distributed-switch-alerts, sections "Not alerted" (a distributed switch is a group of ESXi hosts and port groups, already covered by their alerts; a network has no clear 100%) and "Misconceptions"; vsphere/object-types/distributed-port-group/distributed-port-group-alerts (red, share of packets dropped, 10% in the catalog row alert-dpg-dropped-red).
- Why one answer: the numbers in the prompt give 0.35% for a weighted share, and the redundancy follows from the objects already being covered. The question does not ask about a switch-level metric of a vendor; it asks about the share defined in the prompt.
- Debatable risk: this is the author's design decision (no alert on the switch). Option D argues the opposite on ownership. The question avoids a preference by asking what the figure shows and whether it adds information: with the numbers given, D's value of 0.3% is within 6x of the normal background of 0.05%, which the key states as the reason. A reader could still prefer a switch alert for a different failure (a switch-wide setting error); the prompt shows no such case.

## Metadata
```yaml
id: "0344"
title: "A request for a distributed switch alert"
product: [vcf-operations, vsphere]
technology: [network, system]
task: judge-setting
level: 400
answer_type: deterministic
input: [text]
object: [network, esxi]
tool: [vcf-operations]
knowledge:
  - vsphere/object-types/distributed-switch/distributed-switch-alerts
  - vsphere/object-types/distributed-port-group/distributed-port-group-alerts
  - vsphere/object-types/esxi/esxi-alerts
knowledge_main: vsphere/object-types/distributed-switch/distributed-switch-alerts
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
answer: [A]
misconception: [B, D]
misconception_type: [average-hides-worst, same-name-other-object]
status: draft
```
