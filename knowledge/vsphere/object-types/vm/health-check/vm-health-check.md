# VM: health check

## Answers
- Is this VM (virtual machine) healthy? Which VM metrics matter most, in what order: CPU, memory, storage, network.
- Which VM metrics show performance, and which only show consumption.

## Symptom
- None. A scheduled or on-demand check of one VM: the what. A failed step opens a troubleshooting flow: the why.
- A user complaint ("the VM is slow") counts as a failed health check: start at `sp5-framework/performance/troubleshooting/vm-slow-triage`.

## Flow
```mermaid
flowchart TD
  S1[1. Availability: future] --> S2[2. VM Performance green?]
  S2 -->|no| S3[3. CPU contention]
  S3 --> S4[4. Memory contention]
  S4 --> S5[5. Storage contention]
  S5 --> S6[6. Network contention]
  S2 -->|yes| S7[7. Guest OS health check]
  S6 --> S7
  S7 --> S8[8. Configuration]
  S8 --> S9[9. Efficiency: sizing]
```

## Principle
- A VM is a consumer. Its performance is the runtime, memory, IO and network it demanded and did not get: contention.
- Order: contention first, then consumption, then context. Consumption sizes the VM; it does not show whether the VM suffers.
- Read contention at the 20-second peak, not the 5-minute average: short waits disappear in averages. See `vsphere/tools/vcf-operations/peak-20-second-metrics`.
- The VM is the virtual motherboard. Run queue, page-outs and disk queue inside the guest belong to the Guest OS layer. See `guest-os/system/metrics/guest-os-performance`.

## Checks, in order
Order of `sp5-framework/concepts/health-risk-efficiency`: present health (availability, performance, security), then risk (capacity, configuration, compliance), then efficiency.
1. Availability (VirtualMachine). Future, after 1.0: VM down, restarted by HA, unresponsive; mostly from logs and events. State what was not checked. → step 2.
2. Performance: VM Performance (%) (VirtualMachine). Combines the VM contention metrics into one KPI with colour bands. Start here at scale (`vsphere/object-types/vm/kpis/vm-performance`). Green → step 7. Yellow or worse → step 3, and read only the resources whose sub-metric fails.
3. CPU contention (VirtualMachine). Ready and Co-stop are the main counters; Overlap and Other Wait usually read much lower (`vsphere/technology/cpu/metrics/comparisons/vm-contention-metrics`). Read Ready against Run: 2% Ready on 10% Run is bad; 2% Ready on 98% Run is fine (`vsphere/technology/cpu/metrics/virtual-motherboard/ready`). Co-stop: `vsphere/technology/cpu/metrics/virtual-motherboard/co-stop`. Contention (VCF Operations) includes limit time (`vsphere/technology/cpu/metrics/virtual-motherboard/contention`). Latency includes Hyper-Threading and frequency effects: not a pure wait (`vsphere/technology/cpu/metrics/virtual-motherboard/latency`). High → `vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high`. → step 4.
4. Memory contention (VirtualMachine). Latency is the only true memory contention counter (`vsphere/technology/memory/metrics/virtual-motherboard/latency`). Then, in order: swap-in, decompression, host cache, balloon. Ballooned, swapped and compressed memory are past reclamation, not current waiting (`vsphere/technology/memory/metrics/comparisons/vm-memory-metrics`). High → `vsphere/technology/memory/troubleshooting/vm-memory-latency-high`. → step 5.
5. Storage contention (VirtualMachine). Disk latency per virtual disk, read and write separately (`vsphere/technology/storage/metrics/virtual-motherboard/disk-latency`). Outstanding IO: queued IO adds latency at any load (`vsphere/technology/storage/metrics/virtual-motherboard/outstanding-io`). Bus resets and commands aborted should stay at 0. High → `vsphere/technology/storage/troubleshooting/vm-storage-performance-checks`. → step 6.
6. Network contention (VirtualMachine). Dropped packets are the only network contention metric of a VM; vSphere has no network latency or retransmit counter (`vsphere/technology/network/metrics/virtual-motherboard/packets-dropped`). Receive drops → `vsphere/technology/network/troubleshooting/vnic-rx-drops`. → step 7.
7. Guest OS (Guest OS layer). Guest OS Performance (%): run queue, disk queue, free memory, page-out rate (`guest-os/system/metrics/guest-os-performance`). A separate layer: the VM can be green while the Guest OS waits on its own queues. → step 8.
8. Configuration (VirtualMachine). `vsphere/object-types/vm/configuration/vm-configuration-review`. Also the drill-down when an earlier step failed: a configuration issue can cause an availability, performance or security problem, and known bugs are mostly configuration (older version, incompatible settings). Limits, shares and reservations explain contention the host does not cause (`vsphere/architecture/resource-controls`). vMotion stun time: `vsphere/object-types/vm/metrics/vmotion`. → step 9.
9. Efficiency (VirtualMachine). Consumption sizes the VM:
   - CPU: Run, Usage, Demand. Usage includes Turbo; compare with Run before upsizing (`vsphere/technology/cpu/metrics/comparisons/consumption-metrics`). Oversized: `vsphere/technology/cpu/health-check/oversized-vm-downsizing`.
   - Memory: Consumed is the main counter; size the VM from Guest OS metrics, not VM metrics (`vsphere/technology/memory/metrics/virtual-motherboard/consumed`).
   - Storage: IOPS and throughput (`vsphere/technology/storage/metrics/virtual-motherboard/iops`). Network: throughput (`vsphere/technology/network/metrics/virtual-motherboard/throughput`).
   - Idle VM: `vsphere/technology/cpu/metrics/virtual-motherboard/idle-vm`.
- Not checked in 1.0: security and compliance (future phase).

## Why this order
- Availability first: a VM that is down has no performance problem.
- Contention before consumption: consumption sizes the VM; it does not show whether the VM suffers.
- VM before Guest OS: contention is waiting the hypervisor imposes, which the Guest OS cannot see.
- Efficiency last: sizing is done when there is no problem.

## How to read the result
- Present health, risk and efficiency are read separately, never as one score.
- VM Performance green, Guest OS Performance red → the VM gets what it demands; the Guest OS or the application waits on its own queues.

## Traps
- "VM CPU Usage is 95%, so the VM is short of CPU" → Usage includes Turbo and is consumption. Check Ready, Co-stop and Run.
- "Ballooned memory above 0, so the VM is slow" → balloon is reclamation. Check memory Latency.
- "The 5-minute average is low, so the VM did not wait" → check the 20-second peak.
- "Guest OS run queue is a VM metric" → it is the Guest OS layer.

## Metadata
```yaml
id: vsphere/object-types/vm/health-check/vm-health-check
retriever_guide: health-check
scope: vsphere
technology:
- cpu
- memory
- storage
- network
pillar:
- availability
- performance
- capacity
- value
product:
- vsphere
- vcf-operations
object:
- VirtualMachine
internal_derive:
- sp5-framework/concepts/health-risk-efficiency
- vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high
- vsphere/technology/memory/troubleshooting/vm-memory-latency-high
- vsphere/technology/network/troubleshooting/vnic-rx-drops
- vsphere/object-types/vm/configuration/vm-configuration-review
- vsphere/technology/cpu/metrics/comparisons/vm-contention-metrics
- vsphere/technology/memory/metrics/comparisons/vm-memory-metrics
- vsphere/technology/storage/troubleshooting/vm-storage-performance-checks
- vsphere/technology/network/metrics/comparisons/vm-network-metrics
- vsphere/object-types/vm/kpis/vm-performance
related:
- sp5-framework/performance/troubleshooting/vm-slow-triage
- vsphere/object-types/esxi/health-check/esxi-health-check
- vsphere/object-types/cluster/health-check/cluster-health-check
- vsphere/tools/vcf-operations/peak-20-second-metrics
- guest-os/system/metrics/guest-os-performance
source:
  document: Knowledge base synthesis of the linked files (author's book; vSphere 9.1 documentation)
  path: Linked files in each section
corrections:
- 'Whole file: author decisions 2026-11-08: "what to monitor" is a health check; troubleshooting is part of the health check and comes after it; availability, security and compliance are future, after 1.0.'
review_notes:
- 'Section ''Checks, in order'': the order of the pillars follows health-risk-efficiency (book); the order inside performance (CPU, memory, storage, network) is Claude''s synthesis of the linked files. Author to confirm (Q062).'
- 'Moved 2026-11-08 from vsphere/object-types/vm/overview-what-to-monitor.'
status: draft
```
