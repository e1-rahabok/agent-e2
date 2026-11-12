# Disk latency peak 40 times the average

## Prompt
The screenshot is the VCF Operations chart of one VM over one day: the 20-second peak disk latency and the 5-minute average read and write latency. The attached table is a one-day export, in 5-minute samples, of the read and write latency of each of its 20 virtual disks.

- At 02:15, the peak is about 10,000 ms; the highest 5-minute average of the VM is about 250 ms.
- The application owner asks whether the peak is real, and how it affects the VM KPI.

Is the peak real? What does it measure, where did it come from, and which reading does the VM KPI use?

## Input to supply
- Screenshot: VCF Operations 9.1, VM > Metrics, the 20-second peak disk latency (Peak Latency within collection cycle) and the 5-minute read and write latency, one day.
- Table: export of the same VM, 288 rows (5-minute samples) × 40 columns (read and write latency of each of 20 virtual disks).
- Condition for the key: one virtual disk (record it in the Notes) has a 5-minute write latency far above the others at 02:15; the VM peak at that time is more than 15 times its 5-minute average.
- Save as `benchmark/questions/89/vm-virtual-disk-latency-one-day.xlsx` and `benchmark/questions/89/vcf-operations-vm-peak-disk-latency.png`.

## Likely wrong answer
"The peak cannot be 40 times the average: the maximum gap is 15x, so the metric is wrong."

## Expected key points
- The peak is real: it is the highest of the 15 twenty-second points in the cycle, taken across all virtual disks, read and write. A VM with 20 virtual disks has 40 sets × 15 points = 600 values, and the peak is the highest.
- The gap can exceed 15x: one or two bursts far above the average.
- The table shows the source: the virtual disk named in the Notes, on writes, at 02:15.
- The VM KPI reads the 20-second peak of the worst virtual disk, so this peak pulls the VM Performance score down for that cycle; there is no SLI.
- A one-off peak with a low average elsewhere is not a pattern: compare the peak with the average across the day.

## Notes
- Previous id: question-0089 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0089"
title: "Disk latency peak 40 times the average"
product: [vcf-operations]
technology: [storage]
task: read-metric
level: 400
answer_type: judged
input: [table, screenshot]
knowledge:
  - vcf-operations/features/peak-20-second-metrics
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
  - vsphere/object-types/vm/vm-performance
attachments:
  - 0089/vm-virtual-disk-latency-one-day.xlsx
  - 0089/vcf-operations-vm-peak-disk-latency.png
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
status: awaiting-input
```
