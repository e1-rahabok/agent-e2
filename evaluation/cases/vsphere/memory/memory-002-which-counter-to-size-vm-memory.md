---
id: vsphere-memory-002
title: "Which counter to size VM memory"
scope: vsphere
area: memory
input: text
tests: distinction
knowledge:
  - vsphere/system/concepts/guest-os-sizing
  - vsphere/memory/concepts/guest-os-vs-vm-memory
  - vsphere/memory/metrics/virtual-machine/consumed
  - vsphere/memory/metrics/virtual-machine/active
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > Memory > Q1 VM Memory Rightsize"
format: multiple-choice
level: l400
answer: [E]
trap: [A,B,D]
status: draft
---

## Prompt
Choose the most accurate counter to rightsize a VM.

A. VM Memory Consumed
B. VM Memory Active
C. (VM Memory Consumed + VM Memory Active) / 2
D. VM Memory Active + Balloon + Swapped + Zipped
E. Guest OS Memory Used. In some cases, add the cache.

Hint: think of the VM as a virtual motherboard: a printed circuit board with hardware mounted on it. What you size is the OS running on it.

## Likely wrong answer
A or B (VM-level counters), or D (mixing VM and Guest OS realms).

## Expected key points
- Answer: E.
- A is wrong: a VM-level counter full of idle pages.
- B is wrong: a VM-level counter, a sample of active pages taken regularly.
- C is wrong: mixes two different concepts.
- D is wrong: mixes the VM realm and the Guest OS realm.
- E is the base answer; variants exist (for example adding cache).

## Notes

