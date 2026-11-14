# VM vMotion metrics

## Metrics, in order of importance
| Metric | Type | Expected | Investigate |
|---|---|---|---|
| Downtime | Contention | Under 200 ms | Above 1 second |
| Stun time | Contention | Under 200 ms | Above 1 second |
| Copy bandwidth | Consumption | Stable, matching the capacity assigned to vMotion | Too low slows vMotion |

- Units for downtime and stun time: microseconds.
- Values vary per migration: watch both outliers and averages. Alarm on high values.
- Source: VCF Operations for logs (Log Insight) metrics vmw_esxi_vmdowntime and vmw_esxi_vmprecopystuntime. Plot the worst value: leading indicator.
- The stun time table shows the ESXi host, not the VM name.

## Downtime
- In the final phase the VM is quiesced on the source, the last memory changes are copied, and the VM resumes on the target.
- The guest pauses briefly: the largest guest impact (sudden latency rise). Depends on network, shared storage, host hardware, vSphere version and guest workload.

## Stun time
- A checkpoint stun: no guest instruction executes on the same vmx file.
- Caused by device reset, disk branching, disk promotion, snapshot take and snapshot consolidate.
- A compute vMotion copies the VM's state (memory, registers, network connections) to the target host; it creates no delta disk. Stun time is the switch-over: the VM is paused while its last memory pages and device state are copied, then resumes on the target (vSphere 9.1 documentation, Stages in vSphere vMotion).

## Misconceptions
- "Downtime value 150,000 is 150 seconds" → the unit is microseconds: 150 ms.

## Metadata
```yaml
id: vsphere/object-types/vm/vmotion
retriever_guide: metric-meaning
scope: vsphere
technology:
- system
- memory
- network
pillar:
- performance
- availability
product:
- vsphere
- vcf-operations
object:
- VirtualMachine
layer:
- virtual-motherboard
metric_class: contention
internal_derive:
- vsphere/architecture/overhead
- sp5-framework/performance/performance-kpi-design
same_name: []
same_meaning: []
related:
- sp5-framework/performance/performance-kpi-design
- vsphere/technology/storage/concepts/snapshot-impact
source:
  document: Knowledge base
  path: 'Consumer Objects > Performance: VM & Guest OS > vMotion'
corrections: []
review_notes: []
status: draft
```
