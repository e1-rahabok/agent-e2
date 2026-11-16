# Guest deleted data, datastore used unchanged

## Prompt
- fs-03 is a Windows file server VM with one 4 TB thin virtual disk on VMFS 6 datastore DS-FILE01, on a thin-provisioned array.
- Yesterday the team deleted 600 GB of old files inside Windows.
- Today, in VCF Operations, the VM's Disk Space | Virtual Disk Used and the datastore's used space are almost unchanged.

Which statements are correct?

- A. fs-03's thin disk shrinks only once Windows sends TRIM or unmap for the freed blocks.
- B. The space came back at the delete; the counters lag until the next collection cycle.
- C. VMFS 6 sends unmap to the array only when an administrator runs a manual unmap command.
- D. VMFS 6 reclaims space in units of its 1 MB block, so smaller free regions stay allocated.
- E. Powering off fs-03 returns the deleted space to the datastore and to the array.
- F. With a thick disk, the same guest unmap would lower the datastore's used space.
- G. At the default reclamation priority, VMFS 6 needs hours to return 600 GB of unmapped space to the array.

## Likely wrong answer
B: deleted in the guest means free on the datastore.

## Expected key points
- Answer: A, D, G.
- A is correct: a guest delete marks blocks free inside the guest filesystem only; the thin disk and the array keep them. TRIM (ATA) or unmap (SCSI) passes the free blocks down to the virtual disk and the array.
- B is wrong: nothing is released until an unmap reaches the disk.
- C is wrong: VMFS 6 reclaims automatically, in the background, at a throttled rate set by the space reclamation priority; a manual unmap only catches up at once.
- D is correct: reclamation works in units of the 1 MB VMFS block; free regions smaller than that are not reclaimed.
- E is wrong: powering off frees only the swap file.
- F is wrong: a thick disk keeps its full size; unmap applies only to thin disks.
- G is correct: at the default Low priority (25-50 MB/s), 600 GB takes about 3.5 to 7 hours; the vSphere Client offers only Low and None, so a faster rate (Medium, High or a fixed rate) needs esxcli. VMFS frees the space at once, while the array's free space lags.

## Notes
- Synthetic, 2026-11-12. Counts only after author approval.
- Windows sends unmap on delete when delete notifications are on and the virtual hardware supports it; the stem implies it did not, so the guest side is the first thing to check. The options do not depend on why.
- Vendor documents: VMFS 6 automatic space reclamation and its 1 MB granularity, vSphere Storage, "Space Reclamation Requests from VMFS Datastores" (https://docs.vmware.com/en/VMware-vSphere/8.0/vsphere-storage/GUID-BC1A172C-E649-4812-B8B2-A9E45AC97051.html); Broadcom KB 314380 (unmap granularity above 1 MB). The key does not depend on the exact reclamation rate: the knowledge base gives 25-50 MB/s at Low (vSphere 9.1); Broadcom KB 452963 (ESXi 7.x, 8.x) gives 100 MB/s.

## Metadata
```yaml
id: "0182"
title: "Guest deleted data, datastore used unchanged"
product: [vsphere, windows, vcf-operations]
technology: [storage]
task: decide-capacity
level: 300
answer_type: deterministic
input: [text]
object: [vm, datastore, guest-os]
tool: [vcf-operations]
knowledge:
  - sp5-framework/capacity/reclamation
  - vsphere/technology/storage/metrics/host/datastore
  - vsphere/technology/storage/concepts/vm-files
knowledge_main: vsphere/technology/storage/metrics/host/datastore
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-12"
answer: [A, D, G]
misconception: [B]
misconception_type: [layer-confusion]
status: draft
```
