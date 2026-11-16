# Many outstanding reads at low latency

## Prompt
- A DBA says the vSphere Client shows too many outstanding reads on the data disk (scsi0:1) of database VM db-sql-09, and asks to move the VM to a faster datastore. The disk is on an NVMe datastore.
- He attaches [the VM's Virtual disk chart, exported to CSV](0416/vcenter-vm-virtual-disk-realtime.csv), Real-time, 10 minutes at 20-second samples.

Which statements are correct?

- A. In the export, read requests per second times read latency in seconds comes out close to the outstanding reads.
- B. A long queue at this latency means the storage completes many requests in parallel.
- C. A high number of outstanding IOs means the storage is too slow.
- D. The outstanding reads of scsi0:1 also count the reads of other VMs on the same NVMe datastore.
- E. The export calls for a datastore with lower latency.
- F. Read latency alone shows how many reads are in flight on the disk.
- G. At the same read rate, higher latency would raise the number of outstanding reads.
- H. The outstanding reads include the requests still waiting in the Guest OS before the virtual disk.
- I. Read latency in the export sits at several milliseconds, which explains the long queue.

## Likely wrong answer
C: a long queue of outstanding reads means slow storage, so move the VM. Or E: move the VM to a faster datastore.

## Expected key points
- Answer: A, B, G.
- A true: reading. Little's law: outstanding IO = IOPS x latency. In every row `Average read requests per second for scsi0:1` x `Read Latency (us) for scsi0:1` / 1,000,000 is within 20% of `Average number of outstanding read requests for scsi0:1` (about 27,000 x 0.0007 s = 19).
- B true: `Read Latency (us)` stays below 1,000 us while 16 or more reads are in flight: the device serves them in parallel. A long queue is acceptable while latency stays low.
- C false: the misconception. High outstanding IO needs a check of latency; here latency is below 1 ms.
- D false: a virtual disk counter counts only the IO this VM issues to that disk; other VMs' IO on the datastore is not in it.
- E false: the wrong action. Latency is already below 1 ms; the queue follows from the read rate the database issues.
- F false: the over-correction. Latency is a time per IO; how many IOs are in flight needs the read rate too (Little's law) or the outstanding count itself. Read with latency, outstanding IO shows the concurrency.
- G true: at a given IOPS, a longer time per IO means more IOs in flight.
- H false: IO queued inside the Guest OS has not reached the hypervisor; the virtual disk counters start at the virtual disk.
- I false: reading. `Read Latency (us) for scsi0:1` is 600-900 us (0.6-0.9 ms) in every row; the queue comes from the read rate.

## Notes
- Paired with the theory question 0028 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item C21 (origin: synthetic). Counts only after author approval.
- Review 2026-11-15: options reworded away from 0028 (A and I are now screen readings, one true and one false). Key unchanged: A, B, G.
- 2026-11-15: the screenshot replaced by a generated export (project/practical-questions-as-exports-2026-11-15.md). The export carries latency in microseconds (Read Latency (us)): the millisecond counter prints whole numbers and cannot show 0.2-1.0 ms.
- Re-review 2026-11-16: D (queue and latency move independently) was the negation of G and of A; it now tests that a virtual disk counter holds only this VM's IO. F (outstanding IO adds nothing once latency is known) was arguable by Little's law when IOPS is known too; it now says latency alone shows the reads in flight. Key unchanged: A, B, G.

## Metadata
```yaml
id: "0416"
title: "Many outstanding reads at low latency"
product: [vsphere]
technology: [storage]
task: read-metric
level: 300
answer_type: deterministic
input: [table]
object: [vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/storage/metrics/virtual-motherboard/outstanding-io
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
  - vsphere/technology/storage/metrics/virtual-motherboard/iops
knowledge_main: vsphere/technology/storage/metrics/virtual-motherboard/outstanding-io
attachments:
  - 0416/vcenter-vm-virtual-disk-realtime.csv
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C21"
answer: [A, B, G]
misconception: [C, E]
misconception_type: [unit-and-normalization, consumption-as-contention]
pair: "0028"
status: draft
```
