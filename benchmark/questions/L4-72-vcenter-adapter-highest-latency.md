# Highest latency below the worst read latency

## Prompt
The attached screenshot is the vSphere Client performance chart of one ESXi host, Storage adapter: Read latency, Write latency and Highest latency, per vmhba.

- Highest latency stays below the read latency of the busiest adapter for most of the hour.

Why?

- A. Highest latency averages read and write per adapter first, then takes the worst adapter. A read-heavy spike is diluted by low write latency.
- B. Highest latency takes the worst read or write of any adapter, so the chart is wrong.
- C. Highest latency covers only the active paths, read latency covers all paths.
- D. The read latency includes the Guest OS queue.

## Input to supply
- Tool: vSphere Client 9.1, host > Monitor > Performance > Advanced > Storage adapter, real-time, one hour.
- Counters: Read latency, Write latency, Highest latency, for every vmhba.
- Condition for the key: on the busiest adapter, read latency is clearly above write latency, and Highest latency is below that read latency for most points.
- Mask WWNs and IQNs.
- Save as `benchmark/questions/72/vcenter-host-storage-adapter-latency.png`.

## Likely wrong answer
B: assuming Highest latency is the worst read or write.

## Expected key points
- Answer: A.
- Highest latency averages read and write per adapter first, then takes the worst adapter. So it can be lower than the worst read latency.
- The useful value is the highest read or write latency among all adapters or paths.
- D is wrong: ESXi does not see the Guest OS queue.

## Notes
- Previous id: question-0072 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "72"
title: "Highest latency below the worst read latency"
product: [vsphere]
technology: [storage]
task: read-metric
level: 400
answer_type: deterministic
input: [screenshot]
knowledge:
  - vsphere/technology/storage/metrics/host/adapter-and-path
attachments:
  - 72/vcenter-host-storage-adapter-latency.png
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
answer: [A]
trap: [B]
status: awaiting-input
```
