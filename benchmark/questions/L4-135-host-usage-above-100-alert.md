# Host CPU Usage above 100% at night: evacuate the host?

## Prompt
- At 02:10 an alert fires: the ESXi host esx-prod-11's CPU Usage (%) has passed 100%. The on-call engineer wants to vMotion VMs off it at once.
- The host has 32 cores at a 2.4 GHz base clock, Hyper-Threading on (64 threads), Turbo Boost on, and the Balanced power policy.
- You export [the vCenter CPU chart of the host](0374/vcenter-host-cpu-realtime.csv), Real-time, for the last hour, and [the VCF Operations list of the VMs on the host](0374/vcf-operations-host-vms.csv) with each metric's maximum over the same hour.

Which statements are correct?

- A. A Usage reading above 100% counts cycles beyond the base clock: Turbo Boost, not demand the host refused.
- B. The host is out of CPU: move VMs off it now.
- C. A Usage value above 100% is a fault in the statistics, to be reported to support.
- D. In the vCenter export, Core Utilization stays below 100%: some cores ran no thread at times.
- E. In the vCenter export, Utilization stays above 75%.
- F. Close to half of the host's threads were idle at the busy time.
- G. The VCF Operations list shows that the VMs rarely waited for a physical thread.
- H. Core Utilization near 100% means the host has no room left for more vCPUs.
- I. A second busy thread on a core doubles that core's throughput.
- J. Whether the VMs suffer is read from their Ready and Co-stop, not from host Usage.

## Likely wrong answer
B: Usage above 100% means the host is out of CPU, so evacuate it.

## Expected key points
- Answer: A, D, F, G, J.
- A true: host Usage counts cycles against the base clock and is no longer capped; Turbo Boost lifts it above 100%. In the vCenter export `Usage for esx-prod-11` is 106-116 from 01:55 on while `Core Utilization for esx-prod-11` is 90-98: Usage above Core Utilization is the clock above base.
- B false: the misconception and the wrong action. Usage measures speed, not a shortage; the VMs do not wait.
- C false: the cap of older releases is removed in vCenter and VCF Operations; above 100% is a valid reading.
- D true: reading. `Core Utilization for esx-prod-11` stays below 100 in every row (at most 98): cores with no thread running for part of the time.
- E false: reading. `Utilization for esx-prod-11` stays at 52-58 in the busy rows and lower before them; never above 75.
- F true: reading. Utilization is the average of thread utilization; at 52-58%, 42-48% of the threads are idle.
- G true: reading. `CPU|Peak vCPU Ready within collection cycle (%) (Max)` is below 1 and `CPU|Peak vCPU Co-Stop within collection cycle (%) (Max)` below 0.5 on every VM row.
- H false: Core Utilization counts a core as fully used when one of its two threads runs; capacity is counted in threads, and about half are free.
- I false: the misconception. A second thread shares the core: Hyper-Threading gives about 1.25 times per core, not 2 times.
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
- Converted to exports 2026-11-15 (project/practical-questions-as-exports-2026-11-15.md): vCenter host CSV and VCF Operations list CSV. C, D, E and G reworded from the chart and screen to the exports; truth unchanged. The VCF Operations list layout is assumed (no captured List export yet).

## Metadata
```yaml
id: "0374"
title: "Host CPU Usage above 100% at night: evacuate the host?"
product: [vsphere, vcf-operations]
technology: [cpu]
task: troubleshoot
level: 400
answer_type: deterministic
input: [table]
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
  - 0374/vcenter-host-cpu-realtime.csv
  - 0374/vcf-operations-host-vms.csv
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C14"
answer: [A, D, F, G, J]
misconception: [B]
misconception_type: [consumption-as-contention, frequency-and-hyper-threading]
pair: "0058"
status: draft
```
