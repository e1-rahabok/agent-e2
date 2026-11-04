# Performance vs capacity view of utilization

## Prompt
Performance management and capacity management are highly related, so they are not the same thing.

In a private cloud (finite hardware), choose all the correct statements:

A. For performance, 100% utilization is not only good, it is perfect. As long as there is no queue, higher utilization means more throughput.
B. For capacity, 100% utilization is bad news, especially if it breaches Usable Capacity. Capacity is low: add capacity or reclaim.
C. For performance, low utilization may be bad news: no work is being done. Check for a bottleneck elsewhere causing it.
D. ESXi capacity looks at ESXi utilization; ESXi performance looks at how it serves its running VMs. Two perspectives.
E. The time horizon of performance is short (seconds to minutes); capacity management considers longer trends.

## Likely wrong answer
Rejecting A (100% utilization seen as a performance problem) or C.

## Expected key points
- Answer: all (A to E).
- A: maximum utilization yields the highest throughput.
- B: capacity management keeps a buffer because procurement takes time.
- C: check contention: context switch, queue, latency.
- D: provider vs consumer perspective.
- E: the two pillars have different time horizons, although they are intertwined.

## Notes

## Metadata
```yaml
id: vsphere-general-001
title: "Performance vs capacity view of utilization"
scope: vsphere
area: general
input: text
tests: concept
knowledge:
  - operations-management/capacity/capacity-model
  - vsphere/object-types/cluster/concepts/cluster-utilization-vs-contention
  - foundations/metric-perspectives
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > CPU > Q10 Performance vs Capacity"
format: multiple-choice
level: l400
answer: [A,B,C,D,E]
trap: []
status: draft
```
