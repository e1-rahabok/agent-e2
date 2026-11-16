# Broadcast flood in a VLAN

## Prompt
- An ESXi cluster of 6 hosts on one distributed switch runs 40 VMs in VLAN 30. The hosts' vMotion VMkernel ports use VLAN 31 on the same uplinks.
- After a software update, one VM in VLAN 30 starts sending about 200,000 broadcast packets per second.

Which statements are correct?

- A. Every VM of VLAN 30, on all 6 hosts, has to receive and process each of these broadcasts.
- B. The vMotion VMkernel ports in VLAN 31 also receive the broadcasts, because they share the uplinks.
- C. Placing a VLAN 30 VM on the host with the most free CPU keeps the broadcasts away from it.
- D. The VM with the most receive drops in VLAN 30 is the source of the flood.
- E. The sending VM shows the flood in its transmitted broadcast packet counter.
- F. Each receiving VM's Packets received counter includes these broadcasts, next to its unicast.
- G. Any broadcast in a VLAN is a fault: a healthy VM receives no broadcast packets at all.

## Answers
A, E, F

## Explanation
- A true: a VLAN is one broadcast domain; a broadcast reaches every port of the VLAN on every host that carries it, and each packet costs CPU to receive, whatever its size.
- B false: a broadcast stays inside its VLAN; VLAN 31 is another broadcast domain, even on the same uplinks.
- C false: the wrong action. The VLAN spans the hosts, so the VM receives every broadcast on any host; free CPU only changes how many it drops.
- D false: the misconception. Drops show where the flood is received, not where it starts: the receivers drop, while the sender shows the transmitted broadcasts (E).
- E true: VM broadcast packets are counted per direction; the sender transmits them.
- F true: a VM's packet counts include broadcast and multicast packets (and exclude dropped ones), so the flood shows in Packets received of every VM in VLAN 30.
- G false: the over-correction. Broadcast has purposes and should be low, not zero; even a vCenter VM receives some broadcasts.
- Misconception: D: "the VM that drops the most is where the flood comes from."

## Notes
- Theory half of the pair with 0216 (practical; design.md, section 3.9). Different VLANs and numbers from 0216.
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item B18 (origin: synthetic).
- Review 2026-11-15: new situation (the second VLAN carries vMotion, not VMs) and options reworded away from 0216; B, C and A rest on the VLAN line added to distributed-switch/packets (vSphere 9.1 documentation). Key unchanged: A, E, F.
- Audit 2026-11-15: F (a full guest ring counts as a VM receive drop; redundancy #54, over the cap) replaced in place with "Packets received includes the broadcasts" (vm-network-metrics; second question with 0211 D). G (low Mbps read as low load; redundancy #60, over the cap) dropped with no replacement: old H relettered to G (letter map: A-F unchanged, H -> G). D made concrete. misconception_type emptied: unit-and-normalization went with old G.

## Metadata
```yaml
id: "0411"
title: "Broadcast flood in a VLAN"
product: [vsphere]
technology: [network]
task: troubleshoot
level: 300
answer_type: deterministic
input: [text]
object: [vm, network]
tool: [none]
knowledge:
  - vsphere/technology/network/metrics/distributed-switch/packets
  - vsphere/technology/network/metrics/virtual-motherboard/packets
  - vsphere/technology/network/metrics/vm-network-metrics
knowledge_main: vsphere/technology/network/metrics/distributed-switch/packets
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item B18"
misconception: [D]
misconception_type: []
pair: "0216"
status: draft
```
