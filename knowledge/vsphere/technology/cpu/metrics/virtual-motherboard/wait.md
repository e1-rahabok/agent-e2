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
- See `vsphere/technology/cpu/concepts/vcpu-states`.

## Sub-metrics
```text
Wait = Idle + Swap Wait + Other Wait
```

| Sub-metric | Waiting for | Guest OS sizing |
|---|---|---|
| Idle | Work. | Exclude. |
| Swap Wait | Memory pages from ESXi swap. | Include. |
| Other Wait | Anything else: disk IO, network IO, vMotion, snapshots. | Include. |

- Wait mixes consumption (Idle) and contention (Swap Wait, Other Wait). The book groups it separately.
- The Guest OS does not see Swap Wait or Other Wait. It experiences a freeze.

## Misconceptions
- "High CPU Wait means the VM waits for disk or memory" → wrong. Mostly idle time.
- "VM Wait equals Guest OS IO Wait" → Guest OS IO wait can show as VM Run or VM Wait.

## Metadata
```yaml
id: vsphere/technology/cpu/metrics/virtual-motherboard/wait
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
layer:
- virtual-motherboard
metric_class: context
internal_derive:
- vsphere/architecture/provider-consumer
- vsphere/technology/cpu/concepts/vcpu-states
same_name: []
same_meaning: []
related:
- vsphere/technology/cpu/concepts/guest-os-vs-vm-cpu
- vsphere/technology/cpu/concepts/idle-and-unused-vcpus
- vsphere/technology/cpu/metrics/virtual-motherboard/idle
- vsphere/technology/cpu/metrics/virtual-motherboard/swap-wait
- vsphere/technology/cpu/metrics/virtual-motherboard/other-wait
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: The World of Metrics > Metrics Nuances > Complexity > Naming Complexity; CPU > Architecture > State of a VM vCPU; CPU > VM > Wait Metrics
corrections: []
review_notes:
- 'To check: metric_class: set to context; the book groups Wait separately from contention and consumption.'
- Sections Mechanism and the last misconception: from CPU > Architecture.
- 'Section Sub-metrics: from CPU > VM. The IO wait and memory wait cases in vsphere/technology/cpu/concepts/vcpu-states map to Other Wait and Swap Wait.'
status: draft
```
