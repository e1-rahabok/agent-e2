# Hyper-Threading

## Definition
- Hyper-Threading (also called simultaneous multithreading, SMT) lets one physical core behave like two logical processors.
- The two logical processors run threads at the same time.
- Gain: a slight to significant increase in system performance, by keeping the processor pipeline busy.
- Hyper-Threading does not double performance. Twice as many physical cores can roughly double performance. Hyper-Threading can provide anywhere from a slight to a significant increase.

## Enablement
- ESX uses Hyper-Threading automatically when the hardware and BIOS support it.
- The BIOS must support it. Check the system documentation.
- Enable it in the system BIOS.
- BIOS labels vary: "Logical Processor" or "Enable Hyper-Threading".
- The source recommends activating it for best performance.

## Logical processor numbering
- ESX assigns adjacent CPU numbers to the logical processors of one core.
- Example:
  - CPU 0 and CPU 1 share the first core,
  - CPU 2 and CPU 3 share the second core.

## Scheduling behaviour
- ESX spreads load across all physical cores.
- A logical processor with no work is halted.
- Its execution resources become available to the other logical processor on the same core.
- The scheduler places a VM's vCPUs on two different cores before using both logical processors of one core.
- A vCPU running on one logical processor of a busy core gets slightly more than half the throughput it gets alone on the core.
- The scheduler accounts for this: a VM running with a whole core (sibling halted) is charged more than a VM running on half a core.
- The gain is application dependent. Some applications slow down, because the two logical processors share caches and execution units.

## Affinity caution
- The two logical processors share most processor resources.
- Pinning vCPUs to both logical processors of one core can cause poor performance.
- The source gives this example: CPU 0 and CPU 1 on the same core.
- The caution applies whether the vCPUs come from different VMs or from one SMP VM.

- CPU admission control ignores affinity: a pinned VM can be admitted and still not get its reservation.
- A VM's affinity covers its vCPUs and its helper worlds (devices, display). Pinning a 1-vCPU VM to one CPU, or a 2-vCPU VM to two CPUs, stops the helpers from running alongside the vCPUs. Include at least one extra CPU.
- Affinity may no longer fit after vMotion to a host with a different CPU count.

## vCPU count and hyper-threads
- Hyper-threads count as logical threads.
- A VM with more vCPUs than physical cores is sometimes permissible.
- The same configuration can create contention when the vCPUs are used.

## NUMA and hyper-threads
- A VM with more vCPUs than cores per NUMA node, but fewer than logical processors per NUMA node, can use logical processors with local memory.
- Setting: `numa.vcpu.preferHT`, per VM.
- Details: see `vsphere/cpu/concepts/numa`.

## Traps
- "Hyper-Threading doubles CPU capacity" → the source gives a slight to significant gain, not a doubling.
- "Pin each vCPU to a logical processor for isolation" → pinning both threads of one core can cause poor performance.

## Metadata
```yaml
id: vsphere/cpu/concepts/hyper-threading
retriever_guide: how-it-works
scope: vsphere
technology:
- cpu
pillar:
- performance
- capacity
product:
- vsphere
object:
- HostSystem
internal_derive: []
related:
- vsphere/cpu/concepts/numa
- vsphere/cpu/configuration/latency-sensitivity
- vsphere/cpu/configuration/side-channel-scheduling
- vsphere/cpu/metrics/comparisons/consumption-metrics
- vsphere/cpu/concepts/idle-and-unused-vcpus
- vsphere/cpu/concepts/cpu-efficiency
- vsphere/cpu/concepts/cpu-topology
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: ESX CPU Considerations > Hyper-Threading (p. 28); Guest Operating System CPU Considerations (p. 57); Hardware BIOS Settings (p. 21)
corrections: []
review_notes:
- 'Sections ''Scheduling behaviour'', ''Affinity caution'': throughput, charging, scheduler preference and affinity side effects from the vSphere 9.1 documentation, vSphere Resource Management > Hyperthreading and ESX Hosts, Using CPU Affinity, Potential Issues with CPU Affinity (pp. 1829-1831).'
- Checked against 9.1 (revision 20260624). Page 28 unchanged. Page references updated.
- 'Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices'
- This source gives no Hyper-Threading penalty percentages. The book's 37.5% (VM Usage) and 50% (ESXi Used) figures are not confirmed by this source. Author to confirm.
status: draft
```
