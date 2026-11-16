# A counter missing from the history

## Prompt
- vCenter 9.1, statistics level 1 for every interval (the default).
- Three days ago, VM sql-07 (8 vCPUs) was slow for an hour. During the incident an engineer opened the vSphere Client advanced chart, Real-time: Co-stop was high on several vCPUs.
- Today you open the same VM's chart for the past week. Co-stop is not offered as a counter, and CPU Ready shows one line for the whole VM.

Which statements are correct?

- A. The Real-time chart offered Co-stop per vCPU because it reads the host's samples, whatever the level.
- B. Raising the 1 Week interval to level 3 now brings back the Co-stop history of the incident.
- C. The past-week chart offers no CPU Demand for sql-07 either: Demand is not kept at level 1.
- D. Raising every interval to level 4 and leaving it there is the safe fix: it costs only database space.
- E. The newest hour of the past-week chart can still be empty: its points arrive up to an hour late.
- F. With Ready summed over the vCPUs, the VM's Ready history is of no use at all for this incident.

## Likely wrong answer
B: expecting a higher level to fill in the past. Or D: level 4 everywhere, permanently.

## Expected key points
- Answer: A, C, E.
- A is correct: statistics levels decide which counters vCenter stores for the history intervals. The Real-time chart of a powered-on VM reads the host's own samples for the last hour and offers every counter the host collects, whatever the level.
- B is wrong: the misconception. A level applies from the moment it is set; it does not rebuild history that was never stored.
- C is correct: CPU Demand (cpu.demand) is a level 2 counter in the vSphere API 9.1; at level 1 it has a Real-time chart and no history.
- D is wrong: the wrong action. Levels 3 and 4 add per-instance counters and raise vCenter load sharply; the vpxd process can grow until it runs out of memory. Raise a level for a short time, after a problem appears.
- E is correct: a point appears only after its interval closes and the rollup runs; 1 Week data can be up to 1 hour behind (30 minutes for the 1 Week interval plus 30 for 1 Day), and the chart is empty for that time.
- F is wrong: the over-correction. The sum still shows how long the vCPUs waited in total; divided by 8 it is the mean per vCPU, and a low sum rules out a long wait on any vCPU.

## Notes
- Synthetic, 2026-11-12.
- Changed in the 2026-11-15 audit: C (level 1 Ready is the sum of the vCPUs) and E (the sum hides which vCPU waited), held by 0105 and 0369, replaced in place by two true facts of vcenter-statistics no other question tests: CPU Demand has no level 1 history (C) and the rollup delay of the 1 Week chart (E). Key unchanged: A, C, E.
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
source_path: "Synthetic, 2026-11-12"
answer: [A, C, E]
misconception: [B, D]
misconception_type: [rollup-and-interval, tool-confusion]
status: draft
```
