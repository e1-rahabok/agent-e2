# esxtop and vCenter show a different VM transmit rate

## Prompt
- An iperf3 test sends a steady stream from a Linux VM to a server on another host.
- See [the esxtop network panel](0412/esxtop-network-panel.png) and [the vSphere Client network chart of the VM](0412/vcenter-vm-network-real-time.png), captured in the same minute.
- The application owner says the two tools disagree and asks which one is wrong.

Which statements are correct?

- A. Both tools are right: esxtop shows megabits per second; the vSphere Client chart shows kilobytes per second.
- B. One of the two tools is wrong, since both show the same traffic in the same minute.
- C. The vSphere Client value times 8, divided by about 1,000, gives about the esxtop value.
- D. The vSphere Client value is in megabits per second, the same unit as esxtop.
- E. The vSphere Client value is in kilobits per second, so dividing it by 1,000 gives the esxtop value.
- F. The only difference is bits against bytes: esxtop shows 8 times the vSphere Client value.
- G. The gap comes from the sampling interval: esxtop averages a few seconds, the chart 20 seconds.
- H. The VM transmits about 3 Gb/s.
- I. Open a support case for the vCenter network counter.

## Input to supply
- Product and version: vSphere 9.1 (ESXi 9.1, vSphere Client 9.1).
- Object: one Linux VM with one VMXNET3 adapter; an iperf3 server on a VM or machine outside the VM's host.
- How to produce it: in the VM, `iperf3 -c <server> -b 3G -t 900` (a steady 3 Gb/s for 15 minutes). Wait 2 minutes before capturing.
- Screen 1, esxtop on the VM's host, `n` (network panel), default 5-second refresh: the header and the row of the VM's port (USED-BY shows the VM), with PORT-ID, USED-BY, TEAM-PNIC, PKTTX/s, MbTX/s, PKTRX/s, MbRX/s visible. Save as `0412/esxtop-network-panel.png`.
- Screen 2, vSphere Client > the VM > Monitor > Performance > Advanced > Network, Chart Options: Real-time, object the VM, counters Data transmit rate and Data receive rate, with the legend table (Units column, Latest, Maximum). Keep the chart title in the capture. Save as `0412/vcenter-vm-network-real-time.png`.
- Capture both within the same minute.
- Condition the key depends on: esxtop MbTX/s of the VM's port between 2,800 and 3,200; the vSphere Client Data transmit rate between 340,000 and 390,000 KBps (Latest), with the line flat within about 5% over the last 10 minutes.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
B: the numbers are about 125 times apart, so one tool must be wrong. Or F: only bits against bytes, a factor of 8.

## Expected key points
- Answer: A, C, H.
- A true: esxtop network throughput is megabits per second (MbTX/s); vCenter VM network throughput (Data transmit rate) is kilobytes per second, as the API stores it.
- B false: the units differ; after conversion the two agree.
- C true: KBps x 8 is kilobits per second; divided by about 1,000 it is megabits per second. About 365,000 KBps x 8 / 1,000 is about 2,900-3,000 Mbps.
- D false: the VM's Data transmit rate is kilobytes per second (the legend's Units column), even where a network chart carries Mbps in its title.
- E false: the unit is kilobytes; skipping the factor 8 gives a value 8 times too low.
- F false: bits against bytes is a factor of 8; kilo against mega adds a factor of about 1,000, about 125 in all.
- G false: a steady stream gives the same rate over 5 or 20 seconds; the interval cannot explain a factor of about 125.
- H true: esxtop shows about 3,000 Mbps; the vSphere Client value converts to the same.
- I false: both counters are correct.

## Notes
- Paired with the theory question 0029 (theory and practical; design.md, section 3.9).
- Units checked against the vendor before writing (project/question-pairing-2026-11-14.md, section 5): net.transmitted is kiloBytesPerSecond in the vSphere Web Services API 9.1 reference (https://developer.broadcom.com/xapis/vsphere-web-services-api/9.1/network_counters.html); the vSphere 9.1 documentation lists the VM Data Transmit Rate as kilobytes per second under the chart title Network Rate (Mbps); Broadcom KB 447068 says the performance charts and their CSV export show network metrics in KBps. vcenter-statistics and units-vs-vsphere-client were corrected to this.
- Whether esxtop counts a megabit as 10^6 or 2^20 bits changes the conversion by about 5%; the options use "about" so the key holds either way.
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item C13 (origin: synthetic). Counts only after author approval.

## Metadata
```yaml
id: "0412"
title: "esxtop and vCenter show a different VM transmit rate"
product: [vsphere, linux]
technology: [network]
task: read-metric
level: 300
answer_type: deterministic
input: [screenshot]
object: [vm]
tool: [vcenter, esxtop]
knowledge:
  - vsphere/tools/esxtop/units-vs-vsphere-client
  - vsphere/tools/vsphere-client/vcenter-statistics
  - vsphere/tools/esxtop/network
  - vsphere/technology/network/metrics/virtual-motherboard/throughput
knowledge_main: vsphere/tools/esxtop/units-vs-vsphere-client
attachments:
  - 0412/esxtop-network-panel.png
  - 0412/vcenter-vm-network-real-time.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C13"
answer: [A, C, H]
misconception: [B]
misconception_type: [tool-confusion, unit-and-normalization]
pair: "0029"
status: awaiting-input
```
