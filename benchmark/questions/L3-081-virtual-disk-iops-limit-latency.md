# Latency from a virtual disk IOPS limit

## Prompt
- A virtual disk has an IOPS limit of 600 in the VM's settings.
- The application on that disk issues 96 KB reads as fast as it can.

Which statements are correct?

- A. IO above the limit waits in the ESXi kernel queue, so QAVG and KAVG rise.
- B. Device latency (DAVG) stays at its usual level.
- C. High latency on the virtual disk shows that the array is slow.
- D. Raising the device queue depth removes the wait an IOPS limit creates.
- E. With 96 KB reads, the disk completes about 200 reads per second.
- F. The limit caps the disk's throughput in MB per second rather than its number of IOs.
- G. The limit applies to the whole VM, across all its virtual disks.
- H. Open a case with the array vendor for the virtual disk latency.
- I. The limit also applies to the VM's snapshot files and swap file.
- J. Latency that comes from the VM's own IOPS limit does not slow the application.

## Likely wrong answer
C: the latency is high, so the array is slow. Or J, the overshoot: a wait the VM's own setting causes is harmless.

## Expected key points
- Answer: A, B, E.
- A true: IO above the limit waits in the ESXi kernel queue: esxtop shows high QAVG, inside KAVG and GAVG (Broadcom KB 426790).
- B true: the array is not what holds the IO; DAVG stays normal.
- C false: the misconception. An IOPS limit shows as high QAVG and KAVG with normal DAVG; check the disk's limit.
- D false: the IO is held by the limit in the ESXi IO scheduler, not by a lack of queue slots; a deeper queue holds the same IO, and the cap stays.
- E true: mClock, the ESXi IO scheduler, counts an IO above 32 KB as several: a 96 KB read counts as 3, so 600 / 3 = 200 reads per second.
- F false: a disk IOPS limit exists; a disk throughput limit does not.
- G false: the limit is set per virtual disk, not per VM.
- H false: the wrong action. The wait is in the host, set by the VM's own configuration.
- I false: a limit is not possible for snapshots or swap files.
- J false: the over-correction. The wait is real contention for the VM: it shows in GAVG and in the VM's disk latency, and the application waits for every IO held.

## Notes
- Theory half of pair D6 with 0425 (practical; design.md, section 3.9). Different limit and IO size from 0425.
- No option rests on the Paravirtual SCSI queue depth or Disk.SchedNumReqOutstanding.
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item D6 (origin: synthetic). Counts only after author approval.
- Review 2026-11-15: D replaced (it was close to 0425 G); J is the over-correction now. Key unchanged: A, B, E.

## Metadata
```yaml
id: "0424"
title: "Latency from a virtual disk IOPS limit"
product: [vsphere]
technology: [storage]
task: explain-mechanism
level: 300
answer_type: deterministic
input: [text]
object: [vm]
tool: [esxtop]
knowledge:
  - vsphere/technology/storage/metrics/virtual-motherboard/iops
  - vsphere/technology/storage/concepts/esxi-storage-latency-stack
knowledge_main: vsphere/technology/storage/metrics/virtual-motherboard/iops
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D6"
answer: [A, B, E]
misconception: [C]
misconception_type: [consumption-as-contention]
pair: "0425"
status: draft
```
