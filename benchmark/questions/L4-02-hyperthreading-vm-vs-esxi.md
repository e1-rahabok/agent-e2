# Hyper-Threading and two vantage points

## Prompt
- Two single-vCPU VMs are both fully busy, running on the two hardware threads of the same physical core.
- Each VM shows CPU Usage around 62.5%, not 100%.

Is each VM only getting 62.5% of what it demands? What does the host report for that core?

## Likely wrong answer
"The VMs are under-utilised" — or "it's a reporting bug".

## Expected key points
- VM Usage is HT-aware: when both threads run, the VM is charged with a **37.5% penalty**, so it shows ~62.5%.
- ESXi sees the core as fully busy (100%). ESXi can see both the core and its 2 threads, while a VM cannot.
- Host values for that core: Usage (core level) = 100%; Usage (MHz, core level) reflects the Hyper-Threading benefit; Core Utilization = 100%; Thread Utilization = 100%.
- Core Utilization shows 100% whether 1 or 2 threads run. **Thread Utilization** tells which.

## Notes
- Previous id: vsphere-cpu-003 (renamed 2026-11-05).
- Tests: Same name, different meaning (consumer vs provider vantage point).

## Metadata
```yaml
id: "0003"
title: "Hyper-Threading and two vantage points"
product: [vsphere]
technology: [cpu]
input: [text]
task: read-metric
object: [vm, esxi]
tool: [vcenter]
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/usage
  - vsphere/technology/cpu/metrics/host/usage
  - vsphere/technology/cpu/metrics/host/core-utilization
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/usage
attachments: []
origin: book
source_path: "The World of Metrics > Metrics Nuances: Naming Complexity; Other Nuances (Formula)."
answer_type: judged
level: 400                      # author 2026-11-05
misconception_type: [same-name-other-object, frequency-and-hyper-threading]
status: draft
```
