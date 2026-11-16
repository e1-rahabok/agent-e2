# Patching one host of a five-host cluster

## Prompt
- vSphere 9.1. Cluster prod-cl05: 5 identical hosts (64 cores, 128 threads, 1 TB of memory each), VMFS datastores on a Fibre Channel array, no vSAN.
- DRS fully automated. vSphere HA on, admission control with the cluster resources percentage policy, 20% (one host).
- The team plans to patch esx-05 on Tuesday at 14:00, by putting it into maintenance mode and letting DRS evacuate it.
- vSphere Client, busiest hour of each of the last 7 working days (about 14:00), per host:

| Host | CPU Utilization (%) | Memory Consumed (% of host memory) |
|---|---|---|
| esx-01 | 66 | 73 |
| esx-02 | 64 | 70 |
| esx-03 | 68 | 74 |
| esx-04 | 65 | 71 |
| esx-05 | 67 | 72 |

- On esx-05:
  - lic-app-01 and lic-app-02 are in a VM-Host rule "Must run on hosts in group" whose host group holds esx-05 only (a licensing requirement).
  - nfv-fw-01 has a NIC attached as a Fixed DirectPath (PCI passthrough) device.
  - build-cache-01 has its only virtual disk on esx-05's local datastore.

Which statements are correct?

- A. At the busiest hour, the four hosts left would run at about 82-83% CPU utilization and 90% memory consumed.
- B. Each host runs at about two thirds of its capacity, so a third of the cluster is spare and any one host can leave without effect on the others.
- C. DRS leaves lic-app-01 and lic-app-02 on esx-05 under the required rule, so the host never completes entering maintenance mode.
- D. Maintenance mode takes precedence over VM-Host rules, so DRS evacuates the two licensed VMs with the other VMs.
- E. nfv-fw-01 has to be powered off for the window, or its device changed, because a Fixed DirectPath device blocks vMotion.
- F. During the evacuation DRS moves build-cache-01 together with its disk from the local datastore to a shared datastore.
- G. Turning vSphere HA off for the window is the documented way to keep admission control from stalling the evacuation.
- H. If a second host fails at the busiest hour, the three left would face about 110% of their CPU and 120% of their memory.
- I. Changing the rule to "Should run on hosts in group" for the window lets DRS move the two licensed VMs with the others.

## Likely wrong answer
B and D: "The cluster runs at two thirds, so a host can go, and DRS will move everything off it." G is the over-correction of turning HA off to get the evacuation through.

## Expected key points
- Answer: A, C, E, H, I.
- A is correct: the five hosts carry 66 + 64 + 68 + 65 + 67 = 330 points of CPU utilization and 73 + 70 + 74 + 71 + 72 = 360 points of memory consumed. Spread over four identical hosts: 330 / 4 = 82.5% and 360 / 4 = 90%. The hosts that stay carry the whole load.
- B is wrong: the misconception "the cluster is at 50%, so any host can go": the remaining hosts carry the whole load (5/4 of it each), and rules and pinned VMs decide too.
- C is correct: DRS never violates a required VM-Host rule, so it leaves those VMs on the host and maintenance mode does not complete.
- D is wrong: DRS does not evacuate VMs that a required rule binds to the host.
- E is correct: a Fixed DirectPath (PCI passthrough) device blocks vMotion, so the VM is powered off for the window or its device changed.
- F is wrong: DRS does not move a VM whose storage the other hosts cannot reach.
- G is wrong: the documented way through is to deactivate HA admission control temporarily so vMotion can proceed, and to turn it back on after; turning HA off removes restart protection for the whole cluster.
- H is correct: 330 / 3 = 110% CPU and 360 / 3 = 120% memory of the three hosts left, more than they hold: the window runs at a stated risk, which is the owner's decision.
- I is correct: the decision tree's way out for a pinned VM is to power it off for the window or change the rule to a preferential "should run on" rule, which DRS may break.

## Notes
- No option depends on the HA failover arithmetic during the window: with the percentage policy it depends on the VMs' reservations, which the prompt does not give.
- The CPU Utilization values are thread-based host readings; the arithmetic assumes the evacuated load spreads evenly over identical hosts, as the decision tree does in its step 4.
- vSphere 9.1 documentation: DirectPath and vMotion (pp. 993-994), Using VM-Host Affinity Rules (https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-1/vsphere-resource-management/using-drs-clusters-to-manage-resources/using-vm-host-affinity-rules.html), vSphere HA Admission Control (https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-1/vsphere-availability/creating-and-using-vsphere-ha-clusters/vsphere-ha-admission-control.html).

## Metadata
```yaml
id: "0465"
title: "Patching one host of a five-host cluster"
product: [vsphere]
technology: [system, cpu, memory]
task: decide-capacity
level: 400
answer_type: deterministic
input: [text]
object: [cluster, esxi, vm]
tool: [vcenter]
knowledge:
  - vsphere/object-types/cluster/decision-tree/can-cluster-take-a-host-out
knowledge_main: vsphere/object-types/cluster/decision-tree/can-cluster-take-a-host-out
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-15, question bank audit gap: vsphere/object-types/cluster/decision-tree/can-cluster-take-a-host-out"
answer: [A, C, E, H, I]
misconception: [B, D]
misconception_type: [unit-and-normalization]
status: draft
```
