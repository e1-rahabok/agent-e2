# Host memory state at 11 GB free

## Prompt
- ESXi 9.1 host with 2 TB of memory, no memory tiering.
- For this host, ESXi computes the free memory minimum (minFree) at about 21.1 GB.
- Free memory right now: about 11 GB.

Which statements are correct?

- A. The host is in the Soft state.
- B. Free memory below minFree means that compression and swapping have started.
- C. On this host the Hard state begins at about 6.8 GB of free memory.
- D. The balloon driver cannot make a guest page out to its own page file.
- E. If free memory climbs back to 15 GB, the host leaves the Soft state.
- F. Evacuate the host at once: its VMs stall until it leaves the Soft state.

## Answers
A, C

## Explanation
- A is correct: the states are fractions of minFree: Clear below 300% (about 63 GB here), Soft at 64% (about 13.5 GB), Hard at 32% (about 6.8 GB), Low at 16% (about 3.4 GB). 11 GB is Soft whether free memory is falling (below 13.5 GB) or rising out of Hard (the Hard exit is 48%, about 10.1 GB). In Soft, ESXi inflates balloons.
- B is wrong: compression and swapping start in the Hard state, at 32% of minFree, not when free memory passes below minFree.
- C is correct: the Hard state starts at 32% of minFree, about 6.8 GB here.
- D is wrong: the guest gives the balloon Free pages first, then Cache, Modified and In Use; pages taken from In Use make the guest page out. This is the over-correction of the Soft-state misconception (ballooning is harmless).
- E is wrong: the states have hysteresis. The host leaves Soft upward only above 100% of minFree, about 21.1 GB; at 15 GB it stays in Soft.
- F is wrong: ballooning in the Soft state is reclamation, not a wait; the VMs wait only when they touch swapped or compressed pages. Check VM memory contention, then plan capacity.
- Misconception: B: reclamation by compression and swap read from "below minFree". Or E: "once free memory is back above the Soft line, the host is out of Soft."

## Notes
- States as fractions of minFree (clear 300%, soft 64%, hard 32%, low 16%, with hysteresis on the way back up: Soft left above 100%, Hard above 48%): the knowledge base, ESXi memory states; Frank Denneman, frankdenneman.nl/2011/07/26/mem-minfreepct-sliding-scale-function (minFree: a sliding scale, about 899 MB for the first 28 GB plus 1% of the rest, so about 21.1 GB on a 2 TB host: 0.9 + 20.2). Author answer Q188 (ESXi 9.1 memory reclamation manual, project/sources).
- A VM with a memory limit is compressed and swapped at any host state; C is about the host-wide start.
- Changed in the 2026-11-15 audit: E (Soft read as the VMs waiting; redundancy #40, homed in 0149/0392) replaced by the hysteresis misconception; F's key point now carries the reclamation-is-not-a-wait reason; C's clause removed (near-negation of B). The file name still says 6 GB; the title says 11 GB.

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
source_path: "Synthetic, 2026-11-12"
misconception: [B, E]
misconception_type: [reclamation-as-contention, threshold-transplanted]
pair: "0385"
status: draft
```
