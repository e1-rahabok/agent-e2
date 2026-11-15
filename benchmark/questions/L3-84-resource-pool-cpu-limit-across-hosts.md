# A resource pool CPU limit across hosts

## Prompt
- DRS cluster of 8 hosts, each 48 GHz of CPU. The hosts run at 40-60% CPU at the busiest hour.
- Resource pool RP-Reports holds 24 VMs and has a CPU limit of 60 GHz. Its sibling pool, RP-Apps, has no limit.
- At the busiest hour the 24 VMs of RP-Reports together ask for more than 60 GHz.

Which statements about how the limit acts and how it shows are correct?

- A. A limit on RP-Reports also caps any child pool created under it.
- B. On a host with spare CPU, a VM held by the pool limit shows no CPU Ready.
- C. Two VMs of RP-Reports on different hosts draw on the same 60 GHz.
- D. Capping RP-Reports pushes up the wait of the VMs in RP-Apps.
- E. The vSphere Client keeps the time a vCPU is held back by a limit as a counter of its own.
- F. Spread RP-Reports over two extra hosts to lift its throughput at the peak.
- G. Once capped, the pool's total CPU barely moves from one sample to the next.
- H. CPU Ready on any VM of the cluster is a sign that the limit of RP-Reports is reached.

## Likely wrong answer
B: a limit is read as a cap that leaves Ready at 0 when the host has spare CPU. Or F: more hosts are expected to lift a capped pool.

## Expected key points
- Answer: A, C, E, G.
- A true: a limit on one pool caps that pool and its descendants.
- B false: the misconception. Ready includes the time a vCPU is held back by a limit (the limbo queue), whatever the host's free CPU.
- C true: a pool's reservation, limit and shares apply across the cluster, while each of its VMs runs on one host; the VMs of the pool share one ceiling wherever they run.
- D false: a limit caps only its own pool and frees CPU for the siblings; it cannot raise Ready in a sibling pool.
- E true: vCenter reports the time held back by a limit as Max Limited (ms).
- F false: the wrong action. More hosts do not help a pool at its limit: its VMs share the same cap.
- G true: a pool at its limit shows its CPU usage flat near the limit while its hosts have spare CPU; a pool that is not capped varies with its load.
- H false: the over-correction. Ready also comes from host contention, shares and vMotion; the wait from the pool limit follows the pool, not the host.

## Notes
- Review 2026-11-15: B one fact; A, C, D, E, F, G reworded away from 0239 (its options B, D, E, H, L, M). Key letters unchanged.
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
