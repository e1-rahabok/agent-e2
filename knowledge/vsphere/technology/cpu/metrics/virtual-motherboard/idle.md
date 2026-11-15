# VM CPU Idle

## Meaning
- Time the Guest OS had the vCPU halted (HLT or MWAIT in its idle loop): ESXi de-schedules a halted vCPU, so it holds no physical thread.
- Part of Wait: Wait = Idle + Swap Wait + Other Wait ([`vsphere/technology/cpu/metrics/virtual-motherboard/wait`](wait.md), section Sub-metrics). vSphere Web Services API 9.1 defines `cpu.idle` as total time that the CPU spent in an idle state.
- Relevance for operations: sizing only: excluded from VM and Guest OS sizing (section Sizing). Not a performance signal.

## Mechanism
- The kernel cannot see why the Guest OS does no work: truly idle, or blocked by pending IO.
- It only sees that Windows or Linux is not doing work.
- Accounting issue on ESXi 7.0 Update 2 and later, fixed in ESXi 8.0 Update 3j: time when vCPUs halt is not always attributed to Idle, so an idle VM shows raised esxtop %VMWAIT and VM CPU Other Wait. Cosmetic, with no performance impact (Broadcom KB 338438, legacy 85393).

## Sizing
- Exclude Idle from VM sizing and from Guest OS sizing.
- Reason: the vCPU is not running, so its usage cannot be predicted.
- Fix IO and memory bottlenecks at the Guest OS level, with Windows and Linux metrics.

## Misconceptions
- "High Idle means the VM is waiting for IO" → the kernel cannot tell idle from IO-blocked.
- "Idle time should be sized for" → exclude it.
- "Idle is low on an idle VM, so the VM is busy" → on ESXi 7.0 Update 2 and later before 8.0 Update 3j, halted time can land in Other Wait instead of Idle (Broadcom KB 338438). Check Run: when Run is low, Idle and Other Wait add up to about 100%.

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
  document: Knowledge base; vSphere Web Services API 9.1 reference, CPU Counters; Broadcom KB 338438
  path: CPU > VM > Wait Metrics; https://developer.broadcom.com/xapis/vsphere-web-services-api/9.1/cpu_counters.html, idle; KB 338438 (Increased %VMWAIT for idle VMs after upgrading to ESXi 7.0 U2 or later)
corrections: []
review_notes: []
status: draft
```
