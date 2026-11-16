# Which counter to size VM memory

## Prompt
The application team of a Windows Server VM asks how much memory the VM should be configured with. Which counters are the most accurate inputs?

- A. VM Memory Consumed
- B. VM Memory Active
- C. Guest OS Needed Memory minus VM Memory Ballooned
- D. VM Memory Active + Balloon + Swapped + Zipped
- E. Guest OS memory in use plus the Guest OS cache that Windows ranks high
- F. Guest OS memory in use plus the page file in use

## Answers
E

## Explanation
- A is wrong: a VM-level counter full of idle pages; a page the guest frees stays in Consumed.
- B is wrong: a VM-level counter, a sample of recently touched pages taken regularly; it does not see how the guest uses its cache.
- C is wrong: size on Needed Memory with the balloon in it, no deduction. The balloon also takes in-use pages, which the guest pages out and still needs; a deduction would shrink a VM the balloon already squeezes.
- D is wrong: its base is VM Active, a sampled estimate of recently touched pages that misses the cache the guest works from, and Swapped and Zipped are pages ESXi took without knowing what the guest uses. No sum of VM counters stands in for what the Guest OS needs: Guest OS sizing reads Guest OS counters.
- E is right: size from Guest OS Needed Memory as VMware Tools derives it: In Use plus the cache Windows ranks high and a 5% buffer; Free, Standby Reserve and Standby Normal are left out. Without that cache the guest pages out.
- F is wrong: the page file is excluded from Guest OS sizing: too conservative, since In Use already holds cache, and proactive page-in (memory-mapped files) makes unmet demand impossible to isolate in it.
- Misconception: A or B (VM-level counters), or D (VM counters added up). Or C: the balloon taken off as ESXi's demand, not the application's. Or F, the over-correction: the page file added on top, to be safe.

## Notes
- Hint moved out of the prompt (author, 2026-11-14: a hint helps the frontier model, not the local model), for reviewers: "Hint: the VM is virtual hardware. What you size is the OS running on it."
- Changed in the 2026-11-15 audit: stem names a Windows Server VM and a situation (Needed Memory is defined for Windows); throwaway C replaced in place by the balloon-deduction misconception (guest-os-sizing, Misconceptions line 6); key point E names the Needed Memory rule. D stays false: its base is VM Active, not Needed Memory. Key unchanged: E.
- Paired with 0079 (theory and practical; design.md, section 3.9).
- Changed on 2026-11-16 (re-review): E names the cache Windows ranks high instead of the hedge "part of", which only the correct option carried. Key unchanged.

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
  - guest-os/memory/windows-memory
object: [vm, guest-os]
tool: [none]
knowledge_main: guest-os/system/guest-os-sizing
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > Memory > Q1 VM Memory Rightsize"
answer_type: deterministic
level: 300                      # author 2026-11-05
misconception: [A,B,C,D]
pair: "0079"
misconception_type: [layer-confusion, provider-vs-consumer]
status: draft
```
