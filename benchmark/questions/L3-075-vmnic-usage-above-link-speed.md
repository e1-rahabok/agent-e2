# vmnic Usage above the link speed

## Prompt
- The network team's alert on vmnic Usage fired on the ESXi host esx-17, for vmnic2.
- They say the port is oversubscribed and ask for a second port.
- [The attached vCenter export](0413/esx-17-network-real-time.csv) is the host's Real-time network view, 15 minutes around the alert.
- The chart legend (not in the export) gives the unit of the rate and Usage columns: KBps.
- Output of `esxcli network nic list` on esx-17:

```text
Name    PCI Device    Driver  Admin Status  Link Status  Speed  Duplex  MAC Address         MTU  Description
------  ------------  ------  ------------  -----------  -----  ------  -----------------  ----  -----------------------------------------------
vmnic0  0000:18:00.0  i40en   Up            Up           10000  Full    3c:fd:fe:a4:17:40  1500  Intel(R) Ethernet Controller X710 for 10GbE SFP+
vmnic1  0000:18:00.1  i40en   Up            Up           10000  Full    3c:fd:fe:a4:17:41  1500  Intel(R) Ethernet Controller X710 for 10GbE SFP+
vmnic2  0000:3b:00.0  i40en   Up            Up           10000  Full    3c:fd:fe:a4:2b:80  1500  Intel(R) Ethernet Controller X710 for 10GbE SFP+
vmnic3  0000:3b:00.1  i40en   Up            Up           10000  Full    3c:fd:fe:a4:2b:81  1500  Intel(R) Ethernet Controller X710 for 10GbE SFP+
```

Which statements are correct?

- A. Usage on a full-duplex port can read up to twice the link speed.
- B. A port cannot carry more than its link speed, so a Usage above it shows a counter error.
- C. In every row, the Data receive rate and Data transmit rate of vmnic2 add up to its Usage.
- D. vmnic2 receives at about 90% of its link speed, close to the limit of that direction.
- E. Half of Usage, set against the link speed, is the right measure of how close this port is to its limit.
- F. Usage above the link speed is itself the reason to add a port.
- G. In every row, the Data receive rate of vmnic2 alone stays below its link speed.
- H. Usage is the higher of the receive and transmit rates.
- I. In the export, vmnic2 transmits closer to its link speed than it receives.

## Likely wrong answer
B: a port cannot carry more than its link speed, so the counter is wrong. Or F: add a port because Usage passed the link speed.

## Expected key points
- Answer: A, C, D, G.
- A true: Usage rate = receive + transmit, and full duplex is 100% in each direction, so Usage can reach twice the link speed with no fault.
- B false: the misconception. Usage counts both directions of a full-duplex port (esxcli: Speed 10000, Duplex Full); the counter is right.
- C true: Usage for vmnic2 equals Data receive rate for vmnic2 plus Data transmit rate for vmnic2 in every row (the same holds for every vmnic and for the host).
- D true: the values are KBps (1 KB = 1,024 bytes), so 10 Gb/s is about 1,220,700 KBps. Data receive rate for vmnic2 stays between 1,040,000 and 1,159,000 KBps in every row: 85-95% of the link speed, near the limit of that direction, whatever transmit does.
- E false: the over-correction. Half of Usage is 62-73% of the link speed here and hides that receive is near its own limit; each direction is judged against the link speed.
- F false: the wrong action, for the wrong reason. Usage above the link speed is expected; the risk, if any, is the receive direction alone.
- G true: the highest Data receive rate for vmnic2 is below 1,160,000 KBps, under the 1,220,700 KBps of 10 Gb/s; Usage passes the link speed only because transmit is added.
- H false: Usage is the sum of receive and transmit, not the higher of the two; in every row it is above both.
- I false: Data transmit rate for vmnic2 stays between 366,000 and 732,000 KBps (30-60% of the link speed), below the receive rate in every row.

## Notes
- Paired with the theory question 0040 (theory and practical; design.md, section 3.9).
- Units per vcenter-statistics, section Units (vSphere 9.1 documentation and API: network rates in kilobytes per second).
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item C18 (origin: synthetic). Counts only after author approval.
- Review 2026-11-15: A, C and E reworded away from 0040 (C is now a screen reading); F one fact; I (a false screen reading) added; knowledge_main is host/throughput. Key unchanged: A, C, D, G.
- Converted 2026-11-15 from screenshots to a vCenter Real-time CSV and `esxcli network nic list` text (project/practical-questions-as-exports-2026-11-15.md). C, D and I reworded from chart to export. G replaced: the old G (the values are KBps, 1,100,000 KBps is about 9 Gb/s) made a third question on the KBps unit with 0412 and the old 0415 H; the new G is a reading of the export, still true. The unit is not in the export header (export-templates/HEADERS.md), so D still needs it.

## Metadata
```yaml
id: "0413"
title: "vmnic Usage above the link speed"
product: [vsphere]
technology: [network]
task: read-metric
level: 300
answer_type: deterministic
input: [table]
object: [esxi, network]
tool: [vcenter]
knowledge:
  - vsphere/technology/network/concepts/network-characteristics
  - vsphere/technology/network/metrics/host/throughput
  - vsphere/tools/vsphere-client/vcenter-statistics
knowledge_main: vsphere/technology/network/metrics/host/throughput
attachments:
  - 0413/esx-17-network-real-time.csv
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C18"
answer: [A, C, D, G]
misconception: [B, F]
misconception_type: [unit-and-normalization]
pair: "0040"
status: draft
```
