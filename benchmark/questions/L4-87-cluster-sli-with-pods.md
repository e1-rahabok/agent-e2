# Work out the Cluster SLI

## Prompt
The attached table lists, per running VM and per pod of one cluster, Performance|Number of KPIs Breached for the last cycle. The screenshot is the VCF Operations summary of that cluster, with the number of running VMs and pods.

- 112 running VMs and 8 pods.
- 10 VMs breach 1 KPI each; 1 VM breaches all 4.
- 2 pods breach 2 KPIs each.

What is the Cluster SLI?

- A. 96.25%
- B. 89.17%
- C. 96.88%
- D. 85.00%

## Input to supply
- Table: VCF Operations 9.1 export, one row per running VM and pod of one cluster: name, type (VM or pod), Performance|Number of KPIs Breached.
- Screenshot: VCF Operations cluster summary showing Summary|Number of Running VMs and Summary|Number of Pods.
- Condition for the key: 112 running VMs and 8 pods; breaches exactly as in the prompt (14 for VMs, 4 for pods). The author may build the table to match.
- Save as `benchmark/questions/87/sli-breaches-per-object.xlsx` and `benchmark/questions/87/vcf-operations-cluster-summary.png`.

## Likely wrong answer
B: counting objects that breach instead of breaches.

## Expected key points
- Answer: A.
- Cluster SLI (%) = 100 - (sum of KPIs breached over VMs and pods) / (running VMs + pods) × 100 / 4.
- Breaches = 14 + 4 = 18; objects = 112 + 8 = 120; 100 - (18 / 120 × 100 / 4) = 100 - 3.75 = 96.25%.
- B counts the 13 objects with a breach as a share of 120: the SLI counts breaches, so 1 VM with 4 breaches equals 4 VMs with 1.
- C leaves out the pods: 100 - (14 / 112 × 25). D forgets the division by 4.

## Notes
- Previous id: question-0087 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "87"
title: "Work out the Cluster SLI"
product: [vcf-operations, kubernetes]
technology: [system]
task: read-metric
level: 400
answer_type: deterministic
input: [table, screenshot]
knowledge:
  - vsphere/object-types/cluster/metrics/cluster-sla-sli
attachments:
  - 87/sli-breaches-per-object.xlsx
  - 87/vcf-operations-cluster-summary.png
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
answer: [A]
trap: [B]
status: awaiting-input
```
