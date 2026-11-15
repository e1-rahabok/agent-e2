# A six-minute job across two collection cycles

## Prompt
- A batch job keeps a 4-vCPU VM at 100% CPU for 6 minutes, from 14:12:00 to 14:18:00. The VM is idle before and after.
- VCF Operations collects the VM every 5 minutes; its collection cycles cover 14:05-14:10, 14:10-14:15, 14:15-14:20 and so on.
- The next morning the job owner opens the VM's CPU|Usage (%) in VCF Operations.

Which statements are correct?

- A. The 5-minute points for 14:10-14:15 and 14:15-14:20 each show about 60%.
- B. The chart shows that the job ran at 60% for 10 minutes.
- C. Two adjacent equal points prove the job ran at full load for exactly the cycle length.
- D. Open a support case: VCF Operations split one job across two points.
- E. To fill one 5-minute point at full height whatever its start time, the job would have to last about 10 minutes.
- F. Started at 14:10:00, the same job would fill the 14:10-14:15 point at about 100%.
- G. Within an hour of the job, the vCenter Real-time chart shows it as about 18 samples near 100%.

## Likely wrong answer
B: the two points read as a long job at a steady 60%. Or D: the split read as a collection fault.

## Expected key points
- Answer: A, E, F, G.
- A true: each cycle averages its 15 samples of 20 seconds; 3 of the 5 minutes of each cycle were busy.
- B false: the misconception. The points come from one full-height burst that straddles a cycle boundary; a 5-minute average says nothing about the shape inside the cycle.
- C false: the over-correction. Equal adjacent points only show that the busy time was split evenly; here the job ran 6 minutes, longer than one cycle.
- D false: the wrong action. The split follows from where the job started against the collection cycle; nothing is lost.
- E true: a spike may have to last 10 minutes to cover one whole cycle wherever it starts.
- F true: aligned with a cycle, 5 of the 6 busy minutes fill the 14:10-14:15 point.
- G true: the Real-time chart holds 20-second points for the last hour; 6 minutes are 18 samples.

## Notes
- Review 2026-11-15: a 6-minute job (points about 60%), so the theory half no longer shares the situation and numbers of the practical half 0440; C is now the over-correction of the split pattern. Key unchanged.
- Theory half of the new pair D9; practical half: 0440 (design.md, section 3.9). Different times from the knowledge example (sp5-framework/observability/collection-interval, Short problems), corrected 2026-11-14.
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item D9). Counts only after author approval.

## Metadata
```yaml
id: "0439"
title: "A six-minute job across two collection cycles"
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
