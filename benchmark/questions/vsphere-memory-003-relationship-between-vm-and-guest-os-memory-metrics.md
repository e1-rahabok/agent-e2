# Relationship between VM and Guest OS memory metrics

## Prompt
- These sentences cover the relationship between VM metrics and Guest OS metrics.

Choose all the correct ones:

- A. VM and Guest OS metrics are managed independently. The hypervisor manages the VM; Windows or Linux manages the Guest OS. Neither layer considers the other.
- B. VM memory utilization and Guest OS memory utilization can have significantly different values. Their patterns over time also do not match.
- C. When Windows or Linux frees a page, ESXi automatically frees the same block for the VM within a few minutes.
- D. If VMware Tools is not running, the hypervisor cannot balloon the VM: it cannot make the memory request to Windows or Linux.
- E. If VMware Tools is not running, VCF Operations rightsizing is less accurate. It falls back to Consumed memory, which tends to show higher utilization.

## Likely wrong answer
C (a guest free assumed to propagate to ESXi).

## Expected key points
- Answer: A, B, D, E.
- A: an architecture distinction that is often mixed up.
- B: VM Consumed tends to grow over time, as freed guest pages may not be removed.
- C is wrong: freeing a page only changes the Guest OS page table, a pointer status. The hypervisor does not see it.
- D: without Tools, ESXi cannot ask the Guest OS to give up pages.
- E: correct.

## Notes

## Metadata
```yaml
id: vsphere-memory-003
title: "Relationship between VM and Guest OS memory metrics"
product: [vsphere]
technology: [memory]
input: [text]
task: read-metric
knowledge:
  - vsphere/technology/memory/concepts/guest-os-vs-vm-memory
  - vsphere/technology/memory/concepts/ballooning
  - vsphere/technology/memory/metrics/virtual-motherboard/usage
  - vsphere/foundations/vm-vs-guest-os
attachments: []
origin: quiz
source_path: "vSphere Metric Quiz.docx (author upload 2026-11-03) > Memory > Q2 VM vs Guest OS"
answer_type: deterministic
level: 300                      # draft by Claude 2026-11-05; author to confirm (Q056)
answer: [A,B,D,E]
trap: [C]
status: draft
```
