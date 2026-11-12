# Highest latency below the worst read latency

## Prompt
- [The attached export](0072/esx-14-storage-adapter-latency-1-hour.csv) is the vSphere Client real-time chart of host esx-14, Storage adapter, exported to CSV: read latency and write latency per vmhba, and Highest latency, every 20 seconds for one hour.
- From 09:22 to 09:31, a batch job runs on VMs whose LUNs sit behind vmhba2.
- During the batch, vmhba2 read latency is 14-18 ms, while Highest latency stays below 10 ms.

Which statements are correct?

- A. Highest latency averages read and write per adapter, then takes the worst adapter.
- B. Highest latency is the worst read or write of any adapter, so the export is wrong.
- C. Highest latency counts only the active paths; read latency counts every path.
- D. vmhba2 read latency includes the time IO waits in the Guest OS queues.
- E. The worst adapter latency is the highest read or write latency of any adapter.

## Likely wrong answer
B: assuming Highest latency is the worst read or write latency.

## Expected key points
- Answer: A, E.
- A: in every sample, Highest latency equals the mean of read and write latency of the worse adapter: during the batch about (15 + 0.8) / 2 ≈ 8 ms. So it stays below the read latency of vmhba2.
- E: the useful value is the highest read or write latency among the adapters (here vmhba2 reads, 14-18 ms).
- B is wrong: the export is consistent; the counter is defined differently.
- C is wrong: both are adapter counters over the same IO.
- D is wrong: ESXi does not see the Guest OS queues; adapter latency starts in the host.

## Notes
- Previous id: question-0072 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Revised 2026-11-12 for question set 1.0: the screenshot replaced by a CSV export of the chart; option E added. Counts only after author approval.

## Metadata
```yaml
id: "0072"
title: "Highest latency below the worst read latency"
product: [vsphere]
technology: [storage]
task: read-metric
level: 400
answer_type: deterministic
input: [table]
object: [esxi]
tool: [vcenter]
knowledge:
  - vsphere/technology/storage/metrics/host/adapter-and-path
  - vsphere/architecture/vm-vs-guest-os
knowledge_main: vsphere/technology/storage/metrics/host/adapter-and-path
attachments:
  - 0072/esx-14-storage-adapter-latency-1-hour.csv
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
answer: [A, E]
misconception: [B]
misconception_type: [average-hides-worst]
status: draft
```
