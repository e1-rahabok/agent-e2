# Guest OS availability check

## Check
- A Guest OS is available when its kernel, scheduler, disk subsystem and core IPC and management layers respond. A running VM says nothing about it: the virtual motherboard is available once its BIOS runs, booted Guest OS or not ([`vsphere/architecture/vm-vs-guest-os`](../../vsphere/architecture/vm-vs-guest-os.md), section Availability: VM).
- The check queries the service manager inside the Guest OS, because the service manager answers only when those layers work.

| OS | Command | Meaning |
|---|---|---|
| Windows | `sc query RpcSs` | `sc.exe` queries the Service Control Manager (SCM), the Windows subsystem managing background services, drivers and startup processes. |
| Linux | `systemctl is-system-running` | Queries systemd's state manager across all managed daemons. |

- `systemctl is-system-running` results:
  - `running`: all initialized daemons active.
  - `degraded`: kernel and main system up; at least one service failed or crashed.
  - `starting` / `stopping`: booting or shutting down.

## Misconceptions
- "The VM is powered on, so the Guest OS is up" → the VM is available once its BIOS runs; the Guest OS can still be booting, hung or degraded. Query the service manager inside the Guest OS.

## Metadata
```yaml
id: guest-os/system/guest-os-availability
retriever_guide: how-it-works
scope: guest-os
technology:
- system
pillar:
- availability
product:
- windows
- linux
layer:
- guest-os
internal_derive:
- vsphere/architecture/vm-vs-guest-os
related: []
source:
  document: Knowledge base
  path: 'Availability: Guest OS'
corrections: []
review_notes: []
status: draft
```
