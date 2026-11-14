# Broadcast flood in a VLAN

## Prompt
- One VM in VLAN 30 starts sending about 200,000 broadcast packets per second.
- VLAN 30 has 40 VMs spread over 6 hosts that share one distributed switch. VLAN 31 runs on the same hosts and uplinks.

Which statements are correct?

- A. Every VM in VLAN 30 takes in each broadcast and spends guest CPU on it.
- B. The VMs in VLAN 31 receive these broadcasts too, because they share the hosts and uplinks.
- C. Moving a receiving VM to a less busy host of the cluster stops it from receiving the flood.
- D. The VMs with the most receive drops are the source of the flood.
- E. The sending VM shows the flood in its transmitted broadcast packets.
- F. A guest that cannot empty its receive ring in time drops packets, which the VM counts as receive drops.
- G. Low uplink throughput in Mbps shows that the flood puts little load on the hosts and VMs.
- H. Any broadcast in a VLAN is a fault: a healthy VM receives none.

## Likely wrong answer
D: blaming the VMs that show the most drops. Or G: reading low Mbps as low load.

## Expected key points
- Answer: A, E, F.
- A true: a broadcast is delivered to every VM of its broadcast domain, and each packet costs CPU to receive, whatever its size.
- B false: a broadcast stays inside its VLAN; VLAN 31 is another broadcast domain.
- C false: the VLAN spans the hosts, so the VM still receives every broadcast on another host.
- D false: the receivers show the drops; the source shows the transmitted broadcasts.
- E true: VM broadcast packets are counted per direction; the source transmits them.
- F true: when the guest does not empty the ring in time (CPU busy inside the guest, or the vCPU waiting), the new frame is discarded and counted as a receive drop.
- G false: broadcast packets are small; the load is the packet rate, not the bandwidth.
- H false: broadcast has purposes and should be low, not zero; even a vCenter VM receives some broadcasts.

## Notes
- Theory half of the pair with 0216 (practical; design.md, section 3.9). Different VLANs and numbers from 0216.
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item B18 (origin: synthetic). Counts only after author approval.

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
