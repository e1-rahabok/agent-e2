# Peak transmitted packet dropped percent

## Prompt
- VCF Operations, one VM. The vCenter adapter collects every 5 minutes and receives 15 real-time samples of 20 seconds each.
- In every 20-second sample the VM transmitted 2,000 packets (30,000 packets in the 5 minutes).
- Transmitted packets dropped: 0 in 14 of the samples, 60 in one sample.
- The VM metric "Network | Peak Transmitted Packet Dropped (%)" for this collection cycle is defined as MAX(net.droppedTx_summation) / AVG(net.packetsTx_summation) x 100, taken over the 15 samples.

Which statements are correct?

- A. The metric shows 0.2% for this cycle: 60 dropped out of 30,000 transmitted.
- B. The metric shows 3% for this cycle.
- C. Over the whole 5 minutes, about 0.2% of the transmitted packets were dropped.
- D. The metric keeps all 15 samples, so it shows when in the cycle the drops happened.
- E. The metric value means that this share of the packets was lost across the whole 5-minute cycle.
- F. The metric compares the worst 20 seconds with an average sample, so it is a peak drop rate, not the loss rate of the cycle.
- G. Peak Transmitted Packet Dropped (%) is a vCenter counter that VCF Operations only displays.
- H. At a low packet rate a few dropped packets make a large percentage, so read the drop count and the packet rate with it.

## Likely wrong answer
- A: "0.2%: 60 dropped out of 30,000 transmitted."
- E: "The peak percentage is the loss rate of the whole 5 minutes."

## Expected key points
- Answer: B, C, F, H.
- A is false: the formula divides the worst sample's drops by the average sample's packets, not the cycle's drops by the cycle's packets.
- B is true: MAX(droppedTx) = 60; AVG(packetsTx) = 2,000 per sample; 60 / 2,000 x 100 = 3%.
- C is true: 60 / 30,000 = 0.2% (also 0.2% if the 60 are added to the denominator). The peak is 15 times the 5-minute share here; both are correct, they answer different questions.
- D is false: the peak metric stores only the highest of the 15 values; it shows no pattern within the 300 seconds.
- E is false: the misconception; the 3% is the drop rate of the worst 20-second period. The 5-minute figure (0.2%) hides that burst.
- F is true: the numerator is the worst 20 seconds and the denominator an average sample: the drop rate of the worst 20-second period.
- G is false: the peak and the 5-minute average are VCF Operations metrics, computed from the 20-second vCenter samples; they are not vSphere counters.
- H is true: a drop ratio over few packets is unstable; read the count and the packet rate with the percentage.

## Notes
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
- Public source: Broadcom KB 444403, "Understanding 'Peak' or 'Worst' Performance Metrics in VMware VCF / Aria Operations" (https://knowledge.broadcom.com/external/article/444403/understanding-peak-or-worst-performance.html), no "Updated On" date shown; applies to VCF Operations 9.x and Aria Operations 8.x. It gives Network | Peak Transmitted Packet Dropped (%) = MAX(net.droppedTx_summation) / AVG(net.packetsTx_summation) x 100, and states that the adapter retrieves 15 raw 20-second samples every 5 minutes.
- Why one answer: the formula is in the prompt; the arithmetic is fixed. The reading (worst 20 seconds, not the 5-minute loss rate) follows from the formula.
- Debatable risk: the formula comes from one KB article with no date, and the prompt supplies it. The exact units of AVG(net.packetsTx_summation) (packets per 20-second sample) are the reading used here; the key accepts the 5-minute figure with or without the dropped packets in the denominator.

## Metadata
```yaml
id: "0313"
title: "Peak transmitted packet dropped percent"
product: [vcf-operations, vsphere]
technology: [network]
task: read-metric
level: 400
answer_type: deterministic
answer: [B, C, F, H]
misconception: [A, E]
input: [text]
object: [vm]
tool: [vcf-operations]
knowledge:
  - vcf-operations/features/peak-20-second-metrics
  - vsphere/object-types/vm/vm-alerts
  - vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
knowledge_main: vcf-operations/features/peak-20-second-metrics
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
misconception_type: [rollup-and-interval]
status: draft
```
