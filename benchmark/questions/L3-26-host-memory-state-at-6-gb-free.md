# Host memory state at 11 GB free

## Prompt
- ESXi 9.1 host with 2 TB of memory, no memory tiering.
- For this host, ESXi computes the free memory minimum (minFree) at about 21.1 GB.
- Free memory right now: about 11 GB.

Which statements are correct?

- A. The host is in the Soft state.
- B. Free memory below minFree means that compression and swapping have started.
- C. Compression and host swapping start only when free memory falls to about 6.8 GB.
- D. The balloon driver cannot make a guest page out to its own page file.
- E. In the Soft state, the VMs on this host wait for memory now.
- F. Evacuate the host at once: its VMs stall until it leaves the Soft state.

## Likely wrong answer
B: reclamation by compression and swap read from "below minFree". Or E: the Soft state read as the VMs waiting.

## Expected key points
- Answer: A, C.
- The states are fractions of minFree: Clear below 300% (about 63 GB here), Soft at 64% (about 13.5 GB), Hard at 32% (about 6.8 GB), Low at 16% (about 3.4 GB). 11 GB free is between Soft and Hard.
- A is true: 11 GB is below the Soft line of about 13.5 GB and above the Hard line of about 6.8 GB. In Soft, ESXi inflates balloons.
- B is false: compression and swapping start in the Hard state, at 32% of minFree, not when free memory passes below minFree.
- C is true: the Hard state starts at 32% of minFree, about 6.8 GB here.
- D is false: the guest gives the balloon Free pages first, then Cache, Modified and In Use; pages taken from In Use make the guest page out. This is the over-correction of E (ballooning is harmless).
- E is false: ballooning is reclamation, not a wait. The VMs wait only when they touch pages that are swapped or compressed: check memory latency (contention).
- F is false: the Soft state does not mean the VMs wait, so there is no emergency; check VM memory contention, then plan capacity.

## Notes
- States as fractions of minFree (clear 300%, soft 64%, hard 32%, low 16%, with hysteresis on the way back up): the knowledge base, ESXi memory states; Duncan Epping, yellow-bricks.com, memory states; Frank Denneman, frankdenneman.nl/2011/07/26/mem-minfreepct-sliding-scale-function (minFree: a sliding scale, about 899 MB for the first 28 GB plus 1% of the rest, so about 21.1 GB on a 2 TB host: 0.9 + 20.2). Author answer Q188 (ESXi 9.1 memory reclamation manual, project/sources).
- Rewritten 2026-11-14 (design.md 3.9; project/question-pairing-2026-11-14.md): the stem no longer copies the knowledge example (2 TB host instead of 1 TB); D the over-correction and F the wrong action added. Old C (ballooning starts at about 99% of host memory) and old D (page sharing waits for the Soft state) removed: the same facts are options K and H of 0146. Key letters unchanged (A, C); C now states the Hard line.

## Metadata
```yaml
id: "0144"
title: "Host memory state at 11 GB free"
product: [vsphere]
technology: [memory]
task: read-metric
level: 300
answer_type: deterministic
input: [text]
object: [esxi]
tool: [none]
knowledge:
  - vsphere/technology/memory/concepts/host-memory-states
  - vsphere/technology/memory/metrics/host/state
  - vsphere/technology/memory/concepts/ballooning
knowledge_main: vsphere/technology/memory/concepts/host-memory-states
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
answer: [A, C]
misconception: [B, E]
misconception_type: [reclamation-as-contention, threshold-transplanted]
pair: "0385"
status: draft
```
