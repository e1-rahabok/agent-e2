# Questions for the author

Not indexed. One entry per question.

How to answer:

- Write your reply after `Answer:`. Any length; a letter is enough where there are options.
- Leave `Answer:` empty to skip a question for now.
- Tell Claude the file is updated. Claude applies each answer and moves the entry to [author-questions-resolved.md](author-questions-resolved.md).
- Two sections: Release 1.0 (answer before release 1.0) and Future release.

Each entry:

- Files: the files the answer changes.
- Search: verbatim strings, only for a question about the book.
- Now: what the knowledge base says today.
- Question: what Claude needs from you, with options where they help.
- Recommended: Claude's choice and the reason.
- Answer: for you.

## Release 1.0

### Q-E2-266 · Capacity > Supply · Hosts out of service in total capacity

- Files: [Supply: total and usable capacity](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/supply.md), section Total vs usable after host loss; [Cluster Consumption (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-consumption.md), section Usable capacity and its review note on maintenance mode.
- Adapter text: VCF vCommunity Adapter, [docs/reference/metrics/cluster-consumption.md, lines 30-31](https://github.com/e1-rahabok/PCM-Adapter/blob/de3d6b728a9ac24a2a2f265345285484c90af56d/docs/reference/metrics/cluster-consumption.md#L30-L31), PCM-Adapter commit de3d6b7: "Total Capacity and Usable Capacity count hosts differently. Total Capacity covers every host in the cluster, whatever its state, and changes only when a host is added or removed. Usable Capacity counts only the hosts that can run VMs. A host in maintenance mode, disconnected, powered off or in standby stays in Total Capacity but adds nothing to Usable Capacity." and "Open question: does VCF Operations keep a host that is down in its Total Capacity? [...] This has not been checked on a live system."
- Now:
  - supply: "DPM takes hosts out of total capacity; maintenance mode keeps them in total and takes them out of usable capacity." and "Total Capacity counts only hosts connected to vCenter. A disconnected host's value goes blank."
  - cluster-consumption: "A left-out host stays in total capacity but adds nothing to usable capacity." The left-out hosts include hosts in standby (DPM) and disconnected hosts.
  - The adapter page agrees with cluster-consumption. supply contradicts both for a host in standby and for a disconnected host. Agent E2 answers capacity questions on the live demo from both files.
- Question: which hosts does VCF Operations keep in the Total Capacity of a cluster (`cpu|capacity_provisioned`, `mem|host_provisioned`)?
  - A. supply is right: a host in standby or disconnected leaves Total Capacity; a host in maintenance mode stays. cluster-consumption changes, and the adapter page with it.
  - B. The adapter page is right: every host stays until it is removed from the cluster. supply changes.
  - C. Not known yet: the lab session of milestone M8 reads both stats with one host in maintenance mode, one in standby and one disconnected. Until then, supply and cluster-consumption each carry a review note.
- Recommended: C, unless you know it from the field. The two files disagree, and the adapter marks the point as unchecked.
- Answer:

### Q-E2-265 · Capacity > Close for Business · The Cluster Risk level that new VMs can reopen

- Files: [Cluster Risk (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-risk.md), section Sub-metric weight in Cluster Risk; [Modelling a pillar into one number](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/modelling.md), section Three ways to combine the colours; [Close for Business](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/close-for-business.md), section The rule and its review note.
- Adapter text: VCF vCommunity Adapter, [docs/concepts/kpi-scoring-models.md, line 30](https://github.com/e1-rahabok/PCM-Adapter/blob/de3d6b728a9ac24a2a2f265345285484c90af56d/docs/concepts/kpi-scoring-models.md#L30), PCM-Adapter commit de3d6b7: "This matters for decisions: the Close for Business rule checks Risk at its orange closure level, above 60, so a cluster just above 60 can drop below it after more VMs are deployed, and open again." The same in [docs/reference/metrics/cluster-risk.md, line 201](https://github.com/e1-rahabok/PCM-Adapter/blob/de3d6b728a9ac24a2a2f265345285484c90af56d/docs/reference/metrics/cluster-risk.md#L201).
- Now:
  - cluster-risk: "A cluster just above orange (50) can drop to yellow after VMs are deployed."
  - modelling: "Close for Business reads Risk at orange, so a cluster just inside orange can drop to yellow after VMs are deployed and open again."
  - close-for-business: Risk closes a cluster at its orange closure level, above 60; the display band turns orange above 50. A cluster with Cluster Risk between 50 and 60 is open already, so a drop to yellow opens nothing. The adapter's sentence agrees with close-for-business.
  - The review note of close-for-business says the pack "closes at the display band edges (25, 50, 75)". The pack now closes at 20, 40, 60 and 80 (`CLOSE_RED_BELOW = 20.0` in PCM-Adapter's periodic_cluster_check.py). It still applies the production Risk setting to every cluster.
- Question: which level do cluster-risk and modelling name?
  - A. The closure level: a cluster just above 60, the orange closure level of Close for Business, can drop below it after VMs are deployed, and open again. The review note keeps only the one Risk setting for every cluster.
  - B. Keep both files as they are.
- Recommended: A. Agent E2 and isvara.io's articles would otherwise explain a reopening at a level where nothing closes.
- Answer:

### Q-E2-264 · Terms · Grader or judge for the model that scores free-text answers

- Files: [project/terms.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/terms.md), the row "judge"; [answer-service.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/requirements/answer-service.md), R-E2-005; [benchmark/free-text-rubric.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/free-text-rubric.md).
- Now: terms.md names the model that scored free-text answers 0-3 the "judge" and lists "grader" as the word to avoid. R-E2-005, the workspace's ROADMAP (milestone M3) and the new rubric file call the tool that scores the answer set of release 1.0 the "grader". Both name one concept: a model that scores a free-text answer by the rubric.
- Question: which word do the repositories use?
  - A. "grader": terms.md changes its row; "judge" stays only in the history of the deleted benchmark tool.
  - B. "judge": R-E2-005, the ROADMAP and the rubric file change before M3 builds the tool.
- Recommended: A. M3 builds the tool under this name, the requirements already use it, and the old judge is deleted from main.
- Answer:

## Future release

### Q-E2-271 · Performance and capacity > Metric pages · An empty host's score, and the estate summary of the clusters

- Files: [ESXi Performance (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/esxi/esxi-performance.md), section Misconceptions; [Cluster Performance (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/cluster-performance.md); [Cluster and ESXi availability metrics](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/metrics/availability.md), section Roll-up; [Performance dashboards](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/outputs/performance-dashboards.md), section Misconceptions.
- Adapter pages: VCF vCommunity Adapter, PCM-Adapter commit de3d6b7. The other claims of the metric pages are in a knowledge file, in Q-E2-131 (Cluster Risk and Cluster Consumption are models) or in Q-E2-265, Q-E2-266, Q-E2-269 and Q-E2-270; the table of every claim is in the PCM-Adapter pull request for R-REPO-002.
- Now:
  1. [esxi-performance.md, line 54](https://github.com/e1-rahabok/PCM-Adapter/blob/de3d6b728a9ac24a2a2f265345285484c90af56d/docs/reference/metrics/esxi-performance.md#L54): "A host with no powered-on VMs. No VM sub-metric has data, and bad packets are 0 and left out. Nothing is wrong, so the KPI is 100." esxi-performance: "Host with no VMs scores 100, so the host is fine → the KPI has nothing to score; availability and configuration are separate health check steps." The score of 100 is in both; "Nothing is wrong" contradicts the misconception.
  2. [vsphere-world-metrics.md, line 3](https://github.com/e1-rahabok/PCM-Adapter/blob/de3d6b728a9ac24a2a2f265345285484c90af56d/docs/reference/metrics/vsphere-world-metrics.md#L3): "Six metrics on the vSphere World object summarize the Cluster Performance, Cluster Risk and Cluster Consumption scores of every cluster across all vCenters, so you can watch the whole estate in one place." Each takes the worst cluster and the edge of the worst 10% of the clusters. No knowledge file holds a roll-up of these three scores. availability holds one for availability (average, worst cluster, count below 100%). performance-dashboards: "Group the whole estate in one view → group by class of service and by Datacenter."
- Question:
  1. A: drop "Nothing is wrong" with the page (the knowledge base stays); B: change the misconception.
  2. A: no roll-up in the knowledge base; B: add a section Roll-up to cluster-performance, as availability has: the worst cluster and the 10th percentile of the clusters (90th for Cluster Risk and Cluster Consumption, in their files), read per class of service or Datacenter in a large estate.
- Recommended: 1 A. 2 B. The pack publishes these six values on vSphere World, so users will ask what they mean; grouping first keeps the misconception of performance-dashboards true.
- Answer:

### Q-E2-270 · Performance > Business application KPI · The member KPI, the namespaces and the enterprise

- Files: [Business application KPI](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/business-application-kpi.md), section KPI structure; [KPI design](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/performance-kpi-design.md), section One KPI per realm; [IT leaders dashboards](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/outputs/it-leaders-dashboards.md).
- Adapter text: VCF vCommunity Adapter, [docs/reference/metrics/business-application-performance.md, lines 15-17](https://github.com/e1-rahabok/PCM-Adapter/blob/de3d6b728a9ac24a2a2f265345285484c90af56d/docs/reference/metrics/business-application-performance.md#L15-L17), PCM-Adapter commit de3d6b7. The pack computes these values; its code (`application_performance`, the higher value) follows the super metric it replaced.
- Now:
  1. Tier Performance: "The average VM Guest OS KPI of the Tier's VMs." business-application-kpi: "Member: its own KPI, VM Performance (%) for a VM". performance-kpi-design: "For the application team the two are one entity: report the VM GOS KPI, the average of VM Performance (%) and Guest OS Performance (%)."
  2. Business Application Performance: "The highest of these values: the Performance of each of its K8S Namespaces, and the lowest Tier Performance of its Tiers." business-application-kpi: "Application: the worst of its tiers. Tiers work in sequence, like a convoy". The pack takes the highest value once an application has a namespace.
  3. Business Applications Performance, on the Enterprise: "The average of the Business Applications of the Enterprise." No knowledge file holds it.
- Question:
  1. The member KPI. A: VM Performance (%), as business-application-kpi says. B: the VM Guest OS KPI, as the pack and performance-kpi-design.
  2. A namespace. A: a namespace is a tier, so the application is the worst of its tiers and namespaces, and the pack changes after 1.0. B: the highest, as the pack.
  3. The enterprise. A: add the average to business-application-kpi. B: leave it out.
- Recommended: 1 B: the application runs in the Guest OS, and the application team reads one number per VM. 2 A: microservices also serve a request in sequence, and the highest value hides the slowest part. 3 B: business leaders read IT per application (it-leaders-dashboards), and an average of the crown jewels hides the one that suffers.
- Answer:

### Q-E2-269 · Availability > Cluster · Operational availability with N+k

- Files: [Cluster and ESXi availability metrics](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/metrics/availability.md), section Cluster availability. Related: Q-E2-222, Q-E2-226.
- Adapter text: VCF vCommunity Adapter, [docs/reference/metrics/operational-availability.md](https://github.com/e1-rahabok/PCM-Adapter/blob/de3d6b728a9ac24a2a2f265345285484c90af56d/docs/reference/metrics/operational-availability.md), PCM-Adapter commit de3d6b7. The plan names this page as the source of the availability model after 1.0; the pack computes these rules.
- Now:
  1. Line 45: "k is the number of host failures vSphere HA tolerates, `configuration|dasConfig|hostFailoverLevel` (N+k). The k spare hosts are assumed to be the k worst hosts, so any other degraded host counts against the cluster." Lines 80-81 name the fault the pack fixed in the super metric: "One host was always set aside: a healthy N+0 cluster of 4 hosts showed 75 %, and a healthy single host 0 %." and "Only one host was set aside, whatever the failover level (N+2 or more)." availability holds N+1 only: "Considers HA: N+1 reports 100% with 1 host unavailable (ignore the worst host, average the rest)."
  2. Line 17: "No HA host failover level counts as N+0. This applies when vSphere HA is off, when admission control uses a percentage of resources or a dedicated failover host, or when the value was not collected." No knowledge file holds it.
  3. Line 18: "A cluster where HA tolerates the failure of every host has no value. For example, a 2-host cluster with a failover level of 2: N − k is 0." No knowledge file holds it.
- Question: does availability take the rule for N+k (items 1 to 3)?
  - A. Yes: set the k worst hosts aside for N+k; a cluster without a host failover level is N+0; N − k = 0 has no value.
  - B. Keep N+1 only until the availability model after 1.0.
- Recommended: A. It is the N+1 line of the file for any k, and the pack already publishes it.
- Answer:

### Q-E2-268 · SP5 > Modelling · Claims of the adapter's KPI scoring page

- Files: [Modelling a pillar into one number](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/modelling.md), section Three ways to combine the colours; [KPI design](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/performance-kpi-design.md).
- Adapter page: VCF vCommunity Adapter, [docs/concepts/kpi-scoring-models.md](https://github.com/e1-rahabok/PCM-Adapter/blob/de3d6b728a9ac24a2a2f265345285484c90af56d/docs/concepts/kpi-scoring-models.md), PCM-Adapter commit de3d6b7. The other claims of the page are in modelling, in performance-kpi-design, in Q-E2-131 or in Q-E2-265; the table of every claim is in the PCM-Adapter pull request for R-REPO-002.
- Now (line of the page; what modelling holds):
  1. Line 15: "Several red sub-metrics | Each one counts. | Each one counts. Two reds can already reach the end of the scale. | Each one pushes the KPI further into red." Line 38: "Once two sub-metrics are red the KPI is at the end of the scale, so a cluster with two red leading indicators looks the same as one with six." modelling has no row for several reds; its Rule row holds "same-colour metrics push deeper", and its Ranking row holds "bad clusters all show the end of the scale".
  2. Line 38: "A sum also needs a fixed scale: someone has to decide how many reds make 100, and the source tables don't say." Not in modelling.
  3. Line 22: "It is the standard fix for an average that moves the wrong way, because a sub-metric's weight can't jump when its value changes." Not in modelling.
  4. Line 24: "A second red sub-metric counts half as much as the first only because it comes second, and a fifth red one barely counts." modelling: "a fifth counts nothing". With the weights 8, 4, 2 and 1 a fifth has no weight; if the halving goes on, it has 0.5.
  5. Line 24: "The result is mathematically sound, but an operator can't relate it to the colors of the sub-metrics on the screen." modelling gives the reason as "Ranking throws away the vSphere meaning of each colour".
  6. Line 48: "losing all disks is worse than losing one disk, one NIC, one HBA, one fan and one PSU together." modelling holds the two tables of availability without an example.
  7. Line 40: "A yes-or-no decision that must never move the wrong way, such as closing a cluster, where the difference between bad and very bad doesn't change the answer." modelling holds the best fit without the example.
  8. Line 63: "for these three KPIs the direction of the KPI matters as much as its color." Not in modelling.
- Question: for each item, A: the knowledge base stays as it is, and the claim goes with the page; B: add it to modelling, section Three ways to combine the colours. Item 4: does a fifth red count nothing (A) or barely (B)?
- Recommended: 1 B: it puts a number on the weakness of the sum. 2 B. 3 B: it says why rank weights were the candidate. 4 A: modelling lists four weights. 5 A: modelling's reason covers it. 6 B: an example of a failure that overrides the others. 7 A: Close for Business reads weighted-average scores, and the example suggests a sum. 8 A: no mechanism behind it.
- Answer:

### Q-E2-267 · Capacity > Capacity model · Claims of the adapter's capacity model page

- Files: [Supply: total and usable capacity](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/supply.md); [Capacity demand](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/demand.md); [Cluster Risk (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-risk.md); [Cluster Consumption (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-consumption.md); [KPI vs SLA](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/kpi-vs-sla.md); [ESXi CPU Imbalance](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/imbalance.md); [Overcommit ratio](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/overcommit.md); [vSphere cluster: operations complexity](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/concepts/cluster-operations.md); [Can this cluster take more VMs?](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/decision-tree/can-cluster-take-more-vms.md).
- Adapter page: VCF vCommunity Adapter, [docs/concepts/capacity-management.md](https://github.com/e1-rahabok/PCM-Adapter/blob/de3d6b728a9ac24a2a2f265345285484c90af56d/docs/concepts/capacity-management.md), PCM-Adapter commit de3d6b7. Its diagram is the one in demand, with the closure logic of can-cluster-take-more-vms under it. The other claims of the page are in a knowledge file or in Q-E2-131; the table of every claim is in the PCM-Adapter pull request for R-REPO-002.
- Now (line of the page; what the knowledge base holds):
  1. Lines 29, 30, 41 and 54: "Buffer: capacity kept free for HA and DR.", "the usable capacity, which is the total capacity minus the buffer", "Capacity kept free for HA and DR. It sets how high Utilization can go." and "Buffer (%) | Is the HA and DR capacity still free?" supply contradicts them: Usable Capacity = Total Capacity − Availability protection − Overhead − Buffer, the buffer is applied after HA, and its misconception reads "Buffer = HA → buffer applies after HA". The diagram has one box, Buffer, for all three.
  2. Line 63: "A smaller buffer raises the risk. With less headroom, Consumption turns red sooner." Not in the knowledge base. A smaller buffer gives a larger usable capacity, so the same load reads a lower Cluster Consumption, which turns red later, with less physical room left.
  3. Line 77: "A host has no usable capacity of its own, so its numbers are measured against what the host physically has." supply contradicts it: "ESXi Usable Capacity = Total Capacity - Hypervisor".
  4. Lines 56 and 64: "Contention (%) | Are the VMs waiting for resources? This is the performance SLA." and "Contention is measured at the VM, because the VM's experience is what the SLA covers." kpi-vs-sla contradicts them: "Performance monitoring and troubleshooting use the KPI only. No performance SLA, no SLI, no SLO." The diagram says "Performance SLA to avoid complaint-based operations"; overcommit says it with a KPI.
  5. Line 55: "Consumption (%) | How much of the usable capacity is consumed? The average over the cluster." cluster-consumption contradicts it: "Cluster Consumption is the average of the hosts → it adds up the hosts: a big host counts more." The diagram says "Average. Against Usable".
  6. Line 67: "Imbalance: both hyper-threads of a core are busy. Each thread then gets much less than a full core, so thread utilization overstates the headroom." imbalance: two threads share a core while other cores idle, and "Score 2.0 is always bad → bad only while cores are idle". No file says that thread utilization overstates the headroom.
  7. Line 66: "Monster VM: a VM that is large compared to its host. It is hard to place, especially after a host failure, and it competes with everything else on the host." cluster-operations holds the competition; no file says a monster VM is hard to place after a host failure.
  8. Line 77: "DRS can't always fix this: a monster VM, affinity rules or reservations can pin load to one host." Not in the knowledge base; supply names affinity rules and pinning as pockets of resource.
  9. Line 43: "When VMs are charged to a tenant, it is derived from Utilization and justifies the price. When VMs are free, Utilization drives the plan on its own." overcommit holds the price. The two paths from Utilization are drawn in the diagram (VM Price to Allocation; VM is free to Consumption) and written in no file.
  10. Line 18: "Who does it | The architect, once per cluster design". Not in the knowledge base.
- Question: for each item, A: the knowledge base stays as it is, and the claim goes with the page; B: add the claim to the file named in the recommendation.
- Recommended: 1 A: supply names HA, DR and buffer apart; the diagram's Buffer box holds all three. 2 A: the reasoning runs the other way. 3 A, and add to cluster-risk, section Purpose, the reason the page means: host rows read the host's physical capacity, because HA and the buffer are reserved across the cluster and not on one host (cluster-consumption says this for the cluster). 4 A: operations use the KPI. 5 A: the cluster-wide value is the sum of the hosts against usable capacity, which the misconception guards. 6 A: imbalance holds the mechanism. 7 B, to cluster-risk, section Monster VM: HA restarts the whole VM on one surviving host. 8 B, to cluster-risk, section Purpose, beside the reason for the worst host. 9 B, to demand, section Allocation, as the diagram draws it. 10 A.
- Answer:

### Q-E2-263 · Diagrams · Scope of the SVG rule

- Files: [writing.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/knowledge-rules/writing.md), section Format choices; [CLAUDE.md](https://github.com/e1-rahabok/agent-e2/blob/main/CLAUDE.md), section Repository layout.
- Search strings: "Root documents are not indexed and are for people"; "Diagrams in the root documents are SVG".
- Now: both say diagrams in the root documents are hand-laid SVG. [benchmark/README.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/README.md) and [harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md), section 3, are not root documents and follow the rule too.
- Question: does the rule cover every document for people, or the root documents only?
  - A. Every document for people (not indexed); knowledge files keep Mermaid.
  - B. The root documents only.
- Recommended: A. The other documents already follow it, and one rule for every document for people needs no list.
- Answer:

### Q-E2-262 · Decision trees · Three trees with no branches

- Files: [Does this ESXi host have CPU headroom?](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/decision-tree/host-cpu-capacity-headroom.md), [Downsizing a large, idle VM](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/decision-tree/oversized-vm-downsizing.md), [Is memory overcommit affecting this VM?](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/decision-tree/is-overcommit-affecting-vm.md); the Mermaid chart in each.
- Now: each is a list of checks in order with no branch, so its new chart is a straight line (is-overcommit has one branch: no ballooning, not affected). The decisions sit in section Interpretation as prose (for example, Core Utilization below 100% or Thread Utilization below 50%: cores are free).
- Question: draw the branches in each chart. Claude then updates the numbered steps to match.
  - A. Yes, I edit the three charts.
  - B. Claude drafts the branches from section Interpretation; I review the charts.
  - C. Leave them as straight lines.
- Recommended: B. The branches are already written in Interpretation; turning them into arrows is drafting, and you review the result visually.
- Answer:

### Q-E2-261 · Health check · Is the log a performance check?

- Files: [Health check](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/health-check.md), sections Order of checks and the chart; [flows.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/knowledge-rules/flows.md), the Order line.
- Now: flows.md and the file's text give performance as contention, consumption, configuration, known bug. The chart had a fifth step, Log, after known bug. The model never sees the chart, so the chart now follows the text (2026-11-24).
- Question: does the performance part of a health check read logs?
  - A. No. Keep it as now.
  - B. Yes, last, after known bug. Add it to the text and flows.md.
- Recommended: A. Plan, Not doing: log analysis (logs are mostly about availability and security, not performance); availability and security already read logs.
- Answer:

### Q-E2-258 · Capacity > Cluster Consumption · The grey band: when is a cluster underused?

- Files: [thresholds-capacity.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-capacity.yaml), section sizing and its review note; [user_suggestions.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/user_suggestions.py).
- Search strings: "grey (below green: wastage)"; "Grey is empty until a source gives it".
- Now: the catalog defines a grey band for wastage and leaves it empty. Agent E2's suggested questions have no "underused" situation for Cluster Capacity, so a cluster idling at low consumption gets the "good" questions ("How many more VMs can this cluster take?"), not the cost questions ("Why is this cluster so idle?", "Can I free hosts from it?").
- Question: below which Cluster Consumption (%), 95th percentile of the last 24 hours, is a production cluster underused? Does it differ by class of service?
- Answer:

### Q-E2-257 · Memory tiering · NVMe consumed as saturation, and the signal that replaces compression and swap

- Files: [Memory tiering](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/memory-tiering.md), section Misconceptions; [Is memory tiering slowing the host?](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/decision-tree/is-memory-tiering-slowing-host.md), section Misconceptions.
- Search strings: "it replaces compression and swap as the saturation signal"; "NVMe holds cold pages: saturation, not contention".
- Now: memory-tiering says NVMe consumed "holds cold pages: it is saturation, memory spilled beyond DRAM, not contention. On a tiered host it replaces compression and swap as the saturation signal; the performance signals are active memory against DRAM and NVMe reads." The decision tree says the same in one line.
- Source: none. Found in the audit of 2026-11-19 as an inference. vSphere 9.1 documentation (p. 1847): NVMe write is cold pages moved into the NVMe tier; NVMe read is pages fetched back when they become active. No vendor text calls NVMe consumed saturation or a replacement for compression and swap.
- Question: keep the SP5 reading?
  - A. Keep both lines.
  - B. Keep "NVMe consumed is saturation, not contention"; drop "it replaces compression and swap as the saturation signal".
  - C. Remove both.
- Recommended: B. The first half follows from the vendor text (pages on NVMe are cold until fetched, so holding them costs no wait) and from the SP5 split of contention and consumption. The second half overreaches: compression and swap still run on a tiered host (memory-tiering, section Interactions).
- Answer:

### Q-E2-246 · Storage > Adapter Highest latency · Plain or command-weighted mean of read and write

- Moved to Future release by the author, 2026-11-16. Impact: 0072 is deferred (status `deferred`), key unchanged; its theory half 0406 keeps running (A does not depend on the weighting). The three files keep their lines until this is answered.

- Files: [Storage adapter and path](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/metrics/host/adapter-and-path.md), [VM disk latency](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/metrics/virtual-motherboard/disk-latency.md); question [0072](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-025-vcenter-adapter-highest-latency.md).
- Now: adapter-and-path says Highest latency averages read and write per adapter first; disk-latency says a total latency is a command-weighted average, "not (read latency + write latency) / 2". If the adapter counter is command-weighted, options A, C and E of 0072 flip.
- Source to check: vSphere Web Services API 9.1, storage adapter counters (`storageAdapter.maxTotalLatency`); a lab export with unequal read and write rates settles it.
- Research (2026-11-16): the vSphere Web Services API 9.1 (and 9.0, 8.0) defines `storageAdapter.maxTotalLatency`, label Highest latency, only as "Highest latency value across all storage adapters used by the host" (statistics level 3, rollup latest, host aggregate). No vendor text says how one adapter combines read and write. The adapter group has no per-adapter total latency counter; the disk group defines total latency as kernel plus device latency per command. The author's own screenshot note shows the value below the read latency, which fits both readings. The files disagree: adapter-and-path says averaged per adapter, disk-latency (a different counter) says command-weighted, datastore says "a normalized average".
- Question: which is it for the adapter's Highest latency?
  - A. Plain mean of read and write latency per adapter.
  - B. Weighted by commands.
  - C. Not documented: all three files say "blends read and write per adapter"; 0072 depends only on its CSV.
- Recommended: C. Write one phrase in the three files (the vendor definition, then "blends read and write per adapter; the weights are not documented"). Rewrite 0072 A, C and E so that they hold under both readings (read and write command counts about equal in its CSV, or the options read the CSV numbers only); key unchanged. A lab check (90/10 and 50/50 read/write mix, compare with both formulas) settles it later: Future release.
- Answer:

### Q-E2-248 · Network > Port group drops · Option A of 0345 and the drop formula

- Moved to Future release by the author, 2026-11-16. Impact: 0345 is deferred (status `deferred`), key unchanged; packets-dropped.md is unchanged, with no denominator stated.

- Files: [Distributed switch packets dropped](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/network/metrics/distributed-switch/packets-dropped.md); question [0345](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-107-port-group-drops-received-or-transmitted.md).
- Now: the knowledge base does not define the VCF Operations port group drop percentage (dropped / packets, or dropped / (dropped + delivered)). A first reviewer read option A of 0345 as false; an independent blind checker read it as true (the key). The audit reworded A and the stem ("of which ... were dropped") so A is true as keyed; the disagreement is recorded here as the safety rule asks.
- Research (2026-11-16): VCF Operations 9.1 TechDocs (updated 2026-11-12), Distributed Virtual Port Group Metrics and VMware Distributed Virtual Switch Metrics: one percentage metric, Percentage of Dropped Packets (`network|port_statistics|dropped_pkts_pct`, "Percentage of dropped packets"), no split by direction and no denominator; the rates Egress and Ingress Dropped Packets per second (`dropped_tx_pkts`, `dropped_rx_pkts`), Total Dropped Packets per second, and Total Ingress and Egress Packets per second (`rx_pkts`, `tx_pkts`). The vSphere API has no percentage counter. Host and VM `net|droppedPct` are also undefined. So the vendor gives no formula, and the question's 0.5% is plain arithmetic on its own numbers (0.19 of 38.0 million).
- Source to check: VCF Operations 9.1 metric definitions, port group network metrics.
- Question: confirm the key of 0345 (A) as now worded, and add a formula?
- Recommended: confirm A (it uses no vendor metric); add no formula. Add the vendor metric names to the file, say the denominator is not documented, and say a per-direction share is computed from the rate metrics (`dropped_tx_pkts` over `tx_pkts`), not a vendor metric. A lab check (compare `dropped_pkts_pct` with dropped / (rx + tx) and dropped / (rx + tx + dropped)) can come later.
- Answer:

### Q-E2-244 · Cluster > HA admission control · Three vendor facts for the percentage policy

- Moved to Future release by the author, 2026-11-16 (unsure of the 32 MHz default; minor). Impact: admission-control-and-cluster-state is unchanged, with no 32 MHz or 0 MB default; 0330 stays deferred (status `deferred`), key unchanged. The line "A VM with no reservation passes CPU and memory admission control" stays until this is answered.

- Files: [Admission control and cluster state](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/concepts/admission-control-and-cluster-state.md); question [0330](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-100-ha-failover-percentage-uneven-hosts.md) (deferred until answered).
- Now: the file has none of: the 32 MHz CPU (0 MB memory) default that a powered-on VM without a reservation counts in the percentage policy; the Insufficient Failover Resources warning when a manual percentage is below the share of the largest hosts; the power-on test against the configured percentage. Its line "A VM with no reservation passes CPU and memory admission control" leads a reader away from the key of 0330.
- Research (2026-11-16): confirmed in the vSphere 9.1 PDF, p. 1971: a powered-on VM with no reservation counts 32 MHz CPU (`das.vmcpuminmhz`) and 0 MB memory; admission control disallows the operation when the Current CPU or Memory Failover Capacity is below the Configured Failover Capacity (step 4). Not confirmed: the Insufficient Failover Resources warning for a manual percentage below the share of the N largest hosts. No vSphere 9.1 PDF page, no TechDocs 8.0 or 9.0 page has it. The vendor fault is named "Insufficient Resources to Satisfy Configured Failover Level for HA" (p. 1949); Broadcom KB 424373 describes "Insufficient configured resources to satisfy the desired vSphere HA failover level" for the opposite case (percentage above current capacity); a 2018 post by Duncan Epping (not official) covers one host's share, not N hosts.
- Source to check: vSphere 9.1 documentation, vSphere Availability, Cluster Resources Percentage Admission Control, Computing the Current Available Capacity (project/sources/vmware-vsphere-9-1.pdf, p. 1971).
- Question: add the two confirmed facts, and rewrite 0330 without the warning half?
  - A. Yes: add the 32 MHz / 0 MB default and the power-on test against the configured percentage; 0330 asks only the power-on result (the warning options go).
  - B. No: retire 0330.
- Recommended: A. Both facts are in the vendor text; the warning is not, so no file or key states it.
- Answer:

### Q-E2-245 · VCF Operations > Alerts · Alert-level wait and cancel cycles, criticality, Child and Descendant

- Moved to Future release by the author, 2026-11-16. Impact: 0274, 0275 and 0340 are deferred (status `deferred`); their keys are unchanged and wait for the alert definitions content (plan.md, After 1.0).

- Files: [Alert definitions](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/alert-definitions.md); questions [0274](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-086-alert-wait-cycles-symptom-and-alert-level.md), [0275](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-053-one-alert-warning-and-critical-symptoms.md), [0340](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-102-resource-pool-alert-nested-pool.md).
- Now: the body states the symptom wait and cancel cycles only; it does not state the alert-level Wait Cycle and Cancel Cycle, how they stack on the symptom cycles, Symptom Based criticality (the most critical triggered symptom), or the Child (one level below) and Descendant relationships. The keys of 0274, 0275 and 0340 rest on these vendor facts.
- Source to check: VCF Operations 9.1 TechDocs, Alert Definition Best Practices and Defining Alerts (techdocs.broadcom.com).
- Question: add these facts to the file?
- Recommended: yes; until then the three keys rest on vendor documents cited in their Notes.
- Answer:

### Q-E2-247 · Guest OS > Linux memory · A Linux memory file

- Moved to Future release by the author, 2026-11-16. Impact: no file is written. 0272 stays in the run set as an outside-the-knowledge-base question (design.md 3.5), 0387 stays (its Linux facts are in linux-os-slow), 0079 has no Linux option; keys unchanged.

- Files: none yet (proposed guest-os/memory/linux-memory); [Guest OS sizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/system/guest-os-sizing.md); questions [0272](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-085-linux-oom-kill-from-a-cgroup-limit.md), [0387](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-070-linux-guest-free-memory-low-all-week.md), [0079](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-027-memory-reclaim-from-40-vms.md).
- Now: no knowledge file states Linux available against free memory, the page cache, cgroup v2 memory.max and memory.high, the OOM kill text, that /proc/vmstat swap counters count since boot, the meaning of /proc/pressure/memory, or how VCF Operations derives Guest Needed Memory on Linux. 0272 rests on the Linux kernel documentation (an outside-the-knowledge-base question, design.md 3.5); 0387 C and D rest on PSI and vmstat semantics.
- Question: write a Linux memory file for 1.0 (Claude drafts from kernel.org documentation on your accept), or keep Linux after 1.0 (plan.md, After 1.0)?
- Recommended: a short file now; three running questions lean on it.
- Answer:

### Q-E2-252 · Guest OS sizing · "VM Active shows the limit" for applications that manage their own memory

- Moved to Future release by the author, 2026-11-16. Impact: guest-os-sizing keeps its line for now. 0079 L stays keyed on active.md and sql-server-memory.md (VM Active shows what was touched); a model that reads only the guest-os-sizing line can answer L false. Fixing the line is a one-line change.

- Files: [Guest OS sizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/system/guest-os-sizing.md) (section Applications that manage their own memory), [SQL Server memory](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/memory/sql-server-memory.md), [VM Active](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/virtual-motherboard/active.md); question [0079](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-027-memory-reclaim-from-40-vms.md) (option L).
- Now: guest-os-sizing says VM Active "shows the limit" of an application that manages its own memory; sql-server-memory and active say Active shows what was touched, not the configured limit. 0079 L is keyed on the second reading.
- Question: correct the guest-os-sizing line?
- Recommended: yes, to "Active shows what the application touched, not its configured limit".
- Answer:

### Q-E2-254 · Overhead · vSAN as overhead (after 1.0)

- Moved to Future release by the author, 2026-11-16 (from Q-E2-250). Impact: 0017 no longer tests vSAN (E and K replaced).
- Files: [Overhead](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/architecture/overhead.md) (vSAN processes, FTT policy, the Misconceptions line on FTT).
- Now: the file counts vSAN processes as overhead and the FTT copy as not overhead. Other questions lean on vSAN too and still run: 0390 (vSAN host Consumed in maintenance mode), 0056 (host Consumed with no VMs), 0080 (datastores running out of space: four options on vSAN space), 0215, 0217, 0296, 0409, 0069. They are not changed: Q-E2-250 named 0017 only.
- Question: when vSAN content is written, check the overhead lines against it, and decide for the questions above whether they move to after 1.0 too (0390 and 0080 are the most vSAN-keyed).
- Recommended: move 0390 and 0080 to after 1.0 if vSAN is out of 1.0 as a whole; keep the others, where vSAN is the setting and not the fact tested.
- Answer:

### Q-E2-255 · Object model · Object relationships.json against objects.yaml (after 1.0)

- Files: [Object relationships.json](https://github.com/e1-rahabok/agent-e2/blob/main/project/sources/Object%20relationships.json); [objects.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/objects.yaml); [Object relationships](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/architecture/object-relationships.md). Search strings: `stack_layer`, `plane`, `CONSUMES_FROM`.
- Now: the JSON has 28 object types and 54 relationships; objects.yaml has 12 types and 18 relations. 14 JSON types are new (VirtualDisk, HostBusAdapter, StorageDevice, StorageArray, VirtualNIC, StandardPortGroup, UplinkPortGroup, HostVirtualSwitch, VMkernelNIC, PhysicalNIC, TopOfRackSwitch, GuestOS, Container, VirtualMachineTemplate). It conflicts with the repository in four places: (1) layers: Orchestration, VirtualHardware, Hypervisor, Physical, Container, GuestOS against guest-os, virtual-motherboard, hypervisor, physical; Datastore sits in the hypervisor layer and HostSystem is not in the physical layer; (2) `plane` (ControlPlane, DataPlane) is not a repository term; (3) `Container` is Linux and container scope, After 1.0; (4) edge verbs CONSUMES_FROM, ATTACHED_TO, CONNECTED_TO against contains, resource-parent, runs-on, mounts, stores-files-on, connects-to; VM CONSUMES_FROM ResourcePool runs against resource-parent, and VM CONSUMES_FROM Datastore repeats VM, VirtualDisk, Datastore.
- Question: how does the JSON enter objects.yaml?
  - A. Map the JSON to the repository layers and verbs; drop `plane`, `Container` and the repeated VM to Datastore edge; add the other 13 types.
  - B. Adopt the JSON layers and verbs and change the repository vocabulary (tags.yaml, glossary, the layer rule).
  - C. Keep it as a source only until the live VCF Operations integration needs a graph.
- Recommended: A. The layer rule (a VM is a virtual motherboard; the Guest OS is a separate layer) decides a metric's home, so the repository names stay. Do it in one change set after 1.0, with `kb`, `role`, `supplies` and `charts` for each new type and the new types in tags.yaml.
- Answer:

### Q-E2-241 · CPU > VM Demand · Demand under a limit (lab check)

- Files: [VM CPU Demand](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/demand.md) (section Not unmet demand, two misconceptions).
- Now: the file's lab test shows VM CPU Demand equal to Usage under a limit, so Demand is not unmet demand. The vSphere Web Services API 9.1 defines `cpu.demand` as the CPU a VM would use with no CPU contention or CPU limit, which says the opposite.
- Question: repeat the limit test on a 9.1 host (a VM with a CPU limit below its load; read Demand, Usage, Ready, Max Limited)?
  - A. Demand stays at Usage: keep the text and record a correction against the API definition.
  - B. Demand rises above Usage: follow the API and rewrite the section and the misconceptions.
- Recommended: run the test; until then the text stays with a review note.
- Answer:

### Q-E2-242 · Storage > esxtop · QAVG above KAVG

- Files: [ESXi storage latency stack](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/concepts/esxi-storage-latency-stack.md) (section Counters, one misconception).
- Now: "QAVG can exceed KAVG: QAVG covers VM IO and kernel IO; KAVG covers VM IO only", and the misconception "QAVG cannot exceed KAVG" → QAVG includes kernel IO. The ESXi disk queue note in project/sources gives KAVG = QAVG + VMkernel processing, so QAVG would never exceed KAVG.
- Question:
  - A. Keep the line: you have seen QAVG above KAVG in esxtop.
  - B. Follow the source note: KAVG includes QAVG; drop the misconception.
- Recommended: A only with field evidence, else B.
- Answer:

### Q-E2-222 · SP5 > Availability · Does a host in maintenance mode lower availability?

- Files: [IaaS SLAs](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/sla-metrics.md) (Availability SLA); [Cluster availability](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/metrics/availability.md).
- Now:
  - sla-metrics: the maintenance window is always excluded (your Q-E2-098 answer). One host in maintenance: Operational Availability 100%.
  - Cluster availability: the ESXi state score takes 25% off a host in maintenance mode.
- Question: which availability is the cluster score?
  - A. Actual Availability. Maintenance counts.
  - B. Operational Availability. Maintenance does not count; the 25% row goes.
  - C. A third score. The file gives it its own name.
- Recommended: C. The state score measures operations maturity (a host left in maintenance too long is a finding); the SLA measures the service. Two purposes, two names.
- Answer:

### Q-E2-226 · SP5 > Availability · Usable hosts during maintenance: 8 or 9 of 10?

- Files: [IaaS SLAs](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/sla-metrics.md) (the 10-host example); [Supply](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/supply.md) (Total vs usable after host loss).
- Search: "Example on a 10-host cluster with 1 HA host (usable 9 hosts)".
- Now:
  - 10 hosts, 1 HA host, 1 host in maintenance.
  - supply: usable 8. HA admission control leaves a host in maintenance out and keeps its reserve among the other 9 (vSphere 9.1).
  - sla-metrics: Operational Availability divides by usable 9.
- Question: which divisor does Operational Availability use?
  - A. Planned usable (9), whatever the maintenance. Availability measures the planned service; usable capacity is what is safe now.
  - B. Usable during the event (8). Maintenance never lowers availability.
  - C. Your design lets the HA host cover maintenance. supply then shows two views: protected (8) and unprotected (9).
- Recommended: A.
- Answer:

### Q-E2-235 · Sizing > VM CPU sizing note · Levels and units of the decision matrix

- Files: [VM CPU Sizing Best Practices](https://github.com/e1-rahabok/agent-e2/blob/main/project/sources/vm_cpu_sizing_best_practices.md) (Sizing Decision Matrix, Post-Resize Verification); [rightsizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/rightsizing.md) (Before vs after).
- Now: no number from the note is in the knowledge base. rightsizing has the verification step only.
- Questions:
  1. Queue unit. The matrix reads a total (10, 11-25, above 25 threads). The verification table reads per vCPU (2-3, above 10). Which one?
  2. Ready above 5% and Co-stop above 3% keep the VM at 10 vCPUs. A: use the KPI levels instead (yellow at 2% Ready, 1% Co-stop, 20-second peak). B: a separate sizing rule.
  3. N%L above 90% healthy, below 85% a red flag. Give a source, or drop it.
  4. 14 or 15 vCPUs on a 16-core node, to leave room for hypervisor interrupts. Field experience or a document?
- Recommended: 1 per vCPU (VCF Operations shows the queue per vCPU, Q-E2-217). 2 A (one place per number). 3 drop. 4 yours.
- Answer:

### Q-E2-216 · CPU > NUMA > Virtual NUMA · Topology rebuild and `numa.autosize.once` (lab checks)

- Files: [Virtual NUMA](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/concepts/virtual-numa.md) (Topology initialization, Misconceptions); [NUMA sizing guide](https://github.com/e1-rahabok/agent-e2/blob/main/project/sources/vmware_vsphere_numa_architecture_and_sizing_guide.md) (section 4).
- Now: the guide says ESXi rebuilds the vNUMA topology at every power cycle. vSphere 9.1 says it stays until the vCPU count changes, and lists `numa.autosize.once` (default TRUE). Both stay unverified in the file.
- Lab checks, text output only:
  - (a) `numa.allowHotadd`: hardware 20 or later, 12+ vCPUs, CPU Hot Add on. Power on without the option, then with it. Each time paste `lscpu | grep -i numa` (Linux) or `coreinfo -n` (Windows), and `grep -i numa <vm>.vmx` on the host.
  - (b) Persistence: a VM wider than one NUMA node (24 vCPU). Paste the guest NUMA output and the vmx lines. Power off, vMotion to a host with another node size, power on, paste again.
  - (c) `numa.autosize.once`: is it in the vmx after the first power-on? Add it as FALSE, repeat (b).
- Answer:

### Q-E2-124 · Storage > Unmap · Unmap counters per datastore

- Files: [ESXi Datastore metrics](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/metrics/host/datastore.md) (section Unmap); [esxtop storage](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/tools/esxtop/storage.md).
- Search: "but you can’t aggregate them per datastore".
- Now: unmap counters live on the ESXi host, one instance per datastore. No datastore total across hosts. Counter keys only in a review note.
- Proposed from vendor sources (Claude applies on your accept):
  - Keys `datastore.unmapIOs.summation` (count) and `datastore.unmapSize.summation` (MB), per host and datastore. Not in the 9.1 API pages; seen in live vCenter 7 and 8 lists.
  - Datastore total: sum the hosts that mount it. Complete, since each unmap comes from one host.
  - Per 20 seconds. A VCF Operations 5-minute point is the mean of 15: MB in 5 minutes = value × 15.
  - The vsish counters reset at reboot and when no VM on the host uses the datastore (Broadcom KB 374191).
- For you, in VCF Operations 9.1: does the Datastore object have an unmap metric? What are the Host System metric keys?
- Answer:

### Q-E2-129 · VCF Operations 9.1 · Real-time metrics API for scripts

- Files: [Real-time metrics](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/features/real-time-metrics.md).
- Now: "data is queried with PromQL"; no API section.
- Proposed from the Broadcom API reference (https://developer.broadcom.com/xapis/realtime-metrics-api/latest/; Claude applies on your accept):
  - Prometheus-style endpoints: GET `/api/v1/query`, `/api/v1/query_range`, `/api/v1/metadata`; PUT `/api/v1/vcenters/{vcId}/metrics_config`.
  - `sourceId` (vCenter UUID) required from API 9.1.1. Paged responses.
  - Auth: OpsToken from `/suite-api/api/auth/token/acquire`, exchanged for a JWT with the VCF_VODAP service key.
- For you, one call in your lab: which host answers the API (VCF Operations or the real-time component)? Does the esxtop feature return 2-second data through it?
- Answer:

### Q-E2-149 · Term map · Wrong terms users write

- Files: [user-terms.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/user-terms.yaml).
- Now: rows written from the knowledge base; none from real tickets.
- Question: which wrong terms do admins write in tickets and chats, and what do they mean? Example: "steal time" means VM CPU Ready and Co-stop. A list of term → meaning is enough.
- Ready to add on your accept, from the knowledge base: "latency" with no layer; VM network latency; "ESXi Ready"; "Ready 5%" or "2000 ms"; "VM consumed memory high"; thin provisioning; DRS Score; esxtop load average; SIOC shares (ignored from VCF 9.0); "memory pressure".
- Answer:

### Q-E2-150 · URL questions · Public pages with known errors

- Files: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md) (section 3.4).
- Now: no URL question in the run set.
- Candidates, still published with the error (fetched 2026-11-14):
  - Broadcom KB 419238, Troubleshooting VM performance: %RDY ≥ 10 with no per-vCPU reading; %DRPTX above 0 read as high utilization.
  - Broadcom KB 386180, CPU Ready with high I/O: fixed Ready and Co-stop levels; its capture runs 112.5 minutes, not 15.
  - TechDocs 9.1, Solutions for Memory Performance Problems: "94% or greater" usage and "6% or less" free read as pressure.
  - TechDocs 9.1, Solutions for Poor Network Performance: dropped packets read as a network bottleneck.
  - Broadcom KB 326296: strict co-scheduling; %CSTP above 3 with no per-vCPU reading.
  - Broadcom KB 415396: "focus on active memory".
- Question: accept these, drop some, or add pages you know are wrong?
- Answer:
