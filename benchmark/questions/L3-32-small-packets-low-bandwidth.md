# Small packets at low bandwidth

## Prompt
- log-03 is a log collector VM. About 3,000 devices send it syslog messages over UDP.
- Since the device count doubled, the collector loses messages at peak.
- The host uplinks are 25 GbE. The network team says the uplink carrying log-03 is at 1.9%, so the network cannot be the problem.
- vCenter real-time chart of log-03, one 20-second sample at peak:
  - Packets received: 6,000,000
  - Data receive rate: 58,600 KBps

Which statements are correct?

- A. log-03 receives about 300,000 packets per second in this peak sample.
- B. The average packet that log-03 receives is about 200 bytes long.
- C. At 1.9% of the uplink, the VM's network path cannot be what limits it.
- D. Packets received leaves out broadcast and multicast, so part is missing.
- E. Packets received includes the packets that ESXi dropped for the VM.

## Likely wrong answer
C: reading bandwidth utilization as network load. A low share of the link says nothing about a high packet rate.

## Expected key points
- Answer: A, B.
- A: in the real-time chart, Packets received is a count per 20-second sample: 6,000,000 ÷ 20 = 300,000 packets per second.
- B: 58,600 KBps is kilobytes per second; 58,600 × 1,000 bytes ÷ 300,000 ≈ 195 bytes per packet (200 with 1,024 bytes per KB).
- C is wrong: with small packets the load is the packet rate, not the bandwidth. Each packet costs CPU in the host and in the guest to receive, whatever its size. A 10 GbE link of 1,500-byte frames peaks near 833,000 packets per second each way; this one VM takes 300,000 per second at only 1.9% of a 25 GbE link.
- D is wrong: the packet count includes broadcast and multicast.
- E is wrong: the packet counts exclude dropped packets; drops have their own counters.
- Next: check the VM's receive drops and its vCPU usage, and the guest's receive processing, before asking for more bandwidth.

## Notes
- Drafted by Claude 2026-11-12 for the network slots of question set 1.0 (origin: synthetic). Counts only after author approval.

## Metadata
```yaml
id: "0211"
title: "Small packets at low bandwidth"
product: [vsphere]
technology: [network]
object: [vm]
tool: [vcenter]
task: read-metric
level: 300
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/technology/network/metrics/virtual-motherboard/packets
  - vsphere/technology/network/metrics/virtual-motherboard/throughput
  - vsphere/technology/network/metrics/vm-network-metrics
  - vsphere/tools/esxtop/network
knowledge_main: vsphere/technology/network/metrics/virtual-motherboard/packets
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12, network slots (benchmark/design.md, section 3)"
answer: [A, B]
misconception: [C]
misconception_type: [unit-and-normalization]
status: draft
```
