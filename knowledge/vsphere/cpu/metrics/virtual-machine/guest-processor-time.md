# Guest OS Processor counters (Windows PerfMon)

## Time-based
| Counter | Meaning |
|---|---|
| % Processor Time, % Idle Time | Add up to 100%. |
| % Priority Time | Part of Processor Time spent by elevated-priority threads. |
| % User Time, % Privileged Time | Add up to 100%. A thread switches modes on system calls without a context switch. The author sees little use for the split. |
| % DPC Time | Deferred procedure calls, part of Privileged Time; lower priority than interrupts. High: Windows busy with higher-priority work. Can occur at low CPU with driver or application issues; CPU 0 often higher. |
| % Interrupt Time | Interrupts (clock every 10 ms, network, input). High values hurt performance. |
| % C1, C2, C3 Time | Time in each power level (C0 highest power, C3 lowest). May not add up to Idle Time. |

## Rate-based
| Counter | Meaning |
|---|---|
| C1, C2, C3 Transitions/sec | Frequency of entering each level. High on all three: inconsistent speed. |
| DPC Rate, Interrupts/sec | Inputs to the time counters. |
| System Calls/sec | User-to-kernel transitions (Ring 3 to Ring 0). High together with Privileged Time above 30%: too much OS work. Above 20,000 per core is high; usually below 2,000. Not collected by VMware Tools. |

## Traps
- "Privileged Time high means a CPU shortage" → it means kernel or driver work.

## Metadata
```yaml
id: vsphere/cpu/metrics/virtual-machine/guest-processor-time
retriever_guide: metric-meaning
scope: vsphere
technology:
- cpu
pillar:
- performance
- capacity
product:
- windows
- vcf-operations
object:
- VirtualMachine
metric_class: consumption
internal_derive: []
same_name: []
same_meaning: []
related:
- vsphere/cpu/concepts/windows-cpu-scheduling
source:
  document: PART 3 - Counters.docx
  path: MS Windows > CPU; DPC Time
corrections: []
review_notes: []
status: draft
```
