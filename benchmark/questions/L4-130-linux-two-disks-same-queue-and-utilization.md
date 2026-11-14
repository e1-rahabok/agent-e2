# Linux: two disks with the same queue and the same utilization

## Prompt
- A Linux VM (RHEL 9, kernel 5.14, 8 vCPUs) has two virtual disks on a Paravirtual SCSI controller, driver vmw_pvscsi. The disk sdb holds a PostgreSQL database on the datastore DS-FAST. The disk sdc holds the archive of the write-ahead log and the backups on the datastore DS-ARCH, an older array.
- During a 5-minute window, `iostat -x 300 2` reports for the second interval:

| Device | r/s + w/s | await (ms) | aqu-sz | %util |
|---|---|---|---|---|
| sdb | 8,000 | 4.0 | 32.0 | 100 |
| sdc | 800 | 40.0 | 32.0 | 100 |

- vCenter, the same 5 minutes, virtual disk latency: sdb 3.8 ms, sdc 38 ms. CPU utilization inside Linux is 20%.
- The vmw_pvscsi module runs with its default queue depths.
- Engineer 1 says: "Both disks show 100% utilization and the same queue of 32, so both are saturated and have the same backlog. Raise nr_requests on both."
- Engineer 2 says: "The await of sdb is 4 ms, which is fine. The await of sdc is 40 ms. The queue is the same, so the cause is the Linux queue of sdc. Tune it."

Which statements about the four columns, the two disks and the two engineers are correct?

- A. aqu-sz is the I/O rate times await: 8,000 x 4 ms and 800 x 40 ms both give 32.
- B. Both disks at 100% %util with an aqu-sz of 32 are saturated and carry the same backlog.
- C. The same aqu-sz of 32 means requests served in parallel on sdb and a slow device on sdc.
- D. %util of 100% says only that each disk always had a request in flight; for a parallel device it shows no limit.
- E. On sdc, about 38 of the 40 ms are spent at or below the virtual disk, not in Linux.
- F. sdc has the same queue as sdb and a higher await, so the cause of its await is its Linux queue.
- G. await is the response time of the device, so the array behind sdc answers in about 40 ms.
- H. On sdc, only about 1.6 of the 32 requests wait in Linux before they reach the virtual disk.
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
- A true: Little's Law: sdb 8,000 x 0.004 = 32 and sdc 800 x 0.040 = 32.
- B false: aqu-sz alone does not show a backlog, and %util at 100% does not show a limit for a device that serves requests in parallel. Neither engineer is right.
- C true: 32 requests in service at 8,000 I/Os per second, against 32 requests on a slow device at 800 I/Os per second.
- D true: %util is the share of the time with at least one I/O in flight (field 10). For modern SSDs and arrays, 100% does not show a limit.
- E true: await 40 ms against 38 ms in vCenter: about 2 ms in Linux, 38 ms below the guest. The time is spent on the storage path: the datastore DS-ARCH, the array or the path.
- F false: only about 1.6 requests wait in Linux; the time of sdc is below the guest.
- G false: await covers the queue in Linux, the virtual adapter, the VMkernel and the storage; the vCenter latency shows 38 ms below the guest, and even that includes the VMkernel.
- H true: requests at the virtual disk are 800 x 0.038 = 30.4 of the 32; 32 - 30.4 = 1.6 wait in Linux.
- I false: the vCenter virtual disk latency starts at the virtual disk; the wait in Linux before it is not in it.
- J false: a request counts from the moment it enters the request queue until it finishes, whether it waits or is served.
- K true: only about 1.6 requests wait in Linux; a larger queue only holds more requests in front of a slow device.
- L false: the default device queue depth of vmw_pvscsi is 64, and only about 30 requests are at the virtual disk. No request waits for a free slot.
- M false: await rising with the I/O rate flat is the sign of saturation; spare capacity shows as the I/O rate rising with await flat. For sdb, nothing to tune unless the database needs a response time below 4 ms.
- N true: read device, kernel and queue latency of DS-ARCH in esxtop, the array load and the schedule of the backups; ask whether the archive workload needs better than 38 ms.
- O false: 4.0 ms against 3.8 ms, so Linux adds about 0.2 ms; 8,000 x 0.0038 = 30.4 of the 32 requests are at the virtual disk, in service, and only about 1.6 are in Linux. Not a backlog.

## Notes
- Public source: Linux kernel documentation, I/O statistics fields: field 9 counts requests in progress, field 10 the time with at least one request in progress, field 11 the weighted time. sysstat iostat(1) manual page: aqu-sz is the average queue length of the requests issued to the device; await includes the time in the queue and the time in service; %util for devices serving requests in parallel, such as RAID arrays and modern SSDs, does not reflect their performance limits. aqu-sz = I/O rate x await is Little's Law.
- Why one answer: the arithmetic ties the columns, and the vCenter latency shows how much of await is below the guest.
- Debatable risk: that the vCenter virtual disk latency starts at the virtual disk and excludes the wait in Linux is read from the counter definitions and the knowledge file; the vSphere API reference was not read for this. The numbers are chosen so that the arithmetic is exact.
- Prepared with author question Q194 (the reading of the guest disk queue).
- Converted from judged to multiple choice (Q199 F, 2026-11-14). The prompt now states that vmw_pvscsi runs with its default queue depths, so option L is decidable (64 per device, Broadcom KB 343323). Review 2026-11-14: options M and O turned into near-miss false options that test the same facts (the signature of spare capacity; requests in service on sdb), so fewer options are true.

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
knowledge_main: guest-os/storage/linux-storage-io-path
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for author question Q194 (project/plan.md)"
misconception_type: [layer-confusion, tool-confusion]
status: draft
```
