# Ranking hosts by storage latency over a week

## Prompt
- A weekly report ranks the ESXi hosts of a cluster by storage adapter latency. Each host gets one value per direction (read, write), computed from its 2,016 five-minute samples of the week.
- The team must choose that value: the maximum, the 99th percentile or the 95th percentile.

Which statements are correct?

- A. The weekly maximum is a single sample, so one outlier can put a host at the top of the list.
- B. The 99th percentile leaves out about the 20 highest samples: a host ranks high only when slow again and again.
- C. The maximum is the right ranking value: a host slow even once in the week deserves the first look.
- D. With the 99th percentile in the report, the maximum column can be dropped.
- E. A maximum far above the same host's 99th percentile means about 20 or fewer samples were that high.
- F. A host whose maximum is 40 times its 99th percentile needs a storage case before any other host.
- G. Read and write latency are ranked separately, because a host can be slow on one direction only.
- H. A single value for the whole host can hide one slow adapter or one slow path.
- I. The 95th percentile separates a one-off spike from a recurring problem as well as the 99th does.

## Likely wrong answer
C: rank by the maximum, since it catches everything. Or the reverse: drop the maximum altogether.

## Expected key points
- Answer: A, B, E, G, H.
- A is correct: the maximum is the value of one 5-minute sample; one outlier dominates it.
- B is correct: 1% of 2,016 samples is about 20: the 99th percentile stays low unless more than about 20 samples of the week (about 100 minutes) are high.
- C is wrong: the maximum catches outliers too, so one bad sample ranks a host first; pair it with a percentile.
- D is wrong: worst and percentile are read together: the worst shows the depth, and the gap between the two separates a one-off from a recurring problem.
- E is correct: at most 1% of the 2,016 samples, about 20, lie above the 99th percentile; a maximum far above it is a level that few samples reached, an outlier.
- F is wrong: a maximum 40 times the 99th percentile is the signature of a one-off sample; the hosts with high percentiles come first.
- G is correct: read and write latency are checked separately; write-only latency is common when reads hit cache.
- H is correct: one bad path hides in the host total, so the drill-down goes per adapter and path.
- I is wrong: a problem that fills 1-5% of the samples (about 20 to 100 of the 2,016) leaves the 95th percentile low and the 99th percentile high, so only the 99th tells it from a one-off.

## Notes
- Theory half of the pair with 0081 (practical; design.md, section 3.9). Different numbers from 0081.
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item B7 (origin: synthetic). Counts only after the author's approval.
- Changed in the 2026-11-15 audit: C and D reworded without "because", "every" and "adds nothing" (both still false); I added (95th vs 99th percentile, aggregation, Techniques).

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
misconception: [C, I]
misconception_type: [average-hides-worst]
pair: "0081"
status: draft
```
