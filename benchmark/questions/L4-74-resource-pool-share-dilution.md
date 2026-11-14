# Resource pool shares divided among many VMs

## Prompt
- DRS cluster with 32 physical cores in total, and two sibling resource pools at the root. Scalable Shares is off (the default).
- Prod: CPU shares High (8,000). It holds 40 VMs of 4 vCPUs each.
- Test: CPU shares Normal (4,000). It holds 4 VMs of 4 vCPUs each.
- Every VM has default (Normal) CPU shares. No reservations, no limits.
- During the month-end close, the VMs of both pools demand far more CPU than the cluster has.

Which statements are correct?

- A. During the close, each Prod VM gets about one fifth of the CPU that each Test VM gets.
- B. Each Prod VM gets about twice the CPU of each Test VM, because Prod has High shares and Test has Normal.
- C. When no host is short of CPU, every VM gets what it demands, whatever its pool's shares.
- D. With Scalable Shares on, each Prod VM would get about twice the CPU of each Test VM.
- E. Inside each pool, the pool's CPU is divided among its VMs by their own shares: equally here.

## Likely wrong answer
B: reading the pool's High shares as the priority of each of its VMs.

## Expected key points
- Answer: A, C, D, E.
- A: under contention the pools split the cluster 8,000 : 4,000, so Prod gets 2/3 and Test 1/3. Prod divides 2/3 among 40 VMs (1/60 each); Test divides 1/3 among 4 VMs (1/12 each). A Prod VM gets 1/5 of a Test VM.
- B is wrong: a pool's shares belong to the pool and are divided among its VMs. The more VMs in a pool, the less each gets: dilution.
- C: shares act only when demand exceeds supply, and they are applied on each host.
- D: with Scalable Shares on, a pool's shares follow its VMs (the sum of its VMs' shares × 4 for High, × 2 for Normal): Prod 40 × 4,000 × 4 = 640,000, Test 4 × 4,000 × 2 = 32,000. Per VM: 16,000 vs 8,000, so 2x.
- E: inside a pool, sibling VMs split the pool's entitlement by their own shares; all are equal here.

## Notes
- Drafted 2026-11-12.
- Scalable Shares: vSphere 7.0 and later, per cluster or per resource pool (vSphere 9.1 Resource Management, Scalable Shares).

## Metadata
```yaml
id: "0230"
title: "Resource pool shares divided among many VMs"
product: [vsphere]
technology: [system, cpu]
task: explain-mechanism
level: 400
answer_type: deterministic
input: [text]
object: [resource-pool, cluster, vm]
tool: [vcenter]
knowledge:
  - vsphere/object-types/resource-pool/resource-pool-design
  - vsphere/architecture/resource-controls
knowledge_main: vsphere/object-types/resource-pool/resource-pool-design
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
answer: [A, C, D, E]
misconception: [B]
misconception_type: [same-name-other-object]
status: draft
```
