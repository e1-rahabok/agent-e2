# CPU Latency without contention

## Prompt
- After a host BIOS power policy change, VM CPU Latency went up by about 15%.
- CPU Ready and Co-Stop are unchanged. No limit, reservation or shares were changed on the VM.

Which statements are correct?

- A. CPU Latency includes the effect of running below nominal frequency, so a lower clock raises it.
- B. The 15% rise shows that the vCPUs now wait about 15% longer for a physical CPU to run on.
- C. The VM runs slower per vCPU but is not waiting to be scheduled, as if it ran on an older CPU.
- D. Unchanged Ready and Co-Stop show that the vCPUs do not wait longer for a physical thread.
- E. Like Disk Latency and Memory Latency, CPU Latency measures time the VM waits to be served.
- F. If the guest runs Linux, its Steal Time would rise by about the same amount as CPU Latency.
- G. CPU Latency counts the time a CPU limit holds the vCPU back, so a limit would explain the rise.
- H. Work inside the guest takes as long as before, because only the reported Latency changed.

## Likely wrong answer
- B: "Latency went up, so the VM is waiting for CPU."
- E: "Latency is latency: for CPU it means the same as for disk and memory."

## Expected key points
- Answer: A, C, D.
- A is true: CPU Latency (%LAT_C) includes power saving below nominal frequency; lower frequency raises it.
- B is false: the misconception; the rise is a frequency effect, not time spent waiting. Waiting shows in Ready and Co-Stop, which are flat.
- C is true: at a lower clock the VM runs slower but is not waiting to be served, like on an older CPU.
- D is true: flat Ready and Co-Stop support no added contention.
- E is false: Disk Latency and Memory Latency do mean the VM waits; CPU Latency does not always mean a performance problem (same name, different meaning).
- F is false: Linux Steal Time includes only Ready; VM CPU Latency includes more factors, frequency among them. Ready is flat, so Steal Time stays flat.
- G is false: CPU Latency excludes Max Limited; a limit shows in Ready, not in Latency. The prompt also rules out a new limit.
- H is false: the VM runs slower at the lower clock, so the same work takes longer; it is a speed change, not contention.

## Notes
- Tests: Same name, different meaning (CPU Latency vs Disk / Memory Latency).
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
- Sharpened stem: no resource setting changed on the VM (rules out a limit for option G).

## Metadata
```yaml
id: "0002"
title: "CPU Latency without contention"
product: [vsphere]
technology: [cpu]
input: [text]
task: read-metric
object: [vm, esxi]
tool: [vcenter]
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/latency
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/architecture/vm-vs-guest-os
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/latency
attachments: []
origin: book
source_path: "The World of Metrics > Metrics Nuances: Naming Complexity (Same name, different meaning; Same name, same purpose, different formula)."
answer_type: deterministic
answer: [A, C, D]
misconception: [B, E]
level: 400                      # author 2026-11-05
misconception_type: [frequency-and-hyper-threading]
status: draft
```
