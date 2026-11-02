# ESXi CPU Wait

## Meaning
- Sum of the Wait of the VMs on the host.
- Example: a host with 2 VMs shows Wait equal to the sum of the 2 VM Wait values.

## Use
- Ignore it. It mixes idle time.

## Traps
- "High host Wait means the host waits for IO" → it is the sum of VM Wait, mostly idle.

## Metadata
```yaml
id: vsphere/cpu/metrics/host/wait
retriever_guide: metric-meaning
scope: vsphere
technology:
- cpu
pillar:
- performance
product:
- vsphere
object:
- HostSystem
metric_class: context
internal_derive: []
same_name:
- vsphere/cpu/metrics/virtual-machine/wait
same_meaning: []
related:
- vsphere/cpu/metrics/virtual-machine/wait
- vsphere/cpu/metrics/host/idle
source:
  document: PART 3 - Counters.docx
  path: CPU > ESXi > Wait Metric
corrections: []
review_notes: []
status: draft
```
