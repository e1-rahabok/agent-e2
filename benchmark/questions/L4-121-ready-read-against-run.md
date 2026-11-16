# CPU Ready on a busy VM and a quiet VM

## Prompt
- Two VMs run on the same busy ESXi 9.1 host. vCenter, the same 20-second sample, per vCPU:
  - db-07 (8 vCPUs): Readiness 4.2%, Run 88%.
  - web-14 (2 vCPUs): Readiness 1.8%, Run 6%.
- The team alerts when Readiness passes 3% per vCPU. Only db-07 raised an alert.

Which statements about CPU Ready and these two readings are correct?

- A. A guest whose processes keep waking and sleeping tends to collect more Ready than a busy one.
- B. For the guest, time in Ready is frozen time that stretches how long its work takes.
- C. What Ready costs a VM depends on how much it runs: weigh the wait per unit of run time.
- D. web-14 waits about 30 ms for every 100 ms it runs; db-07 about 5 ms.
- E. db-07 has the higher Readiness, so its work suffers more from Ready than the work of web-14.
- F. Ready no longer slows a VM's work once the VM runs more than 85% of the time.
- G. db-07, over the team's alert level, is the VM to protect first: reserve CPU for it.
- H. Read Ready from the 5-minute average: a Ready problem builds up over several minutes.
- I. Readiness (%) is normalized by vCPU count, so the 8-vCPU and 2-vCPU VMs compare on one scale.

## Answers
A, B, C, D, I

## Explanation
- A is correct: every wake-up is a scheduling event, and Ready includes scheduling cost, so a guest that keeps waking and sleeping collects more Ready than one that stays busy.
- B is correct: the guest is not told; its clock jumps when the vCPU runs again, so the work takes longer.
- C is correct: Ready is read against Run. A flat threshold reads the same wait as equally bad on a busy and a quiet VM.
- D is correct: 1.8 / 6 = 0.30 and 4.2 / 88 = 0.048.
- E is wrong: the misconception. db-07 loses about 5% against its run time, web-14 about 30%.
- F is wrong: over-correction. Read against Run, Ready on a busy VM is mild, not harmless: very high Ready with high Usage gives poor performance.
- G is wrong: wrong action. Read against Run, db-07's wait is low (about 5 ms per 100 ms of run, like Ready 5% on Run 95%); web-14 is the VM whose work is delayed. Reservations and limits are kept to a minimum: they make operations more complex.
- H is wrong: Ready usually lasts seconds; the 20-second peak shows it, a 5-minute average dilutes it.
- I is correct: the % counter divides by the vCPU count; Ready (ms) sums over the vCPUs and does not compare across VM sizes.
- Misconception: E: db-07 is over the alert level and web-14 is well below it, so db-07 is the VM that suffers.

## Notes
- 2026-11-16 (author, Q251): level 300 to 400 (the Level 400 example of KNOWLEDGE-ENGINEERING.md section 4).
- Paired with the practical question 0106 (theory and practical; design.md, section 3.9). Situation numbers differ from 0106 on purpose.
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item B1). Counts only after author approval.
- Review 2026-11-15: option G now a wrong action of its own (a reservation for the VM over the alert level), away from 0106. Key unchanged: A, B, C, D, I.
- 2026-11-15 audit: A (Ready is demanded run time with no thread free, tested by the pair 0009/0376) replaced in place by another true fact of ready, Floor and size (wake-and-sleep guests collect more Ready). F, G, H reworded without absolutes or because clauses (truth kept); G's key point rests on ready, Read against Run and resource-controls ("Minimise use of limit and reservation"). db-07's Ready was not given in ms: converting VM-level ms per vCPU is at the two-question cap (0105/0369).

## Metadata
```yaml
id: "0364"
title: "CPU Ready on a busy VM and a quiet VM"
product: [vsphere]
technology: [cpu]
task: read-metric
level: 400                      # Q251, author 2026-11-16: relabelled as written (was 300)
answer_type: deterministic
input: [text]
object: [vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/technology/cpu/concepts/vcpu-states
  - vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high
  - vsphere/architecture/resource-controls
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/ready
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item B1"
misconception: [E]
misconception_type: [threshold-transplanted]
pair: "0106"
status: draft
```
