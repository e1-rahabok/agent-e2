# Which counter to size VM memory

## Prompt
Which counters are the most accurate to rightsize the memory of a VM?

- A. VM Memory Consumed
- B. VM Memory Active
- C. (VM Memory Consumed + VM Memory Active) / 2
- D. VM Memory Active + Balloon + Swapped + Zipped
- E. Guest OS memory in use plus part of the Guest OS cache
- F. Guest OS memory in use, without any of its cache

## Likely wrong answer
A or B (VM-level counters), or D (mixing VM and Guest OS layers). Or F, the over-correction: size on In Use alone.

## Expected key points
- Answer: E.
- A is wrong: a VM-level counter full of idle pages; a page the guest frees stays in Consumed.
- B is wrong: a VM-level counter, a sample of recently touched pages taken regularly; it does not see how the guest uses its cache.
- C is wrong: mixes two different concepts.
- D is wrong: mixes the VM layer and the Guest OS layer; balloon, swap and compression are ESXi reclamation, not guest need.
- E is right: size from what the Guest OS needs, including cache, so the guest does not page out. How much cache to include is open.
- F is wrong: sizing on in-use only leaves no cache or free memory, and the Guest OS pages out.

## Notes
- Stem made plural (2026-11-14): the singular form told the candidate that one option is correct (Q199: the count is never disclosed). Was: "Choose the most accurate counter to rightsize a VM."
- Hint moved out of the prompt (author, 2026-11-14: a hint helps the frontier model, not the local model), for reviewers: "Hint: the VM is virtual hardware. What you size is the OS running on it."
- Option E rewritten 2026-11-14 (was "Guest OS Memory Used. In some cases, add the cache.": vague) and option F added, the over-correction (design.md 3.9; project/question-pairing-2026-11-14.md). Key unchanged: E (author approved, 2026-11-14).
- Paired with 0079 (theory and practical; design.md, section 3.9).

## Metadata
```yaml
id: "0021"
title: "Which counter to size VM memory"
product: [vsphere, windows]
technology: [memory]
input: [text]
task: decide-capacity
knowledge:
  - guest-os/system/concepts/guest-os-sizing
  - vsphere/technology/memory/concepts/guest-os-vs-vm-memory
  - vsphere/technology/memory/metrics/virtual-motherboard/consumed
  - vsphere/technology/memory/metrics/virtual-motherboard/active
object: [vm, guest-os]
tool: [none]
knowledge_main: guest-os/system/concepts/guest-os-sizing
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > Memory > Q1 VM Memory Rightsize"
answer_type: deterministic
level: 300                      # author 2026-11-05
answer: [E]
misconception: [A,B,D]
pair: "0079"
misconception_type: [layer-confusion]
status: draft
```
