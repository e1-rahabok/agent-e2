# ESXi alerts

## Coverage and receivers
- An ESXi host is a provider: its alerts go to the infrastructure team. They are not relevant to the application team.
- Alerted: CPU contention and consumption, memory contention and consumption, dropped packets on the virtual and on the physical network.
- Every value (threshold, population, wait) is in the alert rows of [`catalog/thresholds-alerts.yaml`](../../../catalog/thresholds-alerts.yaml), shown with this file. This file says why each symptom is in the alert.
- Contention is read on the host's VMs, where the application feels it. Consumption is read on the host itself.
- Consumption alerts are red only: an orange consumption alert adds false positives; early warning belongs to the daily dashboard. A capacity alert means something took capacity away: a bug or a hardware availability issue ([`sp5-framework/outputs/alert-design`](../../../sp5-framework/outputs/alert-design.md), section Alerts by pillar).

## ESXi CPU contention
- Detects: a share of the host's VMs did not get the CPU time they asked for.
- Shared infrastructure looks at the population, not one VM. The share can mean hundreds of VMs, so the per-VM values are lower than in the VM alert ([`sp5-framework/outputs/alert-design`](../../../sp5-framework/outputs/alert-design.md), section Application team vs infrastructure team).
- VM Peak vCPU Ready, 20-second: the acute part ([`vsphere/technology/cpu/metrics/virtual-motherboard/ready`](../../technology/cpu/metrics/virtual-motherboard/ready.md)).
- VM CPU Contention, 5-minute: the sustained part ([`vsphere/technology/cpu/metrics/virtual-motherboard/contention`](../../technology/cpu/metrics/virtual-motherboard/contention.md)).
- Remediation: the VMs hit, by [`vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high`](../../technology/cpu/troubleshooting/vm-cpu-contention-high.md).

## ESXi CPU consumption
- Detects: the host runs out of CPU capacity.
- ESXi CPU Thread Utilization and ESXi CPU Core Utilization together. A provider is managed for capacity (space), not performance (speed): that is why CPU Usage is not used ([`vsphere/technology/cpu/metrics/host/utilization`](../../technology/cpu/metrics/host/utilization.md), [`vsphere/technology/cpu/metrics/host/core-utilization`](../../technology/cpu/metrics/host/core-utilization.md)).
- The values are low to leave room for HA failover. Ideally the HA buffer is added to the threshold dynamically. With too much noise, raise them up to the point where every core is busy; the HA room is then gone.
- A longer wait than a contention alert: fewer false positives.

## ESXi memory contention
- Detects: VMs on the host waited for memory pages.
- Detects it on a share of the host's VMs, as ESXi CPU contention: the VM's 20-second Peak Memory Contention (acute) and its 5-minute Memory Contention (sustained) together, with lower per-VM values than the VM alert because the share can mean hundreds of VMs.
- Not the host's own Memory Latency: it is a normalized average of its running VMs and hides the victim ([`vsphere/technology/memory/metrics/host/latency`](../../technology/memory/metrics/host/latency.md)).
- Remediation: the VMs hit, by [`vsphere/technology/memory/vm-memory-latency-high`](../../technology/memory/vm-memory-latency-high.md).

## ESXi memory consumption
- Detects: the host is short of memory and has started to reclaim it.
- ESXi Memory Ballooned and ESXi Memory Consumed together. Memory is a cache, so high Consumed alone does not mean slow; ballooning shows the host is reclaiming ([`vsphere/technology/memory/metrics/host/ballooned`](../../technology/memory/metrics/host/ballooned.md), [`vsphere/technology/memory/metrics/host/consumed`](../../technology/memory/metrics/host/consumed.md)).
- Balloon is an absolute size, not a share of consumed memory, so the impact means the same on every host size.
- Swapped and compressed are left out so the alert fires earlier: remediation, such as reducing demand, can take hours or days.
- A longer wait than a contention alert: fewer false positives, and the alert comes that much later.

## ESXi virtual network dropped packets
- Detects: transmitted packets dropped on the host's virtual network. Where each layer counts a drop: [`vsphere/technology/network/concepts/packet-drop-accounting`](../../technology/network/concepts/packet-drop-accounting.md).
- Red only, as on every network object, to avoid alert storms. TCP resends a dropped segment, so the data arrives in the end; the cost is time.

## ESXi physical network dropped packets
- Detects: transmitted packets dropped on the host's physical network adapters (vmnic) ([`vsphere/technology/network/metrics/host/packets-dropped`](../../technology/network/metrics/host/packets-dropped.md)).
- One alert per side, so the alert names where the drop happened.

## Not alerted
- Disk contention: not yet in the set.
- Network consumption: not yet in the set. A network has no clear 100%, so the ceiling is hard to set.
- Disk consumption: not alerted on the host; the daily check or the NOC screen serves better. Datastore space: [`vsphere/object-types/datastore/datastore-alerts`](../datastore/datastore-alerts.md).

## Misconceptions
- "Host CPU consumption alert on Usage" → providers are managed for capacity: Thread and Core Utilization.
- "Host red at 80% core utilization is too low" → the room is for HA failover.
- "Host consumed at 95% is a problem" → memory is a cache. The alert needs ballooning as well.
- "Wait for swapping before alerting" → swap and compression come late; reducing demand takes hours or days, so balloon is the trigger.
- "Balloon as a % of host memory" → an absolute size keeps the meaning the same across host sizes.
- "Read host contention from the host's own Latency" → it averages the running VMs and hides the victim; the alert reads the VMs.

## Metadata
```yaml
id: vsphere/object-types/esxi/esxi-alerts
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
- vsphere/technology/memory/metrics/virtual-motherboard/latency
- vsphere/technology/memory/metrics/host/ballooned
- vsphere/technology/memory/metrics/host/consumed
- vsphere/technology/network/metrics/host/packets-dropped
- vsphere/technology/network/concepts/packet-drop-accounting
related:
- vsphere/object-types/vm/vm-alerts
- vsphere/object-types/cluster/cluster-alerts
- vsphere/object-types/resource-pool/resource-pool-alerts
- vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high
- vsphere/technology/memory/vm-memory-latency-high
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Proactive Operations > Alert > CPU Alerts (Infrastructure Contention, Infrastructure Consumption); Memory Alerts (Infrastructure Contention, Infrastructure Consumption); Network Alerts > Contention Alerts'
corrections:
- 'Section ''ESXi memory contention'': the source gives the per-VM values without a population; written as the CPU alert, a share of the host''s VMs (above 25%), because the values sit below the VM alert''s for the same reason (Q145).'
review_notes:
- 'Section ''ESXi CPU contention'': no wait cycle stated; the threshold design rule gives 5 minutes for contention (sp5-framework/outputs/alert-design).'
status: draft
```
