# Actual vs potential memory contention

## Prompt
Which metric best indicates a VM has an actual memory performance problem? Do not select counters that indicate risk but not actual slowness.

- A. VM Memory Ballooned
- B. VM Memory Swapped + Zipped
- C. VM Memory Latency
- D. When Ballooned = Configured.

Hint: separate actual from potential, risk from reality.

## Likely wrong answer
A or B (balloon, swap or compression read as slowness).

## Expected key points
- Answer: C.
- A is potential: the first leading indicator of saturation.
- B is potential: higher risk.
- C is the actual measurement.
- D is illogical (a distractor).

## Notes
- Previous id: vsphere-memory-004 (renamed 2026-11-05).

## Metadata
```yaml
id: "0023"
title: "Actual vs potential memory contention"
product: [vsphere]
technology: [memory]
input: [text]
task: read-metric
knowledge:
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
  - vsphere/technology/memory/metrics/virtual-motherboard/ballooned
  - vsphere/technology/memory/metrics/virtual-motherboard/swapped
  - vsphere/technology/memory/diagnosis/vm-memory-latency-high
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > Memory > Q3 VM Memory Contention"
answer_type: deterministic
level: 400                      # author 2026-11-05
answer: [C]
trap: [A,B]
status: draft
```
