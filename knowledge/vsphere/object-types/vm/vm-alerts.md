# VM alerts

## Coverage and receivers
- A VM is a consumer: its alerts catch what the VM owner would feel. A VM is a virtual motherboard; the alerts on the Guest OS above it are a separate set ([`guest-os/guest-os-alerts`](../../../guest-os/guest-os-alerts.md)).
- Alerted: CPU contention and consumption, memory contention, disk read latency and disk write latency, network dropped packets.
- Every value (threshold, wait, gate) is in the alert rows of [`catalog/thresholds-alerts.yaml`](../../../catalog/thresholds-alerts.yaml), shown with this file. This file says why each symptom is in the alert.
- Receivers: the infrastructure team gets red and orange; the application team gets red only. The infrastructure team also watches the same VMs through the ESXi, resource pool and cluster contention alerts, with lower per-VM values on a share of the VMs, so it can act before the application team is alerted ([`sp5-framework/outputs/alert-design`](../../../sp5-framework/outputs/alert-design.md), section Application team vs infrastructure team).
- Activity gate: every contention alert also needs VM CPU Usage above a floor. At low activity the business impact is likely negligible; CPU usage is the proxy for application activity. The floor is in GHz, not %: a small percentage of a monster VM is still a sizable load.
- Acute and sustained: each contention alert pairs a 20-second peak (acute) with a 5-minute average (sustained), as the threshold design asks ([`sp5-framework/outputs/alert-design`](../../../sp5-framework/outputs/alert-design.md), section Threshold design). Orange halves every red value: red is 2x orange in the set.
- One policy for every VM: the set has no per-class values. A site with classes of service makes one policy per class; the step between classes: [`sp5-framework/outputs/alert-design`](../../../sp5-framework/outputs/alert-design.md), section Class of service.

## VM CPU contention
- Detects: the VM asked for CPU time and did not get it.
- VM Peak vCPU Ready, the worst vCPU in the worst 20 seconds: the acute part. Ready lasts seconds, so the 5-minute value alone misses it ([`vsphere/technology/cpu/metrics/virtual-motherboard/ready`](../../technology/cpu/metrics/virtual-motherboard/ready.md)).
- VM CPU Ready, 5-minute: the sustained part.
- VM CPU Usage: the activity gate.
- No VM CPU Contention symptom. Contention is Ready plus Co-stop, Overlap and small Other Wait, so it is never below Ready; tested at the Ready value it adds nothing ([`vsphere/technology/cpu/metrics/virtual-motherboard/contention`](../../technology/cpu/metrics/virtual-motherboard/contention.md)). Co-stop is read as insight and in the flow.
- Use it with VM CPU consumption. A consumer can be given capacity at a moment's notice, but adding vCPUs while the VM has contention makes its performance worse.
- Remediation: [`vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high`](../../technology/cpu/troubleshooting/vm-cpu-contention-high.md).

## VM CPU consumption
- Detects: the VM uses all its CPU and work queues inside the Guest OS. High utilization slows the business, above all online workloads where users expect a real-time response.
- VM CPU Net Run: the VM runs near its full capacity ([`vsphere/technology/cpu/metrics/virtual-motherboard/net-run`](../../technology/cpu/metrics/virtual-motherboard/net-run.md)).
- Guest OS CPU Queue: threads wait for a vCPU. Net Run alone also flags a VM that runs at full speed by design; the queue shows a real bottleneck ([`guest-os/cpu/metrics/run-queue`](../../../guest-os/cpu/metrics/run-queue.md)).
- Red only: an orange consumption alert adds false positives; early warning belongs to the daily dashboard.
- A longer wait than the contention alerts: fewer false positives, and the alert comes that much later.
- Remediation:
  1. VM CPU contention also fired: follow it first.
  2. Find the nature of the application. A batch job can hold Net Run near full for its whole run; if it finishes within its window, it is healthy. Exclude it from the alert.
  3. Ask the application team which application or transaction metrics show queueing and latency. If they match the infrastructure numbers, add vCPUs, keeping the VM NUMA-aligned ([`vsphere/technology/cpu/configuration/numa-settings`](../../technology/cpu/configuration/numa-settings.md)).

## VM memory contention
- Detects: the VM's vCPUs waited for memory pages. It measures time lost, not memory missing.
- VM Peak Memory Contention, 20-second: the acute part.
- VM Memory Contention, 5-minute: the sustained part ([`vsphere/technology/memory/metrics/virtual-motherboard/latency`](../../technology/memory/metrics/virtual-motherboard/latency.md)).
- VM CPU Usage: the activity gate.
- Remediation: [`vsphere/technology/memory/vm-memory-latency-high`](../../technology/memory/vm-memory-latency-high.md).

## Memory contention: mixed causes
- A limit, swap-in, decompression and low shares can act at once. The metric gives the total wait, not each cause's share, so the flow checks each cause.
- It is time, not memory: a few hot pages swapped out can stall a VM more than many cold ones.

## VM disk read latency and VM disk write latency
- Read and write are separate alerts: their causes usually differ, so their remediation differs.
- Average latency of the direction, 5-minute: the sustained part ([`vsphere/technology/storage/metrics/virtual-motherboard/disk-latency`](../../technology/storage/metrics/virtual-motherboard/disk-latency.md)).
- VM Peak Disk Latency, 20-second: the acute part. It covers read and write together, a known limit of the 20-second peak ([`vcf-operations/features/peak-20-second-metrics`](../../../vcf-operations/features/peak-20-second-metrics.md)).
- VM CPU Usage and the IOPS of the direction: activity gates. They cut alerts during low activity, where business impact is likely negligible ([`vsphere/technology/storage/metrics/virtual-motherboard/iops`](../../technology/storage/metrics/virtual-motherboard/iops.md)).
- The values are higher and the wait longer than vendor best practice. Lower values are right in theory, but they draw hardly any complaints, and investment is hard to justify without complaints ([`sp5-framework/observability/thresholds`](../../../sp5-framework/observability/thresholds.md)).
- Remediation: [`vsphere/technology/storage/troubleshooting/vm-storage-performance-checks`](../../technology/storage/troubleshooting/vm-storage-performance-checks.md).

## VM dropped packets
- Detects: transmitted packets the VM dropped, as a share of the packets it transmitted ([`vsphere/technology/network/metrics/virtual-motherboard/packets-dropped`](../../technology/network/metrics/virtual-motherboard/packets-dropped.md)).
- VM CPU Usage: the activity gate, as in the other VM contention alerts. A drop ratio over few packets is unstable: a handful of drops at low throughput gives a large share.
- Transmitted only: received drops are far higher and include packets not destined for the VM and drops in a full receive ring, whose cause is in the Guest OS.
- Red only, as on every network object, to avoid alert storms. TCP resends a dropped segment, so the data arrives in the end; the cost is time, as each loss shrinks the congestion window or waits for a retransmit timeout. UDP is not resent.
- The value is set high because it is read within a 20-second period.
- Planned change: make the threshold relative to the packets transmitted.

## Not alerted
- Memory consumption: a VM is a virtual motherboard. Whether its memory is enough is a Guest OS question, and the right value differs per application.
- Disk space: a Guest OS question ([`guest-os/guest-os-alerts`](../../../guest-os/guest-os-alerts.md), section Consumption: daily checks, no alert).
- Network consumption: not yet in the set. A network has no clear 100%, so the ceiling is hard to set.

## Misconceptions
- "High VM CPU usage: add vCPUs" → check contention first; adding vCPUs to a VM with contention makes it worse.
- "CPU Ready above 8% alone is red" → the VM alert also requires the 20-second Peak vCPU Ready and the CPU Usage gate.
- "Add VM CPU Contention to the Ready alert" → Contention is never below Ready; at the same value it adds nothing.
- "Use CPU Usage % to filter idle VMs" → a small % of a monster VM is a large load; the gate is in GHz.
- "Net Run at 95% is a problem" → a batch job runs at full speed by design. The Guest OS CPU Queue shows the bottleneck.
- "Alert on VM memory usage" → a VM is a virtual motherboard; memory sufficiency is a Guest OS question with no common threshold.
- "Memory contention tells which cause dominates" → limit, swap, compression and shares mix; the split cannot be read from the metric.
- "Memory contention of 51% means half the memory is missing" → it is time a vCPU waited, not memory.
- "One latency alert for read and write" → causes differ; the set has separate read and write alerts.
- "VM disk latency above 20 ms is red" → the set alerts far higher, on the 5-minute average and the 20-second peak together; lower values draw no complaints in practice.
- "Alert on latency at any load" → the CPU Usage and IOPS gates keep the alert off idle VMs; low activity has negligible impact.
- "The peak latency in the alert is read latency" → the 20-second peak covers read and write together.
- "4% dropped is low" → it is a high drop rate, set high only because it is read over 20 seconds.
- "Every dropped packet loses data" → TCP resends it; the cost is time, not data. UDP is not resent.
- "Alert on network utilization" → a network has no clear maximum, so the ceiling is hard to set.

## Metadata
```yaml
id: vsphere/object-types/vm/vm-alerts
retriever_guide: what-to-set
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
- vcf-operations
object:
- VirtualMachine
internal_derive:
- sp5-framework/outputs/alert-design
- vsphere/technology/cpu/metrics/virtual-motherboard/ready
- vsphere/technology/cpu/metrics/virtual-motherboard/contention
- vsphere/technology/cpu/metrics/virtual-motherboard/usage
- vsphere/technology/cpu/metrics/virtual-motherboard/net-run
- guest-os/cpu/metrics/run-queue
- vsphere/technology/memory/metrics/virtual-motherboard/latency
- vsphere/technology/storage/metrics/virtual-motherboard/disk-latency
- vsphere/technology/storage/metrics/virtual-motherboard/iops
- vcf-operations/features/peak-20-second-metrics
- vsphere/technology/network/metrics/virtual-motherboard/packets-dropped
- vsphere/technology/network/concepts/packet-drop-accounting
related:
- vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high
- vsphere/technology/memory/vm-memory-latency-high
- vsphere/technology/storage/troubleshooting/vm-storage-performance-checks
- vsphere/technology/cpu/configuration/numa-settings
- guest-os/guest-os-alerts
- vsphere/object-types/esxi/esxi-alerts
- vcf-operations/alert-definitions
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'Proactive Operations > Alert > VM Alerts; CPU Alerts > Contention Alerts > VM Contention; Consumption Alerts > VM Consumption; Memory Alerts > Contention Alerts > VM Contention; Storage Alerts > Contention Alerts > VM Contention; Network Alerts > Contention Alerts'
corrections:
- 'Section ''VM CPU contention'': the source''s red and orange also test VM CPU Contention above 8%. Dropped: Contention is never below Ready (VCF Operations 8.18 formula), so it adds nothing next to Ready. The source''s orange keeps the red Peak vCPU Ready (32%); halved to 16%, as red is 2x orange on every value of the set (Q140, Q144).'
- 'Section ''VM dropped packets'': the source condition ends with "and", a second condition missing. The VM CPU Usage gate of the other VM contention alerts added (Q147).'
- 'Section ''Memory contention: mixed causes'': the source example (51% contention from 5 MB limited, 1 MB swapped, 2 MB compressed) dropped: contention is time, not memory size, so the MB values cannot add up to it (Q145).'
review_notes: []
status: draft
```
