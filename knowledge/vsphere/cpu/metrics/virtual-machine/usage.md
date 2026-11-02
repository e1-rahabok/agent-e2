---
id: vsphere/cpu/metrics/virtual-machine/usage
retriever_guide: metric-meaning
scope: vsphere
technology:
- cpu
pillar:
- performance
- capacity
product:
- vsphere
object:
- VirtualMachine
metric_class: consumption
internal_derive:
- vsphere/cpu/concepts/hyper-threading
- vsphere/foundations/provider-consumer
- vsphere/cpu/concepts/run-time-vs-run-quality
- vsphere/cpu/concepts/cpu-frequency
same_name:
- vsphere/cpu/metrics/host/usage
same_meaning: []
related:
- vsphere/cpu/metrics/comparisons/consumption-metrics
- vsphere/cpu/metrics/host/core-utilization
- vsphere/cpu/concepts/frequency-and-ht-impact-on-vm
- vsphere/cpu/concepts/cpu-efficiency
- vsphere/cpu/concepts/guest-os-vs-vm-cpu
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity; CPU > Architecture (pp. 52-78) > Guest OS vs VM; ESXi ≠ VM + Kernel; CPU Throughput; Impacts on VM
corrections:
- '2026-11-02: Hyper-Threading scenario (section: Hyper-Threading) rewritten from the author. The uploaded document sentence is truncated.'
review_notes:
- The 37.5% penalty is from the author. Not found in Performance Best Practices for vSphere 9.1.
- Sections Throughput, Masked degradation, and the last trap: from CPU > Architecture in the pre-correction book file (uploaded 2026-11-02). Re-check when the corrected file is uploaded.
status: draft
---

# VM CPU Usage

## Hyper-Threading
- Scenario: two vCPUs run on the two threads of the same physical core at the same time.
- VM Usage is HT-aware. When both threads run, the VM is charged a 37.5% penalty, so it shows about 62.5%.
- The VM cannot see the core or its two threads. ESXi can.
- The host view of the same core: see `vsphere/cpu/metrics/host/usage`.

## Cap
- VM CPU Usage (MHz) is not capped.

## Reservation
- CPU reservation is on demand. It is not included in Usage.

## Throughput
- Usage (MHz) counts cycles completed. Read it as throughput.
- The author's name for this metric: CPU Throughput.
- It includes frequency (Turbo, power management) and Hyper-Threading efficiency.
- It includes IO processing done by the hypervisor on behalf of the VM. Significant for heavy databases and NSX Edge.
- It is a performance metric, not a capacity metric: 100% cannot be defined.

## Masked degradation
- At Run 100%, throughput per vCPU can fall from 1.7 GHz to 0.81 GHz as the host fills up (sample CPU, 1 GHz nominal).
- Usage (%) masks this degradation.
- See `vsphere/cpu/concepts/frequency-and-ht-impact-on-vm`.

## Traps
- "VM shows 62.5%, so the metric is wrong" → wrong. Different vantage point from the host.
- "Each VM gets only 62.5% of what it demands" → the 62.5% is an accounting charge for sharing a core.
- "Use Usage for capacity" → it includes frequency. Use Run for capacity.
