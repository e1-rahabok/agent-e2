# CPU Ready on a busy VM and a quiet VM

## Prompt
- Two VMs run on the same busy ESXi 9.1 host. vCenter, the same 20-second sample, per vCPU:
  - db-07 (8 vCPUs): Readiness 4.2%, Run 88%.
  - web-14 (2 vCPUs): Readiness 1.8%, Run 6%.
- The team alerts when Readiness passes 3% per vCPU. Only db-07 raised an alert.

Which statements about CPU Ready and these two readings are correct?

- A. Ready counts time a vCPU had work to run and found no physical thread free to run it on.
- B. For the guest, time in Ready is frozen time that stretches the elapsed time of its work.
- C. What Ready costs a VM depends on how much it runs: the wait is weighed per unit of run time.
- D. web-14 waits about 30 ms for every 100 ms it runs; db-07 about 5 ms.
- E. db-07 has the higher Readiness, so its work suffers more from Ready than the work of web-14.
- F. A VM that runs more than 85% of the time cannot be slowed down by Ready, whatever its value.
- G. Add a vCPU to web-14, so that each vCPU carries less of its load and waits less.
- H. Read Ready from the 5-minute average, since a Ready problem builds up over minutes.
- I. Readiness (%) is normalized by the vCPU count, so the 8-vCPU and the 2-vCPU VM compare on one scale.

## Likely wrong answer
E: db-07 is over the alert level and web-14 is well below it, so db-07 is the VM that suffers.

## Expected key points
- Answer: A, B, C, D, I.
- A true: Ready is demanded run time the kernel could not give, for want of a physical thread.
- B true: the guest is not told; its clock jumps when the vCPU runs again, so the work takes longer.
- C true: Ready is read against Run. A flat threshold reads the same wait as equally bad on a busy and a quiet VM.
- D true: 1.8 / 6 = 0.30 and 4.2 / 88 = 0.048.
- E false: the misconception. db-07 loses about 5% against its run time, web-14 about 30%.
- F false: over-correction. Read against Run, Ready on a busy VM is mild, not harmless: very high Ready with high Usage gives poor performance.
- G false: more vCPUs make a VM harder to schedule on a busy host and tend to raise Ready.
- H false: Ready usually lasts seconds; the 20-second peak shows it, a 5-minute average dilutes it.
- I true: the % counter divides by the vCPU count; Ready (ms) sums over the vCPUs and does not compare across VM sizes.

## Notes
- Paired with the practical question 0106 (theory and practical; design.md, section 3.9). Situation numbers differ from 0106 on purpose.
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item B1). Counts only after author approval.

## Metadata
```yaml
id: "0364"
title: "CPU Ready on a busy VM and a quiet VM"
product: [vsphere]
technology: [cpu]
task: read-metric
level: 300
answer_type: deterministic
input: [text]
object: [vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/technology/cpu/concepts/vcpu-states
  - vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/ready
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item B1"
answer: [A, B, C, D, I]
misconception: [E]
misconception_type: [threshold-transplanted]
pair: "0106"
status: draft
```
