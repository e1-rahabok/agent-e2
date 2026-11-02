---
id: vsphere/cpu/metrics/virtual-machine/wait
retriever_guide: metric-meaning
scope: vsphere
technology:
- cpu
pillar:
- performance
product:
- vsphere
object:
- VirtualMachine
metric_class: context
internal_derive:
- vsphere/foundations/provider-consumer
- vsphere/cpu/concepts/vcpu-states
same_name: []
same_meaning: []
related:
- vsphere/cpu/concepts/guest-os-vs-vm-cpu
- vsphere/cpu/concepts/idle-and-unused-vcpus
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity; CPU > Architecture (pp. 52-78) > State of a VM vCPU
corrections: []
review_notes:
- metric_class set to context. The book groups Wait separately from contention and consumption. Author to confirm.
- Sections Mechanism and the last trap: from CPU > Architecture in the pre-correction book file (uploaded 2026-11-02). Re-check when the corrected file is uploaded.
status: draft
---

# VM CPU Wait

## Meaning
- Includes idle time.
- Most VMs do not run at 100%, so CPU Wait is naturally high.

## Why the name is still correct
- From the kernel scheduler's vantage point, an idle vCPU is waiting to be used.

## Mechanism
- Wait covers both idle and IO wait. The hypervisor cannot tell whether the Guest OS waits for IO or is idle.
- Wait also covers wait caused by hypervisor IO (VM IO).
- Idle means the vCPU executes the idle loop. A CPU cannot stop executing instructions without powering down. The kernel runs a lowest-priority idle task.
- Guest OS IO wait can appear as VM Run (guest IO processing) or as VM Wait (VM IO).
- Wait is one of 4 states: Run + Ready + Co-stop + Wait = 100%, per vCPU.
- See `vsphere/cpu/concepts/vcpu-states`.

## Traps
- "High CPU Wait means the VM waits for disk or memory" → wrong. Mostly idle time.
- "VM Wait equals Guest OS IO Wait" → Guest OS IO wait can show as VM Run or VM Wait.
