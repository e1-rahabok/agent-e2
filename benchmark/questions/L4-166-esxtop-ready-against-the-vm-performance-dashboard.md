# esxtop Ready against the VM Performance dashboard

## Prompt
- VM app-db-07: 8 vCPUs, on host esx-11. VCF Operations 9.1 and vCenter 9.1, default settings.
- At 10:02:15 an engineer opens esxtop on esx-11 (CPU panel, default 5-second refresh), expands the VM and reads one refresh of its vCPU worlds:

| World | %RDY | %CSTP |
|---|---|---|
| vcpu-0 | 15.8 | 0.2 |
| vcpu-1 | 16.4 | 0.1 |
| vcpu-2 | 17.1 | 0.3 |
| vcpu-3 | 15.2 | 0.2 |
| vcpu-4 | 16.0 | 0.1 |
| vcpu-5 | 16.9 | 0.2 |
| vcpu-6 | 15.5 | 0.1 |
| vcpu-7 | 16.3 | 0.2 |

- He closes esxtop after that refresh. At 10:40 he opens the VM Performance dashboard for app-db-07, collection cycle 10:00-10:05: CPU Ready (%) 1.9, Peak vCPU Ready within collection cycle 5.6, Co-stop (%) 0.1.
- He writes: "esxtop shows about 16% Ready on every vCPU, the dashboard 1.9% and 5.6%. VCF Operations under-reports Ready."

Which statements are correct?

- A. Both readings can be right: one 5-second esxtop refresh against a 5-minute mean and the cycle's highest 20-second value.
- B. With no other Ready in vcpu-2's 20-second sample, that sample averages under 5%, below the 5.6% peak.
- C. VCF Operations lost data: a vCPU at 16-17% Ready in esxtop must show at least that much in Peak vCPU Ready for the cycle.
- D. The dashboard reads the esxtop %RDY field from the host, so its 1.9% comes from a quieter esxtop sample than the one he saw.
- E. A 5-second esxtop refresh is too short to mean anything; only the 5-minute values describe the VM's CPU contention.
- F. Until about 11:00 the vCenter Real-time chart shows each vCPU's Ready per 20 seconds, the samples behind the peak.
- G. Open a case with the vendor, since VCF Operations under-reports this VM's Ready by about a factor of 3 at the peak.
- H. Use the VM Contention dashboard instead, which VCF Operations 9.1 maintains as the current dashboard for this check.

## Answers
A, B, F

## Explanation
- A is correct: esxtop fields are sampled every few seconds per world (5 seconds by default); the VM Performance dashboard shows VCF Operations metrics on the VM object per 5 minutes, as an average and as the 20-second peak. The values are not comparable.
- B is correct: vcpu-2 had 17.1% of 5 seconds in Ready, about 0.86 seconds. Spread over a 20-second sample with no other Ready, that is 0.86 / 20 = about 4.3%, under the 5.6% peak. A burst that lasts seconds is diluted in a 20-second average.
- C is wrong: the misconception that esxtop %RDY and the dashboard values are the same reading. A peak of the 20-second averages can sit far below a 5-second esxtop value.
- D is wrong: VCF Operations collects vCenter's 20-second samples; it does not read esxtop fields.
- E is wrong: the over-correction. esxtop samples are finer than vCenter and VCF Operations, which is why they catch bursts the 20-second and 5-minute values dilute.
- F is correct: the Real-time chart keeps the 20-second samples for about an hour, with Ready per vCPU whatever the statistics level; VCF Operations takes the peak of the same 15 samples of each cycle. At 10:40 the 10:02 samples are still there.
- G is wrong: nothing is under-reported; the action follows from C.
- H is wrong: in VCF Operations 9.1 VM Contention is marked (DEP), deprecated, and superseded by VM Performance; it also shows VCF Operations metrics, not esxtop fields.
- Misconception: C and D: "esxtop showed 16%, so the dashboard should show 16%; VCF Operations missed it." G is the action that follows from that reading.

## Notes
- The esxtop rows are per vCPU world (the VM expanded with e), so no option rests on the summed group row.

## Metadata
```yaml
id: "0467"
title: "esxtop Ready against the VM Performance dashboard"
product: [vsphere, vcf-operations]
technology: [cpu]
task: read-metric
level: 400
answer_type: deterministic
input: [text]
object: [vm]
tool: [esxtop, vcf-operations, vcenter]
knowledge:
  - vcf-operations/dashboards/vm-performance-dashboard
  - vcf-operations/features/peak-20-second-metrics
  - vsphere/tools/vsphere-client/vcenter-statistics
  - vsphere/tools/esxtop/overview
knowledge_main: vcf-operations/dashboards/vm-performance-dashboard
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-15, question bank audit gap: vcf-operations/dashboards/vm-performance-dashboard"
misconception: [C, D]
misconception_type: [tool-confusion, rollup-and-interval]
status: draft
```
