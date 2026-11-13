# Port group drops: TCP, UDP and red only

## Prompt
- VCF Operations. The red alert on distributed port groups fires when the share of dropped packets is above 10%, wait cycle 1. There is no orange alert on port groups.
- Two port groups showed 12% dropped packets (transmit side) for two consecutive 5-minute cycles, after a faulty line card on an upstream switch:
  - PG-Files carries SMB file copies over TCP. The VMs and the file servers are 1 ms apart (round-trip time) and one copy normally runs at 2 to 5 Gbit/s per flow.
  - PG-Voice carries RTP voice streams over UDP, with about 200 packets per second per call.
- A colleague proposes two changes: (1) mute the red alert on PG-Files, "because TCP resends every dropped packet, so no data is lost"; (2) add an orange alert at 5% on all port groups "to get an early warning before 10%".
- The network team says the 12% for both groups is an alert it wants on every network object, red only.

Evaluate both proposals. What does 12% loss do to each traffic type, and what should the team do?

## Likely wrong answer
"TCP recovers, so PG-Files is fine and only PG-Voice matters." Or: "An orange alert at 5% is a good early warning." Both miss that TCP throughput collapses at this loss rate even though the data arrives, and that a share-based orange value gave false positives.

## Expected key points
- Do not mute PG-Files. TCP resends, so the data arrives, but the cost is time: each loss halves the congestion window or waits for a retransmission timeout. Throughput per flow falls roughly with 1 / (RTT x square root of the loss rate): at 1 ms RTT and 12% loss, a flow reaches only tens of Mbit/s, against 2 to 5 Gbit/s normally. The file copies stall; users see it as a slow or hanging copy.
- PG-Voice is hit differently: UDP is not resent, so 12% of the packets are lost for good. Voice quality drops (gaps, distortion), and nothing recovers the data.
- Both groups deserve the red alert: the same value has a different effect, and both are above the damage level.
- No orange at 5%: on network objects the set is red only, to avoid alert storms; an orange value gave false positives. A share of dropped packets over a short window is noisy, and early warning belongs in the daily check, not in an alert.
- Next step for the red alert: find the shared fault (the upstream line card). Note that the cause is on the infrastructure side: transmitted drops belong to the network and infrastructure team, as against received drops that can be a Guest OS receive ring.

## Notes
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
answer_type: judged
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
