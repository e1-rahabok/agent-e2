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
- E. The host's vmnic would report a frame that the top-of-rack switch later discarded as a transmit error.
- F. ESXi counts a frame as sent once the NIC has put it on the wire: Ethernet does not acknowledge frames.
- G. A frame that a congested top-of-rack switch discards is counted only in the counters of that switch.
- H. Zero drops in vCenter and on the vmnics do not show that the path beyond the host is clean.
- I. vCenter keeps a TCP retransmission counter per VM, so the retransmits can be confirmed there.
- J. A full VMXNET3 receive ring in this VM would have shown in vCenter as received packets dropped on the VM.
- K. An uplink at about 9.4 of 10 Gbps while the backup runs points at congestion in that hour.
- L. The VM's network latency counter in vCenter would show the delay that the retransmissions add.
- M. Each retransmission costs time, so a loss of a few percent can slow the nightly transfer.
- N. With no drops counted in vCenter, on the vmnics or in Linux, the network is clean and the cause is the application.

## Likely wrong answer
- D: "If a switch dropped our packets, vCenter would show transmit drops on the VM."
- N: "vSphere and Linux show no dropped packets, so the network is clean; it is the application."

## Expected key points
- Answer: A, C, F, G, H, J, K, M.
- A is true: the evidence of a top-of-rack drop is in the switch's discard counters, read by the network team for the same hour.
- B is false: a retransmit only says no acknowledgement came back; the switch counters or a packet capture at both ends locate the loss (top-of-rack, upstream, firewall, WAN link, partner).
- C is true: TCP resends a segment when no acknowledgement returns (timer or duplicate acknowledgements); the retransmits are the evidence of loss.
- D is false: steps 1-5 of the transmit path (guest, vNIC, port group, virtual switch, physical NIC) all count 0; only the switch that drops the frame counts it.
- E is false: the physical NIC finished its part when it serialized the frame; it counts no error for a later discard.
- F is true: Ethernet does not acknowledge frames, so (unless PAUSE flow control holds it back) the frame counts as sent once it is on the wire.
- G is true: the switch ASIC drops the frame and counts it as an input discard or queue drop; no other layer counts it.
- H is true: zero drops in vSphere do not prove the network is clean; a transmit drop beyond the host is invisible to ESXi and to the guest.
- I is false: vSphere has no retransmit counter for VM traffic; retransmits are read inside the guest.
- J is true: a full VMXNET3 receive ring is counted by the hypervisor at the port and the VM (droppedRx, %DRPRX), so the zero rules it out.
- K is true: the uplink near line rate while the backup runs points at congestion in 01:00-02:00.
- L is false: vSphere has no VM network latency counter.
- M is true: each loss forces a resend and slows TCP down; the application sees higher latency.
- N is false: the misconception; a drop at a congested switch is invisible to ESXi and to the guest.

## Notes
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
- Sharpened stem: the VMXNET3 adapter (for option J) and the clean `ip -s link` output (for option N) are stated.

## Metadata
```yaml
id: "0268"
title: "TCP retransmits with no drops in vSphere"
product: [linux, vsphere]
technology: [network]
task: troubleshoot
level: 300
answer_type: deterministic
answer: [A, C, F, G, H, J, K, M]
misconception: [N, D]
input: [text]
object: [guest-os, vm, network]
tool: [guest-os-tools, vcenter]
knowledge:
  - vsphere/technology/network/concepts/packet-drop-accounting
  - vsphere/technology/network/metrics/vm-network-metrics
  - vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
knowledge_main: vsphere/technology/network/concepts/packet-drop-accounting
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
misconception_type: [layer-confusion]
status: draft
```
