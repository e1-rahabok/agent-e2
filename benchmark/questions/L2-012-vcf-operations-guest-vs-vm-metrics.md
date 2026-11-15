# Guest OS metrics in the VM metric tree

## Prompt
Review [the attached screenshot](0051/vcf-operations-vm-guest-and-cpu-metrics.png).

Which of these metrics are Microsoft Windows or Linux metrics, not VMware VM metrics? Choose all that apply.

- A. Guest | CPU Queue
- B. CPU | Ready
- C. Guest | Free Memory
- D. CPU | Co-stop


## Screenshot
![VCF Operations Metrics tab of a Windows VM: Guest CPU Queue, CPU Ready, Guest Free Memory, CPU Co-stop](0051/vcf-operations-vm-guest-and-cpu-metrics.png)

## Likely wrong answer
Taking every metric on the VM object as a VM metric.

## Expected key points
- Answer: A, C.
- The Guest group comes from inside Windows through VMware Tools. It is stored on the VM object, but the Guest OS layer produces it.
- Ready and Co-stop are measured by the VMkernel: VM metrics the Guest OS cannot see.
- Decide by the layer that produces a metric, not by the object that stores it.

## Notes
- 2026-11-14 (project/question-pairing-2026-11-14.md, section 3.B): in the screenshot, the VM name masked in the title and the four chart headings (author: every VM name is masked); the stale `## Input to supply` removed.
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0051"
title: "Guest OS metrics in the VM metric tree"
product: [vcf-operations, vsphere, windows]
technology: [system]
task: read-metric
level: 200
answer_type: deterministic
input: [screenshot]
knowledge:
  - vsphere/architecture/vm-vs-guest-os
  - vsphere/architecture/metric-sources
attachments:
  - 0051/vcf-operations-vm-guest-and-cpu-metrics.png
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
answer: [A, C]
misconception: [B]
object: [vm, guest-os]
tool: [vcf-operations]
knowledge_main: vsphere/architecture/vm-vs-guest-os
misconception_type: []
status: reviewed
```
