# Latency Sensitivity High on a trading VM

## Prompt
- ESXi 9.1 host: 2 sockets of 16 cores at 2.0 GHz, Hyper-Threading on, 512 GB of memory.
- A trading VM: 8 vCPUs, 64 GB of memory, virtual hardware version 21.
- The team wants to set its Latency Sensitivity to High, without virtual Hyper-Threading.

Which statements are correct?

- A. To power on, the VM needs a full memory reservation (64 GB) and a full CPU reservation (8 × 2.0 GHz = 16 GHz).
- B. Once granted, each vCPU holds a whole physical core. Other VMs and VMkernel worlds cannot use those cores, including their second hardware thread.
- C. The setting costs nothing when the trading VM is idle: its cores return to the other VMs.
- D. After the change, the VM's CPU Run and Demand read about 100% even when it is idle. That is the exclusive scheduling, not a CPU shortage.
- E. A full CPU reservation guarantees exclusive cores, even when no NUMA node has enough free cores at power-on.
- F. With High with Hyperthreading instead, the VM would take 4 cores and an 8 GHz CPU reservation.

## Likely wrong answer
C: the cores are shared again when the VM is idle. Or E: the reservation alone guarantees exclusive cores.

## Expected key points
- Answer: A, B, D, F.
- A: High needs 100% of memory reserved. From virtual hardware 14, a 100% CPU reservation (vCPUs × frequency) is required to power on.
- B: once exclusive cores are granted (not guaranteed, see E), each vCPU has a dedicated core without virtual Hyper-Threading; the partner thread is held by an idle world. The cores leave the pool for every other VM and for VMkernel worlds.
- C is wrong: the exclusive assignment holds whether the VM is busy or not.
- D: the vCPUs are always scheduled, so Run and Demand go to 100% and Wait to 0%, while Usage stays near 0%.
- E is wrong: if no NUMA node has enough non-exclusive cores at power-on, the VM may not get exclusive cores.
- F: with virtual Hyper-Threading, consecutive vCPU pairs share one core: (8 / 2) × 2.0 GHz = 8 GHz on 4 cores. It needs virtual hardware 20 or later, and a full memory reservation.

## Notes
- Product behaviour also in Performance Best Practices for VMware vSphere 9.1 (revision 20260624), Latency sensitivity.

## Metadata
```yaml
id: "0112"
title: "Latency Sensitivity High on a trading VM"
product: [vsphere]
technology: [cpu, memory]
task: judge-setting
level: 400
answer_type: deterministic
input: [text]
object: [vm, esxi]
tool: [none]
knowledge:
  - vsphere/technology/cpu/configuration/latency-sensitivity
  - vsphere/technology/cpu/concepts/hyper-threading
knowledge_main: vsphere/technology/cpu/configuration/latency-sensitivity
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12 for the CPU slots (project/plan.md, M2)"
answer: [A, B, D, F]
misconception: [C, E]
misconception_type: [consumption-as-contention]
status: draft
```
