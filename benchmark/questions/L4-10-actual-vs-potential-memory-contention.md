# Actual vs potential memory contention

## Prompt
- A 32 GB Windows VM. In the vSphere Client, its memory chart for the past day (5-minute values) shows:
  - Ballooned: 6 GB, flat all day.
  - Swapped: about 1.2 GB all day.
  - Latency: 0% at every point except 0.8% at 02:05.
- The application team says the VM was slow at 14:00 and blames memory.

Which statements are correct?

- A. Of these three counters, only Latency measures time the VM spent waiting for memory.
- B. A Ballooned value that stays flat all day means the guest did not ask for those pages back during the day.
- C. At 14:00, ESXi did not make the VM wait for memory.
- D. Ballooned at 6 GB shows that the VM is short of memory now.
- E. Swapped at 1.2 GB shows that host swapping slows the VM down.
- F. Ballooned and swapped pages carry no risk for the VM's performance.
- G. Adding memory to the VM is the fix for the slowness at 14:00.
- H. Latency of 0.8% at 02:05 means that 0.8% of the VM's memory was slow to reach.

## Likely wrong answer
D or E: balloon or swap read as the VM being slow now. Or F, the over-correction: reclaimed memory carries no risk.

## Expected key points
- Answer: A, B, C.
- A is true: Latency is the share of time a vCPU waits for a page fault (mostly swap-in, plus decompression): the actual measure. Ballooned and Swapped measure space reclaimed, a potential problem.
- B is true: Ballooned is past tense; a flat value means the guest never requested those pages again during the day.
- C is true: Latency is 0% at 14:00, so the VM did not wait on ESXi for memory then; look elsewhere for the slowness.
- D is false: ballooning by itself does not cause a performance problem; it is the first leading indicator of pressure, and the pages stay ballooned while the guest does not ask for them.
- E is false: swapped pages cost a wait only when the guest touches them (swap-in, which shows in Latency); Swapped is the amount out now, often pages the guest does not use.
- F is false: the more ballooned, swapped and compressed, the higher the chance of a future performance hit: a potential problem, not none. The 0.8% at 02:05 is such a hit.
- G is false: there was no memory wait at 14:00; adding memory does not address a slowness that memory did not cause.
- H is false: Latency is a share of time, not a share of memory space.

## Notes
- Hint moved out of the prompt (author, 2026-11-14: a hint helps the frontier model, not the local model), for reviewers: "Do not select counters that indicate risk but not actual slowness." Stem made plural (Q199); was "Which metric best indicates".
- Hint moved out of the prompt (author, 2026-11-14: a hint helps the frontier model, not the local model), for reviewers: "Hint: separate actual from potential, risk from reality."
- Rewritten 2026-11-14 to the theory option rules (design.md 3.9 and 6.1 F5; project/question-pairing-2026-11-14.md): the definition prompt ("Which metrics best indicate that a VM has an actual memory performance problem?", options Ballooned, Swapped + Zipped, Latency, "Ballooned = Configured") became a situation with values and eight single-fact options. The author's fact stays: Latency is actual, Balloon and Swap are potential. Key changed from C to A, B, C (author approved, 2026-11-14).

## Metadata
```yaml
id: "0023"
title: "Actual vs potential memory contention"
product: [vsphere, windows]
technology: [memory]
input: [text]
task: read-metric
knowledge:
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
  - vsphere/technology/memory/metrics/virtual-motherboard/ballooned
  - vsphere/technology/memory/metrics/virtual-motherboard/swapped
  - vsphere/technology/memory/vm-memory-latency-high
  - vsphere/technology/memory/concepts/ballooning
object: [vm]
tool: [vcenter]
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/latency
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > Memory > Q3 VM Memory Contention"
answer_type: deterministic
level: 400                      # author 2026-11-05
answer: [A, B, C]
misconception: [D, E]
misconception_type: [reclamation-as-contention]
status: draft
```
