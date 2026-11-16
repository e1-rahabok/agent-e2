# vCLS Retreat Mode on a vCenter 9.1 cluster

## Prompt
- vCenter 9.1. Cluster reg-cl01: 6 hosts, all on ESXi 9.1, DRS fully automated, vSphere HA on with admission control.
- The security team wants the vCLS VMs gone from this regulated cluster and asks to switch the cluster to Retreat Mode.
- The change board raises two objections:
  - "The vSphere 9.1 Fault Tolerance pages carry a note that DRS depends on the vCLS VMs. Without them DRS stops and HA restarts are at risk."
  - "The vCLS VMs hold reservations, so the capacity report must subtract them from usable capacity, like the HA failover host."
- An engineer points to Broadcom KB 312147, updated for vCenter 9.0: it deprecates vCLS and recommends switching clusters to Retreat Mode.

Which statements are correct?

- A. On vCenter 9.1, DRS keeps balancing and HA keeps restarting VMs after Retreat Mode deletes the vCLS VMs.
- B. The Fault Tolerance note is text kept from the 7.0 Update 1 era; the KB update for vCenter 9.0 overrides it.
- C. Retreat Mode never touched any cluster service, before vCenter 9.0 either; the 9.0 KB update only restated that.
- D. With every host on ESXi 9.1, the cluster runs Embedded vCLS: at most two vCLS VMs, with no virtual disk on a datastore.
- E. The vCLS VMs of this cluster reserve no more than about 200 MHz of CPU and 400 MB of memory in total.
- F. The vCLS reservations are a capacity cost of the same order as a failover host and belong in the report next to it.
- G. Embedded vCLS needs every host of the cluster on ESXi 8.0 Update 3 or later; one older host keeps the cluster on External vCLS.
- H. Retreat Mode is one vCenter-wide setting: it removes the vCLS VMs from every cluster of the vCenter at once.

## Likely wrong answer
F: "The vCLS VMs hold reservations, so they are a real capacity cost, like a failover host." C misreads the KB update as a restatement instead of a change.

## Expected key points
- Answer: A, B, D, E.
- A is correct: KB 312147 states that from vCenter 9.0 deactivating vCLS does not impact DRS or HA; the recommendation to switch to Retreat Mode follows from it.
- B is correct: the Fault Tolerance note (DRS depends on the vCLS VMs since 7.0 Update 1) is older text kept in the 9.1 documentation; KB 312147 says its 9.0 update overrides earlier statements about the dependency. Performance Best Practices 9.1 no longer carries the vCLS dependency that the 9.0 edition stated.
- C is wrong: before vCenter 9.0, Retreat Mode affected some cluster services; the 9.0 update is what ended the dependency.
- D is correct: Embedded vCLS replaces External vCLS when vCenter is 8.0 Update 3 or later and at least one host runs ESXi 8.0 Update 3 or later; Embedded vCLS runs at most 2 VMs and has no disk on a datastore.
- E is correct: Embedded vCLS reserves about 400 MB and 200 MHz per cluster (100 MHz and 160 MB per VM, two VMs).
- F is wrong: a 6-host cluster's failover host is a whole host of cores and memory; the vCLS reservations are a few hundred MHz and MB.
- G is wrong: Embedded vCLS replaces External vCLS when vCenter is 8.0 Update 3 or later and at least one host of the cluster runs ESXi 8.0 Update 3 or later, not every host.
- H is wrong: Retreat Mode is set per cluster (Configure > vSphere Cluster Services > General > Edit vCLS Mode).

## Notes
- The prompt carries the vendor evidence on both sides (the 9.1 Fault Tolerance note and KB 312147), so the conflict between the knowledge base and the 9.1 documentation is decidable from public documents (benchmark/design.md, sections 3.7 and 6.1 F3).
- misconception_type: the dependency statement of an older release (7.0 Update 1) applied to 9.1; the closest listed type is threshold-transplanted.
- Not tested: the vCLS default state in vCenter 9.1 (open review note of the knowledge file).
- Sources: Broadcom KB 312147, https://knowledge.broadcom.com/external/article/312147; KB 316514 (Retreat Mode per cluster), https://knowledge.broadcom.com/external/article/316514.

## Metadata
```yaml
id: "0464"
title: "vCLS Retreat Mode on a vCenter 9.1 cluster"
product: [vsphere]
technology: [system]
task: judge-setting
level: 300
answer_type: deterministic
input: [text]
object: [cluster, vm]
tool: [vcenter]
knowledge:
  - vsphere/object-types/cluster/concepts/vcls
knowledge_main: vsphere/object-types/cluster/concepts/vcls
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-15, question bank audit gap: vsphere/object-types/cluster/concepts/vcls"
answer: [A, B, D, E]
misconception: [C, F, G]
misconception_type: [threshold-transplanted]
status: draft
```
