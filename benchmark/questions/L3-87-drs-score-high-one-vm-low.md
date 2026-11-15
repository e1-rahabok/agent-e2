# Cluster DRS Score high, one VM low

## Prompt
- Users of one VM report slow responses this morning. The application owner sends [the cluster summary](0433/vcenter-cluster-summary-drs-score.png) and says: "The cluster score is green, so vSphere is fine. The problem must be inside the VM."
- You open [the VM DRS Score list](0433/vcenter-cluster-vm-drs-scores.png) of the cluster and [the CPU chart of that VM](0433/vcenter-vm-cpu-ready-real-time.png).

Which statements are correct?

- A. A green cluster score means no VM in the cluster is short of resources.
- B. The VM DRS Score list shows this VM far below the cluster score.
- C. The CPU chart shows this VM's vCPUs ready but not running for under 1% of the time.
- D. The CPU chart shows the VM's vCPUs, on average, ready to run but not running for more than 5% of the time.
- E. A figure that one slow VM cannot move tells nothing about how well DRS balances the cluster as a whole.
- F. Ask the owner to tune the Guest OS first, since the cluster score clears vSphere.
- G. Something DRS must obey, such as a must-run rule that ties the VM to its host, can keep it on a busy host.

## Input to supply
- Product and version: vSphere 9.1 (vSphere Client), a DRS cluster, fully automated, default migration threshold.
- How to produce it in a lab: a "must run on" VM-Host rule that keeps the test VM and two or three CPU-burner VMs on one host, with their vCPUs together 1.5-2 times that host's physical threads; the other VMs of the cluster stay light. Run the burners and the test VM's load for 20-30 minutes.
- Screen 1: the cluster > Summary, the vSphere DRS card with the Cluster DRS Score. Save as `0433/vcenter-cluster-summary-drs-score.png`.
- Screen 2: the cluster > Monitor > vSphere DRS > VM DRS Score, sorted by score, lowest first, with the test VM at the top. Save as `0433/vcenter-cluster-vm-drs-scores.png`.
- Screen 3: the test VM > Monitor > Performance > Advanced > CPU, Chart Options: Real-time, counters Readiness (%) and Ready (ms), object the VM, with the legend table. Save as `0433/vcenter-vm-cpu-ready-real-time.png`.
- Condition the key depends on: Cluster DRS Score at 90% or more; the test VM's DRS Score below 60% and the lowest in the list; the test VM's Readiness (%) above 5% for most of the window, with the legend's Average above 5%; no CPU limit on the test VM.
- Masking: mask every VM, host, datastore and cluster name, including names in chart titles and legends.

## Likely wrong answer
A: the cluster score read as the state of every VM, so the cause is put inside the Guest OS, and F, the action that follows from it.

## Expected key points
- Answer: B, D, G.
- A false: the misconception. The Cluster DRS Score is a weighted average of the VM scores; it does not bound any single VM, and one VM barely moves it.
- B true: the list puts this VM at the top with a score far below the cluster figure.
- C false: the chart shows Readiness above 5% for most of the window.
- D true: Readiness is Ready per vCPU as a percentage of the sample; above 5% means the vCPUs spent that share of the time ready to run with no physical CPU free (no limit is set).
- E false: the over-correction. The cluster score is the indicator of cluster balance and health; it only cannot speak for a single VM.
- F false: the wrong action. The VM's Ready shows it waits for physical CPU, which no Guest OS tuning removes.
- G true: migrations filtered out by affinity rules or VM-host incompatibilities are causes of a low VM score that DRS cannot fix by itself.

## Notes
- Review 2026-11-15: the owner's quote no longer gives the screen's value; options reworded away from the theory half 0232; a false screen reading added (C). Key unchanged.
- Practical half of 0232 (pair: design.md, section 3.9).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C25). The options hold for any capture that meets the condition above. Counts only after author approval.

## Metadata
```yaml
id: "0433"
title: "Cluster DRS Score high, one VM low"
product: [vsphere]
technology: [system, cpu]
task: troubleshoot
level: 300
answer_type: deterministic
input: [screenshot]
object: [cluster, vm]
tool: [vcenter]
knowledge:
  - vsphere/object-types/cluster/configuration/drs-migration-levels
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/object-types/cluster/cluster-health-check
knowledge_main: vsphere/object-types/cluster/configuration/drs-migration-levels
attachments:
  - 0433/vcenter-cluster-summary-drs-score.png
  - 0433/vcenter-cluster-vm-drs-scores.png
  - 0433/vcenter-vm-cpu-ready-real-time.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C25"
answer: [B, D, G]
misconception: [A, F]
misconception_type: [average-hides-worst]
pair: "0232"
status: awaiting-input
```
