# Which hosts have real storage latency problems

## Prompt
- [The attached export](0081/host-adapter-latency-40-hosts-1-week.csv) is a VCF Operations report of the 40 ESXi hosts of cluster PROD-A over one week, in 5-minute samples: for the worst storage adapter of each host, the maximum, the 99th percentile and the 95th percentile of read and write latency.
- The storage team will look at one or two hosts this week.

Which statements are correct?

- A. esx-017 had a rare spike: its 250 ms maximum sits on a 95th percentile write latency of 0.33 ms.
- B. esx-017 is the host to fix first, because it has the highest maximum latency of all 40 hosts.
- C. esx-024 and esx-031 have real write latency problems: drill down per adapter and per path.
- D. Ranking the hosts by their mean write latency over the week would put esx-017 in first place.
- E. esx-031's problem is less frequent than esx-024's: its 95th percentile write latency is much lower.

## Likely wrong answer
B: ranking hosts by the maximum.

## Expected key points
- Answer: A, C, E.
- A: one outlier dominates the maximum. With a 95th percentile of 0.33 ms, esx-017 was slow in a handful of samples at most.
- C: esx-024 and esx-031 have a 99th percentile write latency above 20 ms, against 5 ms or less on the other hosts: a recurring problem. Drill down per adapter and path, read and write separately.
- E: esx-024 has 14.2 ms at the 95th percentile, so it is slow often; esx-031 has 2.9 ms at the 95th and 22.4 ms at the 99th, so it is slow less often.
- B is wrong: the maximum ranks one sample, not a host problem.
- D is wrong: one 250 ms sample among about 2,000 adds about 0.1 ms to esx-017's mean, which stays below 1 ms; esx-024 is far higher.

## Notes
- Previous id: question-0081 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Revised 2026-11-12 for question set 1.0: 192 hosts reduced to 40; esx-024 and esx-031 replace esx-044 and esx-101; options D and E new. Counts only after author approval.

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
knowledge_main: vsphere/technology/storage/metrics/host/adapter-and-path
attachments:
  - 0081/host-adapter-latency-40-hosts-1-week.csv
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
answer: [A, C, E]
misconception: [B]
misconception_type: [average-hides-worst, rollup-and-interval]
status: draft
```
