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
- B. The array is not the cause. About 64 requests are at the virtual disk, which is the default queue depth of the device, and the other 236 requests wait inside Windows for a free slot.
- C. The queue is normal. Flash serves requests in parallel, so all 300 requests are in service and the 15 ms is the latency of the storage.
- D. All 300 requests wait inside Windows, because the counter holds only requests not yet sent to the adapter, and the 3.2 ms belongs to other requests.
- E. The 11.8 ms between the two latencies is CPU time of the Windows storage stack, so the VM needs more vCPUs.

## Likely wrong answer
A or C: the Windows response time is read as the latency of the storage, or the queue of 300 is read as normal parallelism on flash. D follows the older reading of the counter as the requests not yet sent.

## Expected key points
- Answer: B.
- Avg. Disk Queue Length is derived: Disk Transfers/sec x Avg. Disk sec/Transfer = 20,000 x 0.015 = 300. It counts every request below the partition manager: waiting in the guest queues, in service at the virtual disk and beyond, and completed on the way back.
- Requests at the virtual disk are the I/O rate x the vCenter latency: 20,000 x 0.0032 = 64. That equals the default Paravirtual SCSI queue depth of 64 per device, so the virtual disk is full.
- The remainder, 300 - 64 = 236 requests, waits inside Windows (Storport and adapter driver queues) for a free slot. It is 236 / 20,000 = 11.8 ms of each I/O, the difference between the 15 ms in Windows and the 3.2 ms at the virtual disk.
- A is wrong: the 3.2 ms in vCenter is the storage side, and it is healthy; the 15 ms includes the 11.8 ms wait in Windows. C is wrong: if all 300 requests were in service, the vCenter latency would be 15 ms. D is wrong: the counter also holds the requests in service; 64 of the 300 are. E is wrong: CPU is low, and the wait is queueing for a slot, not CPU time.
- What to do: raise the device queue depth and the ring pages of the Paravirtual SCSI driver (MaxQueueDepth up to 254 and RequestRingPages 32 in the registry, then restart), or spread the files over more virtual disks. The adapter has its own limit of 254 by default, shared by all its disks. Read the 20-second peak values to see the bursts that exceed the depth.

## Notes
- Public source: Microsoft Learn, "Using Storage-related Parameters and Performance Counters" (Windows Server 2012 R2 archive page): the counters represent the requests active below the driver that takes the statistics, including requests in service; Avg. Disk Queue Length = Disk Transfers/sec x Disk sec/Transfer (Little's Law); physical disk statistics are tracked by the partition manager. Broadcom KB 343323 (legacy 2053145, no Updated On date): the Paravirtual SCSI default queue depth is 64 for a device and 254 for an adapter, and the Windows registry values. 
- Why one answer: the three numbers are tied by Little's Law, and the vCenter latency fixes how many requests are at the virtual disk. 64 equals the documented device queue depth.
- Debatable risk: that the vCenter virtual disk latency starts at the virtual disk and excludes the wait in Windows is read from the counter definitions and the knowledge file; the vSphere API reference was not read for this. The numbers are chosen so that the arithmetic is exact.
- Prepared with author question Q194 (the reading of the guest disk queue).
- Stem made plural (2026-11-14): the singular form told the candidate that one option is correct (Q199: the count is never disclosed). Was: "Which statement is correct?"

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
knowledge_main: guest-os/storage/windows-storage-io-path
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for author question Q194 (project/plan.md)"
answer: [B]
misconception: [C, D]
misconception_type: [layer-confusion]
status: draft
```
