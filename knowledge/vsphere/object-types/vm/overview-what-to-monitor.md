# VM: what to monitor, in priority order

## Answers
- Which metrics are most important to monitor on a VM (virtual machine): CPU, memory, storage, network.
- Which VM metrics show performance, and which only show consumption.

## Principle
- A VM is a consumer. Its performance is the runtime, memory, IO and network it demanded and did not get: contention.
- Order: contention first, then consumption, then context. Consumption sizes the VM; it does not show whether the VM suffers.
- Read contention at the 20-second peak, not the 5-minute average: short waits disappear in averages. See `vsphere/object-types/vm/metrics/comparisons/peak-20-second-metrics`.
- The VM is the virtual motherboard. Run queue, page-outs and disk queue inside the guest belong to the Guest OS layer. See `guest-os/system/metrics/guest-os-performance`.

## 1. One score
- VM Performance (%) combines the VM contention metrics into one KPI with colour bands. Start here at scale. See `vsphere/object-types/vm/metrics/vm-performance`.

## 2. CPU contention
- Ready and Co-stop are the main counters. Overlap and Other Wait usually read much lower. See `vsphere/technology/cpu/metrics/comparisons/vm-contention-metrics`.
- Read Ready against Run: 2% Ready on 10% Run is bad; 2% Ready on 98% Run is fine. See `vsphere/technology/cpu/metrics/virtual-motherboard/ready`.
- Co-stop: `vsphere/technology/cpu/metrics/virtual-motherboard/co-stop`.
- Contention (VCF Operations) for troubleshooting CPU-sensitive VMs; it includes limit time. See `vsphere/technology/cpu/metrics/virtual-motherboard/contention`.
- Latency includes Hyper-Threading and frequency effects: not a pure wait. See `vsphere/technology/cpu/metrics/virtual-motherboard/latency`.
- Flow: `vsphere/technology/cpu/diagnosis/vm-cpu-contention-high`.

## 3. Memory contention
- Latency is the only true memory contention counter. See `vsphere/technology/memory/metrics/virtual-motherboard/latency`.
- Then, in order: swap-in, decompression, host cache, balloon. Ballooned, swapped and compressed memory are past reclamation, not current waiting. See `vsphere/technology/memory/metrics/comparisons/vm-memory-metrics`.
- Flow: `vsphere/technology/memory/diagnosis/vm-memory-latency-high`.

## 4. Storage contention
- Disk latency per virtual disk, read and write separately. See `vsphere/technology/storage/metrics/virtual-motherboard/disk-latency`.
- Outstanding IO: queued IO adds latency at any load. See `vsphere/technology/storage/metrics/virtual-motherboard/outstanding-io`.
- Bus resets and commands aborted should stay at 0.
- Flow: `vsphere/technology/storage/diagnosis/vm-storage-performance-checks`.

## 5. Network contention
- Dropped packets are the only network contention metric of a VM. vSphere has no network latency or retransmit counter. See `vsphere/technology/network/metrics/virtual-motherboard/packets-dropped`.
- Flow: `vsphere/technology/network/diagnosis/vnic-rx-drops`.

## 6. Consumption (for sizing)
- CPU: Run, Usage, Demand. Usage includes Turbo; compare with Run before upsizing. See `vsphere/technology/cpu/metrics/comparisons/consumption-metrics`.
- Memory: Consumed is the main counter; size the VM from Guest OS metrics, not VM metrics. See `vsphere/technology/memory/metrics/virtual-motherboard/consumed`.
- Storage: IOPS and throughput. See `vsphere/technology/storage/metrics/virtual-motherboard/iops`.
- Network: throughput. See `vsphere/technology/network/metrics/virtual-motherboard/throughput`.

## 7. Context
- Limits, shares and reservations explain contention the host does not cause. See `vsphere/foundations/resource-controls`.
- vMotion stun time: `vsphere/object-types/vm/metrics/vmotion`.

## Traps
- "VM CPU Usage is 95%, so the VM is short of CPU" → Usage includes Turbo and is consumption. Check Ready, Co-stop and Run.
- "Ballooned memory above 0, so the VM is slow" → balloon is reclamation. Check memory Latency.
- "The 5-minute average is low, so the VM did not wait" → check the 20-second peak.
- "Guest OS run queue is a VM metric" → it is the Guest OS layer.

## Metadata
```yaml
id: vsphere/object-types/vm/overview-what-to-monitor
retriever_guide: what-to-check
scope: vsphere
technology:
- cpu
- memory
- storage
- network
pillar:
- performance
- capacity
product:
- vsphere
- vcf-operations
object:
- VirtualMachine
internal_derive:
- vsphere/technology/cpu/metrics/comparisons/vm-contention-metrics
- vsphere/technology/memory/metrics/comparisons/vm-memory-metrics
- vsphere/technology/storage/diagnosis/vm-storage-performance-checks
- vsphere/technology/network/metrics/comparisons/vm-network-metrics
- vsphere/object-types/vm/metrics/vm-performance
related:
- vsphere/object-types/esxi/overview-what-to-monitor
- vsphere/object-types/cluster/overview-what-to-monitor
- vsphere/object-types/vm/metrics/comparisons/peak-20-second-metrics
- guest-os/system/metrics/guest-os-performance
source:
  document: Knowledge base synthesis of the linked files (author's book; vSphere 9.1 documentation)
  path: Linked files in each section
corrections: []
review_notes:
- 'Whole file: the priority order is Claude''s synthesis of the linked files (contention before consumption before context, README rule). Each statement restates a linked file. Author to confirm the order.'
status: draft
```
