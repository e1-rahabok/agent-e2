# VM availability

## Prompt
A VM is powered on, but Windows inside it has crashed and is stuck on a blue screen. Is the VM available? How would you measure VM availability vs Guest OS availability?

## Likely wrong answer
"No, the VM is down."

## Expected key points
- A VM is a **virtual motherboard**, not a complete machine and not the OS.
- VM is unavailable in only 2 states: **powered off**, or **frozen** (clock paused, e.g. vMotion switchover, ~0.2 s when healthy).
- So the VM is available. The **Guest OS** is not.
- Guest OS availability needs OS-level checks, e.g. `sc query RpcSs` (Windows), `systemctl is-system-running` (Linux).
- OS-level metrics (processes, threads, system calls) do not apply to a VM.

## Notes
- Tests: Principle: a VM is a virtual motherboard, not the OS.

## Metadata
```yaml
id: vsphere-foundations-002
title: "VM availability"
scope: vsphere
area: foundations
input: text
tests: concept
knowledge:
  - vsphere/foundations/vm-vs-guest-os
attachments: []
origin: book
source_path: "The World of Metrics > Metrics Nuances: What, exactly, is a VM?"
format: free-text
status: draft
```
