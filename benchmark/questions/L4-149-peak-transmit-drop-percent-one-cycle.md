# Peak transmit drop percentage in one cycle

## Prompt
- A VM alert on dropped transmit packets fired once yesterday in VCF Operations.
- The application owner asks how much of the VM's traffic was lost, and whether the network team must replace the uplink switch.
- See [the VM's peak transmit drop chart](0421/vcf-operations-vm-peak-tx-dropped-24h.png) and [the VM's transmitted and dropped packets around that point](0421/vcf-operations-vm-tx-packets-and-drops.png).

Which statements are correct?

- A. The peak value comes from the single 20-second sample with the most drops in that cycle.
- B. The peak value is the share of the VM's transmitted packets lost over the whole 5 minutes.
- C. Over that 5-minute cycle, about 0.2% of the transmitted packets were dropped.
- D. The peak metric stores all 15 samples, so its chart can place the burst inside the cycle.
- E. The peak is a calculation artifact with no real loss behind it.
- F. About 3% of the VM's packets were lost all day: ask the network team to replace the uplink switch.
- G. The peak and the 5-minute values are VCF Operations metrics, computed from the 20-second vCenter samples.
- H. A large gap between the peak and the 5-minute value points to a short burst, not sustained loss.
- I. The second screen shows transmit drops in several 5-minute cycles of the day.

## Input to supply
- Product and version: VCF Operations 9.1, vSphere 9.1.
- Object: one VM with steady outbound traffic in about 33 equal streams: 33 iperf3 UDP clients in the VM, each to its own destination port, at the same bitrate (for example 6 Mb/s each), for an hour.
- How to produce it: add an NSX Distributed Firewall rule that drops the VM's outbound traffic to one of the 33 destination ports, keep it on for about 20 seconds, aligned with one 20-second sample as closely as possible, then remove it (about 3% of the packets in that sample; Distributed Firewall drops count as transmitted packets dropped, Broadcom KB 393915). No other drops in the day. Repeat on another day if the condition does not hold.
- Screen 1, VCF Operations > the VM > Metrics > Network: Network|Peak Transmitted Packet Dropped within collection cycle (%), last 24 hours, with the one point visible and its value in the tooltip. Save as `0421/vcf-operations-vm-peak-tx-dropped-24h.png`.
- Screen 2, the same VM, last 24 hours: Network|Total Transmitted Packets Dropped and the Total metric of packets transmitted (Network|Total Packets Transmitted), with the values of the alert point in the tooltip or a list. Use the Total variant of both metrics: the variant without Total is averaged over the 15 samples and reads 15 times lower. Save as `0421/vcf-operations-vm-tx-packets-and-drops.png`.
- Condition the key depends on: the peak at the alert point between 2.5% and 3.5%; the 5-minute dropped packets divided by transmitted packets of the same cycle between 0.15% and 0.25%; no other point of the day above 0.1% on either screen.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
B: about 3% of the traffic was lost over the 5 minutes. Or E: the 5-minute value is the only real one.

## Expected key points
- Answer: A, C, G, H.
- A true: a Peak ... within collection cycle metric is the highest of the 15 values of 20 seconds in the 5-minute cycle: the drop rate of the worst 20-second period.
- B false: the misconception. The 5-minute share is the second screen's ratio, about 0.2%.
- C true: the screen reading. Dropped divided by transmitted for the cycle is 0.15-0.25%; with all drops in one sample of 15, the peak is about 15 times that.
- D false: the metric stores only the peak of the 15 points, so it shows no pattern within the 300 seconds.
- E false: the over-correction. The peak is a real 20-second drop rate; the 5-minute average hides the burst.
- F false: the wrong action, on a misread value. The loss was one short burst in one cycle, not 3% all day.
- G true: both are VCF Operations metrics built from the 20-second samples; they are not vSphere counters.
- H true: comparing the peak with the 5-minute value tells a one-off burst from sustained loss.
- I false: the screen reading. No other point of the day is above 0.1%.

## Notes
- Paired with the theory question 0313 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item C33 (origin: synthetic). Counts only after author approval.
- Review 2026-11-15: A, D, E reworded away from 0313; I (a false screen reading) added; capture by 33 equal streams and a 20-second Distributed Firewall drop on one; the Total metrics named. Key unchanged: A, C, G, H.
- Metric names: Network|Total Transmitted Packets Dropped (Broadcom KB 393915, https://knowledge.broadcom.com/external/article/393915); Peak Transmitted Packet Dropped within collection cycle (%) = maximum dropped over average transmitted (Broadcom KB 444403).

## Metadata
```yaml
id: "0421"
title: "Peak transmit drop percentage in one cycle"
product: [vsphere, vcf-operations, nsx]
technology: [network]
task: read-metric
level: 400
answer_type: deterministic
input: [screenshot]
object: [vm]
tool: [vcf-operations]
knowledge:
  - vcf-operations/features/peak-20-second-metrics
  - vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
  - sp5-framework/observability/collection-interval
knowledge_main: vcf-operations/features/peak-20-second-metrics
attachments:
  - 0421/vcf-operations-vm-peak-tx-dropped-24h.png
  - 0421/vcf-operations-vm-tx-packets-and-drops.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C33"
answer: [A, C, G, H]
misconception: [B, F]
misconception_type: [rollup-and-interval]
pair: "0313"
status: awaiting-input
```
