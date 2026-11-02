# ESXi CPU Idle (ms)

## Meaning
- Includes low activities, not only true idle.
- Considers CPU frequency, not simply whether the CPU is running.

## Rollup with Hyper-Threading
- vCenter measures every 20,000 ms.
- With Hyper-Threading enabled, the maximum value for a completely idle thread is 10,000 ms.
- Why: 20,000 ms is set at core level. A core has 2 threads, each allocated 10,000 ms.

## Values
- Idle + non-idle = 100%.
- With Hyper-Threading: idle thread maximum is 10,000 ms; per core 20,000 ms.
- Example: an idle host with 64 threads showed thread values up to 9,998 ms, and about 640,000 ms in total.
- Without Hyper-Threading: no thread-level counter. The core-level value adds up to 20,000 ms.

## Metadata
```yaml
id: vsphere/cpu/metrics/host/idle
retriever_guide: metric-meaning
scope: vsphere
technology:
- cpu
pillar:
- capacity
product:
- vsphere
object:
- HostSystem
metric_class: context
internal_derive:
- vsphere/cpu/concepts/hyper-threading
same_name: []
same_meaning: []
related:
- vsphere/cpu/concepts/esxi-thread-core-accounting
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Other Nuances; CPU > ESXi > Wait Metric > Idle
corrections: []
review_notes:
- metric_class set to context. Author to confirm.
- 'Section Values: from CPU > ESXi.'
status: draft
```
