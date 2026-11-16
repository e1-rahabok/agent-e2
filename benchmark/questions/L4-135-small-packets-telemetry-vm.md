# A load balancer VM times out at low bandwidth

## Prompt
- lb-web-01 is a VM that runs a software load balancer in front of a web farm, with one VMXNET3 adapter. During a sales campaign, clients get timeouts.
- The VM's owner points to the bandwidth: the VM uses a few percent of its 10 Gb/s link, so he looks for the cause in the web servers.
- [The attached vCenter export](0415/lb-web-01-network-real-time.csv) is the Real-time network view of lb-web-01 for the 30 minutes in which the timeouts started.
- The chart legend (not in the export) gives the unit of the rate and Usage columns: KBps.

Which statements are correct?

- A. Packets received is a count per 20-second sample: divided by 20 it gives packets per second.
- B. Usage divided by the packet rate gives the size of a received packet in this export.
- C. The VM receives roughly 100,000 to 200,000 packets per second.
- D. The average received packet is about 120 to 250 bytes long.
- E. A VM that uses a few percent of its link's bandwidth cannot be limited by its network path.
- F. The Data receive rate column can be ignored here: Packets received alone tells the story.
- G. Give the VM a faster uplink, a 25 Gb/s port instead of 10 Gb/s.
- H. In the export, the rows with receive drops are the rows with the highest Data receive rate.
- I. Each received packet costs CPU to process, whatever its size.
- J. The Packets received column also counts the packets that ESXi dropped before delivery.
- K. In the export, the VM receives about 2 to 4 million packets per second.

## Answers
A, C, D, I

## Explanation
- A true: packet counters are totals per sample interval, not per second; the Real-time interval is 20 seconds (the rows are 20 seconds apart).
- B false: Usage is receive plus transmit, so Usage x 1,024 / (Packets received / 20) gives 260-486 bytes here, overstating the received packet; the size comes from Data receive rate.
- C true: Packets received is between 2,469,827 and 3,701,169 per 20-second sample: about 123,000 to 185,000 packets per second.
- D true: average packet size = throughput / packet rate = Data receive rate x 1,024 / (Packets received / 20); it is 138-236 bytes in every row (for example 24,000 KBps x 1,024 / 180,000 is about 137 bytes), far below 1,500. Usage is receive plus transmit and gives the wrong size.
- E false: the misconception. With small packets the load is the packet rate, not the bandwidth; low Mbps does not mean low network load.
- F false: the over-correction. The data rate is needed to compute the packet size, which shows that the packets are small.
- G false: the wrong action. The bandwidth is not the limit; a faster port adds nothing. Check the VM's receive drops and CPU first.
- H false: Receive packets dropped is above 0 only in rows where Packets received is at least 3,500,000 (175,000 per second); in those rows the packets are smallest and Data receive rate is below every row of the first, quieter part of the window, where the highest Data receive rate is and no packet is dropped. The drops follow the packet rate, not the bandwidth.
- I true: each packet costs CPU to receive; bandwidth can remain while packets per second saturate.
- J false: packet counts exclude dropped packets; drops have their own counters (Receive packets dropped).
- K false: 2.5 to 3.7 million is the count per 20-second sample, about 123,000 to 185,000 per second.
- Misconception: E: a few percent of the bandwidth, so the network cannot be the problem. Or K: reading the count per sample as packets per second.

## Notes
- Paired with the theory question 0211 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item C20 (origin: synthetic).
- Review 2026-11-15: new situation (a load balancer, not a UDP collector); options reworded away from 0211; B no longer the negation of A; K (a false screen reading) added. Key unchanged: A, C, D, I. The lab method stays a UDP stream with small packets: the screen shows only counts and rates.
- Converted 2026-11-15 from a screenshot to a vCenter Real-time CSV (project/practical-questions-as-exports-2026-11-15.md). B, F, J and K reworded from chart to export. H replaced: the old H (Data receive rate is in kilobits per second) made a third question on the KBps unit with 0412 and the old 0413 G; the new H reads Receive packets dropped against Packets received and Data receive rate, still false. Usage and the transmit columns are in the export as near-name columns.
- 2026-11-16 re-review: B (divide by 300) and A were a near-negation pair; B replaced in place with the Usage-based packet size (false). Key-point numbers set to the export (123,491-185,058 packets per second, 138-236 bytes).
- Audit 2026-11-15: the stem no longer says the packet columns are a count per 20-second sample (it gave A away and is the fact A and K test); the unit line keeps KBps, which D needs. Level kept at 400: H reads Receive packets dropped against the packet rate and the data rate, a reading only the mechanism decides; the review's 400 -> 300 relabel conflicts with the pairing plan (C20) and is left to the author.

## Metadata
```yaml
id: "0415"
title: "A load balancer VM times out at low bandwidth"
product: [vsphere]
technology: [network]
task: troubleshoot
level: 400
answer_type: deterministic
input: [table]
object: [vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/network/metrics/virtual-motherboard/packets
  - vsphere/technology/network/metrics/virtual-motherboard/throughput
  - vsphere/technology/network/metrics/vm-network-metrics
  - vsphere/tools/vsphere-client/vcenter-statistics
knowledge_main: vsphere/technology/network/metrics/virtual-motherboard/packets
attachments:
  - 0415/lb-web-01-network-real-time.csv
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C20"
misconception: [E, K]
misconception_type: [unit-and-normalization, consumption-as-contention]
pair: "0211"
status: draft
```
