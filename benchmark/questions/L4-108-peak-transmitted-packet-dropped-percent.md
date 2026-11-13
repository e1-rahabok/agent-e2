# Peak transmitted packet dropped percent

## Prompt
- VCF Operations, one VM. The vCenter adapter collects every 5 minutes and receives 15 real-time samples of 20 seconds each.
- In every 20-second sample the VM transmitted 2,000 packets (30,000 packets in the 5 minutes).
- Transmitted packets dropped: 0 in 14 of the samples, 60 in one sample.
- The VM metric "Network | Peak Transmitted Packet Dropped (%)" for this collection cycle is defined as MAX(net.droppedTx_summation) / AVG(net.packetsTx_summation) x 100, taken over the 15 samples.

What value does the metric show? How does it compare with the percentage of transmitted packets dropped over the whole 5 minutes, and what does the difference tell you?

## Likely wrong answer
"0.2%: 60 dropped out of 30,000 transmitted." Or reading the peak as the loss rate of the whole 5 minutes.

## Expected key points
- Peak value: MAX(droppedTx) = 60; AVG(packetsTx) = 2,000 per sample; 60 / 2,000 x 100 = 3%.
- Over the whole 5 minutes: 60 / 30,000 = 0.2% (0.2% also if 60 is added to the denominator).
- The peak is 15 times the 5-minute share here. The numerator is the worst 20 seconds, the denominator is an average sample; it is the drop rate of the worst 20-second period, not a loss rate of the cycle.
- The 5-minute figure hides a short burst; the peak shows that one 20-second period lost 3% of its packets. Both are correct, they answer different questions.
- A low packet rate makes a small drop count a large percentage; read the drop count and the packet rate with the percentage.

## Notes
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
answer_type: judged
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
