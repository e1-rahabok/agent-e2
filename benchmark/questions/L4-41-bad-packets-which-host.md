# Network receive errors: find the host and the cause

## Prompt
- Cluster c1 has 16 ESXi 9.1 hosts. Each host has four 25 GbE ports on two dual-port cards (slot1 and slot2), all on one distributed switch.
- [The attached export](0088/cluster-c1-vmnic-counters-one-day.csv) lists every vmnic for one day: link speed, duplex, driver, firmware, and the day's totals of packets, errors and drops from vCenter.
- A cluster dashboard averages receive errors over all 64 vmnics and shows a value close to 0. The network team says the cluster's network is clean.
- Users of a few VMs report short stalls during the day.

Is the network clean, and if not, which host and port, what is the likely cause, and what do you do next? Which statements are correct?

- A. The network is not clean: one port, vmnic2 on esx-c1-11, logged about 48,000 receive errors in the day.
- B. A cluster average of receive errors close to 0 shows that the cluster network is clean.
- C. An average over 64 vmnics hides a single bad port; read the worst vmnic of the cluster, not the mean.
- D. esx-c1-04 runs older NIC firmware, so it is the source of the errors behind the stalls.
- E. esxcli on esx-c1-11 splits vmnic2's receive errors by type (CRC, length, frame, FIFO, missed); the vCenter total in the export does not.
- F. Receive errors on a vmnic are ring-buffer overflows, so a larger receive ring on vmnic2 will stop them.
- G. vmnic2's link was negotiated down below 25 Gb/s, which is why only this port logs errors.
- H. About 48,000 errors among roughly 500 million received packets is under 0.01%, an acceptable rate for a 25 GbE port.
- I. The errors come with receive drops on the same port, a sign that the NIC receive ring is full.
- J. The `esxcli network nic stats get` counters are cumulative: read them twice to see if the errors still grow.
- K. Compare with the error counters of the switch port at the other end of the link, with the network team.
- L. The older firmware on esx-c1-04 is a consistency item to fix, even though that host shows no errors.

## Likely wrong answer
- B: "The cluster average is near 0, so the network is clean."
- D: "One host has older firmware, so that host is the cause."
- H: "A few thousand errors in half a billion packets is noise."

## Expected key points
- Answer: A, C, E, J, K, L.
- A true: esx-c1-11 vmnic2 has 48,120 receive errors; every other vmnic has 0 errors and 0 drops.
- B false: on a data center network errors and drops on a vmnic are expected to be 0 at all times; an average over 64 ports turns one bad port into a value near 0.
- C true: an average across members hides the outlier until the problem is widespread; read the worst member.
- D false: esx-c1-04 has 0 errors and 0 drops on all four ports.
- E true: vCenter keeps the total of receive errors per vmnic; `esxcli network nic stats get -n vmnic2` lists the kinds apart, and the kind points to the cause: FIFO errors are a full ring buffer, missed errors a hardware limit of the NIC, CRC and length errors a frame that arrived damaged or with a wrong size.
- F false: the receive error total sums several kinds (CRC, length, frame, FIFO, missed); only FIFO errors are a full ring. The breakdown of vmnic2 is not known yet, and its receive drops are 0.
- G false: the export shows 25,000 Mb/s and Full duplex on vmnic2, as on every other vmnic: auto-negotiation did not lower its link.
- H false: the expected value is 0, not a small rate; any error count on one port is a fault to find.
- I false: receive and transmit drops are 0 on every vmnic.
- J true: esxcli counters are cumulative, so one reading cannot tell a past burst from a current fault.
- K true: a physical-link fault shows on the switch port too; drops and errors on a data center network are a topic for the network team.
- L true: drivers and firmware should be identical across the hosts of a cluster; esx-c1-04 is a consistency fix, not the cause.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
- Revised 2026-11-12: the management pack metric and the screenshot removed (fairness); the 256-row workbook became a 64-row CSV. The CSV is synthetic, generated with a fixed seed: one port with errors, one host with older firmware and no errors.
- Converted from judged to multiple choice (Q199 F, 2026-11-14). The old key point on moving traffic off the port (standby uplink) and checking which VMs use it is left out: no knowledge file settles it.
- Options E, F, G rewritten 2026-11-14 (project/question-pairing-2026-11-14.md, item B11): the old E (fault isolated by the neighbouring port), F (driver) and G (half duplex) rested on inferences host/errors does not state; the new options rest on its esxcli table and on the export's speed and duplex columns. D kept: the export shows 0 errors on esx-c1-04. Key unchanged: A, C, E, J, K, L.
- Paired with 0409 (theory; design.md, section 3.9).

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
answer_type: deterministic
answer: [A,C,E,J,K,L]
misconception: [B,D,H]
input: [table]
knowledge:
  - vsphere/technology/network/metrics/host/errors
  - vsphere/technology/network/metrics/host/packets-dropped
  - vsphere/object-types/esxi/configuration/esxi-configuration-review
  - sp5-framework/observability/aggregation
knowledge_main: vsphere/technology/network/metrics/host/errors
attachments:
  - 0088/cluster-c1-vmnic-counters-one-day.csv
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
misconception_type: [average-hides-worst]
pair: "0409"
status: draft
```
