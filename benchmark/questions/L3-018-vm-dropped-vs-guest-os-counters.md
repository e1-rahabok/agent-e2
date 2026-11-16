# Why VM dropped packets differ from the Guest OS

## Prompt
- An administrator compares a VM's dropped-packet counters in vCenter (Receive packets dropped, Transmit packets dropped) with the interface counters of its Guest OS, and finds that they rarely match.

Which statements are correct?

- A. Frames that break the port group's security policy are dropped by ESXi before the Guest OS can count them.
- B. A packet the host drops after the guest sent it, say on a distributed firewall rule, counts on the VM and not in the guest.
- C. A dropped packet is counted either by ESXi or by the Guest OS, but never by both of them.
- D. The receive drops that vCenter shows for a VM should equal the receive drops that its Guest OS reports, packet for packet.
- E. Across a large fleet of VMs over a month, receive drops run far higher than transmit drops.
- F. Each receive drop that vCenter shows for a VM is a fault to hand to the network team as a ticket.

## Likely wrong answer
D: "The counts should match, so one of them is broken." Or C: "the VM and the guest never see the same drop."

## Expected key points
- Answer: A, B, E.
- A is true: ESXi drops received frames that are not for the guest or that break the port group's security settings; the guest never receives them.
- B is true: transmitted packets are dropped after they leave the Guest OS (for example an NSX distributed firewall reject), so ESXi counts them on the VM and the guest sees only the resend delay.
- C is false: a full VMXNET3 receive ring is counted at the port and on the VM (droppedRx, %DRPRX) and also by the guest driver (Linux `ethtool -S`, pkts rx OOB).
- D is false: received drops happen before the Guest OS and transmitted drops after it, so the two layers count different packets.
- E is true: over 3,938 VMs and one month, receive drops were far higher than transmit drops.
- F is false: a full VMXNET3 receive ring is caused and fixed in the Guest OS (ring size, guest CPU), so the Guest OS owner fixes it; other receive drops are ESXi enforcing policy.

## Notes
- 2026-11-16 (author, Q251): level 200 to 300, as the reviewers read it. A new Level 200 basics question for the guard is still to write.
- Revised 2026-11-12, then after the independent review: Linux guest with a decidable counter. `ip -s link` RX dropped does not include the device's out-of-buffer count; `ethtool -S` shows it as `pkts rx OOB` per queue (upstream Linux vmxnet3 driver, vmxnet3_ethtool.c).
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): the compound option C split; the two options not in the knowledge base (Tools resets counters, bytes against packets) replaced by a misconception and a wrong action.
- Review 2026-11-15: made generic. The stem had become the capture condition of its practical half 0420 in words (vCenter drops above 0, `ip -s link` 0, pkts rx OOB 0), and four options matched 0420's. New options: security-policy drops, host drops after the guest, the over-correction C (ring-drop visibility, also tested in 0420), the fleet profile E and the wrong action F. Key changed from A, B to A, B, E.
- Audit 2026-11-15: level 200 -> 300 (C needs the VMXNET3 shared-ring accounting and B the Distributed Firewall boundary); C reworded without the leading "No ... ever"; B shortened and D, F lengthened (B was 1.7x the wrong mean). The stem stays generic: it is the theory half of 0420.

## Metadata
```yaml
id: "0039"
title: "Why VM dropped packets differ from the Guest OS"
product: [vsphere, linux]
technology: [network]
object: [vm, guest-os]
tool: [vcenter, guest-os-tools]
task: explain-mechanism
level: 300                      # Q251, author 2026-11-16: relabelled as written (was 200)
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
  - vsphere/technology/network/concepts/packet-drop-accounting
  - vsphere/architecture/vm-vs-guest-os
knowledge_main: vsphere/technology/network/concepts/packet-drop-accounting
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-05"
answer: [A, B, E]
misconception: [D, C]
misconception_type: [layer-confusion]
pair: "0420"
status: draft
```
