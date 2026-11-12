# Distributed switch alerts

## Coverage and receivers
- A distributed switch is a network provider: its alerts would go to the infrastructure team, above all the network team.
- No alert in the set.

## Not alerted, and why
- Contention: a distributed switch is a group of ESXi hosts and port groups, already covered by their alerts ([`vsphere/object-types/esxi/esxi-alerts`](../esxi/esxi-alerts.md), [`vsphere/object-types/distributed-port-group/distributed-port-group-alerts`](../distributed-port-group/distributed-port-group-alerts.md)).
- Consumption: a network has no clear 100%, so the ceiling is hard to set.

## Misconceptions
- "Alert on the distributed switch too" → it only groups hosts and port groups, which have their own alerts.

## Metadata
```yaml
id: vsphere/object-types/distributed-switch/distributed-switch-alerts
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
- VmwareDistributedVirtualSwitch
internal_derive:
- sp5-framework/outputs/alert-design
related:
- vsphere/object-types/distributed-port-group/distributed-port-group-alerts
- vsphere/object-types/esxi/esxi-alerts
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Proactive Operations > Alert > Network Alerts > Contention Alerts; Alerts Planning > Design (alert count table)'
corrections: []
review_notes: []
status: draft
```
