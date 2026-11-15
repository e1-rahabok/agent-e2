# ERP slow after the change window

## Prompt
- The cluster:
  - 8 ESXi 9.1 hosts, VMFS datastores on a Fibre Channel array, DRS fully automated, HA with one host of failover capacity.
  - Each host: 2 sockets of 16 cores, Hyper-Threading on, 1 TB of DRAM, Balanced power management.
- The ERP system:
  - erp-db: 24 vCPUs, 384 GB of memory, on host esx02.
  - six application VMs with 8 vCPUs each, spread over the other hosts.
- In the change window on Sunday:
  - the backup product took a snapshot of erp-db before patching. It is still present.
  - esx05 entered maintenance mode and came back.
- Monday, 09:00-10:00, users report the ERP is slow. VCF Operations and esxtop show:
  - erp-db CPU, per vCPU, from VCF Operations: Run 50%, Ready 1.5%, Co-stop 6%, Other Wait 12%; System higher than last week. Guest OS CPU run queue 2, in total for the 24 vCPUs.
  - erp-db memory: Contention 0%, Ballooned 0, Swapped 0.
  - erp-db storage: disk latency 30 ms, mostly reads. Datastore read IOPS of the VM is 1.8 times its virtual disk read IOPS, with the same throughput.
  - erp-db NUMA, in esxtop: NHN 0,1; N%L 70%.
  - esx02: Core Utilization 55%, Thread Utilization 35%.
  - app-03: receive packets dropped 0.5%. The other application VMs: 0.

- The infrastructure manager proposes two changes for tonight: add 8 vCPUs to erp-db, and add a ninth host to the cluster.

What is the most likely cause of the slowness, what do you change tonight, and what do you not change? Which statements are correct?

- A. The snapshot still present on erp-db since Sunday is the most likely cause of the slowness.
- B. Datastore read IOPS at 1.8 times virtual disk read IOPS, with equal throughput, is the signature of a snapshot chain.
- C. Datastore read IOPS above the VM's virtual disk read IOPS show that another VM on the datastore is doing the extra reads.
- D. The extra snapshot reads show in the virtual disk counters of erp-db as well as in its datastore counters.
- E. A snapshot is a known cause of both Co-stop and Other Wait on the VM that has it.
- F. System time above last week fits a snapshot: the kernel copies every guest write into each file of the chain.
- G. Other Wait at 12% is the time the vCPUs spend waiting for the 30 ms disk latency, so the two measure the same delay.
- H. Ready at 1.5% and Core Utilization of 55% on esx02 show that the host is not short of CPU.
- I. Memory Contention, Ballooned and Swapped all at 0 rule memory out as the cause.
- J. The receive drops on app-03 point to a fault in the physical network, for the network team to fix.
- K. Co-stop at 6% shows that erp-db cannot get enough physical CPU, so the 8 extra vCPUs would help.
- L. A ninth host would lower the Co-stop of erp-db by giving DRS more room to place it.
- M. Run at 50% per vCPU and a guest run queue of 2 for 24 vCPUs show that erp-db is not short of vCPUs.
- N. Adding vCPUs to erp-db tends to raise its Co-stop, which grows with the vCPU count.
- O. N%L at 70% means that 70% of the memory of erp-db sits on a remote NUMA node.
- P. Tonight, delete or consolidate the snapshot off-peak, and fix the backup job that left it.
- Q. After the snapshot is gone, read Co-stop and Other Wait again to confirm that they fall.

## Likely wrong answer
- K: "The database is short of CPU: add the 8 vCPUs."
- L: "Add the ninth host."
- C: "The datastore IOPS above the VM's own disk IOPS must be another VM."

## Expected key points
- Answer: A, B, E, H, I, M, N, P, Q.
- A true: the storage and CPU evidence both point to the snapshot left by the backup.
- B true: with a redo-log snapshot on VMFS, reads check the chain; the extra reads return no data, so read IOPS rise while throughput stays equal.
- C false: on VMFS, datastore IOPS above virtual disk IOPS for the same VM points to a snapshot on this VM; these are the VM's own datastore counters.
- D false: virtual disk metrics exclude snapshot IO; datastore metrics include it. That gap is the signature.
- E true: snapshots cause Co-stop (Broadcom KB 2000058) and Other Wait.
- F false: System time rises because the kernel traverses the snapshot chain on reads; writes go only to the newest file of the chain.
- G false: Other Wait showed no correlation with disk latency or outstanding IO; it is a vCPU blocked in the VMM, not a disk latency counter.
- H true: low Ready and a host at 55% Core Utilization (35% Thread Utilization) rule out a host short of CPU.
- I true: no memory contention and no reclamation.
- J false: receive drops on a vNIC are counted at its virtual switch port; the usual cause is a full VMXNET3 receive ring, caused and fixed in the Guest OS driver of that VM, not the network team's problem. One application VM with drops is a local issue, not the cause of a slowness all users feel.
- K false: Co-stop comes from the VM's own vCPUs and the snapshot, not from a lack of physical CPU; Ready is low.
- L false: the cluster is not short of CPU; a host changes neither the snapshot nor the Co-stop of one VM.
- M true: the vCPUs are half busy, and 2 threads waiting for 24 vCPUs is a short queue.
- N true: Co-stop tends to be higher on VMs with more vCPUs; more vCPUs also widen the VM further across NUMA nodes.
- O false: N%L is the local share: 70% local, about 30% remote. A secondary finding: erp-db is wide (24 vCPUs on 16-core nodes), so some remote memory is expected; size it to one node only if the guest demand allows.
- P true: the fix is to remove the snapshot and stop the backup job from leaving it.
- Q true: the check order ends by confirming that the snapshot was the cause; if Other Wait stays high, follow the Other Wait checks.

## Notes
- Revised 2026-11-12: management pack terms removed from the key (fairness); knowledge list without the pack's model files.
- Sources behind the CPU evidence: Broadcom KB 2000058 (snapshots and Co-stop); Broadcom KB 85393 (an accounting issue can inflate Other Wait: check it if Other Wait stays high after the snapshot is gone).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
- Converted from judged to multiple choice (Q199 F, 2026-11-14). Dropped from the old key: "consolidation stuns the VM briefly" (no knowledge file states it).
- Review 2026-11-14: options F (System and the chain), J (app-03 drops) and O (N%L) turned into near misses, so fewer options are correct; each still tests its old key point.

## Metadata
```yaml
id: "0090"
title: "ERP slow after the change window"
product: [vsphere, vcf-operations]
technology: [system, storage, cpu, memory, network]
task: troubleshoot
level: 400
answer_type: deterministic
answer: [A,B,E,H,I,M,N,P,Q]
misconception: [C,K,L]
input: [text]
knowledge:
  - vsphere/technology/storage/concepts/snapshot-impact
  - vsphere/technology/cpu/metrics/virtual-motherboard/co-stop
  - vsphere/technology/cpu/troubleshooting/vm-other-wait-high
  - vsphere/technology/cpu/concepts/numa
  - vsphere/tools/esxtop/memory
  - vsphere/technology/network/vnic-rx-drops
  - vsphere/technology/storage/metrics/virtual-motherboard/datastore
  - vsphere/technology/cpu/metrics/host/core-utilization
knowledge_main: vsphere/technology/storage/concepts/snapshot-impact
object: [vm, esxi, cluster, datastore]
tool: [vcf-operations, esxtop]
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05; revised 2026-11-12"
misconception_type: [consumption-as-contention]
status: draft
```
