# Can this cluster take 12 reserved VMs?

## Prompt
- Cluster prod-cl02: 4 identical hosts. The root resource pool of each host offers 500 GB of memory, so 2,000 GB for the cluster. DRS fully automated, cluster state green.
- vSphere HA admission control: cluster resource percentage, set manually to 25% for CPU and memory.
- Powered-on VMs: 180. Their reserved memory adds up to 1,344 GB. Memory Consumed is 58% of the cluster. CPU Utilization is 39%.
- A project asks to power on 12 VMs, 4 vCPUs and 16 GB each, with the full 16 GB reserved; each will count 16.4 GB of reserved memory. They go to the prod-pool resource pool.
- VCF Operations, one hour, per VM, highest 20-second Ready per vCPU: nine VMs in the dev-pool resource pool show 14% to 18% with Net Run of 40% to 50%. The other 171 VMs show less than 0.5%. dev-pool has a CPU limit of 12 GHz, and its VMs demand about 19 GHz.
- The project manager says: "Consumed is 58%, so 40% of the cluster is free. 12 VMs of 16 GB is 192 GB. Power them on."

Which statements about the 12 VMs and the health check of this cluster are correct?

- A. At most nine of the twelve VMs power on; the tenth fails HA admission control.
- B. Consumed at 58% leaves about 840 GB free, so all twelve VMs can power on.
- C. With 25% kept for failover, reservations plus overhead may total 1,500 GB, which leaves 156 GB for the new VMs.
- D. Powering on the twelve VMs in two batches, an hour apart, lets all twelve pass admission control.
- E. Memory Consumed plays no part in HA admission control with the percentage policy.
- F. Nine VMs at 14% to 18% Ready show the cluster is short of CPU, so it needs a host before any new VM.
- G. Raising the dev-pool CPU limit to about 20 GHz would lower the nine VMs' Ready without adding a host.
- H. A CPU Utilization of 39% shows that no VM in the cluster can be waiting for CPU.
- I. Lowering the new VMs' reservations below 16 GB would let more of them pass admission control.
- J. A fifth identical host would add about 375 GB of reservable memory at the 25% setting.
- K. With HA admission control turned off, reserved VMs are the first that HA cannot restart after a host failure.
- L. The check reads cluster state and failover capacity first, then contention, and capacity after that.
- M. With the full 16 GB reserved, each new VM's Consumed memory jumps to 16 GB at power-on.

## Likely wrong answer
- B: "58% consumed leaves plenty of memory, so all 12 power on."
- F: "Nine VMs show 14% to 18% Ready, so the cluster is out of CPU and needs a host."

## Expected key points
- Answer: A, C, E, G, I, J, K, L.
- A is correct: 156 GB of headroom at 16.4 GB per VM: nine take 147.6 GB, a tenth would take the total to 164 GB. The tenth power-on fails with insufficient failover resources.
- B is wrong: admission control compares reserved memory with the capacity left after the failover share, not Consumed with free memory. A cluster can refuse a power-on with plenty of free memory.
- C is correct: 75% of 2,000 GB is 1,500 GB; 1,500 - 1,344 = 156 GB.
- D is wrong: the reservations of powered-on VMs keep counting; the first batch's reservations still hold when the second batch powers on, so the tenth VM fails whatever the timing.
- E is correct: the percentage policy sums reservations plus overhead of the powered-on VMs; usage plays no part.
- F is wrong: nine of 180 VMs (5%) in one pool wait, the other 171 show no wait, and utilization is 39%. The wait follows the pool, not the hosts: a limit, not a lack of cluster capacity. It is not a reason to refuse the new VMs.
- G is correct: the pool limit (12 GHz) is below its VMs' demand (19 GHz), and Ready includes the time a limit holds back; with the cluster at 39% the hosts have spare CPU, so a limit above the demand removes that wait. Check resource pools and limits in the configuration step.
- H is wrong: cluster utilization is an average; the dev-pool VMs wait at 39% utilization because of their pool limit.
- I is correct: admission control charges each VM's reserved memory; a smaller reservation leaves room for more VMs in the 156 GB.
- J is correct: 500 GB x 75% = 375 GB of reservable memory with 25% kept (more with a lower percentage).
- K is correct: with HA admission control off the 12 VMs power on, but after a host failure HA restarts a VM only where its reservation plus overhead fits.
- L is correct: availability first (green, failover capacity met: 1,344 GB below 1,500 GB), then contention, then configuration and capacity. Contention comes before capacity.
- M is wrong: a memory reservation is backed only as the VM touches memory; Consumed grows with use and does not jump to the reservation.

## Notes
- Synthetic, 2026-11-13, for the coverage gap (project/plan.md).
- Public source: Cluster Resources Percentage Admission Control, vSphere 9.1 (TechDocs, updated 2026-11-09): memory failover capacity is (total host memory - total VM memory requirements) / total host memory, host memory from the root resource pool; reservation plus overhead of each powered-on VM; "If any check fails, admission control disallows the operation"; default reservation 0 MB. Resource pool CPU limit: vSphere 9.1 Resource Management.
- The arithmetic decides: 156 GB of headroom, 16.4 GB per VM, 9 fit and 10 do not. The 16.4 GB per VM (overhead included) is given in the stem: the overhead fact is tested by 0152 and 0292.
- The order part is the design logic of the cluster health check (cluster-health-check, Order rationale: contention overrides utilization; step 4: resource pools and limits first; step 6: can it take more VMs); the key does not require any particular recommendation to the project.
- 2026-11-15 audit: old H (Ready includes limit time, Max Limited) and old J (more hosts do not help a pool at its limit) dropped: the pair 0429/0239 and the VM-limit pair keep those facts. Old D (overhead left out) replaced by the two-batch reading. Letters: A-G unchanged; H dropped; I -> H; J dropped; K -> I; L -> J; M -> K; N -> L; O -> M.

## Metadata
```yaml
id: "0355"
title: "Can this cluster take 12 reserved VMs?"
product: [vsphere, vcf-operations]
technology: [memory, cpu, system]
task: decide-capacity
level: 400
answer_type: deterministic
answer: [A,C,E,G,I,J,K,L]
misconception: [B,F]
input: [text]
object: [cluster, resource-pool, vm]
tool: [vcenter, vcf-operations]
knowledge:
  - vsphere/object-types/cluster/cluster-health-check
  - vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
  - vsphere/object-types/cluster/decision-tree/can-cluster-take-more-vms
  - vsphere/architecture/resource-controls
  - vsphere/object-types/resource-pool/resource-pool-design
knowledge_main: vsphere/object-types/cluster/cluster-health-check
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-13"
misconception_type: [consumption-as-contention]
status: draft
```
