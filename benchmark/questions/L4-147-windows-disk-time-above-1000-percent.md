# Windows % Disk Time above 1,000%

## Prompt
- The Windows administrator of the file-processing VM fp-app-03 (Windows Server 2022) says Performance Monitor proves the disk is overloaded inside Windows, and that the storage is fine.
- The data disk E: is the VM's scsi0:1, on a Paravirtual SCSI controller.
- He logged [the PhysicalDisk counters with typeperf](0418/typeperf-physicaldisk.csv), every 20 seconds for 10 minutes. You export [the VM's Virtual disk chart](0418/vcenter-vm-virtual-disk-realtime.csv) from the vSphere Client, Real-time, the same 10 minutes. Its chart legend (not in the export) gives the units: rates in KBps, latencies in ms.

Which statements are correct?

- A. % Disk Time is the average queue length times 100, so it passes 100% whenever more than one request is active on average.
- B. % Disk Time above 100% shows a counter error.
- C. In the typeperf export, Avg. Disk Queue Length equals Disk Transfers/sec times Avg. Disk sec/Transfer.
- D. The Windows time per transfer is close to the vCenter read latency, so nearly all the time per I/O is spent at or below the virtual disk.
- E. Avg. Disk Queue Length counts only the requests that have not left Windows yet.
- F. Keeping Avg. Disk Queue Length below 2 is the right target for this virtual disk.
- G. Disk transfers per second times the vCenter read latency accounts for most of the Windows queue.
- H. Add vCPUs to the VM so that Windows clears its disk queue faster.
- I. If the storage answered twice as fast at the same transfer rate, % Disk Time would fall to about half.
- J. The vSphere Client read latency already contains the wait in the Windows Storport queue.
- K. Windows disk counters cannot be compared with the vCenter virtual disk counters.
- L. The typeperf export shows Windows spending far longer per transfer than the vCenter Read latency.

## Likely wrong answer
E and F: the queue is waiting inside Windows, and a queue above 2 per disk is the problem. Or B: % Disk Time cannot pass 100%.

## Expected key points
- Answer: A, C, D, G, I.
- A true: % Disk Time is Avg. Disk Queue Length x 100, shown as a percentage; it exceeds 100% whenever the average queue is above 1. In the export `PhysicalDisk(1 E:)\% Disk Time` is 1,000 or more (about 2,400) in every sample, 100 times `Avg. Disk Queue Length`.
- B false: the counter is right; it is a queue length shown as a percentage.
- C true: reading. Windows derives Avg. Disk Queue Length from Disk Transfers/sec x Avg. Disk sec/Transfer (Little's law); in every sample after the first the export shows it within 5% (about 2,400 x 0.010 s = 24).
- D true: reading. `Avg. Disk sec/Transfer` (about 0.010 s) is within 15% of `Read latency for scsi0:1` (9-10 ms) in the same minutes, and `Disk Transfers/sec` within 10% of `Average read requests per second for scsi0:1`; the workload is reads only. When the guest time per I/O is close to the vCenter virtual disk latency, the time is spent in ESXi queues, the storage path and the array; Windows adds little.
- E false: the misconception. The counter counts every request below the partition manager: waiting, in service at the device, and on the way back.
- F false: the Microsoft guideline of about 2 per disk counts physical spindles; a virtual disk has none.
- G true: requests at or below the virtual disk = transfers per second x vCenter latency: about 2,400 x 0.009 s = 22 of a queue of about 24, at least 80% in every sample; the remainder is not a count of requests blocked in Windows.
- H false: the wrong action. The time per I/O is spent below the virtual disk; more vCPUs do not shorten it (`Processor(_Total)\% Processor Time` stays below 20%).
- I true: % Disk Time is the queue x 100, and the queue is transfers x time per transfer; nearly all of that time is below the virtual disk, so halving it about halves the queue.
- J false: the vCenter virtual disk latency starts at the virtual disk; time waiting in Windows queues, Storport included, is not in it.
- K false: the over-correction. Comparing the Windows time per I/O with the vCenter latency for the same period is the first test of where the time is spent.
- L false: reading. `Avg. Disk sec/Transfer` is within 15% of the vCenter `Read latency for scsi0:1`.

## Notes
- Paired with the theory question 0311 (theory and practical; design.md, section 3.9).
- No option rests on the Paravirtual SCSI queue depth.
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item C23 (origin: synthetic). Counts only after author approval.
- Review 2026-11-15: F, I and J reworded away from 0311; L (a false screen reading) added. Key unchanged: A, C, D, G, I.
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
answer: [A, C, D, G, I]
misconception: [E, F]
misconception_type: [layer-confusion]
pair: "0311"
status: draft
```
