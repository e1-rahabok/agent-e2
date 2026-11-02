---
id: vsphere/network/architecture/passthrough-and-offload
type: concept
scope: vsphere
resources: [network, cpu]
objects: [vm, esxi]
related:
  - vsphere/cpu/architecture/latency-sensitivity
  - vsphere/cpu/architecture/hardware-assisted-virtualization
  - vsphere/network/architecture/splitrx-mode
source:
  document: Performance Best Practices for VMware vSphere 9.0 (revision 20250731)
  path: ESX Networking Considerations > Data Processing Units (DPUs, or SmartNICs) (p. 46); DirectPath I/O (p. 46); Single Root I/O Virtualization (SR-IOV) (p. 46)
corrections: []
review_notes:
  - "Superseded: vSphere 9.1 (revision 20260624) exists. This file was written from the 9.0 document (revision 20250731). Re-check against 9.1 before review."
  - "Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-90-performance-best-practices"
  - "Not read: Enhanced Data Path (p. 44). Source links DPU configuration to NSX Manager and to 'What is VMware vSphere Distributed Services Engine' in ESX Installation and Setup. Not read."
status: draft
---

# Direct device access, SR-IOV and DPUs

## DirectPath I/O
- Uses Intel VT-d or AMD-Vi hardware support. See `vsphere/cpu/architecture/hardware-assisted-virtualization`.
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
- Source for supported configurations: DirectPath I/O section of vSphere Networking. Not read.

## SR-IOV
- Single Root I/O Virtualization: a mode of direct guest access to hardware devices.
- Requires Intel VT-d or AMD-Vi, and also BIOS, physical NIC and network driver support.
- Performance benefits and trade-offs are similar to DirectPath I/O.
- Beneficial for workloads with very high packet rates or very low latency requirements.
- Not compatible with the same list as DirectPath I/O: vMotion, physical NIC sharing, snapshots, suspend and resume, Fault Tolerance, NetIOC, memory overcommit, VMsafe, NSX network virtualization.
- Difference from DirectPath I/O: SR-IOV allows a single physical device to be shared among multiple guests.
- Supported configurations: see the SR-IOV section of vSphere Networking. Not read.

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

## Traps
- "DirectPath I/O is a general performance upgrade" → the source says typical VMs do not require it. It removes vMotion, snapshots, FT and NetIOC.
- "SR-IOV gives the same limits as DirectPath I/O" → the list of incompatible features is the same, but SR-IOV allows one device to be shared among guests.
- "UPTv2 needs no memory reservation" → it requires full memory reservation and pinning.
