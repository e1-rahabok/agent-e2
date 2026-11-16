# CPU Latency without contention

## Prompt
- After a host BIOS power policy change, VM CPU Latency went from about 2% to about 17%.
- esxtop power view on the host: %A/MPERF fell from about 100% to about 85% after the change.
- CPU Ready and Co-Stop are unchanged. No limit, reservation or shares were changed on the VM.

Which statements are correct?

- A. CPU Latency includes the effect of running below nominal frequency, so a lower clock raises it.
- B. The rise of about 15 points shows the vCPUs now wait about 15% of the time for a physical CPU.
- C. Each vCPU now runs slower than before, as if the VM had moved to an older CPU.
- D. A lower clock speed adds nothing to the VM's Ready or Co-Stop values.
- E. Like Disk Latency and Memory Latency, CPU Latency measures time the VM waits to be served.
- F. If the guest runs Linux, its Steal Time would rise by about the same amount as CPU Latency.
- G. CPU Latency includes Max Limited, the time a CPU limit holds a vCPU back, so a limit explains the rise.
- H. CPU Latency and CPU Ready track each other closely, so a Latency rise with a flat Ready points to a counting error.
- I. Add two vCPUs to the VM to bring its CPU Latency back to where it was.
- J. At the same Run, the VM's CPU Usage (MHz) is now about 15% lower than before.

## Likely wrong answer
- B: "Latency went up, so the VM is waiting for CPU."
- E: "Latency is latency: for CPU it means the same as for disk and memory."

## Expected key points
- Answer: A, C, D, J.
- A is correct: CPU Latency (%LAT_C) includes power saving below nominal frequency; lower frequency raises it.
- B is wrong: the misconception; the rise of about 15 points is a frequency effect, not time spent waiting. Waiting shows in Ready and Co-Stop, which are flat.
- C is correct: %A/MPERF at about 85% shows the cores run below nominal frequency; at a lower clock the VM runs slower but is not waiting to be served, like on an older CPU.
- D is correct: Ready and Co-Stop count time a vCPU does not run; a lower clock slows a running vCPU and shows in Latency, not in them. So their flat lines show no added waiting.
- E is wrong: Disk Latency and Memory Latency do mean the VM waits; CPU Latency does not always mean a performance problem (same name, different meaning).
- F is wrong: Linux Steal Time includes only Ready; VM CPU Latency includes more factors, frequency among them. Ready is flat, so Steal Time stays flat.
- G is wrong: CPU Latency excludes Max Limited; the time a limit holds a vCPU back shows in Ready, not in Latency. The prompt also rules out a new limit.
- H is wrong: CPU Latency and Ready correlate poorly, since they are built for different purposes; Latency counts Hyper-Threading and frequency, which Ready does not, so Latency can rise with Ready flat (and fall while Ready rises).
- I is wrong: more vCPUs change neither the clock speed nor the Latency of each vCPU, and they make scheduling harder.
- J is correct: Usage (MHz) counts cycles completed and is scaled by frequency; Run counts time only. With %A/MPERF down from about 100% to about 85%, the same run time completes about 15% fewer cycles.

## Notes
- Tests: Same name, different meaning (CPU Latency vs Disk / Memory Latency).
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
- Sharpened stem: no resource setting changed on the VM (rules out a limit for option G). The %A/MPERF line (actual against nominal frequency, named in the latency knowledge file) gives the frequency drop that options C and H need as evidence, not as an inference.
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): C and D no longer negate B; I (the wrong action) added. Key unchanged, A, C, D (author approved, 2026-11-14).
- Paired with 0102 (theory and practical, design.md 3.9).
- 2026-11-16 re-review: H (the same work takes as long) negated C; replaced by a false option of its own fact (Latency and Ready correlate poorly, latency, Use). Key unchanged.
- 2026-11-15 audit: the stem gives the Latency values ("up by about 15%" read as points or as relative); J added (Usage scales with frequency, Run does not), which joins the frequency reading to a second counter.

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
  - vsphere/technology/cpu/metrics/virtual-motherboard/usage
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/latency
attachments: []
origin: book
source_path: "The World of Metrics > Metrics Nuances: Naming Complexity (Same name, different meaning; Same name, same purpose, different formula)."
answer_type: deterministic
answer: [A, C, D, J]
misconception: [B, E]
level: 400                      # author 2026-11-05
misconception_type: [frequency-and-hyper-threading]
pair: "0102"
status: draft
```
