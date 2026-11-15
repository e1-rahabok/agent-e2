# ESXi CPU Idle (ms)

## Meaning
- Time the physical threads of the host spent idle. vSphere Web Services API 9.1 defines `cpu.idle` as total time that the CPU spent in an idle state, for VirtualMachine and HostSystem.
- Includes low activities, not only true idle.
- Considers CPU frequency, not simply whether the CPU is running.
- Relevance for operations: none. A kernel accounting value whose per-thread maximum changes with Hyper-Threading; read Thread Utilization for capacity and Core Utilization for how many cores already run work.

## Rollup with Hyper-Threading
- vCenter measures every 20,000 ms.
- With Hyper-Threading enabled, the maximum value for a completely idle thread is 10,000 ms.
- Why: 20,000 ms is set at core level. A core has 2 threads, each allocated 10,000 ms.
- ESXi CPU Used per thread does not follow the same split: a thread running alone shows Used up to 20,000 ms ([`vsphere/technology/cpu/concepts/hyper-threading`](../../concepts/hyper-threading.md), section Time base).

## Values
- Idle + non-idle = 100%.
- Example: an idle host with 64 threads showed thread values up to 9,998 ms, and about 640,000 ms in total.
- Without Hyper-Threading: no thread-level counter. The core-level value adds up to 20,000 ms.

## Misconceptions
- "Thread Idle of 10,000 ms means the thread was idle half the time" → with Hyper-Threading on, 10,000 ms is a fully idle thread: the 20,000 ms of a sample belong to the core, 10,000 ms of Idle to each thread. Read Thread Utilization for the busy share of a thread.

## Metadata
```yaml
id: vsphere/technology/cpu/metrics/host/idle
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
- vsphere/technology/cpu/concepts/hyper-threading
same_name:
- vsphere/technology/cpu/metrics/virtual-motherboard/idle
same_meaning: []
related:
- vsphere/technology/cpu/concepts/hyper-threading
source:
  document: Knowledge base; vSphere Web Services API 9.1 reference, CPU Counters
  path: The World of Metrics > Metrics Nuances > Complexity > Other Nuances; CPU > ESXi > Wait Metric > Idle; https://developer.broadcom.com/xapis/vsphere-web-services-api/9.1/cpu_counters.html, idle
corrections: []
review_notes: []
status: draft
```
