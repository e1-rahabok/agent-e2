# Peak transmitted packet dropped percent

## Prompt
- One VM, one 5-minute window. The vSphere Client Real-time chart shows the VM's 15 samples of 20 seconds:
  - Packets transmitted: 5,000 in every sample (75,000 in the 5 minutes).
  - Transmitted packets dropped: 0 in 14 of the samples, 300 in one sample.
- In VCF Operations, the same VM shows the metric Network | Peak Transmitted Packet Dropped (%) for the collection cycle that covers this window.

Which statements are correct?

- A. The metric shows about 0.4% for this cycle: 300 dropped out of 75,000 transmitted.
- B. The metric shows about 6% for this cycle.
- C. Over the whole 5 minutes, about 0.4% of the transmitted packets were dropped.
- D. The metric keeps all 15 samples, so it shows when in the cycle the drops happened.
- E. The metric gives the drop rate of the worst 20-second sample of the cycle.
- F. Peak Transmitted Packet Dropped (%) is a vCenter counter that VCF Operations only displays.
- G. At a low packet rate a few dropped packets make a large percentage, so read the drop count and the packet rate with it.
- H. Report the 0.4% and set the peak aside: it overstates what the VM lost.

## Likely wrong answer
- A: "0.4%: 300 dropped out of 75,000 transmitted."
- H: "The 5-minute share is the real loss; the peak only exaggerates it."

## Expected key points
- Answer: B, C, E, G.
- A is false: a Peak ... within collection cycle metric takes the highest of the 15 twenty-second values, not the cycle's drops over the cycle's packets.
- B is true: the worst sample dropped 300 of about 5,000 packets: 300 / 5,000 = 6% (5.7% if the dropped packets are added to the denominator).
- C is true: 300 / 75,000 = 0.4% (also 0.4% with the 300 in the denominator). The peak is 15 times the 5-minute share here; both are correct, they answer different questions.
- D is false: the peak metric stores only the highest of the 15 values; it shows no pattern within the 300 seconds.
- E is true: the peak is the drop rate of the worst 20-second period; the 5-minute figure (0.4%) hides that burst.
- F is false: the peak and the 5-minute average are VCF Operations metrics, computed from the 20-second vCenter samples; they are not vSphere counters.
- G is true: a drop ratio over few packets is unstable; read the count and the packet rate with the percentage.
- H is false: the peak shows the burst that the 5-minute average hides, which is why the VM drop alert reads it within a 20-second period; both values are correct.

## Notes
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): the two stem lines that explained the mechanism (the adapter's collection and the metric formula) removed; new numbers (different from the practical half); the negation pair E/F resolved (old E dropped, F stated positively as E); over-correction and wrong action H added. Key changed from B, C, F, H to B, C, E, G.
- Public source: Broadcom KB 444403, "Understanding 'Peak' or 'Worst' Performance Metrics in VMware VCF / Aria Operations" (https://knowledge.broadcom.com/external/article/444403/understanding-peak-or-worst-performance.html), no "Updated On" date shown; applies to VCF Operations 9.x and Aria Operations 8.x. It gives Network | Peak Transmitted Packet Dropped (%) = MAX(net.droppedTx_summation) / AVG(net.packetsTx_summation) x 100, and states that the adapter retrieves 15 raw 20-second samples every 5 minutes.
- Why this key: the knowledge base defines a Peak ... within collection cycle metric as the highest of the 15 twenty-second values; with 5,000 packets in every sample, the Broadcom KB 444403 formula MAX(droppedTx) / AVG(packetsTx) and the highest per-sample drop rate give the same 6%.
- Debatable risk: the formula comes from one KB article with no date, and the knowledge base does not state it; the constant packet count makes the key hold under either reading. The key accepts both figures with or without the dropped packets in the denominator ("about").

## Metadata
```yaml
id: "0313"
title: "Peak transmitted packet dropped percent"
product: [vcf-operations, vsphere]
technology: [network]
task: read-metric
level: 400
answer_type: deterministic
answer: [B, C, E, G]
misconception: [A, H]
input: [text]
object: [vm]
tool: [vcf-operations]
knowledge:
  - vcf-operations/features/peak-20-second-metrics
  - vsphere/object-types/vm/vm-alerts
  - vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
  - vsphere/technology/network/metrics/virtual-motherboard/packets
knowledge_main: vcf-operations/features/peak-20-second-metrics
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
misconception_type: [rollup-and-interval]
pair: "0421"
status: draft
```
