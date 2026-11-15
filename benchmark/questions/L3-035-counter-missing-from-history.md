# A counter missing from the history

## Prompt
- vCenter 9.1, statistics level 1 for every interval (the default).
- Three days ago, VM sql-07 (8 vCPUs) was slow for an hour. During the incident an engineer opened the vSphere Client advanced chart, Real-time: Co-stop was high on several vCPUs.
- Today you open the same VM's chart for the past week. Co-stop is not offered as a counter, and CPU Ready shows one line for the whole VM.

Which statements are correct?

- A. The Real-time chart offered Co-stop per vCPU because it reads the host's 20-second samples, whatever the statistics level.
- B. Raising the 1 Week interval to level 3 now brings back the Co-stop history of the incident.
- C. At level 1 the VM's CPU Ready history is the sum of its 8 vCPUs, not their average.
- D. Raising every interval to level 4 and leaving it there is the safe fix: it costs only database space.
- E. The level 1 Ready history cannot tell one vCPU that waited a lot from eight vCPUs that each waited a little.
- F. With Ready summed over the vCPUs, the VM's Ready history is of no use for this incident.

## Likely wrong answer
B: expecting a higher level to fill in the past. Or D: level 4 everywhere, permanently.

## Expected key points
- Answer: A, C, E.
- A is true: statistics levels decide which counters vCenter stores for the history intervals. The Real-time chart of a powered-on VM reads the host's own samples for the last hour and offers every counter the host collects, whatever the level.
- B is false: the misconception. A level applies from the moment it is set; it does not rebuild history that was never stored.
- C is true: at level 1 Ready is kept for the VM as a whole, summed over its vCPUs in ms.
- D is false: the wrong action. Levels 3 and 4 add per-instance counters and raise vCenter load sharply; the vpxd process can grow until it runs out of memory. Raise a level for a short time, after a problem appears.
- E is true: the per-vCPU split is gone, so one vCPU waiting a lot and eight waiting a little give the same value.
- F is false: the over-correction. The sum still shows how long the vCPUs waited in total; divided by 8 it is the mean per vCPU, and a low sum rules out a long wait on any vCPU.

## Notes
- Drafted 2026-11-12.
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): A no longer states that level 1 keeps no Co-stop history (the fact 0351 tests); C (stored but hidden, the negation of A) and the compound E replaced by single facts; F added as the over-correction. Key changed from A, E to A, C, E.
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
source_path: "Drafted by Claude 2026-11-12"
answer: [A, C, E]
misconception: [B, D]
misconception_type: [rollup-and-interval, tool-confusion]
status: draft
```
