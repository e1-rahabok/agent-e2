# Broadcast flood in a VLAN

## Prompt
- An ESXi cluster of 6 hosts on one distributed switch runs 40 VMs in VLAN 30. The hosts' vMotion VMkernel ports use VLAN 31 on the same uplinks.
- After a software update, one VM in VLAN 30 starts sending about 200,000 broadcast packets per second.

Which statements are correct?

- A. Every VM of VLAN 30, on all 6 hosts, has to receive and process each of these broadcasts.
- B. The vMotion VMkernel ports in VLAN 31 also receive the broadcasts, because they share the uplinks.
- C. Placing a VLAN 30 VM on the host with the most free CPU keeps the broadcasts away from it.
- D. The drops on the receiving VMs point to the sender.
- E. The sending VM shows the flood in its transmitted broadcast packet counter.
- F. A guest that cannot empty its receive ring in time drops packets, which the VM counts as receive drops.
- G. Low uplink throughput in Mbps shows that the flood puts little load on the hosts and VMs.
- H. Any broadcast in a VLAN is a fault: a healthy VM receives none.

## Likely wrong answer
D: the VMs that drop the most are where the flood comes from. Or G: reading low Mbps as low load.

## Expected key points
- Answer: A, E, F.
- A true: a VLAN is one broadcast domain; a broadcast reaches every port of the VLAN on every host that carries it, and each packet costs CPU to receive, whatever its size.
- B false: a broadcast stays inside its VLAN; VLAN 31 is another broadcast domain, even on the same uplinks.
- C false: the wrong action. The VLAN spans the hosts, so the VM receives every broadcast on any host; free CPU only changes how many it drops.
- D false: the misconception. The receivers show the drops; the sender shows the transmitted broadcasts.
- E true: VM broadcast packets are counted per direction; the sender transmits them.
- F true: when the guest does not empty the ring in time (CPU busy inside the guest, or the vCPU waiting), the new frame is discarded and counted as a receive drop.
- G false: broadcast packets are small; the load is the packet rate, not the bandwidth.
- H false: the over-correction. Broadcast has purposes and should be low, not zero; even a vCenter VM receives some broadcasts.

## Notes
- Theory half of the pair with 0216 (practical; design.md, section 3.9). Different VLANs and numbers from 0216.
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item B18 (origin: synthetic). Counts only after author approval.
- Review 2026-11-15: new situation (the second VLAN carries vMotion, not VMs) and options reworded away from 0216; B, C and A rest on the VLAN line added to distributed-switch/packets (vSphere 9.1 documentation). Key unchanged: A, E, F.

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
  - vsphere/technology/network/concepts/packet-drop-accounting
knowledge_main: vsphere/technology/network/metrics/distributed-switch/packets
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item B18"
answer: [A, E, F]
misconception: [D, G]
misconception_type: [unit-and-normalization]
pair: "0216"
status: draft
```
