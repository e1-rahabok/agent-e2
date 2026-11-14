# Why VM, datastore and host totals differ

## Prompt
- Cluster PROD-B has 8 hosts and 240 VMs. Its 12 VMFS datastores are also mounted by the 6 hosts of cluster PROD-C.
- For one hour, you add up the virtual disk IOPS of all VMs in PROD-B.
- The total differs from the sum of the datastore IOPS, and from the sum of the IOPS of the 8 hosts.

Which statements are correct?

- A. A VM's IO to a virtual disk on a datastore outside the 12, such as a local datastore, is in the VM sum but not in the sum of the 12 datastores.
- B. IO from the PROD-C hosts to the 12 datastores is in the datastore sum but in neither PROD-B sum.
- C. One of the three sums must be wrong, since the same IO is counted in each.
- D. Snapshot IO adds to the datastore sum and not to the VMs' virtual disk sum.
- E. RDM IO adds to the VMs' virtual disk sum and not to the datastore sum.
- F. A gap between one VM's virtual disk read IOPS and its datastore read IOPS cannot point to anything on that VM.
- G. Open a support case to have the vCenter statistics collection checked.

## Likely wrong answer
C: concluding that a metric is broken.

## Expected key points
- Answer: A, B, D, E.
- A is true: a VM's IO on a datastore outside the 12 (a local datastore, another shared one) counts for the VM, not for the 12.
- B is true: the hosts of PROD-C add IO to the 12 datastores that is in neither the PROD-B VM sum nor the PROD-B host sum.
- C is false: the relationships are many-to-many (a VM spans datastores, a datastore holds many VMs and is mounted by hosts of more than one cluster), so totals across VM, datastore, host and cluster do not reconcile, and each value is still correct from its vantage point.
- D is true: virtual disk counters exclude snapshot IO; datastore counters include it.
- E is true: virtual disk counters cover VMDKs and RDMs; datastore counters exclude RDMs, whose data is on their own LUNs.
- F is false: the gap has known causes that tell something; for example a datastore read IOPS consistently above the virtual disk read IOPS on VMFS points to a snapshot on that VM.
- G is false: a gap between vantage points is expected and is no fault of the statistics collection.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Revised 2026-11-12 for question set 1.0: shared datastores stated in the stem. Counts only after author approval.
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): "virtual disk IOPS" in the stem; the vague option "each sum is correct from its vantage point" replaced by single mechanisms (snapshot IO, RDM IO); over-correction F and wrong action G added. Key changed from A, B, D to A, B, D, E.

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
  - vsphere/technology/storage/metrics/virtual-motherboard/virtual-disk
  - vsphere/technology/storage/metrics/virtual-motherboard/datastore
knowledge_main: vsphere/architecture/object-relationships
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
answer: [A, B, D, E]
misconception: [C]
misconception_type: [same-name-other-object]
pair: "0417"
status: draft
```
