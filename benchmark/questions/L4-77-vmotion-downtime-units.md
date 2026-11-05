# vMotion downtime in VCF Operations for logs

## Prompt
The attached screenshot is a VCF Operations for logs chart of `vmw_esxi_vmdowntime` for the vMotions of one week, and a table of `vmw_esxi_vmprecopystuntime`.

Which statements are correct? Choose all that apply.

- A. A value of 150,000 is 150 ms: within the expected range.
- B. A value of 150,000 is 150 seconds: the VM was down for over two minutes.
- C. Values above 1,000,000 need investigation: downtime above 1 second.
- D. The stun time table shows the VM that was stunned.

## Input to supply
- Tool: VCF Operations for logs (9.1), Explore Logs, chart of the field vmw_esxi_vmdowntime (max per hour) for one week, and a table of vmw_esxi_vmprecopystuntime.
- Condition for the key: most values are below 200,000; at least one value is above 1,000,000. The stun time table shows the ESXi host field.
- Mask host names if they reveal the customer.
- Save as `benchmark/questions/77/vcf-operations-logs-vmotion-downtime.png`.

## Likely wrong answer
B: reading the value as milliseconds or seconds instead of microseconds.

## Expected key points
- Answer: A, C.
- Downtime and stun time are in microseconds. Expected under 200 ms; investigate above 1 second.
- Downtime is the final phase: the VM is quiesced on the source and resumes on the target. It is the largest guest impact of a vMotion.
- D is wrong: the stun time table shows the ESXi host, not the VM name.
- Plot the worst value, not only the average: it is the leading indicator.

## Notes
- Previous id: question-0077 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "77"
title: "vMotion downtime in VCF Operations for logs"
product: [vcf-operations]
technology: [system]
task: read-metric
level: 400
answer_type: deterministic
input: [screenshot]
knowledge:
  - vsphere/object-types/vm/metrics/vmotion
attachments:
  - 77/vcf-operations-logs-vmotion-downtime.png
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
answer: [A, C]
trap: [B]
status: awaiting-input
```
