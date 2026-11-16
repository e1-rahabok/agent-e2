# Resource pool alert and a nested pool

## Prompt
- VCF Operations. A cluster of 8 hosts runs 300 VMs. The resource pool Prod holds 10 VMs directly and contains a nested resource pool, Prod-DB, with 30 VMs. All other pools are outside this case.
- The alert definition "Resource pool CPU contention" has the Resource Pool as base object, one symptom set Defined on Child (Virtual Machine), value type Percent, operator ">", value 25, and the conditions combined with All. Red: the highest 20-second vCPU Ready of the VM in the 5-minute cycle is above 24% and the CPU Contention (%) of the cycle is above 6%. Wait cycle 1. The definition is enabled for every pool, Prod and Prod-DB included.
- In the current cycle, 21 of the 30 VMs in Prod-DB meet both red conditions (typically 30% highest Ready, 8% Contention). In Prod, 2 of the 10 directly held VMs meet both red conditions. The other VMs are quiet.
- DRS is on and the hosts are not over their own limits: the hit VMs are in Prod and Prod-DB only, and they run on several hosts.

Which statements about the red alerts of the resource pools are correct?

- A. Prod-DB goes red with 21 of its 30 VMs; Prod stays quiet with 2 of the 10 VMs it holds directly.
- B. Both go red: Prod holds 40 VMs including the nested pool, and 23 of 40 is 57.5%, over 25%.
- C. Neither goes red: the 25% is measured against all 300 VMs of the cluster, and 23 of 300 is 7.7%.
- D. Only Prod goes red: a parent pool reports the contention of everything below it, and the alert of the nested pool is merged into it.
- E. Prod-DB goes red and Prod goes orange: the 2 hit VMs of Prod also meet the lower orange values, which take the nested VMs into account.

## Likely wrong answer
B: a pool is assumed to include the VMs of the pools inside it, as in the resource allocation tree. The share is then 57.5% and the parent goes red too.

## Expected key points
- Answer: A.
- A is correct: Child is one level below the base object, so the VMs of Prod-DB are children of Prod-DB, not of Prod. Prod-DB: 21 of 30 = 70%, over 25%, with both conditions met by the same VMs: red. Prod: only its 10 directly held VMs count, 2 of 10 = 20%: quiet.
- B is wrong: the share does not roll up through the nesting; Prod's population is its own 10 VMs, not 40. A set defined on Descendant would reach the nested VMs, but the alert is built on Child.
- C is wrong: the share is of the pool's own VMs, never of the cluster's VMs.
- D is wrong: a parent pool does not report the contention of the pools below it, and no alert is merged upward; a pool alert does not work with nested pools.
- E is wrong: the orange values use the same child population; 2 of 10 = 20% is under 25%, so Prod gets no orange alert either.

## Notes
- Public source: VMware Aria Operations 8.18, "Creating Alert Definitions" (https://techdocs.broadcom.com/us/en/vmware-cis/aria/aria-operations/8-18/vmware-aria-operations-configuration-guide-8-18/configuring-alerts-and-actions/alert-definitions/creating-alert-definitions.html), last updated 2026-05-20: Child is "an object type that is one level below the base object type"; Descendant is at any level below; Percent is the percentage of the total related objects. vSphere API ResourcePool: the pool's vm property is the set of VMs associated with that pool, and a pool is subdivided by child pools (https://developer.broadcom.com/xapis/vsan-management-api/8.0u3/vim.ResourcePool.html).
- Knowledge file logic: vsphere/object-types/resource-pool/resource-pool-alerts, sections "Resource pool CPU contention" (does not work with nested pools) and "Coverage and receivers" (a share of the pool's VMs); catalog thresholds-alerts.yaml, alert-resource-pool-cpu-contention-red (population over 25%, relation child, VirtualMachine).
- The infrastructure team still sees the nested VMs through the ESXi and cluster contention alerts (the VMs are also children of their hosts).
- Open: no VCF Operations page found that lists the relationships of a Resource Pool object to its VMs and nested pools. The key rests on the vendor definition of Child and on resource-pool-alerts ("does not work with nested resource pools"); confirm on a VCF Operations 9.1 instance that the nested pool's VMs are not children of the outer pool. vcf-operations/alert-definitions does not define Child and Descendant yet.
- Synthetic, 2026-11-13, for the coverage gap (project/plan.md).
- 2026-11-15 audit: the stem no longer contradicts itself (it said only Prod-DB VMs are hit, next to 2 hit VMs in Prod); A shortened (it was the longest option and the only one with the mechanism).

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
source_path: "Synthetic, 2026-11-13"
answer: [A]
misconception: [B]
misconception_type: [average-hides-worst]
status: draft
```
