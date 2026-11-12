# ERP slow after the change window

## Prompt
- The cluster:
  - 8 ESXi 9.1 hosts with vSAN, DRS fully automated, HA with one host of failover capacity.
  - Each host: 2 sockets of 16 cores, Hyper-Threading on, 1 TB of DRAM, Balanced power management.
- The ERP system:
  - erp-db: 24 vCPUs, 384 GB of memory, on host esx02.
  - six application VMs with 8 vCPUs each, spread over the other hosts.
- In the change window on Sunday:
  - the backup product took a snapshot of erp-db before patching. It is still present.
  - esx05 entered maintenance mode and came back.
- Monday, 09:00-10:00, users report the ERP is slow. VCF Operations and esxtop show:
  - erp-db CPU: Ready 1.5%, Co-stop 6%, Other Wait 12%, System higher than last week. CPU Run Queue 2. CPU Run 85%
  - erp-db memory: Contention 0%, Ballooned 0, Swapped 0.
  - erp-db storage: disk latency 30 ms, mostly reads. Datastore read IOPS of the VM is 1.8 times its virtual disk read IOPS, with the same throughput.
  - erp-db NUMA, in esxtop: NHN 0,1; N%L 70%.
  - esx02: Core Utilization 55%, Thread Utilization 35%.
  - app-03: receive packets dropped 0.5%. The other application VMs: 0.

- The infrastructure manager proposes two changes for tonight: add 8 vCPUs to erp-db, and add a ninth host to the cluster.

What is the most likely cause of the slowness? Weigh the evidence for and against CPU, memory, storage and network. Give the checks in order, what you change tonight, and what you do not change, with reasons.

## Likely wrong answer
"The database is short of CPU: add the 8 vCPUs and the ninth host."

## Expected key points
- Most likely cause: the snapshot on erp-db.
- Storage evidence: datastore read IOPS above virtual disk read IOPS with the same throughput is the snapshot signature: reads must check every snapshot file. It explains the read latency.
- CPU evidence: snapshots are a cause of Co-stop (KB 2000058) and of Other Wait; System rises because the kernel traverses the snapshot chain. Ready 1.5% and the host at 55% core utilization rule out a host short of CPU.
- Memory: Contention, Ballooned and Swapped at 0 rule memory out.
- Network: receive drops on app-03 alone are a separate, local issue (check its receive ring); they do not explain a slow ERP across all users.
- Check order: confirm the snapshot and its chain; datastore vs virtual disk IOPS; per virtual disk read and write latency; then Co-stop and Other Wait after the snapshot is gone; check Broadcom KB 85393 if Other Wait stays high.
- Tonight: delete or consolidate the snapshot, off-peak, and fix the backup job that left it. Consolidation stuns the VM briefly.
- Secondary: erp-db is a wide VM (24 vCPUs on 16-core nodes) with 30% remote memory (N%L 70%). It is also a CPU monster (above 50% of 32 cores) and a memory monster (above 256 GB). Size it to one NUMA node only if the Guest OS demand allows.
- Do not add 8 vCPUs: more vCPUs raise Co-stop and spread the VM further across NUMA nodes.
- Do not add a host: Ready is low, core utilization 55%, thread utilization 35%; Cluster Performance is driven by Co-stop of one VM, not by breadth.

## Notes
- Previous id: question-0090 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0090"
title: "ERP slow after the change window"
product: [vsphere, vsan, vcf-operations]
technology: [system, storage, cpu, memory, network]
task: troubleshoot
level: 400
answer_type: judged
input: [text]
knowledge:
  - vsphere/technology/storage/concepts/snapshot-impact
  - vsphere/technology/cpu/metrics/virtual-motherboard/co-stop
  - vsphere/technology/cpu/troubleshooting/vm-other-wait-high
  - vsphere/technology/cpu/concepts/numa
  - vsphere/object-types/cluster/models/cluster-risk
  - vsphere/object-types/cluster/cluster-performance
  - vsphere/technology/network/vnic-rx-drops
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
status: draft
```
