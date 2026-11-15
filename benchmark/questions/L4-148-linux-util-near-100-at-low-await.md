# Linux %util near 100% at a low await

## Prompt
- The Linux administrator of a database VM says iostat shows the data disk is saturated, and asks for a faster datastore.
- See [the iostat output](0419/linux-iostat-data-disk.png) and [the vSphere Client virtual disk chart of the same disk](0419/vcenter-vm-virtual-disk-real-time.png), same minutes.

Which statements are correct?

- A. %util measures the share of time the disk had any I/O outstanding, not how much more it could take.
- B. %util near 100% means the disk is saturated.
- C. On this screen, r/s times r_await gives about the aqu-sz shown.
- D. r_await is close to the vCenter Read latency, so Linux adds little time above the virtual disk.
- E. A request that the virtual disk is already serving no longer counts in aqu-sz.
- F. Move the disk to a faster datastore: %util shows the device has no headroom left.
- G. If the disk were the limit, more load would raise r_await while r/s stayed about the same.
- H. r_await is the time the array behind the datastore takes to answer a read.
- I. %util tells nothing about any Linux disk, whatever the device behind it.
- J. The vSphere Client read latency already contains the time in the blk-mq queues.
- K. On this screen, r_await is more than twice the vCenter Read latency of the same minute.

## Input to supply
- Product and version: a Linux VM (RHEL 9 or another distribution with kernel 5.0 or later, sysstat 12 or later) on vSphere 9.1 (vSphere Client 9.1); one data virtual disk (sdb) on a Paravirtual SCSI controller, on an all-flash datastore.
- How to produce it: `fio --name=r --filename=/dev/sdb --rw=randread --bs=8k --iodepth=24 --direct=1 --runtime=900 --time_based`. Wait 2 minutes, then run `iostat -xd 5 3` and capture the last interval.
- Screen 1, the terminal with `iostat -xd 5` for sdb (r/s, w/s, r_await, aqu-sz, %util). Save as `0419/linux-iostat-data-disk.png`.
- Screen 2, vSphere Client > the VM > Monitor > Performance > Advanced > Virtual disk, Chart Options: Real-time, object the data disk (scsiM:N), counters Read latency and Average read requests per second, with the legend table. Capture within the same minute as screen 1. Save as `0419/vcenter-vm-virtual-disk-real-time.png`.
- Condition the key depends on: %util 97-100; aqu-sz 18-30; r_await 3 ms or less; aqu-sz within 10% of r/s x r_await / 1,000; r_await within 15% of the vCenter Read latency of the same minute.
- Masking: mask every VM, host, datastore and cluster name, and the host name in the shell prompt.

## Likely wrong answer
B: %util near 100% means a saturated disk, so move it to faster storage. Or E: aqu-sz is a backlog waiting in Linux.

## Expected key points
- Answer: A, C, D, G.
- A true: %util is the share of the elapsed time with at least one I/O in flight (field 10 of the disk statistics); it says nothing about how many more requests the device can serve at once.
- B false: the misconception. For devices that serve requests in parallel, such as arrays and modern SSDs, %util at 100% does not show a limit.
- C true: the screen reading. Little's law holds for any device; the screen shows aqu-sz within 10% of r/s x r_await / 1,000.
- D true: a small difference between await and the vCenter virtual disk latency puts the time below the guest; here r_await is within 15% of the vCenter Read latency.
- E false: a request counts in aqu-sz from the moment it enters the request queue until it finishes, whether it waits or is served.
- F false: the wrong action. r_await stays at 3 ms or less with 18-30 requests in flight; the device serves them in parallel, and nothing shows saturation.
- G true: saturation shows as await rising while the I/O rate stays flat; spare capacity as the I/O rate rising with await flat.
- H false: await includes the time in the Linux queue, the virtual adapter, the VMkernel and the storage, not only the array.
- I false: the over-correction. For a device that serves requests one at a time, %util near 100% does mean saturation.
- J false: the vCenter virtual disk latency starts at the virtual disk; time in the Linux queues before it is not in it.
- K false: the screen reading. r_await is within 15% of the vCenter Read latency.

## Notes
- Paired with the theory question 0360 (theory and practical; design.md, section 3.9).
- No option rests on the Paravirtual SCSI queue depth.
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item C24 (origin: synthetic). Counts only after author approval.
- Review 2026-11-15: the await condition is relative (within 15%), since an absolute 0.5 ms fails at sub-millisecond await; options reworded away from 0360; K (a false screen reading) added. Key unchanged: A, C, D, G.

## Metadata
```yaml
id: "0419"
title: "Linux %util near 100% at a low await"
product: [vsphere, linux]
technology: [storage]
task: troubleshoot
level: 400
answer_type: deterministic
input: [screenshot]
object: [vm, guest-os]
tool: [vcenter, guest-os-tools]
knowledge:
  - guest-os/storage/linux-storage-io-path
  - guest-os/storage/disk-queue
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
knowledge_main: guest-os/storage/linux-storage-io-path
attachments:
  - 0419/linux-iostat-data-disk.png
  - 0419/vcenter-vm-virtual-disk-real-time.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C24"
answer: [A, C, D, G]
misconception: [B, F]
misconception_type: [layer-confusion, tool-confusion]
pair: "0360"
status: awaiting-input
```
