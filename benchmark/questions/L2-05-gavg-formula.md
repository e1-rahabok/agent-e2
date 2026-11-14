# How the esxtop storage latencies add up

## Prompt
- In esxtop, the disk device panel shows one LUN with GAVG/cmd 5.4 ms, KAVG/cmd 4.6 ms, QAVG/cmd 4.5 ms and DAVG/cmd 0.8 ms.

Which statements about these counters are correct?

- A. GAVG equals KAVG plus DAVG.
- B. GAVG equals KAVG plus QAVG plus DAVG.
- C. GAVG is the latency that the Guest OS measures for its disk.
- D. DAVG is the time from the host's HBA to the array and back.
- E. A command that finds the device queue full waits in the kernel, which raises QAVG and KAVG.
- F. QAVG can read higher than KAVG, because QAVG also counts IO that the kernel issues for itself.
- G. A KAVG above about 0.5 ms always points to a fault on the host.
- H. With KAVG at 4.6 ms and DAVG at 0.8 ms, open a case with the array vendor.

## Likely wrong answer
B: adding QAVG on top of KAVG, counting the queue time twice. Or H: "Latency is high, so the array is slow."

## Expected key points
- Answer: A, D, E, F.
- A is true: GAVG (total seen from the VM monitor) = KAVG (time in the VMkernel) + DAVG (device): 4.6 + 0.8 = 5.4 ms.
- B is false: QAVG is the queue part of the kernel time, already inside KAVG; adding it again gives 9.9 ms, not the 5.4 ms shown.
- C is false: Guest in GAVG means the VM, measured from the VM monitor down; the Guest OS adds its own queues above it.
- D is true: DAVG covers the HBA, the fabric and the array.
- E is true: when commands exceed the device queue depth (DQLEN), they queue in the VMkernel; QAVG tracks that delay and it shows in KAVG, while DAVG stays as it was.
- F is true: QAVG covers VM IO and kernel IO, KAVG VM IO only, so QAVG can exceed KAVG.
- G is false: a VAAI offload raises KAVG with no problem when no other symptom comes with it.
- H is false: the added time is in the host, before the array (KAVG 4.6 ms against DAVG 0.8 ms); check the queue depths along the stack first.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Revised 2026-11-12 for question set 1.0: values added so the relation can be checked. Counts only after author approval.
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): the theory half of 0086 (a full device queue). Plural stem, new values (different from 0086), one fact per option; over-correction G and wrong action H added. Key changed from A to A, D, E, F.

## Metadata
```yaml
id: "0043"
title: "How the esxtop storage latencies add up"
product: [vsphere]
technology: [storage]
task: explain-mechanism
level: 200
answer_type: deterministic
input: [text]
object: [esxi]
tool: [esxtop]
knowledge:
  - vsphere/technology/storage/concepts/esxi-storage-latency-stack
  - vsphere/tools/esxtop/storage
  - vsphere/technology/storage/troubleshooting/host-storage-latency
knowledge_main: vsphere/technology/storage/concepts/esxi-storage-latency-stack
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
answer: [A, D, E, F]
misconception: [B, H]
misconception_type: [unit-and-normalization, layer-confusion]
pair: "0086"
status: draft
```
