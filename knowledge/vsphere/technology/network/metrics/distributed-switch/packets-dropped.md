# Distributed Switch Packets Dropped (switch, port and LAG)

## Meaning
- Dropped packet counts that vCenter keeps on the distributed switch object, at the switch, per distributed port (DVPort) and per link aggregation group (LAG), each for transmit and receive.
- Dropped packets are the only network contention signal vSphere has: there is no network latency or retransmit counter.

## Counters (vCenter 9.1 API)
| Scope | Transmit | Receive |
|---|---|---|
| Switch | `net.throughput.droppedTx` | `net.throughput.droppedRx` |
| DVPort | `net.throughput.vds.droppedTx` | `net.throughput.vds.droppedRx` |
| LAG | `net.throughput.vds.lagDropTx` | `net.throughput.vds.lagDropRx` |

- Statistics level 3, rollup average: no history at the default level 1.
- No vSphere Client chart: read them through the API or a tool that reads it.

## Reading it
- Each component counts its own drops: the distributed port, the VM vNIC ([`vsphere/technology/network/metrics/virtual-motherboard/packets-dropped`](../virtual-motherboard/packets-dropped.md)), the LAG and the host vmnic ([`vsphere/technology/network/metrics/host/packets-dropped`](../host/packets-dropped.md)). Read each counter for its own component.
- Which component caused a drop is a troubleshooting question the counters alone do not settle. For vNIC receive drops, see [`vsphere/technology/network/troubleshooting/vnic-rx-drops`](../../troubleshooting/vnic-rx-drops.md).
- A drop count means little without the packet count of the same scope: read it as a share of `net.throughput` packets. See [`vsphere/technology/network/metrics/distributed-switch/packets`](packets.md).

## Misconceptions
- "No dropped packets at the switch, so no VM drops packets" → the switch total hides one port; check per DVPort and per vNIC.
- "Drops at level 1 history" → these counters are level 3; the default history holds none.

## Metadata
```yaml
id: vsphere/technology/network/metrics/distributed-switch/packets-dropped
retriever_guide: metric-meaning
scope: vsphere
technology:
- network
pillar:
- performance
product:
- vsphere
object:
- VmwareDistributedVirtualSwitch
metric_class: contention
internal_derive:
- vsphere/technology/network/concepts/network-observability
same_name:
- vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
- vsphere/technology/network/metrics/host/packets-dropped
same_meaning: []
related:
- vsphere/technology/network/metrics/distributed-switch/packets
- vsphere/technology/network/troubleshooting/vnic-rx-drops
- vsphere/tools/vsphere-client/vcenter-statistics
source:
  document: Repository e1-rahabok/Observability-vSphere, vsphere-metrics.csv (vCenter 9.1.0 build 25370922)
  path: https:/github.com/e1-rahabok/Observability-vSphere/blob/main/vsphere-metrics.csv
corrections: []
review_notes:
- 'Whole file: counter names, scopes, level and rollup from the vCenter 9.1.0 API export.'
- 'To check: Section ''Reading it'': port, vNIC and uplink each have their own dropped packet counter; how to use them to find the component that caused a drop is not settled.'
status: draft
```
