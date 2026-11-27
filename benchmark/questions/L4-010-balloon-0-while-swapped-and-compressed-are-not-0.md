# Balloon 0 while Swapped and Compressed are not 0

## Prompt
- An ESXi 9.1 host with 768 GB of memory, no memory tiering.
- vCenter, host memory, Past day: Usage 61-63%; State High in every sample; Balloon 0 in every sample.
- Same window: Swap consumed flat at 3.1 GB; Compressed flat at 1.2 GB.
- Same window: Swap in rate, Swap out rate, Compression rate and Decompression rate are 0 in every sample.
- The administrator asks: "Balloon is 0, so how can anything be swapped or compressed on this host?"

Which statements are correct?

- A. With Balloon at 0 all day, the swapped and compressed amounts point to a counter error.
- B. Swapping and compression happened earlier, and the VMs have not touched those pages since.
- C. The host is not under memory pressure now, so ESXi has no reason to inflate balloons.
- D. Pages left from past swapping and compression can no longer slow any VM.
- E. Swap consumed is the amount swapped out to date minus the amount swapped in to date.
- F. A flat Swap consumed of 3.1 GB shows ESXi swapping pages out at a steady rate.
- G. No VM had a measurable wait on a swapped or compressed page during the day.
- H. Moving some VMs off this host is needed to stop it swapping and compressing.

## Answers
B, C, G

## Explanation
- A is wrong: ballooning comes first only while pressure rises. Swap consumed and Compressed are amounts held now; they stay from past reclamation until the guest touches the pages, while the balloon deflates as soon as its target falls.
- B is correct: compressed and swapped data stays out until the guest requests it. Swap in rate and Decompression rate at 0 show no page came back; Swap out rate and Compression rate at 0 show no new reclamation.
- C is correct: State High in every sample; host-driven ballooning starts in the Soft state. No host pressure and no limit, no balloon.
- D is wrong: a page still swapped or compressed costs a wait when the guest touches it again (a swap-in, or a shorter decompression), counted in VM Memory Latency. This is the over-correction of A.
- E is wrong: Swap in and Swap out are cumulative totals; Swap consumed is what sits in swap now, like VM Swapped, so the difference of the totals is not it.
- F is wrong: Swap consumed is an amount held, not a rate; the Swap out rate is 0 in every sample.
- G is correct: a VM waits on these pages only when one is swapped in or decompressed; the host's Swap in rate and Decompression rate are 0 in every sample.
- H is wrong: the host is not swapping or compressing now (both rates are 0); the amounts are left from the past, and moving VMs answers no current pressure.
- Misconception: A: "Ballooning comes first, so Balloon 0 with Swapped above 0 is impossible: the counters are wrong." - D: "Those pages are old, so they cost nothing any more." - E: "Swap consumed is just swap out minus swap in."

## Notes
- Theory half of 0391 (VCF Operations list of the same pattern). Facts shared with 0391 (past reclamation, the over-correction, the wrong action) are two questions each; E with L3-025 C is two.
- Level 400 is the author's (Q-E2-056, 2026-11-05).
- Changed in the 2026-11-15 audit: the stem gives vCenter values instead of "Consumed is not high. There is clearly capacity to deploy another VM" (an interpretation); old D ("because of memory tiering", undecidable) replaced by the over-correction; E (cumulative totals), F (amount vs rate), G (no measurable wait, true) and H (wrong action) added; A and B reworded without the absolutes and the length cue. Key B, C kept; G added.
- Changed in the 2026-11-16 re-review: A lost its last absolute and reason clause ("since ballooning always comes first"); same fact, still the misconception.

## Metadata
```yaml
id: "0025"
title: "Balloon 0 while Swapped and Compressed are not 0"
product: [vsphere]
technology: [memory]
input: [text]
task: troubleshoot
knowledge:
  - vsphere/technology/memory/metrics/host/ballooned
  - vsphere/technology/memory/metrics/host/swap-used
  - vsphere/technology/memory/metrics/host/compressed
  - vsphere/technology/memory/metrics/host/state
  - vsphere/technology/memory/concepts/swap-and-compression
  - vsphere/technology/memory/concepts/ballooning
  - vsphere/technology/memory/concepts/host-memory-states
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
object: [esxi]
tool: [vcenter]
knowledge_main: vsphere/technology/memory/concepts/swap-and-compression
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > Memory > Q5 ESXi Memory Utilisation"
answer_type: deterministic
level: 400                      # author 2026-11-05
misconception: [A, D, E]
misconception_type: [cumulative-vs-current, reclamation-as-contention]
pair: "0391"
status: draft
```
