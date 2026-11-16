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
- F. With 8 KB reads instead, the disk would complete about 2,400 reads per second.
- G. The limit applies to the whole VM, across all its virtual disks.
- H. Moving the virtual disk to a faster datastore removes the wait.
- I. The limit also applies to the VM's snapshot files and swap file.
- J. Latency that comes from the VM's own IOPS limit does not slow the application.

## Likely wrong answer
C: the latency is high, so the array is slow. Or J, the overshoot: a wait the VM's own setting causes is harmless.

## Expected key points
- Answer: A, B, E.
- A is correct: IO above the limit waits in the ESXi kernel queue: esxtop shows high QAVG, inside KAVG and GAVG (Broadcom KB 426790).
- B is correct: the array is not what holds the IO; DAVG stays normal.
- C is wrong: the misconception. An IOPS limit shows as high QAVG and KAVG with normal DAVG; check the disk's limit.
- D is wrong: a high QAVG means a VMkernel limit holds the commands (the device queue depth DQLEN, DSNRO on a device that several virtual disks share, or an IOPS limit on a virtual disk). Here the IOPS limit, in the ESXi IO scheduler, holds the IO; each limit holds the requests above it, so a deeper device queue holds the same IO and the cap stays.
- E is correct: mClock, the ESXi IO scheduler, counts an IO above 32 KB as several: a 96 KB read counts as 3, so 600 / 3 = 200 reads per second.
- F is wrong: mClock counts only an IO above 32 KB as several; an 8 KB read counts as one, so the disk still completes at most 600 reads per second. 2,400 reads would follow from a cap of 600 x 32 KB = 19.2 MB per second, but a disk throughput limit does not exist.
- G is wrong: the limit is set per virtual disk, not per VM.
- H is wrong: the wrong action. The wait is in the ESXi kernel queue, set by the disk's own limit, which moves with the disk: on a faster datastore the cap of 200 reads per second stays. Remove or raise the limit instead.
- I is wrong: a limit is not possible for snapshots or swap files.
- J is wrong: the over-correction. The wait is real contention for the VM: it shows in GAVG and in the VM's disk latency, and the application waits for every IO held.

## Notes
- Theory half of pair D6 with 0425 (practical; design.md, section 3.9). Different limit and IO size from 0425.
- No option rests on the Paravirtual SCSI queue depth or Disk.SchedNumReqOutstanding.
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item D6 (origin: synthetic). Counts only after author approval.
- Review 2026-11-15: D replaced (it was close to 0425 G); J is the over-correction now. Key unchanged: A, B, E.
- Audit 2026-11-15: D key point cites the VMkernel limits behind a high QAVG (esxi-storage-io-path, added to `knowledge`). Key unchanged: A, B, E.
- Re-review 2026-11-16: F (the limit caps MB per second) was arguable against E's own mechanism (above 32 KB, the cap acts on bytes); it now tests that an IO of 32 KB or less counts as one. H (open a case with the array vendor) repeated C's misconception; it is now the wrong action of moving the disk. Key unchanged: A, B, E.

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
  - vsphere/technology/storage/concepts/esxi-storage-io-path
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
