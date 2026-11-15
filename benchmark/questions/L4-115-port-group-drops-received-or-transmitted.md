# Port group drops: received or transmitted

## Prompt
- VCF Operations. The distributed port group PG-App has 10 VMs. The red alert of the port group fires when more than 10% of the packets are dropped. The alert is owned by the infrastructure team, above all the network team.
- Measured in a 5-minute cycle, summed over the 10 VMs:
  - Transmitted: 38.0 million packets, 0.19 million dropped.
  - Received: 41.0 million packets, 6.15 million dropped.
- 5.9 million of the received drops belong to one VM, a Windows Server 2022 VM with a VMXNET3 adapter at the default receive buffer settings. That VM runs a backup agent; its Guest OS shows a long CPU queue, and the host counter for the adapter shows "running out of buffers" rising.
- The physical network shows no errors on the uplinks, and the port group is configured with the default security policy (promiscuous mode rejected).

Which statements are correct?

- A. The transmitted drops are 0.5%, so the network is healthy. The 15% received drops are mostly one VM's full receive ring, which the Guest OS side owns, so the port group alert should count transmitted packets and not open a network ticket for this.
- B. The received drops are 15%, so the port group alert is right to go red and the network team should check the upstream fabric first.
- C. Transmitted and received together give 8.0%, below 10%, so there is no problem on the port group and the received drops can be ignored.
- D. The received drops are harmless: TCP resends every dropped segment, so the data arrives and the VM is not slowed.
- E. The transmitted drops are 0.5%, so the VM adapter is healthy. A received drop on a port group is always a physical network fault, because the vNIC only transmits.

## Likely wrong answer
B or E: a drop is read as a network fault whatever the direction, as the port group is a network object.

## Expected key points
- Answer: A.
- The transmitted share is 0.19 / 38.0 = 0.5%. Drops here are on the path the infrastructure owns (the VM to the switch and out), and it is far under 10%.
- The received share is 6.15 / 41.0 = 15%, but 5.9 of the 6.15 million drops come from one VM. A received drop includes packets that the VM's adapter cannot take because its receive ring is full, and packets not destined to the VM or refused by the security policy. A full ring depends on the Guest OS: driver, ring size, CPU to drain the queue, and RSS. The counter "running out of buffers" and the long CPU queue point to it (B and E are wrong).
- Combined, (0.19 + 6.15) / (38.0 + 41.0) = 8.0%: below the 10% red value, so a combined count hides a real problem of the VM and sends an unclear signal (C is wrong).
- D is wrong: TCP resends, so the data arrives, but the cost is time (lower congestion window, retransmit timeouts), and that VM does lose speed; UDP is not resent.
- Action: for the infrastructure alert, count transmitted packets only; send the received-drop case to the VM and Guest OS owner: raise the receive buffer or ring size in steps, enable multiple receive queues (RSS), and fix the CPU that drains the queue.

## Notes
- Public source: Broadcom KB 312565 "The output of esxtop shows dropped receive packets at the virtual switch" (https://knowledge.broadcom.com/external/article?articleNumber=312565): drops happen between the virtual switch and the guest driver when the receive ring is full, so esxtop shows them at the switch. Broadcom KB 324556 "Packet loss in the guest OS using VMXNET3 in ESXi" (https://knowledge.broadcom.com/external/article/324556/packet-loss-in-the-guest-os-using-vmxnet.html): the vsish counters "running out of buffers" and "# of times the 1st ring is full"; Windows ring and buffer settings; larger buffers use more host memory. Broadcom KB 440347 "Mitigating VMXNET3 adapter packet drops due to single receive queue": RSS in the guest. I did not read the page dates of these KB articles.
- Knowledge file logic: vsphere/object-types/distributed-port-group/distributed-port-group-alerts, section "Distributed port group dropped packets" (planned change: count transmitted only; received drops include packets not for the VM, security settings and a full receive ring, whose cause and fix are in the Guest OS) and Misconceptions ("every received drop on a port group is a network fault").
- Why one answer: the three numbers (0.5%, 15%, 8.0%) and the one VM with 5.9 of 6.15 million drops separate the cases, and the Guest OS cause is documented by the KB.
- Debatable risk: whether the port group alert should count transmitted only is the author's planned design. The question asks which statement is correct about this case, not about the current alert definition. Option A says "should count transmitted packets", which an expert could contest for a case with a real upstream fault; the prompt closes it with no uplink errors and the one-VM concentration.
- Stem made plural (2026-11-14): the singular form told the candidate that one option is correct (Q199: the count is never disclosed). Was: "Which statement is correct?"

## Metadata
```yaml
id: "0345"
title: "Port group drops: received or transmitted"
product: [vcf-operations, vsphere, windows]
technology: [network, system]
task: troubleshoot
level: 400
answer_type: deterministic
input: [text]
object: [network, vm, guest-os]
tool: [vcf-operations, guest-os-tools]
knowledge:
  - vsphere/object-types/distributed-port-group/distributed-port-group-alerts
  - vsphere/technology/network/concepts/packet-drop-accounting
  - vsphere/technology/network/vnic-rx-drops
knowledge_main: vsphere/object-types/distributed-port-group/distributed-port-group-alerts
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
answer: [A]
misconception: [B, E]
misconception_type: [layer-confusion, average-hides-worst]
status: draft
```
