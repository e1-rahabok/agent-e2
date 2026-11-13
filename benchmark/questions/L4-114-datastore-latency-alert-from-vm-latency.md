# Datastore latency alert built from VM latency

## Prompt
- VCF Operations. Two datastores serve the same VMs in a different way: DS-FAST (all-flash) holds the OS disk of 40 VMs, DS-SLOW (nearline) holds the data disk of 20 VMs. 18 of the 20 VMs have their OS disk on DS-FAST and their data disk on DS-SLOW.
- The storage team builds a first "datastore latency" alert with one symptom set on the VMs of the datastore (Child relationship): more than 25% of the VMs have VM disk latency above 10 ms, wait cycle 1.
- Measured in the same 5-minute cycle:
  - DS-SLOW: latency of the datastore 22 ms. 19 of its 20 VMs report VM disk latency above 10 ms.
  - DS-FAST: latency of the datastore 1.5 ms. 18 of its 40 VMs report VM disk latency above 10 ms (the 18 that also use DS-SLOW). The highest VM disk latency among them is 55 ms.
- The alert goes red on both datastores. The storage team accepts the alert on DS-SLOW, and rejects the one on DS-FAST as a false alarm. DS-FAST also serves 22 VMs that have no disk on DS-SLOW and have latency below 2 ms.

Which change removes the false alarm on DS-FAST in a way that keeps working when VMs move or disks are added?

- A. Add a condition on the latency of the datastore itself (above 5 ms) next to the VM conditions, because a VM's latency covers all its disks and the datastore's own counter is the only value that belongs to one datastore.
- B. Raise the share of VMs from 25% to 50%, because 45% of the VMs of DS-FAST falls under it and 95% of the VMs of DS-SLOW stays over it.
- C. Add a condition on the highest VM disk latency in the population (above 40 ms), because it separates a datastore with a slow tail from one with only a mild average.
- D. Lengthen the wait from 1 to 3 cycles, because only a datastore with persistent latency should alert and a spike on DS-FAST is not persistent.
- E. Lower the VM disk latency value from 10 ms to 5 ms, because a stricter VM value gives the alert more weight on the datastore that is truly slow.

## Likely wrong answer
B (a higher share) or C (a peak condition on the VMs): both keep the VM figure as the evidence, though a VM and a datastore are many-to-many and the VM figure cannot say which datastore is slow.

## Expected key points
- Answer: A.
- VMs and datastores are many-to-many. A VM with disks on two datastores has one VM-level latency value that mixes both. The 18 VMs of DS-FAST that report over 10 ms are slow because of their data disk on DS-SLOW, not because of DS-FAST.
- The latency of the datastore (1.5 ms on DS-FAST, 22 ms on DS-SLOW) is measured on that datastore only. As an extra condition, above 5 ms, it removes DS-FAST and keeps DS-SLOW.
- C does not work here: DS-FAST has VMs at 55 ms (the ones using DS-SLOW), so the highest-VM condition passes on DS-FAST as well.
- B works only by luck of the numbers (45% against 50%): three more VMs with a data disk on DS-SLOW and it alerts again. The VM population stays the wrong measuring point.
- D is wrong because the cause is persistent, not a spike: the same 18 VMs stay slow. E makes the false alarm more likely.
- For this reason a datastore latency alert is not implemented as a plain VM-population alert. Guide if one is built: all of a share of VMs over 10 ms, a highest VM latency over 40 ms, and the datastore's own latency over 5 ms.

## Notes
- Public source: the many-to-many relation is vSphere itself: a virtual disk lives on one datastore, a VM can have disks on several, so a VM-level disk latency counter averages across its disks (vSphere Monitoring and Performance, "Virtual Machine Disk Performance" counters, Broadcom TechDocs, vSphere 9.0; VCF Operations 9.1 VM metrics Disk | Total Latency). The datastore-level latency is a counter of the datastore object. I did not find one vendor page that states the sentence "a VM-level latency cannot be assigned to a datastore", so the answer rests on the knowledge file's design logic and on the metric definitions.
- Knowledge file logic: vsphere/object-types/datastore/datastore-alerts, section "Datastore latency: not implemented": VMs and datastores are many-to-many, so a VM-level condition cannot be set for a datastore; guide values (more than 25% of VMs above 10 ms, highest VM above 40 ms, datastore above 5 ms).
- Why one answer: only the datastore's own latency is measured on one datastore; the numbers (45% against 25%, 55 ms against 40 ms) show that the two VM-based conditions pass on DS-FAST.
- Debatable risk: a reader could argue that per-virtual-disk counters (instances) would map disks to datastores. The prompt gives only the VM-level value the alert reads. B passes this case by chance, but fails the "keeps working" clause. The guide values (10, 40, 5 ms) are the author's design; the question uses only the 5 ms condition as the mechanism and does not ask for the number.

## Metadata
```yaml
id: "0342"
title: "Datastore latency alert built from VM latency"
product: [vcf-operations, vsphere]
technology: [storage, system]
task: judge-setting
level: 400
answer_type: deterministic
input: [text]
object: [datastore, vm]
tool: [vcf-operations]
knowledge:
  - vsphere/object-types/datastore/datastore-alerts
  - vsphere/object-types/vm/vm-alerts
  - vsphere/technology/storage/metrics/host/datastore
knowledge_main: vsphere/object-types/datastore/datastore-alerts
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
answer: [A]
misconception: [B, C]
misconception_type: [same-name-other-object, average-hides-worst]
status: draft
```
