# Memory alerts

## What to set
- Design memory alerts as a set: every object, and for each object both contention and consumption.
- Each alert below fires only when all its conditions hold.

## Why memory contention is hard to trace
- VM Memory Contention combines several causes, and the share of each cannot be separated.
- Example: a VM shows 51% memory contention. It can come from memory held back by a limit (5 MB), swapped (1 MB), compressed (2 MB), and a low shares setting, all at once.
- Metric: `vsphere/technology/memory/metrics/virtual-motherboard/latency` (VCF Operations VM Memory Contention).

## VM memory contention
- Red, all of:
  - VM Peak Memory Contention above 24%;
  - VM Memory Contention above 6%;
  - VM CPU Usage above 1 GHz.
- Orange, all of:
  - VM Peak Memory Contention above 12%;
  - VM Memory Contention above 3%;
  - VM CPU Usage above 1 GHz.
- CPU Usage in GHz filters idle VMs: a small percentage of a monster VM is still a sizable load.

## Infrastructure memory contention
- Objects: ESXi, resource pool, cluster.
- Red, all of:
  - Peak Memory Contention above 16%;
  - Memory Contention above 4%.
- Orange, all of:
  - Peak Memory Contention above 8%;
  - Memory Contention above 2%.
- Cluster: measured on its VMs, closer to the application; aggregating from the ESXi hosts is less accurate.
- Resource pool: does not work with nested resource pools.

## Memory consumption
- VM: no alert. A VM is a virtual motherboard; whether its memory is enough is a Guest OS question.
- Guest OS: no alert; the right value differs per application.
- ESXi, red, all of:
  - ESXi Memory Ballooned above 10 MB;
  - ESXi Memory Consumed above 95%.
- Orange: none; it would add false positives.
- Wait 10 minutes instead of 5 to reduce false positives; the alert comes later.
- Balloon is an absolute 10 MB, not a share of consumed memory, so the impact means the same on every host size.
- Swapped and compressed are left out so the alert fires earlier: remediation, such as reducing demand, can take hours or days.
- Cluster: fires when 50% of its hosts meet the condition. Most clusters have fewer than 20 hosts, and memory works as a cache, so high consumption does not mean slow.
- Metrics: `vsphere/technology/memory/metrics/host/ballooned`, `vsphere/technology/memory/metrics/host/consumed`.

## Misconceptions
- "Memory contention tells which cause dominates" → limit, swap, compression and shares mix; the split cannot be read from the metric.
- "Alert on VM memory usage" → a VM is a virtual motherboard; memory sufficiency is a Guest OS question with no common threshold.
- "Host consumed at 95% is a problem" → memory is a cache. The alert needs ballooning above 10 MB as well.
- "Wait for swapping before alerting" → swap and compression come late; reducing demand takes hours or days, so balloon is the trigger.
- "Balloon as a % of host memory" → 10 MB absolute keeps the meaning the same across host sizes.
- "Cluster memory alert at 25% of hosts, like CPU" → memory uses 50% of hosts.

## Metadata
```yaml
id: vsphere/technology/memory/configuration/memory-alerts
retriever_guide: what-to-set
scope: vsphere
technology:
- memory
pillar:
- performance
- capacity
product:
- vsphere
- vcf-operations
object:
- VirtualMachine
- HostSystem
- ClusterComputeResource
- ResourcePool
internal_derive:
- sp5-framework/outputs/alert-design
- vsphere/technology/memory/metrics/virtual-motherboard/latency
- vsphere/technology/memory/metrics/host/ballooned
- vsphere/technology/memory/metrics/host/consumed
related:
- vsphere/technology/memory/metrics/host/latency
- vsphere/technology/cpu/configuration/cpu-alerts
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Proactive Operations > Alert > Memory Alerts (Contention Alerts: VM Contention, Infrastructure Contention; Consumption Alerts: Infrastructure Consumption)'
corrections: []
review_notes:
- 'Section ''Memory consumption'': the design note says 10 minutes instead of 5; the red condition gives no duration. Written as a 10-minute wait. Q145.'
- 'To check: Section ''Memory consumption'': the object of the red condition, written as ESXi (Infrastructure Consumption, 50% of host members for the cluster); the source does not name it.'
- 'Section ''Why memory contention is hard to trace'': the example values (5 MB, 1 MB, 2 MB) cannot add up to 51%; read as an illustration of mixed causes. Q145.'
- 'Section ''Infrastructure memory contention'': the source does not state the instance of Peak Memory Contention for ESXi and cluster (worst VM or average). Q145.'
status: draft
```
