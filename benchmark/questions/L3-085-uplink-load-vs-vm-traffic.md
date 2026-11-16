# Uplink load and VM network traffic

## Prompt
- The hosts of a cluster share one distributed switch; each host has four 25 GbE uplinks that carry VM traffic, vMotion and vSAN.
- A web VM and a database VM run on the same host and port group and exchange several Gb/s. The application team wants an anti-affinity rule to keep them on different hosts.

Which statements are correct?

- A. Two VMs on one host and port group can exchange more than the uplink speed.
- B. A vMotion leaving the host shows on the vmnics and in no VM's network counters.
- C. The two VMs' traffic already loads the uplinks, so moving them apart changes nothing there.
- D. VM traffic never crosses the uplinks, so VM counters say nothing about uplink load.
- E. Once the two VMs run on different hosts, their flow shows on the vmnics of both hosts.
- F. The vmnic counters break the uplink traffic down per VM, so the flow of these two VMs can be read there.
- G. Once the VMs run apart, their one flow uses a single uplink on each host, however many uplinks the team has.
- H. Size the uplinks for the new placement from the sum of all VMs' transmit and receive on the host.
- I. While on one host, their flow counts twice in the sum of the VM counters: as one VM's transmit and the other's receive.

## Likely wrong answer
C: VM traffic is uplink traffic, so placement does not matter. Or D, the overshoot: VM counters say nothing about the uplinks.

## Expected key points
- Answer: A, B, E, G, I.
- A true: VM-to-VM traffic on the same host never reaches the physical network; while it stays in the host it has no fixed limit, and a VMXNET3 adapter can pass the speed it reports.
- B true: vMotion uses a VMkernel port; the vmnics carry VM and kernel traffic over shared uplinks, and no VM counter includes kernel traffic.
- C false: the misconception. Today the flow is switched inside the host and never touches a vmnic.
- D false: the over-correction. VM traffic to and from outside the host does cross the uplinks; only in-host flows stay off them.
- E true: once the two VMs sit on different hosts, their flow leaves both hosts through the uplinks.
- F false: physical NICs have no per-VM or per-kernel-interface breakdown.
- G true: every teaming algorithm maps one vNIC to one uplink, and IP hash maps one source-destination pair to one uplink; one flow between two VMs never gets more than one uplink's speed.
- H false: the wrong action. The VM sum is not the uplink load (in-host flows, kernel traffic); plan from the vmnic counters per direction, plus the flow that the rule moves onto the wire.
- I true: each VM's counters measure its own side, so one in-host flow appears on two VM ports and on no vmnic.

## Notes
- Theory half of the pair with 0217 (practical; design.md, section 3.9). Different host and numbers from 0217.
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item B9 (origin: synthetic).
- Review 2026-11-15: new situation (an anti-affinity rule, not a capacity planner summing VMs) and options reworded away from 0217. Key unchanged: A, B, E, G, I.
- Audit 2026-11-15: G (full duplex per direction) was over the two-question cap (0040/0413 keep it) and was replaced with the one-flow-one-uplink fact of nic-teaming (second question with 0210); F and I evened in length.

## Metadata
```yaml
id: "0407"
title: "Uplink load and VM network traffic"
product: [vsphere, vsan]
technology: [network]
task: explain-mechanism
level: 300
answer_type: deterministic
input: [text]
object: [esxi, vm, network]
tool: [vcenter]
knowledge:
  - vsphere/technology/network/concepts/network-observability
  - vsphere/technology/network/concepts/network-characteristics
  - vsphere/technology/network/metrics/host/throughput
  - vsphere/technology/network/concepts/nic-teaming
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
