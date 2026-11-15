# CPU Latency without contention

## Prompt
- After a host BIOS power policy change, VM CPU Latency went up by about 15%.
- esxtop power view on the host: %A/MPERF fell from about 100% to about 85% after the change.
- CPU Ready and Co-Stop are unchanged. No limit, reservation or shares were changed on the VM.

Which statements are correct?

- A. CPU Latency includes the effect of running below nominal frequency, so a lower clock raises it.
- B. The 15% rise shows that the vCPUs now wait about 15% longer for a physical CPU to run on.
- C. Each vCPU now runs slower, as if the VM ran on an older CPU.
- D. A lower clock speed adds nothing to Ready or Co-Stop.
- E. Like Disk Latency and Memory Latency, CPU Latency measures time the VM waits to be served.
- F. If the guest runs Linux, its Steal Time would rise by about the same amount as CPU Latency.
- G. CPU Latency includes Max Limited, the time a CPU limit holds a vCPU back, so a limit explains the rise.
- H. Work inside the guest takes as long as before, because only the reported Latency changed.
- I. Add two vCPUs to the VM to bring its CPU Latency back down.

## Likely wrong answer
- B: "Latency went up, so the VM is waiting for CPU."
- E: "Latency is latency: for CPU it means the same as for disk and memory."

## Expected key points
- Answer: A, C, D.
- A is true: CPU Latency (%LAT_C) includes power saving below nominal frequency; lower frequency raises it.
- B is false: the misconception; the rise is a frequency effect, not time spent waiting. Waiting shows in Ready and Co-Stop, which are flat.
- C is true: %A/MPERF at about 85% shows the cores run below nominal frequency; at a lower clock the VM runs slower but is not waiting to be served, like on an older CPU.
- D is true: Ready and Co-Stop count time a vCPU does not run; a lower clock slows a running vCPU and shows in Latency, not in them. So their flat lines show no added waiting.
- E is false: Disk Latency and Memory Latency do mean the VM waits; CPU Latency does not always mean a performance problem (same name, different meaning).
- F is false: Linux Steal Time includes only Ready; VM CPU Latency includes more factors, frequency among them. Ready is flat, so Steal Time stays flat.
- G is false: CPU Latency excludes Max Limited; the time a limit holds a vCPU back shows in Ready, not in Latency. The prompt also rules out a new limit.
- H is false: the VM runs slower at the lower clock, so the same work takes longer; it is a speed change, not contention.
- I is false: more vCPUs change neither the clock speed nor the Latency of each vCPU, and they make scheduling harder.

## Notes
- Tests: Same name, different meaning (CPU Latency vs Disk / Memory Latency).
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
- Sharpened stem: no resource setting changed on the VM (rules out a limit for option G). The %A/MPERF line (actual against nominal frequency, named in the latency knowledge file) gives the frequency drop that options C and H need as evidence, not as an inference.
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): C and D no longer negate B; I (the wrong action) added. Key unchanged, A, C, D (author approved, 2026-11-14).
- Paired with 0102 (theory and practical, design.md 3.9).

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
  - vsphere/technology/cpu/metrics/comparisons/vm-contention-metrics
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/latency
attachments: []
origin: book
source_path: "The World of Metrics > Metrics Nuances: Naming Complexity (Same name, different meaning; Same name, same purpose, different formula)."
answer_type: deterministic
answer: [A, C, D]
misconception: [B, E]
level: 400                      # author 2026-11-05
misconception_type: [frequency-and-hyper-threading]
pair: "0102"
status: draft
```
