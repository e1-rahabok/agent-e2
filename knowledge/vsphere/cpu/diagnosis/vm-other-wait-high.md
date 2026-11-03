# VM CPU Other Wait is high

## Checks, in order
1. Check Broadcom KB 85393: a known accounting issue inflates Other Wait and esxtop %VMWait.
2. Check for snapshots.
3. Check whether several VMs are affected. Find what they share.
4. Check Idle: when Run is low, Idle and Other Wait add up to about 100%.

## Actions
- vMotion the VM.
- Remove snapshots.
- Update ESXi (including physical device drivers), virtual hardware and VMware Tools (virtual device drivers) to the latest build.
- Still high: open a support request with Broadcom. Finding the root cause takes low-level debug data (stats vmx, schedtraces, vprobes).

## Traps
- "Other Wait means storage latency" → no correlation found with disk latency or outstanding IO.

## Metadata
```yaml
id: vsphere/cpu/diagnosis/vm-other-wait-high
retriever_guide: what-to-check
scope: vsphere
technology:
- cpu
pillar:
- performance
product:
- vsphere
- vcf-operations
object:
- VirtualMachine
internal_derive:
- vsphere/cpu/metrics/virtual-motherboard/other-wait
related:
- vsphere/cpu/metrics/virtual-motherboard/wait
- vsphere/cpu/metrics/virtual-motherboard/idle
source:
  document: PART 3 - Counters.docx
  path: CPU > VM (pp. 78-118) > Wait Metrics > Other Wait
corrections: []
review_notes: []
status: draft
```
