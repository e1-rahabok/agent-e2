---
id: vsphere/network/configuration/splitrx-mode
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
- HostSystem
- VirtualMachine
internal_derive: []
related:
- vsphere/network/concepts/passthrough-and-offload
- vsphere/network/configuration/rss-and-interrupt-coalescing
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: ESX Networking Considerations > SplitRx Mode (pp. 49-50)
corrections: []
review_notes:
- Checked against 9.1 (revision 20260624). Pages 49-50 unchanged. The 10,000 packets per second condition is unchanged.
- 'Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices'
- The 10,000 packets per second condition is confirmed in the 9.1 document (p. 49).
status: draft
---

# SplitRx mode

## Definition
- SplitRx mode uses multiple physical CPUs to process network packets received in a single network queue.
- Effect: significantly improved network performance for certain workloads.
- Typical gain: throughput and CPU efficiency for these workloads.

## Workloads that benefit
- Multiple VMs on one ESX host receiving multicast traffic from the same source.
- Traffic between two VMs on the same ESX host, through the vNetwork Appliance (DVFilter) API.

## Automatic activation
- ESX activates SplitRx for a virtual network adapter when it detects both:
  - the only adapter type on which it is supported, VMXNET3,
  - a single network queue on a physical NIC that is heavily utilized, and that receives more than 10,000 broadcast or multicast packets per second.
- Automatic activation applies only when the traffic comes in over a physical NIC.
- For traffic that is entirely internal to the ESX host, SplitRx can be activated manually.

## Host-wide setting
- Variable: `NetSplitRxMode` (under `Net.NetSplitRxMode`).
- `"0"`: deactivates SplitRx for the host.
- `"1"`: activates SplitRx for the host. This is the default.
- Change in vSphere Client: select the host, Configure tab, expand System, Advanced System Settings, Edit, find NetSplitRxMode, set the value, OK.
- The change takes effect immediately. The host does not require a restart.

## Per virtual NIC setting
- Variable in the VMX file: `ethernetX.emuRxMode`, where X is the adapter ID.
- `"0"`: deactivates SplitRx for that adapter. `"1"`: activates it.
- Overrides the host-wide setting for that adapter.
- Change in vSphere Client: right-click the VM, Edit Settings, VM Options tab, expand Advanced, Edit Configuration. Set `ethernetX.emuRxMode`, or add it with Add Configuration Params if it is not present.

## Traps
- "SplitRx is always on for all traffic" → automatic activation requires the conditions above. The default host setting only allows it.
- "SplitRx helps traffic that stays inside the host" → automatic activation does not apply to purely internal traffic. Manual activation is required for that.
