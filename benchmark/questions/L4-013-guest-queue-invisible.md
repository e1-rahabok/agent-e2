# Guest queue invisible to the hypervisor

## Prompt
- Oracle on a Windows VM is slow.
- Windows Performance Monitor, 10:00-10:30, data disk: Avg. Disk Queue Length 150, Disk Transfers/sec 16,000, Avg. Disk sec/Transfer 9.4 ms.
- vCenter, same window, the same virtual disk: 16,000 IOPS, latency 4 ms. The VM has one Paravirtual SCSI adapter at its default queue depth.
- The storage team says storage is fine, so it is not an infrastructure problem.

Which statements about the storage team's conclusion are correct?

- A. I/O still waiting inside Windows has not reached the virtual disk, so vCenter IOPS can under-report what Oracle asks for.
- B. Normal VM disk IOPS and latency in vCenter show the I/O path is healthy, so the slowness is not an infrastructure problem.
- C. The VM's disk latency in vCenter includes the time an I/O spends queued inside Windows.
- D. About 5.4 ms of the 9.4 ms that Windows measures per I/O is spent above the virtual disk, out of the storage team's sight.
- E. The Windows disk queue and the VM's outstanding I/O in vCenter count the same requests.
- F. VMware Tools adjusts the Windows disk counters so that they include the time ESXi holds each I/O.
- G. Windows Disk Queue Length counts only the I/O that Windows has not yet sent to the virtual disk.
- H. Windows does not see where ESXi holds its I/O; it only sees each I/O take longer.

## Likely wrong answer
- B: "vSphere metrics are normal, so the storage path is healthy."

## Expected key points
- Answer: A, D, H.
- A is correct: queues inside the Guest OS (disk queue, driver queue) are not visible to the hypervisor. The I/O has not been sent down yet, so VM-level IOPS can under-report real demand.
- B is wrong: the queue inside the guest is invisible to vCenter, so normal VM metrics leave part of the path unchecked. Look inside the Guest OS too.
- C is wrong: the vCenter virtual disk latency starts at the virtual disk; the wait in the guest before it is not in it.
- D is correct: the Windows time per I/O covers the whole path, while the vCenter latency starts at the virtual disk, so 9.4 - 4 = 5.4 ms is spent above it: in Windows queues, the adapter driver and the completion path (here mostly the 150 - 64 = 86 requests that wait for a free slot).
- E is wrong: requests at the virtual disk equal the I/O rate times the vCenter disk latency, here 16,000 × 0.004 = 64; the Windows queue of 150 also counts requests that still wait in Windows.
- F is wrong: VMware Tools adds new metrics inside the guest; it does not change the existing Windows counters, which stay unaware of virtualization.
- G is wrong: the counter also counts requests in service at the device and requests on their way back up the stack. It is a Little's Law value: I/O rate times time per I/O.
- H is correct: Windows cannot see where ESXi holds its I/O; it feels the hold only as a longer time per I/O.

## Notes
- Tests: visibility of the layers.
- The stem numbers obey Little's Law: 16,000/s × 9.4 ms = 150 in Windows; 16,000/s × 4 ms = 64 at the virtual disk (the Paravirtual SCSI default of 64 per device in Windows), so about 86 requests wait in the guest for a free slot.
- Changed in the 2026-11-15 audit: evidence in the stem (PerfMon and vCenter values); E reworded without "equally high" (still false); old H (Little's Law at the virtual disk) dropped (redundancy #45: the pair 0028/0416 holds it), old I relettered to H. Letter map: A-G unchanged, I -> H. Answer A, D, H, I -> A, D, H.
- Changed in the 2026-11-16 re-review: D ("normal VM metrics do not prove the path is healthy") was the negation of B; D now tests where the time per I/O is spent (Windows time per I/O against the vCenter latency, disk-queue section Interpretation). Still true.

## Metadata
```yaml
id: "0026"
title: "Guest queue invisible to the hypervisor"
product: [vsphere]
technology: [storage]
input: [text]
task: troubleshoot
knowledge:
  - vsphere/architecture/vm-vs-guest-os
  - vsphere/technology/storage/metrics/virtual-motherboard/iops
  - guest-os/storage/disk-queue
object: [vm, guest-os]
tool: [vcenter, guest-os-tools]
knowledge_main: vsphere/architecture/vm-vs-guest-os
attachments: []
origin: book
source_path: "The World of Metrics > Metrics Nuances: Visibility (layers A–D diagram)."
answer_type: deterministic
answer: [A, D, H]
misconception: [B]
level: 400                      # author 2026-11-05
misconception_type: [layer-confusion]
status: draft
```
