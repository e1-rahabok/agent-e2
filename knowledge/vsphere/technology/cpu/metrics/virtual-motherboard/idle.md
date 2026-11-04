# VM CPU Idle

## Meaning
- Time the vCPU was scheduled but had nothing to run.
- Part of Wait.

## Mechanism
- The kernel cannot see why the Guest OS does no work: truly idle, or blocked by pending IO.
- It only sees that Windows or Linux is not doing work.

## Sizing
- Exclude Idle from VM sizing and from Guest OS sizing.
- Reason: the vCPU is not running, so its usage cannot be predicted.
- Fix IO and memory bottlenecks at the Guest OS level, with Windows and Linux metrics.

## Traps
- "High Idle means the VM is waiting for IO" → the kernel cannot tell idle from IO-blocked.
- "Idle time should be sized for" → exclude it.

## Metadata
```yaml
id: vsphere/technology/cpu/metrics/virtual-motherboard/idle
retriever_guide: metric-meaning
scope: vsphere
technology:
- cpu
pillar:
- capacity
- performance
product:
- vsphere
object:
- VirtualMachine
layer:
- virtual-motherboard
metric_class: context
internal_derive:
- vsphere/technology/cpu/metrics/virtual-motherboard/wait
same_name:
- vsphere/technology/cpu/metrics/host/idle
same_meaning: []
related:
- vsphere/technology/cpu/metrics/virtual-motherboard/wait
- vsphere/technology/cpu/metrics/virtual-motherboard/other-wait
- vsphere/technology/cpu/concepts/idle-and-unused-vcpus
source:
  document: PART 3 - Counters.docx
  path: CPU > VM (pp. 78-118) > Wait Metrics
corrections: []
review_notes:
- metric_class set to context, matching vsphere/technology/cpu/metrics/host/idle. Author to confirm.
status: draft
```
