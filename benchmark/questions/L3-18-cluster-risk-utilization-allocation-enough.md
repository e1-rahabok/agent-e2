# Is utilization and allocation enough for cluster risk

## Prompt
Do I need to quantify risk for vSphere Cluster? If yes, what should be the formula? I think it's enough to use utilization and allocation. No?

## Likely wrong answer
Picks one meaning of "risk" without saying so: risk as Time Remaining (days) from a demand projection, the capacity runway of older vRealize Operations material. It never addresses how close the hosts are to contention.

## Expected key points
- Names the ambiguity: "cluster risk" can mean (a) how close the hosts are to contention, (b) capacity runway (Time Remaining against a projection), (c) surviving a host failure. Says which it answers, or answers each.
- Yes, quantify it: Cluster Risk (%) is a leading indicator; Cluster Performance (%) shows contention happening now.
- Utilization and allocation are not enough:
  - it reads the worst ESXi host, not the cluster average: one full host hurts its VMs while the average looks fine;
  - it adds saturation (ballooned, swapped and compressed memory, memory tiering latency), reservation, CPU imbalance and monster VM ratios;
  - monster VMs cause contention despite low utilization, reservation and allocation.
- Formula: each sub-metric scored against its bands; a weighted average where a worse score weighs more; published flipped (100 minus the weighted average), so higher is worse. Green rows such as low utilization are left out while green.
- Risk is a leading indicator: it never closes a cluster on its own.
- Time Remaining is the capacity model's projection: a different question.

## Notes
- Author's prompt to Gemini 3.1 Pro (high effort), 2026-11-10. Gemini answered risk as Time Remaining (days); author: it seems to use an older copy of the vRealize Operations manual or a blog.
- The prompt carries a wrong premise and an ambiguous term: a candidate that names both scores higher. The benchmark is single turn, so asking is scored as naming the meanings.
- Drafted by Claude 2026-11-10 from the knowledge files listed in `knowledge`. Counts only after author approval.

## Metadata
```yaml
id: "0093"
title: "Is utilization and allocation enough for cluster risk"
product: [vsphere, vcf-operations]
technology: [cpu, memory, system]
input: [text]
task: explain-mechanism
knowledge:
  - vsphere/object-types/cluster/models/cluster-risk
  - sp5-framework/capacity/capacity-model
  - vsphere/object-types/cluster/models/close-for-business
attachments: []
origin: synthetic
source_path: "Author's prompt and Gemini 3.1 Pro exchange, 2026-11-10"
answer_type: judged
level: 300
status: draft
```
