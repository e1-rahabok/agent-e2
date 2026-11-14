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

## Likely wrong answer
E (or C): 40% is read as the failover capacity of two hosts out of five, with the host sizes ignored. Or B: the VMs without a reservation are counted as zero.

## Expected key points
- Answer: A.
- With a manual percentage, vSphere HA expects at least the share of the N largest hosts, N being Host Failures Cluster Tolerates. Here the two largest hosts are 100 + 60 = 160 GHz of 300 GHz, 53.3%. 40% is below it, and vSphere HA raises the Insufficient Failover Resources warning whatever the free resources (C and E are wrong).
- The current failover capacity is the total minus the CPU reservations, divided by the total. A VM without a CPU reservation counts 32 MHz: 250 x 32 MHz = 8 GHz. Reserved total is 158 GHz, so the current failover capacity is 142 / 300 = 47.3% (B ignores the 8 GHz).
- Admission control refuses a power-on that would take the current failover capacity below the configured percentage, not below the minimum. After the power-on, 182 GHz are counted and 118 / 300 = 39.3% is left, below the configured 40%. The same cluster would accept a VM that reserves 20 GHz (40.7% left), so D is wrong.
- The actual usage of 35% plays no role: admission control uses reservations, not consumption.

## Notes
- Public source: Cluster Resources Percentage Admission Control, vSphere 9.1 (Availability). https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-1/vsphere-availability/creating-and-using-vsphere-ha-clusters/vsphere-ha-admission-control/cluster-resources-percentage-admission-control.html . Page last updated 2026-11-09. It gives the current failover capacity (total minus the VMs' requirements, divided by the total), the minimum as the combined capacity of the N largest hosts divided by the cluster total, the warning "regardless of available free resources", and the default of 32 MHz CPU and 0 MB memory for a VM without a reservation. vSphere HA Admission Control, vSphere 9.1 (https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-1/vsphere-availability/creating-and-using-vsphere-ha-clusters/vsphere-ha-admission-control.html, last updated 2026-11-09): any action that might violate the failover constraints, powering on a VM among them, is not permitted; actual memory consumed is not considered.
- Why one answer: the minimum, the 32 MHz default and the power-on check against the configured value are all in the vendor text; 53.3%, 47.3% and 39.3% follow from the prompt. Without the 32 MHz default the 24 GHz VM would leave 42% and be accepted, so that default decides the power-on result.
- Debatable risk: the power-on test is stated by the admission control overview ("any action that might violate these constraints is not permitted"); the page does not print the exact formula for a power-on, so the question uses the failover capacity formula after the VM's reservation is added. Memory is excluded on purpose; the 9.1 page notes the memory computation has its own rules for clusters with Memory Tiering, not used here.
- This is a mechanism the cluster health check relies on when it reads "HA failover capacity met"; the question uses no health-check order.
- Rewritten 2026-11-13 to raise difficulty: five uneven hosts and two failures instead of four hosts and one; a power-on whose result depends on the 32 MHz default of unreserved VMs; the warning (minimum) and the power-on check (configured value) are two separate tests that give different numbers.
- Stem made plural (2026-11-14): the singular form told the candidate that one option is correct (Q199: the count is never disclosed). Was: "Which statement is correct?"

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
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
answer: [A]
misconception: [C, E]
misconception_type: [threshold-transplanted]
status: draft
```
