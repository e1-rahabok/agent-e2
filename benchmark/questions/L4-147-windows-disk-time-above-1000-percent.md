# Windows % Disk Time above 1,000%

## Prompt
- The Windows administrator of a file-processing VM says Performance Monitor proves the disk is overloaded inside Windows, and that the storage is fine.
- See [the Performance Monitor report of the data disk](0418/perfmon-physicaldisk-report.png) and [the vSphere Client virtual disk chart of the same disk](0418/vcenter-vm-virtual-disk-real-time.png), same minutes.

Which statements are correct?

- A. % Disk Time is the average queue length times 100, so it passes 100% whenever more than one request is active on average.
- B. % Disk Time above 100% shows a counter error.
- C. In this report, Avg. Disk Queue Length equals Disk Transfers/sec times Avg. Disk sec/Transfer.
- D. The Windows time per transfer is close to the vCenter read latency, so nearly all the time per I/O is spent at or below the virtual disk.
- E. Avg. Disk Queue Length counts only the requests that have not left Windows yet.
- F. Keeping Avg. Disk Queue Length below 2 is the right target for this virtual disk.
- G. Disk transfers per second times the vCenter read latency accounts for most of the Windows queue.
- H. Add vCPUs to the VM so that Windows clears its disk queue faster.
- I. If the storage answered twice as fast at the same transfer rate, % Disk Time would fall to about half.
- J. The vSphere Client read latency already contains the wait in the Windows Storport queue.
- K. Windows disk counters cannot be compared with the vCenter virtual disk counters.
- L. The report shows Windows spending far longer per transfer than the vCenter Read latency.

## Input to supply
- Product and version: Windows Server 2022 VM on vSphere 9.1 (vSphere Client 9.1); one data virtual disk (E:) on a Paravirtual SCSI controller.
- How to produce it: a read-only random load with a deep queue on a datastore with moderate latency (3-15 ms), for example `diskspd -b8K -d900 -o12 -t2 -r -w0 -Sh E:\test.dat` (create the file first). Wait 2 minutes before capturing.
- Screen 1, Performance Monitor, Report view, sample interval 60 seconds, counters PhysicalDisk(the data disk): % Disk Time, Avg. Disk Queue Length, Disk Transfers/sec, Avg. Disk sec/Transfer. Save as `0418/perfmon-physicaldisk-report.png`.
- Screen 2, vSphere Client > the VM > Monitor > Performance > Advanced > Virtual disk, Chart Options: Real-time, object the data disk (scsiM:N), counters Read latency and Average read requests per second, with the legend table. Capture within the same minutes as screen 1. Save as `0418/vcenter-vm-virtual-disk-real-time.png`.
- Condition the key depends on: % Disk Time 1,000% or more; Avg. Disk Queue Length within 5% of Disk Transfers/sec x Avg. Disk sec/Transfer; Avg. Disk sec/Transfer (in ms) within 15% of the vCenter Read latency of the same minutes; Disk Transfers/sec within 10% of the vCenter read requests per second.
- Masking: mask every VM, host, datastore and cluster name, and the computer name in the report.

## Likely wrong answer
E and F: the queue is waiting inside Windows, and a queue above 2 per disk is the problem. Or B: % Disk Time cannot pass 100%.

## Expected key points
- Answer: A, C, D, G, I.
- A true: % Disk Time is Avg. Disk Queue Length x 100, shown as a percentage; it exceeds 100% whenever the average queue is above 1.
- B false: the counter is right; it is a queue length shown as a percentage.
- C true: Windows derives Avg. Disk Queue Length from Disk Transfers/sec x Avg. Disk sec/Transfer (Little's law); the report shows it within 5%.
- D true: when the guest time per I/O is close to the vCenter virtual disk latency, the time is spent in ESXi queues, the storage path and the array; Windows adds little.
- E false: the misconception. The counter counts every request below the partition manager: waiting, in service at the device, and on the way back.
- F false: the Microsoft guideline of about 2 per disk counts physical spindles; a virtual disk has none.
- G true: requests at or below the virtual disk = transfers per second x vCenter latency; with the two latencies within 15%, that is most of the queue, and the remainder is not a count of requests blocked in Windows.
- H false: the wrong action. The time per I/O is spent below the virtual disk; more vCPUs do not shorten it.
- I true: % Disk Time is the queue x 100, and the queue is transfers x time per transfer; nearly all of that time is below the virtual disk, so halving it about halves the queue.
- J false: the vCenter virtual disk latency starts at the virtual disk; time waiting in Windows queues, Storport included, is not in it.
- K false: the over-correction. Comparing the Windows time per I/O with the vCenter latency for the same period is the first test of where the time is spent.
- L false: the screen reading. Avg. Disk sec/Transfer is within 15% of the vCenter Read latency.

## Notes
- Paired with the theory question 0311 (theory and practical; design.md, section 3.9).
- No option rests on the Paravirtual SCSI queue depth (open question Q195).
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item C23 (origin: synthetic). Counts only after author approval.
- Review 2026-11-15: F, I and J reworded away from 0311; L (a false screen reading) added. Key unchanged: A, C, D, G, I.

## Metadata
```yaml
id: "0418"
title: "Windows % Disk Time above 1,000%"
product: [vsphere, windows]
technology: [storage]
task: troubleshoot
level: 400
answer_type: deterministic
input: [screenshot]
object: [vm, guest-os]
tool: [vcenter, guest-os-tools]
knowledge:
  - guest-os/storage/windows-storage-io-path
  - guest-os/storage/disk-queue
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
knowledge_main: guest-os/storage/windows-storage-io-path
attachments:
  - 0418/perfmon-physicaldisk-report.png
  - 0418/vcenter-vm-virtual-disk-real-time.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C23"
answer: [A, C, D, G, I]
misconception: [E, F]
misconception_type: [layer-confusion]
pair: "0311"
status: awaiting-input
```
