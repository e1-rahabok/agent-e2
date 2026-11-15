# Host CPU Usage above 100% at night: evacuate the host?

## Prompt
- At 02:10 an alert fires: an ESXi host's CPU Usage (%) has passed 100%. The on-call engineer wants to vMotion VMs off it at once.
- The host has Hyper-Threading on, Turbo Boost on, and the Balanced power policy.
- See [the vSphere Client host chart](0374/vcenter-host-cpu-busy-hour.png) and [the VCF Operations list of the VMs on the host](0374/vcf-operations-host-vms-peak-waits.png) for the same hour.

Which statements are correct?

- A. A Usage reading above 100% counts cycles beyond the base clock: Turbo Boost, not demand the host refused.
- B. The host is out of CPU: move VMs off it now.
- C. A Usage line above 100% is a fault in the statistics, to be reported to support.
- D. On the chart, Core Utilization stays below 100%: some cores ran no thread at times.
- E. On the chart, Utilization stays above 75%.
- F. Close to half of the host's threads were idle at the busy time.
- G. The VM list shows that the VMs rarely waited for a physical thread.
- H. Core Utilization near 100% means the host has no room left for more vCPUs.
- I. A second busy thread on a core doubles that core's throughput.
- J. Whether the VMs suffer is read from their Ready and Co-stop, not from host Usage.

## Input to supply
- Product and version: vSphere 9.1 (vSphere Client) and VCF Operations 9.1. Host with Hyper-Threading on, Turbo Boost on in the BIOS, power policy Balanced.
- Object: one ESXi host and the VMs on it.
- Screen 1, vSphere Client > the host > Monitor > Performance > Advanced > CPU, Chart Options: Real-time over a busy hour (or Past day zoomed to it), object the host (not the CPU instances), counters Usage (%), Core Utilization (%), Utilization (%), with the legend table (Latest, Maximum, Average). Save as `0374/vcenter-host-cpu-busy-hour.png`.
- Screen 2, VCF Operations list view of the VMs on the host, columns: name, vCPUs, CPU|Peak vCPU Ready within collection cycle and CPU|Peak vCPU Co-Stop within collection cycle (maximum over the same hour). Save as `0374/vcf-operations-host-vms-peak-waits.png`.
- How to produce it in a lab: load the host with VMs running steady CPU burners until nearly every core runs a thread and a few run two, while the VMs still get their run time.
- Condition the key depends on: in the busy hour, Usage (%) 106-116%, Core Utilization (%) 90-98%, Utilization (%) 52-58%; every VM's maximum Peak vCPU Ready below 1% and Peak vCPU Co-Stop below 0.5%.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
B: Usage above 100% means the host is out of CPU, so evacuate it.

## Expected key points
- Answer: A, D, F, G, J.
- A true: host Usage counts cycles against the base clock and is no longer capped; Turbo Boost lifts it above 100%.
- B false: the misconception and the wrong action. Usage measures speed, not a shortage; the VMs do not wait.
- C false: the cap of older releases is removed in vCenter and VCF Operations; above 100% is a valid reading.
- D true: reading. Core Utilization below 100% means cores with no thread running for part of the time.
- E false: reading. Utilization stays at 52-58%.
- F true: reading. Utilization is the average of thread utilization; at 52-58%, 42-48% of the threads are idle.
- G true: reading. Peak vCPU Ready below 1% and Peak vCPU Co-Stop below 0.5% on every VM.
- H false: Core Utilization counts a core as fully used when one of its two threads runs; capacity is counted in threads, and about half are free.
- I false: over-correction. A second thread shares the core: Hyper-Threading gives about 1.25 times per core, not 2 times.
- J true: Ready and Co-stop are the consumer's wait; host Usage includes frequency and is not a contention reading.

## Reasoning path
1. Usage above 100% with Turbo: speed, not overload.
2. Core and thread utilization: cores busy, about half the threads free.
3. VM waits low: nothing to evacuate.

## Notes
- Paired with the theory question 0058 (theory and practical; design.md, section 3.9).
- Usage no longer capped at 100%: Broadcom KB 417702.
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C14). Counts only after author approval.
- Review 2026-11-15: new situation (a night alert and an evacuation) and new wording, away from 0058; condition ranges moved off the knowledge-base example; screen readings D, F, G (true) and E (false); Co-stop added to the VM list so G reads both waits. Key changed from A, D, F, G, I to A, D, F, G, J (new options).

## Metadata
```yaml
id: "0374"
title: "Host CPU Usage above 100% at night: evacuate the host?"
product: [vsphere, vcf-operations]
technology: [cpu]
task: troubleshoot
level: 400
answer_type: deterministic
input: [screenshot]
object: [esxi, vm]
tool: [vcenter, vcf-operations]
knowledge:
  - vsphere/technology/cpu/decision-tree/host-cpu-capacity-headroom
  - vsphere/technology/cpu/metrics/host/usage
  - vsphere/technology/cpu/metrics/host/core-utilization
  - vsphere/technology/cpu/metrics/host/utilization
  - vsphere/technology/cpu/concepts/hyper-threading
knowledge_main: vsphere/technology/cpu/decision-tree/host-cpu-capacity-headroom
attachments:
  - 0374/vcenter-host-cpu-busy-hour.png
  - 0374/vcf-operations-host-vms-peak-waits.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C14"
answer: [A, D, F, G, J]
misconception: [B]
misconception_type: [consumption-as-contention, frequency-and-hyper-threading]
pair: "0058"
status: awaiting-input
```
