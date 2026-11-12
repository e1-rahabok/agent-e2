# Used far below Run in the vCenter chart

## Prompt
The attached screenshot is the vSphere Client advanced performance chart of a 4-vCPU Linux VM: CPU Run, Used, Ready, Co-stop and System, in milliseconds.

- Used is about half of Run for the whole hour.
- Ready, Co-stop and System are low.
- The application team asks for 4 more vCPUs because the VM is slow.

Which statements are correct? Choose all that apply.

- A. Used far below Run with little System and Overlap points to power saving and Hyper-Threading: more vCPUs is the wrong answer.
- B. Add the 4 vCPUs: Run shows the vCPUs are busy.
- C. Check the host power management policy and the actual frequency (esxtop %A/MPERF), and whether the sibling threads are busy.
- D. Used below Run means Turbo Boost is active.

## Input to supply
- Tool: vSphere Client 9.1, VM > Monitor > Performance > Advanced > CPU, real-time, one hour.
- Counters: Run, Used, Ready, Co-stop, System (summation, ms), one line per counter for the VM total.
- Condition for the key: Used is 40-60% of Run; Ready and Co-stop low; System small against Run. A host with Balanced power management and busy sibling threads gives this pattern.
- Mask VM and host names if they reveal the customer.
- Save as `benchmark/questions/71/vcenter-vm-cpu-run-used.png`.

## Likely wrong answer
B: adding vCPUs because Run is high.

## Expected key points
- Answer: A, C.
- Run is time only; Used is scaled by frequency and by Hyper-Threading. Used below Run, with little System and Overlap, means the vCPUs ran at lower speed: power saving and busy sibling threads.
- The example in the knowledge base: a 4-vCPU Ubuntu VM with Used about 44% of Run.
- Check power management and %A/MPERF, and the sibling thread load.
- D is wrong: Turbo raises Used above Run.

## Notes
- Retired 2026-11-12 (question set 1.0): same fact as the author sample on Run above Used.
- Previous id: question-0071 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0071"
title: "Used far below Run in the vCenter chart"
product: [vsphere]
technology: [cpu]
task: troubleshoot
level: 400
answer_type: deterministic
input: [screenshot]
knowledge:
  - vsphere/technology/cpu/troubleshooting/run-vs-used-gap
  - vsphere/technology/cpu/metrics/virtual-motherboard/used
  - vsphere/technology/cpu/metrics/virtual-motherboard/run
attachments:
  - 0071/vcenter-vm-cpu-run-used.png
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
answer: [A, C]
misconception: [B]
status: retired
```
