# Memory usage: VM vs ESXi

## Prompt
- Every VM on an ESXi host shows Memory Usage below 25% in vCenter.
- The host itself shows Memory Usage at 95%.
- The customer wants to buy more RAM.

Is the host running out of memory?

## Likely wrong answer
"Yes, the host is nearly full, buy RAM" — or "the numbers are inconsistent, something is broken".

## Expected key points
- VM Memory Usage maps to **Active**. ESXi Memory Usage maps to **Consumed**. Cluster maps to Consumed + Overhead.
- Reason: 2-level memory hierarchy. VM level = what is actively used (performance). Host level = what VMs have claimed (capacity).
- High Consumed is not proof of shortage. Memory is a cache; near 100% is expected and is good use of money.
- This confusion has led customers to buy more RAM than needed.
- Check contention metrics, not Usage, to decide.

## Notes
- Previous id: vsphere-memory-001 (renamed 2026-11-05).
- Tests: Same name, different formula per object (distinction).

## Metadata
```yaml
id: "20"
title: "Memory usage: VM vs ESXi"
product: [vsphere]
technology: [memory]
input: [text]
task: read-metric
knowledge:
  - vsphere/technology/memory/metrics/virtual-motherboard/usage
  - vsphere/technology/memory/metrics/host/usage
  - foundations/resource-nature
attachments: []
origin: book
source_path: "The World of Metrics > Metrics Nuances: Naming Complexity; Architecture Complexity (Memory)."
answer_type: judged
level: 400                      # author 2026-11-05
status: draft
```
