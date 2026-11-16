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

Which statements about the cause of the slowness, what to change tonight and what not to change are correct?

- A. The snapshot still present on erp-db since Sunday fits the storage signature, the Co-stop, the Other Wait and the higher System time.
- B. Datastore read IOPS at 1.8 times virtual disk read IOPS, with equal throughput, is the signature of a snapshot chain.
- C. Datastore read IOPS above the VM's virtual disk read IOPS show that another VM on the datastore is doing the extra reads.
- D. Other Wait at 12% is the known ESXi accounting issue of idle VMs (Broadcom KB 338438), so ignore it.
- E. A snapshot is a known cause of both Co-stop and Other Wait on the VM that has it.
- F. System time above last week fits a snapshot: the kernel copies every guest write into each file of the chain.
- G. Other Wait at 12% is the time the vCPUs spend waiting for the 30 ms disk latency, so the two measure the same delay.
- H. Ready at 1.5% and Core Utilization of 55% on esx02 show that the host is not short of CPU.
- I. Memory Contention, Ballooned and Swapped all at 0 show that erp-db waits for no memory reclamation.
- J. The receive drops on app-03 point to a fault in the physical network, for the network team to fix.
- K. Co-stop at 6% is normal for a VM as wide as 24 vCPUs and needs no attention.
- L. A ninth host would lower the Co-stop of erp-db by giving DRS more room to place it.
- M. Run at 50% per vCPU and a guest run queue of 2 for 24 vCPUs show that erp-db is not short of vCPUs.
- N. erp-db is split over two NUMA nodes (NHN 0,1), and its size against the node is a cause of Co-stop.
- O. N%L at 70% means that 70% of the memory of erp-db sits on a remote NUMA node.
- P. Tonight, delete or consolidate the snapshot off-peak, and fix the backup job that left it.
- Q. After the snapshot is gone, read Co-stop and Other Wait again to confirm that they fall.

## Answers
A, B, E, H, I, M, N, P, Q

## Explanation
- A is correct: the storage and CPU evidence both point to the snapshot left by the backup: it raises read IOPS at equal throughput, it is a known cause of Co-stop and Other Wait, and the kernel time to traverse the chain shows as System. The NUMA span (N) adds to Co-stop but explains none of the other signs.
- B is correct: with a redo-log snapshot on VMFS, reads check the chain; the extra reads return no data, so read IOPS rise while throughput stays equal.
- C is wrong: on VMFS, datastore IOPS above virtual disk IOPS for the same VM points to a snapshot on this VM; these are the VM's own datastore counters.
- D is wrong: the accounting issue of Broadcom KB 338438 (legacy 85393) is fixed in ESXi 8.0 Update 3j, and these hosts run 9.1; it also shows on idle VMs, and erp-db runs at 50% per vCPU. Other Wait here is real, and a snapshot is a known cause of it.
- E is correct: snapshots cause Co-stop (Broadcom KB 2000058) and Other Wait.
- F is wrong: System time rises because the kernel traverses the snapshot chain on reads; writes go only to the newest file of the chain.
- G is wrong: Other Wait showed no correlation with disk latency or outstanding IO; it is a vCPU blocked in the VMM, not a disk latency counter.
- H is correct: low Ready and a host at 55% Core Utilization (35% Thread Utilization) rule out a host short of CPU.
- I is correct: no memory contention, no ballooning and no swapping. The remote memory share (O) is a separate access cost that these counters do not show.
- J is wrong: receive drops on a vNIC are counted at its virtual switch port; the usual cause is a full VMXNET3 receive ring, caused and fixed in the Guest OS driver of that VM, not the network team's problem. One application VM with drops is a local issue, not the cause of a slowness all users feel.
- K is wrong: in a high-performing environment Co-stop stays below 1%; 6% means the vCPUs are often held back. Its causes here are the snapshot and the VM's span over two NUMA nodes, with a sibling's Ready at 1.5%; more vCPUs would raise it further.
- L is wrong: the cluster is not short of CPU; a host changes neither the snapshot nor the Co-stop of one VM.
- M is correct: the vCPUs are half busy, and 2 threads waiting for 24 vCPUs is a short queue.
- N is correct: NHN 0,1 lists two home nodes, so the 24 vCPUs are split over two 16-core nodes: a wide VM. The VM's size against the NUMA boundary is one of the causes of Co-stop, next to the snapshot and a sibling's Ready.
- O is wrong: N%L is the local share: 70% local, about 30% remote. A secondary finding: erp-db is wide (24 vCPUs on 16-core nodes), so some remote memory is expected; size it to one node only if the guest demand allows.
- P is correct: the fix is to remove the snapshot and stop the backup job from leaving it.
- Q is correct: the check order ends by confirming that the snapshot was the cause; if Other Wait stays high, follow the Other Wait checks.
- Misconception: K: "Big VMs always show some Co-stop; 6% is nothing to worry about." - L: "Add the ninth host." - C: "The datastore IOPS above the VM's own disk IOPS must be another VM."

## Notes
- Revised 2026-11-12: management pack terms removed from the key (fairness); knowledge list without the pack's model files.
- Sources behind the CPU evidence: Broadcom KB 2000058 (snapshots and Co-stop); Broadcom KB 338438 (legacy 85393): an accounting issue inflates Other Wait on idle VMs from ESXi 7.0 Update 2, fixed in 8.0 Update 3j, so it does not apply to these 9.1 hosts.
- Synthetic, 2026-11-05, from the knowledge files listed in `knowledge`. Counts only after author approval.
- The consolidation stun is not asked; vsphere/object-types/vm/vmotion (Stun time) now names snapshot consolidate as a cause of a checkpoint stun.
- Review 2026-11-14: options F (System and the chain), J (app-03 drops) and O (N%L) turned into near misses, so fewer options are correct; each still tests its old key point.
- Audit 2026-11-15: D (snapshot IO in the virtual disk counters, tested by 0045) replaced by the Other Wait accounting issue; K (Co-stop is not a host shortage, over the two-question cap) replaced by "6% is normal"; N (more vCPUs raise Co-stop, over the cap) replaced by the NUMA span read from NHN; stem made plural. Key unchanged.
- Re-review 2026-11-16: A no longer says "most likely cause" (N names a second cause of Co-stop); it now names the signs the snapshot explains. I no longer says "rule memory out as the cause" beside N%L 70%; it now says what the three counters show. Key unchanged.

## Metadata
```yaml
id: "0090"
title: "ERP slow after the change window"
product: [vsphere, vcf-operations]
technology: [system, storage, cpu, memory, network]
task: troubleshoot
level: 400
answer_type: deterministic
misconception: [C,K,L]
input: [text]
knowledge:
  - vsphere/technology/storage/concepts/snapshot-impact
  - vsphere/technology/cpu/metrics/virtual-motherboard/co-stop
  - vsphere/technology/cpu/troubleshooting/vm-other-wait-high
  - vsphere/technology/cpu/metrics/virtual-motherboard/other-wait
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
source_path: "Synthetic, 2026-11-05; revised 2026-11-12"
misconception_type: [consumption-as-contention]
status: draft
```
