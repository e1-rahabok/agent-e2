# Network alerts

## What to set
- Network consumption alerts are hard to define: a network has no clear 100%, so the ceiling is hard to set. Only contention (dropped packets) is alerted.
- Red only on every object, to avoid alert storms. Dropped packets are usually retransmitted, so users rarely feel a problem.

## VM dropped packets
- Red: transmitted packets dropped above 4%.
- 4% is high: 1 packet in 25 dropped. It is set high because it is measured within a 20-second period.
- Planned change: make the threshold relative to the packets transmitted.
- Metric: `vsphere/technology/network/metrics/virtual-motherboard/packets-dropped`.

## ESXi dropped packets
- Red: more than 50 transmitted packets dropped on the virtual network.
- Red: more than 50 transmitted packets dropped on the physical network.
- Metric: `vsphere/technology/network/metrics/host/packets-dropped`.

## Distributed port group dropped packets
- Red: dropped packets above 10%.
- Orange: not set; it gave false positives.
- Planned change: count transmitted packets only.
- Metric: `vsphere/technology/network/metrics/distributed-switch/packets-dropped`.

## Distributed switch
- No alert: a distributed switch is a group of ESXi hosts and port groups, already covered by their alerts.

## Traps
- "4% dropped is low" → it is 1 packet in 25; it is set high only because it is read over 20 seconds.
- "Every dropped packet hurts users" → TCP retransmits; that is why only red is set.
- "Alert on network utilization" → there is no clear 100% for a network.
- "Alert on the distributed switch too" → it only groups hosts and port groups, which have their own alerts.

## Metadata
```yaml
id: vsphere/technology/network/configuration/network-alerts
retriever_guide: what-to-set
scope: vsphere
technology:
- network
pillar:
- performance
product:
- vsphere
- vcf-operations
object:
- VirtualMachine
- HostSystem
- DistributedVirtualPortgroup
- VmwareDistributedVirtualSwitch
internal_derive:
- sp5-framework/alerts/alert-design
- vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
- vsphere/technology/network/metrics/host/packets-dropped
- vsphere/technology/network/metrics/distributed-switch/packets-dropped
related:
- vsphere/technology/network/concepts/packet-drop-accounting
- vsphere/technology/network/troubleshooting/vnic-rx-drops
source:
  document: PART 2 - Consumption for Agent E2.docx
  path: 'Proactive Operations > Alert > Network Alerts > Contention Alerts (p. 26)'
corrections: []
review_notes:
- 'Section ''VM dropped packets'': the source says 4% is 1 in 40 packets; 4% is 1 in 25. Written as 1 in 25. The source row ends with "and", so a second condition may be missing. Q147.'
- 'Section ''What to set'': the source says the ratio is always 100% because dropped packets are retransmitted; meaning unclear, not copied. Q147.'
- 'Section ''Distributed port group dropped packets'': the reason for transmitted only (received drops gave false positives) is a reading of the source text "orange alert is not implemented due to false positive. In future I will change to transmit only". Q147.'
status: draft
```
