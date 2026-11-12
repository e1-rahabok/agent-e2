# CPU alerts

## What to set
- Design CPU alerts as a set: every object, and for each object both contention and consumption.
- Use the contention and consumption alerts together. For a consumer, capacity can be added at a moment's notice; adding vCPUs while the VM has contention makes performance worse.
- Each alert below fires only when all its conditions hold.

## VM CPU contention
- Red, all of:
  - VM Peak vCPU Ready above 32%;
  - VM CPU Ready above 8%;
  - VM CPU Contention above 8%;
  - VM CPU Usage above 1 GHz.
- Orange, all of:
  - VM Peak vCPU Ready above 32%;
  - VM CPU Ready above 4%;
  - VM CPU Contention above 8%;
  - VM CPU Usage above 1 GHz.
- CPU Usage is in GHz, not %: a small percentage of a monster VM is still a sizable load.
- The application team gets red only, at a higher CPU Ready than the infrastructure team (8% against 6%), so infrastructure acts first ([`sp5-framework/outputs/alert-design`](../../../../sp5-framework/outputs/alert-design.md)).
- Remediation: open [`vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high`](../troubleshooting/vm-cpu-contention-high.md).

## Infrastructure CPU contention
- Objects: ESXi, resource pool, cluster. Not Datacenter: its clusters can serve different purposes.
- Shared infrastructure looks at the population. 25% of the VM population is the overall threshold; because that can be hundreds of VMs, the per-VM threshold is lower than for the VM alert.
- Red, all of:
  - Peak vCPU Ready above 24%;
  - CPU Contention above 6%.
- Orange, all of:
  - Peak vCPU Ready above 12%;
  - CPU Contention above 3%.
- Cluster: measured on its VMs, which is closer to the application. Aggregating from the ESXi hosts is less accurate.
- Resource pool: the condition does not work with nested resource pools. A pool inside a pool complicates operations.

## VM CPU consumption
- Goal: high utilization can slow the business, above all online workloads where users expect a real-time response.
- Red, for 15 minutes, all of:
  - VM CPU Net Run above 95%;
  - Guest OS CPU Queue above 4.
- Orange: none; it would add false positives.
- 15 minutes instead of 5 reduces false positives, and delays the alert by 15 minutes.
- The Guest OS CPU Queue shows a real bottleneck, not a VM running at full speed by design.
- Remediation:
  1. Find the nature of the application. A batch job can hold Net Run above 95% for the whole run; if it finishes within its window, that is healthy. Exclude it from the alert.
  2. Ask the application team which application or transaction metrics show queueing and latency. If they match the infrastructure numbers, add vCPUs, keeping the VM NUMA-aligned ([`vsphere/technology/cpu/configuration/numa-settings`](numa-settings.md)).

## Infrastructure CPU consumption
- Red, for 10 minutes, all of:
  - ESXi CPU Thread Utilization above 40%;
  - ESXi CPU Core Utilization above 80%.
- Orange: none; it would add false positives.
- A provider is managed for capacity (space), not performance (speed). That is why CPU Usage is not used.
- The thresholds are low to leave room for HA. Ideally the HA buffer is added to the threshold dynamically. With too much noise, raise them to 50% and 100%.
- Not set for resource pools: their use varies.
- Cluster: fires when more than 25% of its ESXi hosts meet the condition.
- Metrics: [`vsphere/technology/cpu/metrics/host/utilization`](../metrics/host/utilization.md), [`vsphere/technology/cpu/metrics/host/core-utilization`](../metrics/host/core-utilization.md).

## Misconceptions
- "High VM CPU usage: add vCPUs" → check contention first; adding vCPUs to a VM with contention makes it worse.
- "CPU Ready above 8% alone is red" → the VM alert also requires Peak vCPU Ready, CPU Contention and at least 1 GHz of usage.
- "Use CPU Usage % to filter idle VMs" → a small % of a monster VM is a large load; use GHz.
- "Net Run at 95% is a problem" → a batch job runs at full speed by design. The Guest OS CPU Queue above 4 shows the bottleneck.
- "Cluster CPU contention from host averages" → measure the cluster's VMs; host aggregation is less accurate.
- "Host CPU consumption alert on Usage" → providers are managed for capacity: Thread and Core Utilization.
- "Host red at 80% core utilization is too low" → the room is for HA failover.

## Metadata
```yaml
id: vsphere/technology/cpu/configuration/cpu-alerts
retriever_guide: what-to-set
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
- HostSystem
- ClusterComputeResource
- ResourcePool
internal_derive:
- sp5-framework/outputs/alert-design
- vsphere/technology/cpu/metrics/virtual-motherboard/ready
- vsphere/technology/cpu/metrics/virtual-motherboard/contention
- vsphere/technology/cpu/metrics/virtual-motherboard/usage
- vsphere/technology/cpu/metrics/virtual-motherboard/net-run
- vsphere/technology/cpu/metrics/host/utilization
- vsphere/technology/cpu/metrics/host/core-utilization
- guest-os/cpu/metrics/run-queue
related:
- vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high
- vsphere/technology/cpu/configuration/numa-settings
- guest-os/system/configuration/guest-os-alerts
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Proactive Operations > Alert > CPU Alerts (Contention Alerts: VM Contention, Infrastructure Contention; Consumption Alerts: VM Consumption, Infrastructure Consumption)'
corrections: []
review_notes:
- 'Section ''VM CPU contention'': orange keeps Peak vCPU Ready above 32% and CPU Contention above 8%, the same as red; only CPU Ready changes (4% vs 8%). Q144.'
- 'Section ''VM CPU contention'' and ''Infrastructure CPU contention'': the source says see the diagram at the start of the CPU Alert section for remediation; no diagram is in the document. Linked to the knowledge-base flow vm-cpu-contention-high instead. Q144.'
- 'Section ''Infrastructure CPU contention'': no wait cycle stated; the threshold design rule gives 5 minutes for contention (sp5-framework/outputs/alert-design).'
- 'Section ''VM CPU contention'': the 32% Peak vCPU Ready is 4x the 8% CPU Ready, the acute-vs-sustained guide; this reading is not stated in the source.'
status: draft
```
