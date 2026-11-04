# Receive Side Scaling and virtual interrupt coalescing

## Receive Side Scaling (RSS)
- RSS schedules network packets from a single NIC in parallel on multiple CPUs by creating multiple hardware queues.
- Gain: higher packet processing rates and overall throughput.
- Cost: additional CPU utilization, incurred only when the traffic requires it.
- The source notes that with large numbers of CPU threads in recent CPUs, the additional CPU use might not be a concern.
- Use case: environments where a single MAC address gets large amounts of traffic, such as network-intensive virtual appliances.
- Some configurations have RSS deactivated by default, because of the potential for increased CPU overhead.
- Activation per NIC type (9.1 pp. 50-51):
  - Broadcom BCM5741x, BCM5750x, BCM5760x: the bnxtnet driver supports DRSS and NetQueue RSS by default. RSS is supported in pktHandle mode and EDP mode.
  - Intel 82599, X450, X550, X557, E610, E710, XL710, XXV710, E810, E830, E835: enable with the ixgben driver module parameter `RSS`.
  - Marvell FastLinQ 45xxx and 41xxx: the qedentv driver supports DRSS and NetQueue RSS by default. RSS is supported with and without EDP.
  - NVIDIA (previously Mellanox) ConnectX-4 through ConnectX-9: the nmlx5_core driver supports DRSS and NetQueue RSS by default.
- For each VM that uses the feature, once RSS is enabled (by default or by command), add `ethernetX.pNicFeatures = "4"` to the VMX file, where X is the virtual NIC number.
- Exact driver commands are in the source. They are not copied here. Verify against the NIC driver release before use.

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

## Metadata
```yaml
id: vsphere/technology/network/configuration/rss-and-interrupt-coalescing
retriever_guide: what-to-set
scope: vsphere
technology:
- network
- cpu
pillar:
- performance
product:
- vsphere
object:
- VirtualMachine
- HostSystem
internal_derive: []
related:
- vsphere/technology/cpu/configuration/latency-sensitivity
- vsphere/technology/network/configuration/splitrx-mode
- vsphere/technology/cpu/configuration/host-wide-dense-mode
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: ESX Networking Considerations > Receive Side Scaling (RSS) (p. 50); Virtual Network Interrupt Coalescing (p. 51)
corrections: []
review_notes:
- Checked against 9.1 (revision 20260624). RSS NIC list changed in 9.1 (pp. 50-51). Coalescing unchanged.
- 'Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices'
- Exact driver and module commands for RSS are in the source (p. 48). Not copied here. Verify against the NIC driver release before use.
status: draft
```
