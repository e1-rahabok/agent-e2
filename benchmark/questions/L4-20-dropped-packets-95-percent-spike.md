# Packets Dropped at 95% for ten minutes

## Prompt
- In VCF Operations, a reporting VM shows Network Packets Dropped (%) at 95% in two 5-minute samples, 02:10 and 02:15. Every other sample of the week is below 0.1%.
- In those two samples the VM saw about 300 packets in total, delivered and dropped together, against about 400,000 in a normal 5-minute sample. Its throughput is near 0.
- Received Packets Dropped rose in the same samples. Transmitted Packets Dropped stayed at 0.
- Nobody reported an outage, and the 02:00 report job finished on time.

Which statements are correct?

- A. About 95% of the VM's usual traffic, roughly 380,000 packets per sample, was dropped.
- B. It is dropped over dropped plus delivered, so a few drops in a quiet sample read high.
- C. With about 300 packets in the two samples, 95% is fewer than 300 dropped packets.
- D. The formula divides dropped packets by delivered packets alone, so it cannot reach 100%.
- E. Packets Dropped (%) counts transmit drops only, so these receive drops are not part of it.

## Likely wrong answer
A: reading 95% as 95% of the VM's normal traffic lost.

## Expected key points
- Answer: B, C.
- A is wrong: the two samples held about 300 packets in all, not the usual 400,000. The percentage is of the traffic in the sample, not of the usual traffic.
- B: Packets Dropped (%) = dropped / (dropped + delivered) × 100, with dropped = received + transmitted packets dropped. With almost no traffic, a few receive drops dominate the sample.
- C: 95% of about 300 packets is about 285 dropped packets. Read the packet count and the throughput next to the percentage.
- D is wrong: the denominator is dropped plus delivered. Dividing by delivered packets alone could even exceed 100%.
- E is wrong: the formula adds received and transmitted drops; here the receive drops make the whole value.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
- Revised 2026-11-12: this question tests only the formula at low traffic. Transmit drops hidden by TCP are tested in 0074; ranking VMs by the right statistic in 0082.

## Metadata
```yaml
id: "0061"
title: "Packets Dropped at 95% for ten minutes"
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
knowledge_main: vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
answer: [B, C]
misconception: [A]
misconception_type: [unit-and-normalization]
status: draft
```
