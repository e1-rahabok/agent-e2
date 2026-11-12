# Distributed switch and port group alerts

## Coverage and receivers
- The network providers: their alerts go to the infrastructure team, above all the network team.
- Alerted: distributed port group dropped packets. The distributed switch itself gets no alert.
- Every value is in the alert rows of [`catalog/thresholds-alerts.yaml`](../../../../catalog/thresholds-alerts.yaml), shown with this file.
- Only contention (dropped packets) is alerted on a network object. Consumption is hard to define: a network has no clear 100%, so the ceiling is hard to set.
- Red only, to avoid alert storms. Dropped packets are usually retransmitted, so users rarely feel a problem.

## Distributed port group dropped packets
- Detects: packets dropped on the port group, as a share of its packets ([`vsphere/technology/network/metrics/distributed-switch/packets-dropped`](../../../technology/network/metrics/distributed-switch/packets-dropped.md)).
- Orange is not set: it gave false positives.
- Planned change: count transmitted packets only.

## Distributed switch: no alert
- A distributed switch is a group of ESXi hosts and port groups, already covered by their alerts ([`vsphere/object-types/esxi/alerts/esxi-alerts`](../../esxi/alerts/esxi-alerts.md), section ESXi dropped packets).

## Misconceptions
- "Alert on the distributed switch too" → it only groups hosts and port groups, which have their own alerts.
- "An orange port group alert gives early warning" → it gave false positives; red only.

## Metadata
```yaml
id: vsphere/object-types/distributed-switch/alerts/distributed-switch-alerts
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
- DistributedVirtualPortgroup
- VmwareDistributedVirtualSwitch
internal_derive:
- sp5-framework/outputs/alert-design
- vsphere/technology/network/metrics/distributed-switch/packets-dropped
related:
- vsphere/object-types/esxi/alerts/esxi-alerts
- vsphere/object-types/vm/alerts/vm-alerts
- vsphere/technology/network/concepts/packet-drop-accounting
- vsphere/technology/network/troubleshooting/vnic-rx-drops
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Proactive Operations > Alert > Network Alerts > Contention Alerts'
corrections: []
review_notes:
- 'Section ''Distributed port group dropped packets'': the reason for transmitted only (received drops gave false positives) is a reading of the source text "orange alert is not implemented due to false positive. In future I will change to transmit only". Q147.'
status: draft
```
