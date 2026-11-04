# Utilization 50% and Core Utilization 50%

## Prompt
On an ESXi host, CPU Utilization shows 50% and CPU Core Utilization also shows 50%.

What does it tell you?

A. Severe imbalance. Half the cores run 2 threads; the other half is completely idle.
B. Ideal scenario. Each core runs 1 thread, so every running vCPU gets a dedicated core.
C. Nothing. Not enough information to derive any meaningful insight.
D. This combination is not possible. CPU Utilization is always lower than CPU Core Utilization.

## Likely wrong answer
B (equal values read as one thread per core).

## Expected key points
- Answer: A.
- If half the cores run one thread each, Utilization (threads) would be 25%. Utilization at 50% means every running core runs 2 threads.
- B is the opposite of A.
- C is wrong: the two values together give the thread-per-core ratio.
- D is wrong: it is possible, but a corner case.

## Notes

## Metadata
```yaml
id: vsphere-cpu-012
title: "Utilization 50% and Core Utilization 50%"
scope: vsphere
area: cpu
input: text
tests: distinction
knowledge:
  - vsphere/cpu/metrics/host/utilization
  - vsphere/cpu/metrics/host/core-utilization
  - vsphere/cpu/metrics/host/imbalance
  - vsphere/cpu/concepts/hyper-threading
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > CPU > Q9 ESXi CPU Utilisation"
format: multiple-choice
level: l400
answer: [A]
trap: [B]
status: draft
```
