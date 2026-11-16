# Windows % Disk Time above 1,000%

## Prompt
- The Windows administrator of the file-processing VM fp-app-03 (Windows Server 2022) says Performance Monitor proves the disk is overloaded inside Windows, and that the storage is fine.
- The data disk E: is the VM's scsi0:1, on a Paravirtual SCSI controller.
- He logged [the PhysicalDisk counters with typeperf](0418/typeperf-physicaldisk.csv), every 20 seconds for 10 minutes. You export [the VM's Virtual disk chart](0418/vcenter-vm-virtual-disk-realtime.csv) from the vSphere Client, Real-time, the same 10 minutes. Its chart legend (not in the export) gives the units: rates in KBps, latencies in ms.

Which statements are correct?

- A. % Disk Time is the average queue length times 100, so it passes 100% once the average queue is above 1.
- B. % Disk Time above 100% shows a counter error, since a disk cannot be busier than all the time.
- C. In every typeperf sample, Avg. Disk Queue Length is within 1% of Disk Transfers/sec times Avg. Disk sec/Transfer.
- D. Windows time per transfer is close to the vCenter read latency: nearly all of it is at or below the virtual disk.
- E. Avg. Disk Queue Length counts only the requests that have not left Windows yet.
- F. Keeping Avg. Disk Queue Length below 2 is the right target for this virtual disk.
- G. A 1 MB read would add as much to Avg. Disk Queue Length as one of these 8 KB reads.
- H. Add vCPUs to the VM so that Windows clears its disk queue faster.
- I. If the storage answered twice as fast at the same transfer rate, % Disk Time would fall to about half.
- J. The vSphere Client read latency already contains the wait in the Windows Storport queue.
- K. Windows disk counters cannot be compared with the vCenter virtual disk counters.
- L. The PhysicalDisk time per transfer in the typeperf export includes the time spent in the NTFS file system driver.

## Answers
A, C, D, G, I

## Explanation
- A true: % Disk Time is Avg. Disk Queue Length x 100, shown as a percentage; it exceeds 100% whenever the average queue is above 1. In the export `PhysicalDisk(1 E:)\% Disk Time` is 1,000 or more (about 2,400) in every sample, 100 times `Avg. Disk Queue Length`.
- B false: the counter is right; it is a queue length shown as a percentage.
- C true: reading. Windows derives Avg. Disk Queue Length from Disk Transfers/sec x Avg. Disk sec/Transfer (Little's law); in every sample after the first the export shows it within 1% (about 2,400 x 0.010 s = 24).
- D true: reading. `Avg. Disk sec/Transfer` (about 0.010 s) is within 15% of `Read latency for scsi0:1` (9-10 ms) in the same minutes, and `Disk Transfers/sec` within 10% of `Average read requests per second for scsi0:1`; the workload is reads only. When the guest time per I/O is close to the vCenter virtual disk latency, the time is spent in ESXi queues, the storage path and the array; Windows adds little.
- E false: the misconception. The counter counts every request below the partition manager: waiting, in service at the device, and on the way back.
- F false: the Microsoft guideline of about 2 per disk counts physical spindles; a virtual disk has none.
- G true: the queue counts requests, not bytes; each request counts as one while active, whatever its size. In the vCenter export `Read rate for scsi0:1` (KBps) is 8 times the read requests per second in every row: 8 KB reads.
- H false: the wrong action. The time per I/O is spent below the virtual disk; more vCPUs do not shorten it (`Processor(_Total)\% Processor Time` stays below 20%).
- I true: % Disk Time is the queue x 100, and the queue is transfers x time per transfer; nearly all of that time is below the virtual disk, so halving it about halves the queue.
- J false: the vCenter virtual disk latency starts at the virtual disk; time waiting in Windows queues, Storport included, is not in it.
- K false: the over-correction. Comparing the Windows time per I/O with the vCenter latency for the same period is the first test of where the time is spent.
- L false: the partition manager collects the PhysicalDisk counters, so they cover the request from that layer down (disk class driver, Storport, adapter driver, device and back) and leave out the file system above it.
- Misconception: E and F: the queue is waiting inside Windows, and a queue above 2 per disk is the problem. Or B: % Disk Time cannot pass 100%.

## Notes
- Paired with the theory question 0311 (theory and practical; design.md, section 3.9).
- No option rests on the Paravirtual SCSI queue depth.
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item C23 (origin: synthetic). Counts only after author approval.
- Changed in the 2026-11-15 audit: G (requests at the virtual disk = transfers x vCenter latency; Little's Law at the virtual disk is kept by 0028/0416, redundancy #45) replaced in place by the true fact that each request counts once in the queue whatever its size (windows-storage-io-path, Control plane and Misconceptions). The exports cannot carry an outstanding-IO column without regenerating them, so the stem was not changed. Key unchanged.
- Changed on 2026-11-16: L (the negation of D) replaced by the false claim that the PhysicalDisk counters include the file system (windows-storage-io-path, Collection point of the disk counters); C states the 1% match instead of "equals". Key unchanged.
- 2026-11-15: screenshots replaced by generated exports (project/practical-questions-as-exports-2026-11-15.md): typeperf instead of the Performance Monitor report view, at 20-second samples to line up with vCenter Real-time.

## Metadata
```yaml
id: "0418"
title: "Windows % Disk Time above 1,000%"
product: [vsphere, windows]
technology: [storage]
task: troubleshoot
level: 400
answer_type: deterministic
input: [table]
object: [vm, guest-os]
tool: [vcenter, guest-os-tools]
knowledge:
  - guest-os/storage/windows-storage-io-path
  - guest-os/storage/disk-queue
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
knowledge_main: guest-os/storage/windows-storage-io-path
attachments:
  - 0418/typeperf-physicaldisk.csv
  - 0418/vcenter-vm-virtual-disk-realtime.csv
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C23"
misconception: [E, F]
misconception_type: [layer-confusion]
pair: "0311"
status: draft
```
