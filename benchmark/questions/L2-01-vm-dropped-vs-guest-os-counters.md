# Why VM dropped packets differ from the Guest OS

## Prompt
- A Linux VM with one VMXNET3 adapter shows dropped packets in vCenter today: Receive packets dropped and Transmit packets dropped are both above 0.
- Inside Linux, `ip -s link show eth0` shows 0 dropped packets in both directions.
- `ethtool -S eth0` shows `pkts rx OOB: 0` on every receive queue.

Which statements about drops that vCenter counts and Linux does not are correct?

- A. ESXi dropped received frames before delivery, such as frames that break the port group's security policy.
- B. The host dropped packets after the guest sent them, for example on a distributed firewall rule.
- C. Linux has no counter for drops on a full VMXNET3 receive ring.
- D. ESXi and Linux count the same dropped packets, so one of the two counters is faulty.
- E. Raise the VMXNET3 receive ring in Linux to stop the drops that vCenter shows.

## Likely wrong answer
D: "The counts should match, so one of them is broken." Or C: "a full receive ring is invisible to the guest."

## Expected key points
- Answer: A, B.
- A is true: ESXi drops received frames that are not for the guest or that break the port group's security settings. The guest never receives them, so it cannot count them.
- B is true: a packet dropped after it left the guest (for example an NSX distributed firewall reject) is counted by ESXi on the VM, not by the guest. The guest sees only the resend delay.
- C is false: the VMXNET3 device shares a ring-full drop with the guest driver; Linux shows it per receive queue as `pkts rx OOB` in `ethtool -S`. It reads 0 here, so the ring was not full.
- D is false: received drops happen before the Guest OS and transmitted drops after it, so the two layers count different packets.
- E is false: `pkts rx OOB` is 0, so the ring did not overflow; a larger ring changes nothing for these drops.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
- Revised 2026-11-12, then after the independent review: Linux guest with a decidable counter. `ip -s link` RX dropped does not include the device's out-of-buffer count; `ethtool -S` shows it as `pkts rx OOB` per queue (upstream Linux vmxnet3 driver, vmxnet3_ethtool.c).
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): the compound option C split; the two options not in the knowledge base (Tools resets counters, bytes against packets) replaced by the misconception D and the wrong action E. Ring-drop visibility is kept here and in 0212 only. Key unchanged: A, B.

## Metadata
```yaml
id: "0039"
title: "Why VM dropped packets differ from the Guest OS"
product: [vsphere, linux]
technology: [network]
object: [vm, guest-os]
tool: [vcenter, guest-os-tools]
task: explain-mechanism
level: 200
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
  - vsphere/technology/network/concepts/packet-drop-accounting
  - vsphere/architecture/vm-vs-guest-os
knowledge_main: vsphere/technology/network/concepts/packet-drop-accounting
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
answer: [A, B]
misconception: [C, D]
misconception_type: [layer-confusion]
pair: "0420"
status: draft
```
