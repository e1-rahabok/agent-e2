# Demand 130%, Usage 100%: is the host overloaded?

## Prompt
- An ESXi host has 40 cores and 80 threads (Hyper-Threading on).
- Over 7 hours:
  - CPU Demand: about 130%. CPU Usage: flat at 100%.
  - Core Utilization: 85%. Thread Utilization: 62%.
  - Per VM: Ready about 2%, Co-stop below 0.1%.
- The operations manager wants to stop placing VMs on this host because it is overloaded.

Is the host overloaded? What do you base the answer on?

## Likely wrong answer
"Yes: Demand 130% and Usage 100% mean the host is out of CPU."

## Expected key points
- No CPU performance problem: per-VM Ready about 2% and Co-stop below 0.1% show the VMs get their runtime.
- Check contention first, then Core Utilization and Thread Utilization; Demand and Usage are not the capacity reading.
- Core Utilization 85% leaves about 6 cores free; Thread Utilization 62% leaves about 30 threads free.
- Usage is flat at 100% and Demand above 100% because frequency (Turbo) and Hyper-Threading move them; they do not mean the host refuses work.
- Drive the decision by contention: keep watching Ready and Co-stop as VMs are added.

## Notes
- Previous id: question-0058 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0058"
title: "Demand 130%, Usage 100%: is the host overloaded?"
product: [vsphere, vcf-operations]
technology: [cpu]
task: troubleshoot
level: 400
answer_type: judged
input: [text]
knowledge:
  - vsphere/technology/cpu/health-check/host-cpu-capacity-headroom
  - vsphere/technology/cpu/metrics/host/utilization
  - vsphere/technology/cpu/metrics/host/core-utilization
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
status: draft
```
