# Why VM dropped packets differ from the Guest OS

## Prompt
- A Linux VM with one VMXNET3 adapter shows dropped packets in vCenter today: Receive packets dropped and Transmit packets dropped are both above 0.
- Inside Linux, `ip -s link show eth0` shows 0 dropped packets in both directions.
- `ethtool -S eth0` shows `pkts rx OOB: 0` on every receive queue.

Which reasons can explain drops that vCenter counts and Linux does not?

- A. ESXi dropped received frames before delivery, such as frames against the security policy.
- B. The host dropped packets after the guest sent them, for example on a firewall rule.
- C. The VMXNET3 receive ring was full; ESXi counts that drop, and the guest has no counter for it.
- D. VMware Tools resets the Linux network counters every 20 seconds, so they stay at 0.
- E. Linux counts dropped packets in bytes and vCenter in packets, so small counts round to 0.

## Likely wrong answer
C: "a full receive ring is invisible to the guest". Or D and E: looking for a counter bug instead of where the drop happens.

## Expected key points
- Answer: A, B.
- A: ESXi drops received frames that are not for the guest or that break the port group's security settings. The guest never receives them, so it cannot count them.
- B: a packet dropped after it left the guest (for example an NSX distributed firewall reject) is counted by ESXi on the VM, not by the guest. The guest sees only the resend delay.
- C is wrong: the VMXNET3 device reports ring overflows to the guest driver as out-of-buffer packets (`pkts rx OOB` in `ethtool -S`). It reads 0 here, so the ring was not full.
- D and E are wrong: VMware Tools does not change the guest counters, and both tools count packets.

## Notes
- Previous id: question-0039 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
- Revised 2026-11-12 (question set 1.0), then after the independent review: Linux guest with a decidable counter. `ip -s link` RX dropped does not include the device's out-of-buffer count; `ethtool -S` shows it as `pkts rx OOB` per queue (upstream Linux vmxnet3 driver, vmxnet3_ethtool.c).

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
source_path: "Drafted by Claude 2026-11-05 for the Level 100-200 allocation (benchmark/design.md, section 3.6)"
answer: [A, B]
misconception: [C]
misconception_type: [layer-confusion]
status: draft
```
