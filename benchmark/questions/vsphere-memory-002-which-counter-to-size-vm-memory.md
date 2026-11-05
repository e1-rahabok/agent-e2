# Which counter to size VM memory

## Prompt
Choose the most accurate counter to rightsize a VM.

- A. VM Memory Consumed
- B. VM Memory Active
- C. (VM Memory Consumed + VM Memory Active) / 2
- D. VM Memory Active + Balloon + Swapped + Zipped
- E. Guest OS Memory Used. In some cases, add the cache.

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

## Metadata
```yaml
id: vsphere-memory-002
title: "Which counter to size VM memory"
scope: vsphere
product: [vsphere, windows]
technology: [memory]
area: memory
input: [text]
tests: distinction
knowledge:
  - guest-os/system/concepts/guest-os-sizing
  - vsphere/technology/memory/concepts/guest-os-vs-vm-memory
  - vsphere/technology/memory/metrics/virtual-motherboard/consumed
  - vsphere/technology/memory/metrics/virtual-motherboard/active
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > Memory > Q1 VM Memory Rightsize"
answer_type: deterministic
level: 300                      # draft by Claude 2026-11-05; author to confirm (Q056)
answer: [E]
trap: [A,B,D]
status: draft
```
