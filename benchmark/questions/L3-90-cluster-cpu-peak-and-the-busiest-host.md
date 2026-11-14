# Cluster CPU peak and the busiest host

## Prompt
- Cluster prod-cl09: 12 identical hosts, DRS fully automated.
- Over the past month, the cluster's CPU|Usage (%) in VCF Operations, in 5-minute points, peaked at 78%.
- The capacity manager writes in the monthly report: "No host passed 78% this month."

Which statements are correct?

- A. At each 5-minute point, the cluster's CPU usage is the average of its hosts' usage.
- B. A cluster peak of 78% means that no host passed 78%.
- C. At the point where the cluster reached 78%, at least one host was at 78% or higher.
- D. The true peak takes the busiest host at each point, then the highest of those over the month.
- E. The busiest host can change from one 5-minute point to the next.
- F. Plan the cluster's capacity on the busiest host's peak rather than on the cluster average.
- G. Report the month's highest host CPU usage as 78%.
- H. The risk that one host runs hot is read from the busiest host, not from the cluster average.

## Likely wrong answer
B: the cluster peak read as a ceiling for every host, and G, the report that follows from it. Or F, the over-correction.

## Expected key points
- Answer: A, C, D, E, H.
- A true: a cluster utilization is an average across its hosts at each point; with identical hosts, total usage over total capacity is their mean.
- B false: the misconception. The average of the hosts at each point hides a host that may be near 100%.
- C true: an average cannot exceed its highest member; for the cluster to average 78%, at least one host was at 78% or above.
- D true: across time and across members are two kinds of peak; the true peak is the highest of all host points, found by taking the busiest host at each point.
- E true: the busiest host moves over time as DRS and the workload move.
- F false: the over-correction. Capacity is planned per cluster, so the cluster average against usable capacity is the right input; the busiest host is a risk signal.
- G false: the wrong action. 78% is the peak of the average; the highest host value was at least as high and can be far higher.
- H true: an average of 12 hosts reacts too late; a problem on one host is already a problem, so the risk reading takes the highest host.

## Notes
- Theory half of the new pair D3; practical half: 0438 (design.md, section 3.9).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item D3). Counts only after author approval.

## Metadata
```yaml
id: "0437"
title: "Cluster CPU peak and the busiest host"
product: [vcf-operations, vsphere]
technology: [cpu, system]
task: read-metric
level: 300
answer_type: deterministic
input: [text]
object: [cluster, esxi]
tool: [vcf-operations]
knowledge:
  - sp5-framework/observability/aggregation
  - sp5-framework/concepts/performance-vs-capacity
  - vsphere/object-types/cluster/concepts/cluster-utilization-vs-contention
knowledge_main: sp5-framework/observability/aggregation
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D3"
answer: [A, C, D, E, H]
misconception: [B, G]
misconception_type: [average-hides-worst]
pair: "0438"
status: draft
```
