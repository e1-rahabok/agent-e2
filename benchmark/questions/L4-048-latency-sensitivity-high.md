# Latency Sensitivity High on a trading VM

## Prompt
- ESXi 9.1 host: 2 sockets of 16 cores at 2.0 GHz, Hyper-Threading on, 512 GB of memory.
- A trading VM: 8 vCPUs, 64 GB of memory, virtual hardware version 21.
- The team wants to set its Latency Sensitivity to High, without virtual Hyper-Threading.

Which statements are correct?

- A. To power on, the VM needs all 64 GB of memory reserved and a CPU reservation of 8 × 2.0 GHz = 16 GHz.
- B. Once granted, each vCPU holds a whole core: other VMs and VMkernel worlds lose both of its threads.
- C. The setting costs nothing when the trading VM is idle: its cores return to the other VMs.
- D. When the VM is idle after the change, its Run and Demand read about 100% while its Usage stays near 0%.
- E. A full CPU reservation guarantees exclusive cores, even when no NUMA node has enough free cores at power-on.
- F. With High with Hyperthreading instead, the VM would take 4 cores and an 8 GHz CPU reservation.
- G. Run and Demand near 100% after the change show that the trading VM is short of CPU.
- H. High with Hyperthreading gives any latency-sensitive VM more performance than High does.

## Answers
A, B, D, F

## Explanation
- A is correct: High needs 100% of memory reserved. From virtual hardware 14, a 100% CPU reservation (vCPUs × frequency) is required to power on.
- B is correct: once exclusive cores are granted (not guaranteed, see E), each vCPU has a dedicated core without virtual Hyper-Threading; the partner thread is held by an idle world. The cores leave the pool for every other VM and for VMkernel worlds.
- C is wrong: the exclusive assignment holds whether the VM is busy or not.
- D is correct: the vCPUs are always scheduled, so an idle VM shows Run and Demand about 100% and Wait 0%, while Usage stays near 0%.
- E is wrong: if no NUMA node has enough non-exclusive cores at power-on, the VM may not get exclusive cores.
- F is correct: with virtual Hyper-Threading, consecutive vCPU pairs share one core: (8 / 2) × 2.0 GHz = 8 GHz on 4 cores. It needs virtual hardware 20 or later, and a full memory reservation.
- G is wrong: Run and Demand read about 100% because the vCPUs are pinned and always scheduled; Usage stays low, so it is not a CPU shortage.
- H is wrong: locking vCPUs to hyper-threads helps only workloads that use the topology and can stop ESX from using idle cores; most workloads gain nothing or lose.
- Misconception: C: the cores are shared again when the VM is idle. Or E: the reservation alone guarantees exclusive cores. Or G: Demand at 100% read as a CPU shortage.

## Notes
- Changed in the 2026-11-15 audit: D no longer explains its own reading (the explanation is now the misconception G); H added (High with Hyperthreading as a general gain); B shortened.
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
source_path: "Synthetic, 2026-11-12"
misconception: [C, E, G]
misconception_type: [consumption-as-contention]
status: draft
```
