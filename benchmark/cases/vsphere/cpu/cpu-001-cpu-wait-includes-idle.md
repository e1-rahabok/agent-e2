# High CPU Wait

## Prompt
A VM shows CPU Wait at 90%. The application owner says the VM must be stuck waiting on disk or memory. Are they right?

## Likely wrong answer
"Yes, high wait means IO or memory bottleneck."

## Expected key points
- VM CPU Wait **includes idle time**.
- Most VMs do not run at 100%, so Wait is naturally high.
- The name is correct from the kernel scheduler's viewpoint: the vCPU is waiting to be used.
- High Wait alone does not indicate a bottleneck. Requires other evidence (e.g. disk latency, memory contention).

## Notes
- Tests: Confusing name (distinction).

## Metadata
```yaml
id: vsphere-cpu-001
title: "High CPU Wait"
scope: vsphere
area: cpu
input: text
tests: distinction
knowledge:
  - vsphere/cpu/metrics/virtual-motherboard/wait
attachments: []
origin: book
source_path: "The World of Metrics > Metrics Nuances: Naming Complexity (Confusing name)."
format: free-text
status: draft
```
