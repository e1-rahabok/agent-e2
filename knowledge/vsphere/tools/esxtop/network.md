# esxtop network counters

## Scope
- The network panel mixes virtual (VM and VMkernel ports) and physical (vmnic uplinks). Start with the virtual side: closest to VMs and the kernel.
- No latency or retransmit counters.

## Contention
| Counter | Meaning |
|---|---|
| %DRPTX | Dropped transmit packets (%). High: the physical NIC or uplink switch cannot cope. |
| %DRPRX | Dropped receive packets (%). High: the host or VM lacks CPU to process packets, or the ring buffer is too small. |

- Expect at most 0.x%. On dedicated networks (vSAN, vMotion), 0% on every host at all times.
- Receive drops shown at the vSwitch port happen between the virtual switch and the guest driver. More Rx buffers in the virtual NIC driver reduce them (Broadcom KB 312565).

## Consumption
| Counter | Meaning |
|---|---|
| PKTTXMUL/s, PKTRXMUL/s | Multicast packets transmitted, received per second. |
| PKTTXBRD/s, PKTRXBRD/s | Broadcast packets transmitted, received per second. |
| PKTTX/s, PKTRX/s | All packets, including multicast and broadcast. |
| MbTX/s, MbRX/s | Megabits per second (vSphere Client uses bytes). |
| PSZTX, PSZRX | Average packet size. Far below 1,500: discuss with the network team. |
| ACTN/s | Kernel actions per second. Internal. |

- A 10 Gb NIC with 1,500-byte packets peaks at about 833,333 packets per second each way.
- Check broadcast and multicast first; they should be low.

## Configuration
| Counter | Meaning |
|---|---|
| PORT-ID | Virtual port ID. |
| UPLINK | Y: an uplink (vmnic). |
| UP | Y: link up. |
| SPEED | Link speed (Mb/s). |
| FDUPLX | Y: full duplex. N is a problem. |
| USED-BY, DNAME | Port user; virtual device name. |
| TEAM-PNIC | Physical NIC used for the team uplink: on a VM or VMkernel port, the vmnic it uses now. |

- DTYP (hub or switch) is no longer shown; the vSphere 9.1 documentation still lists it, a documentation error. vSphere Client shows switches, VMkernel ports and NICs in more detail.

## RDMA device
- RDMA gives applications direct access to the NIC, bypassing OS overhead.

| Counter | Meaning |
|---|---|
| %PKTDTX, %PKTDRX | Dropped packets as % of sent and received. The only contention counters. |
| PKTTX/s, PKTRX/s | Packets per second. Check the card's packet limit. |
| MbTX/s, MbRX/s | Throughput. No packet-type breakdown, no packet size. |
| QP, CQ | Queue pairs and completion queue pairs allocated. |
| SRQ | Shared receive queues allocated (the NIC can be shared). |
| MR | Memory regions allocated. |
| NAME, DRIVER, STATE, TEAM-PNIC | Device, driver, active or down, paired physical NIC. |

- RDMA counters are not in vSphere Client.

## Misconceptions
- "Receive drops mean the physical network drops" → often between the vSwitch and the guest driver.
- "MbTX/s matches vSphere Client KBps" → bits vs bytes.

## Metadata
```yaml
id: vsphere/tools/esxtop/network
retriever_guide: metric-meaning
scope: vsphere
technology:
- network
pillar:
- performance
product:
- vsphere
object:
- HostSystem
- VirtualMachine
metric_class: contention
internal_derive:
- vsphere/technology/network/concepts/network-observability
same_name: []
same_meaning: []
related:
- vsphere/tools/esxtop/overview
- vsphere/technology/network/metrics/host/packets-dropped
- vsphere/technology/network/vnic-rx-drops
- vsphere/tools/esxtop/units-vs-vsphere-client
- vsphere/technology/network/concepts/nic-teaming
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: Provider Objects > esxtop > Network
corrections: []
review_notes:
- 'The 9.1 documentation still lists DTYP (H = hub, S = switch) in the network panel; the field is not shown on ESXi 9.1; the documentation is out of date.'
- 'To check: KB from the source document, not read: https://knowledge.broadcom.com/external/article/312565/the-output-of-esxtop-show-dropped-receiv.html'
status: draft
```
