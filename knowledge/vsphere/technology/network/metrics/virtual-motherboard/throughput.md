# VM Network Throughput

## Meaning
- Data rate per direction, in KB per second (vCenter). esxtop shows megabits per second.
- Standard packet size: 1,500 bytes. Jumbo frames: 9,000 bytes. NSX adds its Geneve header on the transport network (MTU at least 1,600), not to the VM's packets.
- The vSphere Client chart title says Mbps, but the counters are KBps (1 KB = 1,024 bytes); esxtop Mbps is about KBps × 8 / 1,000 ([`vsphere/tools/esxtop/units-vs-vsphere-client`](../../../../tools/esxtop/units-vs-vsphere-client.md)).
- Relevance for operations: capacity (the VM's network footprint per direction) and performance troubleshooting (with the packet count, the average packet size). Not alerted: a network has no clear 100% ([`vsphere/object-types/vm/vm-alerts`](../../../../object-types/vm/vm-alerts.md), section Not alerted).

## Packet size
```text
Average packet size = throughput / packet count
```

## Misconceptions
- "KBps and Mbps values disagree" → vCenter uses kilobytes, esxtop megabits.
- "The chart title says Mbps, so the VM value is megabits" → the VM network counters are kilobytes per second, whatever the chart title says.

## Metadata
```yaml
id: vsphere/technology/network/metrics/virtual-motherboard/throughput
retriever_guide: metric-meaning
scope: vsphere
technology:
- network
pillar:
- performance
product:
- vsphere
object:
- VirtualMachine
layer:
- virtual-motherboard
metric_class: consumption
internal_derive:
- vsphere/technology/network/concepts/network-characteristics
- sp5-framework/observability/units
same_name:
- vsphere/technology/network/metrics/host/throughput
same_meaning: []
related:
- vsphere/technology/network/metrics/virtual-motherboard/packets
- vsphere/tools/esxtop/units-vs-vsphere-client
source:
  document: Knowledge base
  path: Network > VM > Overview; Consumption Metrics
corrections: []
review_notes:
- 'To check: Section ''Meaning'': whether VM network throughput includes broadcast and multicast packets and leaves out dropped packets, as VM Network Packets does; a live comparison of the throughput and packet counters of one VM.'
status: draft
```
