---
id: vsphere/cpu/architecture/hyper-threading
type: concept
scope: vsphere
resources: [cpu]
objects: [vcpu, esxi]
related:
  - vsphere/cpu/architecture/numa
  - vsphere/cpu/architecture/latency-sensitivity
  - vsphere/cpu/architecture/side-channel-scheduling
  - vsphere/cpu/distinctions
  - vsphere/cpu/architecture/idle-and-unused-vcpus
source:
  document: Performance Best Practices for VMware vSphere 9.0 (revision 20250731)
  path: ESX CPU Considerations > Hyper-Threading (p. 26); Guest Operating System CPU Considerations (p. 55); Hardware BIOS Settings (p. 21)
corrections: []
review_notes:
  - "Superseded: vSphere 9.1 (revision 20260624) exists. This file was written from the 9.0 document (revision 20250731). Re-check against 9.1 before review."
  - "Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-90-performance-best-practices"
  - "This source gives no Hyper-Threading penalty percentages. The book's 37.5% (VM Usage) and 50% (ESXi Used) figures are not confirmed by this source. Author to confirm."
status: draft
---

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

## Affinity caution
- The two logical processors share most processor resources.
- Pinning vCPUs to both logical processors of one core can cause poor performance.
- The source gives this example: CPU 0 and CPU 1 on the same core.
- The caution applies whether the vCPUs come from different VMs or from one SMP VM.

## vCPU count and hyper-threads
- Hyper-threads count as logical threads.
- A VM with more vCPUs than physical cores is sometimes permissible.
- The same configuration can create contention when the vCPUs are used.

## NUMA and hyper-threads
- A VM with more vCPUs than cores per NUMA node, but fewer than logical processors per NUMA node, can use logical processors with local memory.
- Setting: `numa.vcpu.preferHT`, per VM.
- Details: see `vsphere/cpu/architecture/numa`.

## Traps
- "Hyper-Threading doubles CPU capacity" → the source gives a slight to significant gain, not a doubling.
- "Pin each vCPU to a logical processor for isolation" → pinning both threads of one core can cause poor performance.
