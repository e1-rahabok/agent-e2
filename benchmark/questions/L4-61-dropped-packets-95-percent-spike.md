# Packets Dropped at 95% for ten minutes

## Prompt
- In VCF Operations, a VM shows Network Packets Dropped (%) at 95% for about 10 minutes, then back near 0.
- Throughput in those 10 minutes is very low.
- Nobody reported an outage.

Which statements are correct? Choose all that apply.

- A. The VM had a network outage for 10 minutes.
- B. A short spike at low throughput, driven by receive drops, can push the percentage above 95%.
- C. Transmit drops can be large without complaints, because TCP retransmits them; the application only sees higher latency.
- D. The percentage is dropped divided by delivered only, so it cannot exceed 50%.

## Likely wrong answer
A: reading 95% dropped as an outage.

## Expected key points
- Answer: B, C.
- Packets Dropped (%) = dropped / (dropped + delivered). At low throughput a few receive drops give a high percentage for a short time.
- Receive drops are far more common than transmit drops; the 99th percentile was 35x smaller than the maximum.
- TCP retransmits hide transmit drops: millions a month can pass without complaints, so profile them with the network team.
- D is wrong: the formula divides by dropped plus delivered, so it can approach 100%.

## Notes
- Previous id: question-0061 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "61"
title: "Packets Dropped at 95% for ten minutes"
product: [vsphere, vcf-operations]
technology: [network]
task: read-metric
level: 400
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
answer: [B, C]
trap: [A]
status: draft
```
