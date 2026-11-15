# ESXi vmnic error counters

## Prompt
- An ESXi host has four 25 GbE vmnics on a data center network.
- vCenter keeps Packet receive errors and Packet transmit errors for each vmnic. On the host, `esxcli network nic stats get -n vmnic#` shows the port's counters.

Which statements about these counters are correct?

- A. A few errors per million packets are normal background on a 25 GbE port.
- B. A non-zero error count always points to a fault in the ESXi NIC driver.
- C. An average of receive errors over many vmnics can read near 0 while one port logs thousands of errors.
- D. The esxcli counters are cumulative, so a non-zero value can come from a past event.
- E. Receive FIFO errors count frames the NIC could not take because its ring buffer was full.
- F. Replace the NIC as soon as esxcli shows a non-zero receive error count.
- G. The host counts TCP retransmits of its own VMkernel traffic, such as vSAN and vMotion.
- H. The host counts TCP retransmits of the VMs' traffic as well.

## Likely wrong answer
A: a small error rate is normal background. The overshoot is B: every error is a driver fault.

## Expected key points
- Answer: C, D, E, G.
- A false: the misconception. Error, unknown and dropped packets are expected to be 0 at all times; any count is a fault to find.
- B false: the over-correction. Errors have several causes: damaged frames from cabling or optics (CRC and checksum errors), wrong sizes (length errors), a full NIC buffer (FIFO, over errors), hardware limits (missed errors).
- C true: an average across members hides the outlier until the problem is widespread; read the worst vmnic.
- D true: esxcli counters are cumulative: read them twice to see whether they still grow.
- E true: Receive FIFO errors and Transmit FIFO errors mean the NIC cannot process: ring buffer full.
- F false: the wrong action. The count is cumulative and may be old, and the error type points to the cause, which can be the cable, the optic or the switch port rather than the NIC.
- G true: the VMkernel TCP/IP stack carries the host's own traffic (vSAN, vMotion, NFS, iSCSI) and counts its retransmits (vSAN Performance for Support, `net-stats`); they point to loss in the physical network.
- H false: VM traffic is TCP inside the Guest OS; the host does not see its retransmits.

## Notes
- Theory half of the pair with 0088 (practical; design.md, section 3.9). One host, not a cluster as in 0088.
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item B11 (origin: synthetic). Counts only after author approval.
- Review 2026-11-15: framed on one host; the expected-0 option (the negation of the misconception) and the cluster-average ticket option (close to 0088 B) dropped; new wrong action F; the stem no longer says esxcli shows more detail. Key changed from A, D, E, F, H to C, D, E, G (relettered).

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
