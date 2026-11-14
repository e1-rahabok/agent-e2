# esxtop: the time a vCPU could not run

## Prompt
- An application owner asks how much of the last minutes the vCPUs of his 4-vCPU VM spent unable to run.
- You run esxtop on its host, open the CPU panel and expand the VM with `e`. See [the esxtop screen](0376/esxtop-cpu-vm-states.png).

Which statements are correct?

- A. %RDY on a vcpu world is time it had work and no physical thread to run on.
- B. %CSTP on a vcpu world is time it was held back to stay in step with a sibling.
- C. %SWPWT on a vcpu world is time it stalled for a memory page coming back from ESXi swap.
- D. %OVRLP is time a running vCPU was interrupted for kernel work, so the guest made no progress then.
- E. Most of %WAIT on these vcpu worlds is %IDLE: time the guest had no work.
- F. All of %WAIT is time the vCPUs were held back, so it adds to the VM's CPU wait.
- G. Swap wait has a memory cause, so it is not time the vCPU was stopped.
- H. %MLMTD is 0, so none of the VM's Ready came from a CPU limit.
- I. %USED shows how long each vCPU was stopped.
- J. %RDY is above 0: add vCPUs to the VM.

## Input to supply
- Product and version: ESXi 9.1, esxtop in an SSH session (interactive mode), CPU panel (`c`).
- Object: one VM with 4 vCPUs, expanded with `e` so its vcpu worlds show.
- Screen: the CPU panel with the expanded VM. Fields shown: %USED, %RUN, %SYS, %WAIT, %VMWAIT, %RDY, %IDLE, %OVRLP, %CSTP, %MLMTD, %SWPWT (use `f` to add any missing). Save as `0376/esxtop-cpu-vm-states.png`.
- How to produce it in a lab: a 4-vCPU VM with moderate load on a busy host (other VMs running CPU burners) and memory pressure on the VM so that pages it touches come back from ESXi swap, for example a memory limit well below the memory a load in the guest keeps touching. No CPU limit.
- Condition the key depends on: on the vcpu worlds, %RDY 2-10%, %CSTP above 0.5% on at least one, %SWPWT above 0.5%, %OVRLP above 0; %IDLE within 10 points of %WAIT; %MLMTD 0.00.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
F: all of %WAIT is time lost to the VM. Or G: swap wait is memory, not time the vCPU stopped.

## Expected key points
- Answer: A, B, C, D, E, H.
- A true: Ready is demanded run time the kernel could not give.
- B true: Co-stop holds a vCPU that ran ahead of a sibling.
- C true: the vCPU stalls until the page is read back; the guest sees a freeze.
- D true: Overlap is time stolen from a running vCPU for system services; the guest is frozen during it, even though Run keeps counting.
- E true: %WAIT = %VMWAIT + %IDLE; here %IDLE is nearly all of it.
- F false: the misconception. %IDLE inside %WAIT is the guest's own idle time, not a wait imposed on it.
- G false: over-correction. Swap wait is a stall of the vCPU, whatever its cause; it belongs to memory contention, but the vCPU could not run.
- H true: %MLMTD (Max Limited) is counted inside %RDY; at 0 the Ready is not from a limit.
- I false: %USED is consumption and moves with frequency and Hyper-Threading; it does not measure stopped time.
- J false: wrong action. More vCPUs tend to raise Ready on a busy host.

## Notes
- Paired with the theory question 0009 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C29). Counts only after author approval.

## Metadata
```yaml
id: "0376"
title: "esxtop: the time a vCPU could not run"
product: [vsphere]
technology: [cpu, memory]
task: read-metric
level: 300
answer_type: deterministic
input: [screenshot]
object: [vm]
tool: [esxtop]
knowledge:
  - vsphere/technology/cpu/metrics/comparisons/vm-contention-metrics
  - vsphere/tools/esxtop/cpu
  - vsphere/technology/cpu/metrics/virtual-motherboard/overlap
  - vsphere/technology/cpu/metrics/virtual-motherboard/swap-wait
  - vsphere/technology/cpu/metrics/virtual-motherboard/wait
knowledge_main: vsphere/technology/cpu/metrics/comparisons/vm-contention-metrics
attachments:
  - 0376/esxtop-cpu-vm-states.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C29"
answer: [A, B, C, D, E, H]
misconception: [F]
misconception_type: [consumption-as-contention]
pair: "0009"
status: awaiting-input
```
