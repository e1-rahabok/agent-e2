# Utilization 50% and Core Utilization 50%

## Prompt
- An ESXi host has Hyper-Threading on: each core runs 2 hardware threads.
- In one Real-time sample of the vSphere Client, the host's CPU Utilization reads 50% and its CPU Core Utilization also reads 50%.

Which statements are correct?

- A. Whenever a core ran in this sample, both of its threads ran: the worst spread for this load.
- B. Each running core runs one thread, so every running vCPU has a core to itself.
- C. Half of the host's threads are still free to take more vCPUs or kernel work.
- D. With Hyper-Threading on this cannot occur: Utilization always sits below Core Utilization.
- E. Turning off Hyper-Threading is the recommended fix for this spread of threads.
- F. With Hyper-Threading off, the two counters always read the same.
- G. Half the cores run two threads and the other half run one thread each.
- H. Both threads busy on every running core would be expected once Core Utilization reaches 100%.

## Answers
A, C, F, H

## Explanation
- A is true: Core Utilization counts a core as busy while one or both of its threads run; Utilization is the mean over all threads. Per core, Core Utilization adds the time one thread runs and the time both run, Utilization adds half the first and all of the second; the two are equal only if no core ever ran a single thread. So a running core always ran both threads: two threads per running core (imbalance score 2.0) while core time sits idle is the worst spread. The sample does not say whether half the cores ran all the time or every core ran half the time.
- B is false: one thread per running core with Core Utilization at 50% would give Utilization 25%.
- C is true: Utilization is the share of threads in use; for capacity, half the threads are free.
- D is false: with Hyper-Threading on, Utilization ranges from half of Core Utilization up to Core Utilization; equal values are the case where every running core runs both threads.
- E is false: Performance Best Practices for vSphere 9.1 recommends Hyper-Threading on. The scheduler already places vCPUs on separate cores first; uneven core load comes from the workload and NUMA placement, and half the threads are still free.
- F is true: each core is one thread, so the two counters are the same.
- G is false: that spread would give Core Utilization 100% and Utilization 75%.
- H is true: a score of 2.0 is a concern only while cores are idle; at 100% Core Utilization two threads per core are expected.
- Misconception: B (equal values read as one thread per core). Or D, the over-correction: equal values read as impossible.

## Notes
- Rewritten 2026-11-14 as the theory half of 0004 (project/question-pairing-2026-11-14.md, A1; design.md 3.9): the stem states that Hyper-Threading is on; one fact per option; old C ("Nothing. Not enough information") was vague; E (the wrong action), F, G and H are new; D scoped to Hyper-Threading on (review 2026-11-15), so that F does not contradict it. Key changed from A to A, C, F, H (author approved, 2026-11-14).
- Changed in the 2026-11-15 audit: A reworded (a time-averaged sample does not prove that half the cores sat idle); throwaway E (out of capacity) replaced by the Hyper-Threading-off fix; H (CPU Latency from a busy sibling, tested in 0002 and 0102) replaced by the imbalance-at-100% fact.
- Paired with 0004 (theory and practical, design.md 3.9).

## Metadata
```yaml
id: "0012"
title: "Utilization 50% and Core Utilization 50%"
product: [vsphere]
technology: [cpu]
input: [text]
task: read-metric
object: [esxi]
tool: [vcenter]
knowledge:
  - vsphere/technology/cpu/metrics/host/utilization
  - vsphere/technology/cpu/metrics/host/core-utilization
  - vsphere/technology/cpu/metrics/host/imbalance
  - vsphere/technology/cpu/concepts/hyper-threading
knowledge_main: vsphere/technology/cpu/metrics/host/utilization
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > CPU > Q9 ESXi CPU Utilisation"
answer_type: deterministic
level: 400                      # author 2026-11-05
misconception: [B, D]
misconception_type: [average-hides-worst, frequency-and-hyper-threading]
pair: "0004"
status: draft
```
