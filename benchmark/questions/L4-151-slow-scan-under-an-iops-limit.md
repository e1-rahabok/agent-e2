# A slow disk scan with a fast array

## Prompt
- Users of a reporting VM say a scan of its data disk takes hours.
- The VM owner says vCenter proves the storage is slow. The storage team says the array answers in under a millisecond.
- See [the vSphere Client virtual disk chart](0425/vcenter-vm-virtual-disk-real-time.png), [the esxtop disk device panel](0425/esxtop-disk-device-panel.png) and [the VM's hard disk settings](0425/vcenter-vm-hard-disk-settings.png).

Which statements are correct?

- A. The reads are about 128 KB each: read rate divided by read requests per second.
- B. With 128 KB reads, the 1,000 IOPS limit caps the disk at about 250 reads per second.
- C. The disk runs at about a quarter of its limit, so the limit is not what holds it back.
- D. The time is spent in the ESXi kernel queue: KAVG and QAVG are high while DAVG stays below 1 ms.
- E. The array is slow: the virtual disk latency comes from the device.
- F. Ask the storage team to move the LUN to faster media.
- G. A high QAVG on a LUN always means an IOPS limit on one of its virtual disks.
- H. Removing the limit, which is the default setting, takes away the wait in the kernel queue.

## Input to supply
- Product and version: vSphere 9.1 (ESXi 9.1, vSphere Client 9.1).
- Object: one VM with a data disk (Hard disk 2) on a LUN that no other VM uses; the array's latency under 1 ms.
- How to produce it: set Limit - IOPS to 1000 on Hard disk 2; in the VM run `fio --rw=read --bs=128k --iodepth=16 --direct=1 --runtime=900 --time_based` on that disk. Wait 2 minutes before capturing.
- Screen 1, vSphere Client > the VM > Monitor > Performance > Advanced > Virtual disk, Chart Options: Real-time, object Hard disk 2 (scsiM:N), counters Average read requests per second, Read rate and Read latency, with the legend table (Units column, Latest, Average). Save as `0425/vcenter-vm-virtual-disk-real-time.png`.
- Screen 2, esxtop on the VM's host, `u` (disk device panel), the row of the LUN, with CMDS/s, READS/s, MBREAD/s, DAVG/cmd, KAVG/cmd, GAVG/cmd and QAVG/cmd visible. Save as `0425/esxtop-disk-device-panel.png`.
- Screen 3, vSphere Client > the VM > Edit Settings, Hard disk 2 expanded, showing Limit - IOPS 1000. Save as `0425/vcenter-vm-hard-disk-settings.png`.
- Condition the key depends on: read requests per second flat at 230-260; Read rate divided by read requests per second about 128 KB; Read latency 30 ms or more; esxtop DAVG/cmd below 1 ms, KAVG/cmd at least 10 times DAVG/cmd, QAVG/cmd within 20% of KAVG/cmd.
- Masking: mask every VM, host, datastore and cluster name, and the device identifier.

## Likely wrong answer
E or F: the latency is high, so the array is slow. Or C: 250 reads per second is far below the 1,000 limit, so the limit cannot be the cause.

## Expected key points
- Answer: A, B, D, H.
- A true: about 32,000 KBps / 250 reads per second is about 128 KB per read.
- B true: mClock counts an IO above 32 KB as several: a 128 KB read counts as 4, so 1,000 / 4 = 250 reads per second, the flat line on screen 1.
- C false: the misconception. The limit counts 128 KB reads four times; the disk sits at its limit.
- D true: IO above the limit waits in the kernel queue: high QAVG, inside KAVG and GAVG, with normal DAVG (Broadcom KB 426790).
- E false: DAVG below 1 ms shows the device answers fast; the wait is before the IO reaches it.
- F false: the wrong action. Faster media do not change a wait set by the VM's own limit.
- G false: the over-correction. High QAVG means IO waits in a kernel queue; queue depths at each level of the stack are other causes. Here screen 3 shows the limit.
- H true: the default is no limit; without it the reads are no longer held in the kernel queue.

## Reasoning path
1. Read rate / read requests per second: the IO size.
2. Limit / (IO size / 32 KB): the cap in reads per second; compare with the flat line.
3. esxtop: where the time is spent (KAVG and QAVG against DAVG).

## Notes
- Practical half of pair D6 with 0424 (theory; design.md, section 3.9).
- No option rests on the Paravirtual SCSI queue depth or Disk.SchedNumReqOutstanding (open question Q195).
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item D6 (origin: synthetic). Counts only after author approval.

## Metadata
```yaml
id: "0425"
title: "A slow disk scan with a fast array"
product: [vsphere]
technology: [storage]
task: troubleshoot
level: 400
answer_type: deterministic
input: [screenshot]
object: [vm, esxi]
tool: [vcenter, esxtop]
knowledge:
  - vsphere/technology/storage/metrics/virtual-motherboard/iops
  - vsphere/technology/storage/concepts/esxi-storage-latency-stack
  - vsphere/tools/esxtop/storage
knowledge_main: vsphere/technology/storage/metrics/virtual-motherboard/iops
attachments:
  - 0425/vcenter-vm-virtual-disk-real-time.png
  - 0425/esxtop-disk-device-panel.png
  - 0425/vcenter-vm-hard-disk-settings.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D6"
answer: [A, B, D, H]
misconception: [C, E]
misconception_type: [consumption-as-contention, unit-and-normalization]
pair: "0424"
status: awaiting-input
```
