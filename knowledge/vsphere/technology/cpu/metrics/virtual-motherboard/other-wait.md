# VM CPU Other Wait

## Meaning
- Time a vCPU is blocked by something other than memory: disk IO, network IO, vMotion, snapshots.
- Example: the VMM layer tries to do something and is blocked.
- Part of Wait. Contention for the guest: the guest experiences a freeze.
- Called VM Wait in parts of VCF Operations and in older documents. Earlier named IO Wait by mistake.
- Relevance for operations: performance troubleshooting only, when a VM is slow and the other CPU counters do not explain it ([`vsphere/technology/cpu/troubleshooting/vm-other-wait-high`](../../troubleshooting/vm-other-wait-high.md)). Not in the VM KPI, because idle VMs can show it without waiting (section Known issue).

## Formula (VCF Operations)
```text
Other Wait = Wait - Idle - Swap Wait
```

## Mechanism
- The hypervisor scheduled the vCPU, but it is blocked.
- Many reasons exist. Pinpointing one requires low-level debug data: stats vmx, schedtraces, custom vprobes.
- Snapshot is a common reason.
- Include Other Wait in Guest OS CPU sizing: it is runtime the guest demanded.

## Observations
- 4,000 production VMs: the value is not low.
- No correlation with Ready or Co-stop.
- No correlation with disk latency or outstanding IO.
- A VM with sustained Other Wait around 15% had low Run, Usage and Demand. The only correlated metric was Idle: the two add up to about 100% when Run is low.

## Known issue
- Broadcom KB 338438 (legacy 85393): on ESXi 7.0 Update 2 and later, time when vCPUs halt is not always attributed to Idle, so idle VMs show raised esxtop %VMWAIT. VCF Operations shows it as the wait that excludes Idle and Swap Wait (Other Wait), and its alert on a long wait for IO can fire.
- The KB calls it a cosmetic accounting issue with no performance impact. Fixed in ESXi 8.0 Update 3j.

## Misconceptions
- "Other Wait means storage latency" → no correlation was found with disk latency or outstanding IO.
- "Other Wait correlates with Ready" → no correlation found.
- "High Other Wait is always real" → on ESXi 7.0 Update 2 and later before 8.0 Update 3j, idle VMs show it by accounting (Broadcom KB 338438). Check the ESXi build and whether Run is low.

## Metadata
```yaml
id: vsphere/technology/cpu/metrics/virtual-motherboard/other-wait
retriever_guide: metric-meaning
scope: vsphere
technology:
- cpu
pillar:
- performance
product:
- vsphere
object:
- VirtualMachine
layer:
- virtual-motherboard
metric_class: contention
internal_derive:
- vsphere/technology/cpu/metrics/virtual-motherboard/wait
same_name: []
same_meaning: []
related:
- vsphere/technology/cpu/metrics/virtual-motherboard/wait
- vsphere/technology/cpu/metrics/virtual-motherboard/idle
- vsphere/technology/cpu/metrics/virtual-motherboard/swap-wait
- vsphere/technology/cpu/troubleshooting/vm-other-wait-high
- vsphere/technology/cpu/metrics/comparisons/vm-contention-metrics
source:
  document: Knowledge base; Broadcom KB 338438
  path: CPU > VM > Wait Metrics > Other Wait; KB 338438 (legacy 85393, Increased %VMWAIT for idle VMs after upgrading to ESXi 7.0 U2 or later)
corrections: []
review_notes: []
status: draft
```
