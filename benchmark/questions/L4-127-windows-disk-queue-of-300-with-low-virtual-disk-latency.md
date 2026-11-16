# Windows disk queue of 300 with 3.2 ms at the virtual disk

## Prompt
- A Windows Server 2022 VM with 16 vCPUs runs SQL Server 2022. The data files are on one virtual disk, on an all-flash VMFS datastore, behind a Paravirtual SCSI controller. The Paravirtual SCSI driver parameters were never changed.
- Every night between 02:10 and 02:40 a checkpoint and an index rebuild run. The application team reports that the batch steps take three times longer than a month ago.
- Performance Monitor, PhysicalDisk of the data disk, 5-minute average for 02:15 to 02:20:
  - Disk Transfers/sec: 20,000
  - Avg. Disk sec/Transfer: 0.015
  - Avg. Disk Queue Length: 300
  - Current Disk Queue Length at 02:20: 310
- vCenter, the same 5 minutes, the same virtual disk: 20,000 IOPS and a virtual disk latency of 3.2 ms for reads and for writes.
- Other VMs on the same datastore show normal latency. The array reports no alert. In Windows, Processor Time is 38%. VM CPU Ready is 0.2%.
- The storage team says: "Windows measures 15 ms for each I/O, so the array is slow." The application team says: "A queue of 300 is normal on all-flash storage, because flash likes deep queues, so there is nothing to fix."

Which statements are correct?

- A. The array is slow. Windows measures 15 ms for each I/O, and the 300 requests of the queue wait at the array.
- B. The array is not the cause: about 64 requests sit at the virtual disk, the device default, and 236 wait in Windows.
- C. The queue is normal. Flash serves requests in parallel, so all 300 requests are in service and the 15 ms is the latency of the storage.
- D. The default device queue depth of the Paravirtual SCSI driver is 254, so the virtual disk still has free slots.
- E. The 11.8 ms between the two latencies is CPU time of the Windows storage stack, so the VM needs more vCPUs.
- F. Raising the PVSCSI device queue depth and ring pages, then restarting, would shorten the wait in Windows.
- G. The adapter queue limit of 254, shared by its disks, is what holds these requests back in Windows.

## Likely wrong answer
A or C: the Windows response time is read as the latency of the storage, or the queue of 300 is read as normal parallelism on flash. D: the Linux driver default of 254 per device taken for the Windows one.

## Expected key points
- Answer: B, F.
- A is wrong: the 3.2 ms in vCenter is the storage side, and it is healthy; the 15 ms in Windows includes the wait inside Windows. Requests at the virtual disk are the I/O rate x the vCenter latency: 20,000 x 0.0032 = 64, not 300.
- B is correct: Avg. Disk Queue Length is derived, 20,000 x 0.015 = 300, and counts every request below the partition manager. 64 are at the virtual disk, the default Paravirtual SCSI depth of 64 per device in Windows, so the device is full. The remainder, 300 - 64 = 236, waits in Storport and the adapter driver for a free slot: 236 / 20,000 = 11.8 ms of each I/O, the gap between 15 ms and 3.2 ms.
- C is wrong: if all 300 requests were in service, the vCenter latency would be 15 ms, not 3.2 ms.
- D is wrong: 254 per device is the Linux vmw_pvscsi default (and the Windows per-adapter default); the Windows driver default is 64 per device, and 64 requests at the virtual disk fill it.
- E is wrong: Processor Time is 38% and Ready 0.2%; the 11.8 ms is queueing for a slot, not CPU time.
- F is correct: the Windows registry value DriverParameter (MaxQueueDepth up to 254, RequestRingPages 32), applied after a restart, gives the disk more slots; spreading the files over more virtual disks is the other fix.
- G is wrong: the adapter default of 254 is shared by its disks, and this one disk holds only 64; the per-device depth is the limit.

## Notes
- Public source: Microsoft Learn, "Using Storage-related Parameters and Performance Counters" (Windows Server 2012 R2 archive page): the counters represent the requests active below the driver that takes the statistics, including requests in service; Avg. Disk Queue Length = Disk Transfers/sec x Disk sec/Transfer (Little's Law); physical disk statistics are tracked by the partition manager. Broadcom KB 343323 (legacy 2053145, no Updated On date): the Paravirtual SCSI default queue depth is 64 for a device and 254 for an adapter, and the Windows registry values. 
- Debatable risk: that the vCenter virtual disk latency starts at the virtual disk and excludes the wait in Windows is read from the counter definitions and the knowledge file; the vSphere API reference was not read for this. The numbers are chosen so that the arithmetic is exact.
- Prepared with author question Q194 (the reading of the guest disk queue).
- Changed in the 2026-11-15 audit: key points one per option; B shortened (length cue); D ("the counter holds only requests not yet sent", a third copy after 0311/0418, redundancy #46) replaced in place by the Linux-default transplant (254 per device); F (true fix) and G (false, adapter limit) added. The review's option on 5-minute averages hiding bursts was not added: that fact is over the two-question cap (redundancy #13).

## Metadata
```yaml
id: "0359"
title: "Windows disk queue of 300 with 3.2 ms at the virtual disk"
product: [windows, vsphere]
technology: [storage]
task: troubleshoot
level: 400
answer_type: deterministic
input: [text]
object: [vm, guest-os]
tool: [guest-os-tools, vcenter]
knowledge:
  - guest-os/storage/windows-storage-io-path
  - guest-os/storage/disk-queue
  - vsphere/technology/storage/concepts/esxi-storage-latency-stack
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
  - guest-os/storage/linux-storage-io-path
knowledge_main: guest-os/storage/windows-storage-io-path
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for author question Q194 (project/plan.md)"
answer: [B, F]
misconception: [C, D]
misconception_type: [layer-confusion, threshold-transplanted]
status: draft
```
