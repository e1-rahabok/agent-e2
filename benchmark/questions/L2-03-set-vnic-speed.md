# Setting a vNIC speed

## Prompt
- An application owner asks for their VM to be limited to 500 Mbps of network bandwidth.
- The VM has one VMXNET3 adapter. Windows shows its link speed as 10 Gbps, although the host uplinks are 25 GbE.
- The VM's port group is on a vSphere Distributed Switch with Network I/O Control version 3 enabled.

Which statements are correct?

- A. Setting the adapter speed to 500 Mbps in the Windows adapter properties caps the VM at 500 Mbps.
- B. The 10 Gbps that Windows shows is a label the virtual adapter reports; it caps nothing.
- C. The VMX option that changes the reported link speed accepts no value below 10 Gbps.
- D. A traffic shaping policy on the port group, with average and peak bandwidth, can cap the VM's bandwidth.
- E. A Network I/O Control limit set on the VM's network adapter can cap its bandwidth.
- F. A Network I/O Control limit takes effect only when the uplink is saturated.
- G. A Network I/O Control limit on the adapter caps both the traffic the VM sends and the traffic it receives.
- H. On a distributed switch, traffic shaping can be set separately for traffic into and out of the VM.
- I. A Network I/O Control reservation of 500 Mbps on the adapter also caps the VM at 500 Mbps.
- J. Network I/O Control shares hold the VM to its share of the uplink even when the uplink is idle.
- K. When an adapter limit and a port group shaping average both apply, the lower of the two sets the cap.
- L. vCenter has a counter that shows when Network I/O Control capped the VM's bandwidth.

## Likely wrong answer
- A: "Just set the NIC to 500 Mbps in Windows (or in the VM settings) and it can't send more than that."

## Expected key points
- Answer: B, C, D, E, H, K.
- A is false: the guest speed setting caps nothing; 500 Mbps cannot be allocated through the vNIC speed.
- B is true: the virtual device has no physical link to negotiate; VMXNET3 reports 10 Gbps by default, whatever the vmnic behind the port group, and moves data as fast as host CPU, virtual switch policies and uplinks allow.
- C is true: `ethernetX.linkspeed` (vSphere 8.0 Update 2 and later) accepts 10,000 to 65,000 Mbps; a value outside the range falls back to 10 Gbps, and the setting caps nothing.
- D is true: traffic shaping (average, peak, burst) is a port group policy that caps bandwidth.
- E is true: Network I/O Control v3 gives each VM network adapter shares, a reservation and a limit.
- F is false: Network I/O Control limits are enforced even when the switch is not saturated.
- G is false: Network I/O Control controls transmit traffic only; traffic shaping can cover receive.
- H is true: a distributed switch shapes in and out; a standard switch shapes outbound only.
- I is false: a reservation is a guaranteed minimum, not a cap.
- J is false: shares divide the link only among consumers that want bandwidth; unused bandwidth is available to others.
- K is true: a 200 Mbps adapter limit under a 100 Mbps shaping average gives 100 Mbps.
- L is false: Network I/O Control has no metric that shows it capped bandwidth; check the logs.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
- Revised 2026-11-12. The VMX setting is `ethernetX.linkspeed`, from vSphere 8.0 Update 2, 10,000 to 65,000 Mbps; values outside the range fall back to 10 Gbps. Vendor sources for the reported link speed: Broadcom KB 368812, How to change the vmxnet3 link speed of a VM, https://knowledge.broadcom.com/external/article/368812/how-to-change-the-vmxnet3-link-speed-of.html; Broadcom KB 444078, VMXNET3 guest OS link speed does not enforce bandwidth limits, https://knowledge.broadcom.com/external/article/444078/vmxnet3-guest-os-link-speed-resets-and-d.html.
- Prompt sharpened: the port group is on a distributed switch with Network I/O Control v3, so the options on Network I/O Control and on shaping in each direction are decidable.
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
- Options rewritten 2026-11-14 to the option rules (design.md 3.9; project/question-pairing-2026-11-14.md): the negation pair B/C removed (old C dropped; B states the label positively); D made one fact; L (no Network I/O Control metric) added. The old L (the lower of limit and shaping wins) stays as K: resource-controls states it, so it is decidable. Key changed from B, D, E, F, I, L to B, C, D, E, H, K (same facts, relettered).

## Metadata
```yaml
id: "0041"
title: "Setting a vNIC speed"
product: [vsphere, windows]
technology: [network]
object: [vm, network]
tool: [vcenter, guest-os-tools]
task: judge-setting
level: 200
answer_type: deterministic
answer: [B, C, D, E, H, K]
misconception: [A]
input: [text]
knowledge:
  - vsphere/technology/network/concepts/network-characteristics
  - vsphere/technology/network/concepts/netioc
  - vsphere/architecture/resource-controls
knowledge_main: vsphere/technology/network/concepts/network-characteristics
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
misconception_type: []
status: draft
```
