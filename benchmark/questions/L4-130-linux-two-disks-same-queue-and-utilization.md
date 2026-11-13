# Linux: two disks with the same queue and the same utilization

## Prompt
- A Linux VM (RHEL 9, kernel 5.14, 8 vCPUs) has two virtual disks on a Paravirtual SCSI controller, driver vmw_pvscsi. The disk sdb holds a PostgreSQL database on the datastore DS-FAST. The disk sdc holds the archive of the write-ahead log and the backups on the datastore DS-ARCH, an older array.
- During a 5-minute window, `iostat -x 300 2` reports for the second interval:

| Device | r/s + w/s | await (ms) | aqu-sz | %util |
|---|---|---|---|---|
| sdb | 8,000 | 4.0 | 32.0 | 100 |
| sdc | 800 | 40.0 | 32.0 | 100 |

- vCenter, the same 5 minutes, virtual disk latency: sdb 3.8 ms, sdc 38 ms. CPU utilization inside Linux is 20%.
- Engineer 1 says: "Both disks show 100% utilization and the same queue of 32, so both are saturated and have the same backlog. Raise nr_requests on both."
- Engineer 2 says: "The await of sdb is 4 ms, which is fine. The await of sdc is 40 ms. The queue is the same, so the cause is the Linux queue of sdc. Tune it."

Is either engineer right? What do the four columns say about each disk, where is the time of sdc spent, and what do you check next?

## Likely wrong answer
"Both disks have 100% utilization and an aqu-sz of 32, so both are saturated and the queue is the problem; raise the queue size (nr_requests or the queue depth) on both."

## Expected key points
- Neither engineer is right.
- aqu-sz is the I/O rate x await (Little's Law): sdb 8,000 x 0.004 = 32 and sdc 800 x 0.040 = 32. The same aqu-sz has opposite meanings: 32 requests served in parallel at 8,000 I/Os per second, and 32 requests on a slow device at 800 I/Os per second. aqu-sz alone does not show a backlog.
- %util is the share of the time with at least one I/O in flight. For devices that serve requests in parallel, such as modern SSDs and arrays, 100% does not show a limit. Both disks are never idle; that is all it says.
- sdb: await 4.0 ms is close to the vCenter latency of 3.8 ms, so Linux adds about 0.2 ms. The requests at the virtual disk are 8,000 x 0.0038 = 30.4 of the 32: the queue is requests in service, not a backlog. Whether sdb has headroom shows when the load rises: the I/O rate rises with await flat. Saturation shows as await rising with the I/O rate flat.
- sdc: await 40 ms against 38 ms in vCenter, so about 2 ms is in Linux and 38 ms is below the guest. The requests at the virtual disk are 800 x 0.038 = 30.4 of the 32, so only about 1.6 wait in Linux. The time is spent on the storage path: the datastore DS-ARCH, the array or the path.
- Raising the Linux queue size does not help sdc: only about 1.6 requests wait in Linux, and a larger queue would only hold more requests in front of a slow device.
- Next: for sdc, read the datastore latency of DS-ARCH and its parts (device, kernel and queue latency in esxtop), the array load and the schedule of the backups; ask whether the archive workload needs better than 38 ms. For sdb, nothing to tune unless the database needs a response time below 4 ms.

## Notes
- Public source: Linux kernel documentation, I/O statistics fields: field 9 counts requests in progress, field 10 the time with at least one request in progress, field 11 the weighted time. sysstat iostat(1) manual page: aqu-sz is the average queue length of the requests issued to the device; await includes the time in the queue and the time in service; %util for devices serving requests in parallel, such as RAID arrays and modern SSDs, does not reflect their performance limits. aqu-sz = I/O rate x await is Little's Law.
- Why one answer: the arithmetic ties the columns, and the vCenter latency shows how much of await is below the guest.
- Debatable risk: that the vCenter virtual disk latency starts at the virtual disk and excludes the wait in Linux is read from the counter definitions and the knowledge file; the vSphere API reference was not read for this. The numbers are chosen so that the arithmetic is exact.
- Prepared with author question Q194 (the reading of the guest disk queue).

## Metadata
```yaml
id: "0360"
title: "Linux: two disks with the same queue and the same utilization"
product: [linux, vsphere]
technology: [storage]
task: troubleshoot
level: 400
answer_type: judged
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
