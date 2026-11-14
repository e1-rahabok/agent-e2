# ESXi CPU contention metrics

## The set
- vSphere Client host-level counters: Co-stop, Ready, Latency, Readiness, Wait, Swap wait, Idle.
- They are aggregates of the VMs. The host itself has no contention.
- Co-stop and Ready exclude contention faced by non-VM worlds.
![vCenter ESXi CPU contention counters](../../images/vcenter-esxi-cpu-contention-counters-table.png)

## Lagging, not leading
- Averaged over all running VMs. By the time they are high, the problem is serious.
- Leading indicators are covered at cluster level.

## Consumption vs contention
- Physical vs virtual: ESXi metrics look at physical CPU; contention metrics look at vCPUs.
- Hyper-Threading and power management.
- Imbalance: many VMs on one host have different experiences.
- Limits, directly or through resource pools.
- CPU pinning (rare).
- Averaging hides peaks.

## Example
- Host total capacity 111 GHz. Demand reached 315%. Sum of VM CPU Usage reached 143%. Ready and Co-stop were high.
- Both exceed total capacity: Demand sums VM demand, and Usage includes Turbo above base frequency.
- Per-vCPU view: Ready of 128 s across 250 vCPUs = 514 ms per vCPU = about 2.5%.

## Misconceptions
- "Host Ready is the host waiting" → it is the VMs' Ready summed.
- "Host contention low, so all VMs are fine" → averages hide individual VMs.

## Metadata
```yaml
id: vsphere/technology/cpu/metrics/comparisons/host-contention-metrics
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
metric_class: contention
internal_derive:
- vsphere/architecture/provider-consumer
same_name: []
same_meaning: []
related:
- vsphere/technology/cpu/metrics/comparisons/vm-contention-metrics
- vsphere/technology/cpu/metrics/virtual-motherboard/ready
- vsphere/technology/cpu/metrics/virtual-motherboard/co-stop
images:
  - path: ../../images/vcenter-esxi-cpu-contention-counters-table.png
    product: [vsphere]
    object: [HostSystem]
    metric: ['ESXi CPU Ready', 'ESXi CPU Co-stop', 'ESXi CPU Latency']
    image_type: table
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: CPU > ESXi > Contention Metrics
corrections: []
review_notes: []
status: draft
```
