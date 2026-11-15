# Metric sources: ESXi vs vCenter

## Definition
- ESXi is the source of the vSphere metrics: it samples its counters every 20 seconds ([`vsphere/tools/vsphere-client/vcenter-statistics`](../tools/vsphere-client/vcenter-statistics.md), section Definition).
- vCenter stores the ESXi samples, rolls them up into coarser intervals, and adds counters of its own, such as VM CPU Usage (MHz) and Usage (%).
- ESXi and vCenter formulas do not match in every case. Example: ESXi CPU Used is a % in esxtop and ms in vCenter ([`vsphere/technology/cpu/metrics/host/used`](../technology/cpu/metrics/host/used.md)).
- Which VM CPU counter comes from ESXi and which from vCenter: [`vsphere/technology/cpu/metrics/comparisons/consumption-metrics`](../technology/cpu/metrics/comparisons/consumption-metrics.md), section Source of each.

## Each tool reads a different copy
- esxtop reads the host directly, at its own refresh interval (5 seconds by default), and in its own units: network in megabits per second, where vCenter shows kilobytes per second ([`vsphere/tools/esxtop/units-vs-vsphere-client`](../tools/esxtop/units-vs-vsphere-client.md)).
- The vSphere Client Real-time chart shows the 20-second samples; history from 1 Day onward shows rolled-up averages at the configured statistics level.
- VCF Operations collects from vCenter every 5 minutes and stores the 5-minute average of the 20-second samples; its 20-second peak metrics keep the highest of the 15 samples ([`vcf-operations/features/peak-20-second-metrics`](../../vcf-operations/features/peak-20-second-metrics.md)).
- VCF Operations also computes metrics of its own under a vSphere name. ESXi CPU Demand in VCF Operations counts the kernel's CPU reservation and, per running VM, the higher of its demand and its CPU reservation; vCenter `cpu.demand` leaves both reservations out ([`vsphere/technology/cpu/metrics/host/demand`](../technology/cpu/metrics/host/demand.md), section vCenter vs VCF Operations).
- Guest OS counters on the VM object come from VMware Tools, inside the Guest OS, not from ESXi ([`vsphere/architecture/vm-vs-guest-os`](vm-vs-guest-os.md)).

## Consequence
- When two tools disagree on a value, check four things before calling either wrong: the source (ESXi, vCenter, VCF Operations, Guest OS), the formula, the interval and rollup, and the unit.
- A metric file states its data source (ESXi, vCenter, VCF Operations, Guest OS), because one name can carry several formulas.

## Misconceptions
- "esxtop and vCenter show different values for the same counter, so one tool is wrong" → the interval (5 seconds against 20-second samples or rolled-up averages), the unit and sometimes the formula differ. Convert the unit and compare the same interval first.
- "ESXi CPU Demand in vCenter and in VCF Operations is one counter" → same name, two formulas: VCF Operations counts the CPU reservations of the kernel and the VMs. Subtract them before comparing.

## Metadata
```yaml
id: vsphere/architecture/metric-sources
retriever_guide: how-it-works
scope: vsphere
technology:
- cpu
- network
pillar:
- performance
product:
- vsphere
- vcf-operations
object:
- VirtualMachine
- HostSystem
internal_derive:
- vsphere/tools/vsphere-client/vcenter-statistics
- vsphere/technology/cpu/metrics/comparisons/consumption-metrics
- vsphere/tools/esxtop/units-vs-vsphere-client
- vcf-operations/features/peak-20-second-metrics
- vsphere/technology/cpu/metrics/host/demand
related:
- vsphere/architecture/provider-consumer
- vsphere/technology/cpu/metrics/host/used
- vsphere/architecture/vm-vs-guest-os
- vcf-operations/vcf-operations-role
source:
  document: Knowledge base
  path: The World of Metrics > Metrics Nuances > Complexity > Architecture Complexity
corrections: []
review_notes: []
status: draft
```
