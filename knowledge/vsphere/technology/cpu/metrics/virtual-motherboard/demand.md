# VM CPU Demand

## Meaning
- What VM utilization would be had the VM experienced no issue, including Hyper-Threading.
- Like Usage, but assumes the VM does not share the physical core.
- An internal metric of the kernel resource scheduler. The book's advice: ignore it for operations.
- Unit: MHz. Source: ESXi. VM level only. vCenter counter: cpu.demand.average.
- VM realm, not Guest OS realm: the VMkernel computes it and sees physical threads. Its value is affected by Hyper-Threading (it removes the Hyper-Threading charge that Usage applies).
- Not a contention counter: it does not measure a vCPU being unable to run.

## Not unmet demand
- Demand is not what Usage would be if the VM got all the runtime it demanded.
- Test: a VM with an intentional limit had Co-stop 8.78%, Ready 15.91%, Wait 13.16%, Run 62.15% (total 100%).
- Its Demand equalled Usage.
- Reason: from the kernel's view the VM did not demand more. The limit is intentional.

## Behaviour
- No competition for resources: Demand and Usage are similar.
- Both threads of the core busy: Usage is 37.5% lower. Demand is not.
- Demand is averaged over a longer time. Peaks are shorter but wider. Usage can be higher than Demand at some points.
- Turbo Boost: Demand (MHz) and Usage (MHz) can exceed 100% of total capacity. Total capacity is based on base clock speed.
- Example: a 32-vCPU Hadoop worker, the only VM on a host with more than 32 cores. Demand and Usage were identical and exceeded total capacity several times.

## Demand vs Usage vs Contention
- Demand jumps and Usage drops: the VM demanded more CPU, and the extra demand was not met.
- Contention can exceed Demand - Usage.
- Example: Demand 25%, Usage 15%, Contention about 20%.
- Reason: Contention includes both frequency and Hyper-Threading. Demand - Usage includes only Hyper-Threading.

## Formula (VCF Operations)
```text
Demand (%) = Demand (MHz) / Total Capacity (MHz) × 100
```

## Misconceptions
- "Demand - Usage = unmet demand" → a limit leaves Demand equal to Usage. Check Ready.
- "Demand above 100% means add vCPUs" → Turbo raises Demand above 100%. See [`vsphere/technology/cpu/concepts/cpu-frequency`](../../concepts/cpu-frequency.md).
- "Usage above Demand is impossible" → Demand is smoothed over a longer window.

## Metadata
```yaml
id: vsphere/technology/cpu/metrics/virtual-motherboard/demand
retriever_guide: metric-meaning
scope: vsphere
technology:
- cpu
pillar:
- performance
- capacity
product:
- vsphere
- vcf-operations
object:
- VirtualMachine
layer:
- virtual-motherboard
metric_class: consumption
internal_derive:
- vsphere/technology/cpu/concepts/cpu-frequency
same_name:
- vsphere/technology/cpu/metrics/host/demand
same_meaning: []
related:
- vsphere/technology/cpu/metrics/virtual-motherboard/usage
- vsphere/technology/cpu/metrics/virtual-motherboard/contention
- vsphere/technology/cpu/metrics/virtual-motherboard/ready
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: CPU > VM > Consumption Metrics > Demand
corrections: []
review_notes: []
status: draft
```
