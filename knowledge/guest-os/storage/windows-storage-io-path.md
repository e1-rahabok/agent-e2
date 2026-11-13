# Windows storage I/O path

## Layer
- Guest OS layer: Windows, running on the VM. The VM is a virtual motherboard; it cannot see inside the Guest OS.
- The counters in this file are collected inside Windows (Performance Monitor, WMI, VMware Tools). vCenter and VCF Operations store some of them on the VirtualMachine object. That is a data path, not ownership.

## Control plane and data plane
- The Windows storage stack is a control plane: its drivers pass descriptors (I/O request packets, memory descriptor lists, SCSI request blocks) and do not copy the data.
- The data plane is the payload. For an unbuffered write (a database engine that opens its files with FILE_FLAG_NO_BUFFERING), the kernel locks the buffer pages in RAM with a memory descriptor list, and the hardware moves the bytes by DMA, with no copy by the driver stack.
- A counter at a driver layer counts requests, not bytes. A 4 KB request and a 1 MB request each count as one request while active.

## Stack from application to adapter driver
| Layer | Driver | What it does |
|---|---|---|
| Application | sqlservr.exe, any process | Calls WriteFile with a buffer, a file handle and a size. |
| I/O manager | ntoskrnl.exe | Creates the I/O request packet and locks the buffer pages. |
| File system | ntfs.sys, refs.sys | Translates the file offset into a logical cluster number. |
| Volume manager | volmgr.sys | Translates the cluster into a volume block address. Handles software striping. |
| Partition manager | partmgr.sys | Translates the volume address into a disk address. Collects the PhysicalDisk counters. |
| Disk class driver | disk.sys | Builds the storage request block. |
| Storport | storport.sys | Queues requests per device and binds the protocol. |
| Adapter driver | pvscsi (in a VM), stornvme (NVMe hardware) | Turns the request into a command for the adapter and signals it. |

## Collection point of the disk counters
- PhysicalDisk statistics are tracked by the partition manager. LogicalDisk statistics are tracked at the volume level, by the volume manager.
- A counter at the partition manager covers a request from that layer down: disk class driver, Storport, adapter driver, device, and back. It leaves out the file system above it.
- Continuous monitoring of the disk counters can cost up to a few percent CPU on a server with a heavy I/O load. Enable them on a sampling basis or for a diagnosis.

## Avg. Disk Queue Length
- Avg. Disk Queue Length is a derived counter: Disk Transfers/sec x Avg. Disk sec/Transfer. This is Little's Law: queue length = arrival rate x time in the system. The read and write versions are derived the same way.
- It counts the requests active below the partition manager. A request is not necessarily waiting. It can be in a Storport queue, in a queue of the adapter driver, in a controller queue, in an array queue, in service at the disk, or completed and on its way back up the stack.
- The derivation assumes the number of outstanding requests is the same at the start and at the end of each sampling interval. A burst that starts and ends inside one interval is smoothed.
- Current Disk Queue Length is the number of active requests at the instant of the sample. It varies widely. Use it to find short bursts or to check a value of Avg. Disk Queue Length.
- % Disk Time is Avg. Disk Queue Length x 100, shown as a percentage. It exceeds 100% whenever the average queue is above 1.
- At the same IOPS, a lower Avg. Disk sec/Transfer gives a lower Avg. Disk Queue Length, because the counter includes the time in service.
- The counter does not separate the waiting part from the part in service. A second measurement is needed for that (section Waiting inside Windows in a VM).

## Reading the value
- SSD and NVMe devices work in parallel and do better with long queues. A high Avg. Disk Queue Length on such a device is mostly requests in service at the same time.
- The Microsoft guideline of about 2 per physical disk counts spindles that the server knows. It is hard to apply to thin provisioned or tiered storage, and a virtual disk has no spindles to count.
- SQL Server issues asynchronous I/O in bursts that push the queue length up. A long queue alone does not show a problem. Avg. Disk sec/Transfer is the direct indicator of response time.

## Waiting inside Windows in a VM
- The bottom of the Windows stack in a VM is the adapter driver, pvscsi for the Paravirtual SCSI adapter. Below it are the virtual adapter, the VMkernel and the physical storage.
- Avg. Disk sec/Transfer in Windows covers everything below the partition manager: the guest queues, the virtual adapter, the VMkernel and the storage.
- The vCenter virtual disk latency starts at the virtual disk. The time a request waits in Windows for a free slot of the virtual adapter is not in it.
- The Paravirtual SCSI adapter default queue depth is 64 for a device and 254 for an adapter. The ring has 8 pages by default. In Windows the values are set with the registry value DriverParameter, for example RequestRingPages=32,MaxQueueDepth=254, under HKLM\SYSTEM\CurrentControlSet\services\pvscsi\Parameters\Device, and take effect after a restart.
- Requests at the virtual disk: Disk Transfers/sec x the vCenter virtual disk latency, over the same interval. This follows from Little's Law.
- Requests held inside Windows before the virtual disk: Avg. Disk Queue Length minus the requests at the virtual disk.
- A remainder near zero means the counter shows requests in service, which the application itself generates. The queue is not a wait in Windows.
- A remainder that is large, with the requests at the virtual disk at the device queue depth, means requests wait in Windows for a free slot. The array is not the cause when the vCenter latency is low. Raise the queue depth and the ring pages, or spread the I/O over more virtual disks.
- An average over 5 minutes hides a burst. Read the 20-second peak values to see a burst that exceeds the queue depth for a short time.

## Misconceptions
- "Avg. Disk Queue Length counts the requests waiting inside Windows" → it counts every request below the partition manager: waiting, in service, and completed on the way back.
- "A queue of 32 on an NVMe disk means the disk is saturated" → the device works 32 requests in parallel. Compare with the response time.
- "Keep the disk queue below 2 per disk" → the guideline counts physical spindles. A virtual disk has none.
- "The disk queue and the VM disk latency are unrelated" → they connect through Little's Law: queue = IOPS x latency. Compare the queue with IOPS x the vCenter latency.
- "A 1 MB request adds ten times the queue of a 100 KB request" → each request counts as one while active.
- "% Disk Time cannot exceed 100%" → it is the average queue length x 100, so it does.

## Metadata
```yaml
id: guest-os/storage/windows-storage-io-path
retriever_guide: how-it-works
scope: guest-os
technology:
- storage
pillar:
- performance
product:
- windows
- vcf-operations
layer:
- guest-os
internal_derive: []
related:
- guest-os/storage/disk-queue
- guest-os/storage/linux-storage-io-path
- vsphere/technology/storage/concepts/esxi-storage-latency-stack
- vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
- vsphere/technology/storage/concepts/guest-os-vs-vm-storage
source:
  document: Microsoft Learn, Using Storage-related Parameters and Performance Counters (Windows Server 2012 R2 archive page); Broadcom KB 343323, Large-scale workloads with intensive I/O patterns might require queue depths significantly greater than Paravirtual SCSI default values
  path: Logical disks and physical disks; Queue lengths (Microsoft). Resolution (Broadcom KB)
corrections: []
review_notes:
- 'To check: Section ''Stack from application to adapter driver'': the layer order and the role of each driver, against the Windows driver documentation on learn.microsoft.com (storage drivers, Storport, partition manager).'
- 'To check: Section ''Waiting inside Windows in a VM'': that the vCenter virtual disk latency starts at the virtual disk (read the counter definition in the vSphere API reference, developer.broadcom.com), and the subtraction of requests at the virtual disk from Avg. Disk Queue Length, which is a derivation from Little''s Law, not a vendor procedure.'
- 'Source URL, Microsoft: https://learn.microsoft.com/previous-versions/dn567651(v=vs.85)'
- 'Source URL, Broadcom KB 343323 (legacy 2053145, no Updated On date shown): https://knowledge.broadcom.com/external/article?legacyId=2053145'
status: draft
```
