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
- F. vCenter keeps a TCP retransmission counter per VM, so the retransmits can be confirmed there.
- G. The uplink at 9.4 of 10 Gbps shows that the host's own NIC dropped the lost frames.
- H. Each retransmission costs time; a loss of a few percent slows the nightly transfer.
- I. With no drops counted in vCenter, on the vmnics or in Linux, the network is clean: ask the application team to fix the export.

## Likely wrong answer
- D: "If a switch dropped our packets, vCenter would show transmit drops on the VM."
- I: "vSphere and Linux show no dropped packets, so the network is clean; it is the application."

## Expected key points
- Answer: A, C, E, H.
- A is true: the evidence of a top-of-rack drop is in the switch's discard counters, read by the network team for the same hour.
- B is false: a retransmit only says no acknowledgement came back; the switch counters or a packet capture at both ends locate the loss (top-of-rack, upstream, firewall, WAN link, partner).
- C is true: TCP resends a segment when no acknowledgement returns (timer or duplicate acknowledgements); the retransmits are the evidence of loss.
- D is false: steps 1-5 of the transmit path (guest, vNIC, port group, virtual switch, physical NIC) all count 0; only the switch that drops the frame counts it, as an input discard or queue drop.
- E is true: Ethernet does not acknowledge frames, so (unless PAUSE flow control holds it back) the frame counts as sent once it is on the wire.
- F is false: vSphere has no retransmit counter for VM traffic; retransmits are read inside the guest.
- G is false: a drop at the host's physical NIC is counted as a dropped packet on that vmnic, and the vmnics show none.
- H is true: each loss forces a resend and slows TCP down; the application sees higher latency.
- I is false: the misconception; a drop at a congested switch is invisible to ESXi and to the guest, so the zero counts do not clear the network.

## Notes
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): the negation pair H/N resolved (old H dropped); old E (vmnic transmit error) dropped next to D; old J (full receive ring in vCenter) dropped, as ring-drop visibility stays in 0039 and 0212; old L (VM network latency counter) dropped, as 0214 holds that fact; over-correction I added; K carries the wrong action. Key changed from A, C, F, G, H, J, K, M to A, C, E, F, H, J.
- Review 2026-11-15: old F (a top-of-rack discard counted only by the switch) deleted, as it negated D; old H (an uplink near line rate means congestion) deleted, as the knowledge base does not state it; the uplink load stays in the stem as a case fact. Options relettered; key changed from A, C, E, F, H, J to A, C, E, H.
- Audit 2026-11-15: level 300 -> 400 (the key is a correct zero that misleads: a top-of-rack drop is counted only in that switch, combined over nstat, vCenter, the vmnics and the uplink load); the hedge "can slow" in H made plain.
- Sharpened stem: the VMXNET3 adapter and the clean `ip -s link` output (for option I) are stated.

## Metadata
```yaml
id: "0268"
title: "TCP retransmits with no drops in vSphere"
product: [linux, vsphere]
technology: [network]
task: troubleshoot
level: 400
answer_type: deterministic
answer: [A, C, E, H]
misconception: [I, D]
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
source_path: "Synthetic, 2026-11-12"
misconception_type: [layer-confusion]
status: draft
```
