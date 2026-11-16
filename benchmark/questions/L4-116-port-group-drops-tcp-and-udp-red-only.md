# Port group drops: TCP, UDP and red only

## Prompt
- VCF Operations. The red alert on distributed port groups fires when the share of dropped packets is above 10%, wait cycle 1. There is no orange alert on port groups.
- VCF Operations showed 12% dropped packets (transmit side) on two port groups, for two consecutive 5-minute cycles. The cause is still being traced:
  - PG-Files carries SMB file copies over TCP. The VMs and the file servers are 1 ms apart (round-trip time) and one copy normally runs at 2 to 5 Gbit/s per flow.
  - PG-Voice carries RTP voice streams over UDP, with about 200 packets per second per call.
- A colleague proposes two changes: (1) mute the red alert on PG-Files, "because TCP resends every dropped packet, so no data is lost"; (2) add an orange alert at 5% on all port groups "to get an early warning before 10%".
- The network team says the 12% for both groups is an alert it wants on every network object, red only.

Which statements are correct?

- A. TCP resends every dropped segment, so 12% loss on PG-Files costs the file copies no throughput.
- B. Each loss makes TCP shrink its congestion window or wait for a retransmission timeout.
- C. The distributed switch total shows 0.4% dropped in the same cycles, so the 12% on the two port groups is a data error.
- D. At 1 ms round trip and 12% loss, one TCP flow falls from 2 to 5 Gbit/s to tens of Mbit/s or less.
- E. An orange alert at 5% on all port groups gives the team a reliable early warning before 10%.
- F. On PG-Voice, UDP does not resend, so 12% of the voice packets are lost for good.
- G. Muting the red alert on PG-Files is wrong: the data arrives in the end, but the copies stall.
- H. Voice tolerates 12% loss well, because RTP plays on without waiting for retransmissions.
- I. The same 12% hurts both groups, in different ways, so both deserve the red alert.
- J. The 12% is VCF Operations' value for each port group, aggregated over its ports on all hosts; vCenter keeps none.
- K. vCenter keeps drop counters per distributed port, at statistics level 3 and through the API, to find the ports that drop.

## Likely wrong answer
- A: "TCP recovers, so PG-Files is fine and only PG-Voice matters."
- C: "The switch as a whole shows almost no drops, so the port group value is wrong."
- E: "An orange alert at 5% is a good early warning."

## Expected key points
- Answer: B, D, F, G, I, J, K.
- A is false: the misconception; TCP resends, so the data arrives, but the cost is time, and at this loss rate the throughput collapses.
- B is true: each loss halves the congestion window (RFC 5681) or waits for a retransmission timeout.
- C is false: the switch total divides the drops of every port group by all the switch's packets, so two port groups at 12% read as a small share of the whole switch; a low switch total hides a port group and does not make its value an error.
- D is true: TCP throughput per flow falls roughly with 1 / (RTT x square root of the loss rate) (Mathis et al.): with MSS 1460 bytes, RTT 1 ms and p = 0.12, about 41 Mbit/s, against 2 to 5 Gbit/s normally. At this loss timeouts push it lower still.
- E is false: the misconception; on network objects the set is red only, to avoid alert storms, and an orange value gave false positives. Early warning belongs in the daily check.
- F is true: UDP is not resent, so 12% of the packets are lost and nothing recovers them.
- G is true: users see a slow or hanging copy; the red alert stays.
- H is false: voice quality drops at this loss (gaps, distortion); not waiting for a resend does not bring the lost audio back.
- I is true: the same value has a different effect per traffic type, and both are above the damage level.
- J is true: the distributed port group has no vCenter performance counters; VCF Operations aggregates the port group's metrics over the ports on all hosts.
- K is true: vCenter keeps dropped-packet counters on the distributed switch object per DVPort (and per LAG and for the switch), at statistics level 3, readable through the API with no vSphere Client chart; they locate the port that drops.

## Notes
- Review 2026-11-14: the stem no longer blames a faulty line card on an upstream switch. A frame dropped beyond the host is counted only in that switch, not by vSphere (vsphere/technology/network/concepts/packet-drop-accounting), so it could not show as 12% on the port groups. The cause stays open; the TCP and UDP effects and the red-only design do not depend on where the drop happens.
- Public source: TCP behavior under loss is standard transport-layer theory: the steady-state throughput of a TCP flow is proportional to MSS / (RTT x sqrt(p)) (Mathis, Semke, Mahdavi, Ott, "The Macroscopic Behavior of the TCP Congestion Avoidance Algorithm", ACM SIGCOMM Computer Communication Review, 1997; RFC 5681 for the congestion window reaction to loss). With MSS 1460 bytes, RTT 1 ms, p = 0.12 and the constant 1.22, one flow reaches about 41 Mbit/s; at 12% loss timeouts dominate and the model overstates the rate, so D says "tens of Mbit/s or less". UDP has no retransmission (RFC 768). D and H are decided from public TCP and VoIP knowledge; no knowledge file holds the loss-throughput relation or a voice loss tolerance.
- Knowledge file logic: vsphere/object-types/distributed-port-group/distributed-port-group-alerts (red only on network objects, TCP cost is time, orange gave false positives); vsphere/object-types/vm/vm-alerts, "VM dropped packets" (congestion window, retransmit timeout; UDP is not resent); vsphere/technology/network/metrics/distributed-switch/packets-dropped (switch, DVPort and LAG counters at level 3; the switch total hides one port; no vCenter port group counter).
- Audit 2026-11-15: C (RTP retransmission, a throwaway beside F) replaced with the switch-total dilution misconception; J (unstable ratio over few packets) and K (receive drops to the Guest OS owner) replaced with the port group aggregate and the DVPort counters, as both facts were over the two-question cap (0061/0082 and 0345/0060 keep them). Stem: the 12% is shown by VCF Operations, as vCenter keeps no port group counter.

## Metadata
```yaml
id: "0346"
title: "Port group drops: TCP, UDP and red only"
product: [vcf-operations, vsphere]
technology: [network]
task: judge-setting
level: 400
answer_type: deterministic
answer: [B, D, F, G, I, J, K]
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
