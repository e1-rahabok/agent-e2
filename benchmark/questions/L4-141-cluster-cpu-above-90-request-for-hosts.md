# A week of cluster CPU and a request for hosts

## Prompt
- The capacity manager sends [the VCF Operations export of cluster prod-cl03](0431/vcf-operations-cluster-cpu-7-days.csv) for the past week, one row per hour: "Look at the cluster's CPU this week. The VMs must be suffering. Order two hosts now to fix the performance."
- You export [the cluster's VMs with their CPU for the same week](0431/vcf-operations-cluster-vms-cpu-7-days.csv) from VCF Operations.

Which statements are correct?

- A. A week this busy in the cluster's CPU usage means the cluster's VMs are being slowed down.
- B. Even the VM with the week's highest CPU contention stays below 1%: the VMs get the CPU they ask for.
- C. Order the two hosts now to restore the performance of the cluster's VMs.
- D. The VMs get the most work done that these hosts can give them this week.
- E. The cluster has little room left for the next project's workload.
- F. Once the VMs' contention is read, the cluster's CPU usage answers no remaining question.
- G. The cluster's CPU usage reads the provider; the VMs' contention reads the consumers.
- H. The VMs' average contention is the fairer reading: the top VM's value overstates the cluster.

## Answers
B, D, E, G

## Explanation
- A is wrong: the misconception. Usage is consumption; a performance problem exists only when the VMs face contention, and the top row of the VM export, `CPU|Contention (%) (Max)`, is below 1%. Many VMs read `CPU|Usage (%) (Max)` near 100%: busy, not waiting.
- B is correct: the VM export's highest `CPU|Contention (%) (Max)` over the week is below 1%; the worst VM is the depth of the cluster's performance, so no VM waits for long.
- C is wrong: the wrong action. Hosts do not fix a performance problem that does not exist; the capacity question is separate.
- D is correct: high utilization with no queue is the most work done; for performance it is the best case.
- E is correct: capacity is read against usable capacity, which sits below total once HA and buffer are taken out, and against demand, which is at least the utilization. `CPU|Usage (%) (Avg)` is 90% or more in most weekday business hours (09:00-18:00), so the cluster has little room for new workload.
- F is wrong: the over-correction. The cluster's usage answers the capacity question (E); utilization also serves troubleshooting, for example to find the busiest host.
- G is correct: utilization is the provider view; contention per VM is the consumer view.
- H is wrong: an average across the VMs hides the worst; the worst VM gives the depth of the cluster's performance and the average says nothing about it. Here the top VM is below 1% anyway, so the reading changes no conclusion.
- Misconception: A: high utilization read as a performance problem, and C, the action that follows from it. Or F, the over-correction.

## Notes
- Changed in the 2026-11-15 audit: H replaced (a misread of the usage column) by the average-across-VMs reading (aggregation, Depth and breadth); the generator's check that usage passes 80% still holds but no option rests on it now.
- Converted to an export 2026-11-15 (project/practical-questions-as-exports-2026-11-15.md, row 0431): a seeded VCF Operations list view of the cluster, one row per hour for 7 days (Avg and Max of the 5-minute values, plus the cluster's average contention), and a list of the cluster's 140 VMs with the weekly Max of CPU Contention and CPU Usage, sorted by contention. The manager's quote no longer states the level ("very high all week"), so the level is read from the export (E). A, F, G, H reworded from chart and list to the export's values. The list view CSV format is assumed (project/tools/exportgen/README.md). The key holds for the generated export; the generator checks every condition against the rows.
- Practical half of 0019 (pair: design.md, section 3.9).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C7). Counts only after the author's approval.
- Changed in the 2026-11-16 re-review: the title no longer states the level ("above 90%"), which the stem leaves to the export; the note on the quote now names E, the option that reads the level.

## Metadata
```yaml
id: "0431"
title: "A week of cluster CPU and a request for hosts"
product: [vcf-operations, vsphere]
technology: [cpu, system]
task: decide-capacity
level: 400
answer_type: deterministic
input: [table]
object: [cluster, vm]
tool: [vcf-operations]
knowledge:
  - sp5-framework/concepts/performance-vs-capacity
  - vsphere/object-types/cluster/concepts/cluster-utilization-vs-contention
  - sp5-framework/observability/aggregation
knowledge_main: sp5-framework/concepts/performance-vs-capacity
attachments:
  - 0431/vcf-operations-cluster-cpu-7-days.csv
  - 0431/vcf-operations-cluster-vms-cpu-7-days.csv
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C7"
misconception: [A, C]
misconception_type: [consumption-as-contention, provider-vs-consumer]
pair: "0019"
status: draft
```
