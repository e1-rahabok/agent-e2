---
id: vsphere-storage-003
title: "Latency and outstanding IO"
scope: vsphere
area: storage
input: text
tests: concept
knowledge:
  - vsphere/storage/metrics/virtual-machine/outstanding-io
  - vsphere/storage/metrics/virtual-machine/disk-latency
  - vsphere/storage/metrics/virtual-machine/iops
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > Storage > Q1 Latency vs OIO"
status: draft
---

## Prompt
What is the relationship between the disk latency metric and disk outstanding IO?

A. None. The correlation is weak: one is before processing, the other after.
B. Outstanding IO = IO commands per second x Latency
C. Outstanding IO = IO commands per second / Latency
D. Outstanding IO = Throughput x Latency

## Likely wrong answer
A, or D (throughput instead of commands).

## Expected key points
- Answer: B (Little's law).
- The higher the latency, the longer the queue at a given IOPS.
- D is wrong: OIO counts commands, not data size.
- Units: IOPS (per second) x latency (seconds) = commands in flight.

## Notes

