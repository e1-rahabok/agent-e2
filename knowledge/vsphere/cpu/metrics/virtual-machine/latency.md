# VM CPU Latency

## Meaning
- Does not always indicate a performance problem.
- Affected by CPU frequency, which goes up or down.
- At lower frequency the VM runs slower but is not waiting to be served. Equivalent to running on an older CPU.

## Contrast with other Latency metrics
- Memory Latency and Disk Latency do indicate a performance problem. They are primary counters for how well the VM is served.

## Contrast with Linux Steal Time
- Linux Steal Time includes only CPU Ready.
- VM CPU Latency includes many factors, including CPU frequency.
- Pattern: same purpose, different formula.

## Hyper-Threading
- Ready, Co-stop and Wait do not register Hyper-Threading contention. Contention for shared core resources happens in hardware, not in the scheduler.
- CPU Latency is the counter for throughput lost when the sibling thread runs.
- Hyper-Threading changes CPU Latency by 0% to 37.5%.

## Traps
- "CPU Latency rose, so the VM has CPU contention" → check whether CPU frequency changed. Waiting shows in unmet-demand metrics (Ready, Co-Stop). See `vsphere/foundations/visibility-layers`, area D.
- "Steal Time inside Linux equals VM CPU Latency" → different formulas.

## Metadata
```yaml
id: vsphere/cpu/metrics/virtual-machine/latency
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
- vsphere/foundations/visibility-layers
- vsphere/cpu/concepts/vcpu-states
- vsphere/cpu/concepts/cpu-efficiency
same_name:
- vsphere/memory/metrics/virtual-machine/latency
- vsphere/storage/metrics/virtual-machine/disk-latency
same_meaning: []
related:
- vsphere/cpu/metrics/virtual-machine/ready
- vsphere/cpu/concepts/guest-os-vs-vm-cpu
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity; CPU > Architecture (pp. 52-78) > Architecture intro; State of a VM vCPU
corrections: []
review_notes:
- Sections Hyper-Threading: from CPU > Architecture.
status: draft
```
