# A five-minute job shows as two half-height points

## Prompt
- An application owner says a batch job kept his VM rpt-batch-11 (4 vCPUs) busy for a few minutes. During the job he exported [the VM's vCenter Real-time CPU](0440/vcenter-vm-cpu-real-time.csv); later that day he exported [the VM's CPU|Usage (%) from VCF Operations](0440/vcf-operations-vm-cpu-usage-2-hours.csv) for two hours around the job.
- He thinks VCF Operations lost data during the job.

Which statements are correct?

- A. The job ran at about half load for 10 minutes, as the VCF Operations export shows.
- B. The job started partway through a collection cycle, so its 5 minutes are split across two VCF Operations values.
- C. Each of those two values averages about half busy samples and half idle ones.
- D. VCF Operations lost samples during the job; open a support case.
- E. 5-minute data can never show a 5-minute burst at full height.
- F. The vCenter Real-time export shows the job at its full height because its rows are 20-second averages.
- G. The VCF Operations export has one value near 100% at the time of the job.

## Likely wrong answer
A: two half-height points read as a long job at half load. Or D: the split read as lost data.

## Expected key points
- Answer: B, C, F.
- A false: the misconception. `Usage for rpt-batch-11` in the vCenter export holds 15 consecutive rows (5 minutes) at 90% or more, with the rows before and after below 10%: one 5-minute plateau near 100%, not 10 minutes at half load.
- B true: the vCenter time stamps are UTC and the VCF Operations ones GMT+08:00. The first busy vCenter row is 02:05:20Z, so the job started at 02:05:00Z (10:05:00 local), inside the cycle that ends at 10:07:40; the job ends inside the cycle that ends at 10:12:40. Those two VCF Operations values are the only ones between 40% and 60%.
- C true: a VCF Operations 5-minute value is the mean of the cycle's 15 samples of 20 seconds; the 10:07:40 value is the mean of the vCenter rows 02:03:00Z to 02:07:40Z (8 busy, 7 idle), the 10:12:40 value the mean of 02:08:00Z to 02:12:40Z (7 busy, 8 idle).
- D false: the wrong action. Nothing is lost; every VCF Operations value covered by the vCenter export equals the mean of its 15 rows, and the split follows from where the job started against the cycle.
- E false: the over-correction. A 5-minute burst aligned with a cycle fills one point at full height; a burst that may start anywhere needs about 10 minutes to fill one whole point.
- F true: Real-time rows are 20 seconds apart, each a 20-second average, short enough to show a 5-minute plateau at full height.
- G false: the two values that hold the job read between 40% and 60%; no value passes 70%.

## Notes
- Review 2026-11-15: the owner's question no longer gives the chart's value; G (VCF Operations CPU Usage as a different counter) dropped, as no knowledge file settles it; G is now a false reading of the chart. Key unchanged.
- Converted to an export 2026-11-15 (project/practical-questions-as-exports-2026-11-15.md, row 0440): a seeded vCenter Real-time export (30 minutes, 20-second rows, Usage plus the Readiness columns of the CPU % view) and a VCF Operations chart export (2 hours, 5-minute values); every VCF Operations value is the mean of its 15 twenty-second samples. The owner's question no longer says that VCF Operations never shows the full peak, so G is read from the export. A, B, C, F, G reworded from chart and points to the exports' values. The key holds for the generated exports; the generator checks every condition against the rows.
- Practical half of the new pair D9; theory half: 0439 (design.md, section 3.9).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item D9). Counts only after author approval.

## Metadata
```yaml
id: "0440"
title: "A five-minute job shows as two half-height points"
product: [vcf-operations, vsphere]
technology: [cpu, system]
task: troubleshoot
level: 400
answer_type: deterministic
input: [table]
object: [vm]
tool: [vcenter, vcf-operations]
knowledge:
  - sp5-framework/observability/collection-interval
  - vsphere/tools/vsphere-client/vcenter-statistics
knowledge_main: sp5-framework/observability/collection-interval
attachments:
  - 0440/vcenter-vm-cpu-real-time.csv
  - 0440/vcf-operations-vm-cpu-usage-2-hours.csv
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D9"
answer: [B, C, F]
misconception: [A, D]
misconception_type: [rollup-and-interval]
pair: "0439"
status: draft
```
