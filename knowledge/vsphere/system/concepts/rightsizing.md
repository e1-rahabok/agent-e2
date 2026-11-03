# Why rightsizing matters for VMs

## Two sizing jobs, not one
- There is no single "VM rightsizing". Guest OS sizing (internal, Guest OS counters, includes guest queue, excludes VM overhead) and VM footprint (external, vSphere counters, includes VM overhead, excludes guest queue) answer different questions. See `guest-os/system/concepts/guest-os-sizing` and `vsphere/system/concepts/vm-footprint-sizing`.
- This file covers why a smaller vCPU count helps once the right size is known.

## NUMA example
- Host: 2 sockets × 16 cores. VM: 16 vCPU at 90%, fits one socket.
- Linux run queue below 2 per vCPU 95% of the time: busy but serving all processes.
- Sizing on CPU Usage, which runs 25% higher due to Turbo: 16 × 90% × 125% = 18 vCPU.
- 18 vCPU spans 2 NUMA nodes (9 + 9 or 10 + 8). Rounding up to 20 for buffer spreads vCPUs and memory over 2 sockets: NUMA effect.
- With CCDs inside a socket, a smaller NUMA effect exists within a socket too.

## Other benefits of fewer vCPUs
- Higher frequency: fewer active threads let ESXi boost the active cores. Check CPU Usage (MHz) per vCPU.
- Lower Co-stop and Ready: the Guest OS demands that all vCPUs be scheduled, used or not.
- Faster snapshots, especially with memory.
- Faster vMotion: Windows and Linux use memory as cache; more memory, more to copy.
- Faster boot: without a reservation, vSphere creates a swap file the size of configured RAM; slow storage delays boot.
![Usage (MHz) per vCPU](../images/vm-cpu-usage-mhz-per-vcpu.png)

## Traps
- "Size on CPU Usage" → Turbo inflates it 25% in this example, pushing the VM across NUMA nodes.

## Metadata
```yaml
id: vsphere/system/concepts/rightsizing
retriever_guide: how-it-works
scope: vsphere
technology:
- cpu
- memory
- system
pillar:
- capacity
- performance
- value
product:
- vsphere
- vcf-operations
object:
- VirtualMachine
internal_derive: []
related:
- guest-os/system/concepts/guest-os-sizing
- vsphere/system/concepts/vm-footprint-sizing
- vsphere/cpu/concepts/cpu-topology
- vsphere/cpu/concepts/numa
images:
  - path: ../images/vm-cpu-usage-mhz-per-vcpu.png
    product: [vsphere]
    object: [VirtualMachine]
    metric: ['VM CPU Usage (MHz)']
    topic: 'Rightsizing'
    image_type: timeline
source:
  document: PART 3 - Counters.docx
  path: 'Consumer Objects > Capacity: Guest OS > Benefits'
corrections: []
review_notes: []
status: draft
```
