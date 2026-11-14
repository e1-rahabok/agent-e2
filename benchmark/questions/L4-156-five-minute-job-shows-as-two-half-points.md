# A five-minute job shows as two half-height points

## Prompt
- An application owner says a batch job ran his VM at full CPU for 5 minutes. He sends [the vCenter Real-time chart](0440/vcenter-vm-cpu-usage-real-time.png) taken during the job, and [the VCF Operations chart](0440/vcf-operations-vm-cpu-usage-2-hours.png) of the same VM from later that day.
- He asks why VCF Operations shows no point above about half, and thinks VCF Operations lost data.

Which statements are correct?

- A. The job ran at about half load for 10 minutes, as the VCF Operations chart shows.
- B. The job started partway through a collection cycle, so its 5 minutes are split across two points.
- C. Each of the two points averages about half busy samples and half idle ones.
- D. VCF Operations lost samples during the job; open a support case.
- E. 5-minute data can never show a 5-minute burst at full height.
- F. The Real-time chart shows the job at its full height because its points are 20-second averages.
- G. VCF Operations CPU Usage is a different counter from the vCenter one, which explains the lower peak.

## Input to supply
- Product and version: vSphere 9.1 (vSphere Client) and VCF Operations 9.1 collecting from that vCenter every 5 minutes.
- Object: one idle VM with 2 or 4 vCPUs.
- How to produce it: in VCF Operations, read the time stamps of the VM's 5-minute CPU|Usage (%) points (for example 10:02, 10:07, 10:12). Start a CPU burner on all vCPUs 2.5 minutes after one of them (for example at 10:04:30) for exactly 300 seconds (Linux: `stress-ng --cpu 0 --timeout 300s`).
- Screen 1: vSphere Client > the VM > Monitor > Performance > Advanced > CPU, Chart Options: Real-time, counter Usage (%), object the VM, captured within the hour, with the legend table. Save as `0440/vcenter-vm-cpu-usage-real-time.png`.
- Screen 2: VCF Operations > the VM > Metrics, CPU|Usage (%), a 2-hour range around the job, after two or more later cycles have been collected; hover or zoom so the two points are readable. Save as `0440/vcf-operations-vm-cpu-usage-2-hours.png`.
- Condition the key depends on: the Real-time chart shows 14-16 consecutive samples at 90% or more, with the samples before and after below 10%; VCF Operations shows two adjacent points each between 40% and 60%, the points before and after below 10%, and no point above 70%.
- Masking: mask every VM, host, datastore and cluster name, including names in chart titles and legends.

## Likely wrong answer
A: two half-height points read as a long job at half load. Or D: the split read as lost data.

## Expected key points
- Answer: B, C, F.
- A false: the misconception. The Real-time chart shows one 5-minute plateau near 100%, not 10 minutes at half load.
- B true: the burst straddles a cycle boundary; each cycle holds half of it.
- C true: a VCF Operations 5-minute value averages the cycle's 15 samples of 20 seconds; about half of each cycle was busy.
- D false: the wrong action. Nothing is lost; the split follows from where the job started against the cycle.
- E false: the over-correction. A 5-minute burst aligned with a cycle fills one point at full height; a burst that may start anywhere needs about 10 minutes to fill one whole point.
- F true: Real-time points are 20-second averages, short enough to show a 5-minute plateau at full height.
- G false: VM CPU Usage is passed through from vCenter; the same samples, averaged over the 5-minute cycle, give the lower points.

## Notes
- Practical half of the new pair D9; theory half: 0439 (design.md, section 3.9).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item D9). The options hold for any capture that meets the condition above. Counts only after author approval.

## Metadata
```yaml
id: "0440"
title: "A five-minute job shows as two half-height points"
product: [vcf-operations, vsphere]
technology: [cpu, system]
task: troubleshoot
level: 400
answer_type: deterministic
input: [screenshot]
object: [vm]
tool: [vcenter, vcf-operations]
knowledge:
  - sp5-framework/observability/collection-interval
  - vsphere/tools/vsphere-client/vcenter-statistics
  - vcf-operations/vcf-operations-role
knowledge_main: sp5-framework/observability/collection-interval
attachments:
  - 0440/vcenter-vm-cpu-usage-real-time.png
  - 0440/vcf-operations-vm-cpu-usage-2-hours.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D9"
answer: [B, C, F]
misconception: [A, D]
misconception_type: [rollup-and-interval, tool-confusion]
pair: "0439"
status: awaiting-input
```
