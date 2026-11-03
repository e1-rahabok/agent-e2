# Which counter to size VM CPU

## Prompt
A correctly sized VM balances performance, capacity and cost. Choose the most accurate counter from the list. The context is sizing, not performance troubleshooting.

A. VM CPU Usage (MHz)
B. VM CPU Usage (%)
C. VM CPU Demand (MHz)
D. VM CPU Demand (%)
E. VM CPU Run - Overlap. In VCF Operations this is CPU Net Run (%).

Hint: since a VM is a motherboard, what you size is the Guest OS, not the VM. You size Windows or Linux, not a piece of hardware.

## Likely wrong answer
C or D (Demand), because it includes unmet demand; or A/B (Usage).

## Expected key points
- Answer: E.
- A and B are wrong: you size the Guest OS. Frequency-based metrics measure throughput.
- C and D are wrong: Demand is an internal counter the kernel uses for scheduling decisions. It does not apply to the Guest OS.
- More accurate: configured vCPU - Idle + a CPU Run Queue factor. No such counter exists; build it as a super metric.

## Notes

## Metadata
```yaml
id: vsphere-cpu-008
title: "Which counter to size VM CPU"
scope: vsphere
area: cpu
input: text
tests: distinction
knowledge:
  - vsphere/system/concepts/rightsizing
  - vsphere/system/concepts/guest-os-sizing
  - vsphere/cpu/metrics/virtual-motherboard/net-run
  - vsphere/cpu/metrics/virtual-motherboard/demand
  - vsphere/cpu/metrics/virtual-motherboard/usage
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > CPU > Q5 VM CPU Rightsize"
format: multiple-choice
level: l400
answer: [E]
trap: [C,D]
status: draft
```
