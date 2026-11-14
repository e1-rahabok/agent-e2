# A 1-vCPU VM under a CPU limit: Demand, Usage and Max Limited

## Prompt
- A 1-vCPU VM, build-runner-03, runs compile jobs. Its host has a base clock of 2.8 GHz.
- The VM has a CPU limit of 1,200 MHz.
- [The attached vSphere Client export](0103/build-runner-03-cpu-real-time.csv) holds 30 minutes of Real-time points (20 seconds): CPU Demand (MHz), Usage (MHz), Run (ms), Used (ms) and Max limited (ms).
- System time is about 25 ms per sample.

Which statements are correct?

- A. Usage is flat just under 1,200 MHz, and Max limited takes more than half of each sample.
- B. Demand equals Usage, so the limit is not holding the VM back.
- C. Used is above Run because of the VM's System time.
- D. Run at about 36% shows the guest is idle almost two thirds of the time, so it needs no more CPU.
- E. Remove or raise the limit: it caps this VM in MHz.
- F. Add a second vCPU to give the VM more CPU.

## Likely wrong answer
B: equal Demand and Usage read as a VM that gets all it asks for. Or D: Run at 36% read as spare CPU.

## Expected key points
- Answer: A, E.
- A: Usage stays at 1,181-1,197 MHz for 30 minutes, and Max limited is about 12,500-12,900 ms of each 20,000 ms sample: almost two thirds of the time the vCPU was ready but held back by the limit.
- B is wrong: Max limited, not Demand, shows whether a limit holds the VM back. Here Demand stays equal to Usage while the limit is active.
- C is wrong: System is about 25 ms, far too small for a gap of about 1,300 ms between Used and Run.
- D is wrong: Run (about 7,200 ms) plus Max limited (about 12,700 ms) fill almost the whole sample. The vCPU was held back, not idle.
- E: the limit holds Usage at its value in MHz whatever the guest demands.
- F is wrong: a second vCPU would share the same 1,200 MHz; the limit, not the vCPU count, caps this VM.

## Notes
- From the author's samples: a single-vCPU VM under a CPU limit whose Demand equals Usage. Export regenerated 2026-11-14 with new numbers and a new VM (seeded script; project/question-pairing-2026-11-14.md, decision 3): the old export reproduced the example of run-vs-used-gap. Option A states the reading only (its old clause negated B); F (the wrong action) added. Key unchanged (author approved, 2026-11-14).
- Paired with 0066 (theory and practical, design.md 3.9).
- Revised 2026-11-12 after review: the earlier option on why Demand equals Usage under a limit was dropped. The vSphere API defines cpu.demand as what the VM would use with no contention or limit, while the knowledge base says a limit leaves Demand equal to Usage; the conflict goes to the author. The question keeps only the observation. The Used vs Run (Turbo) option was dropped: 0100 tests it.

## Metadata
```yaml
id: "0103"
title: "A 1-vCPU VM under a CPU limit: Demand, Usage and Max Limited"
product: [vsphere]
technology: [cpu]
task: read-metric
level: 400
answer_type: deterministic
input: [table]
object: [vm]
tool: [vcenter]
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/technology/cpu/metrics/virtual-motherboard/demand
  - vsphere/technology/cpu/metrics/virtual-motherboard/used
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/ready
attachments:
  - 0103/build-runner-03-cpu-real-time.csv
origin: book
source_path: "Author samples (docx, 2026-11-12) > Single vCPU VM with a 2 GHz limit: Demand vs Usage"
answer: [A, E]
misconception: [B, D]
misconception_type: [consumption-as-contention]
pair: "0066"
status: draft
```
