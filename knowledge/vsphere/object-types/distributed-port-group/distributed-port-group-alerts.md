# Distributed port group alerts

## Coverage and receivers
- A distributed port group is a network provider: its alerts go to the infrastructure team, above all the network team.
- Alerted: dropped packets. Only contention is alerted on a network object: a network has no clear 100%, so a consumption ceiling is hard to set.
- Every value is in the alert rows of [`catalog/thresholds-alerts.yaml`](../../../catalog/thresholds-alerts.yaml), shown with this file.

## Distributed port group dropped packets
- Detects: packets dropped on the port group, as a share of its packets ([`vsphere/technology/network/metrics/distributed-switch/packets-dropped`](../../technology/network/metrics/distributed-switch/packets-dropped.md)).
- Red only, as on every network object, to avoid alert storms. TCP resends a dropped segment, so the data arrives in the end; the cost is time.
- Orange is not set: it gave false positives.
- Planned change: count transmitted packets only. Received drops include packets not destined for the VM or against the security settings ([`vsphere/technology/network/metrics/virtual-motherboard/packets-dropped`](../../technology/network/metrics/virtual-motherboard/packets-dropped.md)), and drops in a VM's full receive ring, whose cause and fix are in the Guest OS ([`vsphere/technology/network/concepts/packet-drop-accounting`](../../technology/network/concepts/packet-drop-accounting.md)). Transmit drops stay with what the infrastructure team owns.

## Misconceptions
- "An orange port group alert gives early warning" → it gave false positives; red only.
- "Every received drop on a port group is a network fault" → a full receive ring in the VM is a Guest OS problem.

## Metadata
```yaml
id: vsphere/object-types/distributed-port-group/distributed-port-group-alerts
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
internal_derive:
- sp5-framework/outputs/alert-design
- vsphere/technology/network/metrics/distributed-switch/packets-dropped
- vsphere/technology/network/concepts/packet-drop-accounting
- vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
related:
- vsphere/object-types/distributed-switch/distributed-switch-alerts
- vsphere/object-types/esxi/esxi-alerts
- vsphere/object-types/vm/vm-alerts
- vsphere/technology/network/vnic-rx-drops
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Proactive Operations > Alert > Network Alerts > Contention Alerts'
corrections: []
review_notes: []
status: draft
```
