# Cluster DRS Score high, one VM low

## Prompt
- Users of the VM pay-api-03 report slow responses this morning. The application owner sends the cluster score from PowerCLI and says: "The cluster score is green, so vSphere is fine. The problem must be inside the VM."

```text
PS> (Get-Cluster cl-prod-02).ExtensionData.Summary.DrsScore
94
```

- You export [the VM DRS Score list of the cluster](0433/vcenter-cluster-vm-drs-scores.csv) (Monitor > vSphere DRS > VM DRS Score) and [the vCenter CPU chart of pay-api-03](0433/vcenter-vm-cpu-realtime.csv), Real-time, for the last 30 minutes.

Which statements are correct?

- A. A green cluster score means no VM in the cluster is short of resources.
- B. In the VM DRS Score export, this VM is far below the cluster score.
- C. The VM's CPU export shows its vCPUs ready but not running for under 1% of the time.
- D. The VM's CPU export shows its vCPUs ready but not running for over 5% of the time, on average.
- E. A figure that one slow VM cannot move tells nothing about the health of the cluster as a whole.
- F. Ask the owner to tune the Guest OS first, since the cluster score clears vSphere.
- G. Every VM with a low score in the VM DRS Score export waits for physical CPU.
- H. A Cluster DRS Score of 85% and one of 95% show a real difference in performance.

## Likely wrong answer
A: the cluster score read as the state of every VM, so the cause is put inside the Guest OS, and F, the action that follows from it.

## Expected key points
- Answer: B, D.
- A is wrong: the misconception. The Cluster DRS Score is a weighted average of the VM scores; it does not bound any single VM, and one VM barely moves it.
- B is correct: reading. The cluster score is 90 or more; pay-api-03 has the lowest `DRS Score` in the list, below 50%.
- C is wrong: reading. `Readiness for pay-api-03` is above 5 in most rows and never below 2.
- D is correct: reading. Readiness is Ready per vCPU as a percentage of the sample; `Readiness for pay-api-03` averages above 5 over the rows, so the vCPUs spent that share of the time ready to run with no physical CPU free (`Max limited for pay-api-03` is 0: no limit).
- E is wrong: the over-correction. Since vSphere 7.0 the Cluster DRS Score replaces the load-balance metric and indicates cluster health; it only cannot speak for a single VM.
- F is wrong: the wrong action. The VM's Ready shows it waits for physical CPU, which no Guest OS tuning removes.
- G is wrong: reading and mechanism. The VM DRS Score is execution efficiency over CPU, memory, network and storage, not CPU contention alone: rpt-batch-09 also scores low, with `CPU Readiness` below 1% and swapped and ballooned memory.
- H is wrong: a cluster score of 85% and one of 95% both sit in the range that indicates no performance impact; the range matters, not the exact value.

## Notes
- Practical half of 0232 (pair: design.md, section 3.9).
- 2026-11-15 audit: old G (a must-run rule keeps the VM on a busy host) dropped, as 0065 and 0438 keep the DRS-blocker fact; H added (85% vs 95%, false; drs-migration-levels Misconceptions); E now says "health", as the knowledge base says the score indicates cluster health, not load balance (the old wording read as true). Letters: A-F unchanged; G dropped; H -> G; H new.
- Synthetic, 2026-11-14, for the question pairing plan (project/question-pairing-2026-11-14.md, item C25). Counts only after author approval.
- Converted to exports 2026-11-15 (project/practical-questions-as-exports-2026-11-15.md): cluster score as PowerCLI text, VM DRS Score list and VM CPU chart as CSV. B, C and D reworded from list, chart and screen to the exports; truth unchanged. A false option (now G) added: a second low-score VM with low CPU Readiness, the distractor of the export plan. The VM DRS Score list CSV layout is assumed (not in the export templates yet).

## Metadata
```yaml
id: "0433"
title: "Cluster DRS Score high, one VM low"
product: [vsphere]
technology: [system, cpu]
task: troubleshoot
level: 300
answer_type: deterministic
input: [table]
object: [cluster, vm]
tool: [vcenter]
knowledge:
  - vsphere/object-types/cluster/configuration/drs-migration-levels
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/object-types/cluster/cluster-health-check
  - vsphere/object-types/vm/vm-performance
knowledge_main: vsphere/object-types/cluster/configuration/drs-migration-levels
attachments:
  - 0433/vcenter-cluster-vm-drs-scores.csv
  - 0433/vcenter-vm-cpu-realtime.csv
origin: synthetic
source_path: "Synthetic, 2026-11-14, pairing plan item C25"
answer: [B, D]
misconception: [A, F]
misconception_type: [average-hides-worst]
pair: "0232"
status: draft
```
