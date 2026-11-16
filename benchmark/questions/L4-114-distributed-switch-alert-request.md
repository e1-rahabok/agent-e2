# A request for a distributed switch alert

## Prompt
- One vSphere Distributed Switch (version 9.0, MTU 9000) connects 24 ESXi hosts and has 30 distributed port groups.
- VCF Operations has a red alert on every distributed port group: the share of packets dropped on the port group is above 10%, wait cycle 1. Every ESXi host has its own alert on dropped packets of the physical network, and the infrastructure team and the network team receive them.
- The network team asks for one more alert on the distributed switch itself: the share of packets dropped on the whole switch (all drops divided by all packets of its port groups) above 10%, "so that one alert shows a network problem on the switch".
- In the last 5-minute cycle:
  - The port group PG-Backup carries 2% of all packets of the switch. 15% of its packets were dropped (cause still being traced).
  - The other 29 port groups carry 98% of the packets and dropped 0.05% of them.
  - All 24 hosts show normal values on their physical network.

What would the switch-level alert show in this cycle, and is the alert worth building? Which statements are correct?

- A. About 0.35%: the switch alert stays silent while the red alert on PG-Backup is already on, so it dilutes the fault.
- B. 15%, the value of the worst port group, so it goes red with PG-Backup's alert and gives the team a single place to look.
- C. About 0.55%, the plain average of the 30 port groups: silent at 10%, but an early warning if its value were set at 0.5%.
- D. About 0.35%, silent now, but worth building at 0.3%, because the network team owns the switch and should be alerted at that level.
- E. About 0.35%, so the switch is healthy: PG-Backup's 15% is a short spike to close without opening a ticket.
- F. The switch alert adds nothing: the port groups and hosts it groups already have alerts of their own.

## Likely wrong answer
B or D: a switch is assumed to need its own alert because the network team owns the switch. The share is a weighted figure, so the faulty port group is diluted.

## Expected key points
- Answer: A, F.
- A is correct: a share of packets is weighted by traffic: 2% x 15% + 98% x 0.05% = 0.30% + 0.049% = about 0.35%, far below 10%, while the port group alert on PG-Backup already fires at 15%. The switch value hides the one faulty port group.
- B is wrong: a ratio of totals is weighted by packets, not the worst member; the switch reads about 0.35%, not 15%.
- C is wrong: 0.55% is the plain average of the 30 shares, (15 + 29 x 0.05) / 30; the alert divides all drops by all packets, so it does not compute that, and a port group alert already gives the warning.
- D is wrong: a switch alert at 0.3% sits within 6x of the 0.05% background of the healthy port groups, so it would fire on noise; owning the switch is no reason, because the switch only groups hosts and port groups that have their own alerts.
- E is wrong: a low switch share does not clear a port group; PG-Backup is red on its own alert, and the switch total dilutes it.
- F is correct: a distributed switch is a group of ESXi hosts and port groups, already covered by their alerts; a switch alert would duplicate them or hide the fault in the total.

## Notes
- Public source: no vendor page defines this design. The arithmetic (a ratio of totals is weighted by packets) is mathematics. A distributed switch is the set of hosts and distributed port groups it connects (vSphere Networking, "vSphere Distributed Switch Architecture", Broadcom TechDocs, vSphere 9.0).
- Knowledge file logic: vsphere/object-types/distributed-switch/distributed-switch-alerts, sections "Not alerted" (a distributed switch is a group of ESXi hosts and port groups, already covered by their alerts; a network has no clear 100%) and "Misconceptions"; vsphere/object-types/distributed-port-group/distributed-port-group-alerts (red, share of packets dropped, 10% in the catalog row alert-dpg-dropped-red).
- The question asks about the share defined in the prompt, not a vendor switch metric. vCenter does keep switch-scope drop counters (net.throughput.droppedTx and droppedRx at statistics level 3, vsphere/technology/network/metrics/distributed-switch/packets-dropped): the question is whether an alert on them adds anything, not whether the data exists.
- Audit 2026-11-15: the stem no longer names a misconfigured upstream switch port as the cause (a drop beyond the host is counted only in that switch, packet-drop-accounting); the old A (two facts) was split into A (the diluted value) and F (the redundancy); E (7.5% "shared by the 24 hosts", a throwaway) was replaced with the switch-total misconception.
- Debatable risk: no alert on the switch is a design decision. Option D argues the opposite on ownership. The question avoids a preference by asking what the figure shows and whether it adds information: with the numbers given, D's value of 0.3% is within 6x of the normal background of 0.05%, which the key states as the reason. A reader could still prefer a switch alert for a different failure (a switch-wide setting error); the prompt shows no such case.

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
  - vsphere/technology/network/metrics/distributed-switch/packets-dropped
knowledge_main: vsphere/object-types/distributed-switch/distributed-switch-alerts
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
answer: [A, F]
misconception: [B, D]
misconception_type: [average-hides-worst, same-name-other-object]
status: draft
```
