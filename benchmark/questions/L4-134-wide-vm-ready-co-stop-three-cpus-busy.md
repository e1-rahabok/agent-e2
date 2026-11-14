# A 24-vCPU VM waits while 3 CPUs work

## Prompt
- The owner of a 24-vCPU database VM says it waits for CPU and asks for 8 more vCPUs.
- See [the VCF Operations chart of the VM](0373/vcf-operations-vm-cpu-7-days.png) for the last 7 days, [the Task Manager screen](0373/task-manager-logical-processors.png) from inside the guest at a busy hour, and [the VCF Operations list of the other VMs on its host](0373/vcf-operations-host-vms-ready.png) for the same 7 days.

Which statements are correct?

- A. At the busy hours the guest keeps about 3 of its 24 CPUs busy.
- B. Add the 8 vCPUs, so that the work spreads and each vCPU waits less.
- C. Reduce the VM toward what the guest uses: fewer vCPUs fit into free physical threads more easily.
- D. A downsize would lower Co-stop but not Ready, since Ready depends only on the host's load.
- E. Co-stop shows the database threads waiting on each other inside the guest.
- F. Co-stop here follows from Ready: when one vCPU waits for a thread, its siblings are held back to stay in step.
- G. The host is short of CPU: move the other VMs off it first.
- H. By default a smaller VM gets fewer shares per vCPU, so after a downsize each vCPU would wait longer.
- I. Ready and Co-stop of a few percent are too small to matter, whatever the VM's run time.

## Input to supply
- Product and version: VCF Operations 9.1, vSphere 9.1; Windows Server guest.
- Object: one VM with 24 vCPUs; the host it runs on; the other VMs on that host (2-4 vCPUs each).
- Screen 1, VCF Operations > the VM > Metrics: CPU|Ready (%), CPU|Co-stop (%), CPU|Net Run (%) on one chart, last 7 days, with the values of one busy hour visible on hover. Save as `0373/vcf-operations-vm-cpu-7-days.png`.
- Screen 2, Task Manager > Performance > CPU, graph changed to Logical processors, at a busy hour: 3 of the 24 processor graphs busy, the rest near 0. Save as `0373/task-manager-logical-processors.png`.
- Screen 3, VCF Operations list view of the VMs on the same host, columns: name, vCPUs, CPU|Ready (%) maximum over the 7 days. Save as `0373/vcf-operations-host-vms-ready.png`.
- How to produce it in a lab: a 24-vCPU VM running a 3-thread load on a host with about 32-48 physical threads, where other small VMs keep about half the threads busy. No limits; default shares.
- Condition the key depends on: at the busy hours, the large VM shows Ready 2-6%, Co-stop 1-4% and Net Run 8-15%, with Ready plus Co-stop at least a quarter of Net Run; Task Manager shows 3 (2 to 4) busy logical processors; every other VM on the host has a 7-day maximum Ready below 0.5%.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
B: the VM waits for CPU, so give it more vCPUs. Or G: the host is short of CPU.

## Expected key points
- Answer: A, C, F.
- A true: Task Manager shows 3 busy logical processors; Net Run of 8-15% across 24 vCPUs is 2-4 vCPUs of work.
- B false: the misconception and wrong action. More vCPUs need more threads free at about the same time: Ready and Co-stop tend to rise.
- C true: the guest uses about 3 CPUs; a smaller VM is easier to schedule, so Ready and Co-stop fall.
- D false: over-correction. Downsizing usually lowers Ready too: fewer vCPUs fit free threads more easily.
- E false: Co-stop is a wait in the ESXi scheduler, not inside the guest.
- F true: Ready on one vCPU leads to Co-stop on its siblings; co-stopped vCPUs stop even when threads are free.
- G false: the other VMs barely wait; the wait comes from this VM's width.
- H false: default shares are per vCPU; each vCPU keeps its share after a downsize.
- I false: read against run time. Ready plus Co-stop at a quarter or more of Net Run is a large share of the time the VM works.

## Reasoning path
1. Task Manager and Net Run: about 3 vCPUs of work on 24.
2. The other VMs barely wait: the host is not the problem.
3. Ready and Co-stop come from the VM's width: downsize.

## Notes
- Paired with the theory question 0107 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C11). Counts only after author approval.

## Metadata
```yaml
id: "0373"
title: "A 24-vCPU VM waits while 3 CPUs work"
product: [vsphere, vcf-operations, windows]
technology: [cpu]
task: decide-capacity
level: 400
answer_type: deterministic
input: [screenshot]
object: [vm, esxi, guest-os]
tool: [vcf-operations, guest-os-tools]
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/co-stop
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/technology/cpu/concepts/vcpu-states
  - vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/co-stop
attachments:
  - 0373/vcf-operations-vm-cpu-7-days.png
  - 0373/task-manager-logical-processors.png
  - 0373/vcf-operations-host-vms-ready.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C11"
answer: [A, C, F]
misconception: [B, G]
misconception_type: [provider-vs-consumer]
pair: "0107"
status: awaiting-input
```
