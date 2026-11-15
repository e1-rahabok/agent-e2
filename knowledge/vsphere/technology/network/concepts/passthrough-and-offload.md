# Device passthrough and offload

## DirectPath I/O
- Uses Intel VT-d or AMD-Vi hardware support. See [`vsphere/technology/cpu/concepts/hardware-assisted-virtualization`](../../cpu/concepts/hardware-assisted-virtualization.md).
- The guest OS accesses a physical NIC directly, instead of an emulated device (for example E1000) or a paravirtualized device (for example VMXNET or VMXNET3).
- Gain: limited increases in throughput, and a reduction in CPU cost for networking-intensive workloads.
- Not compatible with:
  - vMotion,
  - physical NIC sharing,
  - snapshots,
  - suspend and resume,
  - Fault Tolerance,
  - NetIOC,
  - memory overcommit,
  - VMsafe,
  - NSX network virtualization.
- Typical VMs and workloads do not require DirectPath I/O.
- Candidates: workloads that are very networking intensive (especially high packet rates) and do not use the core virtualization features in the list above.
- Supported configurations: the DirectPath I/O section of vSphere Networking.

## SR-IOV
- Single Root I/O Virtualization: a mode of direct guest access to hardware devices.
- Requires Intel VT-d or AMD-Vi, and also BIOS, physical NIC and network driver support.
- Performance benefits and trade-offs are similar to DirectPath I/O.
- Beneficial for workloads with very high packet rates or very low latency requirements.
- Not compatible with the same list as DirectPath I/O: vMotion, physical NIC sharing, snapshots, suspend and resume, Fault Tolerance, NetIOC, memory overcommit, VMsafe, NSX network virtualization.
- Difference from DirectPath I/O: SR-IOV allows a single physical device to be shared among multiple guests.
- Supported configurations: the section What is Single Root I/O Virtualization (SR-IOV) of vSphere Networking.

## Data processing units (DPUs, SmartNICs)
- Improve networking performance and reduce CPU load.
- Provide many advantages of DirectPath I/O and SR-IOV, and still allow vSphere high-availability and migration features.
- Two data path modes:
  - MUX mode: higher flexibility. Continues to use some host CPU resources.
  - UPTv2 mode: higher performance by offloading all network processing to the DPU. Requires:
    - virtual hardware version 20 or later,
    - a VMXNET3 vNIC guest driver version that supports the feature,
    - full memory reservation and pinning of guest memory.
- Both MUX and UPTv2 provide accelerated networking services for VLAN and overlay networking, checksum offload, TCP Segmentation Offload (TSO), and Receive Side Scaling (RSS).
- Configuring a data path mode requires NSX Manager. Some configuration options do not require an NSX license.

## Enhanced Data Path (EDP)
- EDP is a networking stack mode of ESX for higher network performance. It requires the full VCF package.
- EDP is active by default on new installations of VCF 9.1; an upgrade from an earlier version keeps its earlier setting.
- NIC support: the Broadcom Compatibility Guide, IO Devices, ESXi 9.1, feature EDP Dedicated or EDP Standard.

## Misconceptions
- "DirectPath I/O is a general performance upgrade" → Performance Best Practices for vSphere 9.1 says typical VMs do not require it. It removes vMotion, snapshots, FT and NetIOC.
- "An upgrade to VCF 9.1 turns on Enhanced Data Path" → EDP is on by default only on new installations; an upgrade keeps its earlier setting.
- "SR-IOV gives the same limits as DirectPath I/O" → the list of incompatible features is the same, but SR-IOV allows one device to be shared among guests.
- "UPTv2 works without a memory reservation" → it requires full memory reservation and pinning.

## Metadata
```yaml
id: vsphere/technology/network/concepts/passthrough-and-offload
retriever_guide: how-it-works
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
- vsphere/technology/cpu/concepts/hardware-assisted-virtualization
- vsphere/technology/network/configuration/splitrx-mode
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: ESX Networking Considerations > Enhanced Data Path (EDP) (p. 46); Data Processing Units (DPUs, or SmartNICs) (p. 48); DirectPath I/O (p. 48); Single Root I/O Virtualization (SR-IOV) (p. 49)
corrections: []
review_notes: []
status: draft
```
