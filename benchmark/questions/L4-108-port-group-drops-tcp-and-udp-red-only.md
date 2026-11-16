# Port group drops for TCP and UDP traffic

## Prompt
- VCF Operations. The red alert on distributed port groups fires when the share of dropped packets is above 10%, wait cycle 1.
- VCF Operations showed 12% dropped packets (transmit side) on two port groups, for two consecutive 5-minute cycles. The cause is still being traced:
  - PG-Files carries SMB file copies over TCP. The VMs and the file servers are 1 ms apart (round-trip time) and one copy normally runs at 2 to 5 Gbit/s per flow.
  - PG-Voice carries RTP voice streams over UDP, with about 200 packets per second per call.
- A colleague proposes two changes: (1) mute the red alert on PG-Files, "because TCP resends every dropped packet, so no data is lost"; (2) add an orange alert at 5% on all port groups "to get an early warning before 10%".

Which statements are correct?

- A. TCP resends every dropped segment, so 12% loss on PG-Files costs the file copies no throughput.
- B. Each loss makes TCP shrink its congestion window or wait for a retransmission timeout.
- C. The distributed switch total shows 0.4% dropped in the same cycles, so the 12% on the two port groups is a data error.
- D. If the port group alert is changed to count transmitted packets only, both groups stay above 10% and red.
- E. An orange alert at 5% on all port groups gives the team a reliable early warning before 10%.
- F. On PG-Voice, UDP does not resend, so 12% of the voice packets are lost for good.
- G. Muting PG-Files removes the only alert on that port group: on port groups only dropped packets are alerted.
- H. The VM dropped packets alert counts each VM's received drops too, so it also flags a guest with a full receive ring.
- I. The same 12% hurts both groups, in different ways, so both deserve the red alert.
- J. The 12% is VCF Operations' value for each port group, aggregated over its ports on all hosts; vCenter keeps none.
- K. vCenter keeps drop counters per distributed port, at statistics level 3 and through the API, to find the ports that drop.

## Answers
B, D, F, G, I, J, K

## Explanation
- A is false: the misconception; TCP resends, so the data arrives, but the cost is time: each loss shrinks the congestion window or waits for a retransmit timeout, so the copies slow down or stall.
- B is true: each loss halves the congestion window (RFC 5681) or waits for a retransmission timeout.
- C is false: the switch total divides the drops of every port group by all the switch's packets, so two port groups at 12% read as a small share of the whole switch; a low switch total hides a port group and does not make its value an error.
- D is true: the planned change counts transmitted packets only, because received drops include packets not meant for the VM and full guest receive rings; the 12% here is on the transmit side, so the transmit-only share is at least 12% and both groups stay red.
- E is false: the misconception; on network objects the set is red only, to avoid alert storms, and an orange value gave false positives. Early warning belongs in the daily check.
- F is true: UDP is not resent, so 12% of the packets are lost and nothing recovers them.
- G is true: a network object has no clear 100%, so only contention, dropped packets, is alerted on a port group; muting it leaves PG-Files with no alert, while users see slow or hanging copies.
- H is false: the VM dropped packets alert counts transmitted packets only; received drops are far higher and include drops in a full receive ring, whose cause is in the Guest OS.
- I is true: the same value has a different effect per traffic type, and both are above the damage level.
- J is true: the distributed port group has no vCenter performance counters; VCF Operations aggregates the port group's metrics over the ports on all hosts.
- K is true: vCenter keeps dropped-packet counters on the distributed switch object per DVPort (and per LAG and for the switch), at statistics level 3, readable through the API with no vSphere Client chart; they locate the port that drops.
- Misconception: A: "TCP recovers, so PG-Files is fine and only PG-Voice matters." - C: "The switch as a whole shows almost no drops, so the port group value is wrong." - E: "An orange alert at 5% is a good early warning."

## Notes
- Review 2026-11-14: the stem no longer blames a faulty line card on an upstream switch. A frame dropped beyond the host is counted only in that switch, not by vSphere (vsphere/technology/network/concepts/packet-drop-accounting), so it could not show as 12% on the port groups. The cause stays open; the TCP and UDP effects and the red-only design do not depend on where the drop happens.
- Public source for B and F: RFC 5681 (congestion window reaction to loss) and RFC 768 (UDP has no retransmission); both are also in vm-alerts.
- 2026-11-16 re-review: D (Mathis throughput model) and H (voice loss tolerance) rested on outside TCP and VoIP knowledge and on an MSS the stem did not give; replaced in place with the planned transmit-only count (D, true; distributed-port-group-alerts) and the VM alert's transmit-only count (H, false; vm-alerts). G no longer restates A's negation; it tests that drops are the only port group alert (true). Stem lines "There is no orange alert on port groups" and "red only" removed: they pre-answered E. A and B stay as the misconception and its mechanism.
- Knowledge file logic: vsphere/object-types/distributed-port-group/distributed-port-group-alerts (red only on network objects, TCP cost is time, orange gave false positives); vsphere/object-types/vm/vm-alerts, "VM dropped packets" (congestion window, retransmit timeout; UDP is not resent); vsphere/technology/network/metrics/distributed-switch/packets-dropped (switch, DVPort and LAG counters at level 3; the switch total hides one port; no vCenter port group counter).
- Audit 2026-11-15: C (RTP retransmission, a throwaway beside F) replaced with the switch-total dilution misconception; J (unstable ratio over few packets) and K (receive drops to the Guest OS owner) replaced with the port group aggregate and the DVPort counters, as both facts were over the two-question cap (0061/0082 and 0345/0060 keep them). Stem: the 12% is shown by VCF Operations, as vCenter keeps no port group counter.

## Metadata
```yaml
id: "0346"
title: "Port group drops for TCP and UDP traffic"
product: [vcf-operations, vsphere]
technology: [network]
task: judge-setting
level: 400
answer_type: deterministic
misconception: [A, C, E]
input: [text]
object: [network]
tool: [vcf-operations, vcenter]
knowledge:
  - vsphere/object-types/distributed-port-group/distributed-port-group-alerts
  - vsphere/object-types/vm/vm-alerts
  - vsphere/technology/network/concepts/packet-drop-accounting
  - vsphere/technology/network/metrics/distributed-switch/packets-dropped
  - vsphere/technology/network/metrics/distributed-switch/packets
knowledge_main: vsphere/object-types/distributed-port-group/distributed-port-group-alerts
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
misconception_type: [threshold-transplanted, unit-and-normalization, average-hides-worst]
status: draft
```
