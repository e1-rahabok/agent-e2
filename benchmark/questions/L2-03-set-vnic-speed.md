# Setting a vNIC speed

## Prompt
- An application owner asks for their VM to be limited to 500 Mbps of network bandwidth.
- The VM has one VMXNET3 adapter. Windows shows its link speed as 10 Gbps, although the host uplinks are 25 GbE.
- The VM's port group is on a vSphere Distributed Switch with Network I/O Control version 3 enabled.

Which statements are correct?

- A. Setting the adapter speed to 500 Mbps in the Windows adapter properties caps the VM at 500 Mbps.
- B. The 10 Gbps that Windows shows is a label the virtual adapter reports, not a limit on its throughput.
- C. The VMXNET3 adapter can never move more than 10 Gbps, the link speed it reports to Windows.
- D. The VMX option that changes the reported link speed accepts only 10 Gbps and up, so 500 Mbps cannot be set there.
- E. A traffic shaping policy on the port group, with average and peak bandwidth, can cap the VM's bandwidth.
- F. A Network I/O Control limit set on the VM's network adapter can cap its bandwidth.
- G. A Network I/O Control limit takes effect only when the uplink is saturated.
- H. A Network I/O Control limit on the adapter caps both the traffic the VM sends and the traffic it receives.
- I. On a distributed switch, traffic shaping can be set separately for traffic into and out of the VM.
- J. A Network I/O Control reservation of 500 Mbps on the adapter also caps the VM at 500 Mbps.
- K. Network I/O Control shares hold the VM to its share of the uplink even when the uplink is idle.
- L. When an adapter limit and a port group shaping average both apply, the lower of the two sets the cap.

## Likely wrong answer
- A: "Just set the NIC to 500 Mbps in Windows (or in the VM settings) and it can't send more than that."

## Expected key points
- Answer: B, D, E, F, I, L.
- A is false: the guest speed setting caps nothing; 500 Mbps cannot be allocated through the vNIC speed.
- B is true: the virtual device has no physical link to negotiate; VMXNET3 reports 10 Gbps by default, whatever the vmnic behind the port group.
- C is false: the adapter moves data as fast as host CPU, virtual switch policies and uplinks allow; VM-to-VM traffic on one host can exceed the reported speed.
- D is true: `ethernetX.linkspeed` (vSphere 8.0 Update 2 and later) accepts 10,000 to 65,000 Mbps; a value outside the range falls back to 10 Gbps, and the setting caps nothing.
- E is true: traffic shaping (average, peak, burst) is a port group policy that caps bandwidth.
- F is true: Network I/O Control v3 gives each VM network adapter shares, a reservation and a limit.
- G is false: Network I/O Control limits are enforced even when the switch is not saturated.
- H is false: Network I/O Control controls transmit traffic only; traffic shaping can cover receive.
- I is true: a distributed switch shapes in and out; a standard switch shapes outbound only.
- J is false: a reservation is a guaranteed minimum, not a cap.
- K is false: shares divide the link only among consumers that want bandwidth; unused bandwidth is available to others.
- L is true: a 200 Mbps adapter limit under a 100 Mbps shaping average gives 100 Mbps.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
- Revised 2026-11-12. The VMX setting is `ethernetX.linkspeed`, from vSphere 8.0 Update 2, 10,000 to 65,000 Mbps; values outside the range fall back to 10 Gbps. Vendor sources for the reported link speed: Broadcom KB 368812, How to change the vmxnet3 link speed of a VM, https://knowledge.broadcom.com/external/article/368812/how-to-change-the-vmxnet3-link-speed-of.html; Broadcom KB 444078, VMXNET3 guest OS link speed does not enforce bandwidth limits, https://knowledge.broadcom.com/external/article/444078/vmxnet3-guest-os-link-speed-resets-and-d.html.
- Prompt sharpened: the port group is on a distributed switch with Network I/O Control v3, so the options on Network I/O Control and on shaping in each direction are decidable.
- Converted from judged to multiple choice (Q199 F, 2026-11-14).

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
answer: [B, D, E, F, I, L]
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
