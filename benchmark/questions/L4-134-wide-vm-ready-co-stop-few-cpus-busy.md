# A 16-vCPU app server waits while a third of it works

## Prompt
- The owner of a 16-vCPU Java application server wants it doubled before the quarter-end peak: "It already waits for CPU, and the developers say Co-stop means our threads block each other."
- See [the VCF Operations chart of the VM](0373/vcf-operations-vm-cpu-7-days.png) for the last 7 days, [the top screen](0373/linux-top-per-cpu.png) from inside the guest at a peak hour, and [the VCF Operations list of the other VMs on its host](0373/vcf-operations-host-vms-ready.png) for the same 7 days.
- The VM fits within one NUMA node of its host and has no snapshot.

Which statements are correct?

- A. In `top`, the guest keeps about 5-6 of its 16 CPUs busy at the peak hour.
- B. Double the VM to 32 vCPUs: the work spreads and each vCPU waits less.
- C. A narrower VM, closer to what the guest uses, needs fewer free threads at once, so its Ready and Co-stop tend to fall.
- D. The Co-stop on the chart shows the application's threads waiting on each other's locks inside the guest.
- E. Co-stop on this VM follows from Ready on its siblings: when one vCPU waits for a thread, the others are held back.
- F. On the chart, Co-stop stays above Ready all week.
- G. The other VMs on the host wait as much as this one: the host is short of CPU.
- H. A downsize lowers Co-stop only; Ready depends on the host alone.
- I. Net Run on the chart matches the CPUs busy in `top`: about a third of the 16 vCPUs.

## Input to supply
- Product and version: VCF Operations 9.1, vSphere 9.1; a Linux guest (for example RHEL 9).
- Object: one VM with 16 vCPUs that fits one NUMA node of its host (at least 16 cores per socket), no snapshot; the host it runs on; the other VMs on that host (2-4 vCPUs each).
- Screen 1, VCF Operations > the VM > Metrics: CPU|Ready (%), CPU|Co-stop (%), CPU|Net Run (%) on one chart, last 7 days, with the values of one peak hour visible on hover. Save as `0373/vcf-operations-vm-cpu-7-days.png`.
- Screen 2, `top` in the guest at a peak hour with the per-CPU view (press `1`): 5 or 6 of the 16 CPU lines busy, the rest near idle. Save as `0373/linux-top-per-cpu.png`.
- Screen 3, VCF Operations list view of the VMs on the same host, columns: name, vCPUs, CPU|Ready (%) maximum over the 7 days. Save as `0373/vcf-operations-host-vms-ready.png`.
- How to produce it in a lab: the 16-vCPU VM running a 5-6 thread load at peak hours on a host where other small VMs keep about half the threads busy. No limits; default shares.
- Condition the key depends on: at the peak hours, the large VM shows Ready 1.5-4%, Co-stop 0.5-2% and below Ready, and Net Run 28-40%; `top` shows 5 or 6 CPUs above 80% busy and the rest below 20%; every other VM on the host has a 7-day maximum Ready below 0.5%.
- Masking: mask every VM, host, datastore and cluster name; mask the guest's host name in the `top` screen if it shows.

## Likely wrong answer
B: the VM waits for CPU, so give it more vCPUs. Or D: Co-stop means the application's threads block each other.

## Expected key points
- Answer: A, C, E, I.
- A true: reading. Five or six CPU lines are busy; the rest are near idle.
- B false: the misconception and wrong action. More vCPUs need more threads free at about the same time: Ready and Co-stop tend to rise.
- C true: the guest uses about a third of its vCPUs; a narrower VM fits free threads more easily.
- D false: Co-stop is a wait in the ESXi scheduler that keeps the vCPUs in step; the guest does not see it, and its own locks do not cause it.
- E true: with the VM inside one NUMA node and no snapshot, the remaining cause of Co-stop is Ready on a sibling vCPU; co-stopped vCPUs stop even when threads are free.
- F false: reading. Co-stop stays below Ready.
- G false: reading. The other VMs barely wait; the wait comes from this VM's width.
- H false: over-correction. Downsizing usually lowers Ready too: fewer vCPUs fit free threads more easily.
- I true: Net Run of 28-40% across 16 vCPUs is about 4.5-6.5 vCPUs of work, as `top` shows.

## Reasoning path
1. `top` and Net Run: about a third of the 16 vCPUs work.
2. The other VMs barely wait: the host is not the problem.
3. Ready and Co-stop come from the VM's width: narrow it, do not double it.

## Notes
- Paired with the theory question 0107 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C11). Counts only after author approval.
- Review 2026-11-15: new situation (16-vCPU Linux application server, a request to double it, the developers' reading of Co-stop) and new wording, away from 0107; NUMA fit and no snapshot added so E is decidable; screen readings F, G (false) and I (true) added. Key changed from A, C, F to A, C, E, I (options relettered).

## Metadata
```yaml
id: "0373"
title: "A 16-vCPU app server waits while a third of it works"
product: [vsphere, vcf-operations, linux]
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
  - 0373/linux-top-per-cpu.png
  - 0373/vcf-operations-host-vms-ready.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C11"
answer: [A, C, E, I]
misconception: [B, D]
misconception_type: [provider-vs-consumer]
pair: "0107"
status: awaiting-input
```
