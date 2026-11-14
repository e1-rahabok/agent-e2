# A telemetry VM loses messages at low bandwidth

## Prompt
- A telemetry ingest VM receives sensor messages over UDP. Since more sensors were added, the application reports gaps in the data.
- The network team says the VM uses a tiny part of its 10 Gb/s uplink, so the network cannot be the cause.
- See [the vSphere Client network chart of the VM](0415/vcenter-vm-network-packets-real-time.png).

Which statements are correct?

- A. Packets received is a count per 20-second sample: divided by 20 it gives packets per second.
- B. Packets received is already a rate in packets per second.
- C. The VM receives roughly 100,000 to 200,000 packets per second.
- D. The average received packet is about 120 to 250 bytes long.
- E. A small share of the uplink's bandwidth shows that the network path cannot limit the VM.
- F. Bandwidth counters are of no use for this VM: only packet counts matter.
- G. Move the VM to a host with faster uplinks.
- H. Data receive rate is in kilobits per second.
- I. Each received packet costs CPU in the host and in the guest, whatever its size.
- J. Packets received includes the packets that ESXi dropped for the VM.

## Input to supply
- Product and version: vSphere 9.1 (vSphere Client 9.1).
- Object: one receiving VM with one VMXNET3 adapter.
- How to produce it: run `iperf3 -s` in the VM; from another machine, `iperf3 -c <vm> -u -l 128 -b 150M -t 900` (UDP, 128-byte payloads, about 150,000 packets per second). Wait 2 minutes before capturing.
- Screen, vSphere Client > the VM > Monitor > Performance > Advanced > Network, Chart Options: Real-time, object the VM, counters Packets received, Data receive rate and Receive packets dropped, with the legend table (Units column, Latest, Maximum, Average). Save as `0415/vcenter-vm-network-packets-real-time.png`.
- Condition the key depends on: Packets received 2,000,000-4,000,000 per 20-second sample (Latest); Data receive rate 15,000-40,000 KBps; average packet size (Data receive rate x 1,024 / (Packets received / 20)) between 120 and 250 bytes.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
E: a tiny share of the bandwidth, so the network cannot be the problem. Or B: reading the packet count as packets per second.

## Expected key points
- Answer: A, C, D, I.
- A true: packet counters are totals per sample interval, not per second; the Real-time interval is 20 seconds.
- B false: the counter is a summation over the 20-second sample.
- C true: 2,000,000 to 4,000,000 per sample is 100,000 to 200,000 packets per second.
- D true: average packet size = throughput / packet rate. For example 25,000 KBps x 1,024 / 150,000 is about 170 bytes, far below 1,500.
- E false: with small packets the load is the packet rate, not the bandwidth; low Mbps does not mean low network load.
- F false: the over-correction. The data rate is needed to compute the packet size, which shows that the packets are small.
- G false: the uplink bandwidth is not the limit; faster uplinks add nothing. Check the VM's receive drops and CPU first.
- H false: vCenter network rates are kilobytes per second.
- I true: each packet costs CPU to receive; bandwidth can remain while packets per second saturate.
- J false: packet counts exclude dropped packets; drops have their own counters.

## Notes
- Paired with the theory question 0211 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item C20 (origin: synthetic). Counts only after author approval.

## Metadata
```yaml
id: "0415"
title: "A telemetry VM loses messages at low bandwidth"
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
misconception: [E]
misconception_type: [unit-and-normalization, consumption-as-contention]
pair: "0211"
status: awaiting-input
```
