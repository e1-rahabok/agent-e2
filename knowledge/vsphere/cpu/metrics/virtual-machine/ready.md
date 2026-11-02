# VM CPU Ready

## Meaning
- Ready applies to a consumer (the VM). A physical core or thread is always ready, so Ready does not apply to ESXi.

## Values above 100%
- VM CPU Ready can exceed 100%. Many VM-level values in esxtop exceed 100%.
- Cause: summation, not average.

## Effect of limits
- A CPU limit impacts CPU Ready.

## Mechanism
- Ready: the vCPU demands runtime, and the kernel has no physical thread to run it.
- Caused by ESXi, not by the VM. Making the VM smaller does not reduce Ready.
- For the Guest OS, Ready is frozen time. Linux reports it as Steal Time. Windows does not account it.
- Ready does not register Hyper-Threading contention. A busy sibling thread does not put a vCPU into Ready.
- Ready on one vCPU can cause Co-stop on a sibling vCPU of the same VM.
- See `vsphere/cpu/concepts/vcpu-states`.

## Read against Run
- Ready 5% with Run 95%: low.
- Ready 2% with Run 10%: very high. Ready is 20% of Run.

## Units
- vCenter and VCF Operations Ready (ms) is not normalized by vCPU count. A 4-vCPU VM totals 80,000 ms of Run + Ready + Co-stop + Wait per 20-second sample.
- The % version is normalized by vCPU count. Prefer it.

## Traps
- "Host-level Ready is the host waiting for CPU" → Ready is a consumer metric. See `vsphere/foundations/provider-consumer`.
- "Ready 2% is always low" → read it against Run.
- "Reduce VM size to fix Ready" → that reduces Co-stop. Ready is caused by ESXi.

## Metadata
```yaml
id: vsphere/cpu/metrics/virtual-machine/ready
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
metric_class: contention
internal_derive:
- vsphere/foundations/provider-consumer
- vsphere/foundations/resource-management
- vsphere/cpu/concepts/vcpu-states
same_name: []
same_meaning: []
related:
- vsphere/cpu/metrics/virtual-machine/latency
- vsphere/cpu/concepts/guest-os-vs-vm-cpu
- vsphere/cpu/metrics/virtual-machine/run
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Other Nuances; CPU > Architecture (pp. 52-78) > State of a VM vCPU; State Across Time; State Across Multiple vCPU
corrections: []
review_notes:
- Sections Mechanism, Read against Run, Units, and the last 2 traps: from CPU > Architecture.
status: draft
```
