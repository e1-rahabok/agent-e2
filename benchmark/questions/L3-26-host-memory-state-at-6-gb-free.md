# Host memory state at 6 GB free

## Prompt
- ESXi 9.1 host with 1 TB of memory, no memory tiering.
- For this host, ESXi computes the free memory minimum (minFree) at about 10.8 GB.
- Free memory right now: about 6 GB.

Which statements are correct?

- A. The host is in the soft state: ballooning has started.
- B. Compression and swapping have started, because free memory is below minFree.
- C. On this host, ballooning from host pressure starts only when about 99% of the memory is in use.
- D. Page sharing waits for the soft state before it shares any page.
- E. In the soft state, the VMs on this host wait for memory now.

## Likely wrong answer
B: reclamation by compression and swap read from "below minFree". Or E: the soft state read as the VMs waiting.

## Expected key points
- Answer: A, C.
- The states are fractions of minFree: clear below 300%, soft at 64% (about 6.9 GB here), hard at 32% (about 3.5 GB), low at 16% (about 1.7 GB). 6 GB free is between soft and hard: soft.
- A: in the soft state, ESXi inflates balloons.
- B is wrong: compression and swapping start in the hard state, at 32% of minFree.
- C: soft starts at about 6.9 GB free of 1 TB, so about 99.3% is in use. A host at 90% shows no balloon from host pressure.
- D is wrong: sharing starts earlier. In the clear state (below 300% of minFree) ESXi breaks large pages and page sharing collapses identical pages, before any ballooning (within each VM by default).
- E is wrong: ballooning is reclamation, not a wait. The VMs wait only when they touch pages that are swapped or compressed: check memory latency (contention).

## Notes
- States as fractions of minFree (clear 300%, soft 64%, hard 32%, low 16%, with hysteresis on the way back up): the knowledge base, ESXi memory states; Duncan Epping, yellow-bricks.com, memory states; Frank Denneman, frankdenneman.nl/2011/07/26/mem-minfreepct-sliding-scale-function (minFree: a sliding scale, about 899 MB for the first 28 GB plus 1% of the rest, so about 10.8 GB on a 1 TB host). Author answer Q188 (ESXi 9.1 memory reclamation manual, project/sources).

## Metadata
```yaml
id: "0144"
title: "Host memory state at 6 GB free"
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
  - vsphere/technology/memory/concepts/page-sharing
knowledge_main: vsphere/technology/memory/concepts/host-memory-states
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12 for the memory slots (project/plan.md, M2)"
answer: [A, C]
misconception: [B, E]
misconception_type: [reclamation-as-contention, threshold-transplanted]
status: draft
```
