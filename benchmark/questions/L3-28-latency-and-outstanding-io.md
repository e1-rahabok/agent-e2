# Latency and outstanding IO

## Prompt
What is the relationship between the disk latency metric and disk outstanding IO?

- A. None. The correlation is weak: one is before processing, the other after.
- B. Outstanding IO = IO commands per second x Latency
- C. Outstanding IO = IO commands per second / Latency
- D. Outstanding IO = Throughput x Latency

## Likely wrong answer
A, or D (throughput instead of commands).

## Expected key points
- Answer: B (Little's law).
- The higher the latency, the longer the queue at a given IOPS.
- D is wrong: OIO counts commands, not data size.
- Units: IOPS (per second) x latency (seconds) = commands in flight.

## Notes
- Previous id: vsphere-storage-003 (renamed 2026-11-05).

## Metadata
```yaml
id: "28"
title: "Latency and outstanding IO"
product: [vsphere]
technology: [storage]
input: [text]
task: explain-mechanism
knowledge:
  - vsphere/technology/storage/metrics/virtual-motherboard/outstanding-io
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
  - vsphere/technology/storage/metrics/virtual-motherboard/iops
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > Storage > Q1 Latency vs OIO"
answer_type: deterministic
level: 300                      # author 2026-11-05
answer: [B]
trap: [A,D]
status: draft
```
