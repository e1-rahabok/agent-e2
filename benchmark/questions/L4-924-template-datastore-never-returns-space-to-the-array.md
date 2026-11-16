# Template datastore never returns space to the array

## Prompt
- Array pool P2 is thin-provisioned: 120 TB usable, 94% used. It backs ten thin LUNs of 16 TB each, every one a VMFS 6 datastore mounted by the same four ESXi 9.1 hosts.
- Four weeks ago, 6 TB of VMs moved by Storage vMotion from DS-TPL01 to DS-APP02, both on pool P2. Since then DS-TPL01 holds only templates and powered-off VMs.
- vCenter shows DS-TPL01 with 2.4 TB used and 13.6 TB free. Its space reclamation priority is Low.
- The array team reports that pool P2's used space has not fallen since the move.
- VCF Operations, last four weeks: Unmap Size (MB) of DS-TPL01 is 0 on each of the four hosts.
- Same period, on host esx-11, DS-APP02 shows Unmap IO of about 1,800 in several cycles, and the storage team asks whether that load slows the VMs there.

Which statements are correct?

- A. Pool P2's free space, about 7.2 TB, not DS-TPL01's 13.6 TB, limits how far P2's thin LUNs can still grow.
- B. DS-TPL01 has 13.6 TB free, so the VMs on pool P2 still have ample room to grow.
- C. With no file on DS-TPL01 open, VMFS 6 sends no automatic unmap for it, hence the Unmap Size of 0.
- D. Raising DS-TPL01's space reclamation priority to High would return the 6 TB to P2 with no other change.
- E. Powering on a VM whose files sit on DS-TPL01 lets the background unmap release the freed blocks.
- F. The 6 TB stays allocated on the array because the guests of the moved VMs never sent TRIM.
- G. The Unmap IO on DS-APP02 adds array load like the same number of writes, so it slows the VMs there.
- H. The Unmap Size of DS-TPL01 read on one host is the datastore's total for all four hosts.
- I. The provisioned-to-capacity ratio of each datastore also covers the space risk of pool P2.

## Likely wrong answer
"DS-TPL01 shows 13.6 TB free, so space is not our problem" (B). Or the storage team's reading of the unmap counter: "1,800 unmap commands is IO load on the array" (G).

## Expected key points
- Answer: A, C, E.
- A is correct: on thin LUNs (thin on thin), read the array's free space too; the datastore can show room the array no longer has. 6% of 120 TB is 7.2 TB free on the pool, while the ten LUNs present 160 TB.
- B is wrong: the misconception. VMFS free space is the datastore's view; the array pool behind the thin LUN is nearly full.
- C is correct: a VMFS 6 datastore releases blocks only while at least one of its files is open, for example the files of a powered-on VM. Templates and powered-off VMs keep no file open, so nothing is unmapped.
- D is wrong: the wrong action. Without an open file there is no unmap at any priority; the vSphere Client also offers only Low and None (Medium and High need esxcli).
- E is correct: an open file on the datastore lets VMFS 6 send its background unmap again. A manual unmap with esxcli also releases the space at once.
- F is wrong: unmap starts from two places, the VMFS datastore (deleted or migrated VMs, consolidated snapshots) and the Guest OS (files deleted on a thin disk). The blocks of VMs moved off a datastore are freed by VMFS, not by the guests.
- G is wrong: the misconception. An unmap command asks the array to release blocks; no data is read or written. A host sending unmap regularly is normal on a thin-provisioned array.
- H is wrong: Unmap IO and Unmap Size exist per host and datastore only; the datastore total is the sum over the hosts that mount it.
- I is wrong: the datastore ratio counts the datastore's capacity; with thin LUNs, the array pool can fill first, so read the pool's free space too.

## Metadata
```yaml
id: "0460"
title: "Template datastore never returns space to the array"
product: [vsphere, vcf-operations]
technology: [storage]
task: decide-capacity
level: 400
answer_type: deterministic
input: [text]
object: [datastore, esxi]
tool: [vcenter, vcf-operations]
knowledge:
  - vsphere/technology/storage/metrics/host/datastore
  - vsphere/technology/storage/datastore-space-headroom
knowledge_main: vsphere/technology/storage/metrics/host/datastore
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-15, question bank audit gap: vsphere/technology/storage/metrics/host/datastore"
answer: [A, C, E]
misconception: [B, G]
misconception_type: [layer-confusion]
status: draft
```
