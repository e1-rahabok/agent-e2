# Can this cluster take 12 reserved VMs?

## Prompt
- Cluster prod-cl02: 4 identical hosts. The root resource pool of each host offers 500 GB of memory, so 2,000 GB for the cluster. DRS fully automated, cluster state green.
- vSphere HA admission control: cluster resource percentage, set manually to 25% for CPU and memory.
- Powered-on VMs: 180. Their memory reservations plus overhead add up to 1,344 GB. Memory Consumed is 58% of the cluster. CPU Utilization is 39%.
- A project asks to power on 12 VMs, 4 vCPUs and 16 GB each, with the full 16 GB reserved. Each has about 0.4 GB of overhead memory. They go to the prod-pool resource pool.
- VCF Operations, one hour, per VM, highest 20-second Ready per vCPU: nine VMs in the dev-pool resource pool show 14% to 18% with Net Run of 40% to 50%. The other 171 VMs show less than 0.5%. dev-pool has a CPU limit of 12 GHz, and its VMs demand about 19 GHz.
- The project manager says: "Consumed is 58%, so 40% of the cluster is free. 12 VMs of 16 GB is 192 GB. Power them on."

Which statements about the 12 VMs and the health check of this cluster are correct?

- A. At most nine of the twelve VMs power on; the tenth fails HA admission control.
- B. Consumed at 58% leaves about 840 GB free, so all twelve VMs can power on.
- C. With 25% kept for failover, reservations plus overhead may total 1,500 GB, which leaves 156 GB for the new VMs.
- D. Each new VM is charged only its 16 GB reservation; its overhead memory stays out of the admission check.
- E. Memory Consumed plays no part in HA admission control with the percentage policy.
- F. Nine VMs at 14% to 18% Ready show the cluster is short of CPU, so it needs a host before any new VM.
- G. The nine dev-pool VMs wait because the pool's 12 GHz CPU limit is below the 19 GHz its VMs demand.
- H. Time a VM is held back by a CPU limit is not counted as Ready, so the dev-pool Ready must come from busy hosts.
- I. A CPU Utilization of 39% shows that no VM in the cluster can be waiting for CPU.
- J. Adding a fifth host would not remove the Ready of the dev-pool VMs.
- K. Lowering the new VMs' reservations below 16 GB would let more of them pass admission control.
- L. A fifth identical host would add about 375 GB of reservable memory at the 25% setting.
- M. With HA admission control turned off, reserved VMs are the first that HA cannot restart after a host failure.
- N. The check reads cluster state and failover capacity first, then contention, and capacity after that.
- O. With the full 16 GB reserved, each new VM's Consumed memory jumps to 16 GB at power-on.

## Likely wrong answer
- B: "58% consumed leaves plenty of memory, so all 12 power on."
- F: "Nine VMs show 14% to 18% Ready, so the cluster is out of CPU and needs a host."

## Expected key points
- Answer: A, C, E, G, J, K, L, M, N.
- A true: 156 GB of headroom at 16.4 GB per VM: nine take 147.6 GB, a tenth would take the total to 164 GB. The tenth power-on fails with insufficient failover resources.
- B false: admission control compares reservations plus overhead with unreserved capacity, not Consumed with free memory. A cluster can refuse a power-on with plenty of free memory.
- C true: 75% of 2,000 GB is 1,500 GB; 1,500 - 1,344 = 156 GB.
- D false: per-VM overhead memory counts as reserved, on top of the memory reservation: 16.4 GB per VM.
- E true: admission control counts reservations, not usage.
- F false: nine of 180 VMs (5%) in one pool wait, the other 171 show no wait, and utilization is 39%. The wait follows the pool, not the hosts: a limit, not a lack of cluster capacity. It is not a reason to refuse the new VMs.
- G true: the pool limit (12 GHz) is below its demand (19 GHz). Check resource pools and limits in the configuration step.
- H false: Ready includes time held back by a limit; vCenter also shows that part as Max Limited.
- I false: cluster utilization is an average; the dev-pool VMs wait at 39% utilization because of their pool limit.
- J true: more hosts do not help a pool at its limit; its VMs share the same cap.
- K true: admission control charges the reservation plus overhead. Reserving what the VMs use, or powering on in phases, are options for the project.
- L true: 500 GB x 75% = 375 GB of reservable memory with 25% kept (more with a lower percentage).
- M true: with HA admission control off the 12 VMs power on, but after a host failure HA restarts a VM only where its reservation plus overhead fits.
- N true: availability first (green, failover capacity met: 1,344 GB below 1,500 GB), then contention, then configuration and capacity. Contention comes before capacity.
- O false: a memory reservation is backed only as the VM touches memory; Consumed grows with use and does not jump to the reservation.

## Notes
- Public source: Cluster Resources Percentage Admission Control, vSphere 9.1 (TechDocs, updated 2026-11-09): memory failover capacity is (total host memory - total VM memory requirements) / total host memory, host memory from the root resource pool; reservation plus overhead of each powered-on VM; "If any check fails, admission control disallows the operation"; default reservation 0 MB. Resource pool CPU limit: vSphere 9.1 Resource Management.
- Why one answer: the arithmetic decides: 156 GB of headroom, 16.4 GB per VM, 9 fit and 10 do not. Same mechanism as question L2-10 and L3-57, here combined with the contention check.
- Debatable risk: low on the number. The overhead of 0.4 GB is given in the prompt so nobody has to estimate it. The "order" part is the design logic of the cluster health check (availability, then contention, then configuration, then capacity); the key does not require any particular recommendation to the project.
- Rests on: the vendor page above for the 9; the knowledge file's design logic (cluster-health-check, Order rationale: contention overrides utilization; step 4: resource pools and limits first; step 6: can it take more VMs) for the order.
- Converted from judged to multiple choice (Q199 F, 2026-11-14). Knowledge added: resource-pool-design (a pool at its limit: Ready follows the pool; more hosts do not help).

## Metadata
```yaml
id: "0355"
title: "Can this cluster take 12 reserved VMs?"
product: [vsphere, vcf-operations]
technology: [memory, cpu, system]
task: decide-capacity
level: 400
answer_type: deterministic
answer: [A,C,E,G,J,K,L,M,N]
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
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
misconception_type: [consumption-as-contention]
status: draft
```
