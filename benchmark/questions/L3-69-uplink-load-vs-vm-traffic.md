# Uplink load and VM network traffic

## Prompt
- An ESXi host has four 25 GbE uplinks on one distributed switch. They carry VM traffic, vMotion and vSAN.
- The capacity planner wants to size the uplinks from the network counters of the VMs on the host.

Which statements are correct?

- A. Traffic between two VMs on the same host and the same port group does not show on any vmnic.
- B. The vmnic counters include VMkernel traffic such as vMotion and vSAN, which no VM counter shows.
- C. The load on the uplinks equals the sum of the VMs' transmit and receive.
- D. VM traffic never crosses the uplinks, so the VM counters say nothing about them.
- E. Moving one of two VMs that exchange a lot of traffic to another host raises the uplink load of both hosts.
- F. The vmnic counters break their traffic down per VM.
- G. With full duplex, each 25 GbE uplink carries up to 25 Gb/s in each direction at the same time.
- H. When the VMs' traffic adds up to more than the uplinks' speed, the host needs more uplinks.
- I. A flow between two VMs on the same host counts twice in the VM sum: as transmit on one VM and as receive on the other.

## Likely wrong answer
C: adding up the VMs' throughput and reading it as the load on the uplinks.

## Expected key points
- Answer: A, B, E, G, I.
- A true: VM-to-VM traffic on the same host is switched inside the host and never reaches the physical network; vmnic metrics do not see it.
- B true: the vmnics carry VM and kernel traffic over shared uplinks; vMotion and vSAN use VMkernel ports, not VM ports.
- C false: in-host VM-to-VM traffic and kernel traffic break that equation.
- D false: VM traffic to and from outside the host does cross the uplinks; only in-host flows stay off them.
- E true: once the two VMs sit on different hosts, their flow leaves both hosts through the uplinks.
- F false: physical NICs have no per-VM or per-kernel-interface breakdown.
- G true: full duplex is 100% in each direction.
- H false: the VM sum is not the uplink load; plan uplink capacity from the vmnic counters, per direction.
- I true: each VM's counters measure its own side of the flow, so one in-host flow appears on two VM ports and on no vmnic.

## Notes
- Theory half of the pair with 0217 (practical; design.md, section 3.9). Different host and numbers from 0217.
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item B9 (origin: synthetic). Counts only after author approval.

## Metadata
```yaml
id: "0407"
title: "Uplink load and VM network traffic"
product: [vsphere, vsan]
technology: [network]
task: decide-capacity
level: 300
answer_type: deterministic
input: [text]
object: [esxi, vm, network]
tool: [vcenter]
knowledge:
  - vsphere/technology/network/concepts/network-observability
  - vsphere/technology/network/concepts/network-characteristics
  - vsphere/technology/network/metrics/host/throughput
knowledge_main: vsphere/technology/network/concepts/network-observability
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item B9"
answer: [A, B, E, G, I]
misconception: [C]
misconception_type: [provider-vs-consumer, same-name-other-object]
pair: "0217"
status: draft
```
