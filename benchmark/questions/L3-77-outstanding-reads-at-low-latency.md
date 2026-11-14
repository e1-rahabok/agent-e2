# Many outstanding reads at low latency

## Prompt
- A DBA says the vSphere Client shows too many outstanding reads on the data disk of a database VM, and asks to move the VM to a faster datastore.
- See [the vSphere Client virtual disk chart of the VM](0416/vcenter-vm-virtual-disk-real-time.png).

Which statements are correct?

- A. The outstanding reads are about the read requests per second times the read latency in seconds.
- B. A long queue at this latency means the storage completes many requests in parallel.
- C. A high number of outstanding IOs means the storage is too slow.
- D. Outstanding IO and latency have no fixed relation: one is counted before processing, the other after.
- E. Move the VM to a faster datastore to cut the queue.
- F. Outstanding IO is of no use: only latency matters.
- G. At the same read rate, higher latency would raise the number of outstanding reads.
- H. The outstanding reads include the requests still waiting in the Guest OS before the virtual disk.
- I. Read throughput in KBps times the latency gives the outstanding reads.

## Input to supply
- Product and version: vSphere 9.1 (vSphere Client 9.1).
- Object: one VM with a data virtual disk (scsi0:1) on a fast datastore (all-flash or NVMe).
- How to produce it: in the VM, a random read load with a deep queue, for example fio `--rw=randread --bs=4k --iodepth=32 --direct=1 --runtime=900` on the data disk. Wait 2 minutes before capturing.
- Screen, vSphere Client > the VM > Monitor > Performance > Advanced > Virtual disk, Chart Options: Real-time, object the data disk (scsi0:1), counters Average number of outstanding read requests, Average read requests per second and Read latency, with the legend table (Units column, Latest, Maximum, Average). Save as `0416/vcenter-vm-virtual-disk-real-time.png`.
- Condition the key depends on: outstanding reads 16-40; Read latency 0.2-1.0 ms; read requests per second x Read latency / 1,000 within 20% of the outstanding reads.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
C: a long queue of outstanding reads means slow storage, so move the VM. Or D: queue and latency are not linked.

## Expected key points
- Answer: A, B, G.
- A true: Little's law: average latency = average outstanding IO / average IOPS, so outstanding IO = IOPS x latency. The chart's values agree within the condition's 20%.
- B true: latency stays at 1 ms or less while 16 or more reads are in flight: the device serves them in parallel. A long queue is acceptable while latency stays low.
- C false: the misconception. High outstanding IO needs a check of latency; here latency is low.
- D false: the two are linked by Little's law at a given IOPS.
- E false: the wrong action. Latency is already low; the queue follows from the read rate the database issues.
- F false: the over-correction. Read with latency, outstanding IO shows the concurrency; it is less useful alone, not useless.
- G true: at a given IOPS, a longer time per IO means more IOs in flight.
- H false: IO queued inside the Guest OS has not reached the hypervisor; the virtual disk counters start at the virtual disk.
- I false: outstanding IO counts commands, not data: IOPS, not throughput, times latency.

## Notes
- Paired with the theory question 0028 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item C21 (origin: synthetic). Counts only after author approval.

## Metadata
```yaml
id: "0416"
title: "Many outstanding reads at low latency"
product: [vsphere]
technology: [storage]
task: read-metric
level: 300
answer_type: deterministic
input: [screenshot]
object: [vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/storage/metrics/virtual-motherboard/outstanding-io
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
  - vsphere/technology/storage/metrics/virtual-motherboard/iops
knowledge_main: vsphere/technology/storage/metrics/virtual-motherboard/outstanding-io
attachments:
  - 0416/vcenter-vm-virtual-disk-real-time.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C21"
answer: [A, B, G]
misconception: [C, E]
misconception_type: [unit-and-normalization, consumption-as-contention]
pair: "0028"
status: awaiting-input
```
