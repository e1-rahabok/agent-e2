# Resource pool alerts

## Coverage and receivers
- A resource pool is a provider: its alerts go to the infrastructure team.
- Alerted: CPU contention and memory contention, read on the pool's VMs. Same design as the ESXi contention alerts ([`vsphere/object-types/esxi/alerts/esxi-alerts`](../../esxi/alerts/esxi-alerts.md)).
- Every value (threshold, population, wait) is in the alert rows of [`catalog/thresholds-alerts.yaml`](../../../../catalog/thresholds-alerts.yaml), shown with this file.

## Resource pool CPU contention
- Detects: a share of the pool's VMs did not get the CPU time they asked for: a burst (VM Peak vCPU Ready) and sustained contention (VM CPU Contention) together.
- Does not work with nested resource pools. A pool inside a pool complicates operations ([`vsphere/object-types/resource-pool/configuration/resource-pool-design`](../configuration/resource-pool-design.md)).
- Remediation: the VMs hit, by [`vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high`](../../../technology/cpu/troubleshooting/vm-cpu-contention-high.md); then the pool's own limit, reservation and shares.

## Resource pool memory contention
- Detects: VMs in the pool waited for memory pages: the 20-second peak and the 5-minute value together.
- Does not work with nested resource pools.
- Remediation: the VMs hit, by [`vsphere/technology/memory/troubleshooting/vm-memory-latency-high`](../../../technology/memory/troubleshooting/vm-memory-latency-high.md).

## Not alerted, and why
- Consumption, all four resources: the use of a resource pool varies, so no consumption value fits.
- Disk and network contention: a resource pool does not divide storage or network.

## Misconceptions
- "Alert on a resource pool's CPU usage" → pool use varies; only contention is alerted.
- "The pool alert covers pools inside it" → the condition does not work with nested pools.

## Metadata
```yaml
id: vsphere/object-types/resource-pool/alerts/resource-pool-alerts
retriever_guide: what-to-set
scope: vsphere
technology:
- cpu
- memory
pillar:
- performance
product:
- vsphere
- vcf-operations
object:
- ResourcePool
internal_derive:
- sp5-framework/outputs/alert-design
- vsphere/object-types/esxi/alerts/esxi-alerts
related:
- vsphere/object-types/resource-pool/configuration/resource-pool-design
- vsphere/object-types/cluster/alerts/cluster-alerts
- vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high
- vsphere/technology/memory/troubleshooting/vm-memory-latency-high
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Proactive Operations > Alert > CPU Alerts (Infrastructure Contention, Infrastructure Consumption); Memory Alerts > Contention Alerts > Infrastructure Contention; Alerts Planning > Design (alert count table)'
corrections: []
review_notes:
- 'Section ''Resource pool memory contention'': the source does not state how the pool is read (worst VM, average, or a share of its VMs as in the CPU alert); the catalog tests the pool object. Q145.'
- 'To check: Section ''Resource pool CPU contention'', remediation: the pool''s own limit, reservation and shares as the second step is not in the source.'
- 'To check: Section ''Not alerted, and why'': the source''s count table marks disk and network contention N/A for the resource pool without a reason; the reason written (a pool does not divide storage or network) is not in the source.'
status: draft
```
