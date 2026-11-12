# A 1-vCPU VM under a CPU limit: Demand, Usage and Max Limited

## Prompt
- A 1-vCPU VM, web-proxy-01. Its host has a base clock of 2.095 GHz.
- The VM has a CPU limit of 2,000 MHz.
- [The attached vSphere Client export](0103/web-proxy-01-cpu-real-time.csv) holds 30 minutes of Real-time points (20 seconds): CPU Demand (MHz), Usage (MHz), Run (ms), Used (ms) and Max limited (ms).
- System time is about 30 ms per sample.

Which statements are correct?

- A. The limit is active even though Demand equals Usage: Usage is flat just under 2,000 MHz and Max limited is about a third of each sample.
- B. Demand equals Usage, so the limit is not holding the VM back.
- C. Used is above Run because of the VM's System time.
- D. Run at about 66% shows the guest is idle a third of the time, so it needs no more CPU.
- E. Remove or raise the limit before any change to the vCPU count: the limit, not the vCPU count, caps this VM.

## Likely wrong answer
B: equal Demand and Usage read as a VM that gets all it asks for. Or D: Run at 66% read as spare CPU.

## Expected key points
- Answer: A, E.
- A: Usage is pinned just under the 2,000 MHz limit for 30 minutes, and Max limited is about 6,700 ms of each 20,000 ms sample: a third of the time the vCPU was ready but held back by the limit.
- B is wrong: Max limited, not Demand, shows whether a limit holds the VM back. Here Demand stays equal to Usage while the limit is active.
- C is wrong: System is about 30 ms, far too small for a gap of about 5,400 ms between Used and Run.
- D is wrong: Run (about 13,200 ms) plus Max limited (about 6,700 ms) fill almost the whole sample. The vCPU was held back, not idle.
- E: the VM is capped in MHz by the limit. More vCPUs would share the same 2,000 MHz.

## Notes
- From the author's samples: a single-vCPU VM on a 2.095 GHz host with a 2 GHz limit; Demand and Usage both about 1.96 GHz; Used about 18,600 ms. Values reproduced in the export, with Max limited added (the sample did not show it).
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
  - 0103/web-proxy-01-cpu-real-time.csv
origin: book
source_path: "Author samples (docx, 2026-11-12) > Single vCPU VM with a 2 GHz limit: Demand vs Usage"
answer: [A, E]
misconception: [B, D]
misconception_type: [consumption-as-contention]
status: draft
```
