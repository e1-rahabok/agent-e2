# Port group drops: received or transmitted

## Prompt
- VCF Operations. The distributed port group PG-App has 10 VMs. The red alert of the port group fires when more than 10% of the packets are dropped. The alert notifies the network team's queue.
- Measured in a 5-minute cycle, summed over the 10 VMs:
  - Transmitted: 38.0 million packets, of which 0.19 million were dropped.
  - Received: 41.0 million packets, of which 6.15 million were dropped.
- 5.9 million of the received drops belong to one VM, a Windows Server 2022 VM with a VMXNET3 adapter at the default receive buffer settings. That VM runs a backup agent; its Guest OS shows a long CPU queue, and the host counter for the adapter shows "running out of buffers" rising.
- The physical network shows no errors on the uplinks, and the port group is configured with the default security policy (promiscuous mode rejected).

Which statements are correct?

- A. Transmit drops are 0.5%, under the red value; most receive drops are one VM's full receive ring, a Guest OS fix that is not for the network team's alert.
- B. The received share is 15%, so the port group alert is right to go red, and the network team should check the upstream fabric before the VM.
- C. Transmitted and received together give 8.0%, below the 10% red value, so the port group has no problem and the received drops can be ignored.
- D. The received drops are harmless: TCP resends every dropped segment, so the data arrives in full and the backup VM is not slowed.
- E. ESXi cannot see a full receive ring inside the guest, so the backup VM's 5.9 million received drops were lost on the physical network.

## Answers
A

## Explanation
- A is correct: transmit 0.19 / 38.0 = 0.5%, far under 10%, and transmit drops are what the infrastructure team owns. 0.5% is below the alert, not proof of a clean network: a data center network should be free of drops. 5.9 of the 6.15 million received drops come from one VM whose host counter shows "running out of buffers" and whose Guest OS has a long CPU queue: a full receive ring, caused and fixed in the Guest OS, so it does not belong in the network team's port group alert.
- B is wrong: 15% (6.15 / 41.0) is real, but the uplinks are clean and the drops sit on one VM's receive ring; checking the upstream fabric first sends the case to the wrong team. Not every received drop on a port group is a network fault.
- C is wrong: (0.19 + 6.15) / (38.0 + 41.0) = 8.0% is the right arithmetic, but the combined share hides one VM's real receive problem.
- D is wrong: TCP resends, so the data arrives, but the cost is time (a smaller congestion window, retransmit timeouts), so the VM loses speed; UDP is not resent.
- E is wrong: ESXi counts a full VMXNET3 receive ring at the port and on the VM (droppedRx, %DRPRX), and the guest sees it too; the host counter "running out of buffers" shows it here, and the uplinks show no errors.
- Action for the Guest OS owner: first the vCPU that drains the ring (the Guest OS CPU queue, VM CPU Ready and Co-stop), then RSS if the adapter has one receive queue, and only then a larger ring; a larger ring only delays the drops while the vCPU is starved (Broadcom KB 312565, KB 440347).
- Misconception: B or E: a dropped packet on a port group is read as a network fault whatever the direction, as the port group is a network object.

## Notes
- Public source: Broadcom KB 312565 "The output of esxtop shows dropped receive packets at the virtual switch" (https://knowledge.broadcom.com/external/article?articleNumber=312565): drops happen between the virtual switch and the guest driver when the receive ring is full, so esxtop shows them at the switch. Broadcom KB 324556 "Packet loss in the guest OS using VMXNET3 in ESXi" (https://knowledge.broadcom.com/external/article/324556/packet-loss-in-the-guest-os-using-vmxnet.html): the vsish counters "running out of buffers" and "# of times the 1st ring is full"; Windows ring and buffer settings; larger buffers use more host memory. Broadcom KB 440347 "Mitigating VMXNET3 adapter packet drops due to single receive queue": RSS in the guest.
- Knowledge file logic: vsphere/object-types/distributed-port-group/distributed-port-group-alerts, section "Distributed port group dropped packets" (planned change: count transmitted only; received drops include packets not for the VM, security settings and a full receive ring, whose cause and fix are in the Guest OS) and Misconceptions ("every received drop on a port group is a network fault").
- Why one answer: the three numbers (0.5%, 15%, 8.0%) and the one VM with 5.9 of 6.15 million drops separate the cases, and the Guest OS cause is documented by the KB.
- Debatable risk: leaving received drops out of the port group alert is a planned design. A says only that this case's ring drops do not belong in the network team's alert, which the clean uplinks and the one-VM concentration decide. Audit 2026-11-15: one review judged the earlier A false over "so the network is healthy" and an unstated drop formula; the blind key check judged it true. A and the stem were reworded (counts given as "of which ... were dropped"; no health verdict) so A is true as keyed.
- Deferred 2026-11-16 (author, Q-E2-248 moved to Future release): the vendor documents give no denominator for the port group drop percentage, and A rests on the stem's own arithmetic, on which two reviewers disagreed. Runs again once Q-E2-248 is answered. Key unchanged.
- Stem made plural (2026-11-14): the singular form told the candidate that one option is correct (Q-E2-199: the count is never disclosed). Was: "Which statement is correct?"

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
misconception: [B, E]
misconception_type: [layer-confusion, average-hides-worst]
status: deferred
```
