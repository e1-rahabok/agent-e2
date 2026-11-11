# ESXi CPU Usage

## Hyper-Threading
- When both threads of a core run, ESXi sees the core as fully busy.

| ESXi metric (core level) | Value |
|---|---|
| Usage (%) | 100% |
| Usage (MHz) | Reflects the Hyper-Threading benefit |
| Core Utilization | 100% |
| Thread Utilization | 100% |

## Cap
- ESXi CPU Usage is no longer capped at 100%, in vCenter or VCF Operations. On a busy host with Turbo it exceeds 100% of nominal capacity.
- Older releases capped it at 100%: older charts and the book's ESXi 7 examples show a flat 100%.
- Cause: an accounting decision error in ESXi. Known issue, documented in an official VMware KB.

## Same metric, two names
- vCenter shows the same ESXi CPU utilization as Consumed (%) and as Usage (%).

## Formula
```text
ESXi Usage = sum over physical cores (not sum of VMs + kernel)
```
- Physical perspective. Based on Core Utilization, adjusted for frequency and Hyper-Threading.
- Usage relates to Utilization as VM Usage relates to VM Run. A physical thread has no Overlap; System does not apply.
- Volatile: Turbo pushes it up, power saving pulls it down.
- High-load example: Usage (%) stayed above 100% because it is measured against base frequency. Less volatile than Thread Utilization: Hyper-Threading adds only 1.25x.
- Low-load example: Core Utilization 48%, Usage lower. The kernel clocked cores down to save power.

## Names and units
- Used (ms), Used (%), Usage (%), Usage (MHz). esxtop uses Used (%). vSphere Client uses the other 3.
- vSphere Client labels it Used in summary views and Usage in charts. Treat Used (MHz) = Usage (MHz).
- The book sees a use case only for Usage (MHz).
- Usage is added by vCenter. It does not exist at ESXi level.
- Summary value (Used CPU): summary.quickStats.overallCpuUsage. Likely a multi-minute average; it does not match the chart exactly.
- vSphere has no usable capacity concept for CPU: Free = Capacity - Used. Example: capacity 35.18 GHz, used 11.3 GHz.
- Consumed CPU (%) in the host list = Usage (%). The last value of the Usage chart is the table value.
- vSphere Host Client shows the same, with a breakdown per CPU package.

## Cap by tool
- vCenter: no longer capped (Broadcom KB 417702, KB 431027).
- VCF Operations: no longer capped since Aria Operations 8.18.

## Misconceptions
- "ESXi CPU Usage cannot exceed 100%" → the cap is removed. Above 100% means Turbo above nominal frequency.
- "A flat 100% line means the host is at its limit" → on older releases the value was capped.
- "ESXi Usage = sum of VM Usage + kernel" → it is summed over physical cores.
- "Usage below Core Utilization means an error" → power saving clocks cores down at low load.

## Metadata
```yaml
id: vsphere/technology/cpu/metrics/host/usage
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
- HostSystem
metric_class: consumption
internal_derive:
- vsphere/technology/cpu/concepts/hyper-threading
- vsphere/architecture/provider-consumer
same_name:
- vsphere/technology/cpu/metrics/virtual-motherboard/usage
same_meaning: []
related:
- vsphere/technology/cpu/metrics/host/core-utilization
- vsphere/technology/cpu/metrics/comparisons/consumption-metrics
- vsphere/technology/cpu/concepts/hyper-threading
- vsphere/technology/cpu/metrics/comparisons/host-consumption-metrics
- vsphere/technology/cpu/metrics/host/peak-core-usage
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity; CPU > ESXi > Used | Usage; Usage; Usage and 100%; Consumed
corrections:
- '2026-11-02: Hyper-Threading values (section: Hyper-Threading) are not in the uploaded document.'
- 'Section Cap: the cap is removed in vCenter (Broadcom KB 417702, KB 431027) and in VCF Operations since Aria Operations 8.18; the uploaded document shows the older capped behaviour.'
review_notes:
- 'Sections Formula, Names and units, Cap by tool: from CPU > ESXi.'
status: draft
```
