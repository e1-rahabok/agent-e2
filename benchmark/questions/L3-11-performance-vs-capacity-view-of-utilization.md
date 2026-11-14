# Performance vs capacity view of utilization

## Prompt
In a private cloud (finite hardware), choose all the correct statements about performance management and capacity management:

- A. For performance, a host at 100% utilization with no queue is the best case: it does the most work.
- B. For capacity, a host near 100% is bad news: demand has passed usable capacity, so add capacity or reclaim.
- C. For performance, low utilization can be bad news: work may be held up by a bottleneck elsewhere.
- D. Capacity reads a host's own utilization; performance reads how well the host serves its running VMs.
- E. Performance looks at seconds to minutes; capacity looks at trends over months.
- F. A cluster at 95% CPU usage has a VM performance problem.
- G. Utilization plays no part in performance troubleshooting.
- H. When a host runs at 95% CPU usage, migrate VMs off it to restore their performance.

## Likely wrong answer
F (high utilization read as a performance problem) and H (the action that follows from it); or G, the over-correction.

## Expected key points
- Answer: A, B, C, D, E.
- A is true: maximum utilization yields the highest throughput as long as nothing queues.
- B is true: capacity is measured against usable capacity and keeps a buffer, because procurement takes time.
- C is true: unmet demand at low utilization is common (imbalance, limits); check contention: queue, latency, context switch.
- D is true: the provider view (the host's utilization) against the consumer view (its VMs' contention).
- E is true: the two pillars have different time horizons, although they are intertwined.
- F is false: utilization is consumption; a performance problem exists only when the VMs face contention (Ready, Co-stop, memory and disk latency).
- G is false: cluster performance reads contention, and utilization is still used in troubleshooting, for example to find the busiest host.
- H is false: high utilization with no contention needs no migration; read the VMs' contention first.

## Notes
- Hint moved out of the prompt (author, 2026-11-14: a hint helps the frontier model, not the local model), for reviewers: "Performance management and capacity management are highly related. Related is not identical: two things that are related are, by that fact, two different things."
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): A-E one fact each; F (the misconception), G (its over-correction) and H (the wrong action) added, so not every option is true. Key unchanged, A to E (author approved, 2026-11-14).

## Metadata
```yaml
id: "0019"
title: "Performance vs capacity view of utilization"
product: [vsphere]
technology: [system]
input: [text]
task: explain-mechanism
knowledge:
  - sp5-framework/concepts/performance-vs-capacity
  - vsphere/object-types/cluster/concepts/cluster-utilization-vs-contention
  - sp5-framework/observability/metric-perspectives
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > CPU > Q10 Performance vs Capacity"
answer_type: deterministic
level: 300                      # author 2026-11-05
answer: [A, B, C, D, E]
misconception: [F, H]
object: [esxi, cluster]
tool: [none]
knowledge_main: sp5-framework/concepts/performance-vs-capacity
misconception_type: [consumption-as-contention]
pair: "0431"
status: draft
```
