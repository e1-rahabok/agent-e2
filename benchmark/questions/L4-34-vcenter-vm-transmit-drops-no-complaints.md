# Transmit drops with no complaints

## Prompt
The attached screenshot is the vSphere Client performance chart of a VM: network packets transmitted, received, transmit packets dropped and receive packets dropped, over one day.

- Transmit packets dropped is above 0 most of the day. Receive packets dropped is 0.
- Nobody has reported a problem with the application.

Which statements are correct? Choose all that apply.

- A. Transmit drops can be large without complaints: TCP retransmits the packets, and the application sees only higher latency.
- B. No complaints, so the drops can be ignored.
- C. The drops count against the VM KPI: transmit dropped packets is one of its contention sub-metrics.
- D. The drops are caused by a full receive ring in the VMXNET3 driver.

## Input to supply
- Tool: vSphere Client 9.1, VM > Monitor > Performance > Advanced > Network, one day.
- Counters: packetsTx, packetsRx, droppedTx, droppedRx for the VM.
- Condition for the key: droppedTx above 0 for most of the day; droppedRx at 0.
- Mask VM names if they reveal the customer.
- Save as `benchmark/questions/74/vcenter-vm-network-dropped.png`.

## Likely wrong answer
B: ignoring drops because users do not complain.

## Expected key points
- Answer: A, C.
- TCP retransmits hide transmit drops: millions a month can pass without complaints. Profile them with the network team.
- The VM KPI (VM Performance) includes transmit dropped packets as a contention sub-metric; receive drops are left out.
- D is wrong: a full receive ring causes receive drops, and receive drops are 0 here.

## Notes
- Previous id: question-0074 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0074"
title: "Transmit drops with no complaints"
product: [vsphere]
technology: [network]
task: troubleshoot
level: 400
answer_type: deterministic
input: [screenshot]
knowledge:
  - vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
  - vsphere/object-types/vm/kpis/vm-performance
attachments:
  - 0074/vcenter-vm-network-dropped.png
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
answer: [A, C]
trap: [B]
status: awaiting-input
```
