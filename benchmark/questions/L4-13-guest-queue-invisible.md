# Guest queue invisible to the hypervisor

## Prompt
- Oracle on a Windows VM is slow.
- Windows shows a high Disk Queue Length.
- In vCenter, the VM's disk IOPS and disk latency look normal.
- The storage team says storage is fine, so it is not an infrastructure problem.

Which statements about the storage team's conclusion are correct?

- A. I/O still waiting inside Windows has not reached the virtual disk, so vCenter IOPS can under-report what Oracle asks for.
- B. Normal VM disk IOPS and latency in vCenter show the I/O path is healthy, so the slowness is not an infrastructure problem.
- C. The VM's disk latency in vCenter includes the time an I/O spends queued inside Windows.
- D. Normal disk metrics at the VM level do not prove the I/O path is healthy from the application down.
- E. A high Windows disk queue shows up in vCenter as an equally high count of outstanding I/O on the VM.
- F. VMware Tools adjusts the Windows disk counters so that they include the time ESXi holds each I/O.
- G. Windows Disk Queue Length counts only the I/O that Windows has not yet sent to the virtual disk.
- H. The I/O rate times the vCenter disk latency counts the requests at the virtual disk; only the Windows queue above it can wait in the guest.
- I. Windows does not see where ESXi holds its I/O; it only sees each I/O take longer.

## Likely wrong answer
- B: "vSphere metrics are normal, so the storage path is healthy."

## Expected key points
- Answer: A, D, H, I.
- A true: queues inside the Guest OS (disk queue, driver queue) are not visible to the hypervisor. The I/O has not been sent down yet, so VM-level IOPS can under-report real demand.
- B false: the queue inside the guest is invisible to vCenter, so normal VM metrics leave part of the path unchecked. Look inside the Guest OS too.
- C false: the vCenter virtual disk latency starts at the virtual disk; the wait in the guest before it is not in it.
- D true: normal vSphere metrics do not prove the I/O path is healthy end to end.
- E false: requests at the virtual disk equal the I/O rate times the vCenter disk latency. The guest queue also counts requests that still wait in Windows, so the two need not match.
- F false: VMware Tools adds new metrics inside the guest; it does not change the existing Windows counters, which stay unaware of virtualization.
- G false: the counter also counts requests in service at the device and requests on their way back up the stack. It is a Little's Law value: I/O rate times time per I/O.
- H true: requests at the virtual disk are the I/O rate times the vCenter latency (Little's Law); only the excess of the guest queue over that figure is spent above the virtual disk. A large excess means requests wait for a free slot of the virtual adapter.
- I true: the mental model of the two views: the Guest OS sees its own queues and its own use; the VM view sees the guest's use, hypervisor work for the VM and unmet demand. The guest only feels the hypervisor's wait as slowness.

## Notes
- Tests: Visibility layers (principle + diagram).
- Converted from judged to multiple choice (Q199 F, 2026-11-14). Knowledge added: guest-os/storage/disk-queue (what Disk Queue Length counts; the split by Little's Law, author question Q194).

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
answer: [A,D,H,I]
misconception: [B]
level: 400                      # author 2026-11-05
misconception_type: [layer-confusion]
status: draft
```
