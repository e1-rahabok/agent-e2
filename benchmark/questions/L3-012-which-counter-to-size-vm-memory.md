# Which counter to size VM memory

## Prompt
Which counters are the most accurate to rightsize the memory of a VM?

- A. VM Memory Consumed
- B. VM Memory Active
- C. (VM Memory Consumed + VM Memory Active) / 2
- D. VM Memory Active + Balloon + Swapped + Zipped
- E. Guest OS memory in use plus part of the Guest OS cache
- F. Guest OS memory in use plus the page file in use

## Likely wrong answer
A or B (VM-level counters), or D (VM counters added up). Or F, the over-correction: the page file added on top, to be safe.

## Expected key points
- Answer: E.
- A is wrong: a VM-level counter full of idle pages; a page the guest frees stays in Consumed.
- B is wrong: a VM-level counter, a sample of recently touched pages taken regularly; it does not see how the guest uses its cache.
- C is wrong: mixes two different concepts.
- D is wrong: its base is VM Active, a sampled estimate of recently touched pages that misses the cache the guest works from, and Swapped and Zipped are pages ESXi took without knowing what the guest uses. No sum of VM counters stands in for what the Guest OS needs: Guest OS sizing reads Guest OS counters.
- E is right: size from what the Guest OS needs, including cache, so the guest does not page out. How much cache to include is open.
- F is wrong: the page file is excluded from Guest OS sizing: too conservative, since In Use already holds cache, and proactive page-in (memory-mapped files) makes unmet demand impossible to isolate in it.

## Notes
- Stem made plural (2026-11-14): the singular form told the candidate that one option is correct (Q199: the count is never disclosed). Was: "Choose the most accurate counter to rightsize a VM."
- Hint moved out of the prompt (author, 2026-11-14: a hint helps the frontier model, not the local model), for reviewers: "Hint: the VM is virtual hardware. What you size is the OS running on it."
- Option E rewritten 2026-11-14 (was "Guest OS Memory Used. In some cases, add the cache.": vague) and option F added, the over-correction (design.md 3.9; project/question-pairing-2026-11-14.md). Key unchanged: E (author approved, 2026-11-14).
- Review 2026-11-15: F was "Guest OS memory in use, without any of its cache", the negation of E; it now adds the page file (guest-os-sizing, Exclude page file). The reason for D no longer says it mixes layers (all four are VM counters). No option rests on whether ballooned memory belongs in Guest OS sizing; settled 2026-11-15 (Q227): include it, no deduction (guest-os-sizing, section Ballooned memory in sizing). D stays false: its base is VM Active, not Needed Memory. Key unchanged: E.
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
  - guest-os/system/guest-os-sizing
  - vsphere/technology/memory/concepts/guest-os-vs-vm-memory
  - vsphere/technology/memory/metrics/virtual-motherboard/consumed
  - vsphere/technology/memory/metrics/virtual-motherboard/active
object: [vm, guest-os]
tool: [none]
knowledge_main: guest-os/system/guest-os-sizing
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
