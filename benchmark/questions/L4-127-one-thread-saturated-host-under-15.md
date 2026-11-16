# A CPU-bound report job on a host under 15%

## Prompt
- The owner of the reporting VM rpt-db-02 (4 vCPUs) says the nightly report job is slow and CPU-bound.
- The host team answers: "That host is under 15% CPU. It is not CPU."
- The host esx-rpt-03, from PowerCLI:

```text
Name                 : esx-rpt-03
ProcessorType        : Intel(R) Xeon(R) Gold 5317 CPU @ 3.00GHz
NumCpu               : 24
CpuTotalMhz          : 71832
HyperthreadingActive : True
```

- You export [the vCenter CPU chart of the host with all CPU instances](0379/vcenter-host-cpu-instances-realtime.csv) and [the vCenter CPU chart of the VM with its vCPU instances](0379/vcenter-vm-cpu-realtime.csv), Real-time, for the same 10 minutes while the job runs.

Which statements are correct?

- A. The host value averages its threads: one thread near 100% moves it by about 2 points.
- B. In the host export, no CPU instance passes 50% at any time in the window.
- C. The host is under 15% CPU, so the job cannot be held back by the CPU at all.
- D. The VM export shows the job's work spread evenly over all its vCPUs.
- E. The VM's Readiness stays low: its busy vCPU rarely waited for a thread.
- F. One saturated thread is a performance finding; it says nothing about the host's free threads.
- G. Move the VM to an emptier host so that the job gets more CPU and runs faster.
- H. In the host export the saturated thread changes once, from one instance to another.
- I. The VM's Usage (%) of about 30% shows that the VM has CPU to spare for the job.

## Likely wrong answer
C: the host is under 15%, so the CPU cannot be the bottleneck. Or I: the VM is at 30%, so it has CPU to spare. Or G: move the VM to a quieter host.

## Expected key points
- Answer: A, E, F, H.
- A true: host Utilization is the average of thread utilization; with 48 threads (24 cores, Hyper-Threading active), one thread at 100% moves it by about 2 points (100 / 48). `Utilization for esx-rpt-03` stays below 10 in every row and equals the mean of the 48 instance columns.
- B false: reading. `Utilization for 13` is 95-100 in the first part of the window and `Utilization for 37` in the rest: the hot thread moved once.
- C false: the misconception. The host average hides the hot threads that the per-instance columns show.
- D false: reading. `Usage in MHz for 0` carries the work (3,250-3,550 MHz); `Usage in MHz for 1` to `3` stay below 300 MHz, a tenth of the base clock.
- E true: reading. `Readiness for rpt-db-02` stays below 1% in every row: the host gave the vCPU nearly all the run time it asked for.
- F true: the busiest thread is read for performance, a hot thread that the host average hides; it is not a capacity reading, since one busy thread says nothing about the free threads of the host.
- G false: wrong action. The VM does not wait for a thread (Readiness below 1%, E), so an emptier host has no CPU time to add; the job already gets the one thread it uses.
- H true: reading. `Utilization for 13` is the busiest instance until about 01:26 and `Utilization for 37` after it: the vCPU moved to another thread once, and the reading (one saturated thread) stays the same.
- I false: the misconception. The VM value averages its four vCPUs: `Usage in MHz for 0` runs above the 3,000 MHz base clock (Turbo on an otherwise idle core) while the other three stay below 300 MHz, so `Usage for rpt-db-02` near 30% hides one saturated vCPU.

## Reasoning path
1. Host average below 10%, yet one or two instances at 95-100%: the average hides the hot thread.
2. VM: one vCPU busy above the base clock, Readiness low: the job gets its thread and runs as fast as one thread runs.
3. The limit is the job's single thread, not the host.

## Notes
- Paired with the theory question 0378 (theory and practical; design.md, section 3.9).
- Built on the vCenter per-instance chart. The VCF Operations host metric for the busiest core is not used: its presence in VCF Operations 9.1 is not confirmed (fairness F2).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item D5). Counts only after author approval.
- Review 2026-11-15: condition moved off the knowledge-base example (host below 10%, one or two threads at 95-100%, 48 threads or more); host summary added for the base clock and thread count; screen readings B, D (false) and H (true); E reads "rarely waited". Key changed from A, C, E, F, I to A, E, F, H (new options).
- Changed in the 2026-11-15 audit: H (Usage above base is Turbo, tested in 0366 and 0101) replaced by the reading that the hot thread moved (0378 H is the theory side); I added, the whole-VM average as the misconception; A and F shortened (the correct options were the longest).
- Changed 2026-11-16 (re-review): F (one thread's clock sets the job's speed, not free host capacity) rested on a mechanism no knowledge file states; replaced by the performance-not-capacity reading of the busiest thread (peak-core-usage, Meaning), still true. G's key point now rests on Readiness (ready). The single-thread mechanism remains a knowledge-base gap (also 0378 F).
- Converted to exports 2026-11-15 (project/practical-questions-as-exports-2026-11-15.md): host CSV with the host and 48 instance columns, cut to 30 rows (10 minutes); VM CSV per vCPU; host hardware as PowerCLI text. A, B, D and H reworded from line, legend, chart and the Usage (MHz) label to the exports; truth unchanged.

## Metadata
```yaml
id: "0379"
title: "A CPU-bound report job on a host under 15%"
product: [vsphere]
technology: [cpu]
task: troubleshoot
level: 400
answer_type: deterministic
input: [table]
object: [esxi, vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/cpu/metrics/host/peak-core-usage
  - vsphere/technology/cpu/metrics/host/utilization
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/technology/cpu/metrics/virtual-motherboard/usage-disparity
  - vsphere/technology/cpu/metrics/virtual-motherboard/usage
knowledge_main: vsphere/technology/cpu/metrics/host/peak-core-usage
attachments:
  - 0379/vcenter-host-cpu-instances-realtime.csv
  - 0379/vcenter-vm-cpu-realtime.csv
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D5"
answer: [A, E, F, H]
misconception: [C, I]
misconception_type: [average-hides-worst]
pair: "0378"
status: draft
```
