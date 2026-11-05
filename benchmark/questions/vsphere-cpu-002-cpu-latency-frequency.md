# CPU Latency without contention

## Prompt
- After a host BIOS power policy change, VM CPU Latency went up by about 15%.
- CPU Ready and Co-Stop are unchanged.

Is the VM now suffering a CPU performance problem?

## Likely wrong answer
"Yes, latency means the VM is waiting for CPU."

## Expected key points
- CPU Latency is affected by **CPU frequency**. Lower frequency raises it.
- The VM is running at a lower speed, but it is **not waiting to be served**. Like running on an older CPU.
- Unlike Disk Latency and Memory Latency, CPU Latency does not *always* mean a performance problem.
- Contrast: Linux Steal Time only includes CPU Ready. VM CPU Latency includes more factors, including frequency.
- Ready and Co-Stop being flat supports "no contention".

## Notes
- Tests: Same name, different meaning (CPU Latency vs Disk / Memory Latency).

## Metadata
```yaml
id: vsphere-cpu-002
title: "CPU Latency without contention"
product: [vsphere]
technology: [cpu]
input: [text]
task: read-metric
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/latency
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/foundations/vm-vs-guest-os
attachments: []
origin: book
source_path: "The World of Metrics > Metrics Nuances: Naming Complexity (Same name, different meaning; Same name, same purpose, different formula)."
answer_type: judged
level: 400                      # author 2026-11-05
status: draft
```
