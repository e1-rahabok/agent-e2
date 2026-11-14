# Latency and outstanding IO

## Prompt
- A database VM's virtual disk shows, in the vSphere Client, an average of 24 outstanding read requests at about 6,000 read IOPS.
- The storage administrator asks how outstanding IO relates to the disk's latency, and whether 24 is a problem.

Which statements about outstanding IO and latency are correct?

- A. Outstanding IO and latency are not linked by any formula: one is counted before processing, the other after.
- B. Outstanding IO equals IOPS multiplied by latency.
- C. Outstanding IO equals IOPS divided by latency.
- D. Outstanding IO equals throughput multiplied by latency.
- E. A high outstanding IO count means high latency, whatever the IOPS.
- F. At 6,000 IOPS, 24 outstanding IOs correspond to an average latency of about 4 ms.
- G. Outstanding IO never signals a bottleneck: only latency does.
- H. With 24 requests outstanding, move the VM to a faster datastore.

## Likely wrong answer
A, or D (throughput instead of commands). Or E: "A long queue means the disk is slow."

## Expected key points
- Answer: B, F.
- A is false: Little's law links them: average latency = average outstanding IO / average IOPS.
- B is true: IOPS (per second) × latency (seconds) = commands in flight.
- C is false: dividing IOPS by latency gives no queue length; the units do not work out.
- D is false: outstanding IO counts commands, not bytes.
- E is false: outstanding IO rises with IOPS; a long queue is acceptable while latency stays low, so read it with latency.
- F is true: 24 / 6,000 per second = 0.004 s, about 4 ms.
- G is false: IOs issued and not completed wait in a queue, which is a bottleneck signal; it is read together with latency, not dropped.
- H is false: the queue length alone says nothing about the datastore; check the latency first (here about 4 ms).

## Notes
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): plural stem with the operator's values; the author's options A-D kept; misconception E, over-correction G and wrong action H added (author approved, 2026-11-14). Key changed from B to B, F.

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
object: [vm]
tool: [none]
knowledge_main: vsphere/technology/storage/metrics/virtual-motherboard/outstanding-io
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > Storage > Q1 Latency vs OIO"
answer_type: deterministic
level: 300                      # author 2026-11-05
answer: [B, F]
misconception: [A, E]
misconception_type: [unit-and-normalization]
pair: "0416"
status: draft
```
