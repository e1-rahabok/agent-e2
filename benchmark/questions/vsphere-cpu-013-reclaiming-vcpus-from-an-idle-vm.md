# Reclaiming vCPUs from an idle VM

## Prompt
- A 32-vCPU VM has been idle for weeks.
- You want to reclaim it to free capacity.

Choose all the correct statements:

- A. Reclaim at most 16 vCPU, because idle in VCF Operations means using less than half.
- B. Reclaiming 20 vCPU frees 20 vCPU. On a 2 GHz ESXi host, that frees 40 GHz of capacity.
- C. You are basically reclaiming blank air, because the reclaimed CPU is idle. You cannot assume you can safely deploy an active VM. Idle CPU is not the same as active CPU.
- D. Power off the VM, as this also frees the VM memory.
- E. Do not check only CPU. Make sure network packet processing and disk command execution are also low: high IO processing can happen with near 0 CPU cycles.

## Likely wrong answer
B (vCPU x GHz counted as freed capacity) or E (IO assumed to cost no CPU).

## Expected key points
- Answer: C, D.
- A is wrong: idle is absolute (based on CPU Usage), not relative.
- B is wrong: idle vCPUs consume no cycles, so nothing measurable is freed.
- C is correct: CPU is transient; memory is sticky.
- D is correct: VM Consumed memory holds many idle pages; power-off releases them.
- E is wrong: every IO incurs compute overhead across several layers, even with offload.

## Notes

## Metadata
```yaml
id: vsphere-cpu-013
title: "Reclaiming vCPUs from an idle VM"
product: [vsphere]
technology: [cpu]
input: [text]
task: decide-capacity
knowledge:
  - operations-management/capacity/rightsizing
  - vsphere/technology/cpu/diagnosis/oversized-vm-downsizing
  - vsphere/technology/cpu/concepts/idle-and-unused-vcpus
  - vsphere/technology/memory/concepts/memory-as-storage
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > CPU > Q11 Reclamation"
answer_type: deterministic
level: 300                      # draft by Claude 2026-11-05; author to confirm (Q056)
answer: [C,D]
trap: [B,E]
status: draft
```
