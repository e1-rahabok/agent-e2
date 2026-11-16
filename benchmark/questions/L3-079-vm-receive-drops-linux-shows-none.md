# VM receive drops that Linux does not count

## Prompt
- ingest-04 is a Linux VM (Ubuntu 22.04, kernel 5.15) with 4 vCPUs and one VMXNET3 adapter, ens192.
- Its application team says the network is fine, because Linux counts no dropped packets. The monitoring team says vCenter disagrees.
- [The attached vCenter export](0420/ingest-04-network-real-time.csv) is the Real-time network view of ingest-04, last 30 minutes.
- In the same half hour, the application team ran `ip -s link show ens192` in the VM:

```text
2: ens192: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000
    link/ether xx:xx:xx:xx:xx:xx brd xx:xx:xx:xx:xx:xx
    RX:     bytes    packets errors dropped  missed   mcast           
    3340686687518 3213157552      0       0       0    7097 
    TX:     bytes    packets errors dropped carrier collsns           
       2325516622   13501251      0       0       0       0 
```

- Then `ethtool -S ens192 | grep -i -E "queue|oob|drop"`:

```text
     Tx Queue#: 0
       drv dropped tx total: 0
     Tx Queue#: 1
       drv dropped tx total: 0
     Tx Queue#: 2
       drv dropped tx total: 0
     Tx Queue#: 3
       drv dropped tx total: 0
     Rx Queue#: 0
       pkts rx OOB: 0
       drv dropped rx total: 0
     Rx Queue#: 1
       pkts rx OOB: 0
       drv dropped rx total: 0
     Rx Queue#: 2
       pkts rx OOB: 0
       drv dropped rx total: 0
     Rx Queue#: 3
       pkts rx OOB: 0
       drv dropped rx total: 0
```

Which statements are correct?

- A. The receive ring of the VMXNET3 adapter overflowed, a drop that only the hypervisor can see.
- B. The frames were discarded on the host side of the vNIC, before Linux could take them.
- C. rx_dropped in `ip -s link` includes the ring-full drops of the VMXNET3 adapter.
- D. The pkts rx OOB counters in the ethtool output rule out a full receive ring.
- E. The gap between the vCenter export and the Linux counters shows a counter fault in vCenter.
- F. Enlarging the Linux receive ring with `ethtool -G` will make the vCenter drops go away.
- G. The physical network dropped these packets before they reached the host.
- H. In the export, Receive packets dropped is a count per 20-second sample.
- I. In the sample with the most drops, the VM lost more than half of the packets sent to it.
- J. Every receive drop that ESXi counts on a VM also shows somewhere in Linux.

## Likely wrong answer
A: the ring overflowed, and only the hypervisor sees that. Or E: one of the tools miscounts.

## Expected key points
- Answer: B, D, H.
- A false: the misconception. VMXNET3 shares a ring-full drop with the guest driver, which shows it as pkts rx OOB; the ethtool output reads 0 on all four receive queues.
- B true: Receive packets dropped is above 0 in the export (a 12-minute run of rows), while Linux shows RX dropped 0 and pkts rx OOB 0. ESXi dropped the frames before delivery, for example on an NSX Distributed Firewall rule (filtered at the port's I/O chain) or against the port's security settings; the guest never received them, so it cannot count them.
- C false: rx_dropped counts only frames the driver itself dropped; the ring-full count is pkts rx OOB.
- D true: the vmxnet3 driver shows the ring-full count per receive queue as pkts rx OOB (pktsRxOutOfBuf); it is 0 on Rx Queue 0 to 3, so the ring never ran full.
- E false: each layer counts what it sees; a drop before delivery exists only in the hypervisor's counters.
- F false: the wrong action. The ring was not full; a larger ring does not change a drop that happens before delivery.
- G false: a frame dropped in the physical network never reaches the host, so the VM counters cannot count it.
- H true: packet and drop counters are totals per sample interval (summation), not rates per second. The rows are 20 seconds apart, and Packets received / 20 at about 1,000 bytes per packet matches Data receive rate (KBps) in every row.
- I false: in the worst row, Receive packets dropped is 3-8% of Packets received (below 10% by construction), far from half.
- J false: the over-correction. Drops before delivery (a firewall rule, the security policy) never reach Linux; only a full ring is counted on both sides.

## Notes
- Paired with the theory question 0039 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 from project/question-pairing-2026-11-14.md, item C26 (origin: synthetic). Counts only after author approval.
- Review 2026-11-15: options reworded away from 0039; I (a false value reading) and J (over-correction) added; capture by an NSX Distributed Firewall Drop rule (Broadcom KB 449113, added to packet-drop-accounting). Key unchanged: B, D, H.
- Converted 2026-11-15 from screenshots to a vCenter Real-time CSV and Linux tool text (project/practical-questions-as-exports-2026-11-15.md). D, E and H reworded from screen to export; truth values unchanged. B and J rest on the Distributed Firewall boundary of Broadcom KB 449113 (ESXi 8.x, NSX 4.x), still to check on 9.1 (review note in packet-drop-accounting); the security-policy drop keeps B and J true either way.

## Metadata
```yaml
id: "0420"
title: "VM receive drops that Linux does not count"
product: [vsphere, linux, nsx]
technology: [network]
task: troubleshoot
level: 300
answer_type: deterministic
input: [table]
object: [vm, guest-os]
tool: [vcenter, guest-os-tools]
knowledge:
  - vsphere/technology/network/concepts/packet-drop-accounting
  - vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
  - vsphere/tools/vsphere-client/vcenter-statistics
knowledge_main: vsphere/technology/network/concepts/packet-drop-accounting
attachments:
  - 0420/ingest-04-network-real-time.csv
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C26"
answer: [B, D, H]
misconception: [A, E]
misconception_type: [layer-confusion]
pair: "0039"
status: draft
```
