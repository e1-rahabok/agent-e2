# Network receive errors: find the host and the cause

## Prompt
- Cluster c1 has 16 ESXi 9.1 hosts. Each host has four 25 GbE ports on two dual-port cards (slot1 and slot2), all on one distributed switch.
- [The attached export](0088/cluster-c1-vmnic-counters-one-day.csv) lists every vmnic for one day: link speed, duplex, driver, firmware, and the day's totals of packets, errors and drops from vCenter.
- A cluster dashboard averages receive errors over all 64 vmnics and shows a value close to 0. The network team says the cluster's network is clean.
- Users of a few VMs report short stalls during the day.

Is the network clean? If not, which host and port, what is the likely cause, and what do you do next?

## Likely wrong answer
"The cluster average is near 0, so the network is clean." Or "one host has older firmware, so that host is the cause."

## Expected key points
- No. One port is not clean: esx-c1-11 vmnic2 has about 48,000 receive errors in the day. Every other vmnic has 0 errors and 0 drops.
- An average over 64 vmnics hides one bad port. On a data center network, errors and drops on a vmnic should be 0: read the worst port, not the average.
- vmnic3 on the same card (slot2), with the same driver and firmware, is clean. That points to the physical link of that one port: cable, transceiver or the switch port, not the driver.
- esx-c1-04 runs older NIC firmware (NVM 4.20 against 4.40) on all its ports but shows no errors: a consistency item to fix, not the cause.
- Next: read the port's detail with `esxcli network nic stats get -n vmnic2` (CRC and receive errors; the counters are cumulative since boot, so read them twice to see the rate), compare with the switch port's error counters, move traffic off the port (standby) while the cable or transceiver is replaced, and check which VMs use that uplink.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
- Revised 2026-11-12: the management pack metric and the screenshot removed (fairness); the 256-row workbook became a 64-row CSV. The CSV is synthetic, generated with a fixed seed: one port with errors, one host with older firmware and no errors.

## Metadata
```yaml
id: "0088"
title: "Network receive errors: find the host and the cause"
product: [vsphere]
technology: [network]
object: [esxi, network]
tool: [vcenter]
task: troubleshoot
level: 400
answer_type: judged
input: [table]
knowledge:
  - vsphere/technology/network/metrics/host/errors
  - vsphere/technology/network/metrics/host/packets-dropped
  - vsphere/object-types/esxi/configuration/esxi-configuration-review
knowledge_main: vsphere/technology/network/metrics/host/errors
attachments:
  - 0088/cluster-c1-vmnic-counters-one-day.csv
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
misconception_type: [average-hides-worst]
status: draft
```
