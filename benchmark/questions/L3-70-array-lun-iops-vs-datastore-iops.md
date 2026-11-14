# Array LUN IOPS against datastore IOPS

## Prompt
- A VMFS datastore sits on one LUN of an FC array and is mounted by the 8 hosts of one cluster. No other datastore uses the LUN.
- The storage team compares, hour by hour, the IOPS the array reports for the LUN with the datastore IOPS in vCenter.

Which statements are correct?

- A. The vCenter datastore IOPS count only the IO that the hosts in this vCenter send to the datastore.
- B. The array counts every IO on the LUN: from every initiator, and from its own jobs such as replication.
- C. With one datastore on one LUN the two must always match, so any gap is a counting fault.
- D. Array IOPS and vCenter IOPS cannot be compared, even with one datastore on one LUN.
- E. A LUN-to-datastore IOPS ratio of 1.5 means one third of the LUN's IO comes from outside the hosts in vCenter.
- F. A backup proxy that reads the LUN directly over the SAN adds IO that the array counts and vCenter does not.
- G. A snapshot on one of the VMs adds IO that the array counts and the datastore counters miss.
- H. When the array shows more IOPS than vCenter, lower the IO of the VMs on the datastore.

## Likely wrong answer
C: the IOPS of a datastore and of its only LUN must match, so one tool miscounts.

## Expected key points
- Answer: A, B, E, F.
- A true: vCenter sees only its own hosts; a host of another vCenter or a non-ESXi initiator is invisible to it.
- B true: the array counts the LUN's IO from every initiator and from its own jobs (replication, array snapshots, rebuilds).
- C false: each tool is right from its vantage point; a ratio above 1 is IO no host in vCenter sends.
- D false: with a 1:1 mapping the ratio LUN IOPS / datastore IOPS is the check, and 1 is the expected value.
- E true: 1.5 means the other IO is half of what the hosts send: 0.5 / 1.5 = one third of the LUN's IO.
- F true: a SAN-mode backup proxy is another initiator on the LUN.
- G false: snapshot IO passes through the hosts and is counted in the datastore metrics, which include every file on the datastore.
- H false: the extra IO is not the VMs' IO; find the other initiator or array job with the storage team.

## Notes
- Theory half of the pair with 0188 (practical; design.md, section 3.9). Different situation and numbers from 0188.
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item B10 (origin: synthetic). Counts only after author approval.

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
