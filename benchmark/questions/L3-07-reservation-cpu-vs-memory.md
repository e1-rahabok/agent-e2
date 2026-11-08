# Memory reservation vs CPU reservation

## Prompt
- A 16 GB VM with a 10 GB memory reservation and a 4 GHz CPU reservation is powered on and sits at the BIOS screen (no OS booted).

What do its Memory Consumed and CPU usage metrics show?

## Likely wrong answer
"Memory Consumed jumps to the 10 GB reservation" — or "both show the reserved amounts".

## Expected key points
- **Memory:** Consumed stays low. Memory reservation is also on demand: untouched reserved memory is not counted and the VMkernel can give it to other VMs.
- Once a reserved page has been touched, ESXi keeps it held for the VM, even if the VM is idle for days.
- **CPU:** reservation is on demand too. Run, Used, Demand and Usage stay at 0 or near 0. CPU reservation does not affect utilization metrics.

## Notes
- Previous id: vsphere-foundations-001 (renamed 2026-11-05).
- Tests: Same name, different behaviour (principle: CPU vs memory are different in nature).

## Metadata
```yaml
id: "0014"
title: "Memory reservation vs CPU reservation"
product: [vsphere]
technology: [system]
input: [text]
task: judge-setting
knowledge:
  - vsphere/architecture/resource-controls
attachments: []
origin: book
source_path: "The World of Metrics > Metrics Nuances: Resource Management."
answer_type: judged
level: 300                      # author 2026-11-05
status: draft
```
