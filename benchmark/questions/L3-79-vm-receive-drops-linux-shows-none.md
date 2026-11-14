# VM receive drops that Linux does not count

## Prompt
- The application team of a Linux VM says the network is fine, because Linux counts no dropped packets. The monitoring team says vCenter disagrees.
- See [the vSphere Client network chart of the VM](0420/vcenter-vm-network-drops-real-time.png) and [the Linux interface counters](0420/linux-ip-link-and-ethtool.png), same hour.

Which statements are correct?

- A. The VMXNET3 receive ring was full, and the guest has no counter for that.
- B. ESXi dropped received frames before it delivered them to the guest, so Linux never saw them.
- C. rx_dropped in `ip -s link` includes the ring-full drops of the VMXNET3 adapter.
- D. A full receive ring would show in `ethtool -S` as pkts rx OOB above 0.
- E. One of the two tools is wrong, since the VM and the guest count the same packets.
- F. Raise the receive ring size in Linux to stop these drops.
- G. The physical network dropped these packets before they reached the host.
- H. Receive packets dropped in the Real-time chart is a count per 20-second sample.

## Input to supply
- Product and version: a Linux VM (kernel 5.0 or later) with one VMXNET3 adapter on vSphere 9.1 (vSphere Client 9.1).
- How to produce it: take it from the field, or in a lab let ESXi drop frames before delivery to the VM (for example a distributed switch traffic filtering rule with action Drop on part of the traffic to the VM's port); first check in the chart that the drops show on the VM. A full guest receive ring does not qualify: it shows in the guest.
- Screen 1, vSphere Client > the VM > Monitor > Performance > Advanced > Network, Chart Options: Real-time, the last hour, object the VM, counters Receive packets dropped and Packets received, with the legend table. Save as `0420/vcenter-vm-network-drops-real-time.png`.
- Screen 2, a terminal in the VM in the same hour: `ip -s link show <interface>` and `ethtool -S <interface> | grep -i -E "oob|drop"`, showing rx dropped and pkts rx OOB of every receive queue. Save as `0420/linux-ip-link-and-ethtool.png`.
- Condition the key depends on: Receive packets dropped above 0 in several samples of the hour; `ip -s link` RX dropped 0; pkts rx OOB 0 on every receive queue.
- Masking: mask every VM, host, datastore and cluster name, and the host name in the shell prompt.

## Likely wrong answer
A: a full ring is invisible to the guest. Or E: one of the tools miscounts.

## Expected key points
- Answer: B, D, H.
- A false: the misconception. VMXNET3 shares a ring-full drop with the guest driver, which shows it as pkts rx OOB; it is 0 on every queue here.
- B true: ESXi drops received frames before delivery, for example frames not for the guest or against the port's security settings; the guest never receives them, so it cannot count them. With the ring not full (pkts rx OOB 0), this is what is left.
- C false: rx_dropped counts only frames the driver itself dropped; the ring-full count is pkts rx OOB.
- D true: the vmxnet3 driver shows the ring-full count per receive queue as pkts rx OOB (device counter pktsRxOutOfBuf).
- E false: each layer counts what it sees; a drop before delivery exists only in the hypervisor's counters.
- F false: the wrong action. The ring was not full; a larger ring does not change a drop that happens before delivery.
- G false: a frame dropped in the physical network never reaches the host, so the VM counters cannot count it.
- H true: packet and drop counters are totals per sample interval (summation), not rates per second.

## Notes
- Paired with the theory question 0039 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item C26 (origin: synthetic). Counts only after author approval.

## Metadata
```yaml
id: "0420"
title: "VM receive drops that Linux does not count"
product: [vsphere, linux]
technology: [network]
task: troubleshoot
level: 300
answer_type: deterministic
input: [screenshot]
object: [vm, guest-os]
tool: [vcenter, guest-os-tools]
knowledge:
  - vsphere/technology/network/concepts/packet-drop-accounting
  - vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
  - vsphere/tools/vsphere-client/vcenter-statistics
knowledge_main: vsphere/technology/network/concepts/packet-drop-accounting
attachments:
  - 0420/vcenter-vm-network-drops-real-time.png
  - 0420/linux-ip-link-and-ethtool.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C26"
answer: [B, D, H]
misconception: [A, E]
misconception_type: [layer-confusion]
pair: "0039"
status: awaiting-input
```
