# Guest deleted data, datastore used unchanged

## Prompt
- fs-03 is a Windows file server VM with one 4 TB thin virtual disk on VMFS 6 datastore DS-FILE01, on a thin-provisioned array.
- Yesterday the team deleted 600 GB of old files inside Windows.
- Today, in VCF Operations, the VM's Disk Space | Virtual Disk Used and the datastore's used space are almost unchanged.

Which statements are correct?

- A. A guest delete leaves the blocks allocated; the thin disk frees them when the guest sends TRIM or unmap.
- B. The space came back at the delete; the counters only lag until the next collection cycle.
- C. VMFS 6 passes the guest's unmap on to the array in the background, at a throttled rate.
- D. Free regions smaller than the 1 MB VMFS block size are not reclaimed by VMFS 6.
- E. Powering off fs-03 returns the deleted space to the datastore and to the array.
- F. With a thick disk, the same guest unmap would lower the datastore's used space.

## Likely wrong answer
B: deleted in the guest means free on the datastore.

## Expected key points
- Answer: A, C, D.
- A: a guest delete marks blocks free inside the guest filesystem only. TRIM (ATA) or unmap (SCSI) passes the free blocks down to the virtual disk and the array.
- C: VMFS 6 reclaims automatically, in the background, at a throttled rate set by the space reclamation priority, so array space returns over time, not at once. The host's Unmap IO and Unmap Size counters show it working.
- D: reclamation works in units of the 1 MB VMFS block.
- B is wrong: nothing is released until an unmap reaches the disk.
- E is wrong: powering off frees only the swap file.
- F is wrong: a thick disk keeps its full size; unmap applies only to thin disks.

## Notes
- Drafted by Claude 2026-11-12. Counts only after author approval.
- Windows sends unmap on delete when delete notifications are on and the virtual hardware supports it; the stem implies it did not, so the guest side is the first thing to check. The options do not depend on why.
- Vendor documents: VMFS 6 automatic space reclamation and its 1 MB granularity, vSphere Storage, "Space Reclamation Requests from VMFS Datastores" (https://docs.vmware.com/en/VMware-vSphere/8.0/vsphere-storage/GUID-BC1A172C-E649-4812-B8B2-A9E45AC97051.html); Broadcom KB 314380 (unmap granularity above 1 MB). The key does not depend on the exact reclamation rate: the knowledge base gives 25-50 MB/s at Low, some Broadcom pages give 100 MB/s.

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
source_path: "Drafted by Claude 2026-11-12"
answer: [A, C, D]
misconception: [B]
misconception_type: [layer-confusion]
status: draft
```
