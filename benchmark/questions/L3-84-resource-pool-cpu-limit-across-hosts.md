# A resource pool CPU limit across hosts

## Prompt
- DRS cluster of 8 hosts, each 48 GHz of CPU. The hosts run at 40-60% CPU at the busiest hour.
- Resource pool RP-Reports holds 24 VMs and has a CPU limit of 60 GHz. Its sibling pool, RP-Apps, has no limit.
- At the busiest hour the 24 VMs of RP-Reports together ask for more than 60 GHz.

Which statements about how the limit acts and how it shows are correct?

- A. The limit caps the pool's VMs together, across all the hosts they run on.
- B. On a host with spare CPU, a VM held by the pool limit shows lower CPU Usage and no CPU Ready.
- C. A VM of RP-Reports on a quiet host can be held back by the load of the pool's VMs on other hosts.
- D. The limit on RP-Reports raises CPU Ready in the VMs of RP-Apps.
- E. vCenter reports the time a VM is held back by a limit as Max Limited (ms).
- F. Add two hosts to the cluster, so that the pool's VMs get more CPU at the busiest hour.
- G. At the limit, the pool's CPU usage runs flat at one value, sample after sample.
- H. CPU Ready on any VM of the cluster is a sign that the limit of RP-Reports is reached.

## Likely wrong answer
B: a limit is read as a cap on Usage that leaves Ready at 0 when the host has spare CPU. Or F: Ready is read as a cluster short of CPU.

## Expected key points
- Answer: A, C, E, G.
- A true: a pool's reservation, limit and shares apply across the cluster, while each of its VMs runs on one host.
- B false: the misconception. Ready includes the time a vCPU is held back by a limit (the limbo queue), whatever the host's free CPU.
- C true: the cap is cluster-wide, so the pool's load elsewhere can hold back a VM on a host with spare CPU.
- D false: a limit caps only its own pool and frees CPU for the siblings; it cannot raise Ready in a sibling pool.
- E true: vCenter also reports the time held back by a limit as Max Limited (ms).
- F false: the wrong action. More hosts do not help a pool at its limit: its VMs share the same cap.
- G true: a pool at its limit shows its CPU usage flat near the limit while its hosts have spare CPU; a pool that is not capped varies with its load.
- H false: the over-correction. Ready also comes from host contention, shares and vMotion; the wait from the pool limit follows the pool, not the host.

## Notes
- Theory half of 0239 (pair: design.md, section 3.9). Different numbers and names from 0239, so one does not give away the other.
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item B4). Counts only after author approval.

## Metadata
```yaml
id: "0429"
title: "A resource pool CPU limit across hosts"
product: [vsphere]
technology: [cpu, system]
task: explain-mechanism
level: 300
answer_type: deterministic
input: [text]
object: [resource-pool, vm, cluster]
tool: [vcenter]
knowledge:
  - vsphere/object-types/resource-pool/resource-pool-design
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/architecture/resource-controls
knowledge_main: vsphere/object-types/resource-pool/resource-pool-design
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item B4"
answer: [A, C, E, G]
misconception: [B, F]
misconception_type: [provider-vs-consumer]
pair: "0239"
status: draft
```
