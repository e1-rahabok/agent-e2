# Host CPU Usage above 100% at night: evacuate the host?

## Prompt
- At 02:10 an alert fires: the ESXi host esx-prod-11's CPU Usage (%) has passed 100%. The on-call engineer wants to vMotion VMs off it at once.
- The host has 32 cores at a 2.4 GHz base clock, Hyper-Threading on (64 threads), Turbo Boost on, and the Balanced power policy.
- You export [the vCenter CPU chart of the host](0374/vcenter-host-cpu-realtime.csv), Real-time, for the last hour, and [the VCF Operations list of the VMs on the host](0374/vcf-operations-host-vms.csv) with each metric's maximum over the same hour.

Which statements are correct?

- A. The host is out of CPU: move VMs off it now, before the VMs on it slow down.
- B. A Usage value above 100% is a fault in the statistics, to be reported to support.
- C. Where Usage passes 100% in the vCenter export, busy cores mostly ran just one thread.
- D. In the vCenter export, Utilization stays above 75% for most of the hour.
- E. A second thread on a busy core raises Utilization but not that core's Usage.
- F. The VCF Operations list shows that the VMs rarely waited for a physical thread.
- G. Core Utilization near 100% means the host has no room left for more vCPUs.
- H. A second busy thread on a core doubles the work that the core gets done.

## Likely wrong answer
A: Usage above 100% means the host is out of CPU, so evacuate it.

## Expected key points
- Answer: C, E, F.
- A is wrong: the misconception and the wrong action. Usage above 100% is Turbo Boost against the base clock, speed and not a shortage; the VMs do not wait (F).
- B is wrong: the cap of older releases is removed in vCenter (8.0 Update 3, Broadcom KB 417702) and VCF Operations; above 100% is a valid reading.
- C is correct: reading and arithmetic. Per core, Core Utilization adds the time one thread runs and the time both run; Utilization adds half the first and all of the second. In every row where `Usage for esx-prod-11` passes 100, `Core Utilization for esx-prod-11` is 90-98 and `Utilization for esx-prod-11` 52-58, so two-thread time is at most about 23% of core time and one-thread time at least about 69%.
- D is wrong: reading. `Utilization for esx-prod-11` stays at 52-58 in the busy rows and lower before them; never above 75.
- E is correct: ESXi Usage counts a core with one or two busy threads once, so a second thread on a busy core raises its Thread Utilization and leaves its Usage unchanged.
- F is correct: reading. `CPU|Peak vCPU Ready within collection cycle (%) (Max)` is below 1 and `CPU|Peak vCPU Co-Stop within collection cycle (%) (Max)` below 0.5 on every VM row.
- G is wrong: Core Utilization counts a core as fully used when one of its two threads runs; capacity is counted in threads, and about half are free.
- H is wrong: the misconception. A second thread shares the core: Hyper-Threading gives about 1.25 times per core, not 2 times.

## Reasoning path
1. Usage above 100% with Turbo: speed, not overload.
2. Core and thread utilization: cores busy, mostly with one thread each; about half the threads free.
3. VM waits low: nothing to evacuate.

## Notes
- Paired with the theory question 0058 (theory and practical; design.md, section 3.9).
- Usage no longer capped at 100%: Broadcom KB 417702.
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C14). Counts only after author approval.
- Review 2026-11-15: new situation (a night alert and an evacuation) and new wording, away from 0058; condition ranges moved off the knowledge-base example; screen readings D, F, G (true) and E (false); Co-stop added to the VM list so G reads both waits. Key changed from A, D, F, G, I to A, D, F, G, J (new options).
- Changed in the 2026-11-15 audit (cap of two questions per fact; the pair 0058/0374 repeated facts homed in 0366/0101, 0004/0012 and 0019/0431): old A (Usage above 100% is Turbo) and old J (waits are read from Ready and Co-stop) dropped; old D (Core Utilization below 100%) replaced by the one-thread reading, old F (half the threads idle) by the second-thread Usage fact that 0058 F also tests. Letter map: A dropped, B→A, C→B, D→C (new), E→D, F→E (new), G→F, H→G, I→H, J dropped. Key changed from A, D, F, G, J to C, E, F; misconception from B to A. D lengthened ("for most of the hour"), truth unchanged.
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
answer: [C, E, F]
misconception: [A]
misconception_type: [consumption-as-contention, frequency-and-hyper-threading]
pair: "0058"
status: draft
```
