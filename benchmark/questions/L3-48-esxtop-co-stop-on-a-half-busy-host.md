# esxtop Co-stop on a host at half load

## Prompt
- A database team says their 16-vCPU VM stalls for short moments and asks for 8 more vCPUs.
- You run esxtop on its host, open the CPU panel and expand the VM's group with `e`. See [the esxtop screen](0375/esxtop-cpu-vm-expanded.png).

Which statements are correct?

- A. PCPU UTIL near half shows free threads existed while vcpu worlds of the large VM sat in %CSTP.
- B. The %CSTP of the large VM shows the host had no thread free for those vCPUs.
- C. %MLMTD at 0 rules out a CPU limit behind the large VM's %RDY.
- D. The large VM's group row sums its 16 vcpu worlds, so its %RDY can pass 100%.
- E. %CSTP above 2% on the large VM shows it needs the 8 extra vCPUs.
- F. The 1-vCPU VMs on the screen show %CSTP above 0.
- G. A narrower VM would tend to show less %CSTP.
- H. The %RDY on some vcpu worlds has nothing to do with the %CSTP on their siblings.

## Input to supply
- Product and version: ESXi 9.1, esxtop in an SSH session (interactive mode), CPU panel (`c`).
- Object: one VM with 16 vCPUs (12-24 is fine), expanded with `e` so its vcpu worlds show; at least two 1-vCPU VMs visible on the same screen.
- Screen: the CPU panel with the header lines (PCPU USED(%), PCPU UTIL(%)), the large VM's group row and its expanded vcpu worlds. Fields shown: %USED, %RUN, %SYS, %WAIT, %RDY, %IDLE, %OVRLP, %CSTP, %MLMTD (use `f` to add any missing). Save as `0375/esxtop-cpu-vm-expanded.png`.
- How to produce it in a lab: run a multi-thread load in the 16-vCPU VM on a host that is about half busy with other burners, so that vCPUs of the large VM sometimes find no free thread.
- Condition the key depends on: PCPU UTIL(%) AVG between 40% and 60%; several vcpu worlds of the large VM with %CSTP above 2%; at least one of its vcpu worlds with %RDY above 0; the 1-vCPU VMs with %CSTP 0.00; %MLMTD 0.00 on the large VM.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
B: Co-stop means the host had no free threads. Or E: the VM stalls, so give it more vCPUs.

## Expected key points
- Answer: A, C, D, G.
- A true: reading. With PCPU UTIL near half, threads were free; co-stopped vCPUs are held back to stay in step with a sibling, even when a thread is free for them.
- B false: the misconception. Waiting for a thread is Ready; Co-stop holds a vCPU that ran ahead of a sibling.
- C true: %MLMTD (time held back by a limit) is counted inside %RDY; at 0 the Ready is not from a limit.
- D true: a group row sums its worlds, so %RDY of a 16-vCPU VM can exceed 100%.
- E false: wrong action. Co-stop tends to rise with the vCPU count; 8 more vCPUs make it worse.
- F false: reading. The 1-vCPU VMs show 0.00: Co-stop needs sibling vCPUs.
- G true: fewer vCPUs keep in step more easily.
- H false: over-correction. Ready on one vCPU is the usual cause of Co-stop on its siblings.

## Notes
- Paired with the theory question 0053 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C28). Counts only after author approval.
- Review 2026-11-15: options tied to the screen (A, C, D, F) and reworded away from 0053. Key changed from A, C, D, H to A, C, D, G (new options).

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
answer: [A, C, D, G]
misconception: [B]
misconception_type: [provider-vs-consumer]
pair: "0053"
status: awaiting-input
```
