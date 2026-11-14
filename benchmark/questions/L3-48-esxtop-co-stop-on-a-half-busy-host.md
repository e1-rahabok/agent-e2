# esxtop Co-stop on a host at half load

## Prompt
- A database team says their 16-vCPU VM stalls for short moments.
- You run esxtop on its host, open the CPU panel and expand the VM's group with `e`. See [the esxtop screen](0375/esxtop-cpu-vm-expanded.png).

Which statements are correct?

- A. A vCPU in Co-stop is held back to stay in step with a sibling vCPU that has fallen behind.
- B. The %CSTP values show the host had no free physical thread for these vCPUs.
- C. The 1-vCPU VMs on the screen show %CSTP 0 because Co-stop needs sibling vCPUs.
- D. While a vCPU is co-stopped, its physical thread can run another VM.
- E. %CSTP is time the vCPU waits for disk IO to complete.
- F. Co-stop and Ready are unrelated counters: one never leads to the other.
- G. Add vCPUs to the VM to spread the stalls over more of them.
- H. Fewer vCPUs on this VM would tend to lower its Co-stop.

## Input to supply
- Product and version: ESXi 9.1, esxtop in an SSH session (interactive mode), CPU panel (`c`).
- Object: one VM with 16 vCPUs (12-24 is fine), expanded with `e` so its vcpu worlds show; at least two 1-vCPU VMs visible on the same screen.
- Screen: the CPU panel with the header lines (PCPU USED(%), PCPU UTIL(%)) and the expanded VM. Fields shown: %USED, %RUN, %SYS, %WAIT, %RDY, %IDLE, %OVRLP, %CSTP, %MLMTD (use `f` to add any missing). Save as `0375/esxtop-cpu-vm-expanded.png`.
- How to produce it in a lab: run a multi-thread load in the 16-vCPU VM on a host that is about half busy with other burners, so that vCPUs of the large VM sometimes find no free thread.
- Condition the key depends on: PCPU UTIL(%) AVG between 40% and 60%; several vcpu worlds of the large VM with %CSTP above 2%; at least one of its vcpu worlds with %RDY above 0; the 1-vCPU VMs with %CSTP 0.00; %MLMTD 0 on the large VM.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
B: Co-stop means the host had no free threads, like Ready. Or E: Co-stop is an IO wait.

## Expected key points
- Answer: A, C, D, H.
- A true: the kernel stops a vCPU that runs too far ahead of a sibling that cannot be served, to keep the guest's vCPUs in step.
- B false: the misconception. With PCPU UTIL near half, threads were free; co-stopped vCPUs stop even then. Ready, not Co-stop, is the wait for a thread.
- C true: a 1-vCPU VM has no sibling, so Co-stop is always 0.
- D true: during Co-stop, Ready or Wait the vCPU holds no thread.
- E false: IO waits show in %WAIT (%VMWAIT), not %CSTP.
- F false: over-correction. Ready on one vCPU leads to Co-stop on its siblings.
- G false: wrong action. Co-stop tends to rise with the vCPU count.
- H true: a narrower VM keeps its vCPUs in step more easily.

## Notes
- Paired with the theory question 0053 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C28). Counts only after author approval.

## Metadata
```yaml
id: "0375"
title: "esxtop Co-stop on a host at half load"
product: [vsphere]
technology: [cpu]
task: read-metric
level: 300
answer_type: deterministic
input: [screenshot]
object: [vm, esxi]
tool: [esxtop]
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/co-stop
  - vsphere/technology/cpu/concepts/vcpu-states
  - vsphere/tools/esxtop/cpu
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/co-stop
attachments:
  - 0375/esxtop-cpu-vm-expanded.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C28"
answer: [A, C, D, H]
misconception: [B, E]
misconception_type: [provider-vs-consumer]
pair: "0053"
status: awaiting-input
```
