# Actual vs potential memory contention

## Prompt
- A 32 GB Windows VM. In the vSphere Client, its memory chart for the past day (5-minute values) shows:
  - Swapped: about 1.2 GB all day. Compressed: about 0.3 GB all day.
  - Swap out rate and Compression rate: 0 at every point.
  - Swap in rate and Decompression rate: 0 at every point except 02:05 (Swap in rate about 150 KBps).
  - Latency: 0% at every point except 0.8% at 02:05.
- The application team says the VM was slow at 14:00 and blames memory.

Which statements are correct?

- A. The VM waited for memory around 02:05.
- B. The 0.3 GB compressed sits outside Granted until ESXi decompresses it.
- C. At 14:00, ESXi did not make the VM wait for memory.
- D. Swapped at 1.2 GB shows that host swapping slows the VM down all day.
- E. The swap-in at 02:05 shows that the host was short of memory at 02:05.
- F. Since the host was not reclaiming memory, the swap-in at 02:05 cost the VM no time.
- G. Add memory to the host: Swapped and Compressed above 0 show that it is short of memory now.

## Answers
A, B, C

## Explanation
- A is true: at 02:05 the guest touched swapped and compressed pages; each page read back is a wait for the vCPU that touched it, and Latency rose to 0.8% with the swap-in. That is the actual problem; the amounts are only potential.
- B is true: a compressed page is not directly accessible to the VM, so VM Granted excludes it; the guest's next touch makes ESXi decompress it, and that is a wait.
- C is true: Latency, Swap in rate and Decompression rate are 0 at 14:00, so the VM did not wait on ESXi for memory then; look elsewhere for the slowness.
- D is false: swapped pages cost a wait only when the guest touches them (swap-in, which shows in Latency); Swapped is the amount out now, often pages the guest does not use.
- E is false: swap-in means the guest asked for a page swapped out earlier; it does not mean the host is under pressure now. Here no page went out all day.
- F is false: the guest still waits for each page it reads back, whatever the host's state; Latency at 02:05 shows it. This is the over-correction of D.
- G is false: Swapped or Compressed above 0 does not show the host short of memory now (Swap out rate and Compression rate are 0 all day, so no page went out); the cause was high host Consumed or a limit, and the pages can be guest cache. Check for a limit on the VM or its pools before host capacity: a limit reclaims on a host with free memory too.
- Misconception: D: the swapped amount read as the VM being slow. Or F, the over-correction: with no host pressure, swap-in is harmless.

## Notes
- Hint moved out of the prompt (author, 2026-11-14: a hint helps the frontier model, not the local model), for reviewers: "Do not select counters that indicate risk but not actual slowness." Stem made plural (Q-E2-199); was "Which metric best indicates".
- Hint moved out of the prompt (author, 2026-11-14: a hint helps the frontier model, not the local model), for reviewers: "Hint: separate actual from potential, risk from reality."
- Rewritten 2026-11-14 to the theory option rules (design.md 3.9 and 6.1 F5; project/question-pairing-2026-11-14.md): the definition prompt ("Which metrics best indicate that a VM has an actual memory performance problem?", options Ballooned, Swapped + Zipped, Latency, "Ballooned = Configured") became a situation with values and single-fact options. The author's fact stays: the wait (swap-in, decompression, Latency) is actual; swapped and compressed amounts are potential (author approved, 2026-11-14).
- Changed in the 2026-11-15 audit: level 400 to 300 (each option is one public rule read on two rows); B replaced (swapped and compressed amounts are past reclamation is tested by the pair 0025/0391; the fact now is that compressed pages sit outside Granted); key point G adds the limit check.
- Review 2026-11-15: refocused on swap and compression, amounts against rates. The balloon options repeated 0052, and the option on Latency as a share of memory repeated 0149; both removed. Key letters A, B, C (new options).

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
  - vsphere/technology/memory/metrics/virtual-motherboard/swapped
  - vsphere/technology/memory/metrics/virtual-motherboard/compressed
  - vsphere/technology/memory/metrics/virtual-motherboard/swap-in-rate
  - vsphere/technology/memory/concepts/swap-and-compression
  - vsphere/technology/memory/vm-memory-latency-high
object: [vm]
tool: [vcenter]
knowledge_main: vsphere/technology/memory/metrics/virtual-motherboard/latency
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > Memory > Q3 VM Memory Contention"
answer_type: deterministic
level: 300
misconception: [D]
misconception_type: [reclamation-as-contention, cumulative-vs-current]
status: draft
```
