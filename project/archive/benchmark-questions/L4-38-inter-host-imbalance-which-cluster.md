# Inter-host imbalance across clusters

## Prompt
The attached screenshot is a VCF Operations list of clusters with their Cluster Inter-Host Imbalance values.

- Cluster P shows 200.
- Cluster Q shows 1.
- Cluster R shows 0.
- Cluster S shows -3.

Which statements are correct? Choose all that apply.

- A. Cluster P has 2 high hosts and no low host: DRS has nowhere to move VMs inside the cluster; moving VMs to another cluster may be required.
- B. Cluster P has 200% imbalance, twice as bad as a cluster at 100%, but still balanced.
- C. Cluster S has 3 low hosts and no high host: wastage, not a performance risk.
- D. Cluster R has every host idle.

## Input to supply
- Tool: VCF Operations 9.1, a list view of clusters with the vCommunity Cluster Inter-Host Imbalance metric (or a super metric that implements it), with a color per value.
- Condition for the key: four clusters, labeled P, Q, R and S in the question, show 200, 1, 0 and -3. Rename them in the image if needed, and record the mapping in the Notes.
- Save as `benchmark/questions/78/vcf-operations-cluster-imbalance-list.png`.

## Likely wrong answer
B: reading the value as a percentage; D: reading 0 as idle.

## Expected key points
- Answer: A, C.
- Imbalance = high hosts / low hosts. High: Core Utilization above 90% and Thread Utilization above 80%. Low: below 50% and below 40%.
- Red: 1 or more high hosts and no low host, shown as 100, 200, 300: so 200 is 2 high hosts with no low host.
- Negative whole numbers are grey: low hosts and no high host, wastage. -3 is 3 low hosts.
- Q at 1 (orange): high hosts equal low hosts. R at 0 (green): no high host while hosts are used; 0 does not mean idle.

## Notes
- Retired 2026-11-12 (question set 1.0): vCommunity metric inter-host imbalance (fairness).
- Previous id: question-0078 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0078"
title: "Inter-host imbalance across clusters"
product: [vcf-operations]
technology: [system, cpu]
task: decide-capacity
level: 400
answer_type: deterministic
input: [screenshot]
knowledge:
  - vsphere/technology/cpu/metrics/cluster/inter-host-imbalance
attachments:
  - 0078/vcf-operations-cluster-imbalance-list.png
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
answer: [A, C]
misconception: [B, D]
status: retired
```
