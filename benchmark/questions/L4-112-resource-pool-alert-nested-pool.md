# Resource pool alert and a nested pool

## Prompt
- VCF Operations. A cluster of 8 hosts runs 300 VMs. The resource pool Prod holds 10 VMs directly and contains a nested resource pool, Prod-DB, with 30 VMs. All other pools are outside this case.
- The alert definition "Resource pool CPU contention" has the Resource Pool as base object, one symptom set Defined on Child (Virtual Machine), value type Percent, operator ">", value 25, and the conditions combined with All. Red: the highest 20-second vCPU Ready of the VM in the 5-minute cycle is above 24% and the CPU Contention (%) of the cycle is above 6%. Wait cycle 1. The definition is enabled for every pool, Prod and Prod-DB included.
- In the current cycle, 21 of the 30 VMs in Prod-DB meet both red conditions (typically 30% highest Ready, 8% Contention). In Prod, 2 of the 10 directly held VMs meet both red conditions. The other VMs are quiet.
- DRS is on and the hosts are not over their own limits: only the VMs of Prod-DB are hit, and they run on several hosts.

Which statement about the red alerts of the resource pools is correct?

- A. Prod-DB goes red: 21 of its 30 VMs is 70%. Prod stays quiet: its set reads the VMs held directly by Prod, 2 of 10 is 20%, and the VMs of Prod-DB are not its children.
- B. Both go red: Prod holds 40 VMs including the nested pool, and 23 of 40 is 57.5%, over 25%.
- C. Neither goes red: the 25% is measured against all 300 VMs of the cluster, and 23 of 300 is 7.7%.
- D. Only Prod goes red: a parent pool reports the contention of everything below it, and the alert of the nested pool is merged into it.
- E. Prod-DB goes red and Prod goes orange: the 2 hit VMs of Prod also meet the lower orange values, which take the nested VMs into account.

## Likely wrong answer
B: a pool is assumed to include the VMs of the pools inside it, as in the resource allocation tree. The share is then 57.5% and the parent goes red too.

## Expected key points
- Answer: A.
- Child is one level below the base object. The VMs of Prod-DB are children of Prod-DB, not of Prod. The population of Prod is only its 10 directly held VMs: 2 of 10 = 20%, not over 25%, so Prod stays quiet.
- Prod-DB: 21 of 30 = 70%, over 25%, with both conditions met by the same VMs, so it goes red.
- The shares are never a share of the cluster (C), and they do not roll up through the nesting (B, D, E). A relationship defined on Descendant would reach the nested VMs, but the alert is built on Child.
- A pool alert therefore does not work with nested pools: a hit in the inner pool is invisible at the outer pool. The infrastructure team still sees the same VMs through the ESXi and cluster contention alerts (the VMs are also children of their hosts), and a pool inside a pool complicates operations.

## Notes
- Public source: VMware Aria Operations 8.18, "Creating Alert Definitions" (https://techdocs.broadcom.com/us/en/vmware-cis/aria/aria-operations/8-18/vmware-aria-operations-configuration-guide-8-18/configuring-alerts-and-actions/alert-definitions/creating-alert-definitions.html), last updated 2026-05-20: Child is "an object type that is one level below the base object type"; Descendant is at any level below; Percent is the percentage of the total related objects. vSphere API ResourcePool: the pool's vm property is the set of VMs associated with that pool, and a pool is subdivided by child pools (https://developer.broadcom.com/xapis/vsan-management-api/8.0u3/vim.ResourcePool.html).
- Knowledge file logic: vsphere/object-types/resource-pool/resource-pool-alerts, sections "Resource pool CPU contention" (does not work with nested pools) and "Coverage and receivers" (a share of the pool's VMs); catalog thresholds-alerts.yaml, alert-resource-pool-cpu-contention-red (population over 25%, relation child, VirtualMachine).
- Why one answer: Child is defined by the vendor as one level, and the VM-to-pool membership is one pool per VM, so the outer pool's population is its direct VMs only.
- Debatable risk: I could not find a VCF Operations page that lists the exact relationships of a Resource Pool object to its VMs and nested pools. The prompt states the set as Defined on Child, and the answer rests on the vendor definition of Child plus the knowledge file's statement that the condition does not work with nested pools. The author should confirm on a VCF Operations 9.1 instance that the nested pool's VMs are not children of the outer pool.

## Metadata
```yaml
id: "0340"
title: "Resource pool alert and a nested pool"
product: [vcf-operations, vsphere]
technology: [cpu, system]
task: judge-setting
level: 400
answer_type: deterministic
input: [text]
object: [resource-pool, vm]
tool: [vcf-operations]
knowledge:
  - vsphere/object-types/resource-pool/resource-pool-alerts
  - vsphere/object-types/resource-pool/resource-pool-design
  - vcf-operations/alert-definitions
knowledge_main: vsphere/object-types/resource-pool/resource-pool-alerts
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
answer: [A]
misconception: [B]
misconception_type: [average-hides-worst]
status: draft
```
