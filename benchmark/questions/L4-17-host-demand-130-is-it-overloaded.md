# Demand above capacity, Usage above 100%: is the host full?

## Prompt
- An ESXi 9.1 host has 40 cores at a 2.0 GHz base clock (80,000 MHz of capacity) and 80 threads (Hyper-Threading on).
- Over 7 hours, in the vSphere Client:
  - CPU Demand: about 104,000 MHz against 80,000 MHz of capacity. CPU Usage: about 104%.
  - Core Utilization: 85%. Utilization (per thread): 62%.
  - Per VM: Ready about 2%, Co-stop below 0.1%.
- The operations manager wants to stop placing VMs on this host because it is overloaded.

Is the host full? What do you base the answer on?

## Likely wrong answer
"Yes: Demand at 130% of capacity and Usage above 100% mean the host is out of CPU. Stop placing VMs."

## Expected key points
- No CPU performance problem now: Ready about 2% and Co-stop below 0.1% per VM show the VMs get their run time.
- Usage above 100% is Turbo Boost measured against the base clock.
- Demand above Usage is the Hyper-Threading charge that Usage applies and Demand does not; it is not work the host refuses.
- Capacity is read from Core Utilization and Utilization: 85% of cores busy leaves about 6 cores; 62% of threads leaves about 30 threads.
- Decide by contention as VMs are added: keep placing VMs while Ready and Co-stop per VM stay low, and watch Utilization rise toward its planned ceiling.

## Notes
- Revised 2026-11-12: ESXi 9.1 no longer caps host CPU Usage at 100% (the book's example was an older release with a flat 100%); task moved from troubleshoot to decide-capacity, since the question is whether to keep placing VMs.

## Metadata
```yaml
id: "0058"
title: "Demand above capacity, Usage above 100%: is the host full?"
product: [vsphere]
technology: [cpu]
task: decide-capacity
level: 400
answer_type: judged
input: [text]
object: [esxi, vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/cpu/decision-tree/host-cpu-capacity-headroom
  - vsphere/technology/cpu/metrics/host/utilization
  - vsphere/technology/cpu/metrics/host/core-utilization
  - vsphere/technology/cpu/metrics/host/usage
knowledge_main: vsphere/technology/cpu/decision-tree/host-cpu-capacity-headroom
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6); revised 2026-11-12"
misconception_type: [consumption-as-contention, frequency-and-hyper-threading]
status: draft
```
