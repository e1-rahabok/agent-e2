# HA failover percentage on uneven hosts

## Prompt
- A vSphere 9.1 cluster has 5 ESXi hosts with 40, 40, 60, 60 and 100 GHz of CPU. The cluster total is 300 GHz. Memory is plentiful and is not a constraint.
- vSphere HA admission control uses the Cluster Resources Percentage policy. Host Failures Cluster Tolerates is 2.
- The administrator switched the policy from automatic to manual and typed 40% for CPU: two hosts out of five.
- The powered-on VMs with a CPU reservation reserve 150 GHz in total. 250 other powered-on VMs have no CPU reservation. The cluster uses about 35% of its CPU.
- A VM with 12 vCPUs and a CPU reservation of 24 GHz is powered on.

Which statements are correct?

- A. The Insufficient Failover Resources warning is shown, because 40% is below the 53.3% minimum for two failures. The power-on is refused, because the failover capacity left after it, about 39.3%, is below the configured 40%.
- B. The Insufficient Failover Resources warning is shown, because 40% is below the 53.3% minimum for two failures. The power-on succeeds, because the VMs without a reservation count nothing and the failover capacity left is about 42%.
- C. No warning is shown, because 40% is two hosts out of five. The power-on is refused, because the failover capacity left after it, about 39.3%, is below the configured 40%.
- D. The Insufficient Failover Resources warning is shown, because 40% is below the 53.3% minimum for two failures. The power-on is refused, because vSphere HA enforces the 53.3% minimum and the cluster has only 47.3% of failover capacity now.
- E. No warning is shown, because 40% is two hosts out of five. The power-on succeeds, because 24 GHz is 8% of the cluster and 47.3% of the CPU is still unreserved.

## Answers
A

## Explanation
- A is correct: with a manual percentage, vSphere HA expects at least the share of the N largest hosts (N = Host Failures Cluster Tolerates): 100 + 60 = 160 of 300 GHz, 53.3%, so 40% raises the Insufficient Failover Resources warning. A VM without a CPU reservation counts 32 MHz: 250 x 32 MHz = 8 GHz, so 158 GHz are counted now (47.3% left) and 182 GHz after the power-on, leaving 118 / 300 = 39.3%, below the configured 40%: refused.
- B is wrong: it counts the 250 unreserved VMs as zero; with their 8 GHz the capacity left is 39.3%, not 42%.
- C is wrong: 40% is two hosts out of five only for equal hosts; the reserve is sized on the largest hosts, so the warning is shown.
- D is wrong: the power-on is tested against the configured 40%, not the 53.3% minimum; the same cluster would accept a VM that reserves 20 GHz (40.7% left).
- E is wrong: the warning is shown (as in C), and admission control counts reservations, not the 35% usage: 39.3% would be left, below 40%.
- Misconception: E (or C): 40% is read as the failover capacity of two hosts out of five, with the host sizes ignored. Or B: the VMs without a reservation are counted as zero.

## Notes
- Deferred 2026-11-16 (question bank audit): from the knowledge base alone options A and B cannot be told apart; the key needs three vendor facts the knowledge base does not hold (the 32 MHz CPU default for VMs with no reservation, the warning for a manual percentage below the largest hosts' share, the power-on test against the configured value). Runs again once admission-control-and-cluster-state states them (author question Q-E2-244).
- Synthetic, 2026-11-13, for the coverage gap (project/plan.md).
- The key rests on three vendor facts the knowledge base does not hold yet: the 32 MHz CPU (0 MB memory) default for a powered-on VM without a reservation, the Insufficient Failover Resources warning when the manual percentage is below the share of the N largest hosts, and the power-on test against the configured value. Source: vSphere 9.1 documentation, vSphere Availability, Cluster Resources Percentage Admission Control, Computing the Current Available Capacity (VMware vSphere 9.1 PDF, build of 2026-11-02, p. 1971; online https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-1/vsphere-availability/creating-and-using-vsphere-ha-clusters/vsphere-ha-admission-control/cluster-resources-percentage-admission-control.html, last updated 2026-11-09). The knowledge-base line "A VM with no reservation passes CPU and memory admission control" reads toward B until the 32 MHz default is added to admission-control-and-cluster-state.
- vSphere HA Admission Control, vSphere 9.1 (https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-1/vsphere-availability/creating-and-using-vsphere-ha-clusters/vsphere-ha-admission-control.html): any action that might violate the failover constraints, powering on a VM among them, is not permitted; actual memory consumed is not considered.
- Debatable risk: the page does not print the exact formula for a power-on, so the question uses the failover capacity formula after the VM's reservation is added. Memory is excluded on purpose; the 9.1 page notes the memory computation has its own rules for clusters with Memory Tiering, not used here.
- Each option joins a warning half and a power-on half; splitting them into single facts waits until the knowledge base holds the three facts above (the key stays A).

## Metadata
```yaml
id: "0330"
title: "HA failover percentage on uneven hosts"
product: [vsphere]
technology: [system, cpu]
task: judge-setting
level: 400
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
source_path: "Synthetic, 2026-11-13"
misconception: [C, E]
misconception_type: [threshold-transplanted]
status: deferred
```
