# ESXi vmnic error counters

## Prompt
- vCenter keeps Packet receive errors and Packet transmit errors for each vmnic of an ESXi host. On the host, `esxcli network nic stats get -n vmnic#` shows the same port's counters in more detail.
- A cluster has 12 hosts with four vmnics each, all 25 GbE on a data center network.

Which statements about these counters are correct?

- A. On a healthy data center network, a vmnic's error counters are expected to stay at 0.
- B. A few errors per million packets are normal background on a 25 GbE port.
- C. A non-zero error count always points to a fault in the ESXi NIC driver.
- D. The average of receive errors over the 48 vmnics can read near 0 while one port logs thousands of errors.
- E. The esxcli counters are cumulative, so a non-zero value can come from a past event.
- F. Receive FIFO errors count frames the NIC could not take because its ring buffer was full.
- G. Close the network ticket when the average of receive errors over all vmnics of the cluster is near 0.
- H. The host counts TCP retransmits of its own VMkernel traffic, such as vSAN and vMotion.
- I. The host counts TCP retransmits of the VMs' traffic as well.

## Likely wrong answer
B: a small error rate is normal background. Or G: the cluster average is near 0, so the network is clean. The overshoot is C: every error is a driver fault.

## Expected key points
- Answer: A, D, E, F, H.
- A true: error, unknown and dropped packets are expected to be 0 at all times.
- B false: the expected value is 0, not a small rate; any count is a fault to find.
- C false: errors have several causes: damaged frames from cabling or optics (CRC and checksum errors), wrong sizes (length errors), a full NIC buffer (FIFO, over errors), hardware limits (missed errors).
- D true: an average across members hides the outlier until the problem is widespread; read the worst vmnic.
- E true: esxcli counters are cumulative: read them twice to see whether they still grow.
- F true: Receive FIFO errors and Transmit FIFO errors mean the NIC cannot process: ring buffer full.
- G false: one bad port averages to a value near 0 over 48 ports.
- H true: the VMkernel TCP/IP stack carries the host's own traffic (vSAN, vMotion, NFS, iSCSI) and counts its retransmits (vSAN Performance for Support, `net-stats`); they point to loss in the physical network.
- I false: VM traffic is TCP inside the Guest OS; the host does not see its retransmits.

## Notes
- Theory half of the pair with 0088 (practical; design.md, section 3.9). Different cluster and numbers from 0088.
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item B11 (origin: synthetic). Counts only after author approval.

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
answer: [A, D, E, F, H]
misconception: [B, G]
misconception_type: [average-hides-worst, cumulative-vs-current]
pair: "0088"
status: draft
```
