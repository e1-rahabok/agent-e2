# ESXi CPU Core Utilization

## Meaning
- Reports 100% when one thread of the core runs.
- Also reports 100% when both threads run.
- To tell the two cases apart, check Thread Utilization.
- Definition: a core counts as utilized while at least one of its threads is unhalted (vSphere 9.1 documentation, esxtop CORE UTIL(%); vSphere Web Services API 9.1, cpu.coreUtilization: either or both logical CPUs).

## Reason
- The core does the work, not the thread. A core running one thread is fully busy.
- Both threads busy: Core Utilization stays at 100%, and each thread's Thread Utilization reads 100%. No counter adds the two threads of a core: [`vsphere/technology/cpu/concepts/hyper-threading`](../../concepts/hyper-threading.md), section Thread Utilization.
- Core Utilization is a static metric: it ignores frequency.
- It is not the capacity reading under Hyper-Threading: a core with one busy thread still has a free thread. For capacity (space) use Thread Utilization. See [`vsphere/technology/cpu/metrics/host/utilization`](utilization.md), section The capacity reading.
- Its use is speed: it shows how many cores already run work, where a second thread would share the core.
- With All-Core Turbo at 20%, Usage (%) = 120% when Core Utilization = 100%. See [`vsphere/technology/cpu/concepts/cpu-frequency`](../../concepts/cpu-frequency.md).

## Rollup
- ESXi Core Utilization = average of core values.
- vSphere Client lists threads (PCPUs) only when Hyper-Threading is on. Each thread shows the core value, duplicated.
- Usually higher than Thread Utilization. Without Hyper-Threading, equal to it.
- Core Utilization below 2 × Thread Utilization: some cores run 2 threads while others are idle.
- ESXi Usage (%) is based on Core Utilization, not Thread Utilization.

## Misconceptions
- "Core Utilization 100% means both threads are busy" → it is 100% with one busy thread too.
- "Core Utilization 70%, so 70% of the host's capacity is used" → for capacity count threads: Thread Utilization.

## Metadata
```yaml
id: vsphere/technology/cpu/metrics/host/core-utilization
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
- vsphere/technology/cpu/concepts/cpu-measurement-levels
same_name: []
same_meaning: []
related:
- vsphere/technology/cpu/metrics/host/usage
- vsphere/technology/cpu/concepts/cpu-frequency
- vsphere/technology/cpu/concepts/hyper-threading
- vsphere/technology/cpu/metrics/host/imbalance
source:
  document: Knowledge base; VMware vSphere 9.1 product documentation (PDF built 2026-11-02; the copyright page carries no revision number); vSphere Web Services API 9.1 reference, CPU Counters
  path: The World of Metrics > Metrics Nuances > Complexity > Other Nuances; CPU > Architecture > ESXi ≠ VM + Kernel; Impacts on ESXi; CPU > ESXi > Thread Utilization; vSphere Monitoring and Performance > resxtop and esxtop > CPU Panel, CORE UTIL(%) (p. 2155); https://developer.broadcom.com/xapis/vsphere-web-services-api/9.1/cpu_counters.html, coreUtilization
corrections: []
review_notes:
- Sections Reason: from CPU > Architecture.
- 'Section Rollup: from CPU > ESXi.'
status: draft
```
