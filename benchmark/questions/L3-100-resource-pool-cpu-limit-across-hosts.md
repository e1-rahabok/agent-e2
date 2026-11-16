# A resource pool CPU limit across hosts

## Prompt
- DRS cluster of 8 hosts, each 48 GHz of CPU. The hosts run at 40-60% CPU at the busiest hour.
- Resource pool RP-Reports holds 24 VMs and has a CPU limit of 60 GHz. Its sibling pool, RP-Apps, has no limit.
- At the busiest hour the 24 VMs of RP-Reports together ask for more than 60 GHz.

Which statements about how the limit acts and how it shows are correct?

- A. On a host with spare CPU, a VM of the capped pool is not held back.
- B. Two VMs of RP-Reports on different hosts draw on the same 60 GHz.
- C. Capping RP-Reports pushes up the wait of the VMs in RP-Apps.
- D. Spread RP-Reports over two extra hosts to lift its throughput at the peak.
- E. Once capped, the pool's total CPU barely moves from one sample to the next.
- F. CPU Ready on any VM of the cluster is a sign that the limit of RP-Reports is reached.

## Answers
B, E

## Explanation
- A is wrong: the misconception. The pool's limit applies across the cluster; once the pool's VMs together reach 60 GHz, each of them is held back wherever it runs, also on a host with spare CPU.
- B is correct: a pool's reservation, limit and shares apply across the cluster, while each of its VMs runs on one host; the VMs of the pool share one ceiling wherever they run.
- C is wrong: a limit caps only its own pool and frees CPU for the siblings; it cannot raise Ready in a sibling pool.
- D is wrong: the wrong action. More hosts do not help a pool at its limit: its VMs share the same cap.
- E is correct: a pool at its limit shows its CPU usage flat near the limit while its hosts have spare CPU; a pool that is not capped varies with its load.
- F is wrong: the over-correction. Ready also comes from host contention, shares and vMotion; the wait from the pool limit follows the pool, not the host.
- Misconception: A: a pool limit is read as a per-host cap that leaves a VM free on a host with spare CPU. Or D: more hosts are expected to lift a capped pool.

## Notes
- Theory half of 0239 (pair: design.md, section 3.9). Different numbers and names from 0239, so one does not give away the other.
- Synthetic, 2026-11-14, for the question pairing plan (project/question-pairing-2026-11-14.md, item B4). Counts only after author approval.
- 2026-11-15 audit: old A (a limit caps the child pools) dropped, as 0140 and 0291 keep it; old E (Max Limited) dropped, as the VM-limit pair 0103/0066 keeps the limit-time fact; misconception B reworded to the pool-scope fact (still false). Letters: A dropped; B -> A (new text); C -> B; D -> C; E dropped; F -> D; G -> E; H -> F.

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
source_path: "Synthetic, 2026-11-14, pairing plan item B4"
misconception: [A, D]
misconception_type: [provider-vs-consumer]
pair: "0239"
status: draft
```
