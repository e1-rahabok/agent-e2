# A cluster above 90% CPU and a request for hosts

## Prompt
- The capacity manager sends [the VCF Operations cluster CPU chart](0431/vcf-operations-cluster-cpu-usage-7-days.png): "CPU usage has been above 90% most of the week. The VMs must be suffering. Order two hosts now to fix the performance."
- You add [the list of the cluster's VMs by CPU contention](0431/vcf-operations-cluster-vms-cpu-contention-7-days.png) for the same week.

Which statements are correct?

- A. CPU usage above 90% for most of the week shows that the VMs of this cluster are waiting for CPU.
- B. Even the VM with the highest CPU contention of the week stays low, so the VMs get the CPU they ask for.
- C. Order the two hosts now to restore the VMs' performance.
- D. For performance, a cluster doing this much work with no queue is in a good state.
- E. For capacity, the cluster has little room left for new workload or growth at this usage.
- F. The usage chart has no value in this case: only contention counts.
- G. The usage chart reads the provider; the contention list reads the consumers, the VMs.

## Input to supply
- Product and version: VCF Operations 9.1, a vSphere 9.1 cluster with DRS.
- Screen 1: the cluster > Metrics, metric CPU|Usage (%), last 7 days. Save as `0431/vcf-operations-cluster-cpu-usage-7-days.png`.
- Screen 2: a list view of the cluster's VMs (Environment > the cluster > the VMs, or a custom list view) with the column CPU|Contention (%) and the transformation Maximum over the same 7 days, sorted highest first; the top 10-20 VMs visible. Save as `0431/vcf-operations-cluster-vms-cpu-contention-7-days.png`.
- How to produce it: a production or lab cluster that runs hot but fits; a lab can run CPU burners in many small VMs (1-2 vCPUs each) spread by DRS, with total vCPUs below the cluster's physical threads.
- Condition the key depends on: cluster CPU|Usage (%) at 90% or more for most of the business hours of the week; the highest VM's maximum CPU|Contention (%) over the week below 3%; no VM with a CPU limit.
- Masking: mask every VM, host, datastore and cluster name, including names in chart titles and legends.

## Likely wrong answer
A: high utilization read as a performance problem, and C, the action that follows from it. Or F, the over-correction.

## Expected key points
- Answer: B, D, E, G.
- A false: the misconception. Usage is consumption; a performance problem exists only when the VMs face contention, and the worst VM's contention stays low.
- B true: the worst VM is the depth of the cluster's performance; when even it stays low, no VM waits for long.
- C false: the wrong action. Hosts do not fix a performance problem that does not exist; the capacity question is separate.
- D true: high utilization with no queue is the most work done; for performance it is the best case.
- E true: capacity is read against usable capacity, which sits below total once HA and buffer are taken out; at this usage the cluster has little room for growth.
- F false: the over-correction. Utilization is the input to capacity and still serves troubleshooting, for example to find the busiest host.
- G true: utilization is the provider view; contention per VM is the consumer view.

## Notes
- Practical half of 0019 (pair: design.md, section 3.9).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C7). The options hold for any capture that meets the condition above. Counts only after author approval.

## Metadata
```yaml
id: "0431"
title: "A cluster above 90% CPU and a request for hosts"
product: [vcf-operations, vsphere]
technology: [cpu, system]
task: decide-capacity
level: 400
answer_type: deterministic
input: [screenshot]
object: [cluster, vm]
tool: [vcf-operations]
knowledge:
  - sp5-framework/concepts/performance-vs-capacity
  - vsphere/object-types/cluster/concepts/cluster-utilization-vs-contention
  - sp5-framework/observability/aggregation
knowledge_main: sp5-framework/concepts/performance-vs-capacity
attachments:
  - 0431/vcf-operations-cluster-cpu-usage-7-days.png
  - 0431/vcf-operations-cluster-vms-cpu-contention-7-days.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C7"
answer: [B, D, E, G]
misconception: [A, C]
misconception_type: [consumption-as-contention, provider-vs-consumer]
pair: "0019"
status: awaiting-input
```
