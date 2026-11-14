# ESXi CPU Wait

## Meaning
- Sum of the Wait of the VMs on the host.
- Example: a host with 2 VMs shows Wait equal to the sum of the 2 VM Wait values.

## Use
- Ignore it. It mixes idle time.

## Misconceptions
- "High host Wait means the host waits for IO" → it is the sum of VM Wait, mostly idle.

## Metadata
```yaml
id: vsphere/technology/cpu/metrics/host/wait
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
internal_derive:
- vsphere/technology/cpu/concepts/vcpu-states
- vsphere/architecture/provider-consumer
same_name:
- vsphere/technology/cpu/metrics/virtual-motherboard/wait
same_meaning: []
related:
- vsphere/technology/cpu/metrics/virtual-motherboard/wait
- vsphere/technology/cpu/metrics/host/idle
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: CPU > ESXi > Wait Metric
corrections: []
review_notes: []
status: draft
```
