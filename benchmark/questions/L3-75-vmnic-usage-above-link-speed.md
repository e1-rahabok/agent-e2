# vmnic Usage above the link speed

## Prompt
- The network team's alert on vmnic Usage fired on an ESXi host.
- They say the port is oversubscribed and ask for a second port.
- See [the vSphere Client network chart of the vmnic](0413/vcenter-vmnic-network-real-time.png) and [the host's Physical adapters page](0413/vcenter-host-physical-adapters.png).

Which statements are correct?

- A. Usage adds receive and transmit, so it can pass the link speed with no fault.
- B. A port cannot carry more than its link speed, so a Usage above it shows a counter error.
- C. On a full-duplex port, each direction has the full link speed to itself.
- D. Receive runs at about 90% of the link speed, close to the limit of that direction.
- E. Divided by twice the link speed, Usage shows the port well below its capacity in both directions.
- F. Add a second port, because Usage above the link speed shows the port is oversubscribed.
- G. The chart values are kilobytes per second: about 1,100,000 KBps of receive is about 9 Gb/s.
- H. Usage is the higher of the receive and transmit rates.

## Input to supply
- Product and version: vSphere 9.1 (ESXi 9.1, vSphere Client 9.1).
- Object: one ESXi host with a 10 GbE vmnic, full duplex (the options use 10 GbE values).
- How to produce it: send about 9 Gb/s into VMs on the host through that vmnic (iperf3 from servers outside the host, several parallel streams) and, at the same time, about 3-6 Gb/s out of VMs on the host through the same vmnic (iperf3 in the other direction). Keep it steady for 10 minutes.
- Screen 1, vSphere Client > the host > Monitor > Performance > Advanced > Network, Chart Options: Real-time, object the vmnic only, counters Usage, Data receive rate and Data transmit rate, with the legend table (Units column, Latest, Maximum, Average). Save as `0413/vcenter-vmnic-network-real-time.png`.
- Screen 2, vSphere Client > the host > Configure > Networking > Physical adapters, with the vmnic's row (Actual Speed, Configured Speed) and its duplex visible. Save as `0413/vcenter-host-physical-adapters.png`.
- Condition the key depends on: Data receive rate 1,040,000-1,160,000 KBps (85-95% of 10 Gb/s); Data transmit rate 366,000-732,000 KBps (30-60% of 10 Gb/s); Usage equal to receive plus transmit and above 1,220,000 KBps (10 Gb/s); the Physical adapters page shows 10 Gbit/s and full duplex.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
B: a port cannot carry more than its link speed, so the counter is wrong. Or F: add a port because Usage passed the link speed.

## Expected key points
- Answer: A, C, D, G.
- A true: Usage rate = receive + transmit; with full duplex it can exceed the physical link speed.
- B false: Usage counts both directions of a full-duplex port; the counter is right.
- C true: full duplex is 100% in each direction: a 10 Gb port handles 10 Gb transmit plus 10 Gb receive.
- D true: receive at about 9 Gb/s on a 10 Gb port is near the limit of that direction, whatever transmit does.
- E false: the over-correction. Averaging the two directions hides that receive is near its own limit; each direction is judged against the link speed.
- F false: the wrong action, for the wrong reason. Usage above the link speed is expected; the risk, if any, is the receive direction alone.
- G true: vSphere Client network rates are kilobytes per second; 1,100,000 x 8 / 1,000 is about 8,800 Mb/s, about 9 Gb/s.
- H false: Usage is the sum of receive and transmit, not the higher of the two.

## Notes
- Paired with the theory question 0040 (theory and practical; design.md, section 3.9).
- Units per vcenter-statistics, section Units (vSphere 9.1 documentation and API: network rates in kilobytes per second).
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item C18 (origin: synthetic). Counts only after author approval.

## Metadata
```yaml
id: "0413"
title: "vmnic Usage above the link speed"
product: [vsphere]
technology: [network]
task: read-metric
level: 300
answer_type: deterministic
input: [screenshot]
object: [esxi, network]
tool: [vcenter]
knowledge:
  - vsphere/technology/network/concepts/network-characteristics
  - vsphere/technology/network/metrics/host/throughput
  - vsphere/tools/vsphere-client/vcenter-statistics
knowledge_main: vsphere/technology/network/concepts/network-characteristics
attachments:
  - 0413/vcenter-vmnic-network-real-time.png
  - 0413/vcenter-host-physical-adapters.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C18"
answer: [A, C, D, G]
misconception: [B, F]
misconception_type: [unit-and-normalization]
pair: "0040"
status: awaiting-input
```
