# GPU monitoring

## Counters
| Counter (chart label) | Object | Unit, rollup, level | Meaning |
|---|---|---|---|
| Utilization (GPU Compute Usage) | HostSystem, per GPU device | %, Average, level 4 | Share of GPU compute in use. Vendor and architecture specific. |
| Memory used (GPU Memory Usage) | HostSystem, per GPU device | KB and %, Average, level 4 | Frame buffer (VRAM) allocated to vGPUs, not workload use. |
| Temperature (GPU Temperature) | HostSystem, per GPU device | °C, Average, level 4 | GPU device temperature. |
| GPU (watts) | VirtualMachine | Watts, level 1 (VM power group) | Power drawn by the VM's virtual GPU. |

- Utilization, memory used and temperature per GPU device on the host are statistics level 4 counters in the chart tables: at the default level 1, vCenter keeps no per-device history. See [`vsphere/tools/vsphere-client/vcenter-statistics`](../../tools/vsphere-client/vcenter-statistics.md).
- Cluster and resource pool GPU counters are level 1 in the vCenter 9.1 API, so their history exists by default:

| Counter | Rollup | Meaning (vCenter summary) |
|---|---|---|
| `gpu.utilization` | average | Compute utilization of a GPU, % |
| `gpu.mem.used` | average | GPU memory used by workloads, KB |
| `gpu.mem.reserved` | latest | GPU memory consumed by virtual GPUs, KB |
| `gpu.mem.total` | latest | Total GPU memory, KB |
| `gpu.power.used` | latest | Power used by a GPU, watts |
| `gpu.temperature` | average | GPU temperature, °C |

- GPU counters appear only when the GPU vendor driver is installed on the host.
- The host GPU charts show the 10 devices with the highest value: compute usage, memory allocation, temperature.
- The VM GPU power group appears only for VMs with NVIDIA GPUs.
- Preconfigured vCenter alarms: GPU ECC Uncorrected Memory, GPU ECC Corrected Memory, GPU Thermal Condition.

## Reading the counters
- High GPU utilization means either effective use or a bottleneck at peak. It does not show which, and it is not comparable across GPU vendors or architectures.
- The host per-device chart Memory used (level 4) shows the frame buffer allocated to vGPUs, not the active workload of the VMs. A host can show high GPU memory while the VMs are idle.
- At cluster and resource pool level vCenter reports the two separately: `gpu.mem.reserved` (memory consumed by virtual GPUs) and `gpu.mem.used` (memory used by workloads).
- The word "used" means allocation in the host per-device chart and workload use in cluster `gpu.mem.used`. Same word, different meaning.
- `gpu.mem.reserved` is the sum of the vGPU profile frame buffers of the powered-on vGPU VMs. NVIDIA allocates the whole frame buffer of the profile on the physical GPU when the VM powers on and frees it when the VM powers off (Broadcom KB 439680).
- DirectPath I/O (PCI passthrough) GPUs are not in `gpu.mem.reserved`. The whole GPU is mapped into the VM and bypasses the NVIDIA vGPU Manager on ESXi, so the host cannot account for or monitor that GPU's memory. Monitor it from inside the Guest OS with the vendor tool, for example nvidia-smi.
- vSphere 9.0 and 9.1: `gpu.mem.used` is the frame buffer the workloads touch, at or below `gpu.mem.reserved`, because the profile is the upper bound of the frame buffer a vGPU VM can use.
- vSphere 8.x: `gpu.mem.used` does not follow that rule. Do not compare it with `gpu.mem.reserved` on 8.x hosts.
- Reserved above used is normal: a reservation is a setting, used is the result of activity, and a workload need not use all it reserved.
- GPU frame buffer is never overcommitted with NVIDIA vGPU. Only compute is time-sliced between vGPUs, so low `gpu.utilization` frees no GPU memory for another VM.
- Rising temperature leads to thermal throttling: the GPU lowers its clock and performance drops before any failure. It can also damage hardware.
- vSphere has no GPU contention counter. Quality-of-service problems inside a vGPU (time slicing between vGPUs) are tracked with the GPU vendor's tools.

## vGPU and host memory
- A VM with a vGPU (a PCI device) gets a full memory reservation automatically.
- Consequences:
  - its memory is never ballooned, compressed or swapped;
  - it counts in full against host, resource pool and HA admission control;
  - it is excluded from memory tiering and stays in DRAM.
- Unlike an ordinary memory reservation, which is backed only as the guest touches pages, the whole memory of a passthrough or vGPU VM is allocated at power-on: the device reads and writes guest memory directly (DMA), so every page must stay backed and in place. The host sees it as Consumed from power-on, whatever the guest uses.
- Effect on the other VMs of the host and cluster: the reserved memory leaves the reclaimable pool. The unreserved VMs share only what is left, so their overcommit ratio rises, and every later shortage (their growth, a host failure, maintenance mode) is reclaimed from them alone.
- HA admission control (cluster resource percentage) sees the vGPU VMs' reservations, which fit as long as all reservations stay below the capacity minus the failover percentage. The unreserved VMs count only their overhead, so admission control stays green while the hosts left after a failure cannot hold the unreserved VMs' Consumed memory. Check memory after a failure as the remaining capacity minus all reservations, against the unreserved VMs' Consumed ([`vsphere/object-types/cluster/concepts/admission-control-and-cluster-state`](../../object-types/cluster/concepts/admission-control-and-cluster-state.md)).
- A VM can have up to 16 vGPU devices (virtual hardware version 21).

## vGPU capacity
- A vGPU profile fixes the frame buffer size per VM. The physical GPU holds a fixed number of instances per profile.
- Placement needs one physical GPU with one contiguous free frame buffer of the profile size. A vGPU never spans two physical GPUs.
- Example: four GPUs with 8 GB free each give 32 GB free in the cluster, and a 16 GB profile still fails to power on.
- Cluster `gpu.mem.reserved` against `gpu.mem.total` hides this fragmentation, so placement can fail long before reserved reaches total. DirectPath Profiles Remaining, per profile, shows when a profile is exhausted.
- SameSize: a physical GPU that already holds a vGPU accepts only vGPUs of the same profile size. Older NVIDIA architectures (before Ampere) support only this mode.
- MixedSize: Ampere, Ada Lovelace and Hopper GPUs can hold different profile sizes on one GPU, for example an 8Q and a 4Q, when the host is set to MixedSize. Each profile size has fixed placement positions on the GPU, so free memory on one GPU can still be too fragmented for a large profile.
- MixedSize lowers the maximum instances of some profiles. Example: A16-1Q drops from 24 instances (SameSize) to 16 (MixedSize).
- DirectPath Profiles report vGPU capacity per host and cluster:

| Value | Meaning |
|---|---|
| Consumed | Instances allocated to powered-on VMs. Excludes VMs still powering on or arriving by vMotion. |
| Remaining | Instances still allocatable, assuming no new VMs and no competition. |
| Maximum | Total instances with no VMs running. |

- Consumed + Remaining can be less than Maximum: NVIDIA placement rules limit how profiles fit on a physical GPU.
- A vGPU VM can fail to power on while the cluster shows GPU memory free. Causes: fragmented GPU device memory, exhausted device memory, or exhausted assignable processor engines on every single GPU. Broadcom KB 312021.

## Placement and migration
- Host graphics policy: spread VMs across GPUs (best performance) or group VMs on a GPU until full (GPU consolidation, more free GPUs for large profiles).
- DRS spreads vGPU VMs breadth-first across hosts. This fragments GPU capacity: many partly used GPUs, none free for a large profile.
- To keep GPUs free for large profiles: the same vGPU profile on all VMs of a cluster, GPU consolidation on hosts, or manual migration.
- DRS migrates a vGPU VM automatically only when its estimated stun time is below the vMotion stun time limit (default 100 seconds). The VM is paused while the GPU state copies, so large frame buffers mean long stuns.

## Misconceptions
- "GPU memory 90% used, so the VMs are busy" → vGPU frame buffers are reserved at power-on. Check GPU utilization.
- "The 1-week chart shows no GPU data, so the GPU was idle" → per-device host GPU counters are level 4; default history holds none. Use the cluster or resource pool GPU counters, which are level 1.
- "GPU memory reserved is high, so the workloads are busy" → compare with `gpu.mem.used` and utilization.
- "Cluster GPU memory is free, so the vGPU VM will power on" → placement is per physical GPU and per profile. Check DirectPath Profiles Remaining.
- "GPU utilization is low, so another vGPU fits" → frame buffer is allocated whole at power-on and never overcommitted; only compute is shared.
- "`gpu.mem.reserved` includes the passthrough GPUs" → DirectPath I/O GPUs bypass the vGPU Manager; the host does not count their memory.
- "DirectPath Profiles charts cover DirectPath I/O passthrough" → DirectPath Profiles count vGPU profile instances.
- "`gpu.mem.used` is at or below reserved on every release" → true on vSphere 9.0 and 9.1, not on 8.x.
- "Balloon the vGPU VM to free host memory" → vGPU VMs are fully reserved; nothing is reclaimed.
- "Host Consumed leaves enough free memory for the new vGPU VMs, and admission control agrees, so the cluster has room" → the vGPU VMs fit today, but their reservations shrink what the unreserved VMs can use; admission control does not see the unreserved VMs' usage, so check their room in normal operation and after a host failure.
- "Fully reserved vGPU VMs larger than the HA failover percentage fail admission control" → with the percentage policy the reservations are compared with the capacity left after the failover percentage, not with the failover percentage itself.

## Metadata
```yaml
id: vsphere/technology/gpu/gpu-monitoring
retriever_guide: how-it-works
scope: vsphere
technology:
- gpu
pillar:
- performance
- capacity
product:
- vsphere
object:
- HostSystem
- VirtualMachine
- ClusterComputeResource
internal_derive:
- vsphere/tools/vsphere-client/vcenter-statistics
related:
- vsphere/tools/vsphere-client/vcenter-statistics
- vsphere/technology/memory/concepts/memory-tiering
- vsphere/object-types/cluster/concepts/drs-overview
- vsphere/technology/cpu/concepts/numa
source:
  document: VMware vSphere 9.1 product documentation (PDF built 2026-11-02; the copyright page carries no revision number); Repository e1-rahabok/Observability-vSphere, vsphere-metrics.csv (vCenter 9.1.0 build 25370922); Broadcom KB 439680; Broadcom KB 312021
  path: vSphere Monitoring and Performance > Metric Groups, Statistics Levels, Hosts > GPU Compute, GPU Memory, GPU Compute Usage, GPU Memory Allocation, GPU Temperature, Preconfigured vSphere Alarms (pp. 2028-2030, 2065-2067, 2142); vSphere Resource Management > Configure Virtual Graphics, Migrating VMs with vGPUs, Configuring vGPU Size, Capacity Visualization of DirectPath Profiles, DRS Placement of vGPUs (pp. 1880-1884, 1902); Memory Tiering, Virtual Machine Profiles (PCI Passthrough VM in DRAM only, p. 1846); cluster and resource pool counters from https://github.com/e1-rahabok/Observability-vSphere/blob/main/vsphere-metrics.csv
corrections: []
review_notes:
- 'To check: Section ''Reading the counters'': whether DirectPath I/O GPUs are also left out of gpu.mem.total; a live reading on a cluster with one passthrough GPU.'
- 'To check: Section ''Reading the counters'': thermal throttling as a clock reduction; the vSphere 9.1 documentation says only that overheating can cause throttling and reduced performance; NVIDIA Virtual GPU Software User Guide, https://docs.nvidia.com/vgpu/latest/pdf/grid-vgpu-user-guide.pdf.'
- 'To check: Section ''Placement and migration'': that breadth-first placement fragments GPU capacity (inferred from the remedies the vSphere 9.1 documentation gives: same profile, GPU consolidation, manual migration), and the pause while the GPU state copies (not in the documentation); vSphere 9.1 documentation, Migrating VMs with vGPUs, or a live vMotion of a vGPU VM.'
- 'To check: Section ''vGPU and host memory'': that the whole memory of a passthrough or vGPU VM is allocated at power-on rather than backed as the guest touches it; the vSphere 9.1 documentation says only that a DirectPath I/O device sets the memory reservation to the VM memory size (p. 1192) and that a vGPU VM gets a full reservation (p. 1881); a live host Consumed reading at power-on.'
status: draft
```
