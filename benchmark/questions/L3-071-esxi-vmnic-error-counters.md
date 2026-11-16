# ESXi vmnic error counters

## Prompt
- An ESXi host has four 25 GbE vmnics on a data center network.
- vCenter keeps Packet receive errors and Packet transmit errors for each vmnic. On the host, `esxcli network nic stats get -n vmnic#` shows the port's counters.

Which statements about these counters are correct?

- A. A few errors per million packets are normal background on a busy 25 GbE data center port.
- B. A non-zero error count always points to a fault in the ESXi NIC driver on that host.
- C. An average of receive errors over many vmnics reads near 0 while one port logs thousands.
- D. The esxcli counters are cumulative: a non-zero value is not proof of a current fault.
- E. Receive FIFO errors count frames the NIC could not take because its ring buffer was full.
- F. Replace the NIC as soon as esxcli shows a non-zero receive error count on its port.
- G. The host counts TCP retransmits of its own VMkernel traffic, such as vSAN and vMotion.
- H. vCenter keeps a TCP retransmit counter for each vmnic, next to its two error counters.

## Likely wrong answer
A: a small error rate is normal background. The overshoot is B: every error is a driver fault.

## Expected key points
- Answer: C, D, E, G.
- A false: the misconception. Error, unknown and dropped packets are expected to be 0 at all times; any count is a fault to find.
- B false: the over-correction. Errors have several causes: damaged frames, typically a bad cable (CRC and checksum errors), wrong sizes (length errors), a NIC that cannot keep up at its ring size (FIFO, missed errors), its hardware buffer (over errors).
- C true: an average across members hides the outlier until the problem is widespread; read the worst vmnic.
- D true: esxcli counters are cumulative: read them twice to see whether they still grow.
- E true: Receive FIFO errors and Transmit FIFO errors mean the NIC cannot process: ring buffer full.
- F false: the wrong action. The count is cumulative and may be old, and the error type points to the cause: a CRC error is typically a bad cable, a FIFO or missed error a ring too small for the traffic.
- G true: the VMkernel TCP/IP stack carries the host's own traffic (vSAN, vMotion, NFS, iSCSI) and counts its retransmits (vSAN Performance for Support, `net-stats`); they point to loss in the physical network.
- H false: vCenter shows only a receive and a transmit error total per vmnic; the host's retransmits are read in vSAN Performance for Support or with `net-stats`, and VM traffic retransmits only inside the Guest OS.

## Notes
- Theory half of the pair with 0088 (practical; design.md, section 3.9). One host, not a cluster as in 0088.
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item B11 (origin: synthetic).
- Review 2026-11-15: framed on one host; the expected-0 option (the negation of the misconception) and the cluster-average ticket option (close to 0088 B) dropped; new wrong action F; the stem no longer says esxcli shows more detail. Key changed from A, D, E, F, H to C, D, E, G (relettered).
- Audit 2026-11-15: hedges in correct C and D made plain; H (the host does not count VM retransmits, the near-negation of G) replaced with a false option on where the host's retransmits are read.

## Metadata
```yaml
id: "0409"
title: "ESXi vmnic error counters"
product: [vsphere, vsan]
technology: [network]
task: read-metric
level: 300
answer_type: deterministic
input: [text]
object: [esxi, network]
tool: [vcenter]
knowledge:
  - vsphere/technology/network/metrics/host/errors
  - sp5-framework/observability/aggregation
knowledge_main: vsphere/technology/network/metrics/host/errors
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item B11"
answer: [C, D, E, G]
misconception: [A]
misconception_type: [average-hides-worst, cumulative-vs-current]
pair: "0088"
status: draft
```
