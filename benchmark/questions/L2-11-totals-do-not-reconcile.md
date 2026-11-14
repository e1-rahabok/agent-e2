# Why VM, datastore and host totals differ

## Prompt
- Cluster PROD-B has 8 hosts and 240 VMs. Its 12 VMFS datastores are also mounted by the 6 hosts of cluster PROD-C.
- For one hour, you add up the disk IOPS of all VMs in PROD-B.
- The total differs from the sum of the datastore IOPS, and from the sum of the IOPS of the 8 hosts.

Why? Choose all the correct statements.

- A. Some VMs also have virtual disks on datastores outside the 12, such as a local datastore.
- B. The 12 datastores also carry IO from the hosts and VMs of cluster PROD-C.
- C. One of the three sums must be wrong, since the same IO is counted in each.
- D. Each of the three sums is correct from its own vantage point.

## Likely wrong answer
C: concluding that a metric is broken.

## Expected key points
- Answer: A, B, D.
- A: a VM's IO on a datastore outside the 12 (a local datastore, another shared one) is in the VM sum and the host sum, not in the sum of the 12.
- B: hosts of PROD-C add IO to the 12 datastores that is in neither the PROD-B VM sum nor the PROD-B host sum.
- The relationships are many-to-many: a VM spans datastores, a datastore holds many VMs, and a datastore is mounted by hosts of more than one cluster.
- So totals across VM, datastore, host and cluster do not reconcile, and each value is still correct from its vantage point.
- C is wrong: a gap between vantage points is expected.
- Snapshots also add datastore IO that virtual disk counters exclude: another reason for a gap.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Revised 2026-11-12 for question set 1.0: shared datastores stated in the stem. Counts only after author approval.

## Metadata
```yaml
id: "0049"
title: "Why VM, datastore and host totals differ"
product: [vsphere]
technology: [system, storage]
task: explain-mechanism
level: 200
answer_type: deterministic
input: [text]
object: [vm, datastore, esxi, cluster]
tool: [vcenter]
knowledge:
  - vsphere/architecture/object-relationships
  - vsphere/technology/storage/concepts/storage-layers
  - vsphere/technology/storage/concepts/snapshot-impact
knowledge_main: vsphere/architecture/object-relationships
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
answer: [A, B, D]
misconception: [C]
misconception_type: [same-name-other-object]
status: draft
```
