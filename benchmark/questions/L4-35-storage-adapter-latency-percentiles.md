# Which hosts have real storage latency problems

## Prompt
- [The attached export](0081/host-adapter-latency-36-hosts-1-week.csv) is a VCF Operations report of the 36 ESXi hosts of cluster PROD-K over one week, in 5-minute samples: for the worst storage adapter of each host, the maximum, the 99th percentile and the 95th percentile of read and write latency.
- The storage team will look at one or two hosts this week.

Which statements are correct?

- A. esxi-k2-09 had a rare spike: its 184 ms maximum read latency sits on a 95th percentile read latency of 0.41 ms.
- B. esxi-k2-09 is the host to fix first, because it has the highest maximum latency of all 36 hosts.
- C. esxi-k2-22 and esxi-k2-30 have recurring latency problems: drill down per adapter and per path.
- D. Ranked by 99th percentile latency, esxi-k2-09 would be among the three worst hosts of the cluster.
- E. esxi-k2-30's problem is less frequent than esxi-k2-22's: its 95th percentile latency is much lower.
- F. esxi-k2-22 is slow on writes and esxi-k2-30 on reads, so each is followed up on its own direction.
- G. The maximum column can be dropped from such reports, since it says nothing useful about a host.

## Likely wrong answer
B: ranking hosts by the maximum.

## Expected key points
- Answer: A, C, E, F.
- A true: one outlier dominates the maximum. With a 95th percentile of 0.41 ms and a 99th of 0.72 ms, esxi-k2-09 was slow in at most about 20 of its 2,016 samples, most likely one.
- B false: the maximum ranks one sample, not a host problem.
- C true: esxi-k2-22 (write, 99th percentile 31.6 ms) and esxi-k2-30 (read, 99th percentile 26.7 ms) are far above the other hosts, whose 99th percentiles stay near or below 2 ms: a recurring problem. Drill down per adapter and path.
- D false: esxi-k2-09's 99th percentiles are 0.72 ms (read) and 0.9 ms (write), in the lower half of the cluster; the percentile ranks it as a healthy host.
- E true: esxi-k2-22 has 17.9 ms at the 95th percentile, so it is slow often; esxi-k2-30 has 3.4 ms at the 95th and 26.7 ms at the 99th, so it is slow less often.
- F true: read and write latency are checked separately; esxi-k2-22's reads and esxi-k2-30's writes are as low as on the other hosts.
- G false: worst and percentile are read together: the worst gives the depth, and a maximum far above the 95th percentile is what marks a one-off.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Revised 2026-11-12 for question set 1.0: 192 hosts reduced to 40; esx-024 and esx-031 replace esx-044 and esx-101; options D and E new. Counts only after author approval.
- CSV regenerated 2026-11-14 with a seeded script: new scenario (36 hosts, a one-off on reads, one frequent write problem, one less frequent read problem), new names and numbers, because adapter-and-path states the old values (project/question-pairing-2026-11-14.md, item B7). Options and key points updated; D (the mean) replaced by a percentile ranking, F and G new. Key changed from A, C, E to A, C, E, F.
- Paired with 0405 (theory; design.md, section 3.9).

## Metadata
```yaml
id: "0081"
title: "Which hosts have real storage latency problems"
product: [vsphere, vcf-operations]
technology: [storage]
task: troubleshoot
level: 400
answer_type: deterministic
input: [table]
object: [esxi]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/storage/metrics/host/adapter-and-path
  - vsphere/technology/storage/troubleshooting/host-storage-latency
  - sp5-framework/observability/aggregation
knowledge_main: vsphere/technology/storage/metrics/host/adapter-and-path
attachments:
  - 0081/host-adapter-latency-36-hosts-1-week.csv
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
answer: [A, C, E, F]
misconception: [B]
misconception_type: [average-hides-worst, rollup-and-interval]
pair: "0405"
status: draft
```
