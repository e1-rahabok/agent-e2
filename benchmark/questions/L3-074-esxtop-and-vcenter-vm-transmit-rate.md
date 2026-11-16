# esxtop and vCenter show a different VM transmit rate

## Prompt
- An iperf3 test sends a steady stream from the Linux VM rpt-lnx-14 to a server on another host.
- I exported the VM's Real-time network chart from the vSphere Client, the chart titled Network Rate (Mbps): [the attached vCenter export](0412/rpt-lnx-14-network-realtime.csv).
- In the same minute, esxtop on the VM's host, network panel:

```text
2:14:40pm up 63 days 04:21, 1196 worlds, 11 VMs, 38 vCPUs; CPU load average: 0.41, 0.39, 0.37
   PORT-ID USED-BY                         TEAM-PNIC DNAME              PKTTX/s  MbTX/s   PSZTX    PKTRX/s  MbRX/s   PSZRX %DRPTX %DRPRX 
 100663303 Management                            n/a vSwitch0              0.00    0.00    0.00       0.00    0.00    0.00   0.00   0.00 
 100663308 vmk0                               vmnic0 vSwitch0             20.66    0.06  339.31      14.05    0.06  554.06   0.00   0.00 
 100663309 vmk1                               vmnic0 vSwitch0              1.01    0.00  263.80       0.75    0.00  471.09   0.00   0.00 
 100663330 2104500:app-web-22                 vmnic1 vSwitch1            149.70    1.00  832.28      93.46    0.34  453.73   0.00   0.00 
 100663331 2104537:mon-col-01                 vmnic1 vSwitch1           4567.28   17.30  473.38    4398.54   14.71  417.90   0.00   0.00 
 100663332 2104574:app-web-21                 vmnic0 vSwitch1           2769.59   15.86  715.68    2417.15    4.91  253.74   0.00   0.00 
 100663333 2104611:ci-agent-03                vmnic1 vSwitch1             18.09    0.13  908.41      12.83    0.01   85.99   0.00   0.00 
 100663320 2104417:rpt-lnx-14                 vmnic1 vSwitch1           243152.93 2945.07 1514.00  116713.41   61.62   66.00   0.00   0.00 
2248146951 vmnic0                                  - vSwitch0           2791.25   15.92  712.74    2431.94    4.97  255.54   0.00   0.00 
2248146952 vmnic1                                  - vSwitch1           247888.01 2963.49 1494.37  121218.24   76.68   79.07   0.00   0.00 
```

- The application owner says the two tools disagree and asks which one is wrong.

Which statements are correct?

- A. esxtop shows the rate in megabits per second.
- B. One of the two tools is wrong, since both show the same traffic in the same minute.
- C. The vSphere Client value times 8, divided by about 1,000, gives about the esxtop value.
- D. The vCenter export's Data transmit rate is already in megabits per second, as the chart title says.
- E. The vSphere Client value is in kilobits per second, so dividing it by 1,000 gives the esxtop value.
- F. The only difference is bits against bytes: esxtop shows 8 times the vSphere Client value.
- G. The gap comes from the sampling interval: esxtop averages a few seconds, vCenter Real-time 20 seconds.
- H. The VM transmits about 3 Gb/s.
- I. Open a support case for the vCenter network counter.
- J. esxtop and the vSphere Client cannot be compared for the same VM.
- K. The number in the vCenter export is about 125 times smaller than the number in esxtop.

## Likely wrong answer
B: the numbers are about 125 times apart, so one tool must be wrong. Or F: only bits against bytes, a factor of 8. The overshoot is J: the tools cannot be compared.

## Expected key points
- Answer: A, C, H.
- A true: esxtop network throughput is megabits per second: the MbTX/s column of the VM's port row reads 2,800-3,200.
- B false: the misconception. Both are right: vCenter VM network throughput (Data transmit rate) is kilobytes per second, as the API stores it; after conversion the two agree within 10%.
- C true: `Data transmit rate for rpt-lnx-14` in the last rows is 340,000-390,000; KBps x 8 is kilobits per second, divided by about 1,000 it is megabits per second: about 2,900-3,000, within 10% of MbTX/s.
- D false: the VM's Data transmit rate is kilobytes per second, even where the network chart carries Mbps in its title; nothing is converted. Read as Mbps, 365,000 would be 365 Gb/s on one vNIC.
- E false: the unit is kilobytes; skipping the factor 8 gives a value 8 times too low (about 365 against about 2,990).
- F false: bits against bytes is a factor of 8; kilo against mega adds a factor of about 1,000, about 125 in all (365,000 against about 2,990).
- G false: the stream is steady (the export's Data transmit rate stays within 5% for the last 10 minutes); the interval cannot explain a factor of about 125.
- H true: esxtop MbTX/s is about 3,000; the vCenter value converts to the same.
- I false: the wrong action. Both counters are correct.
- J false: the over-correction. A steady stream gives the same rate in both tools once kilobytes per second are turned into megabits per second.
- K false: the reading. The vCenter number (340,000-390,000) is about 125 times larger than the esxtop number (2,800-3,200), because kilobytes are a smaller unit than megabits.

## Notes
- Paired with the theory question 0029 (theory and practical; design.md, section 3.9).
- Units checked against the vendor before writing (project/question-pairing-2026-11-14.md, section 5): net.transmitted is kiloBytesPerSecond in the vSphere Web Services API 9.1 reference (https://developer.broadcom.com/xapis/vsphere-web-services-api/9.1/network_counters.html); the vSphere 9.1 documentation lists the VM Data Transmit Rate as kilobytes per second under the chart title Network Rate (Mbps); Broadcom KB 447068 says the performance charts and their CSV export show network metrics in KBps. vcenter-statistics and network-units-vs-vsphere-client were corrected to this.
- Whether esxtop counts a megabit as 10^6 or 2^20 bits changes the conversion by about 5%; the options use "about" so the key holds either way.
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item C13 (origin: synthetic). Counts only after author approval.
- Converted to exports 2026-11-15 (project/practical-questions-as-exports-2026-11-15.md): vCenter Real-time CSV and the esxtop network panel as text, generated by project/tools/exportgen. The CSV has no units (export-templates/vcenter-chart-export/README.md), so the owner quotes the chart title in the prompt. D, G and K reworded from screen to export. Key unchanged: A, C, H.
- Review 2026-11-15: A one fact (it was the negation of B); D reworded away from 0029; J (over-correction) and K (a false screen reading) added; the condition ties the two values together. Key unchanged: A, C, H.

## Metadata
```yaml
id: "0412"
title: "esxtop and vCenter show a different VM transmit rate"
product: [vsphere, linux]
technology: [network]
task: read-metric
level: 300
answer_type: deterministic
input: [table]
object: [vm]
tool: [vcenter, esxtop]
knowledge:
  - vsphere/tools/esxtop/network-units-vs-vsphere-client
  - vsphere/tools/vsphere-client/vcenter-statistics
  - vsphere/tools/esxtop/network
  - vsphere/technology/network/metrics/virtual-motherboard/throughput
knowledge_main: vsphere/tools/esxtop/network-units-vs-vsphere-client
attachments:
  - 0412/rpt-lnx-14-network-realtime.csv
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C13"
answer: [A, C, H]
misconception: [B]
misconception_type: [tool-confusion, unit-and-normalization]
pair: "0029"
status: draft
```
