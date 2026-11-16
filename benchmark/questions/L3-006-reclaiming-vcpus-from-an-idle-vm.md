# Reclaiming vCPUs from an idle VM

## Prompt
- VCF Operations, vm-erp-old: 32 vCPUs, 128 GB configured, Memory Consumed 118 GB.
- CPU Usage of the VM stayed between 30 and 60 MHz on every day of the last 30 days.
- Host: 2 sockets of 32 cores, 2.0 GHz base clock, Hyper-Threading on.
- The owner agrees that the VM can be reclaimed to free capacity.

Choose all the correct statements:

- A. Idle is best judged as CPU Usage below 5% of the VM's size, so a 32-vCPU VM and a 1-vCPU VM meet one standard.
- B. Removing 20 of its idle vCPUs frees about 40 GHz of CPU cycles for other VMs.
- C. Removing 20 vCPUs frees allocation: the cluster's CPU overcommit ratio (vCPUs per physical thread) falls.
- D. Power off the VM: that frees the host memory its guest once touched.
- E. A VM can process heavy disk and network IO with almost no CPU cycles.
- F. Reducing the idle VM's vCPU count also frees its memory on the host.
- G. A VM busy 2 hours each Monday and quiet the rest of the week counts as idle: it is idle 98.8% of the week.

## Answers
C, D

## Explanation
- A is wrong: idle is absolute, a CPU Usage threshold in MHz (the policy row `idle-vm-cpu`), not relative to VM size; 5% of a 32-vCPU VM is 32 times the cycles of 5% of a 1-vCPU VM.
- B is wrong: idle vCPUs used almost no cycles, so no cycles are freed; reclaiming them frees allocation only. A busy VM placed in that "room" adds real load.
- C is correct: an idle or oversized VM gives back allocation, which lowers the cluster's overcommit ratio, counted per physical thread.
- D is correct: Windows and Linux keep memory they once touched, so the host keeps it mapped (Consumed 118 GB); power-off releases it.
- E is wrong: every IO costs CPU cycles (packets processed, data copied to memory), so CPU idleness implies low disk and network activity, and idle is defined on CPU alone.
- F is wrong: reducing vCPUs frees allocation, not memory; only power-off returns the consumed pages.
- G is wrong: idle is evaluated every day, not over the whole window; a VM used 2 hours a week does business work and is not idle.
- Misconception: B (vCPUs × GHz counted as freed cycles) or E (IO assumed to cost no CPU). Also A (an idle threshold relative to VM size) and G (idle judged over the whole week).

## Notes
- Changed in the 2026-11-15 audit: evidence stem (VCF Operations values instead of "idle for weeks"); A replaced (was a throwaway: idle as half of the vCPUs) by the relative-threshold misconception; G added (idle over the week); C names the ratio per physical thread.

## Metadata
```yaml
id: "0013"
title: "Reclaiming vCPUs from an idle VM"
product: [vsphere]
technology: [cpu]
input: [text]
task: decide-capacity
object: [vm]
tool: [vcf-operations]
knowledge:
  - sp5-framework/capacity/reclamation
  - vsphere/technology/cpu/decision-tree/oversized-vm-downsizing
  - vsphere/technology/cpu/concepts/idle-and-unused-vcpus
  - vsphere/technology/memory/concepts/memory-as-storage
knowledge_main: sp5-framework/capacity/reclamation
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > CPU > Q11 Reclamation"
answer_type: deterministic
level: 300                      # author 2026-11-05
misconception: [A, B, E, G]
misconception_type: [unit-and-normalization, rollup-and-interval]
status: draft
```
