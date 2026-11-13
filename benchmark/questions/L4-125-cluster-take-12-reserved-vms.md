# Can this cluster take 12 reserved VMs?

## Prompt
- Cluster prod-cl02: 4 identical hosts. The root resource pool of each host offers 500 GB of memory, so 2,000 GB for the cluster. DRS fully automated, cluster state green.
- vSphere HA admission control: cluster resource percentage, set manually to 25% for CPU and memory.
- Powered-on VMs: 180. Their memory reservations plus overhead add up to 1,344 GB. Memory Consumed is 58% of the cluster. CPU Utilization is 39%.
- A project asks to power on 12 VMs, 4 vCPUs and 16 GB each, with the full 16 GB reserved. Each has about 0.4 GB of overhead memory. They go to the prod-pool resource pool.
- VCF Operations, one hour, per VM, highest 20-second Ready per vCPU: nine VMs in the dev-pool resource pool show 14% to 18% with Net Run of 40% to 50%. The other 171 VMs show less than 0.5%. dev-pool has a CPU limit of 12 GHz, and its VMs demand about 19 GHz.
- The project manager says: "Consumed is 58%, so 40% of the cluster is free. 12 VMs of 16 GB is 192 GB. Power them on."

Can the cluster take the 12 VMs? Walk through the health check in the order you would read it and say what decides the answer.

## Likely wrong answer
"Yes: 58% consumed leaves plenty of memory, so all 12 power on." Or "No: nine VMs show 14% to 18% Ready, so the cluster is out of CPU and needs a host."

## Expected key points
- No for 12; at most 9 power on. The limit is HA admission control, which counts reservations plus overhead, not Consumed. With 25% kept for failover, 75% of 2,000 GB, that is 1,500 GB, may be reserved. 1,500 - 1,344 = 156 GB are left. Each VM takes 16.4 GB: nine take 147.6 GB, a tenth would take the total to 164 GB. The tenth power-on fails with insufficient failover resources.
- Consumed (58%) and the 192 GB against free memory are the wrong test: admission control compares reservations with the unreserved capacity, so a cluster can be refused with plenty of free memory.
- Order: availability first. The cluster is green and the failover capacity is met now (1,344 GB below 1,500 GB), so the check continues. Contention comes before capacity.
- Contention: nine of 180 VMs (5%) in one pool, Ready 14% to 18% with Run of 40% to 50%, and the pool limit (12 GHz) is below its demand (19 GHz). The cause is a limit, not a lack of cluster capacity: the other 171 VMs show no wait and utilization is 39%. Check resource pools and limits (configuration step); adding a host does not remove a limit. It is not a reason to refuse the new VMs.
- Options for the project: reserve what the VMs use, not the full 16 GB; power on in phases; or add a host. A fifth host adds 500 GB x 75% = 375 GB of reservable memory with 25% kept (more with a lower percentage).
- Turning HA admission control off would power all 12 on, but after a host failure HA restarts a VM only where its reservation fits, so reserved VMs are the first to stay down.

## Notes
- Public source: Cluster Resources Percentage Admission Control, vSphere 9.1 (TechDocs, updated 2026-11-09): memory failover capacity is (total host memory - total VM memory requirements) / total host memory, host memory from the root resource pool; reservation plus overhead of each powered-on VM; "If any check fails, admission control disallows the operation"; default reservation 0 MB. Resource pool CPU limit: vSphere 9.1 Resource Management.
- Why one answer: the arithmetic decides: 156 GB of headroom, 16.4 GB per VM, 9 fit and 10 do not. Same mechanism as question L2-10 and L3-57, here combined with the contention check.
- Debatable risk: low on the number. The overhead of 0.4 GB is given in the prompt so nobody has to estimate it. The "order" part is the design logic of the cluster health check (availability, then contention, then configuration, then capacity); the key does not require any particular recommendation to the project.
- Rests on: the vendor page above for the 9; the knowledge file's design logic (cluster-health-check, Order rationale: contention overrides utilization; step 4: resource pools and limits first; step 6: can it take more VMs) for the order.

## Metadata
```yaml
id: "0355"
title: "Can this cluster take 12 reserved VMs?"
product: [vsphere, vcf-operations]
technology: [memory, cpu, system]
task: decide-capacity
level: 400
answer_type: judged
input: [text]
object: [cluster, resource-pool, vm]
tool: [vcenter, vcf-operations]
knowledge:
  - vsphere/object-types/cluster/cluster-health-check
  - vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
  - vsphere/object-types/cluster/decision-tree/can-cluster-take-more-vms
  - vsphere/architecture/resource-controls
knowledge_main: vsphere/object-types/cluster/cluster-health-check
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
misconception_type: [consumption-as-contention]
status: draft
```
