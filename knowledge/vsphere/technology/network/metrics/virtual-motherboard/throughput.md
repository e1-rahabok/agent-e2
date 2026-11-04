# VM Network Throughput

## Meaning
- Data rate per direction, in KB per second (vCenter). esxtop shows megabits per second.
- The book assumes it includes broadcast and multicast and excludes dropped packets.
- Standard packet size: 1,500 bytes. Jumbo frames: 9,000 bytes. NSX: typically 1,600.

## Packet size
```text
Average packet size = throughput / packet count
```

## Traps
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
internal_derive: []
same_name: []
same_meaning: []
related:
- vsphere/technology/network/metrics/virtual-motherboard/packets
- vsphere/technology/network/metrics/comparisons/esxtop-vs-vsphere-client-units
source:
  document: PART 3 - Counters.docx
  path: Network > VM > Overview; Consumption Metrics
corrections: []
review_notes: []
status: draft
```
