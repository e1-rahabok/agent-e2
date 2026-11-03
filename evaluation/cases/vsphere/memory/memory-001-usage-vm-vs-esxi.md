---
id: vsphere-memory-001
title: "Memory usage: VM vs ESXi"
scope: vsphere
area: memory
input: text
tests: distinction
knowledge:
  - vsphere/memory/metrics/virtual-motherboard/usage
  - vsphere/memory/metrics/host/usage
  - foundations/resource-nature
attachments: []
origin: book
source_path: "The World of Metrics > Metrics Nuances: Naming Complexity; Architecture Complexity (Memory)."
format: free-text
status: draft
---

## Prompt
Every VM on an ESXi host shows Memory Usage below 25% in vCenter. The host itself shows Memory Usage at 95%. The customer wants to buy more RAM. Is the host running out of memory?

## Likely wrong answer
"Yes, the host is nearly full, buy RAM" — or "the numbers are inconsistent, something is broken".

## Expected key points
- VM Memory Usage maps to **Active**. ESXi Memory Usage maps to **Consumed**. Cluster maps to Consumed + Overhead.
- Reason: 2-level memory hierarchy. VM level = what is actively used (performance). Host level = what VMs have claimed (capacity).
- High Consumed is not proof of shortage. Memory is a cache; near 100% is expected and is good use of money.
- This confusion has led customers to buy more RAM than needed.
- Check contention metrics, not Usage, to decide.

## Notes
- Tests: Same name, different formula per object (distinction).
