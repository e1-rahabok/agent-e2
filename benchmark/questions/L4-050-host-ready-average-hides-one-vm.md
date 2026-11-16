# Low host Ready, one slow database

## Prompt
- ESXi host esx-07: 2 sockets of 24 cores, Hyper-Threading on. 28 VMs with 110 vCPUs in total, none with a snapshot. Host Utilization about 60%.
- Between 14:00 and 15:00 the DBA of db-07 reported slow queries.
- In VCF Operations, esx-07's CPU Ready (%) for that hour is 1.1%.
- [The attached VCF Operations list](0115/esx-07-vms-cpu-14-to-15.csv) shows every VM on esx-07 for that hour: the highest Peak vCPU Ready within collection cycle and Peak vCPU Co-Stop within collection cycle, and the highest 5-minute Net Run (%).

Which statements are correct?

- A. The host value averages the VMs' Ready, so the one VM that waits, db-07, is diluted by the other 27.
- B. Host Ready of 1.1% for the hour shows that every VM on esx-07 got the CPU it asked for.
- C. db-07's Co-stop comes from its Ready: its siblings stop while one of its vCPUs waits.
- D. The other VMs are fine, so the problem must be inside the guest of db-07, not in ESXi.
- E. db-07 waits because of Hyper-Threading: a busy sibling thread puts its vCPUs into Ready.
- F. Check db-07's limit and shares, its resource pool, its size and the other load on esx-07 at that hour.
- G. Read each VM's own Ready per vCPU at the 20-second peak; the host value is only a starting point.
- H. Add a host to the cluster before anything else, since esx-07 is short of CPU.

## Likely wrong answer
B: the host average read as every VM. Or D: the slowness must be in the guest.

## Expected key points
- Answer: A, C, F, G.
- A is correct: db-07 shows Ready 7.8% at the peak; all other VMs are below 0.7%. The host value is averaged over the running VMs, so one 16-vCPU VM is diluted by the other 27.
- B is wrong: Ready belongs to each VM; a host value is a sum or average of its consumers.
- C is correct: Co-stop of 1.9% on a 16-vCPU VM: a vCPU in Ready makes its siblings stop to stay in step. The other listed causes are ruled out: no snapshot (stem), and 16 vCPUs fit one 24-core socket. The database feels both.
- D is wrong: Ready and Co-stop are waits in the ESXi scheduler, below the guest.
- E is wrong: Ready does not register Hyper-Threading; a busy sibling thread slows a running vCPU, it does not make it wait.
- F is correct: a CPU limit or low shares on db-07 or its resource pool can hold one VM back; a 16-vCPU VM needs many threads free at about the same time; and other load on the host at that hour competes with it. Check these before treating it as a cluster capacity problem.
- G is correct: contention is per consumer; sort the VMs by their own Ready, at the 20-second peak that keeps short waits visible.
- H is wrong: the other 27 VMs barely wait (Ready below 0.7%) and the host runs at about 60%; one large VM waits, so check its size, limits and shares before any capacity change.

## Notes
- Changed 2026-11-16 (re-review): the stem says no VM has a snapshot, so C's cause (Ready) is the only one left among co-stop's listed causes; truth unchanged.
- Changed in the 2026-11-15 audit: A no longer claims a weighting over vCPUs that the knowledge base does not state; C and F shortened and B and H lengthened (the correct options were the longest); the CSV header and the prompt name the product's peak metrics (Peak vCPU Ready and Peak vCPU Co-Stop within collection cycle); Net Run is the hour's highest 5-minute value, since the product has no peak Net Run metric.
- Stem changed 2026-11-14 (design.md 6.2; project/question-pairing-2026-11-14.md, A3): the phrase "averaged over its 110 vCPUs" stated the mechanism that option A tests; the stem now gives only the host's value. H (the wrong action) added. Key unchanged.
- Paired with 0016 (theory and practical, design.md 3.9).

## Metadata
```yaml
id: "0115"
title: "Low host Ready, one slow database"
product: [vsphere, vcf-operations]
technology: [cpu]
task: troubleshoot
level: 400
answer_type: deterministic
input: [table]
object: [vm, esxi]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/technology/cpu/metrics/virtual-motherboard/co-stop
  - vsphere/technology/cpu/metrics/comparisons/host-contention-metrics
  - vsphere/architecture/provider-consumer
knowledge_main: vsphere/technology/cpu/metrics/comparisons/host-contention-metrics
attachments:
  - 0115/esx-07-vms-cpu-14-to-15.csv
origin: synthetic
source_path: "Synthetic, 2026-11-12"
answer: [A, C, F, G]
misconception: [B, D]
misconception_type: [average-hides-worst, provider-vs-consumer]
pair: "0016"
status: draft
```
