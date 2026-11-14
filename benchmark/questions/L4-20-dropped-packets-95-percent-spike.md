# Packets Dropped near 90% for ten minutes

## Prompt
- In VCF Operations, a reporting VM shows Network Packets Dropped (%) at 88% at 03:20 and 90% at 03:25. Every other 5-minute sample of the week is below 0.1%.
- The same VM, same two samples:
  - Packets Received: 12 and 15;
  - Packets Transmitted: 3 and 4;
  - Received Packets Dropped: 110 and 171;
  - Transmitted Packets Dropped: 0 and 0;
  - Network Usage Rate: below 1 KBps.
- In a normal 5-minute sample the VM receives about 250,000 and transmits about 150,000 packets.
- Nobody reported an outage, and the 03:00 report job finished on time.

Which statements are correct?

- A. About nine tenths of the VM's usual traffic, some 355,000 packets per sample, was lost in those ten minutes.
- B. Packets Dropped (%) divides the dropped packets by the dropped plus the delivered packets of the same sample.
- C. Fewer than 300 packets were dropped in the two samples together.
- D. Packets Dropped (%) counts transmitted drops only, so these received drops are not part of it.
- E. Packets Dropped (%) has no use for any VM: only the dropped packet count matters.
- F. Open an outage ticket for the VM's network for 03:20 to 03:30.

## Likely wrong answer
A: reading 88-90% as that share of the VM's normal traffic lost.

## Expected key points
- Answer: B, C.
- A is false: the two samples held about 315 packets in all, not the usual 400,000. The percentage is of the traffic in the sample, not of the usual traffic.
- B is true: Packets Dropped (%) = dropped / (dropped + delivered) × 100, with dropped = received + transmitted packets dropped and delivered = packets received + packets transmitted: 110 / 125 = 88% and 171 / 190 = 90%.
- C is true: 110 + 171 = 281 dropped packets. Read the packet count and the throughput next to the percentage.
- D is false: the formula adds received and transmitted drops; here the received drops make the whole value.
- E is false: the percentage is read with the packet count, not dropped: a drop profile uses the 99th percentile of the drop percentage next to the sum of dropped packets.
- F is false: a short spike near 90% at near-zero throughput, driven by received drops, is not an outage; no user saw one and the job finished on time.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): the stem gives the counters instead of the formula's terms ("delivered and dropped together") and no longer mirrors the knowledge file's example; the negation pair B/D resolved (old D dropped); over-correction E and wrong action F added. Key unchanged: B, C.
- Revised 2026-11-12: this question tests only the formula at low traffic. Transmit drops hidden by TCP are tested in 0074; ranking VMs by the right statistic in 0082.

## Metadata
```yaml
id: "0061"
title: "Packets Dropped near 90% for ten minutes"
product: [vsphere, vcf-operations]
technology: [network]
object: [vm]
tool: [vcf-operations]
task: read-metric
level: 400
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
  - vsphere/technology/network/metrics/virtual-motherboard/packets
knowledge_main: vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
answer: [B, C]
misconception: [A]
misconception_type: [unit-and-normalization]
pair: "0082"
status: draft
```
