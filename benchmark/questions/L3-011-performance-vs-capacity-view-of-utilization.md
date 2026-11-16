# Performance vs capacity view of utilization

## Prompt
In a private cloud (finite hardware), choose all the correct statements about performance management and capacity management:

- A. For performance, a host at 100% utilization with no queue is the best case: it does the most work.
- B. For capacity, a cluster near 100% is bad news: demand has passed usable capacity, so add capacity or reclaim.
- C. For performance, low utilization with work queued points to a bottleneck elsewhere.
- D. Capacity asks whether the hosts run hot; performance asks whether the VMs are served well.
- E. Performance looks at seconds to minutes; capacity looks at trends over months.
- F. High CPU utilization of a host or cluster shows that its VMs are slow.
- G. Performance troubleshooting reads VM contention counters; host utilization is left out of it.
- H. When a host's CPU utilization is high, moving VMs off it is the first step for their performance.
- I. Performance is read against usable capacity, so a host above its usable line is a performance risk.
- J. Cluster utilization rising slowly means performance will degrade slowly: the utilization trend shows when it drops.

## Answers
A, B, C, D, E

## Explanation
- A is correct: maximum utilization yields the highest throughput as long as nothing queues.
- B is correct: capacity reads demand against usable capacity, which sits below total capacity after HA, buffer and hypervisor overhead; near 100% there is no room left.
- C is correct: unmet demand at low utilization is common (imbalance, limits); queued work at low utilization means the bottleneck is elsewhere. Check contention: queue, latency, context switch.
- D is correct: cluster capacity looks at the hosts (top down, against usable capacity); cluster performance looks at the VMs inside (bottom up, from their contention).
- E is correct: the two pillars have different time horizons (seconds to an hour against days to a year), although they are intertwined.
- F is wrong: utilization is consumption; a performance problem exists only when the VMs face contention (Ready, Co-stop, memory and disk latency). 100% with no queue is the most work done.
- G is wrong: cluster performance reads contention, and utilization is still used in troubleshooting, for example to find the busiest host.
- H is wrong: high utilization with no contention needs no migration; read the VMs' contention first.
- I is wrong: usable capacity is a capacity concept; performance is read against total capacity and ignores HA, buffer and reservation. Running above the usable line gives more work done, not worse performance.
- J is wrong: performance stays flat while utilization rises, then drops steeply once contention starts, first on the hottest host; a utilization trend does not say when performance drops. Watch contention.
- Misconception: F (high utilization read as a performance problem) and H (the action that follows from it); or G, the over-correction.

## Notes
- For reviewers (kept out of the prompt): "Performance management and capacity management are highly related. Related is not identical: two things that are related are, by that fact, two different things."
- Changed in the 2026-11-15 audit: F, G, H reworded without absolutes and C without hedges (the hedges sat only on true options, the absolutes only on false ones); B reads the cluster; I and J added from the misconceptions of performance-vs-capacity.

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
misconception: [F, H, J]
object: [esxi, cluster]
tool: [none]
knowledge_main: sp5-framework/concepts/performance-vs-capacity
misconception_type: [consumption-as-contention]
pair: "0431"
status: draft
```
