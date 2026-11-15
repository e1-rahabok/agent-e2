# CPU consumption metrics: VM and ESXi

## The choices
- VM: 5 consumption metrics: Run, Used, Usage, Usage (MHz), Demand.
- ESXi: 7 consumption metrics: Core Utilization, Utilization, Used, Usage, Usage (MHz), Consumed, Demand.
- Relevance for operations: by counter, VM Run and ESXi Thread Utilization for capacity and sizing; VM and ESXi Usage (MHz) for throughput, VM Used and Usage for chargeback; ESXi Demand in its VCF Operations form for capacity; VM Demand and the scheduler counters (Entitlement, Demand-to-entitlement ratio) none.

## Source of each
- ESXi provides Run (ms), Used (ms), Demand (MHz).
- vCenter adds Usage (MHz) and Usage (%).

## Reservation
- CPU reservation is on demand. It is not included in VM Run, Used, Demand or Usage, nor in the vCenter ESXi counters.
- One exception: ESXi CPU Demand in VCF Operations counts, per running VM, the higher of demand and reservation, and adds the kernel's reservation ([`vsphere/technology/cpu/metrics/host/demand`](../host/demand.md), section vCenter vs VCF Operations).

## VM consumption counters (vCenter)
| Counter | Unit | Source | Instance |
|---|---|---|---|
| Run | ms | ESXi | vCPU (VM = sum of vCPUs) |
| Used | ms | ESXi | vCPU, VM |
| Usage | MHz | vCenter | vCPU, VM |
| Usage | % | vCenter | VM |
| Demand | MHz | ESXi | VM |

- VM-level Used and Usage include System time and other charges not tied to a vCPU. Summing vCPUs leaves a small gap to the VM value.
- vCenter lists 9 VM CPU consumption counters, including Demand-to-entitlement ratio, Entitlement, System and VCPU Usage. Some exist for the kernel scheduler, not for operations. Their names follow the scheduler's view.
- Reservation and allocation are properties, not metrics.
- VM CPU reservation is set in MHz or GHz, not in vCPUs. Moving the VM to a host with a different frequency requires a manual adjustment.
![vCenter VM CPU consumption counters](../../images/vcenter-vm-cpu-consumption-counters-table.png)

## Misconceptions
- "A VM's CPU reservation shows in its Run, Used, Demand or Usage" → a CPU reservation acts only under contention and is in none of them. Only ESXi CPU Demand in VCF Operations counts reservations.
- "The per-vCPU values of Used or Usage add up to the VM value" → the VM value also holds System time and other charges not tied to a vCPU, so the VM value is higher.

## Metadata
```yaml
id: vsphere/technology/cpu/metrics/comparisons/consumption-metrics
retriever_guide: metric-meaning
scope: vsphere
technology:
- cpu
pillar:
- performance
- capacity
product:
- vsphere
object:
- VirtualMachine
- HostSystem
metric_class: consumption
internal_derive:
- vsphere/architecture/metric-sources
- sp5-framework/observability/metric-volume
same_name: []
same_meaning: []
related:
- vsphere/technology/cpu/metrics/virtual-motherboard/run
- vsphere/technology/cpu/metrics/virtual-motherboard/used
- vsphere/technology/cpu/metrics/virtual-motherboard/usage
- vsphere/technology/cpu/metrics/host/usage
- vsphere/technology/cpu/metrics/host/demand
- vsphere/technology/cpu/metrics/host/core-utilization
- vsphere/technology/cpu/concepts/run-time-vs-run-quality
- vsphere/technology/cpu/concepts/cpu-measurement-levels
- vsphere/technology/cpu/metrics/virtual-motherboard/demand
- vsphere/technology/cpu/metrics/virtual-motherboard/net-run
- vsphere/technology/cpu/metrics/virtual-motherboard/system
- vsphere/technology/cpu/metrics/virtual-motherboard/usage-disparity
- vsphere/technology/cpu/metrics/comparisons/vm-vs-esxi-ht-ramp-test
- vsphere/technology/cpu/metrics/comparisons/host-consumption-metrics
- vsphere/technology/cpu/concepts/hyper-threading
images:
  - path: ../../images/vcenter-vm-cpu-consumption-counters-table.png
    product: [vsphere]
    object: [VirtualMachine]
    metric: ['VM CPU Usage', 'VM CPU Usage (MHz)', 'VM CPU Demand', 'VM CPU Used', 'VM CPU Run']
    image_type: table
source:
  document: Knowledge base
  path: The World of Metrics > Metrics Nuances > Complexity > Other Nuances; CPU > VM > Consumption Metrics
corrections: []
review_notes: []
status: draft
```
