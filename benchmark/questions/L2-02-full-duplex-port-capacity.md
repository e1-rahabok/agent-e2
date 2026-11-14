# Full-duplex port capacity

## Prompt
An ESXi host has one 25 Gb physical NIC port, full duplex.

Which statements about the capacity of this port are correct?

- A. Transmit and receive share one pool of 25 Gb.
- B. The port carries up to 25 Gb transmit and 25 Gb receive at the same time.
- C. Each direction gets half the port speed, 12.5 Gb.
- D. The port carries 50 Gb in one direction while the other direction is idle.
- E. The host's network usage rate adds receive and transmit, so it can read above 25 Gbps on this port with no fault.
- F. Receive and transmit are each judged against 25 Gb.
- G. The port is saturated only when its usage rate reaches 50 Gbps.
- H. A usage rate of 44 Gbps on this port shows that it is overloaded: add a second port.

## Likely wrong answer
A: treating the port speed as one pool for both directions.

## Expected key points
- Answer: B, E, F.
- A is false: full duplex is 100% in each direction.
- B is true: a 25 Gb port handles 25 Gb transmit plus 25 Gb receive.
- C is false: neither direction is halved; each has the full 25 Gb.
- D is false: each direction is capped at the port speed; idle receive capacity cannot carry transmit traffic.
- E is true: usage rate = receive + transmit, so it can exceed the physical link speed.
- F is true: measure and size each direction separately.
- G is false: one direction alone saturates at 25 Gb, while the usage rate may then read only a little above 25 Gbps.
- H is false: 44 Gbps can be, for example, 24 Gb receive and 20 Gb transmit, both under 25 Gb; split it by direction before deciding.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
- Options rewritten 2026-11-14 to the option rules (design.md 3.9; project/question-pairing-2026-11-14.md): plural stem; usage-rate option E, per-direction option F, over-correction G (50 Gbps) and wrong action H added. Key changed from B to B, E, F.

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
