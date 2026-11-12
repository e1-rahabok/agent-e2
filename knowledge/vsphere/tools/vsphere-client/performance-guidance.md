# vSphere documentation performance guidance

## Scope
- Thresholds and actions that the vSphere 9.1 documentation publishes for the vSphere Client performance charts.
- They are generic starting points, not proof of a problem. Each section states where the knowledge base reads the same counter differently, and why.
- Contention metrics confirm a problem. The documentation mostly starts from consumption (usage). Check contention before acting.

## CPU
| Condition in the documentation | Documentation reading |
|---|---|
| Short spike in host, cluster or resource pool CPU usage | Good use of resources. |
| Host CPU usage constantly high | Raises VM Ready time and processor queuing. |
| VM CPU Usage above 90% and VM CPU Ready above 20% | Performance is impacted. |

- Causes the documentation lists: host short of CPU; too many vCPUs relative to physical cores; storage or network IO that puts the CPU in a wait state; Guest OS load.
- VM CPU Ready in the vCenter chart is a percentage averaged over the vCPUs at statistics level 1.
- The knowledge base reads Ready against Run, not against a fixed value: 2% Ready on 10% Run delayed 20% of transactions. See [`vsphere/technology/cpu/metrics/virtual-motherboard/ready`](../../technology/cpu/metrics/virtual-motherboard/ready.md).
- High Ready while Usage sits at the VM CPU limit: the limit causes it. esxtop %MLMTD is counted inside %RDY. Remove or raise the limit.
- More shares give one VM more chances to run. Total host Ready stays the same when the host itself is short of CPU.
- Idle vCPUs still cost host CPU: the hypervisor maintains them. Right-size to the vCPUs the workload runs. See [`vsphere/technology/cpu/concepts/idle-and-unused-vcpus`](../../technology/cpu/concepts/idle-and-unused-vcpus.md).
- Documentation actions: VMware Tools installed; CPU reservations for high-priority VMs; fewer vCPUs on oversized VMs; DRS and more hosts; TCP Segmentation Offload, large memory pages and jumbo frames to cut CPU per IO.

## Memory
| Condition in the documentation | Documentation reading |
|---|---|
| Host memory usage consistently 94% or higher | Host probably short of memory. The same text adds: if balloon and swap are not high, performance is probably not affected. |
| Memory usage consistently 24% or lower | Memory size probably too large. |
| Host free memory 6% or less, with frequent swapping | Host cannot meet the combined active memory of its VMs. Reclamation degrades performance. |
| VM Active equal to Granted | Demand for memory exceeds what is available. |
| VM Active consistently low | VM memory size might be too large. |
| Host has free memory, yet a VM shows high balloon or swap | The VM, or its resource pool, has hit its memory limit. |

- Sizing rule in the documentation: host memory slightly larger than the combined Active of its VMs; VM memory slightly larger than average guest memory usage.
- vSphere Client host Memory Usage (%) is Consumed / total. Consumed holds guest cache, so high usage alone is not a problem. See [`vsphere/technology/memory/metrics/host/usage`](../../technology/memory/metrics/host/usage.md) and [`vsphere/technology/memory/concepts/memory-as-storage`](../../technology/memory/concepts/memory-as-storage.md).
- Swap-out and compression mean pressure or a limit. VM Memory Latency and swap-in mean the VM is waiting. See [`vsphere/technology/memory/concepts/swap-and-compression`](../../technology/memory/concepts/swap-and-compression.md).
- A memory reservation far above Active blocks reclamation of idle pages. Lower it so the kernel can give them to other VMs.
- The documentation calls ballooning and swapping regular reclamation that generally does not affect performance, provided the balloon driver runs.
- Documentation actions: VMware Tools and the balloon driver enabled; smaller VM memory where the guest cache is oversized; lower oversized reservations; DRS; more host memory.

## Storage latency
| vCenter counter | esxtop | Documentation guidance |
|---|---|---|
| kernelLatency | KAVG | Best 0-1 ms. Above 4 ms: VMs send more throughput than the configuration supports. Check CPU usage; increase the queue depth. |
| deviceLatency | DAVG | Above 15 ms, depending on the hardware: probable array problem. Move the active VMDK to a volume with more spindles or add disks to the LUN. |
| queueLatency | QAVG | Must always be 0. Above 0: workload too high; the array cannot process data fast enough. |
| totalReadLatency, totalWriteLatency | GAVG | kernelLatency + deviceLatency. |

- The knowledge base uses lower values: KAVG above 0.5 ms → check QAVG and queue depths; DAVG healthy well within 5 ms. See [`vsphere/technology/storage/troubleshooting/host-storage-latency`](../../technology/storage/troubleshooting/host-storage-latency.md).
- The documentation's device remedy names spindles: the 15 ms value comes from spinning-disk arrays. Flash arrays run far lower; compare with the array's own baseline.
- Documentation actions: more VM memory for guest caching (less IO); antivirus on-demand scans off for VMDK and VMEM files; array-side statistics; Storage vMotion to spread IO-heavy VMs; spread busy LUNs across adapters; adequate HBA and RAID controller queue depth (Disk.SchedNumReqOutstanding); multipathing when IO exceeds one HBA; preallocated virtual disks.

## Storage space
- A datastore is full when Used equals Capacity.
- Allocated (provisioned) space can exceed capacity: thin-provisioned disks and snapshots.
- Snapshots holding much space: consolidate them. Consolidation deletes the redo logs.

## Network
- Dropped packets indicate a network bottleneck. Check droppedTx and droppedRx in vCenter, or %DRPTX and %DRPRX in esxtop.
- Drops at the virtual switch port: increase the vNIC driver ring buffers. See [`vsphere/technology/network/vnic-rx-drops`](../../technology/network/vnic-rx-drops.md).
- No drops but a slow receive rate: host or VM CPU cannot keep up with the packet rate.
- Small packets: more packets per byte, so more CPU per byte. Large packets: fewer packets and less CPU, but possibly higher latency.
- vSphere has no network latency counter. The documentation points to external tools. See [`vsphere/technology/network/concepts/network-observability`](../../technology/network/concepts/network-observability.md).
- Documentation checks: VMs per physical NIC; VMs on the same host that talk to each other on the same virtual switch (no physical hop); separate physical NICs per traffic type (VM, iSCSI, vMotion); physical NIC speed and duplex as expected (a 1 Gbps NIC reset to 100 Mbps by an older switch; half duplex); vmxnet3; TCP Segmentation Offload and jumbo frames.

## Misconceptions
- "Host memory usage 94%, so add memory" → only when balloon, swap-in or VM Memory Latency are also high.
- "VM CPU Ready below 20%, so CPU is fine" → read Ready against Run; check Co-stop and limits.
- "DAVG 10 ms is healthy because the documentation allows 15 ms" → 15 ms reflects spinning disks; compare with the array baseline.
- "Balloon above 0 means a performance problem" → reclamation; check swap-in and latency.

## Metadata
```yaml
id: vsphere/tools/vsphere-client/performance-guidance
retriever_guide: how-it-works
scope: vsphere
technology:
- cpu
- memory
- storage
- network
pillar:
- performance
product:
- vsphere
object:
- VirtualMachine
- HostSystem
- ClusterComputeResource
- ResourcePool
- Datastore
internal_derive:
- vsphere/technology/cpu/metrics/virtual-motherboard/ready
- vsphere/technology/memory/metrics/host/usage
- vsphere/technology/memory/concepts/swap-and-compression
- vsphere/technology/storage/troubleshooting/host-storage-latency
related:
- vsphere/tools/vsphere-client/vcenter-statistics
- vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high
- vsphere/technology/memory/vm-memory-latency-high
- vsphere/technology/storage/concepts/esxi-storage-latency-stack
- vsphere/technology/network/vnic-rx-drops
- sp5-framework/observability/thresholds
source:
  document: VMware vSphere 9.1 product documentation (PDF built 2026-11-02; the copyright page carries no revision number)
  path: vSphere Monitoring and Performance > Overview Performance Charts > Chart Analysis sections (Clusters, Hosts, Resource Pools, Virtual Machines); Troubleshoot and Enhance Performance (pp. 2033-2123)
corrections: []
review_notes:
- 'Whole file: thresholds and actions from the vSphere 9.1 documentation, not the book. The knowledge-base readings are from the existing files linked in each section.'
- 'Section ''Storage latency'': the documentation (4 ms kernel, 15 ms device, queue 0) differs from the book values in vsphere/technology/storage/troubleshooting/host-storage-latency (KAVG 0.5 ms, DAVG within 5 ms).'
- 'To check: Section ''Storage latency'': the 15 ms value comes from spinning-disk arrays (inferred from the remedy text, more spindles).'
- 'Section ''CPU'': the documentation gives VM CPU Ready above 20% with Usage above 90% in the VM chart analysis and in Solutions for Consistently High CPU Usage.'
- 'To check: Section ''Network'': AppSpeed is a discontinued product, so the file says external tools; the documentation names VMware AppSpeed for network latency.'
- 'Omitted as irrelevant or outdated: defragment guest file systems, MemTrimRate=0, separate page-file disk, Fault Tolerance and Memory Mode (PMem) advice.'
status: draft
```
