# Windows disk queue length of 48

## Prompt
- A Windows Server 2022 VM with one virtual disk on a paravirtual SCSI (PVSCSI) controller.
- Performance Monitor, PhysicalDisk, same 5 minutes: Disk Transfers/sec 3,000; Avg. Disk sec/Transfer 0.016; Avg. Disk Queue Length 48.
- vCenter, the same 5 minutes: virtual disk latency about 15 ms.
- A colleague says: "48 requests are waiting inside Windows before they reach the VM, so the Guest OS is the bottleneck. Storage is fine, its latency is only 15 ms."

Which statements are correct?

- A. The 48 requests are waiting inside Windows above the driver and have not reached the virtual disk yet.
- B. The numbers do not support the colleague's conclusion that the Guest OS is the bottleneck.
- C. A queue length above 2 per disk shows a bottleneck in the Guest OS, whatever the latency.
- D. The numbers show requests waiting in Windows for a free slot of the PVSCSI adapter.
- E. About 45 requests (3,000 x 0.015 s) are at or below the virtual disk; the other 3 are within tool error.
- F. Windows sees 16 ms per transfer and vCenter 15 ms: nearly all the time per I/O is spent at or below the virtual disk.
- G. Because the vCenter latency is only 15 ms, storage can be ruled out as the source of the queue.
- H. Avg. Disk Queue Length is Disk Transfers/sec times Avg. Disk sec/Transfer here: 3,000 x 0.016 = 48.
- I. At the same 3,000 IOPS, lower storage latency would lower the queue length.
- J. The counter also counts requests in service at the virtual disk and the array, or on their way back.
- K. The vCenter virtual disk latency of 15 ms includes the time requests waited in Windows queues.

## Likely wrong answer
- A: "48 I/Os are queued in Windows and have not reached the VM or the storage."
- C: "A queue above 2 per disk is a bottleneck."
- G: "Storage is fine at 15 ms, so the queue is a Windows problem."

## Expected key points
- Answer: B, E, F, H, I, J.
- A is false: the misconception; the counter counts requests active below the driver that takes the statistics, including I/O already sent to the virtual disk and the storage.
- B is true: the conclusion needs a queue that has not reached the device, which the numbers do not show.
- C is false: Microsoft's "about 2 per physical disk" counts spindles; it cannot be applied to a virtual disk on shared storage.
- D is false: waiting for an adapter slot needs a large remainder with the requests at the virtual disk at the adapter queue depth (PVSCSI default 64 per device); here about 45 are at the disk and the remainder is about 3.
- E is true: requests at the virtual disk = I/O rate x virtual disk latency = 45; a remainder of a few requests is within the difference between two tools that sample and average separately, not a count of blocked requests.
- F is true: when the guest time per I/O is close to the vCenter virtual disk latency, the time is spent in the virtual storage path and the array; the Guest OS adds about 1 ms.
- G is false: the queue follows from the time per I/O, which is spent almost all in storage; the 48 is not independent evidence of a queue in the Guest OS.
- H is true: Windows derives Avg. Disk Queue Length from Disk Transfers/sec x Avg. Disk sec/Transfer (Little's Law); 3,000 x 0.016 = 48, exactly the reported value.
- I is true: the 48 is the concurrency that 3,000 IOPS at 16 ms produces; it follows from the latency, so lower latency at the same IOPS lowers it.
- J is true: a request can wait in a lower queue, be in service at the virtual or physical device, or be completed and on the way back; the counter does not separate waiting from service.
- K is false: the vCenter virtual disk latency starts at the virtual disk; time waiting in Guest OS queues is not in it.

## Notes
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
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
answer_type: deterministic
answer: [B, E, F, H, I, J]
misconception: [A, C, G]
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
