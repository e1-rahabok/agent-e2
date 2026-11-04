# ESXi CPU Utilization for Resources (legacy, avoid)

## Meaning
- 17 legacy metrics in the System group, named "CPU Utilization for Resources" in VCF Operations and rescpu.* in vSphere Client.
- "For resources" means from the resource scheduler's allocation buckets. A resource is any node in the allocation hierarchy that can have shares, reservations or limits, not only a VM.

## Replacements
| Legacy metric (VCF Operations) | vSphere Client | Use instead |
|---|---|---|
| CPU Active (1, 5, 15 min. average; 1, 5, 15 min. peak) | rescpu.actav1/5/15.latest, rescpu.actpk1/5/15.latest | CPU Demand |
| CPU Running (1, 5, 15 min. average; 1, 5, 15 min. peak) | rescpu.runav1/5/15.latest, rescpu.runpk1/5/15.latest | CPU Usage |
| CPU Throttled (1, 5, 15 min. average) | rescpu.maxLimited1/5/15.latest | Effective Limit |
| Group CPU Sample Count | rescpu.sampleCount.latest | - |
| Group CPU Sample Period | rescpu.samplePeriod.latest | - |

## Why
- CPU Active equals CPU Demand.
- VCF Operations averages 20-second and 1-minute values into its collection interval (default 5 minutes). A separate 1-minute metric adds nothing.
- The 15-minute version has no use case: roll up the 5-minute values.

## Traps
- "CPU Active is a different signal from Demand" → they are the same.

## Metadata
```yaml
id: vsphere/technology/cpu/metrics/host/cpu-utilization-for-resources
retriever_guide: metric-meaning
scope: vsphere
technology:
- cpu
pillar:
- capacity
- performance
product:
- vsphere
- vcf-operations
object:
- HostSystem
metric_class: consumption
internal_derive: []
same_name: []
same_meaning: []
related:
- vsphere/technology/cpu/metrics/host/demand
- vsphere/technology/cpu/metrics/host/usage
source:
  document: PART 3 - Counters.docx
  path: CPU > ESXi > Consumption Metrics > Metrics to Avoid > CPU Utilization for Resources
corrections: []
review_notes: []
status: draft
```
