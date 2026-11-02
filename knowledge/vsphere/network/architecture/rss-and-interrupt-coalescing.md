---
id: vsphere/network/architecture/rss-and-interrupt-coalescing
type: concept
scope: vsphere
resources: [network, cpu]
objects: [vm, esxi]
related:
  - vsphere/cpu/architecture/latency-sensitivity
  - vsphere/network/architecture/splitrx-mode
  - vsphere/cpu/architecture/host-wide-dense-mode
source:
  document: Performance Best Practices for VMware vSphere 9.0 (revision 20250731)
  path: ESX Networking Considerations > Receive Side Scaling (RSS) (p. 48); Virtual Network Interrupt Coalescing (pp. 48-49)
corrections: []
review_notes:
  - "Superseded: vSphere 9.1 (revision 20260624) exists. This file was written from the 9.0 document (revision 20250731). Re-check against 9.1 before review."
  - "Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-90-performance-best-practices"
  - "Exact driver and module commands for RSS are in the source (p. 48). Not copied here. Verify against the NIC driver release before use."
status: draft
---

# Receive Side Scaling and virtual interrupt coalescing

## Receive Side Scaling (RSS)
- RSS schedules network packets from a single NIC in parallel on multiple CPUs, by creating multiple hardware queues.
- Gain: higher packet processing rates and overall throughput.
- Cost: additional CPU utilization, which is incurred only when the traffic requires it.
- The source notes that with large numbers of CPU threads in recent CPUs, the additional CPU use might not be a concern.
- Use case: environments where a single MAC address gets large amounts of traffic, such as network-intensive virtual appliances.
- Some configurations have RSS deactivated by default, because of the potential for increased CPU overhead.
- Usable with 10 Gb/s or faster Ethernet physical NICs. The VM uses the RSS capabilities of the physical NIC through the virtual NIC.
- Activation per NIC type (source, p. 48):
  - Intel 82599, X450 and X550 NICs: activate through the ixgben driver module parameter `RSS`.
  - Mellanox ConnectX-4, ConnectX-5 and ConnectX-6 NICs: the driver supports Default Queue RSS (DRSS) and NetQueue RSS by default.
- For each VM using the feature, add `ethernetX.pNicFeatures = "4"` to the VMX file, where X is the virtual NIC number.

## Virtual network interrupt coalescing
- Coalescing reduces the number of interrupts, which can reduce CPU utilization.
- Cost: can increase network latency, from a few hundred microseconds to a few milliseconds, depending on the workload.
- Many workloads are not affected by that latency. The reduced virtual networking overhead can allow more VMs on one host.
- Default: activated for all virtual NICs.
- For VMXNET3, the coalescing scheme is set with `ethernetX.coalescingScheme`:

| Scheme | Setting | Behaviour |
|---|---|---|
| Rate-based (default) | `rbc`, or variable not present | Interrupt rate set by `ethernetX.coalescingParams`. Range 100 to 100,000 interrupts per second. Default 4,000. |
| Static | `static` | Queues a predefined number of packets before interrupting the VM or transmitting. Queue size set by `ethernetX.coalescingParams`. Range 1 to 64. Default 64. |
| Adaptive | `adapt` | Bases the interrupt rate on the VM load and the overall system load. Lower rate at high load, higher rate at low load. |
| Disabled | `disabled` | More interrupts (and higher CPU utilization). Typically lower network latency. |

- Static: a larger queue size can reduce context switches between the VM and the VMkernel, which can reduce CPU use in the VM and in the VMkernel.
- Regardless of queue size, ESX waits no longer than 4 milliseconds before sending or receiving packets. Other events, such as virtual machine interrupts or packet transmission, can trigger earlier delivery.
- Change in vSphere Client: right-click the VM, Edit Settings, VM Options tab, expand Advanced, Edit Configuration. Set `ethernetX.coalescingScheme` or `ethernetX.coalescingParams`.
- Change takes effect after the VM restarts, or after the vNIC is disconnected and reconnected.

## Traps
- "Coalescing is always good" → it can add latency, and disabling it raises CPU use.
- "RSS is free" → it adds CPU use. The source says it is acceptable with recent CPUs, but it is deactivated by default in some configurations.
- "Coalescing latency is always microseconds" → the source gives a few hundred microseconds up to a few milliseconds.
