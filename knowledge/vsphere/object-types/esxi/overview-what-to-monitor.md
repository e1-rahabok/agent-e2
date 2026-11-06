# ESXi: what to monitor, in priority order

## Answers
- Which metrics are most important to monitor on an ESXi (ESX) host: CPU, memory, storage, network, GPU.
- Which host metrics show performance, and which show capacity.

## Principle
- ESXi is a provider. It has no contention of its own: its Ready and Co-stop are sums of its VMs. See `vsphere/foundations/provider-consumer`.
- Host performance is read from the contention of its VMs, at the worst VM. Host-level contention counters average all VMs: lagging, and they hide the VM that suffers. See `vsphere/technology/cpu/metrics/comparisons/host-contention-metrics`.
- Host utilization is capacity, not performance. A host can run at high utilization with no VM waiting, and VMs can wait on a lightly used host.

## 1. Contention of its VMs
- Worst VM CPU Ready and Co-stop, per vCPU. See `vsphere/technology/cpu/metrics/virtual-motherboard/ready`.
- Worst VM memory Latency. Host memory Latency is an average of VMs: use the worst VM. See `vsphere/technology/memory/metrics/host/latency`.
- Storage latency split: KAVG (kernel) vs DAVG (device) vs QAVG (queue). See `vsphere/technology/storage/concepts/esxi-storage-latency-stack` and the flow `vsphere/technology/storage/diagnosis/host-storage-latency`.
- Network: packets dropped and error packets. See `vsphere/technology/network/metrics/host/packets-dropped` and `vsphere/technology/network/metrics/host/errors`.

## 2. CPU capacity
- Primary: Core Utilization and Thread Utilization. Complement with Usage (MHz). See `vsphere/technology/cpu/metrics/host/core-utilization` and `vsphere/technology/cpu/metrics/host/utilization`.
- Usage and Demand can exceed 100% (Turbo; Demand sums VM demand). Not an overload signal on their own. See `vsphere/technology/cpu/metrics/comparisons/host-consumption-metrics`.
- Hot cores and NUMA nodes: Peak Core Usage and Imbalance. See `vcf-operations/metrics/esxi/cpu-peak-core-usage`.
- Flow: `vsphere/technology/cpu/diagnosis/host-cpu-capacity-headroom`.

## 3. Memory capacity
- Consumed is the main capacity counter. It holds guest cache, so high Consumed alone is not a problem. See `vsphere/technology/memory/metrics/host/consumed`.
- Leading warnings: Balloon and State. Past contention: Swap and Compressed. See `vsphere/technology/memory/metrics/comparisons/host-memory-metrics`.
- Memory tiering hosts: active memory against DRAM, NVMe latency. See `vsphere/technology/memory/concepts/memory-tiering`.

## 4. Storage and network consumption
- Device, adapter and path throughput and IOPS. See `vsphere/technology/storage/metrics/host/disk` and `vsphere/technology/storage/metrics/host/adapter-and-path`.
- Network throughput per vmnic. See `vsphere/technology/network/metrics/host/throughput`.

## 5. GPU
- GPU utilization, memory and temperature are statistics level 4 counters: no history at the default level. See `vsphere/technology/gpu/concepts/gpu-monitoring`.

## 6. Context
- Hypervisor overhead (vSAN, NSX, kernel). See `vsphere/foundations/overhead`.
- Power management and BIOS settings change what utilization means. See `vsphere/technology/cpu/configuration/host-power-management` and `vsphere/object-types/esxi/configuration/bios-settings`.

## Documentation guidance (esxtop)
- Performance Best Practices for vSphere 9.1 gives these esxtop readings:
  - esxtop CPU panel, first line (load average): a value equal to or greater than 1 means the system is overloaded.
  - esxtop PCPU line (usage of physical CPUs): 80% is a reasonable ceiling.
  - esxtop PCPU line: 90% should be a warning.
  - The source notes that organizations set their own standards for the target load percentage.
- Knowledge base reading: these are utilization levels, so they are capacity signals. Confirm a performance problem with the contention of the host's VMs (section 1). Load average 1.00 means all PCPUs fully used. See `vsphere/tools/esxtop/cpu`.

## Traps
- "Host CPU at 90%, so VMs are slow" → check worst VM Ready and Co-stop.
- "Host Ready is low, so every VM is fine" → it is an average. Check the worst VM.
- "Demand 130%, so the host is overloaded" → check Core Utilization, Thread Utilization and VM contention.
- "Host memory Consumed at 95%, so add memory" → check balloon, swap-in and worst VM memory Latency.

## Metadata
```yaml
id: vsphere/object-types/esxi/overview-what-to-monitor
retriever_guide: what-to-check
scope: vsphere
technology:
- cpu
- gpu
- memory
- storage
- network
pillar:
- performance
- capacity
product:
- vsphere
object:
- HostSystem
internal_derive:
- vsphere/technology/cpu/metrics/comparisons/host-contention-metrics
- vsphere/technology/cpu/metrics/comparisons/host-consumption-metrics
- vsphere/technology/cpu/diagnosis/host-cpu-capacity-headroom
- vsphere/technology/memory/metrics/comparisons/host-memory-metrics
- vsphere/technology/storage/concepts/esxi-storage-latency-stack
related:
- vsphere/object-types/vm/overview-what-to-monitor
- vsphere/object-types/cluster/overview-what-to-monitor
- vsphere/foundations/provider-consumer
- vsphere/tools/vsphere-client/performance-guidance
- vsphere/tools/esxtop/cpu
source:
  document: Knowledge base synthesis of the linked files (author's book; vSphere 9.1 documentation) + Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: Linked files in each section; section 'Documentation guidance (esxtop)' from ESX CPU Considerations (pp. 27-28)
corrections: []
review_notes:
- 'Whole file: the priority order is Claude''s synthesis of the linked files (contention before consumption before context, README rule). Each statement restates a linked file. Author to confirm the order.'
- 'Section ''Documentation guidance (esxtop)'': moved from vsphere/foundations/overhead (section Host CPU monitoring, 2026-11-04), where a merge had placed it; it is host monitoring, not overhead. Text kept as written.'
status: draft
```
