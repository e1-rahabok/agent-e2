# Full-duplex port capacity

## Prompt
An ESXi host has one 25 Gb physical NIC port, full duplex.

Which statements about the capacity of this port are correct?

- A. Transmit and receive share one pool of 25 Gb.
- B. Transmit can be saturated while receive is nearly idle.
- C. Each direction gets half the port speed, 12.5 Gb.
- D. The port carries 50 Gb in one direction while the other direction is idle.
- E. The Usage counter can show 40 Gbps on this port with no fault.
- F. Receive and transmit are each judged against 25 Gb.
- G. The port is saturated only when its Usage reaches 50 Gbps.
- H. Set the Usage alert of this port at 25 Gbps, the link speed.

## Likely wrong answer
A: treating the port speed as one pool for both directions.

## Expected key points
- Answer: B, E, F.
- A is false: full duplex is 100% in each direction.
- B is true: each direction has its own 25 Gb, so one direction can be full while the other carries almost nothing.
- C is false: neither direction is halved; each has the full 25 Gb.
- D is false: each direction is capped at the port speed; idle receive capacity cannot carry transmit traffic.
- E is true: Usage = receive + transmit, so it can exceed the link speed, up to 50 Gbps on a 25 Gb full-duplex port.
- F is true: measure and size each direction separately.
- G is false: one direction alone saturates at 25 Gb, while Usage may then read only a little above 25 Gbps.
- H is false: Usage sums both directions, so it passes 25 Gbps on a healthy port (for example 20 Gb receive and 10 Gb transmit); alert on each direction against 25 Gb.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
- Options rewritten 2026-11-14 to the option rules (design.md 3.9; project/question-pairing-2026-11-14.md): plural stem; usage-rate option E, per-direction option F, over-correction G (50 Gbps) and wrong action H added. Key changed from B to B, E, F.
- Review 2026-11-15: B no longer restates F (one fact) and no longer reads as the negation of A; E and H reworded so they share no wording with the practical half 0413. Key unchanged: B, E, F.

## Metadata
```yaml
id: "0040"
title: "Full-duplex port capacity"
product: [vsphere]
technology: [network]
object: [network]
tool: [none]
task: decide-capacity
level: 200
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/technology/network/concepts/network-characteristics
  - vsphere/technology/network/metrics/host/throughput
knowledge_main: vsphere/technology/network/concepts/network-characteristics
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
answer: [B, E, F]
misconception: [A]
misconception_type: [unit-and-normalization]
pair: "0413"
status: draft
```
