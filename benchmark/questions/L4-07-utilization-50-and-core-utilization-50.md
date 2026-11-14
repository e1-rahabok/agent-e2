# Utilization 50% and Core Utilization 50%

## Prompt
- An ESXi host has Hyper-Threading on: each core runs 2 hardware threads.
- In one Real-time sample of the vSphere Client, the host's CPU Utilization reads 50% and its CPU Core Utilization also reads 50%.

Which statements are correct?

- A. Half the cores run both of their threads while the other half sit idle: the worst possible imbalance.
- B. Each running core runs one thread, so every running vCPU has a core to itself.
- C. Half of the host's threads are free to take more work.
- D. This combination cannot occur: Utilization is always lower than Core Utilization.
- E. The host is out of CPU capacity: add a host before placing more VMs on it.
- F. With Hyper-Threading off, the two counters always read the same.
- G. Half the cores run two threads and the other half run one.
- H. The running vCPUs share their cores with busy sibling threads, which raises their CPU Latency.

## Likely wrong answer
B (equal values read as one thread per core). Or D, the over-correction: equal values read as impossible.

## Expected key points
- Answer: A, C, F, H.
- A is true: Core Utilization counts a core as busy when one or both of its threads run, so 50% means half the cores run; Utilization 50% is half of all threads, so every running core runs both threads. Two threads per running core while cores sit idle is the worst spread.
- B is false: one thread per running core with Core Utilization at 50% would give Utilization 25%.
- C is true: Utilization is the share of threads in use; for capacity, half the threads are free.
- D is false: with Hyper-Threading on, Utilization ranges from half of Core Utilization up to Core Utilization; equal values are the case where every running core runs both threads.
- E is false: half the threads are free; capacity is counted in threads.
- F is true: each core is one thread, so the two counters are the same.
- G is false: that spread would give Core Utilization 100% and Utilization 75%.
- H is true: a vCPU on a thread whose sibling is busy loses throughput to Hyper-Threading, which CPU Latency counts (up to 37.5%).

## Notes
- Rewritten 2026-11-14 as the theory half of 0004 (project/question-pairing-2026-11-14.md, A1; design.md 3.9): the stem states that Hyper-Threading is on; one fact per option; old C ("Nothing. Not enough information") was vague; E (the wrong action), F, G and H are new. Key changed from A to A, C, F, H (author approved, 2026-11-14).
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
  - vsphere/technology/cpu/metrics/virtual-motherboard/latency
knowledge_main: vsphere/technology/cpu/metrics/host/utilization
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > CPU > Q9 ESXi CPU Utilisation"
answer_type: deterministic
level: 400                      # author 2026-11-05
answer: [A, C, F, H]
misconception: [B, D]
misconception_type: [average-hides-worst, frequency-and-hyper-threading]
pair: "0004"
status: draft
```
