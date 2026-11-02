---
id: vsphere/network/distinctions
type: distinction
scope: vsphere
resources: [network]
objects: [vm, esxi]
related:
  - foundations/units
  - foundations/resource-nature
  - vsphere/foundations/provider-consumer
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances
corrections: []
review_notes: []
status: draft
---

# Network distinctions

## Unit: esxtop vs vSphere Client
- pattern: same-object-same-metric-different-name (unit differs)
- esxtop shows network counters in megabits.
- vSphere Client shows network counters in kilobytes.
- trap: comparing esxtop and vSphere Client values without converting bits ↔ bytes and mega ↔ kilo.
- src: Complexity > Other Nuances

## ESXi network: provider metric vs sum of consumers
- Physical network in ESXi: provider metric. No VM equivalent.
- Sum of VM network in ESXi: sum-of-consumers metric.
- The metric name does not say which kind it is.
- src: Virtualization Impact
- See `vsphere/foundations/provider-consumer`.

## Network is line and dot
- Cables are lines. Switches are dots. This makes network metrics harder than node (server, storage) metrics.
- See `foundations/resource-nature`.
