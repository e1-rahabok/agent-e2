# A CPU-bound report job on a host under 15%

## Prompt
- The owner of a reporting VM says the nightly report job is slow and CPU-bound.
- The host team answers: "That host is under 15% CPU. It is not CPU."
- See [the host CPU chart](0379/vcenter-host-cpu-instances-real-time.png), [the VM CPU chart](0379/vcenter-vm-cpu-per-vcpu-real-time.png) for the same 15 minutes, and [the host's hardware summary](0379/vcenter-host-summary-hardware.png).

Which statements are correct?

- A. The host line averages all of the host's threads, so one or two threads near 100% move it by only a few points.
- B. The legend shows no CPU instance above 50% at any time in the window.
- C. The host is under 15%, so the job cannot be held back by CPU.
- D. The VM chart shows the job's work spread evenly over all its vCPUs.
- E. The VM's Readiness stays low: its busy vCPU rarely waited for a thread.
- F. The job runs as fast as one vCPU can go: its speed is set by one thread's clock, not by the host's free capacity.
- G. Move the VM to an emptier host to speed up the job.
- H. The busy vCPU's Usage (MHz) above the host's base clock is Turbo Boost on its core.

## Input to supply
- Product and version: vSphere 9.1 (vSphere Client).
- Object: one ESXi host with Hyper-Threading on, 48 or more logical processors, and other light load only; one VM on it with 4 vCPUs.
- Screen 1, vSphere Client > the host > Monitor > Performance > Advanced > CPU, Chart Options: Real-time, the last 15 minutes, counter Utilization (%), objects: the host and all CPU instances, with the legend table sorted by Maximum, highest first (the host row and the top instances visible). Save as `0379/vcenter-host-cpu-instances-real-time.png`.
- Screen 2, vSphere Client > the VM > Monitor > Performance > Advanced > CPU, Chart Options: Real-time, the same 15 minutes, counters Usage (MHz) for each vCPU instance and Readiness (%) for the VM, with the legend table. Save as `0379/vcenter-vm-cpu-per-vcpu-real-time.png`.
- Screen 3, vSphere Client > the host > Summary, the Hardware card: CPU model, base clock (GHz), logical processors. Save as `0379/vcenter-host-summary-hardware.png`.
- How to produce it in a lab: run a single-threaded CPU burner in the VM, pinned to one guest CPU (for example `taskset -c 0 stress-ng --cpu 1` on Linux, or `start /affinity 1` with a one-thread loop on Windows), for at least 15 minutes, on a host where other VMs are quiet.
- Condition the key depends on: host Utilization (%) average below 10% in the window; one or two CPU instances with a Maximum of 95-100%; in the VM, one vCPU instance with Usage (MHz) above the host's base clock and the other vCPUs below 10% of it; VM Readiness below 1%. If the hot thread moves between many instances, shorten the window and capture again.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
C: the host is under 15%, so the CPU cannot be the bottleneck. Or G: move the VM to a quieter host.

## Expected key points
- Answer: A, E, F, H.
- A true: host Utilization is the average of thread utilization; with 48 or more threads, one thread at 100% moves it by about 2 points or less.
- B false: reading. One or two instances reach 95-100% in the legend's Maximum column.
- C false: the misconception. The host average hides the hot threads that the per-instance view shows.
- D false: reading. One vCPU carries the work; the others stay below a tenth of it.
- E true: reading. Readiness below 1%: the host gave the vCPU nearly all the run time it asked for.
- F true: a single busy vCPU is limited by its clock speed; the host's free threads cannot help it.
- G false: wrong action. The VM does not wait for a thread, and another host gives the same one thread; only a faster clock or a job that uses more threads speeds it up.
- H true: reading. Usage (MHz) above the base clock on one vCPU means its core runs above base frequency.

## Reasoning path
1. Host average below 10%, yet one or two instances at 95-100%: the average hides the hot thread.
2. VM: one vCPU busy above the base clock, Readiness low: the job gets its thread and runs as fast as one thread runs.
3. The limit is the job's single thread, not the host.

## Notes
- Paired with the theory question 0378 (theory and practical; design.md, section 3.9).
- Built on the vCenter per-instance chart. The VCF Operations host metric for the busiest core is not used: its presence in VCF Operations 9.1 is not confirmed (fairness F2).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item D5). Counts only after author approval.
- Review 2026-11-15: condition moved off the knowledge-base example (host below 10%, one or two threads at 95-100%, 48 threads or more); host summary added for the base clock and thread count; screen readings B, D (false) and H (true); E reads "rarely waited". Key changed from A, C, E, F, I to A, E, F, H (new options).

## Metadata
```yaml
id: "0379"
title: "A CPU-bound report job on a host under 15%"
product: [vsphere]
technology: [cpu]
task: troubleshoot
level: 400
answer_type: deterministic
input: [screenshot]
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
  - 0379/vcenter-host-cpu-instances-real-time.png
  - 0379/vcenter-vm-cpu-per-vcpu-real-time.png
  - 0379/vcenter-host-summary-hardware.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D5"
answer: [A, E, F, H]
misconception: [C]
misconception_type: [average-hides-worst]
pair: "0378"
status: awaiting-input
```
