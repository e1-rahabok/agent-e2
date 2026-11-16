# Peak transmitted packet dropped percent

## Prompt
- One VM, one 5-minute window. The vSphere Client Real-time chart shows the VM's 15 samples of 20 seconds:
  - Packets transmitted: 5,000 in every sample (75,000 in the 5 minutes).
  - Transmitted packets dropped: 0 in 14 of the samples, 300 in one sample.
- In VCF Operations, the same VM shows the metric Network | Peak Transmitted Packet Dropped (%) for the collection cycle that covers this window.

Which statements are correct?

- A. The metric shows about 0.4% for this cycle: 300 dropped out of 75,000 transmitted.
- B. The metric shows a value of about 6% for this collection cycle.
- C. The cycle as a whole lost about 0.4% of what the VM transmitted.
- D. The metric can tell whether the 300 drops fell in the first or the last minute of the cycle.
- E. With 5,000 packets in every sample, the metric equals the worst sample's drops over its packets.
- F. A drop threshold on this peak metric must sit higher than one on the 5-minute share.
- G. Leave the peak out of the report, since the 5-minute share is the loss that matters.
- H. Like Packets Dropped (%), the metric adds the VM's received drops to its transmitted drops.

## Answers
B, C, E, F

## Explanation
- A is wrong: a Peak ... within collection cycle metric takes the highest of the 15 twenty-second values, not the cycle's drops over the cycle's packets.
- B is correct: the worst sample dropped 300 of about 5,000 packets: 300 / 5,000 = 6% (5.7% if the dropped packets are added to the denominator).
- C is correct: 300 / 75,000 = 0.4% (also 0.4% with the 300 in the denominator). The peak is 15 times the 5-minute share here; both are correct, they answer different questions.
- D is wrong: the peak metric stores only the highest of the 15 values; it shows no pattern within the 300 seconds.
- E is correct: the peak is the highest of the 15 twenty-second values; with the same packet count in every sample, that is the worst sample's 300 drops over its 5,000 packets. The 5-minute figure (0.4%) hides that burst.
- F is correct: a threshold holds only for the interval it was set on; 20-second peaks read higher than 5-minute values, so their threshold must be higher (the VM drop alert is set high because it reads a 20-second period).
- G is wrong: the peak shows the burst that the 5-minute average hides; both values are correct and answer different questions.
- H is wrong: Packets Dropped (%) adds received and transmitted drops, but the peak transmit metric, like the VM drop alert, reads transmitted drops only; received drops include packets not meant for the VM and drops in a full guest receive ring.
- Misconception: A: "0.4%: 300 dropped out of 75,000 transmitted." - G: "The 5-minute share is the real loss; the peak only exaggerates it."

## Notes
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): the two stem lines that explained the mechanism (the adapter's collection and the metric formula) removed; new numbers (different from the practical half); the negation pair E/F resolved (old E dropped, F stated positively as E); over-correction and wrong action H added. Key changed from B, C, F, H to B, C, E, G.
- Review 2026-11-15: D, E, F and H reworded so they share no wording with the practical half 0421; F now tests the interval rule of thresholds (the old F, "a vCenter counter", negated 0421 G). Key changed from B, C, E, G to B, C, E, F, G.
- Public source: Broadcom KB 444403, "Understanding 'Peak' or 'Worst' Performance Metrics in VMware VCF / Aria Operations" (https://knowledge.broadcom.com/external/article/444403/understanding-peak-or-worst-performance.html), no "Updated On" date shown; applies to VCF Operations 9.x and Aria Operations 8.x. It gives Network | Peak Transmitted Packet Dropped (%) = MAX(net.droppedTx_summation) / AVG(net.packetsTx_summation) x 100, and states that the adapter retrieves 15 raw 20-second samples every 5 minutes.
- Why this key: the knowledge base defines a Peak ... within collection cycle metric as the highest of the 15 twenty-second values; with 5,000 packets in every sample, the Broadcom KB 444403 formula MAX(droppedTx) / AVG(packetsTx) and the highest per-sample drop rate give the same 6%.
- Changed in the 2026-11-15 audit: old G (a drop ratio over few packets is unstable) dropped, because 0061 and 0082 test that fact; letters: old H is now G; new H added (received drops are not in the transmit peak). Key changed from B, C, E, F, G to B, C, E, F. E kept: it states the constant-rate condition that makes B decidable.
- Debatable risk: the formula comes from one KB article with no date, and the knowledge base does not state it; the constant packet count makes the key hold under either reading. The key accepts both figures with or without the dropped packets in the denominator ("about").

## Metadata
```yaml
id: "0313"
title: "Peak transmitted packet dropped percent"
product: [vcf-operations, vsphere]
technology: [network]
task: read-metric
level: 400
answer_type: deterministic
misconception: [A, G]
input: [text]
object: [vm]
tool: [vcf-operations]
knowledge:
  - vcf-operations/features/peak-20-second-metrics
  - vsphere/object-types/vm/vm-alerts
  - vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
  - vsphere/technology/network/metrics/virtual-motherboard/packets
  - sp5-framework/observability/thresholds
knowledge_main: vcf-operations/features/peak-20-second-metrics
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
misconception_type: [rollup-and-interval]
pair: "0421"
status: draft
```
