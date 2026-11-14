# A CPU-bound job on a host under 20%

## Prompt
- The owner of a VM says his single-threaded report job is CPU-bound and runs too slowly.
- The host team answers: "The host is under 20% CPU. It cannot be CPU."
- See [the host CPU chart](0379/vcenter-host-cpu-instances-real-time.png) and [the VM CPU chart](0379/vcenter-vm-cpu-per-vcpu-real-time.png) for the same 15 minutes.

Which statements are correct?

- A. The host's Utilization averages all its threads, so one or two threads near 100% barely move it.
- B. With the host below 20%, no thread was busy enough to slow the job.
- C. One to three CPU instances of the host reach 90-100% while the host stays below 20%.
- D. Busy threads next to idle ones show that the scheduler misbalances the host.
- E. The VM's Readiness below 1% shows its vCPUs found a thread whenever they had work.
- F. One vCPU of the VM runs at about full speed while its siblings stay almost idle.
- G. Move the VM to a less busy host to speed up the job.
- H. Add vCPUs to the VM so that the job runs faster.
- I. The job is held by the speed of the one vCPU it runs on, not by the host's capacity.

## Input to supply
- Product and version: vSphere 9.1 (vSphere Client).
- Object: one ESXi host with Hyper-Threading on and other light load only; one VM on it with 4 vCPUs.
- Screen 1, vSphere Client > the host > Monitor > Performance > Advanced > CPU, Chart Options: Real-time, the last 15 minutes, counter Utilization (%), objects: the host and all CPU instances, with the legend table sorted by Maximum, highest first (the host row and the top instances visible). Save as `0379/vcenter-host-cpu-instances-real-time.png`.
- Screen 2, vSphere Client > the VM > Monitor > Performance > Advanced > CPU, Chart Options: Real-time, the same 15 minutes, counters Usage (MHz) for each vCPU instance and Readiness (%) for the VM, with the legend table. Save as `0379/vcenter-vm-cpu-per-vcpu-real-time.png`.
- How to produce it in a lab: run a single-threaded CPU burner in the VM, pinned to one guest CPU (for example `taskset -c 0 stress-ng --cpu 1` on Linux, or `start /affinity 1` with a one-thread loop on Windows), for at least 15 minutes, on a host where other VMs are quiet.
- Condition the key depends on: host Utilization (%) average below 20% in the window; one to three CPU instances with a Maximum of 90-100%; in the VM, one vCPU instance with Usage (MHz) at or above about the host's base clock and the other vCPUs below 10% of it; VM Readiness below 1%. If the hot thread moves between many instances, shorten the window and capture again.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
B: the host is under 20%, so the CPU cannot be the bottleneck. Or G: move the VM to a quieter host.

## Expected key points
- Answer: A, C, E, F, I.
- A true: host Utilization is the average of thread utilization; one thread at 100% moves it by 100 divided by the thread count (about 3 points on 32 threads).
- B false: the misconception. The per-instance view shows threads at 90-100%; the average hides them.
- C true: reading of the legend's Maximum column against the host row.
- D false: over-correction. Imbalance among threads at low load is normal; one busy vCPU runs on one thread.
- E true: the vCPU did not wait for a thread; the host gave it all the run time it asked for.
- F true: one vCPU instance at about the clock speed, the others near 0.
- G false: wrong action. The VM does not wait (Readiness below 1%), and the host has free threads; another host gives the same one thread.
- H false: the job uses one thread; more vCPUs add idle vCPUs.
- I true: a single busy vCPU is limited by its clock speed; the host's free threads cannot help it.

## Reasoning path
1. Host average below 20%, yet one to three instances at 90-100%: the average hides the hot thread.
2. VM: one vCPU busy at full speed, Readiness low: the job gets its thread and runs as fast as one thread runs.
3. The limit is the job's single thread, not the host.

## Notes
- Paired with the theory question 0378 (theory and practical; design.md, section 3.9).
- Built on the vCenter per-instance chart. The VCF Operations host metric for the busiest core is not used: its presence in VCF Operations 9.1 is not confirmed (fairness F2).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item D5). Counts only after author approval.

## Metadata
```yaml
id: "0379"
title: "A CPU-bound job on a host under 20%"
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
knowledge_main: vsphere/technology/cpu/metrics/host/peak-core-usage
attachments:
  - 0379/vcenter-host-cpu-instances-real-time.png
  - 0379/vcenter-vm-cpu-per-vcpu-real-time.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item D5"
answer: [A, C, E, F, I]
misconception: [B]
misconception_type: [average-hides-worst]
pair: "0378"
status: awaiting-input
```
