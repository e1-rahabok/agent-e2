# Guest OS run queue alert on a 16-vCPU VM

## Prompt
- VCF Operations 9.1. The team's red alert "Guest OS CPU run queue" fires when, for 3 consecutive collection cycles, Guest|Peak vCPU Queue within collection cycle is above 20 and VM CPU Net Run is above 75%.
- The team also runs a VM CPU contention alert and a VM CPU consumption alert. Neither fired on this VM in the evening below.
- VM win-app-21: Windows Server 2022, 16 vCPUs. Collection cycles 19:10 to 19:25:

| Cycle | Guest\|Peak vCPU Queue within collection cycle | Guest\|CPU Queue | CPU Net Run (%) | Peak vCPU Ready within collection cycle (%) |
|---|---|---|---|---|
| 19:10 | 22 | 9 | 81 | 0.8 |
| 19:15 | 24 | 11 | 84 | 0.6 |
| 19:20 | 26 | 12 | 83 | 0.7 |

- Performance Monitor inside the guest at the same minutes: System \ Processor Queue Length 350-420. Processor(_Total): % Processor Time 85-90%, % Privileged Time 60-65%, % User Time 22-27%. Every vCPU shows 80-92% Processor Time.
- The application owner says: "PerfMon shows 400 threads waiting and VCF Operations shows 24: the alert's metric is broken." A colleague proposes adding 16 vCPUs.

Which statements are correct?

- A. VCF Operations shows the guest's queue divided by the 16 vCPUs, so 22-26 is about 350-420 threads, in line with PerfMon.
- B. The alert threshold of 20 is a total of 20 threads for the VM, so the alert should have fired long before the queue reached 400.
- C. The 5-minute Guest|CPU Queue of 9-12 is also per vCPU: on average about 140-190 threads waited during each cycle.
- D. As neither VM CPU alert fired, the next step is to find why the guest keeps so many threads ready.
- E. Privileged Time far above User Time points to kernel work, such as drivers or interrupts, not to the application.
- F. Add 16 vCPUs: at 32 vCPUs the same queue reads 11-13 per vCPU, under the alert threshold, which fixes the problem.
- G. A Guest OS queue this long shows that ESXi does not give the VM enough CPU time.
- H. Threads blocked on a lock (a mutex or semaphore) wait in the processor queue, so a lock alone can explain the 400.
- I. A peak of 26 per vCPU is within the normal range for a 16-vCPU Windows VM, so the alert is a false positive to suppress.

## Answers
A, C, D, E

## Explanation
- A is correct: both VCF Operations queue metrics are the guest's total queue divided by the vCPU count. 22 × 16 = 352 and 26 × 16 = 416, the PerfMon range.
- B is wrong: the symptom reads the per-vCPU value, so 20 means 20 × 16 = 320 threads on this VM; the value is set high on purpose so that the alert fires only on an extreme queue.
- C is correct: Guest|CPU Queue is the mean of the 15 twenty-second samples, per vCPU: 9 × 16 = 144 and 12 × 16 = 192 threads.
- D is correct: when the alert fires and neither the VM CPU contention nor the consumption alert did, the cause is in the guest: why the application or kernel keeps so many threads ready.
- E is correct: high Privileged Time with low User Time means the kernel (drivers, interrupts, DPCs) uses the CPU, not the application: a driver or kernel-locking problem.
- F is wrong: the halving assumes the total queue stays the same across the resize, which it does not (Windows counts waiting threads only, and the runnable threads move too); and more vCPUs do not remove the kernel work that creates the queue.
- G is wrong: Peak vCPU Ready is under 1%, so ESXi gave the vCPUs their time; the queue is a Guest OS reading and the cause lies there.
- H is wrong: a thread blocked on a lock is in the Wait state; it joins the queue only when the lock is released.
- I is wrong: about 400 ready threads on 16 vCPUs is an extreme queue; PerfMon's own text treats under 10 per processor as normally acceptable.
- Misconception: B: "20 is a total, so VCF Operations and PerfMon disagree and the metric is broken." G reads the Guest OS queue as an ESXi shortage; F is the action that follows; I is the over-correction.

## Notes
- The alert values are the team's rule, given in the prompt (benchmark/design.md, section 6.1 F3).
- The consumption alert of the team needs Net Run above 95%; with Net Run at 81-84% it did not fire although the 5-minute queue is high. The prompt states only that neither alert fired.

## Metadata
```yaml
id: "0468"
title: "Guest OS run queue alert on a 16-vCPU VM"
product: [vcf-operations, windows, vsphere]
technology: [cpu]
task: troubleshoot
level: 400
answer_type: deterministic
input: [text]
object: [vm, guest-os]
tool: [vcf-operations, guest-os-tools]
knowledge:
  - guest-os/guest-os-alerts
  - guest-os/cpu/metrics/run-queue
  - guest-os/cpu/windows-cpu-scheduling
knowledge_main: guest-os/guest-os-alerts
attachments: []
origin: synthetic
source_path: "Synthetic, 2026-11-15, question bank audit gap: guest-os/guest-os-alerts"
misconception: [B, G]
misconception_type: [unit-and-normalization, layer-confusion]
status: draft
```
