# Cluster Risk fell after deploying VMs

## Prompt
- A cluster's Cluster Risk (%) was 67.9, driven by one busy host.
- The team deployed ten idle 4-vCPU VMs. The CPU overcommit ratio of the hosts rose from 0.5 to about 1.1.
- Cluster Risk is now 64.5.
- The capacity manager says the deployment lowered the risk.

Is the manager right? Explain.

## Likely wrong answer
"Yes: the KPI went down, so the risk is lower."

## Expected key points
- No: the risk did not fall. More vCPUs per core cannot lower risk.
- Known limitation of the weighted average: the overcommit row left its Excluded green and entered yellow with a weight of about 2. Its score is better than the rows already driving the KPI, so it pulls the average up and Cluster Risk down.
- This happens only when Cluster Risk is already high; with green sub-metrics a worse row always raises it.
- Read the sub-metrics before acting on a falling Cluster Risk; a cluster just above orange (50) can drop to yellow after VMs are deployed.

## Notes
- Retired 2026-11-12 (question set 1.0): vCommunity metric Cluster Risk (fairness).
- Previous id: question-0064 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0064"
title: "Cluster Risk fell after deploying VMs"
product: [vcf-operations]
technology: [system]
task: decide-capacity
level: 400
answer_type: judged
input: [text]
knowledge:
  - vsphere/object-types/cluster/models/cluster-risk
  - sp5-framework/performance/performance-kpi-design
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
status: retired
```
