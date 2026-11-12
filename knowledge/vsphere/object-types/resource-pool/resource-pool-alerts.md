# Resource pool alerts

## Coverage and receivers
- A resource pool is a provider: its alerts go to the infrastructure team.
- Alerted: CPU contention and memory contention, read on a share of the pool's VMs. Same design as the ESXi contention alerts ([`vsphere/object-types/esxi/esxi-alerts`](../esxi/esxi-alerts.md)).
- Every value (threshold, population, wait) is in the alert rows of [`catalog/thresholds-alerts.yaml`](../../../catalog/thresholds-alerts.yaml), shown with this file.

## Resource pool CPU contention
- Detects: a share of the pool's VMs did not get the CPU time they asked for: a burst (VM Peak vCPU Ready) and sustained contention (VM CPU Contention) together.
- Does not work with nested resource pools. A pool inside a pool complicates operations ([`vsphere/object-types/resource-pool/resource-pool-design`](resource-pool-design.md)).
- Remediation: the VMs hit, by [`vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high`](../../technology/cpu/troubleshooting/vm-cpu-contention-high.md).

## Resource pool memory contention
- Detects: a share of the pool's VMs waited for memory pages: the 20-second peak (VM Peak Memory Contention) and the 5-minute value (VM Memory Contention) together.
- Does not work with nested resource pools.
- Remediation: the VMs hit, by [`vsphere/technology/memory/vm-memory-latency-high`](../../technology/memory/vm-memory-latency-high.md).

## Not alerted, and why
- Consumption, all four resources: the use of a resource pool varies, so no consumption value fits.
- Disk and network: a resource pool divides CPU and memory only.

## Misconceptions
- "Alert on a resource pool's CPU usage" → pool use varies; only contention is alerted.
- "The pool alert covers pools inside it" → the condition does not work with nested pools.

## Metadata
```yaml
id: vsphere/object-types/resource-pool/resource-pool-alerts
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
- vsphere/object-types/esxi/esxi-alerts
related:
- vsphere/object-types/resource-pool/resource-pool-design
- vsphere/object-types/cluster/cluster-alerts
- vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high
- vsphere/technology/memory/vm-memory-latency-high
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Proactive Operations > Alert > CPU Alerts (Infrastructure Contention, Infrastructure Consumption); Memory Alerts > Contention Alerts > Infrastructure Contention; Alerts Planning > Design (alert count table)'
corrections: []
review_notes: []
status: draft
```
