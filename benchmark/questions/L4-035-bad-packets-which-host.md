# Network receive errors: find the host and the cause

## Prompt
- Cluster c1 has 16 ESXi 9.1 hosts. Each host has four 25 GbE ports on two dual-port cards (slot1 and slot2), all on one distributed switch.
- [The attached export](0088/cluster-c1-vmnic-counters-one-day.csv) lists every vmnic for one day: link speed, duplex, driver, firmware, and the day's totals of packets, errors and drops from vCenter.
- A cluster dashboard divides the receive errors of all 64 vmnics by their received packets and shows 0.0002% for the day. The network team says the cluster's network is clean.
- Users of a few VMs report short stalls during the day.

Is the network clean, and if not, which host and port, what is the likely cause, and what do you do next? Which statements are correct?

- A. The network is not clean: one port, vmnic2 on esx-c1-11, logged about 48,000 receive errors in the day.
- B. A cluster-wide receive error share of 0.0002% shows that the cluster network is clean.
- C. The dashboard's 0.0002% comes from one port, whose errors are spread over the packets of all 64 vmnics.
- D. The host with older firmware, esx-c1-04, is where the receive errors of the cluster come from.
- E. esxcli on esx-c1-11 splits vmnic2's receive errors by type (CRC, FIFO, missed and more); vCenter does not.
- F. Receive errors on a vmnic are ring-buffer overflows, so a larger receive ring on vmnic2 will stop them.
- G. vmnic2's link was negotiated down below 25 Gb/s, which is why only this port logs errors.
- H. An error rate under 0.01% of packets is acceptable background on a busy 25 GbE port.
- I. The errors come with receive drops on the same port, a sign that the NIC receive ring is full.
- J. The esxcli NIC counters are cumulative: read them twice to see if the errors still grow.
- K. Record vmnic2's counters before any reboot of the host: a reboot resets them to 0.
- L. The older firmware on esx-c1-04 is a consistency item to fix, even though that host shows no errors.

## Answers
A, C, E, J, K, L

## Explanation
- A true: esx-c1-11 vmnic2 has 48,120 receive errors; every other vmnic has 0 errors and 0 drops.
- B false: on a data center network errors and drops on a vmnic are expected to be 0 at all times; a share over 64 ports turns one bad port into a value near 0.
- C true: 48,120 errors in about 29.2 billion received packets is about 0.0002%, all from vmnic2 on esx-c1-11. An aggregate across members hides the outlier until the problem is widespread; read the worst member.
- D false: the host with older firmware, esx-c1-04, has 0 errors and 0 drops on all four ports.
- E true: vCenter keeps the total of receive errors per vmnic; `esxcli network nic stats get -n vmnic2` lists the kinds apart, and the kind points to the cause: FIFO and missed errors a NIC that cannot keep up at its ring size, CRC errors a damaged frame (typically a bad cable), length errors a wrong size.
- F false: the receive error total sums several kinds (CRC, length, frame, FIFO, missed); a larger ring addresses FIFO and missed errors only, not CRC errors (Broadcom KB 341594). The breakdown of vmnic2 is not known yet, and its receive drops are 0.
- G false: the export shows 25,000 Mb/s and Full duplex on vmnic2, as on every other vmnic: auto-negotiation did not lower its link.
- H false: vmnic2's 48,120 errors in about 518 million packets are under 0.01%, but the expected value is 0, not a small rate; any error count on one port is a fault to find.
- I false: receive and transmit drops are 0 on every vmnic.
- J true: esxcli counters are cumulative, so one reading cannot tell a past burst from a current fault.
- K true: the counters are cumulative and a reboot resets them; record them first, then watch whether they still grow (Broadcom KB 341594).
- L true: drivers and firmware should be identical across the hosts of a cluster; esx-c1-04 is a consistency fix, not the cause.
- Misconception: B: "The cluster value is near 0, so the network is clean." - D: "One host has older firmware, so that host is the cause." - H: "Under 0.01% of the packets is noise."

## Notes
- Revised 2026-11-12: the management pack metric and the screenshot removed (fairness); the 256-row workbook became a 64-row CSV. The CSV is synthetic, generated with a fixed seed: one port with errors, one host with older firmware and no errors.
- The old key point on moving traffic off the port (standby uplink) and checking which VMs use it is left out: no knowledge file settles it.
- Options E, F, G rewritten 2026-11-14 (project/question-pairing-2026-11-14.md, item B11): the old E (fault isolated by the neighbouring port), F (driver) and G (half duplex) rested on inferences host/errors does not state; the new options rest on its esxcli table and on the export's speed and duplex columns. D kept: the export shows 0 errors on esx-c1-04. Key unchanged: A, C, E, J, K, L.
- Paired with 0409 (theory; design.md, section 3.9).
- Review 2026-11-15: D and H one fact each; K (the switch port with the network team) is not in the vendor document and is replaced by the KB 341594 step of recording the counters before a reboot. Key unchanged: A, C, E, J, K, L.
- 2026-11-16 re-review: the dashboard value is now the cluster-wide share the export gives (48,120 / 29,150,312,761 = 0.00017%, shown as 0.0002%), not "close to 0" (the mean per vmnic is 752 errors); C reworded from the averaging rule (the negation of B) to where the 0.0002% comes from. Truth values unchanged.
- Audit 2026-11-15: E shortened and D lengthened (E was 1.63x the wrong mean); truth unchanged.

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
source_path: "Synthetic, 2026-11-05"
misconception_type: [average-hides-worst]
pair: "0409"
status: draft
```
