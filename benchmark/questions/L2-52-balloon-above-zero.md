# Balloon above 0: is the VM slow?

## Prompt
- A VM shows Balloon at 2 GB for the last hour.

Is the VM slow because of memory? What does the balloon tell you, and what do you check?

## Likely wrong answer
"Yes, balloon above 0 means the VM is short of memory and slow."

## Expected key points
- Not necessarily: balloon is the first sign of memory pressure on the host, not unmet demand of the VM.
- The balloon driver inside the Guest OS allocates memory in the guest; ESXi does not back it with physical pages, so other VMs can use them. Whether the guest gave up free or used pages cannot be told.
- Check the VM memory contention (Memory Latency), and swapped and compressed memory, to see whether the VM waits for memory.

## Notes
- Previous id: question-0052 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "52"
title: "Balloon above 0: is the VM slow?"
product: [vsphere]
technology: [memory]
task: read-metric
level: 200
answer_type: judged
input: [text]
knowledge:
  - vsphere/technology/memory/concepts/ballooning
  - vsphere/technology/memory/metrics/virtual-motherboard/ballooned
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 100-200 allocation (benchmark/design.md, section 3.6)"
status: draft
```
