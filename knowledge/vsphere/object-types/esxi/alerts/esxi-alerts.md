# ESXi alerts

## Coverage and receivers
- An ESXi host is a provider: its alerts go to the infrastructure team. They are not relevant to the application team.
- Alerted: CPU contention and consumption, memory contention and consumption, dropped packets on the virtual and on the physical network.
- Every value (threshold, population, wait) is in the alert rows of [`catalog/thresholds-alerts.yaml`](../../../../catalog/thresholds-alerts.yaml), shown with this file. This file says why each symptom is in the alert.
- Contention is read on the host's VMs, where the application feels it. Consumption is read on the host itself.
- Consumption alerts are red only: an orange consumption alert adds false positives; early warning belongs to the daily dashboard. A capacity alert means something took capacity away: a bug or a hardware availability issue ([`sp5-framework/outputs/alert-design`](../../../../sp5-framework/outputs/alert-design.md), section What to alert, by pillar).

## ESXi CPU contention
- Detects: a share of the host's VMs did not get the CPU time they asked for.
- Shared infrastructure looks at the population, not one VM. The share can mean hundreds of VMs, so the per-VM values are lower than in the VM alert ([`sp5-framework/outputs/alert-design`](../../../../sp5-framework/outputs/alert-design.md), section Application team vs infrastructure team).
- VM Peak vCPU Ready, 20-second: the acute part ([`vsphere/technology/cpu/metrics/virtual-motherboard/ready`](../../../technology/cpu/metrics/virtual-motherboard/ready.md)).
- VM CPU Contention, 5-minute: the sustained part ([`vsphere/technology/cpu/metrics/virtual-motherboard/contention`](../../../technology/cpu/metrics/virtual-motherboard/contention.md)).
- Remediation: the VMs hit, by [`vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high`](../../../technology/cpu/troubleshooting/vm-cpu-contention-high.md).

## ESXi CPU consumption
- Detects: the host runs out of CPU capacity.
- ESXi CPU Thread Utilization and ESXi CPU Core Utilization together. A provider is managed for capacity (space), not performance (speed): that is why CPU Usage is not used ([`vsphere/technology/cpu/metrics/host/utilization`](../../../technology/cpu/metrics/host/utilization.md), [`vsphere/technology/cpu/metrics/host/core-utilization`](../../../technology/cpu/metrics/host/core-utilization.md)).
- The values are low to leave room for HA failover. Ideally the HA buffer is added to the threshold dynamically. With too much noise, raise them up to the point where every core is busy; the HA room is then gone.
- A longer wait than a contention alert: fewer false positives.

## ESXi memory contention
- Detects: VMs on the host waited for memory pages.
- Same design as ESXi CPU contention: the 20-second Peak Memory Contention (acute) and the 5-minute Memory Contention (sustained) together, with lower values than the VM alert.
- The host's own Memory Latency is a normalized average of its running VMs and hides the victim ([`vsphere/technology/memory/metrics/host/latency`](../../../technology/memory/metrics/host/latency.md)).
- Remediation: the VMs hit, by [`vsphere/technology/memory/troubleshooting/vm-memory-latency-high`](../../../technology/memory/troubleshooting/vm-memory-latency-high.md).

## ESXi memory consumption
- Detects: the host is short of memory and has started to reclaim it.
- ESXi Memory Ballooned and ESXi Memory Consumed together. Memory is a cache, so high Consumed alone does not mean slow; ballooning shows the host is reclaiming ([`vsphere/technology/memory/metrics/host/ballooned`](../../../technology/memory/metrics/host/ballooned.md), [`vsphere/technology/memory/metrics/host/consumed`](../../../technology/memory/metrics/host/consumed.md)).
- Balloon is an absolute size, not a share of consumed memory, so the impact means the same on every host size.
- Swapped and compressed are left out so the alert fires earlier: remediation, such as reducing demand, can take hours or days.
- A longer wait than a contention alert: fewer false positives, and the alert comes that much later.

## ESXi virtual network dropped packets
- Detects: transmitted packets dropped on the host's virtual network: the virtual switch ports of its VMs and VMkernel adapters. Where a drop is counted: [`vsphere/technology/network/concepts/packet-drop-accounting`](../../../technology/network/concepts/packet-drop-accounting.md).
- Red only, as on every network object, to avoid alert storms. Dropped packets are usually retransmitted, so users rarely feel a problem.

## ESXi physical network dropped packets
- Detects: transmitted packets dropped on the host's physical network adapters (vmnic) ([`vsphere/technology/network/metrics/host/packets-dropped`](../../../technology/network/metrics/host/packets-dropped.md)).
- A separate alert from the virtual network: the cause and the team that fixes it differ (the virtual switch and its VMs, against the uplinks and the physical network).

## Not alerted, and why
- Disk contention: not yet in the set.
- Network consumption: not yet in the set. A network has no clear 100%, so the ceiling is hard to set.
- Disk consumption: not alerted on the host; the daily check or the NOC screen serves better. Datastore space: [`vsphere/object-types/datastore/alerts/datastore-alerts`](../../datastore/alerts/datastore-alerts.md).

## Misconceptions
- "Host CPU consumption alert on Usage" → providers are managed for capacity: Thread and Core Utilization.
- "Host red at 80% core utilization is too low" → the room is for HA failover.
- "Host consumed at 95% is a problem" → memory is a cache. The alert needs ballooning as well.
- "Wait for swapping before alerting" → swap and compression come late; reducing demand takes hours or days, so balloon is the trigger.
- "Balloon as a % of host memory" → an absolute size keeps the meaning the same across host sizes.
- "Read host contention from the host's own Latency" → it averages the running VMs and hides the victim; the alert reads the VMs.

## Metadata
```yaml
id: vsphere/object-types/esxi/alerts/esxi-alerts
retriever_guide: what-to-set
scope: vsphere
technology:
- cpu
- memory
- network
pillar:
- performance
- capacity
product:
- vsphere
- vcf-operations
object:
- HostSystem
internal_derive:
- sp5-framework/outputs/alert-design
- vsphere/technology/cpu/metrics/virtual-motherboard/ready
- vsphere/technology/cpu/metrics/virtual-motherboard/contention
- vsphere/technology/cpu/metrics/host/utilization
- vsphere/technology/cpu/metrics/host/core-utilization
- vsphere/technology/memory/metrics/host/latency
- vsphere/technology/memory/metrics/host/ballooned
- vsphere/technology/memory/metrics/host/consumed
- vsphere/technology/network/metrics/host/packets-dropped
- vsphere/technology/network/concepts/packet-drop-accounting
related:
- vsphere/object-types/vm/alerts/vm-alerts
- vsphere/object-types/cluster/alerts/cluster-alerts
- vsphere/object-types/resource-pool/alerts/resource-pool-alerts
- vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high
- vsphere/technology/memory/troubleshooting/vm-memory-latency-high
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Proactive Operations > Alert > CPU Alerts (Infrastructure Contention, Infrastructure Consumption); Memory Alerts (Infrastructure Contention, Infrastructure Consumption); Network Alerts > Contention Alerts'
corrections: []
review_notes:
- 'Section ''ESXi CPU contention'': no wait cycle stated; the threshold design rule gives 5 minutes for contention (sp5-framework/outputs/alert-design).'
- 'Section ''ESXi memory contention'': the source does not state how the host is read (worst VM, average, or a share of its VMs as in the CPU alert); the catalog tests the host object. Q145.'
- 'Section ''ESXi memory consumption'': the design note says 10 minutes instead of 5; the red condition gives no duration. Written as a 10-minute wait. Q145.'
- 'To check: Section ''ESXi memory consumption'': the object of the red condition, written as ESXi (Infrastructure Consumption, 50% of host members for the cluster); the source does not name it.'
- 'To check: Sections ''ESXi virtual network dropped packets'' and ''ESXi physical network dropped packets'': what each side covers (VM and VMkernel ports; vmnic uplinks) and the reason for two alerts are not in the source, which lists the two conditions and counts 2 alerts.'
- 'To check: Section ''ESXi memory contention'': the line on the host''s own Memory Latency is from the metric file vsphere/technology/memory/metrics/host/latency, not from the alert chapter.'
status: draft
```
