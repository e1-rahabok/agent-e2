# Highest latency below the worst read latency

## Prompt
- [The attached export](0072/esx-14-storage-adapter-latency-1-hour.csv) is the vSphere Client real-time chart of host esx-14, Storage adapter, exported to CSV: read latency and write latency per vmhba, and Highest latency, every 20 seconds for one hour.
- From 09:22 to 09:31, a batch job runs on VMs whose LUNs sit behind vmhba2. Its users say it ran slowly.
- The team's storage alert watches Highest latency, with a threshold of 10 ms.

Which statements are correct?

- A. In every sample of the batch, Highest latency is about the mean of vmhba2's read and write latency.
- B. Highest latency follows vmhba2's read latency sample by sample during the batch.
- C. During the batch, Highest latency stays at about 7-10 ms while vmhba2 reads run at about 14-18 ms.
- D. vmhba2 read latency includes the time IO waits in the Guest OS queues.
- E. The 10 ms alert on Highest latency stays silent through the batch.
- F. Open a case: the export is corrupt, since Highest latency sits below vmhba2's read latency.
- G. Highest latency is of no use here: it does not move with the worst adapter at all.
- H. The batch's read latency is on vmhba2's Read latency line, not on Highest latency.

## Likely wrong answer
B: reading Highest latency as the worst read or write latency of any adapter. Or F: the export must be wrong.

## Expected key points
- Answer: A, C, E, H.
- A true: Highest latency averages read and write per adapter, then takes the worst adapter; in every sample of the export it equals the mean of the worse adapter, during the batch about (15 + 0.8) / 2 = 8 ms.
- B false: the misconception. Highest latency runs at about half of vmhba2's read latency, because vmhba2's fast writes are averaged in.
- C true: the export shows Highest latency at 7.4-9.7 ms and vmhba2 read latency at 14.0-18.5 ms during the batch.
- D false: ESXi does not see the Guest OS queues; adapter latency starts in the host.
- E true: Highest latency never reaches 10 ms (9.7 ms at most), so an alert on it stays silent while the reads run at 14-18 ms.
- F false: the wrong action. The export is consistent; the counter is defined differently.
- G false: the over-correction. Highest latency rises from about 1 ms to 7-10 ms with vmhba2 during the batch; it follows the worst adapter, after averaging read and write.
- H true: the useful value is the highest read or write latency among the adapters, here vmhba2 reads.

## Notes
- Drafted 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Revised 2026-11-12 for question set 1.0: the screenshot replaced by a CSV export of the chart; option E added. Counts only after author approval.
- Stem bullet that read the batch values out of the CSV for the candidate removed 2026-11-14 (design.md 6.2; project/question-pairing-2026-11-14.md, item B8). Key unchanged: A, E.
- Paired with 0406 (theory; design.md, section 3.9).
- Review 2026-11-15: options rewritten to read the CSV (the old A and E were general facts that 0406 tests; C, active paths, is not settled by the knowledge base and is removed); the alert threshold added as a case fact; over-correction G and wrong action F added. Key changed from A, E to A, C, E, H.

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
source_path: "Drafted 2026-11-05"
answer: [A, C, E, H]
misconception: [B, F]
misconception_type: [average-hides-worst]
pair: "0406"
status: draft
```
