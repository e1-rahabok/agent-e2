# TCP retransmits with no drops in vSphere

## Prompt
- A Linux VM with one VMXNET3 adapter exports data to a partner every night. Between 01:00 and 02:00 the transfers slow down.
- Inside Linux, `nstat` in that hour: TcpRetransSegs rises from almost 0 to about 3% of TcpOutSegs. `ip -s link` shows no dropped packets on the interface.
- vCenter, same hour: the VM's transmit and receive dropped packets are 0. The host's vmnics show no drops and no errors.
- The host's 10 GbE uplink transmits about 9.4 Gbps in that hour; the backup also runs then.
- The vSphere team says: "vSphere shows no drops, so the network is clean. It must be the application."

Which statements are correct?

- A. The network team should read the discard and queue-drop counters of the switch ports on the path for 01:00-02:00.
- B. The retransmit counter on its own shows which device on the path dropped the lost segments.
- C. TcpRetransSegs rising is evidence of loss: acknowledgements did not return, so Linux resent the segments.
- D. A frame dropped by the top-of-rack switch would appear in vCenter as a transmitted packet dropped on the VM.
- E. ESXi counts a frame as sent once the physical NIC has put it on the wire.
- F. A frame that a congested top-of-rack switch discards is counted only in the counters of that switch.
- G. vCenter keeps a TCP retransmission counter per VM, so the retransmits can be confirmed there.
- H. An uplink at about 9.4 of 10 Gbps while the backup runs points at congestion in that hour.
- I. The uplink at 9.4 of 10 Gbps shows that the host's own NIC dropped the lost frames.
- J. Each retransmission costs time, so a loss of a few percent can slow the nightly transfer.
- K. With no drops counted in vCenter, on the vmnics or in Linux, the network is clean: ask the application team to fix the export.

## Likely wrong answer
- D: "If a switch dropped our packets, vCenter would show transmit drops on the VM."
- K: "vSphere and Linux show no dropped packets, so the network is clean; it is the application."

## Expected key points
- Answer: A, C, E, F, H, J.
- A is true: the evidence of a top-of-rack drop is in the switch's discard counters, read by the network team for the same hour.
- B is false: a retransmit only says no acknowledgement came back; the switch counters or a packet capture at both ends locate the loss (top-of-rack, upstream, firewall, WAN link, partner).
- C is true: TCP resends a segment when no acknowledgement returns (timer or duplicate acknowledgements); the retransmits are the evidence of loss.
- D is false: steps 1-5 of the transmit path (guest, vNIC, port group, virtual switch, physical NIC) all count 0; only the switch that drops the frame counts it.
- E is true: Ethernet does not acknowledge frames, so (unless PAUSE flow control holds it back) the frame counts as sent once it is on the wire.
- F is true: the switch ASIC drops the frame and counts it as an input discard or queue drop; no other layer counts it.
- G is false: vSphere has no retransmit counter for VM traffic; retransmits are read inside the guest.
- H is true: the uplink near line rate while the backup runs points at congestion in 01:00-02:00.
- I is false: a drop at the host's physical NIC is counted as a dropped packet on that vmnic, and the vmnics show none.
- J is true: each loss forces a resend and slows TCP down; the application sees higher latency.
- K is false: the misconception; a drop at a congested switch is invisible to ESXi and to the guest, so the zero counts do not clear the network.

## Notes
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): the negation pair H/N resolved (old H dropped); old E (vmnic transmit error) dropped next to D; old J (full receive ring in vCenter) dropped, as ring-drop visibility stays in 0039 and 0212; old L (VM network latency counter) dropped, as 0214 holds that fact; over-correction I added; K carries the wrong action. Key changed from A, C, F, G, H, J, K, M to A, C, E, F, H, J.
- Sharpened stem: the VMXNET3 adapter and the clean `ip -s link` output (for option K) are stated.

## Metadata
```yaml
id: "0268"
title: "TCP retransmits with no drops in vSphere"
product: [linux, vsphere]
technology: [network]
task: troubleshoot
level: 300
answer_type: deterministic
answer: [A, C, E, F, H, J]
misconception: [K, D]
input: [text]
object: [guest-os, vm, network]
tool: [guest-os-tools, vcenter]
knowledge:
  - vsphere/technology/network/concepts/packet-drop-accounting
  - vsphere/technology/network/metrics/vm-network-metrics
  - vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
  - vsphere/technology/network/metrics/host/packets-dropped
knowledge_main: vsphere/technology/network/concepts/packet-drop-accounting
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
misconception_type: [layer-confusion]
status: draft
```
