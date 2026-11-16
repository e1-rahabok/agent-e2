# An alert on host Utilization to catch single-threaded jobs

## Prompt
- A capacity team plans one alert per ESXi host: CPU Utilization (%) above 80% for 15 minutes. They expect it to catch the single-threaded month-end jobs that run slowly.
- The hosts have 2 sockets of 28 cores, Hyper-Threading on: 112 threads.

Which statements are correct?

- A. Host Utilization (%) is the mean of the utilization of each of its threads.
- B. A single thread busy all the time adds about 1 point to the Utilization of a 112-thread host.
- C. Below 80% host Utilization, no thread of the host can be saturated.
- D. Read across the threads, the maximum warns of a hot thread earlier than the 95th percentile does.
- E. Threads loaded unevenly on a quiet host mean the scheduler is misbalanced, which is worth its own alert.
- F. When the month-end jobs run slowly, add hosts to the cluster to give them more CPU.
- G. To catch one saturated thread, a check must read the busiest thread, not the host value.
- H. Which thread runs hot can change between samples without changing that reading.
- I. Host Usage (%) rests on the host's cores as a whole, so it hides one busy core in the same way.
- J. Host Utilization should be dropped from capacity planning, since it hides busy threads.

## Likely wrong answer
C: if the host stays below 80%, no single thread can be saturated, so the alert catches the jobs.

## Expected key points
- Answer: A, B, D, G, H, I.
- A true: each thread has its own 100%; the host value is their average.
- B true: 100 / 112 is about 0.9 points.
- C false: the misconception. An average over 112 threads hides one or a few threads at 100%.
- D true: the busiest-core reading uses Max(), not the 95th percentile: both lead to the same remediation, and Max() warns earlier. Among 112 threads the 95th percentile drops the top five or so, so one hot thread does not move it.
- E false: over-correction. Imbalance among threads at low load is normal: load follows the workloads and their NUMA placement.
- F false: wrong action. A single-threaded job is held by one thread's speed, not by the cluster's free capacity.
- G true: the host average cannot show one hot thread; the per-thread values, or their maximum, can.
- H true: threads can take turns being the hot one; the reading is the same.
- I true: host Usage is summed over physical cores and based on Core Utilization, an average over cores, adjusted for frequency.
- J false: over-correction. Thread Utilization is the host's capacity reading (space); it only cannot show the speed of one thread.

## Notes
- Paired with the practical question 0379 (theory and practical; design.md, section 3.9). Situation numbers differ from 0379 on purpose.
- The VCF Operations host metric for the busiest core is left out: its presence in VCF Operations 9.1 is not confirmed (Aria Operations 8.16 documents CPU|Peak CPU Core Usage). Fairness F2.
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item D5). Counts only after author approval.
- Changed 2026-11-16 (re-review): D (the alert stays silent on a quiet host) followed directly from B; D now tests the maximum against the 95th percentile (peak-core-usage, Design), still true.
- Changed in the 2026-11-15 audit: J reworded ("of no use" was an absolute in a wrong option); F lengthened.
- F rests on a fact no knowledge file states yet: a single-threaded job is bound by one core's clock, so free threads or another host do not speed it up (peak-core-usage says only "Not capacity"). Decidable from public knowledge today; add the line to the knowledge base.
- Review 2026-11-15: new situation (an alert plan of a capacity team), away from the story of 0379; options reworded. Key letters A, B, D, G, H, I, on the new options.

## Metadata
```yaml
id: "0378"
title: "An alert on host Utilization to catch single-threaded jobs"
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
