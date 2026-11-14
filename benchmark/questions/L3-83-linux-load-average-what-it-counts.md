# Linux load average: what it counts

## Prompt
- A Linux VM has 4 vCPUs.
- The application owner runs `uptime` and reads: load average: 6.20, 5.90, 4.10.
- He asks whether the VM is short of CPU.

Which statements about the Linux load average are correct?

- A. It counts the tasks that are running or waiting to run, plus the tasks in uninterruptible sleep, which usually wait for disk IO.
- B. It counts only the threads waiting for a vCPU, so here about two threads queue for a vCPU at all times.
- C. It is a count for the whole Guest OS, not a figure per vCPU.
- D. A Linux load average of 1.00 means the same as an esxtop load average of 1.00.
- E. Each figure is an exponentially decaying average of that count, sampled every 5 seconds, over 1, 5 or 15 minutes.
- F. A load average above the vCPU count always points to IO wait, never to a CPU queue.
- G. Add 4 vCPUs, so that the load average falls below the vCPU count.
- H. The load average can stay above the vCPU count while the vCPUs sit mostly idle.

## Likely wrong answer
B: the load average read as the CPU queue, so 6.20 on 4 vCPUs means the VM is short of CPU. Or G, the action that follows from it.

## Expected key points
- Answer: A, C, E, H.
- A true: the load average counts tasks in state R (running or runnable) and in state D (uninterruptible sleep, usually waiting for disk IO).
- B false: the misconception. Tasks waiting for IO are in the count too, so the figure alone does not show a CPU queue; the run queue (`r` in vmstat) and per-vCPU time do.
- C true: the count is not divided by the vCPU count; it is read against it.
- D false: esxtop normalises its load average to the physical CPUs (1.00 = all PCPUs busy) and counts running and ready worlds; the Linux figure is a count of R and D tasks, not divided by anything.
- E true: the kernel samples the count every 5 seconds and keeps three exponentially decaying averages, so the 1-minute figure still carries older samples.
- F false: the over-correction. Runnable tasks are part of the count; a load above the vCPU count with every vCPU busy and a long run queue is a CPU queue.
- G false: the wrong action. The load includes tasks waiting for IO; more vCPUs do not make a disk answer faster. Read the run queue and per-vCPU time first.
- H true: tasks blocked on IO raise the load while the vCPUs idle; a high load with idle vCPUs points to IO, not CPU.

## Notes
- Theory half of 0260 (pair: design.md, section 3.9). Different numbers from 0260, so one does not give away the other.
- Sources: Linux man-pages 6.19, proc_loadavg(5) (state R or state D, averaged over 1, 5 and 15 minutes); Linux kernel source, kernel/sched/loadavg.c (exponentially decaying average of nr_running + nr_uninterruptible) and include/linux/sched/loadavg.h (LOAD_FREQ, 5-second intervals). https://man7.org/linux/man-pages/man5/proc_loadavg.5.html
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item B3). Counts only after author approval.

## Metadata
```yaml
id: "0428"
title: "Linux load average: what it counts"
product: [linux, vsphere]
technology: [cpu, storage]
task: explain-mechanism
level: 300
answer_type: deterministic
input: [text]
object: [guest-os]
tool: [guest-os-tools, esxtop]
knowledge:
  - guest-os/system/troubleshooting/linux-os-slow
  - guest-os/cpu/metrics/run-queue
  - vsphere/tools/esxtop/cpu
knowledge_main: guest-os/system/troubleshooting/linux-os-slow
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item B3"
answer: [A, C, E, H]
misconception: [B, G]
misconception_type: [same-name-other-object, unit-and-normalization]
pair: "0260"
status: draft
```
