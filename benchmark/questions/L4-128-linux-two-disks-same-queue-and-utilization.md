# Linux: two disks with the same queue and the same utilization

## Prompt
- A Linux VM (RHEL 9, kernel 5.14, 8 vCPUs) has two virtual disks on a Paravirtual SCSI controller, driver vmw_pvscsi. The disk sdb holds a PostgreSQL database on the datastore DS-FAST. The disk sdc holds the archive of the write-ahead log and the backups on the datastore DS-ARCH, an older array.
- During a 5-minute window, `iostat -x 300 2` reports for the second interval:

| Device | r/s + w/s | await (ms) | aqu-sz | %util |
|---|---|---|---|---|
| sdb | 6,400 | 5.0 | 32.0 | 100 |
| sdc | 640 | 50.0 | 32.0 | 100 |

- vCenter, the same 5 minutes: virtual disk latency sdb 4.8 ms, sdc 48 ms; virtual disk outstanding IO about 31 on each disk. CPU utilization inside Linux is 20%.
- The vmw_pvscsi module runs with its default queue depths.
- Engineer 1 says: "Both disks show 100% utilization and the same queue of 32, so both are saturated and have the same backlog. Raise nr_requests on both."
- Engineer 2 says: "The await of sdb is 5 ms, which is fine. The await of sdc is 50 ms. The queue is the same, so the cause is the Linux queue of sdc. Tune it."

Which statements about the four columns, the two disks and the two engineers are correct?

- A. aqu-sz is the I/O rate times await: 6,400 x 5 ms and 640 x 50 ms both give 32.
- B. Both disks at 100% %util with an aqu-sz of 32 are saturated and carry the same backlog.
- C. The same aqu-sz of 32 means requests served in parallel on sdb and a slow device on sdc.
- D. %util of 100% says only that each disk always had a request in flight; for a parallel device it shows no limit.
- E. On a device that serves one request at a time, %util near 100% would show saturation.
- F. sdc has the same queue as sdb and a higher await, so the cause of its await is its Linux queue.
- G. await is the response time of the device, so the array behind sdc answers in about 40 ms.
- H. The device queue depth vmw_pvscsi uses on this VM can be read in /sys/module/vmw_pvscsi/parameters/.
- I. The vCenter virtual disk latency includes the time a request waits in Linux before it is issued.
- J. aqu-sz in iostat counts only the requests still waiting to be sent to the driver.
- K. Raising nr_requests or the queue depth for sdc would not lower its await.
- L. The queue of 32 on sdc is at the default Paravirtual SCSI device queue depth, so raising cmd_per_lun would help.
- M. sdb would show spare capacity as a rising await with a flat I/O rate when its load grows.
- N. Next for sdc: the latency of DS-ARCH split into device, kernel and queue latency, and the load of the array.
- O. On sdb, about 30 of the 32 requests wait in Linux, a backlog in front of the virtual disk.

## Likely wrong answer
- B: "Both disks have 100% utilization and an aqu-sz of 32, so both are saturated: raise the queue size on both."
- F: "Same queue, ten times the await on sdc: the Linux queue of sdc is the problem; tune it."

## Expected key points
- Answer: A, C, D, E, H, K, N.
- A true: Little's Law: sdb 6,400 x 0.005 = 32 and sdc 640 x 0.050 = 32.
- B false: aqu-sz alone does not show a backlog, and %util at 100% does not show a limit for a device that serves requests in parallel. Neither engineer is right.
- C true: 32 requests in service at 6,400 I/Os per second, against 32 requests on a slow device at 640 I/Os per second.
- D true: %util is the share of the time with at least one I/O in flight (field 10). For modern SSDs and arrays, 100% does not show a limit.
- E true: %util is the share of the time with at least one request in flight; a device that serves one request at a time is then busy all the time, so near 100% it is saturated. Only for parallel devices does 100% show no limit.
- F false: about 31 of the 32 requests are at the virtual disk (640 x 0.048 = 30.7, the outstanding IO vCenter shows), so only about 1.3 wait in Linux; await 50 ms against 48 ms in vCenter puts the time of sdc below the guest.
- G false: await covers the queue in Linux, the virtual adapter, the VMkernel and the storage; the vCenter latency shows 48 ms below the guest, and even that includes the VMkernel.
- H true: the module parameters in use (cmd_per_lun, ring_pages) are listed under /sys/module/vmw_pvscsi/parameters/; they are set as module options in /etc/modprobe.d/ or on the kernel command line.
- I false: the vCenter virtual disk latency starts at the virtual disk; the wait in Linux before it is not in it.
- J false: a request counts from the moment it enters the request queue until it finishes, whether it waits or is served.
- K true: only about 1.3 requests wait in Linux; a larger queue only holds more requests in front of a slow device.
- L false: the default device queue depth of vmw_pvscsi on kernel 5.14 is 254 (cmd_per_lun), and only about 31 requests are at the virtual disk. No request waits for a free slot.
- M false: await rising with the I/O rate flat is the sign of saturation; spare capacity shows as the I/O rate rising with await flat. For sdb, nothing to tune unless the database needs a response time below 5 ms.
- N true: read device, kernel and queue latency of DS-ARCH in esxtop, the array load and the schedule of the backups; ask whether the archive workload needs better than 48 ms.
- O false: 5.0 ms against 4.8 ms, so Linux adds about 0.2 ms; 6,400 x 0.0048 = 30.7 of the 32 requests are at the virtual disk, in service, and only about 1.3 are in Linux. Not a backlog.

## Notes
- Public source: Linux kernel documentation, I/O statistics fields: field 9 counts requests in progress, field 10 the time with at least one request in progress, field 11 the weighted time. sysstat iostat(1) manual page: aqu-sz is the average queue length of the requests issued to the device; await includes the time in the queue and the time in service; %util for devices serving requests in parallel, such as RAID arrays and modern SSDs, does not reflect their performance limits. aqu-sz = I/O rate x await is Little's Law.
- Debatable risk: that the vCenter virtual disk latency starts at the virtual disk and excludes the wait in Linux is read from the counter definitions and the knowledge file; the vSphere API reference was not read for this. The numbers are chosen so that the arithmetic is exact.
- Prepared with author question Q194 (the reading of the guest disk queue).
- The prompt states that vmw_pvscsi runs with its default queue depths, so option L is decidable. The Linux vmw_pvscsi default cmd_per_lun is 254 (PVSCSI_DEFAULT_QUEUE_DEPTH in drivers/scsi/vmw_pvscsi.c, kernel 5.0 and later); the 64 per device of Broadcom KB 343323 is the Windows driver default. L stays false under either value, because about 31 requests are at the virtual disk.
- Changed in the 2026-11-15 audit: the iostat and vCenter numbers changed so they are no longer the knowledge-base example (aqu-sz 32 kept for L); the requests at the virtual disk are given in the stem as vCenter outstanding IO (redundancy #45: the Little's Law fact stays with 0028/0416), and old E (time at or below the virtual disk) and H (1.6 requests wait in Linux) were replaced in place by two true facts no question tests: %util near 100% does show saturation on a serial device (from the retired 0419), and where the vmw_pvscsi parameters in use are read.

## Metadata
```yaml
id: "0360"
title: "Linux: two disks with the same queue and the same utilization"
product: [linux, vsphere]
technology: [storage]
task: troubleshoot
level: 400
answer_type: deterministic
answer: [A,C,D,E,H,K,N]
misconception: [B,F]
input: [text]
object: [vm, guest-os]
tool: [guest-os-tools, vcenter]
knowledge:
  - guest-os/storage/linux-storage-io-path
  - guest-os/storage/disk-queue
  - vsphere/technology/storage/concepts/esxi-storage-latency-stack
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
  - vsphere/technology/storage/metrics/virtual-motherboard/outstanding-io
knowledge_main: guest-os/storage/linux-storage-io-path
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for author question Q194 (project/plan.md)"
misconception_type: [layer-confusion, tool-confusion]
status: draft
```
