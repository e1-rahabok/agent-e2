# Distributed Switch Packets (switch, port and LAG)

## Meaning
- Packet counts that vCenter keeps on the distributed switch object, at three scopes:
  - the switch as a whole;
  - each distributed port (DVPort), which a VM vNIC, a VMkernel adapter or an uplink connects to;
  - each link aggregation group (LAG) of uplinks.
- Each scope splits by direction (transmit, receive) and traffic type (all packets, multicast, broadcast).
- The distributed port group object has no vCenter performance counters. Port-level counts live on the switch object, per DVPort.

## Counters (vCenter 9.1 API)
| Scope | Transmit | Receive |
|---|---|---|
| Switch | `net.throughput.pktsTx`, `pktsTxMulticast`, `pktsTxBroadcast` | `net.throughput.pktsRx`, `pktsRxMulticast`, `pktsRxBroadcast` |
| DVPort | `net.throughput.vds.pktsTx`, `pktsTxMcast`, `pktsTxBcast` | `net.throughput.vds.pktsRx`, `pktsRxMcast`, `pktsRxBcast` |
| LAG | `net.throughput.vds.lagTx`, `lagTxMcast`, `lagTxBcast` | `net.throughput.vds.lagRx`, `lagRxMcast`, `lagRxBcast` |

- All are statistics level 3, rollup average. At the default level 1 vCenter keeps no history for them: only the real-time view after the level is raised.
- The vSphere Client has no performance charts for distributed switches or port groups. The counters are reachable through the API and the tools that read it.
- The counter summaries call them a rate of packets; the API stat type is absolute. Read a value as packets per sample interval unless the tool states otherwise.

## Reading it
- Most traffic should be unicast. A high multicast or broadcast share explains receive drops and wasted CPU on every VM in the broadcast domain. See [`vsphere/technology/network/metrics/vm-network-metrics`](../vm-network-metrics.md).
- LAG counts show whether traffic spreads across the uplinks of a link aggregation group.
- VCF Operations shows distributed port group metrics aggregated over all hosts. vCenter itself keeps none on the port group. See [`vsphere/technology/network/concepts/network-observability`](../../concepts/network-observability.md).

## Misconceptions
- "No chart for the distributed switch, so vCenter has no switch data" → the counters exist at level 3, through the API.
- "Distributed port group has its own counters in vCenter" → it has none; port data sits on the switch, per DVPort.
- "Switch packets = sum of vmnic packets" → the switch also counts VM-to-VM traffic that never leaves the host.

## Metadata
```yaml
id: vsphere/technology/network/metrics/distributed-switch/packets
retriever_guide: metric-meaning
scope: vsphere
technology:
- network
pillar:
- performance
- capacity
product:
- vsphere
object:
- VmwareDistributedVirtualSwitch
metric_class: consumption
internal_derive:
- vsphere/technology/network/concepts/network-observability
same_name:
- vsphere/technology/network/metrics/virtual-motherboard/packets
same_meaning: []
related:
- vsphere/technology/network/metrics/distributed-switch/packets-dropped
- vsphere/technology/network/metrics/host/throughput
- vsphere/tools/vsphere-client/vcenter-statistics
source:
  document: Repository e1-rahabok/Observability-vSphere, vsphere-metrics.csv (vCenter 9.1.0 build 25370922)
  path: https://github.com/e1-rahabok/Observability-vSphere/blob/main/vsphere-metrics.csv; README section Object types without metrics
corrections: []
review_notes:
- 'Whole file: counter names, scopes, level, rollup, stat type and summaries from the vCenter 9.1.0 API export. The distributed port group returned no counters (same README).'
- 'To check: Sections ''Meaning'' (what a DVPort connects to), ''Reading it'' and the third misconception: inferred from the counter scopes, not from a document.'
- 'Section ''Reading it'': VCF Operations port group metrics aggregated over all hosts restates network-observability (book).'
status: draft
```
