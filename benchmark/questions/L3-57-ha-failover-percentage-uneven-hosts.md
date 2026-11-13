# HA failover percentage on uneven hosts

## Prompt
- A vSphere 9.1 cluster has 4 ESXi hosts. Three hosts have 60 GHz of CPU each, and one host has 120 GHz. The cluster total is 300 GHz.
- vSphere HA admission control uses the Cluster Resources Percentage policy. Host Failures Cluster Tolerates is 1.
- The administrator switched the policy from automatic to manual and typed 25% for CPU: one host out of four.
- The cluster is lightly loaded: the VMs reserve 30 GHz of CPU in total and use less than 25% of the cluster.

Which statement is correct?

- A. 25% is enough: the cluster tolerates one failed host out of four, and the load is far below 75% of the cluster.
- B. The minimum CPU percentage is 20%, the share of the smallest host (60 of 300 GHz), so 25% is above the minimum.
- C. The minimum CPU percentage is 40%, the share of the largest host (120 of 300 GHz). Below it, vSphere HA raises an Insufficient Failover Resources warning, whatever the free resources.
- D. The minimum CPU percentage is 40%, but the warning appears only when the unreserved CPU of the cluster falls below 40%.
- E. A manual percentage has no minimum: vSphere HA checks it only when a VM powers on, against the free resources at that moment.

## Likely wrong answer
A: one host of four is 25%, so 25% is read as the failover capacity of one host, with the host sizes ignored.

## Expected key points
- Answer: C.
- With a manual percentage, vSphere HA expects at least the share of the N largest hosts in the cluster, where N is Host Failures Cluster Tolerates. Here N = 1: the largest host is 120 GHz of 300 GHz, 40%.
- 25% of 300 GHz is 75 GHz. The largest host is 120 GHz, so the reserved failover capacity cannot cover its loss.
- Below the minimum, vSphere HA raises the Insufficient Failover Resources warning regardless of the free resources, so a lightly loaded cluster does not remove it (D and E are wrong).
- A is wrong: the failover level is counted in hosts, but the capacity lost depends on which host fails. B is wrong: the smallest host is not the one to cover.

## Notes
- Public source: Cluster Resources Percentage Admission Control, vSphere 9.1 (Availability). https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-1/vsphere-availability/creating-and-using-vsphere-ha-clusters/vsphere-ha-admission-control/cluster-resources-percentage-admission-control.html . Page last updated 2026-11-09. It states the minimum as the sum of the N largest hosts divided by the cluster total, and the warning "regardless of available free resources".
- Why one answer: the documentation gives the formula for the minimum and says the warning does not depend on free resources; 120 / 300 = 40% follows from the prompt.
- Debatable risk: none on the rule. Whether 40% is the best design is not asked; the question asks only what the documented minimum is and when the warning shows. Auto mode is outside the question (the prompt says manual). CPU only; the memory minimum is computed the same way.
- This is a mechanism the cluster health check relies on when it reads "HA failover capacity met"; the question uses no health-check order.

## Metadata
```yaml
id: "0330"
title: "HA failover percentage on uneven hosts"
product: [vsphere]
technology: [system, cpu]
task: judge-setting
level: 300
answer_type: deterministic
input: [text]
object: [cluster, esxi]
tool: [vcenter]
knowledge:
  - vsphere/object-types/cluster/cluster-health-check
  - vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
knowledge_main: vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
answer: [C]
misconception: [A]
misconception_type: [threshold-transplanted]
status: draft
```
