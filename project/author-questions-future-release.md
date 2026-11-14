# Questions for the author: future release

To-do items for a release after 1.0. Not blocking release 1.0. Rules for answering: [author-questions.md](author-questions.md). Release 1.0 questions: [author-questions-release-1.0.md](author-questions-release-1.0.md).

## Open

### Q166 · ARCHITECTURE.md, section Troubleshooting questions · Code evaluates flow branches

- Files: [harness/flows.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/flows.py), [project/design-thresholds.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/design-thresholds.md).
- What the knowledge base says now: the flow tool serves step text; the model compares values and picks the branch.
- Question: (a) executable steps: the model extracts values into a case state, code compares them with catalog thresholds and picks the branch, the model explains; (b) keep as is.
- Proposed answer: (a), for 1.0, starting with the VM slow flow.
- Answer: Yes, (a) for 1.0.
- Applied 2026-11-12: Recorded in project/plan.md, M1 open work: executable flow steps (the model extracts values into a case state, code compares them with catalog thresholds and picks the branch), starting with the VM slow flow.

### Q128 · Glossary · Proposed terms from Capacity Management

- Files: [Terminology](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/glossary.md) (section Capacity); [Demand](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/demand.md).
- Search: "Stop Provisioning (Yes/No)"
- Question: three glossary proposals: (a) "Closed cluster" (also called stop provisioning); (b) pair "Demand (capacity) vs ESXi CPU Demand"; (c) pair "Idle vs oversized vs unused VM". Keep, rename or drop?
- Written as now: glossary entry **Closed cluster** ("A cluster that accepts no new VM and no VM upsize, decided from Cluster Consumption (%), Cluster Performance (%) and Cluster Risk (%)"; Also called: Stop provisioning; File: can-cluster-take-more-vms). Entry **Demand (capacity)** with "Not to confuse with ESXi CPU Demand". (c) removed by your glossary edit of 2026-11-11. demand.md still says "Stop Provisioning (yes or no): … decided from Performance (%), Capacity Remaining (%) and Risk (%)".
- Final answer (2026-11-12; (c) settled by your edit; (a), (b) expert call):
  - (a) Rename the entry to **Close for Business**: 1 = closed (no new VM, no VM upsize), 0 = open, decided from Cluster Consumption, Cluster Performance and Cluster Risk. Also called: Closed cluster, Stop provisioning. File: close-for-business, then can-cluster-take-more-vms. Reason: one word per concept, and the pack metric (`vCommunity|Periodic Cluster Check|Close for Business`), the file title and the plan already use it.
  - Fix demand.md: Cluster Consumption replaced Capacity Remaining in the closure ([Q121](project/author-questions-resolved.md#q121--part-1--capacity-model--cluster-closure--logic--non-production-capacity-and-the-orange-case)).
  - (b) Keep, and widen Not to confuse with to CPU Demand (VM and ESXi): VM CPU Demand is the same confusion. A third use exists: VCF Operations names a capacity setting Capacity Buffer (Demand) (cluster-consumption).
  - (c) Settled: you removed the pair. Nothing to do.
  - Change if accepted: glossary (Close for Business entry; Demand entry); demand.md (Stop Provisioning line).
  - For you: nothing.
- Answer: Agree (2026-11-12).
- Applied 2026-11-12: glossary entry Close for Business (Also called: Closed cluster, Stop provisioning; File: close-for-business); Demand (capacity) not to confuse with CPU Demand (VM and ESXi), plus Capacity Buffer (Demand); demand.md Stop Provisioning line reads Cluster Consumption, Performance and Risk. Closed.
