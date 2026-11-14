# VM CPU Other Wait

## Meaning
- Time a vCPU is blocked by something other than memory: disk IO, network IO, vMotion, snapshots.
- Example: the VMM layer tries to do something and is blocked.
- Part of Wait. Contention for the guest: the guest experiences a freeze.
- Called VM Wait in parts of VCF Operations and in older documents. Earlier named IO Wait by mistake.

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
- An accounting issue wrongly inflates Other Wait and esxtop %VMWait (Broadcom KB 85393).

## Misconceptions
- "Other Wait means storage latency" → no correlation was found with disk latency or outstanding IO.
- "Other Wait correlates with Ready" → no correlation found.
- "High Other Wait is always real" → check KB 85393 first.

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
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: CPU > VM > Wait Metrics > Other Wait
corrections: []
review_notes:
- 'To check: KB 85393 (legacy id) cited by the book, not read (https://knowledge.broadcom.com/external/article?legacyId=85393).'
- 'Section ''Meaning'': the book uses VM Wait and Other Wait for the same metric. Proposed as synonyms in glossary.'
status: draft
```
