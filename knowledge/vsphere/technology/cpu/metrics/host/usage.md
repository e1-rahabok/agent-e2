# ESXi CPU Usage

## Meaning
- Busy time per physical core, scaled by frequency against the base clock: a core with one or two busy threads counts once, and 100% is the base clock.
- Broadcom KB 431027: the host `cpu.usage` counter reflects physical core saturation, not logical thread availability, and Turbo raises it; for capacity planning the KB names `cpu.utilization` (Thread Utilization).
- Relevance for operations: performance and throughput reporting, in Usage (MHz) (section Names and units). Not capacity, because Turbo and power saving move it: read Thread Utilization ([`vsphere/technology/cpu/metrics/host/utilization`](utilization.md), section The capacity reading).

## Hyper-Threading
- When both threads of a core run, ESXi sees the core as fully busy.

| ESXi metric (core level) | Value, both threads busy, nominal clock |
|---|---|
| Usage (%) | 100% |
| Usage (MHz) | The core's clock speed: no Hyper-Threading gain |
| Core Utilization | 100% |
| Thread Utilization | 100% on each thread |

- No Hyper-Threading gain: ESXi CPU Used gives each thread of a busy pair half the core; the 1.25x is in VM CPU Used only ([`vsphere/technology/cpu/concepts/hyper-threading`](../../concepts/hyper-threading.md), section Hyper-Threading accounting: VM CPU Used and ESXi CPU Used).

## Cap
- ESXi CPU Usage is no longer capped at 100%, in vCenter or VCF Operations. On a busy host with Turbo it exceeds 100% of nominal capacity.
- Older releases capped it at 100%: older charts and ESXi 7 examples show a flat 100%.
- vCenter: from vSphere 8.0 Update 3 the vSphere Client shows the actual Consumed CPU (%), measured against base frequency, instead of capping it at 100% (Broadcom KB 417702). esxtop reports scheduled time and stays below 100% on the same host.
- VCF Operations: no longer capped since Aria Operations 8.18.

## Same metric, two names
- vCenter shows the same ESXi CPU utilization as Consumed (%) and as Usage (%).

## Formula
```text
ESXi Usage = sum over physical cores (not sum of VMs + kernel)
```
- Physical perspective. Based on Core Utilization, adjusted for frequency. Hyper-Threading adds no gain: a core with one or two busy threads counts once.
- Usage relates to Utilization as VM Usage relates to VM Run. A physical thread has no Overlap; System does not apply.
- Volatile: Turbo pushes it up, power saving pulls it down.
- High-load example: Usage (%) stayed above 100% because it is measured against base frequency. Less volatile than Thread Utilization: a second thread on a busy core doubles that core's Thread Utilization and leaves its Usage unchanged.
- Low-load example: Core Utilization 48%, Usage lower. The kernel clocked cores down to save power.

## Names and units
- Used (ms), Used (%), Usage (%), Usage (MHz). esxtop uses Used (%). vSphere Client uses the other 3.
- vSphere Client labels it Used in summary views and Usage in charts. Treat Used (MHz) = Usage (MHz).
- Of Usage (%) and Usage (MHz), only Usage (MHz) has an operational use case.
- The legacy CPU Running metrics (rescpu.runav, rescpu.runpk) duplicate Usage; avoid them ([`vsphere/technology/cpu/metrics/host/cpu-utilization-for-resources`](cpu-utilization-for-resources.md)).
- esxtop has no Usage field; the vSphere Host Client (ESXi) shows Usage, and the API has cpu.usagemhz on HostSystem.
- Summary value (Used CPU): summary.quickStats.overallCpuUsage. Likely a multi-minute average; it does not match the chart exactly.
- vSphere has no usable capacity concept for CPU: Free = Capacity - Used. Example: capacity 35.18 GHz, used 11.3 GHz.
- Consumed CPU (%) in the host list = Usage (%). The last value of the Usage chart is the table value.
- vSphere Host Client shows the same, with a breakdown per CPU package.

## Misconceptions
- "ESXi CPU Usage cannot exceed 100%" → the cap is removed. Above 100% means Turbo above nominal frequency.
- "A flat 100% line means the host is at its limit" → before vSphere 8.0 Update 3 the value was capped at 100% (Broadcom KB 417702). Check Core Utilization, Thread Utilization and contention.
- "ESXi Usage = sum of VM Usage + kernel" → it is summed over physical cores.
- "Usage below Core Utilization means an error" → power saving clocks cores down at low load.
- "ESXi CPU Usage of a core with both threads busy is 125%" → ESXi CPU Used gives each thread of the pair half the core; the 1.25x is in VM CPU Used and VM CPU Usage only.

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
- vsphere/technology/cpu/metrics/host/cpu-utilization-for-resources
source:
  document: Knowledge base; VMware vSphere 9.1 product documentation (PDF built 2026-11-02; the copyright page carries no revision number); Broadcom KB 335065; Broadcom KB 417702; Broadcom KB 431027
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity; CPU > ESXi > Used | Usage; Usage; Usage and 100%; Consumed; vSphere Monitoring and Performance > resxtop and esxtop > CPU Panel, PCPU USED(%) (p. 2153); KB 335065, Cause; KB 417702 (ESXi host reporting over 100% CPU usage), Cause; KB 431027 (ESXi host CPU usage appears high in vCenter default charts due to Turbo Boost and Hyperthreading counter behavior), Cause and Resolution
corrections: []
review_notes: []
status: draft
```
