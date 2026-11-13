# Linux storage I/O path

## Layer
- Guest OS layer: Linux, running on the VM. The VM is a virtual motherboard; it cannot see inside the Guest OS.
- The counters in this file are collected inside Linux (/proc/diskstats, iostat, sar, a node exporter). vCenter and VCF Operations store some of them on the VirtualMachine object when VMware Tools collects them. That is a data path, not ownership.

## Control plane and data plane
- The Linux block layer is a control plane: its code passes descriptors (struct bio, struct request, page pointers, scatter-gather lists) and does not copy the data.
- The data plane is the payload. For a direct write (a database that opens its files with O_DIRECT, or uses io_uring or libaio), the kernel pins the user pages in RAM, and the hardware moves the bytes by DMA, with no copy by the block layer.
- A queue counter at the block layer counts requests, not bytes. A 4 KB request and a 1 MB request each count as one request while in flight.

## Stack from application to driver
| Layer | Component | What it does |
|---|---|---|
| Application | PostgreSQL, MySQL | Calls pwrite or io_uring_enter, with O_DIRECT for a direct write. |
| System call | sys_pwrite64, io_uring handler | Switches the CPU from user mode to kernel mode. |
| Virtual file system | vfs_write | Checks the file descriptor, the locks and the offset. |
| File system | ext4, xfs | Translates the file offset into a block number. |
| Block layer | submit_bio, struct bio | Builds the I/O descriptor with the list of memory pages. |
| Multi-queue layer | blk-mq | Turns the bio into a struct request on a software queue per CPU, then on a hardware dispatch queue. |
| I/O scheduler | none, mq-deadline, kyber | Optionally merges or reorders requests. |
| Driver | nvme (NVMe hardware), vmw_pvscsi under sd (in a VM) | Turns the request into a command for the device and signals it. |

## Collection point of the queue statistics
- iostat, sar and node exporters read the block statistics from /proc/diskstats or /sys/block/DEVICE/stat. The kernel keeps them at the block layer, from the moment a request is given to the request queue until it finishes.
- Field 9 is the number of I/Os in progress: incremented as requests are given to the request queue, decremented as they finish. It is the only field that goes back to zero.
- Field 10 is the milliseconds spent doing I/Os. It grows while field 9 is not zero. Since kernel 5.0 it counts jiffies in which at least one request was started or completed.
- Field 11 is the weighted milliseconds spent doing I/Os: at each I/O start, completion, merge or read of the statistics, the number of I/Os in progress times the milliseconds since the last update is added.
- The statistics file has 17 fields. All except field 9 are cumulative counters, so a tool takes the difference between two reads.
- A request counts from the moment it enters the request queue. A request that waits in a blk-mq software queue or in the I/O scheduler is counted as in progress, the same as a request that the device is serving.

## iostat columns
- aqu-sz is the average queue length of the requests issued to the device: the increase of field 11 over the interval, divided by the length of the interval in milliseconds.
- aqu-sz equals the I/O rate times await. This is Little's Law, and it holds for any device.
- await is the average time in milliseconds for an I/O request to be served. It includes the time in the queue and the time in service. r_await and w_await are the read and write versions.
- r/s and w/s are the completed reads and writes per second. Their sum is the I/O rate.
- %util is the percentage of the elapsed time during which I/O requests were issued to the device (field 10). A device that serves requests one at a time is saturated when %util is near 100%. For devices that serve requests in parallel, such as RAID arrays and modern SSDs, %util at 100% does not show a performance limit.
- aqu-sz does not separate requests waiting in the software queues from requests being served by the device.

## Reading the value
- A high aqu-sz on an NVMe device or on a virtual disk backed by a parallel array is mostly requests served at the same time. It is not a backlog by itself.
- The same aqu-sz can mean opposite things. aqu-sz of 32 with 8,000 I/Os per second and await of 4 ms is 32 requests served in parallel. aqu-sz of 32 with 800 I/Os per second and await of 40 ms is a slow device.
- Compare await with the response time of the layer below. A large await with a small difference from the vCenter virtual disk latency puts the time below the guest.
- Saturation shows as await rising while the I/O rate stays flat. Spare capacity shows as the I/O rate rising while await stays flat.

## Waiting inside Linux in a VM
- The driver for the Paravirtual SCSI adapter is vmw_pvscsi, under the SCSI disk driver. Below it are the virtual adapter, the VMkernel and the physical storage.
- await in Linux covers the queue in Linux, the virtual adapter, the VMkernel and the storage. The vCenter virtual disk latency starts at the virtual disk, so the time a request waits in Linux before it is issued to the virtual disk is not in it.
- The Paravirtual SCSI adapter default queue depth is 64 for a device and 254 for an adapter. The ring has 8 pages by default. The module options are cmd_per_lun and ring_pages, set for example with options vmw_pvscsi cmd_per_lun=254 ring_pages=32 in a file under /etc/modprobe.d/, or on the kernel command line. The values in use are in /sys/module/vmw_pvscsi/parameters/.
- Requests at the virtual disk: the I/O rate times the vCenter virtual disk latency, over the same interval. This follows from Little's Law.
- Requests held inside Linux before the virtual disk: aqu-sz minus the requests at the virtual disk. A remainder near zero means aqu-sz shows requests the device serves in parallel. A large remainder, with the requests at the virtual disk at the queue depth, means requests wait for a free slot.

## Misconceptions
- "%util at 100% means the disk is saturated" → %util is the share of time with at least one I/O in flight. For a parallel device it does not show a limit.
- "aqu-sz of 32 means a backlog of 32 requests" → aqu-sz equals the I/O rate times await. At 8,000 I/Os per second and 4 ms it is 32 requests in service.
- "await is the response time of the device" → await includes the time in the Linux queue.
- "The iostat queue counts only requests not yet sent to the driver" → a request counts from the moment it enters the request queue, until it finishes, whether it waits or is served.
- "A large aqu-sz at a low vCenter latency proves the problem is in Linux" → only the part above the I/O rate times the vCenter latency is held in Linux.

## Metadata
```yaml
id: guest-os/storage/linux-storage-io-path
retriever_guide: how-it-works
scope: guest-os
technology:
- storage
pillar:
- performance
product:
- linux
- vcf-operations
layer:
- guest-os
internal_derive: []
related:
- guest-os/storage/disk-queue
- guest-os/storage/windows-storage-io-path
- vsphere/technology/storage/concepts/esxi-storage-latency-stack
- vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
- vsphere/technology/storage/concepts/guest-os-vs-vm-storage
source:
  document: Linux kernel documentation, I/O statistics fields (admin-guide/iostats, development tree 7.4.0-rc2); sysstat iostat(1) manual page (man-pages July 2025); Broadcom KB 343323, Large-scale workloads with intensive I/O patterns might require queue depths significantly greater than Paravirtual SCSI default values
  path: Fields 9 to 11 (kernel documentation); aqu-sz, await, %util (iostat); Resolution (Broadcom KB)
corrections: []
review_notes:
- 'To check: Section ''Stack from application to driver'' and the blk-mq detail (software queue per CPU, hardware dispatch queue, scheduler names): against the kernel block layer documentation, docs.kernel.org/block.'
- 'To check: Section ''Collection point of the queue statistics'': the point at which a request starts to count in the in-flight statistics on blk-mq (request creation or dispatch) differs by kernel version; the kernel documentation says it counts from the moment the request is given to the request queue.'
- 'To check: Section ''Waiting inside Linux in a VM'': the vmw_pvscsi default of cmd_per_lun and ring_pages (the Broadcom KB states 64 and 254 as the adapter defaults and 8 ring pages, not the module defaults); that the vCenter virtual disk latency starts at the virtual disk; the subtraction is a derivation from Little''s Law, not a vendor procedure.'
- 'Source URL, kernel documentation: https://www.kernel.org/doc/html/latest/admin-guide/iostats.html'
- 'Source URL, iostat: https://man7.org/linux/man-pages/man1/iostat.1.html'
- 'Source URL, Broadcom KB 343323 (legacy 2053145, no Updated On date shown): https://knowledge.broadcom.com/external/article?legacyId=2053145'
status: draft
```
