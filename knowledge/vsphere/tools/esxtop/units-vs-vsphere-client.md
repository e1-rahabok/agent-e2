# Network units: esxtop vs vSphere Client

## Meaning
- esxtop shows network counters in megabits.
- vSphere Client: the API stores network counters in kilobytes per second (KBps); the host and cluster Network charts show megabits per second (Mbps).

## Misconceptions
- Comparing values from the two tools without converting bits to bytes and mega to kilo.

## Metadata
```yaml
id: vsphere/tools/esxtop/units-vs-vsphere-client
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
- HostSystem
- VirtualMachine
metric_class: consumption
internal_derive:
- sp5-framework/observability/units
same_name: []
same_meaning: []
related: []
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: The World of Metrics > Metrics Nuances > Complexity > Other Nuances
corrections: []
review_notes: []
status: draft
```
