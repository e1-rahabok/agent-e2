---
id: vsphere/foundations/vm-vs-guest-os
type: concept
scope: vsphere
resources: [cpu, memory, storage, network]
objects: [vm, guest-os]
related:
  - vsphere/foundations/visibility-layers
  - vsphere/foundations/kernel-worlds
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Virtualization Impact > What, exactly, is a VM?
corrections: []
review_notes: []
status: draft
---

# VM vs Guest OS

## Definition
- A VM is a virtual motherboard: a circuit board with electronics mounted on it.
- A VM is not a complete machine. It is not an operating system.
- The Guest OS (Windows, Linux) is a separate layer running on the VM.
- VM and Guest OS have a 1:1 relationship and are adjacent layers. They are still distinct.
- Common mistake: the word "machine" suggests a complete entity (like a washing machine or ATM). That mental model makes people mix up VM and Guest OS.

## Consequences for metrics
- OS-level metrics are not VM metrics. Examples that do not apply to a VM:
  - processes,
  - threads,
  - system calls per second.
- A VM introduces its own metrics and properties.
- Resources consumed by the Guest OS ≠ resources consumed by the VM. Power management and CPU SMT add to the difference.
- See `vsphere/foundations/visibility-layers` for what each layer can and cannot see.

## Availability: VM
- The virtual motherboard is unavailable in only two states:

| State | Meaning |
|---|---|
| Powered off | BIOS not running. |
| Frozen | System clock paused. Occurs during the actual downtime of vMotion (not stun time, not copy time). About 0.2 s when healthy. |

- If the BIOS is running, the VM is 100% available, even if Windows or Linux has not booted.

## Availability: Guest OS
- Requires checking that the kernel, scheduler, disk subsystem and core IPC/management layers are responding.

| OS | Command | Meaning |
|---|---|---|
| Windows | `sc query RpcSs` | `sc.exe` queries the Service Control Manager (SCM), the Windows subsystem managing background services, drivers and startup processes. |
| Linux | `systemctl is-system-running` | Queries systemd's state manager across all managed daemons. |

- `systemctl is-system-running` results:
  - `running`: all initialized daemons active.
  - `degraded`: kernel and main system up; at least one service failed or crashed.
  - `starting` / `stopping`: booting or shutting down.

## Traps
- "Guest OS crashed, so the VM is down" → wrong. The VM is available while BIOS runs; the Guest OS is unavailable.
- Asking for VM process or thread counts → wrong layer. Those are Guest OS metrics.
