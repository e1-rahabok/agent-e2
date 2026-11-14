# Packet drop accounting

## Receive drop: full guest receive ring
- Causes:
  - a microburst larger than the guest's receive ring buffer;
  - the guest does not empty the ring in time: CPU busy inside the guest, or the vCPU waiting on the hypervisor (Ready, Co-stop).
- When the ring has no free descriptor, the hypervisor cannot copy the frame into guest memory. The new frame is discarded: tail drop, not first in first out.
- The hypervisor-to-vNIC path is Layer 2, memory-mapped rings. It knows nothing of TCP state.

### VMXNET3 on ESXi
| Layer | Counts the drop? | Where |
|---|---|---|
| Distributed switch port | Yes | Dropped packets of the dvPort |
| VM (vNIC) | Yes | esxtop %DRPRX; vCenter `net.droppedRx.summation` |
| Guest OS | Yes | VMXNET3 shares the drop with the guest through shared memory |

- Linux: `ethtool -S <interface>` shows the ring-full count per receive queue as `pkts rx OOB` (device counter `pktsRxOutOfBuf`). `rx_dropped` (`ip -s link`) leaves it out: it counts only frames the driver itself dropped (receive errors, failed buffer allocation).
- Windows: confirm the drop at the host (vsish `rxSummary`, running out of buffers). The Windows counter that carries the ring-full count is in `review_notes`.
- So the drop is visible to the hypervisor and to the guest. It is caused and fixed in the guest (larger ring, CPU), which is why the Guest OS owner fixes it.

## Transmit drop: congested top-of-rack switch
- Ethernet does not acknowledge frames. Unless 802.3x PAUSE flow control holds it back, ESXi counts a frame as sent once the physical NIC has put it on the wire.
- A frame dropped by a congested top-of-rack switch is counted only in that switch.

```mermaid
sequenceDiagram
    participant GOS as 1. Guest OS (TX)
    participant vNIC as 2. VM vNIC (TX)
    participant vPG as 3. Port group (RX)
    participant vSW as 4. ESXi virtual network (TX)
    participant pNIC as 5. ESXi physical NIC (TX)
    participant TOR as 6. Top-of-rack switch (RX)
    GOS->>vNIC: 1. TX descriptor on the shared ring. Drop count 0
    vNIC->>vPG: 2. VMkernel reads the packet. Drop count 0
    vPG->>vSW: 3. Port group receives it. Drop count 0
    vSW->>pNIC: 4. Forwarded to the uplink. Drop count 0
    pNIC->>TOR: 5. Serialized onto the cable. Drop count 0
    TOR--xTOR: 6. Buffers full: tail drop or WRED. InDiscards +1
```

- Steps 1-5 count 0: the guest, the vNIC, the port group, the virtual network and the physical NIC all completed their part.
- Step 6: the switch ASIC drops the frame and counts it as an input discard or input queue drop.
- Recovery is TCP in the guest: no acknowledgement returns, the retransmission timer expires (or duplicate acknowledgements arrive), and the guest sends the payload again in a new frame.
- vSphere metrics cannot show this drop. Evidence: TCP retransmissions in the Guest OS, and the switch's discard counters (network team).

## Misconceptions
- "The Guest OS shows no dropped packets, so the network is clean" → on transmit, a drop at the top-of-rack switch is invisible to ESXi and to the guest; look at TCP retransmissions and the switch counters.
- "A receive drop on the VM means the physical network dropped it" → a full guest receive ring drops it inside the host; check the guest's CPU, the vCPU's Ready and the ring size.
- "The hypervisor cannot see a VMXNET3 ring drop" → it counts it at the port and the VM (%DRPRX, droppedRx); the guest sees it too.

## Metadata
```yaml
id: vsphere/technology/network/concepts/packet-drop-accounting
retriever_guide: how-it-works
scope: vsphere
technology:
- network
pillar:
- performance
product:
- vsphere
object:
- VirtualMachine
- HostSystem
- DistributedVirtualPortgroup
internal_derive:
- vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
related:
- vsphere/technology/network/metrics/host/packets-dropped
- vsphere/tools/esxtop/network
- sp5-framework/concepts/realms-and-layers
source:
  document: Packet Lifecycle and Metric Accounting in Virtualized Networks (2026-11-07)
  path: Scenario 1 (RX, guest buffer exhaustion); Scenario 2 (TX, top-of-rack congestion)
corrections:
- '2026-11-07: a full VMXNET3 receive ring is counted by the hypervisor (port, %DRPRX, droppedRx) and the guest. Corrects the reason given in Q070 (not visible to the hypervisor); the conclusion, fixed in the guest, stands.'
- '2026-11-14: the source names the Linux counter rx_out_of_buffer (a Mellanox mlx5 name). The vmxnet3 driver shows the ring-full count as "pkts rx OOB" (pktsRxOutOfBuf) in ethtool -S, and rx_dropped leaves it out (https://github.com/torvalds/linux/blob/master/drivers/net/vmxnet3/vmxnet3_ethtool.c).'
review_notes:
- 'To check: which Windows VMXNET3 counter carries the ring-full count (Packets Received Discarded, ifHCInDiscards, or none); Broadcom KB 324556 and KB 437897 name only the host view (vsish rxSummary, running out of buffers).'
status: draft
```
