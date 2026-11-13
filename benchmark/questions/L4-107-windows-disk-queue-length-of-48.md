# Windows disk queue length of 48

## Prompt
- A Windows Server 2022 VM with one virtual disk on a paravirtual SCSI (PVSCSI) controller.
- Performance Monitor, PhysicalDisk, same 5 minutes: Disk Transfers/sec 3,000; Avg. Disk sec/Transfer 0.016; Avg. Disk Queue Length 48.
- vCenter, the same 5 minutes: virtual disk latency about 15 ms.
- A colleague says: "48 requests are waiting inside Windows before they reach the VM, so the Guest OS is the bottleneck. Storage is fine, its latency is only 15 ms."

Is this conclusion supported by the numbers? What does Avg. Disk Queue Length show here?

## Likely wrong answer
"48 I/Os are queued in Windows above the driver and have not reached the VM or the storage." Or: "A queue above 2 per disk is a bottleneck."

## Expected key points
- Not supported.
- Avg. Disk Queue Length is derived, not measured: Disk Transfers/sec x Avg. Disk sec/Transfer (Little's Law). Here 3,000 x 0.016 = 48, exactly the reported value.
- The counter counts requests that are active below the driver that takes the statistics: waiting in lower queues, in service at the device or array, or completed and on the way back. It includes I/O already sent to the virtual disk and the storage, not only I/O waiting inside Windows.
- Windows measures 16 ms per transfer and vCenter shows about 15 ms: nearly all of the time per I/O is spent below the Guest OS, in the virtual storage path and the array. The Guest OS adds about 1 ms.
- The 48 is the concurrency that 3,000 IOPS at 16 ms produces. It follows from the latency; it is not independent evidence of a queue in the Guest OS. Lower storage latency at the same IOPS would lower the counter.
- Microsoft's "about 2 per physical disk" guidance counts spindles; it cannot be applied to a virtual disk on shared storage.

## Notes
- Public source: Microsoft Learn (archived page), "Using Storage-related Parameters and Performance Counters" (https://learn.microsoft.com/previous-versions/dn567651(v=vs.85)), page date 2016-05-02, updated 2021-12-02, Windows Server 2012 R2 era. It states that Average Disk Queue Length is equal to (Disk Transfers/sec) x (Disk sec/Transfer), based on Little's Law, that the requests may be in service and not necessarily queued, and that the guideline of two per physical disk assumes known physical disks.
- Why one answer: 3,000 x 0.016 = 48 shows the counter is the product of two other counters, and the vendor says it includes requests in service. The conclusion needs a queue that has not reached the device, which the numbers do not show.
- Debatable risk: the page is archived and describes Windows Server 2012 R2. The derivation is a property of the counter definition; the prompt does not ask for a threshold. The knowledge file guest-os/storage/disk-queue said the queue is "above the SCSI driver"; it was corrected on 2026-11-13 to the Microsoft reading (author question Q194).

## Metadata
```yaml
id: "0311"
title: "Windows disk queue length of 48"
product: [windows, vsphere]
technology: [storage]
task: troubleshoot
level: 400
answer_type: judged
input: [text]
object: [guest-os, vm]
tool: [guest-os-tools, vcenter]
knowledge:
  - guest-os/storage/disk-queue
  - guest-os/guest-os-alerts
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
  - guest-os/storage/windows-storage-io-path
knowledge_main: guest-os/storage/disk-queue
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
misconception_type: [layer-confusion]
status: draft
```
