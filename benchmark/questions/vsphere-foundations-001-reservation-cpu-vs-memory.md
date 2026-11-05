# Memory reservation vs CPU reservation

## Prompt
- A 16 GB VM with a 10 GB memory reservation and a 4 GHz CPU reservation is powered on and sits at the BIOS screen (no OS booted).

What do its Memory Consumed and CPU usage metrics show?

## Likely wrong answer
"Both near 0, nothing is running" — or "both show the reserved amounts".

## Expected key points
- **Memory:** Consumed jumps to ~10 GB. Reservation is counted even though the pages are not actually used, because ESXi has set the space aside.
- Once a reserved page has been used, ESXi keeps it locked to the VM, even if the VM is idle for days.
- **CPU:** reservation is on-demand. Run, Used, Demand and Usage stay at 0 or near 0. CPU reservation does not affect utilization metrics.

## Notes
- Tests: Same name, different behaviour (principle: CPU vs memory are different in nature).

## Metadata
```yaml
id: vsphere-foundations-001
title: "Memory reservation vs CPU reservation"
scope: vsphere
product: [vsphere]
technology: [system]
area: foundations
input: [text]
tests: concept
knowledge:
  - vsphere/foundations/resource-controls
attachments: []
origin: book
source_path: "The World of Metrics > Metrics Nuances: Resource Management."
answer_type: judged
level: 300                      # draft by Claude 2026-11-05; author to confirm (Q056)
status: draft
```
