# GPU monitoring

## Counters
| Counter (chart label) | Object | Unit, rollup, level | Meaning |
|---|---|---|---|
| Utilization (GPU Compute Usage) | HostSystem, per GPU device | %, Average, level 4 | Share of GPU compute in use. Vendor and architecture specific. |
| Memory used (GPU Memory Usage) | HostSystem, per GPU device | KB and %, Average, level 4 | GPU frame buffer (VRAM) in use. |
| Temperature (GPU Temperature) | HostSystem, per GPU device | °C, Average, level 4 | GPU device temperature. |
| GPU (watts) | VirtualMachine | Watts, level 1 (VM power group) | Power drawn by the VM's virtual GPU. |

- Utilization, memory used and temperature are statistics level 4 counters. At the default level 1, vCenter keeps no GPU history: only real-time data. See `vsphere/foundations/vcenter-statistics`.
- GPU counters appear only when the GPU vendor driver is installed on the host.
- The host GPU charts show the 10 devices with the highest value: compute usage, memory allocation, temperature.
- The VM GPU power group appears only for VMs with NVIDIA GPUs.
- Preconfigured vCenter alarms: GPU ECC Uncorrected Memory, GPU ECC Corrected Memory, GPU Thermal Condition.

## Reading the counters
- High GPU utilization means either effective use or a bottleneck at peak. It does not show which, and it is not comparable across GPU vendors or architectures.
- GPU memory used with vGPU reflects the frame buffer reserved for each vGPU profile, not the active workload of the VM. A host can show high GPU memory while the VMs are idle.
- Rising temperature leads to thermal throttling: the GPU lowers its clock and performance drops before any failure. It can also damage hardware.
- vSphere has no GPU contention counter. Quality-of-service problems inside a vGPU (time slicing between vGPUs) are tracked with the GPU vendor's tools.

## vGPU and host memory
- A VM with a vGPU (a PCI device) gets a full memory reservation automatically.
- Consequences:
  - its memory is never ballooned, compressed or swapped;
  - it counts in full against host, resource pool and HA admission control;
  - it is excluded from memory tiering and stays in DRAM.
- A VM can have up to 16 vGPU devices (virtual hardware version 21).

## vGPU capacity
- A vGPU profile fixes the frame buffer size per VM. The physical GPU holds a fixed number of instances per profile.
- Heterogeneous sizes per GPU (MixedSize) allow different profiles on one device, but lower the maximum instances of some profiles. Example: A16-1Q drops from 24 instances (SameSize) to 16 (MixedSize).
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

## Traps
- "GPU memory 90% used, so the VMs are busy" → vGPU frame buffers are reserved at power-on. Check GPU utilization.
- "The 1-week chart shows no GPU data, so the GPU was idle" → GPU counters are level 4; default history holds none.
- "Cluster GPU memory is free, so the vGPU VM will power on" → placement is per physical GPU and per profile. Check DirectPath Profiles Remaining.
- "Balloon the vGPU VM to free host memory" → vGPU VMs are fully reserved; nothing is reclaimed.

## Metadata
```yaml
id: vsphere/system/concepts/gpu-monitoring
retriever_guide: how-it-works
scope: vsphere
technology:
- system
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
- vsphere/foundations/vcenter-statistics
related:
- vsphere/foundations/vcenter-statistics
- vsphere/memory/concepts/memory-tiering
- vsphere/resource-management/concepts/drs-overview
- vsphere/cpu/concepts/numa
source:
  document: VMware vSphere 9.1 product documentation (PDF built 2026-11-02; the copyright page carries no revision number)
  path: vSphere Monitoring and Performance > Metric Groups, Statistics Levels, Hosts > GPU Compute, GPU Memory, GPU Compute Usage, GPU Memory Allocation, GPU Temperature, Preconfigured vSphere Alarms (pp. 2028-2030, 2065-2067, 2142); vSphere Resource Management > Configure Virtual Graphics, Migrating VMs with vGPUs, Configuring vGPU Size, Capacity Visualization of DirectPath Profiles, DRS Placement of vGPUs (pp. 1880-1884, 1902)
corrections: []
review_notes:
- 'Whole file: from the vSphere 9.1 documentation, not the book.'
- 'Section ''Reading the counters'': thermal throttling as a clock reduction, and vGPU time slicing as the quality-of-service mechanism, are Claude''s own knowledge. The documentation says overheating can cause throttling and reduced performance, and points to the GPU vendor for QoS.'
- 'Section ''Placement and migration'': the statement that breadth-first placement fragments GPU capacity is Claude''s inference from the documentation''s remedies (same profile, GPU consolidation, manual migration to open up unused physical GPU capacity). The pause during GPU state copy is Claude''s own knowledge.'
- 'Section ''vGPU and host memory'': exclusion from memory tiering follows from the documentation listing PCI Passthrough VMs as DRAM-only.'
status: draft
```
