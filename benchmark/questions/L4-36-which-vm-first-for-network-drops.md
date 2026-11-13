# Which VM to investigate first for network drops

## Prompt
- [The attached export](0082/vm-network-drops-one-week.csv) is a VCF Operations view of 40 VMs over one week, built from 5-minute samples: the maximum and the 99th percentile of Packets Dropped (%), the week's sum of received and transmitted packets dropped, and the average usage rate.
- The team sorted the view by the maximum of Packets Dropped (%) and plans to open network tickets for the top five VMs.
- You can open one ticket today.

Which VM should be investigated first?

- A. batch-03: it has the highest maximum of the week, 98.7%, so it is the worst VM.
- B. db-07: the highest 99th percentile, and over 4 million transmit drops in the week.
- C. web-04: it has the highest maximum of the VMs that carry real traffic, 31.4%.
- D. rpt-11: its receive drops are the highest of the five VMs at the top of the list.
- E. None: every 99th percentile is below 2%, so no VM loses enough packets to matter.

## Likely wrong answer
A: ranking VMs by the maximum percentage, which short spikes on near-idle VMs dominate.

## Expected key points
- Answer: B.
- The top five by maximum are near-idle job VMs: their 99th percentile is 0 and they dropped a few hundred to about 1,300 packets in the week. A high percentage in a sample with almost no traffic is a few packets.
- db-07: 1% of the week's samples (about 100 minutes) are at 1.9% or more, and it dropped about 4.18 million transmitted packets while carrying real traffic. At about 1.5 KB per packet that is about 6 GB resent.
- Rank drops by a percentile and by the packet count, not by the maximum percentage. The maximum of a short, spiky metric says little.
- C is wrong: web-04's 99th percentile is 0.02% and its totals are small; its maximum is one spike.
- E is wrong: on a busy database, about 100 minutes a week at 1.9% or more and millions of dropped packets are real loss that TCP hides by resending. Raise it with the network team.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
- Revised 2026-11-12 (question set 1.0): the 400-VM workbook became a 40-VM CSV; the management pack score removed (fairness). The question now tests which statistic ranks VMs for drops; the spike formula is in 0061, transmit drops hidden by TCP in 0074. The CSV is synthetic, generated with a fixed seed.

## Metadata
```yaml
id: "0082"
title: "Which VM to investigate first for network drops"
product: [vsphere, vcf-operations]
technology: [network]
object: [vm]
tool: [vcf-operations]
task: troubleshoot
level: 400
answer_type: deterministic
input: [table]
knowledge:
  - vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
knowledge_main: vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
attachments:
  - 0082/vm-network-drops-one-week.csv
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
answer: [B]
misconception: [A]
misconception_type: [rollup-and-interval]
status: draft
```
