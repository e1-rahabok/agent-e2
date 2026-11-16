# Latency and outstanding IO

## Prompt
- A backup server VM writes its nightly backup to one virtual disk.
- The vSphere Client shows, for that disk, Average number of outstanding write requests about 48 at about 16,000 Average write requests per second.
- The backup administrator asks the storage team what the 48 means.

Which statements about outstanding IO and latency are correct?

- A. Latency equals outstanding IO multiplied by IOPS.
- B. Outstanding IO equals IOPS multiplied by latency.
- C. Outstanding IO equals IOPS divided by latency.
- D. Outstanding IO equals throughput multiplied by latency.
- E. Two virtual disks with the same outstanding IO count have the same latency.
- F. 48 outstanding writes at 16,000 writes per second mean a write latency of about 3 ms.
- G. Outstanding IO is available for the datastore as well as for the virtual disk.
- H. Open a case with the array team: 48 writes waiting show that the array cannot keep up.
- I. A queue of outstanding IO is harmless at any length, as long as the disk keeps a high IOPS.
- J. Another disk with 2 outstanding writes at 50 writes per second has a low write latency.

## Likely wrong answer
D (throughput instead of commands), or E and H: "A long queue means the disk is slow." Or J, the reverse: "A short queue means the disk is fast."

## Expected key points
- Answer: B, F.
- A is wrong: latency is outstanding IO divided by IOPS (Little's law), not multiplied.
- B is correct: IOPS (per second) × latency (seconds) = commands in flight.
- C is wrong: dividing IOPS by latency gives no queue length; the units do not work out.
- D is wrong: outstanding IO counts commands, not bytes.
- E is wrong: the same queue at a higher IOPS means a lower latency; outstanding IO rises with IOPS, so it is read together with latency.
- F is correct: 48 / 16,000 per second = 0.003 s, about 3 ms.
- G is wrong: the counter exists at the virtual disk level only; for a datastore it is derived from latency and IOPS.
- H is wrong: the queue follows the IO rate; at about 3 ms the writes complete quickly, so the array is keeping up.
- I is wrong: at a fixed IOPS a longer queue means a higher latency (latency = outstanding IO / IOPS); a long queue is acceptable only while latency stays low.
- J is wrong: latency = outstanding IO / IOPS = 2 / 50 per second = 0.04 s, about 40 ms. At a low IOPS a long latency still gives a small count, so the latency is read, not the count.

## Notes
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): plural stem with the operator's values; the author's options A-D kept; misconception E, over-correction G and wrong action H added (author approved, 2026-11-14). Key changed from B to B, F.
- Review 2026-11-15: new situation (a backup VM writing, 48 outstanding writes at 16,000 per second), so it shares no situation or wording with its practical half 0416; A restated as a wrong formula (no longer the negation of B); G (datastore level) and over-correction I replace the options that copied 0416. Key unchanged: B, F.
- Audit 2026-11-15: "always" removed from E (still false: the same count at another IOPS is another latency); J added (low outstanding IO at low IOPS, outstanding-io Misconceptions); F reworded for length (truth unchanged). Key unchanged: B, F.

## Metadata
```yaml
id: "0028"
title: "Latency and outstanding IO"
product: [vsphere]
technology: [storage]
input: [text]
task: explain-mechanism
knowledge:
  - vsphere/technology/storage/metrics/virtual-motherboard/outstanding-io
  - vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
  - vsphere/technology/storage/metrics/virtual-motherboard/iops
  - vsphere/technology/storage/metrics/host/datastore
object: [vm]
tool: [vcenter]
knowledge_main: vsphere/technology/storage/metrics/virtual-motherboard/outstanding-io
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > Storage > Q1 Latency vs OIO"
answer_type: deterministic
level: 300                      # author 2026-11-05
answer: [B, F]
misconception: [D, E, H, J]
misconception_type: [unit-and-normalization]
pair: "0416"
status: draft
```
