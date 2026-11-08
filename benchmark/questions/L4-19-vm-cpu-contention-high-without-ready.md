# High CPU Contention without Ready

## Prompt
- In VCF Operations, a VM shows CPU Contention at 40%.
- In the same hour:
  - VM CPU Ready: 0.3%. VM CPU Co-stop: 0.05%.
  - Guest OS CPU Run Queue and Context Switch: low. Guest OS CPU Usage: normal.
- The ESXi host power management is Balanced.

Which statements are correct? Choose all that apply.

- A. The cause is frequency scaling and Hyper-Threading, not CPU starvation.
- B. The VM is starved of CPU: add a host to the cluster.
- C. Setting power management to maximum performance rules out frequency scaling; Hyper-Threading then remains as a cause.
- D. Raise the VM's CPU shares to remove the contention.

## Likely wrong answer
B: reading Contention above 37.5% as starvation.

## Expected key points
- Answer: A, C.
- CPU Contention in VCF Operations includes the effect of frequency scaling and Hyper-Threading. With Ready, Co-stop and the Guest OS queues all low, those two are the cause.
- Hyper-Threading cuts per-thread CPU time by about 37.5%; applications rarely notice.
- Power management at maximum rules out frequency scaling. Shares do not help: there is no contention between VMs to arbitrate.

## Notes
- Previous id: question-0059 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0059"
title: "High CPU Contention without Ready"
product: [vsphere, vcf-operations]
technology: [cpu]
task: troubleshoot
level: 400
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high
  - vcf-operations/metrics/vm/cpu-contention
  - vsphere/technology/cpu/concepts/hyper-threading
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
answer: [A, C]
trap: [B]
status: draft
```
