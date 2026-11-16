# Small packets at low bandwidth

## Prompt
- dns-02 is an internal DNS resolver VM. Since a new application went live, it answers twice as many queries, and some clients see resolution time-outs at peak.
- The host uplinks are 25 GbE. The network team says the uplink carrying dns-02 is at 1.2%.
- vCenter real-time chart of dns-02, one 20-second sample at peak:
  - Packets received: 5,400,000
  - Data receive rate: 26,400 KBps

Which statements are correct?

- A. dns-02 receives about 270,000 packets per second in this peak sample.
- B. dns-02's packets carry about 100 bytes each on average.
- C. Since the uplink is 1.2% busy, the network side of dns-02 has headroom to spare.
- D. Packets received leaves out broadcast and multicast, so part of the traffic is missing.
- E. Packets that ESXi drops for dns-02 are left out of its Packets received.
- F. Bandwidth is never what limits a VM's network; only the packet rate is.
- G. Move dns-02 to a port group on a less busy uplink.

## Answers
A, B, E

## Explanation
- A is true: in the real-time chart, Packets received is a count per 20-second sample: 5,400,000 ÷ 20 = 270,000 packets per second.
- B is true: 26,400 KBps is kilobytes per second; 26,400 × 1,024 bytes ÷ 270,000 ≈ 100 bytes per packet, against about 1,500 bytes for full frames.
- C is false: with small packets the load is the packet rate, not the bandwidth. Each packet costs CPU in the host and in the guest to receive, whatever its size.
- D is false: the packet count includes broadcast and multicast.
- E is true: the packet counts exclude dropped packets; drops have their own counters.
- F is false: the uplink is shared and often oversubscribed, so bandwidth can limit a VM too; throughput and packets per second are both consumption to read.
- G is false: the uplink is at 1.2%; the limit is the per-packet work at 270,000 packets per second, which a quieter uplink does not change. The next check is dns-02's receive drops and the CPU of the vCPU that drains its receive ring.
- Misconception: C: reading bandwidth utilization as network load. A low share of the link says nothing about a high packet rate.

## Notes
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): over-correction F and wrong action G added. Key unchanged: A, B.
- Review 2026-11-15: new scenario (a DNS resolver, 270,000 packets per second of about 100 bytes) so it shares no situation or wording with its practical half 0415; C, E, F and G reworded (E now states the dropped-packet rule as true). Key changed from A, B to A, B, E.

## Metadata
```yaml
id: "0211"
title: "Small packets at low bandwidth"
product: [vsphere]
technology: [network]
object: [vm]
tool: [vcenter]
task: read-metric
level: 300
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/technology/network/metrics/virtual-motherboard/packets
  - vsphere/technology/network/metrics/virtual-motherboard/throughput
  - vsphere/technology/network/metrics/vm-network-metrics
  - vsphere/tools/esxtop/network
  - vsphere/technology/network/concepts/network-characteristics
knowledge_main: vsphere/technology/network/metrics/virtual-motherboard/packets
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-12"
misconception: [C, G]
misconception_type: [unit-and-normalization]
pair: "0415"
status: draft
```
