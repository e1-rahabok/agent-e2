---
id: vsphere/cpu/architecture/latency-sensitivity
type: concept
scope: vsphere
resources: [cpu, memory, network]
objects: [vm, vcpu, esxi]
related:
  - vsphere/cpu/architecture/hyper-threading
  - vsphere/cpu/architecture/host-power-management
  - vsphere/cpu/architecture/bios-settings
  - vsphere/cpu/resource-management/resource-settings-guidance
  - vsphere/network/architecture/passthrough-and-offload
  - vsphere/network/architecture/rss-and-interrupt-coalescing
source:
  document: Performance Best Practices for VMware vSphere 9.0 (revision 20250731)
  path: Network Considerations > Running Network Latency Sensitive Workloads (pp. 49-51)
corrections: []
review_notes:
  - "Superseded: vSphere 9.1 (revision 20260624) exists. This file was written from the 9.0 document (revision 20250731). Re-check against 9.1 before review."
  - "Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-90-performance-best-practices"
  - "Inconsistent source naming: p. 50 says 'Set the ESX host power policy to Maximum performance'. The power policy list on p. 29 names 'High Performance'. Likely the same policy. Author to confirm."
  - "Source names the white paper 'Best Practices for Performance Tuning of Latency-Sensitive Workloads in vSphere VMs' and calls it dated. Not read."
status: draft
---

# Latency sensitivity

## Default trade-off
- The default ESX network stack drives high network throughput at low CPU cost.
- Cost: potentially higher network latency.
- Latency-sensitive workloads are impacted by latency on the order of a few tens of microseconds.

## Latency sensitivity setting per VM
- Options: Normal (default), High, High with Hyperthreading.
- High with Hyperthreading requires virtual hardware version 20 or later.

## Normal
- ESX can assign the vCPUs of the VM to any hyper-thread on any physical core of the host.
- The source says this gives the best overall performance for the VMs on the host in most cases.

## High
- The scheduler attempts to grant each vCPU of the VM exclusive access to one physical CPU core.
- The core is used as a whole. This effectively deactivates Hyper-Threading for that core.
- Effect: can increase the performance of that one VM.
- Trade-off: can reduce the performance of other VMs on the same host.

## High with Hyperthreading
- The scheduler grants each vCPU exclusive access to one hyper-thread of a physical core.
- Consecutive vCPU pairs share one core:
  - vCPUs 0 and 1 on one physical core,
  - vCPUs 2 and 3 on another physical core.
- ESX exposes this hyper-threaded topology to the guest OS.
- Benefit: the guest OS and applications can use cache locality. This matters for the few guest workloads that can use awareness of the hyper-threading topology.
- For most workloads: no performance benefit, and possibly reduced performance.
- Locking vCPUs to specific hyper-threads can stop ESX from scheduling vCPUs on otherwise idle physical cores. This can limit performance.
- The source recommends High with Hyperthreading only for workloads known to be aware of, and to benefit from, the underlying topology.

## Effect of High or High with Hyperthreading
- Network-related latency and jitter are greatly reduced.
- The assigned physical cores are no longer available to other VMs or to VMkernel worlds.

## Requirements for High or High with Hyperthreading
- Memory for the VM must be reserved at 100%.
- A 100% CPU reservation is set in advance, to get exclusive assignment of the cores the VM uses.
- Even with a 100% CPU reservation, the VM might not get exclusive cores if no NUMA node has enough non-exclusive cores when the VM powers on.
- Virtual hardware version before 14:
  - a 100% CPU reservation is not required to set High,
  - without it, the VM might not get exclusive access to physical CPUs, because of pre-existing CPU overcommitment.
- Virtual hardware version 14 or later with High or High with Hyperthreading:
  - a 100% CPU reservation is a requirement to power on the VM,
  - can be changed with `latency.enforceCpuMin` set to FALSE.
- CPU and memory reservations, and the latency sensitivity setting, persist when the VM is moved with vMotion.

## Full reservations for any latency setting
- Fully reserving memory is required for High and High with Hyperthreading.
- Fully reserving memory can also reduce latency when latency sensitivity is Normal.
- Fully reserving CPUs can also reduce latency when latency sensitivity is Normal.

## Other measures for latency-sensitive traffic
- SR-IOV or DirectPath I/O, to give the VM direct access to the network device. Also tune the interrupt rate for the device in the guest. See `vsphere/network/architecture/passthrough-and-offload`.
- VMXNET3 is the best choice when direct device access is unavailable or undesirable.
- Enhanced Data Path (EDP) is an option without the limitations of SR-IOV. See the source, p. 44. Not read.
- NFV workloads that depend on high packet throughput (telco, 5G, IoT) might benefit from Enhanced Network Stack (ENS), also called EDP, in VCF.

## Host power management
- Power management features in newer server hardware can increase network latency.
- Preferred: set the ESX host power policy to Maximum performance. See `vsphere/cpu/architecture/host-power-management`.
- Alternative: deactivate power management in the BIOS.
- BIOS steps:
  - deactivate C1E and other C-states,
  - activate Turbo Boost.
- See `vsphere/cpu/architecture/bios-settings`.

## Virtual NIC tuning
- For most general-purpose workloads, and moderately latency-sensitive workloads, the default VMXNET3 settings give the best performance.
- Workloads with a low packet rate or few active threads might benefit from deactivating VMXNET3 virtual interrupt coalescing for the NIC.
- Workloads with many outstanding network requests can see reduced performance when interrupt coalescing is deactivated.
- See `vsphere/network/architecture/rss-and-interrupt-coalescing`.

## Traps
- "High latency sensitivity is free" → it removes the physical cores from the pool for other VMs and VMkernel worlds.
- "High with Hyperthreading gives more performance for any VM" → the source says it is not a general-purpose setting, and can reduce performance for most workloads.
- "A 100% CPU reservation guarantees exclusive cores" → not if no NUMA node has enough non-exclusive cores when the VM powers on.
