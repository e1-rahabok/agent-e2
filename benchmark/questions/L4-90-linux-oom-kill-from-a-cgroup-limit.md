# Linux OOM kill with memory available

## Prompt
- A RHEL 9 VM with 32 GB runs a Java service as a systemd unit. The vendor's unit file sets `MemoryMax=4G`.
- Twice this week the service died at its daily peak. The kernel log shows:
  `Memory cgroup out of memory: Killed process 4127 (java) total-vm:9871236kB, anon-rss:4155312kB, file-rss:0kB`
- At that time: `free -m` shows about 19,000 MB available; `sar -W` shows no swapping.
- vCenter: Memory Latency 0%, Ballooned 0, Swapped 0. The host has free memory.
- The application team asks for 16 GB more memory for the VM.

Why was the process killed, and will 16 GB more help? What do you change?

## Likely wrong answer
"Linux ran out of memory and the OOM killer fired: add memory to the VM."

## Expected key points
- The kill came from a memory limit on one control group, not from Linux running out of memory: the log says "Memory cgroup out of memory". A system-wide shortage logs "Out of memory" without "Memory cgroup".
- systemd `MemoryMax=4G` sets the cgroup's `memory.max`. When the service's memory reaches it and reclaim cannot free enough, the kernel runs the OOM killer inside that cgroup, even with 19 GB available in Linux.
- 16 GB more for the VM does not help: the limit belongs to the service, not to the VM or to Linux.
- Fix the limit or the demand: raise `MemoryMax` for the service, or size the Java heap and other memory so the process stays below it.
- Confirm in the cgroup: `memory.events` of the service (`max`, `oom`, `oom_kill` counts) or `systemctl status`.
- VM memory counters and Linux's own available memory cannot show a per-cgroup limit.

## Notes
- Outside the knowledge base: keyed from the Linux kernel documentation and the systemd documentation.
- Linux kernel, Control Group v2: memory.max is the hard limit of a cgroup; when usage reaches it and cannot be reduced, the OOM killer runs inside the cgroup; memory.events counts max, oom and oom_kill. https://docs.kernel.org/admin-guide/cgroup-v2.html
- systemd.resource-control(5), MemoryMax=: the absolute limit on memory usage of the unit's processes; the OOM killer acts inside the unit when it cannot be kept; written to the cgroup v2 attribute memory.max (unified hierarchy). https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html

## Metadata
```yaml
id: "0272"
title: "Linux OOM kill with memory available"
product: [linux, vsphere]
technology: [memory]
task: troubleshoot
level: 400
answer_type: judged
input: [text]
object: [guest-os, vm]
tool: [guest-os-tools, vcenter]
knowledge:
  - vsphere/technology/memory/concepts/guest-os-vs-vm-memory
knowledge_main: vsphere/technology/memory/concepts/guest-os-vs-vm-memory
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12 for the outside-the-knowledge-base slot of the Guest OS area (project/plan.md, M2)"
misconception_type: [layer-confusion]
status: draft
```
