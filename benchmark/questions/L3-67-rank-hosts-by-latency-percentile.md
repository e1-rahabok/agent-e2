# Ranking hosts by storage latency over a week

## Prompt
- A weekly report ranks the ESXi hosts of a cluster by storage adapter latency. Each host gets one value per direction (read, write), computed from its 2,016 five-minute samples of the week.
- The team must choose that value: the maximum, the 99th percentile or the 95th percentile.

Which statements are correct?

- A. The weekly maximum is a single sample, so one outlier can put a host at the top of the list.
- B. The 99th percentile leaves out about the 20 highest samples, so a host ranks high only when it is slow again and again.
- C. The maximum is the safest ranking value, because it catches every problem.
- D. Once percentiles are in the report, the maximum adds nothing.
- E. A maximum far above the same host's 95th percentile points to a one-off event.
- F. A host whose maximum is 40 times its 99th percentile needs a storage case before any other host.
- G. Read and write latency are ranked separately, because a host can be slow on one direction only.
- H. A value for the whole host can hide one slow adapter or path.

## Likely wrong answer
C: rank by the maximum, since it catches everything. Or the reverse: drop the maximum altogether.

## Expected key points
- Answer: A, B, E, G, H.
- A true: the maximum is the value of one 5-minute sample; one outlier dominates it.
- B true: 1% of 2,016 samples is about 20: the 99th percentile stays low unless more than about 20 samples of the week (about 100 minutes) are high.
- C false: the maximum catches outliers too; pair it with a percentile.
- D false: worst and percentile are read together: the worst shows the depth, and the gap between the two separates a one-off from a recurring problem.
- E true: worst far above the 95th percentile marks an outlier; close together marks a real problem.
- F false: a maximum 40 times the 99th percentile is the signature of a one-off sample; the hosts with high percentiles come first.
- G true: read and write latency are checked separately; write-only latency is common when reads hit cache.
- H true: one bad path hides in the host total, so the drill-down goes per adapter and path.

## Notes
- Theory half of the pair with 0081 (practical; design.md, section 3.9). Different numbers from 0081.
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item B7 (origin: synthetic). Counts only after author approval.

## Metadata
```yaml
id: "0405"
title: "Ranking hosts by storage latency over a week"
product: [vsphere, vcf-operations]
technology: [storage]
task: read-metric
level: 300
answer_type: deterministic
input: [text]
object: [esxi]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/storage/metrics/host/adapter-and-path
  - sp5-framework/observability/aggregation
  - vsphere/technology/storage/troubleshooting/host-storage-latency
knowledge_main: sp5-framework/observability/aggregation
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item B7"
answer: [A, B, E, G, H]
misconception: [C]
misconception_type: [average-hides-worst]
pair: "0081"
status: draft
```
