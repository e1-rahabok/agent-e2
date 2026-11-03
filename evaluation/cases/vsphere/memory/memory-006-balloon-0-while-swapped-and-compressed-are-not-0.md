---
id: vsphere-memory-006
title: "Balloon 0 while Swapped and Compressed are not 0"
scope: vsphere
area: memory
input: text
tests: troubleshooting
knowledge:
  - vsphere/memory/metrics/host/ballooned
  - vsphere/memory/metrics/host/swap-used
  - vsphere/memory/metrics/host/compressed
  - vsphere/memory/concepts/swap-and-compression
  - vsphere/memory/concepts/host-memory-states
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > Memory > Q5 ESXi Memory Utilisation"
status: draft
---

## Prompt
On ESXi 007:
- The balloon counter has been flat at 0 for the last 24 hours.
- In the same period, Swapped and Compressed are both above 0.
- Consumed is not high. There is clearly capacity to deploy another VM.

Choose the correct statements:

A. This is not possible. Ballooning happens before swapping and compression. If balloon is 0, compressed and swapped must be 0 too.
B. Swapping and compression happened in the past. The pages were not recalled by their VMs since, so they stay in that state.
C. ESXi is not under memory pressure, so it has no reason to inflate the balloon.
D. This happens because of memory tiering.

## Likely wrong answer
A (reclamation order read as a current-state rule) or D.

## Expected key points
- Answer: B, C.
- A is wrong: Swapped and Compressed are accumulative (state) counters.
- B is correct: prove it with the rate counters (swap in/out rate, compression rate).
- C is correct.
- D is wrong: memory tiering is transparent to these counters.

## Notes

