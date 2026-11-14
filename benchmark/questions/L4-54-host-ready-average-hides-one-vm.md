# Low host Ready, one slow database

## Prompt
- ESXi host esx-07: 2 sockets of 24 cores, Hyper-Threading on. 28 VMs with 110 vCPUs in total. Host Utilization about 60%.
- Between 14:00 and 15:00 the DBA of db-07 reported slow queries.
- The host's CPU Ready for that hour, averaged over its 110 vCPUs, is 1.1%.
- [The attached VCF Operations list](0115/esx-07-vms-cpu-14-to-15.csv) shows every VM on esx-07, with the 20-second peaks of CPU Ready (%), Co-stop (%) and Net Run (%) for that hour.

Which statements are correct?

- A. The host value hides db-07: it is weighted over 110 vCPUs, and one 16-vCPU VM waits while the others barely do.
- B. Host Ready of 1.1% shows that every VM on esx-07 got its CPU.
- C. db-07's Co-stop follows its Ready: when one of its vCPUs waits, the siblings are held back to stay in step. The database feels both.
- D. The other VMs are fine, so the problem must be inside the guest of db-07, not in ESXi.
- E. db-07 waits because of Hyper-Threading: a busy sibling thread puts its vCPUs into Ready.
- F. Next, check what else ran on esx-07 at that hour, a CPU limit or low shares on db-07 or its resource pool, and whether its 16 vCPUs fit the host, before any talk of adding hosts.
- G. Read each VM's own Ready per vCPU at the 20-second peak; the host value is only a starting point.

## Likely wrong answer
B: the host average read as every VM. Or D: the slowness must be in the guest.

## Expected key points
- Answer: A, C, F, G.
- A: db-07 shows Ready 7.8% at the peak; all other VMs are below 0.7%. The host value is an aggregate of its VMs and dilutes the one VM that suffers.
- B is wrong: Ready belongs to each VM; a host value is a sum or average of its consumers.
- C: Co-stop of 1.9% on a 16-vCPU VM: a vCPU in Ready makes its siblings stop.
- D is wrong: Ready and Co-stop are waits in the ESXi scheduler, below the guest.
- E is wrong: Ready does not register Hyper-Threading; a busy sibling thread slows a running vCPU, it does not make it wait.
- F: a 16-vCPU VM needs many threads free at about the same time; a limit or low shares can also hold one VM back. Check these before treating it as a cluster capacity problem.
- G: contention is per consumer; sort the VMs by their own Ready, at the 20-second peak that keeps short waits visible.

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
source_path: "Drafted by Claude 2026-11-12"
answer: [A, C, F, G]
misconception: [B, D]
misconception_type: [average-hides-worst, provider-vs-consumer]
status: draft
```
