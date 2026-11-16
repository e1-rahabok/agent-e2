# esxtop: the time a vCPU could not run

## Prompt
- An application owner asks how much of the last minutes the vCPUs of his 4-vCPU VM erp-05 spent unable to run.
- You run esxtop on its host, open the CPU panel and expand the VM with `e`:

```text
(generated)
```

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
- K. %SWPWT reads 0 on every vcpu world, so memory plays no part here.

## Likely wrong answer
F: all of %WAIT is time lost to the VM. Or G: swap wait is memory, not time the vCPU stopped.

## Expected key points
- Answer: A, B, C, D, E, H.
- A true: Ready is demanded run time the kernel could not give. The vcpu worlds show %RDY of 3-8.
- B true: Co-stop holds a vCPU that ran ahead of a sibling.
- C true: the vCPU stalls until the page is read back; the guest sees a freeze.
- D true: Overlap is time stolen from a running vCPU for system services; the guest is frozen during it, even though Run keeps counting.
- E true: reading. On each `vmx-vcpu-N:erp-05` row %WAIT = %VMWAIT + %IDLE; %WAIT is 45 or more and %IDLE is within 6 points of it, so %IDLE is most of it.
- F false: the misconception. %IDLE inside %WAIT is the guest's own idle time, not a wait imposed on it.
- G false: over-correction. Swap wait is a stall of the vCPU, whatever its cause; it belongs to memory contention, but the vCPU could not run.
- H true: reading. %MLMTD (Max Limited) is counted inside %RDY; it is 0.00 on the group row and every world, so the Ready is not from a limit.
- I false: %USED is consumption and moves with frequency and Hyper-Threading; it does not measure stopped time.
- J false: wrong action. More vCPUs tend to raise Ready on a busy host.
- K false: reading. %SWPWT is 0.80 or more on every vcpu world: the vCPUs stall on pages coming back from swap.

## Notes
- Paired with the theory question 0009 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C29). Counts only after author approval.
- Review 2026-11-15: condition now requires %WAIT of 40% or more (E decidable); screen reading K (false) added. Key unchanged: A, B, C, D, E, H.
- Converted to exports 2026-11-15 (project/practical-questions-as-exports-2026-11-15.md): the esxtop CPU panel as text, with %VMWAIT (E reads %WAIT = %VMWAIT + %IDLE). No option changed. E, H and K are the options only the panel decides; A-D repeat the pair's facts (open finding of the 2026-11-15 review, left to the author).

## Metadata
```yaml
id: "0376"
title: "esxtop: the time a vCPU could not run"
product: [vsphere]
technology: [cpu, memory]
task: read-metric
level: 300
answer_type: deterministic
input: [text]
object: [vm]
tool: [esxtop]
knowledge:
  - vsphere/technology/cpu/metrics/comparisons/vm-contention-metrics
  - vsphere/tools/esxtop/cpu
  - vsphere/technology/cpu/metrics/virtual-motherboard/overlap
  - vsphere/technology/cpu/metrics/virtual-motherboard/swap-wait
  - vsphere/technology/cpu/metrics/virtual-motherboard/wait
knowledge_main: vsphere/technology/cpu/metrics/comparisons/vm-contention-metrics
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C29"
answer: [A, B, C, D, E, H]
misconception: [F]
misconception_type: [consumption-as-contention]
pair: "0009"
status: draft
```
