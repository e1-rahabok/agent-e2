# Why VM, datastore and host totals differ

## Prompt
- Cluster PROD-B has 8 hosts and 240 VMs. Its 12 VMFS datastores are also mounted by the 6 hosts of cluster PROD-C.
- For one hour, you add up the virtual disk IOPS of all VMs in PROD-B.
- The total differs from the sum of the datastore IOPS, and from the sum of the IOPS of the 8 hosts.

Which statements are correct?

- A. IO to a virtual disk on a datastore outside the 12, such as a local one, is in the VM sum but not the datastore sum.
- B. IO from the PROD-C hosts to the 12 datastores is in the datastore sum but in neither PROD-B sum.
- C. One of the three sums must be wrong, since the same IO of the same VMs is counted in each of them.
- D. A guest's IO to a network drive over SMB is in none of the three sums: it leaves through the vNIC.
- E. IO that the ESXi kernel issues for its own modules adds to the host sum and to no VM's sum.
- F. A gap between one VM's virtual disk read IOPS and its datastore read IOPS cannot point to anything on that VM.
- G. Raise the vCenter statistics level for the cluster so that the three sums line up.
- H. To leave PROD-C's IO out, compare with the datastore counters of the 8 PROD-B hosts: each holds only its own share.

## Answers
A, B, D, E, H

## Explanation
- A is correct: a VM's IO on a datastore outside the 12 (a local datastore, another shared one) counts for the VM, not for the 12.
- B is correct: the hosts of PROD-C add IO to the 12 datastores that is in neither the PROD-B VM sum nor the PROD-B host sum.
- C is wrong: the relationships are many-to-many (a VM spans datastores, a datastore holds many VMs and is mounted by hosts of more than one cluster), so totals across VM, datastore, host and cluster do not reconcile, and each value is still correct from its vantage point.
- D is correct: a network drive (SMB) is not a virtual disk; its IO goes out through the vNIC and is invisible to the hypervisor as disk IO.
- E is correct: the kernel does IO for all VMs and for its own modules (for example vSAN); its own IO belongs to no VM.
- F is wrong: the gap has known causes that tell something; for example a datastore read IOPS consistently above the virtual disk read IOPS on VMFS points to a snapshot on that VM.
- G is wrong: a gap between vantage points is expected and is no fault of the statistics collection; a statistics level changes which counters vCenter keeps, not how the objects relate.
- H is correct: a host's datastore counters show only that host's share of a shared datastore, while the datastore object spans every host that mounts it, PROD-C's included.
- Misconception: C: concluding that a metric is broken.

## Notes
- 2026-11-16 (author, Q251): level 200 to 300, as the reviewers read it. A new Level 200 basics question for the guard is still to write.
- Synthetic, 2026-11-05, from the knowledge files listed in `knowledge`; shared datastores stated in the stem. Counts only after the author's approval.
- Changed in the 2026-11-15 audit: D replaced (snapshot IO in datastore but not virtual disk counters is tested by 0045 and 0090) by network-drive IO outside all three sums (storage-layers); G reworded from "open a support case" to another wrong action; H added, a true action (host datastore counters hold the host's share); level 200 -> 300 (four vantage points applied to one case).

## Metadata
```yaml
id: "0049"
title: "Why VM, datastore and host totals differ"
product: [vsphere]
technology: [system, storage]
task: explain-mechanism
level: 300                      # Q251, author 2026-11-16: relabelled as written (was 200)
answer_type: deterministic
input: [text]
object: [vm, datastore, esxi, cluster]
tool: [vcenter]
knowledge:
  - vsphere/architecture/object-relationships
  - vsphere/technology/storage/concepts/storage-layers
  - vsphere/technology/storage/concepts/snapshot-impact
  - vsphere/technology/storage/metrics/virtual-motherboard/datastore
knowledge_main: vsphere/architecture/object-relationships
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-05"
misconception: [C]
misconception_type: [same-name-other-object]
pair: "0417"
status: draft
```
