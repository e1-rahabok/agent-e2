# Cluster DRS Score high, one VM low

## Prompt
- Users of one VM report slow responses this morning. The application owner sends [the cluster summary](0433/vcenter-cluster-summary-drs-score.png) and says: "The cluster scores above 90%, so vSphere is fine. The problem must be inside the VM."
- You open [the VM DRS Score list](0433/vcenter-cluster-vm-drs-scores.png) of the cluster and [the CPU chart of that VM](0433/vcenter-vm-cpu-ready-real-time.png).

Which statements are correct?

- A. The cluster score above 90% shows every VM is served well, so the cause lies inside this VM's Guest OS.
- B. The cluster score is a weighted average of the VM scores, so one VM with a low score barely moves it.
- C. The VM's low DRS Score alone proves that it waits for CPU.
- D. The CPU chart shows the VM's vCPUs, on average, ready to run but not running for more than 5% of the time.
- E. The cluster score carries no information here; set it aside.
- F. Set the DRS migration threshold to level 1, so that DRS moves this VM to a host with more room.
- G. A VM-Host affinity rule can keep DRS from moving this VM to a less busy host.

## Input to supply
- Product and version: vSphere 9.1 (vSphere Client), a DRS cluster, fully automated, default migration threshold.
- How to produce it in a lab: a "must run on" VM-Host rule that keeps the test VM and two or three CPU-burner VMs on one host, with their vCPUs together 1.5-2 times that host's physical threads; the other VMs of the cluster stay light. Run the burners and the test VM's load for 20-30 minutes.
- Screen 1: the cluster > Summary, the vSphere DRS card with the Cluster DRS Score. Save as `0433/vcenter-cluster-summary-drs-score.png`.
- Screen 2: the cluster > Monitor > vSphere DRS > VM DRS Score, sorted by score, lowest first, with the test VM at the top. Save as `0433/vcenter-cluster-vm-drs-scores.png`.
- Screen 3: the test VM > Monitor > Performance > Advanced > CPU, Chart Options: Real-time, counters Readiness (%) and Ready (ms), object the VM, with the legend table. Save as `0433/vcenter-vm-cpu-ready-real-time.png`.
- Condition the key depends on: Cluster DRS Score at 90% or more; the test VM's DRS Score below 60% and the lowest in the list; the test VM's Readiness above 5% for most of the window; no CPU limit on the test VM.
- Masking: mask every VM, host, datastore and cluster name, including names in chart titles and legends.

## Likely wrong answer
A: the cluster score read as the state of every VM, so the cause is put inside the Guest OS. Or C: the VM score read as contention.

## Expected key points
- Answer: B, D, G.
- A false: the misconception. A weighted average of the VM scores does not bound any single VM; this VM scores far lower and its Ready shows it waits.
- B true: the Cluster DRS Score is the weighted average of the VM DRS Scores of the powered-on VMs; one VM hardly moves it.
- C false: a VM DRS Score reflects execution efficiency, not contention; the Ready chart is what shows the VM waits.
- D true: Readiness is Ready per vCPU as a percentage of the sample; above 5% means the vCPUs spent that share of the time ready to run with no physical CPU free (no limit is set).
- E false: the over-correction. The cluster score is the indicator of cluster balance and health; it only cannot speak for a single VM.
- F false: the wrong action. At level 1 DRS recommends only mandatory moves (rule violations, maintenance mode); it no longer moves VMs to improve resource availability.
- G true: migrations filtered out by affinity rules or VM-host incompatibilities are causes of a low VM score that DRS cannot fix by itself.

## Notes
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
misconception: [A, C]
misconception_type: [average-hides-worst]
pair: "0232"
status: awaiting-input
```
