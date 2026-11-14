# VM Network Throughput

## Meaning
- Data rate per direction, in KB per second (vCenter). esxtop shows megabits per second.
- Standard packet size: 1,500 bytes. Jumbo frames: 9,000 bytes. NSX adds its Geneve header on the transport network (MTU at least 1,600), not to the VM's packets.

## Packet size
```text
Average packet size = throughput / packet count
```

## Misconceptions
- "KBps and Mbps values disagree" → vCenter uses kilobytes, esxtop megabits.

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
- 'To check: whether VM network throughput includes broadcast and multicast and excludes dropped packets.'
status: draft
```
