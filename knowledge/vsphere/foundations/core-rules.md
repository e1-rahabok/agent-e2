# Core rules of vSphere metrics

The rules that most often decide a Level 400 answer. Each rule undoes a reading that public Internet text teaches. Each points to the file that holds the mechanism.

## Rules
- A VM is a virtual motherboard; the Guest OS is a separate layer. A counter belongs to the layer that produces it, not to the object that stores it. See `vsphere/foundations/vm-vs-guest-os`.
- The same label on another object is another metric: VM CPU Usage and ESXi CPU Usage differ in formula and meaning. Check the `same_name` links before answering. See `vsphere/technology/cpu/metrics/virtual-motherboard/usage`.
- Utilization is not contention. High utilization is not a performance problem; contention is (Ready, Co-stop, memory latency, disk latency, dropped packets). See `vsphere/object-types/cluster/concepts/cluster-utilization-vs-contention`.
- Provider and consumer see different things. ESXi supplies, the VM consumes; Ready applies to the VM, never to ESXi. See `vsphere/foundations/provider-consumer`.
- CPU Latency is not always a problem: lower frequency raises it without any wait. Memory Latency and Disk Latency do mean the VM waits. See `vsphere/technology/cpu/metrics/virtual-motherboard/latency`.
- Hyper-Threading and frequency move Used and Usage; Run is time only. Used far below Run is not a reason to add vCPUs. See `vsphere/technology/cpu/diagnosis/run-vs-used-gap`.
- Ballooned is past tense. Above 0 does not mean pressure now; memory contention decides. See `vsphere/technology/memory/metrics/virtual-motherboard/ballooned`.
- Consumed stays high once pages are touched; it is not demand. Size a Guest OS from Guest OS counters. See `operations-management/capacity/rightsizing`.
- A summation counter is milliseconds per sample. Convert it with the sample interval and the vCPU count. See `vsphere/technology/cpu/metrics/virtual-motherboard/ready`.
- A threshold holds only for its object, its source and its sample interval. A 5-minute average hides 20-second peaks. See `vcf-operations/metrics/vm/peak-20-second-metrics`.
- Admission control counts reservations, not usage. A host at low usage can refuse a power-on. See `vsphere/object-types/cluster/concepts/admission-control-and-cluster-state`.
- Contention on one host while the others are idle points to a DRS blocker; on every host, to cluster capacity or shares. See `vsphere/object-types/cluster/diagnosis/vm-insufficient-resources-in-drs-cluster`.

## Traps
- "A rule of thumb from the Internet applies here" → check the rule above that covers it, then the file it points to.

## Metadata
```yaml
id: vsphere/foundations/core-rules
retriever_guide: how-it-works
scope: vsphere
technology:
- cpu
- memory
- storage
- network
- system
pillar:
- performance
- capacity
product:
- vsphere
- vcf-operations
object:
- VirtualMachine
- HostSystem
- ClusterComputeResource
internal_derive:
- vsphere/foundations/vm-vs-guest-os
- vsphere/technology/cpu/metrics/virtual-motherboard/usage
- vsphere/object-types/cluster/concepts/cluster-utilization-vs-contention
- vsphere/foundations/provider-consumer
- vsphere/technology/cpu/metrics/virtual-motherboard/latency
- vsphere/technology/cpu/diagnosis/run-vs-used-gap
- vsphere/technology/memory/metrics/virtual-motherboard/ballooned
- operations-management/capacity/rightsizing
- vsphere/technology/cpu/metrics/virtual-motherboard/ready
- vcf-operations/metrics/vm/peak-20-second-metrics
- vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
- vsphere/object-types/cluster/diagnosis/vm-insufficient-resources-in-drs-cluster
related:
- glossary
source:
  document: Summary of the knowledge files listed in internal_derive
  path: n/a
corrections: []
review_notes:
- 'Drafted by Claude 2026-11-06 as block 2 of the agent up-front knowledge (harness/AGENT.md, section 3). Each rule summarises the file it points to. Author to confirm the selection and wording (Q059).'
status: draft
```
