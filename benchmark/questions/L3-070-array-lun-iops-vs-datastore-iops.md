# Array LUN IOPS against datastore IOPS

## Prompt
- A VMFS datastore sits on one LUN of an FC array and is mounted by the 8 hosts of one cluster. No other datastore uses the LUN.
- The storage team compares, hour by hour, the IOPS the array reports for the LUN with the datastore IOPS in vCenter.

Which statements are correct?

- A. The vCenter datastore IOPS count only the IO that the hosts in this vCenter send to the datastore.
- B. The array counts every IO on the LUN: from every initiator, and from its own jobs such as replication.
- C. Both count the same IO here, so a higher array number shows that vCenter under-reports.
- D. Array IOPS and vCenter IOPS cannot be compared, even with one datastore on one LUN.
- E. With 3,000 IOPS on the LUN and 2,000 on the datastore, about 1,000 IOPS come from initiators or array jobs outside vCenter.
- F. A backup proxy that reads the LUN directly over the SAN adds IO that the array counts and vCenter does not.
- G. VM snapshot IO is the usual reason the array counts more IO than vCenter.
- H. When the array shows more IOPS than vCenter, lower the IO of the VMs on the datastore.

## Likely wrong answer
C: the datastore and its only LUN see the same IO, so vCenter must under-report.

## Expected key points
- Answer: A, B, E, F.
- A true: vCenter sees only its own hosts; a host of another vCenter or a non-ESXi initiator is invisible to it.
- B true: the array counts the LUN's IO from every initiator and from its own jobs (replication, array snapshots, rebuilds).
- C false: the misconception. The array counts every initiator and its own jobs; vCenter counts only its hosts. Each is right from its vantage point.
- D false: with a 1:1 mapping the ratio LUN IOPS / datastore IOPS is the check, and 1 is the expected value.
- E true: with a 1:1 mapping, LUN IOPS minus datastore IOPS is IO that no host in vCenter sends; the ratio here is 1.5.
- F true: a SAN-mode backup proxy is another initiator on the LUN.
- G false: VM snapshot IO passes through the hosts and is counted in the datastore metrics, which include every file on the datastore; it cannot open a gap to the array. The gap is another initiator or the array's own jobs.
- H false: the extra IO is not the VMs' IO; find the other initiator or array job with the storage team.

## Notes
- Theory half of the pair with 0188 (practical; design.md, section 3.9). Different situation and numbers from 0188.
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item B10 (origin: synthetic). Counts only after author approval.
- Review 2026-11-15: C, E and G reworded away from 0188 (G now names snapshots as the supposed usual reason). Key unchanged: A, B, E, F.

## Metadata
```yaml
id: "0408"
title: "Array LUN IOPS against datastore IOPS"
product: [vsphere]
technology: [storage]
task: explain-mechanism
level: 300
answer_type: deterministic
input: [text]
object: [datastore]
tool: [vcenter]
knowledge:
  - vsphere/technology/storage/concepts/storage-layers
  - vsphere/architecture/object-relationships
  - vsphere/technology/storage/concepts/snapshot-impact
knowledge_main: vsphere/technology/storage/concepts/storage-layers
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item B10"
answer: [A, B, E, F]
misconception: [C]
misconception_type: [provider-vs-consumer]
pair: "0188"
status: draft
```
