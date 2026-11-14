# A five-minute burst across two collection cycles

## Prompt
- A batch job keeps a 4-vCPU VM at 100% CPU for exactly 5 minutes, from 14:12:30 to 14:17:30. The VM is idle before and after.
- VCF Operations collects the VM every 5 minutes; its collection cycles cover 14:05-14:10, 14:10-14:15, 14:15-14:20 and so on.
- The next morning the job owner opens the VM's CPU|Usage (%) in VCF Operations.

Which statements are correct?

- A. The 5-minute points for 14:10-14:15 and 14:15-14:20 each show about 50%.
- B. The chart shows that the job ran at half load for 10 minutes.
- C. A burst shorter than 5 minutes leaves no trace in 5-minute data.
- D. Open a support case: VCF Operations split one job across two points.
- E. To fill one 5-minute point at full height whatever its start time, the job would have to last about 10 minutes.
- F. The same job started at 14:10:00 would show as one point at about 100%.
- G. Within an hour of the job, the vCenter Real-time chart shows it as about 15 samples near 100%.

## Likely wrong answer
B: the two half-height points read as a long job at half load. Or D: the split read as a collection fault.

## Expected key points
- Answer: A, E, F, G.
- A true: each cycle averages its 15 samples of 20 seconds; half of each cycle was busy and half idle.
- B false: the misconception. Two half-height points come from one full-height burst that straddles a cycle boundary; the 5-minute average says nothing about the shape inside the cycle.
- C false: the over-correction. A short burst lifts the points it falls in by its share of their samples; it is diluted, not erased.
- D false: the wrong action. The split follows from where the job started against the collection cycle; nothing is lost.
- E true: a spike may have to last 10 minutes to cover one whole cycle wherever it starts.
- F true: aligned with a cycle, the 5 busy minutes fill one point.
- G true: the Real-time chart holds 20-second points for the last hour; 5 minutes are 15 samples.

## Notes
- Theory half of the new pair D9; practical half: 0440 (design.md, section 3.9). Different times from the knowledge example (sp5-framework/observability/collection-interval, Short problems), corrected 2026-11-14.
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item D9). Counts only after author approval.

## Metadata
```yaml
id: "0439"
title: "A five-minute burst across two collection cycles"
product: [vcf-operations, vsphere]
technology: [cpu, system]
task: read-metric
level: 300
answer_type: deterministic
input: [text]
object: [vm]
tool: [vcf-operations, vcenter]
knowledge:
  - sp5-framework/observability/collection-interval
  - vsphere/tools/vsphere-client/vcenter-statistics
knowledge_main: sp5-framework/observability/collection-interval
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D9"
answer: [A, E, F, G]
misconception: [B, D]
misconception_type: [rollup-and-interval]
pair: "0440"
status: draft
```
