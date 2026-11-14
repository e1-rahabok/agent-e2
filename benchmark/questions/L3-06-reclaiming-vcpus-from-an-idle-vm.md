# Reclaiming vCPUs from an idle VM

## Prompt
- A 32-vCPU VM has been idle for weeks.
- You want to reclaim it to free capacity.

Choose all the correct statements:

- A. Reclaim at most 16 vCPUs, because idle in VCF Operations means using less than half of the vCPUs.
- B. On a 2 GHz host, removing 20 idle vCPUs frees about 40 GHz of CPU cycles for other VMs.
- C. Removing 20 vCPUs frees allocation: the cluster's vCPU-to-core overcommit ratio falls.
- D. Power off the VM: that frees the host memory its guest once touched.
- E. Check disk and network activity too: a VM can process heavy IO with almost no CPU cycles.
- F. Reducing the idle VM's vCPU count also frees its memory on the host.

## Likely wrong answer
B (vCPU × GHz counted as freed cycles) or E (IO assumed to cost no CPU).

## Expected key points
- Answer: C, D.
- A is wrong: idle is absolute (a CPU Usage threshold in MHz, 100 MHz by default), not relative to VM size.
- B is wrong: idle vCPUs used almost no cycles, so no cycles are freed; reclaiming them frees allocation only. A busy VM placed in that "room" adds real load.
- C is correct: an idle or oversized VM gives back allocation, which lowers the overcommit ratio.
- D is correct: Windows and Linux keep memory they once touched, so the host keeps it mapped; power-off releases it.
- E is wrong: every IO costs CPU cycles (packets processed, data copied to memory), so CPU idleness implies the rest.
- F is wrong: reducing vCPUs frees allocation, not memory; only power-off returns the consumed pages.

## Notes
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): old B and C each split into one fact (freed cycles, freed allocation); old C's vague "blank air" wording dropped; F is new. Key letters unchanged, C, D; C now states the allocation fact (author approved, 2026-11-14).

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
answer: [C, D]
misconception: [B, E]
misconception_type: [unit-and-normalization]
status: draft
```
