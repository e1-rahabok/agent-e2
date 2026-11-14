# CPU Swap Wait above zero

## Prompt
- An 8-vCPU database VM. vCenter Real-time chart, per vCPU over 30 minutes: Swap Wait about 3% of each 20-second sample, Readiness below 0.5%, Co-stop 0.
- The DBA sees a CPU counter above 0 and asks for more CPU for the VM.

Which statements about CPU Swap Wait are correct?

- A. Swap Wait is time a vCPU waits for a memory page to be read back from ESXi swap.
- B. Swap Wait is part of the vCPU's Wait state, not of Ready.
- C. Swap Wait shows the VM is short of CPU: its vCPUs wait for physical threads.
- D. VCF Operations counts this wait in Memory Contention (%), not in CPU Contention (%).
- E. Memory Latency also counts time spent decompressing pages, which Swap Wait leaves out.
- F. Because its cause is memory, Swap Wait does not slow the guest's CPU work.
- G. Swap Wait rises while ESXi writes the VM's pages out to swap.
- H. Add vCPUs to the VM, so that the remaining vCPUs can run while some of them wait.
- I. When Swap Wait falls, Run rises, because the vCPUs spend less time stalled.

## Likely wrong answer
C: a CPU counter is above 0, so the VM needs more CPU. Or F: the wait belongs to memory, so it does not affect the CPU.

## Expected key points
- Answer: A, B, D, E, I.
- A true: the vCPU needs data that sits in ESXi swap and stalls until the page comes back.
- B true: Wait = Idle + Swap Wait + Other Wait; Ready is time with work and no physical thread.
- C false: the misconception. Ready below 0.5% and Co-stop 0 show the vCPUs get threads; the stall is a memory cause in a CPU state.
- D true: VCF Operations places Swap Wait in memory contention; CPU Contention leaves it out.
- E true: Memory Latency covers swap-in and decompression; Swap Wait covers swap-in only.
- F false: over-correction. The guest experiences a freeze; Swap Wait is runtime the guest demanded and counts in Guest OS CPU sizing.
- G false: Swap Wait is about pages coming in (swap-in), when the guest touches a swapped page; writing pages out does not stall the vCPU this way.
- H false: wrong action. More vCPUs do not bring pages back faster; the remedy is memory for the VM: less overcommit on the host, a reservation, or a faster swap location.
- I true: with fewer stalls the vCPU runs more of its time.

## Notes
- Paired with the practical question 0109 (theory and practical; design.md, section 3.9). Situation numbers differ from 0109 on purpose.
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item B16). Counts only after author approval.

## Metadata
```yaml
id: "0367"
title: "CPU Swap Wait above zero"
product: [vsphere, vcf-operations]
technology: [cpu, memory]
task: explain-mechanism
level: 300
answer_type: deterministic
input: [text]
object: [vm]
tool: [vcenter, vcf-operations]
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/swap-wait
  - vsphere/technology/cpu/metrics/virtual-motherboard/wait
  - vsphere/technology/cpu/metrics/virtual-motherboard/contention
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/swap-wait
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item B16"
answer: [A, B, D, E, I]
misconception: [C]
misconception_type: [reclamation-as-contention]
pair: "0109"
status: draft
```
