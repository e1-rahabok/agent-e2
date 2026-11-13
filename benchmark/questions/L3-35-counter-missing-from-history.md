# A counter missing from the history

## Prompt
- vCenter 9.1, statistics level 1 for every interval (the default).
- Three days ago, VM sql-07 (8 vCPUs) was slow for an hour. During the incident an engineer opened the vSphere Client advanced chart, Real-time: Co-stop was high on several vCPUs.
- Today you open the same VM's chart for the past week. Co-stop is not offered as a counter, and CPU Ready shows one line for the whole VM.

Which statements are correct?

- A. At level 1 vCenter keeps no Co-stop history and no per-vCPU Ready; the Real-time chart showed them because real-time data does not depend on the statistics level.
- B. Raising the 1 Week interval to level 3 now brings back the Co-stop history of the incident.
- C. The incident is lost from vCenter's history because the 1 Week chart averages 30 minutes; at level 1 the Co-stop values are kept but hidden.
- D. Raising every interval to level 4 and leaving it there is the safe fix: it costs only database space.
- E. At level 1 the VM's CPU Ready history is one value for the whole VM, the sum of its 8 vCPUs, so one vCPU that waited a lot cannot be told apart from eight that each waited a little.

## Likely wrong answer
B: expecting a higher level to fill in the past. Or D: level 4 everywhere, permanently.

## Expected key points
- Answer: A, E.
- A: statistics levels decide which counters vCenter stores for the history intervals. At level 1 a VM keeps CPU Ready (VM total), Highest disk latency, balloon and swap rates, but not Co-stop or per-vCPU counters. Real-time data comes from the host for the last hour, whatever the level.
- B is wrong: a level applies from the moment it is set; it does not rebuild history that was never stored.
- C is wrong: the counter was not collected at all, not stored and hidden.
- D is wrong: levels 3 and 4 add per-instance counters and raise vCenter load sharply; the vpxd process can grow until it runs out of memory. Raise a level for a short time, after a problem appears.
- E: at level 1 Ready is kept for the VM as a whole, summed over its vCPUs; the per-vCPU split is gone, so one vCPU waiting a lot and eight waiting a little give the same value.

## Notes
- Drafted 2026-11-12 for the System slots (question set 1.0, plan M2).
- VM-level CPU Ready is the sum over the vCPUs, not the average: Broadcom KB 387750 (https://knowledge.broadcom.com/external/article/387750).
- Real-time vs historical charts: Broadcom KB 344684, vCenter Server advanced performance charts only display real time counters or some chart metrics are missing entirely (https://knowledge.broadcom.com/external/article/344684).

## Metadata
```yaml
id: "0231"
title: "A counter missing from the history"
product: [vsphere]
technology: [system, cpu]
task: read-metric
level: 300
answer_type: deterministic
input: [text]
object: [vm]
tool: [vcenter]
knowledge:
  - vsphere/tools/vsphere-client/vcenter-statistics
  - vsphere/technology/cpu/metrics/virtual-motherboard/co-stop
knowledge_main: vsphere/tools/vsphere-client/vcenter-statistics
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12 for the System slots (question set 1.0)"
answer: [A, E]
misconception: [B, D]
misconception_type: [rollup-and-interval, tool-confusion]
status: draft
```
