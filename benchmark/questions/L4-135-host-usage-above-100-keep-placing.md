# Host CPU Usage above 100%: stop placing VMs?

## Prompt
- An ESXi 9.1 host with Hyper-Threading on, power policy Balanced.
- The operations manager wants to stop placing VMs on it: "CPU Usage is above 100%. The host is overloaded."
- See [the vSphere Client host chart](0374/vcenter-host-cpu-past-day.png) and [the VCF Operations list of the VMs on the host](0374/vcf-operations-host-vms-peak-ready.png) for the same day.

Which statements are correct?

- A. Usage above 100% means the cores ran above the base clock: Usage is measured against base frequency.
- B. Usage above 100% shows the host is out of CPU, so no more VMs should go on it.
- C. ESXi caps Usage at 100%, so a value above it points to a counter error.
- D. Core Utilization of about 85-95% means some cores ran no thread at all part of the time.
- E. Core Utilization of about 85-95% means that share of the host's capacity is in use.
- F. Utilization (the thread view) of 50-65% leaves about a third or more of the threads free.
- G. Peak vCPU Ready below 2% on every VM shows the VMs get the run time they ask for now.
- H. An idle thread on a busy core gives a new vCPU the speed of a whole free core.
- I. VMs can still be placed here while their Ready and Co-stop stay low, watching Utilization against a planned ceiling.

## Input to supply
- Product and version: vSphere 9.1 (vSphere Client) and VCF Operations 9.1. Host with Hyper-Threading on, Turbo Boost on in the BIOS, power policy Balanced.
- Object: one ESXi host and the VMs on it.
- Screen 1, vSphere Client > the host > Monitor > Performance > Advanced > CPU, Chart Options: Past day (or Real-time over a busy hour), object the host (not the CPU instances), counters Usage (%), Core Utilization (%), Utilization (%), with the legend table (Latest, Maximum, Average). Save as `0374/vcenter-host-cpu-past-day.png`.
- Screen 2, VCF Operations list view of the VMs on the host, columns: name, vCPUs, CPU|Peak vCPU Ready within collection cycle (maximum over the same day). Save as `0374/vcf-operations-host-vms-peak-ready.png`.
- How to produce it in a lab: load the host with VMs running steady CPU burners until most cores run a thread and some run two, while the VMs still get their run time.
- Condition the key depends on: at the busy time, Usage (%) 105-120%, Core Utilization (%) 85-95%, Utilization (%) 50-65%; every VM's maximum Peak vCPU Ready below 2%.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
B: Usage above 100% means the host is out of CPU. Stop placing VMs.

## Expected key points
- Answer: A, D, F, G, I.
- A true: host Usage counts cycles against the base clock and is no longer capped; Turbo Boost lifts it above 100%.
- B false: the misconception and the wrong action. Usage is speed, not capacity; read the utilization counters and VM contention.
- C false: the cap of older releases is removed in vCenter and VCF Operations.
- D true: Core Utilization below 100% means cores with no thread running for part of the time.
- E false: Core Utilization counts a core as fully used when one of its two threads runs; capacity is counted in threads.
- F true: Utilization is the average of thread utilization; 50-65% leaves 35-50% of the threads idle.
- G true: low Ready on every VM: no CPU performance problem now.
- H false: over-correction. A second thread shares the core; Hyper-Threading gives about 1.25 times per core, not 2 times.
- I true: decide by contention as VMs are added; the planned ceiling for thread utilization is set per host, lower at cluster level because of the HA host.

## Reasoning path
1. Usage above 100% with Turbo: speed, not overload.
2. Core and thread utilization: cores busy, threads free.
3. VM Ready low: no contention. Keep placing, watching contention.

## Notes
- Paired with the theory question 0058 (theory and practical; design.md, section 3.9).
- Usage no longer capped at 100%: Broadcom KB 417702.
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C14). Counts only after author approval.

## Metadata
```yaml
id: "0374"
title: "Host CPU Usage above 100%: stop placing VMs?"
product: [vsphere, vcf-operations]
technology: [cpu]
task: decide-capacity
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
  - 0374/vcenter-host-cpu-past-day.png
  - 0374/vcf-operations-host-vms-peak-ready.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C14"
answer: [A, D, F, G, I]
misconception: [B]
misconception_type: [consumption-as-contention, frequency-and-hyper-threading]
pair: "0058"
status: awaiting-input
```
