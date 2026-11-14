# A quiet host and one busy thread

## Prompt
- An ESXi 9.1 host: 2 sockets of 24 cores, Hyper-Threading on, 96 threads.
- vCenter, last hour: host CPU Utilization (%) about 11%, Usage (%) about 13%.
- The owner of a VM on this host says a single-threaded report job is CPU-bound. The host team answers that the host is nearly idle.

Which statements are correct?

- A. Host Utilization (%) is the average of the utilization of its threads.
- B. One thread busy all the time moves the Utilization of a 96-thread host by about 1 point.
- C. With the host at about 11%, no thread can have been much busier than about 11%.
- D. On a lightly loaded host, uneven load among threads is normal: it follows the workloads and where they are placed.
- E. A thread near 100% on a quiet host shows that the ESXi scheduler balances the load badly.
- F. Add a host to the cluster so that the report job gets more CPU.
- G. To find a hot thread, read the busiest thread, not the host value.
- H. Which thread is the hot one can change over time without changing the conclusion.
- I. Host Usage (%) is built on the cores of the host, so one busy core barely moves it either.
- J. A single-threaded job runs faster when its VM gets more vCPUs.

## Likely wrong answer
C: the host is at 11%, so nothing on it can be busy. The job cannot be CPU-bound.

## Expected key points
- Answer: A, B, D, G, H, I.
- A true: each thread has its own 100%; the host value is their average.
- B true: 100 / 96 is about 1.04 points.
- C false: the misconception. An average over 96 threads hides one or a few threads at 100%.
- D true: imbalance among cores is expected while utilization is low; the scheduler spreads vCPUs across cores, but load follows the work and NUMA placement.
- E false: over-correction. Imbalance at low load is not a fault.
- F false: wrong action. The host has plenty of free threads; a single-threaded job is held by one vCPU, not by the cluster's capacity.
- G true: the host average cannot show one hot thread; the per-thread values (or their maximum) can.
- H true: threads can take turns being the hot one; the reading is the same.
- I true: host Usage is summed over physical cores and based on Core Utilization, an average over cores, adjusted for frequency.
- J false: the work runs on one thread; more vCPUs add idle vCPUs.

## Notes
- Paired with the practical question 0379 (theory and practical; design.md, section 3.9). Situation numbers differ from 0379 on purpose.
- The VCF Operations host metric for the busiest core is left out: its presence in VCF Operations 9.1 is not confirmed (Aria Operations 8.16 documents CPU|Peak CPU Core Usage). Fairness F2.
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item D5). Counts only after author approval.

## Metadata
```yaml
id: "0378"
title: "A quiet host and one busy thread"
product: [vsphere]
technology: [cpu]
task: read-metric
level: 300
answer_type: deterministic
input: [text]
object: [esxi]
tool: [vcenter]
knowledge:
  - vsphere/technology/cpu/metrics/host/peak-core-usage
  - vsphere/technology/cpu/metrics/host/utilization
  - vsphere/technology/cpu/metrics/host/usage
  - vsphere/technology/cpu/metrics/host/core-utilization
  - sp5-framework/observability/aggregation
knowledge_main: vsphere/technology/cpu/metrics/host/peak-core-usage
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D5"
answer: [A, B, D, G, H, I]
misconception: [C]
misconception_type: [average-hides-worst]
pair: "0379"
status: draft
```
