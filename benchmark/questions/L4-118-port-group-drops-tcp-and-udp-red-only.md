# Port group drops: TCP, UDP and red only

## Prompt
- VCF Operations. The red alert on distributed port groups fires when the share of dropped packets is above 10%, wait cycle 1. There is no orange alert on port groups.
- Two port groups showed 12% dropped packets (transmit side) for two consecutive 5-minute cycles, after a faulty line card on an upstream switch:
  - PG-Files carries SMB file copies over TCP. The VMs and the file servers are 1 ms apart (round-trip time) and one copy normally runs at 2 to 5 Gbit/s per flow.
  - PG-Voice carries RTP voice streams over UDP, with about 200 packets per second per call.
- A colleague proposes two changes: (1) mute the red alert on PG-Files, "because TCP resends every dropped packet, so no data is lost"; (2) add an orange alert at 5% on all port groups "to get an early warning before 10%".
- The network team says the 12% for both groups is an alert it wants on every network object, red only.

Which statements are correct?

- A. TCP resends every dropped segment, so 12% loss on PG-Files costs the file copies no throughput.
- B. Each loss makes TCP shrink its congestion window or wait for a retransmission timeout.
- C. RTP voice recovers its lost packets through retransmission, the same way the SMB file copy does.
- D. At 1 ms round trip and 12% loss, one TCP flow falls from 2 to 5 Gbit/s to tens of Mbit/s or less.
- E. An orange alert at 5% on all port groups gives the team a reliable early warning before 10%.
- F. On PG-Voice, UDP does not resend, so 12% of the voice packets are lost for good.
- G. Muting the red alert on PG-Files is wrong: the data arrives in the end, but the copies stall.
- H. Voice tolerates 12% loss well, because RTP plays on without waiting for retransmissions.
- I. The same 12% hurts both groups, in different ways, so both deserve the red alert.
- J. A share of dropped packets over a short window jumps when few packets flow, so a low orange fires on noise.
- K. Transmit drops stay with the infrastructure team; receive drops can come from a full guest receive ring.

## Likely wrong answer
- A: "TCP recovers, so PG-Files is fine and only PG-Voice matters."
- E: "An orange alert at 5% is a good early warning."

## Expected key points
- Answer: B, D, F, G, I, J, K.
- A is false: the misconception; TCP resends, so the data arrives, but the cost is time, and at this loss rate the throughput collapses.
- B is true: each loss halves the congestion window (RFC 5681) or waits for a retransmission timeout.
- C is false: RTP runs over UDP, which has no retransmission (RFC 768); a lost voice packet is gone.
- D is true: TCP throughput per flow falls roughly with 1 / (RTT x square root of the loss rate) (Mathis et al.): with MSS 1460 bytes, RTT 1 ms and p = 0.12, about 41 Mbit/s, against 2 to 5 Gbit/s normally. At this loss timeouts push it lower still.
- E is false: the misconception; on network objects the set is red only, to avoid alert storms, and an orange value gave false positives. Early warning belongs in the daily check.
- F is true: UDP is not resent, so 12% of the packets are lost and nothing recovers them.
- G is true: users see a slow or hanging copy; the red alert stays.
- H is false: voice quality drops at this loss (gaps, distortion); not waiting for a resend does not bring the lost audio back.
- I is true: the same value has a different effect per traffic type, and both are above the damage level.
- J is true: a drop ratio over few packets is unstable: a handful of drops at low throughput gives a large share, so a low threshold on a short window is noisy.
- K is true: received drops include packets not destined for the VM and drops in a full receive ring, whose cause and fix are in the Guest OS; transmit drops stay with the network and infrastructure team, here the shared fault upstream.

## Notes
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
- Public source: TCP behavior under loss is standard transport-layer theory: the steady-state throughput of a TCP flow is proportional to MSS / (RTT x sqrt(p)) (Mathis, Semke, Mahdavi, Ott, "The Macroscopic Behavior of the TCP Congestion Avoidance Algorithm", ACM SIGCOMM Computer Communication Review, 1997; RFC 5681 for the congestion window reaction to loss). With MSS 1460 bytes, RTT 1 ms, p = 0.12 and the constant 1.22, one flow reaches about 41 Mbit/s. The key says "tens of Mbit/s" to stay within the model's accuracy. UDP has no retransmission (RFC 768).
- Knowledge file logic: vsphere/object-types/distributed-port-group/distributed-port-group-alerts, section "Distributed port group dropped packets": red only, as on every network object, to avoid alert storms; TCP resends a dropped segment, so the data arrives in the end and the cost is time; orange is not set because it gave false positives; and vsphere/object-types/vm/vm-alerts, "VM dropped packets" (each loss shrinks the congestion window or waits for a retransmit timeout; UDP is not resent).
- Why one answer: the TCP and UDP behavior is protocol standard; the numbers (1 ms, 12%, 2 to 5 Gbit/s) show the effect, so muting is wrong. The red-only rule is the author's design and is supported by the instability of a share over a short window.
- Debatable risk: the orange alert is a design choice. The key accepts any answer that keeps red only and moves early warning to a daily check; it does not require the exact words "false positives". The throughput figure is a model estimate (Mathis), not a vendor number.

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
misconception: [A, E]
input: [text]
object: [network]
tool: [vcf-operations]
knowledge:
  - vsphere/object-types/distributed-port-group/distributed-port-group-alerts
  - vsphere/object-types/vm/vm-alerts
  - vsphere/technology/network/concepts/packet-drop-accounting
knowledge_main: vsphere/object-types/distributed-port-group/distributed-port-group-alerts
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
misconception_type: [threshold-transplanted, unit-and-normalization]
status: draft
```
