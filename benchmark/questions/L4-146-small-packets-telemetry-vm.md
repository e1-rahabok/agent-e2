# A load balancer VM times out at low bandwidth

## Prompt
- A VM runs a software load balancer in front of a web farm. During a sales campaign, clients get timeouts.
- The VM's owner points to the bandwidth: the VM uses a few percent of its 10 Gb/s link, so he looks for the cause in the web servers.
- See [the vSphere Client network chart of the load balancer VM](0415/vcenter-vm-network-packets-real-time.png).

Which statements are correct?

- A. Packets received is a count per 20-second sample: divided by 20 it gives packets per second.
- B. Packets received / 300 gives packets per second in this chart.
- C. The VM receives roughly 100,000 to 200,000 packets per second.
- D. The average received packet is about 120 to 250 bytes long.
- E. A VM that uses a few percent of its link's bandwidth cannot be limited by its network path.
- F. The Data receive rate line can be ignored here: the packet line alone tells the story.
- G. Give the VM a faster uplink, a 25 Gb/s port instead of 10 Gb/s.
- H. Data receive rate is in kilobits per second.
- I. Each received packet costs CPU to process, whatever its size.
- J. The Packets received line also counts packets ESXi discarded before delivery.
- K. On this chart the VM receives about 2 to 4 million packets per second.

## Input to supply
- Product and version: vSphere 9.1 (vSphere Client 9.1).
- Object: one receiving VM with one VMXNET3 adapter.
- How to produce it: run `iperf3 -s` in the VM; from another machine, `iperf3 -c <vm> -u -l 128 -b 150M -t 900` (UDP, 128-byte payloads, about 150,000 packets per second). Wait 2 minutes before capturing.
- Screen, vSphere Client > the VM > Monitor > Performance > Advanced > Network, Chart Options: Real-time, object the VM, counters Packets received, Data receive rate and Receive packets dropped, with the legend table (Units column, Latest, Maximum, Average). Save as `0415/vcenter-vm-network-packets-real-time.png`.
- Condition the key depends on: Packets received 2,000,000-4,000,000 per 20-second sample (Latest); Data receive rate 15,000-40,000 KBps; average packet size (Data receive rate x 1,024 / (Packets received / 20)) between 120 and 250 bytes.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
E: a few percent of the bandwidth, so the network cannot be the problem. Or K: reading the count per sample as packets per second.

## Expected key points
- Answer: A, C, D, I.
- A true: packet counters are totals per sample interval, not per second; the Real-time interval is 20 seconds.
- B false: 300 seconds is the 5-minute interval of the 1 Day history; a Real-time sample is 20 seconds.
- C true: the screen reading. 2,000,000 to 4,000,000 per 20-second sample is 100,000 to 200,000 packets per second.
- D true: average packet size = throughput / packet rate; for example 25,000 KBps x 1,024 / 150,000 is about 170 bytes, far below 1,500.
- E false: the misconception. With small packets the load is the packet rate, not the bandwidth; low Mbps does not mean low network load.
- F false: the over-correction. The data rate is needed to compute the packet size, which shows that the packets are small.
- G false: the wrong action. The bandwidth is not the limit; a faster port adds nothing. Check the VM's receive drops and CPU first.
- H false: vCenter network rates are kilobytes per second.
- I true: each packet costs CPU to receive; bandwidth can remain while packets per second saturate.
- J false: packet counts exclude dropped packets; drops have their own counters.
- K false: the screen reading. The chart's 2 to 4 million is a count per 20-second sample, about 100,000 to 200,000 per second.

## Notes
- Paired with the theory question 0211 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item C20 (origin: synthetic). Counts only after author approval.
- Review 2026-11-15: new situation (a load balancer, not a UDP collector); options reworded away from 0211; B no longer the negation of A; K (a false screen reading) added. Key unchanged: A, C, D, I. The lab method stays a UDP stream with small packets: the screen shows only counts and rates.

## Metadata
```yaml
id: "0415"
title: "A load balancer VM times out at low bandwidth"
product: [vsphere]
technology: [network]
task: troubleshoot
level: 400
answer_type: deterministic
input: [screenshot]
object: [vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/network/metrics/virtual-motherboard/packets
  - vsphere/technology/network/metrics/virtual-motherboard/throughput
  - vsphere/technology/network/metrics/vm-network-metrics
  - vsphere/tools/vsphere-client/vcenter-statistics
knowledge_main: vsphere/technology/network/metrics/virtual-motherboard/packets
attachments:
  - 0415/vcenter-vm-network-packets-real-time.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C20"
answer: [A, C, D, I]
misconception: [E, K]
misconception_type: [unit-and-normalization, consumption-as-contention]
pair: "0211"
status: awaiting-input
```
