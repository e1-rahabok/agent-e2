# Linux OOM kill with memory available

## Prompt
- A RHEL 9 VM with 32 GB runs a Java service as a systemd unit. The vendor's unit file sets `MemoryMax=4G`.
- Twice this week the service died at its daily peak. The kernel log shows:
  `Memory cgroup out of memory: Killed process 4127 (java) total-vm:9871236kB, anon-rss:4155312kB, file-rss:0kB`
- At that time: `free -m` shows about 19,000 MB available; `sar -W` shows no swapping.
- vCenter: Memory Latency 0%, Ballooned 0, Swapped 0. The host has free memory.
- The application team asks for 16 GB more memory for the VM.

Which statements are correct?

- A. Linux as a whole ran out of memory at the peak, so the kernel's OOM killer picked the largest process.
- B. "Memory cgroup out of memory" marks a kill forced by one control group's limit; a system-wide shortage logs "Out of memory".
- C. `MemoryMax=4G` sets the unit's cgroup `memory.max`; at that limit, if reclaim cannot free enough, the OOM killer runs in the cgroup.
- D. 16 GB more for the VM will not stop the kills, because the limit belongs to the service, not to the VM or to Linux.
- E. Raise `MemoryMax` for the service, or size the Java heap and other memory so the process stays below the limit.
- F. The service's `memory.events` (counts of max, oom and oom_kill) or `systemctl status` confirm the limit was hit.
- G. Neither the VM memory counters nor the available memory of Linux as a whole can show a limit set on one cgroup.
- H. `MemoryMax` is a soft target: crossing it only throttles the service's processes and never calls the OOM killer.
- I. The process was killed for using about 9.4 GB of RAM, more than twice its 4 GB limit, as the total-vm value shows.
- J. With Memory Latency 0% in vCenter, the guest had no memory pressure, so the kill is an application bug, not memory.

## Likely wrong answer
- A: "Linux ran out of memory and the OOM killer fired: add memory to the VM."

## Expected key points
- Answer: B, C, D, E, F, G.
- A false: 19,000 MB was available in Linux; the log names a memory cgroup, so the OOM killer ran inside the service's cgroup.
- B true: the kernel prints "Memory cgroup out of memory" for a cgroup OOM and "Out of memory" for a system-wide one (mm/oom_kill.c).
- C true: memory.max is the hard limit of a cgroup; if usage reaches it and cannot be reduced, the OOM killer is invoked in the cgroup (Linux kernel, Control Group v2). systemd writes MemoryMax= to memory.max.
- D true: the VM and Linux have room already; the limit is on the unit.
- E true: fix the limit or the demand.
- F true: memory.events counts max (usage about to pass the limit), oom and oom_kill.
- G true: a cgroup limit sits inside the Guest OS; neither the VM layer nor the system-wide free memory reads it.
- H false: that describes `MemoryHigh` (memory.high), which throttles and never invokes the OOM killer; memory.max is the hard limit.
- I false: total-vm is the process's virtual address space; anon-rss, about 4 GB (4,155,312 kB), is the resident memory near the 4 GB limit.
- J false: VM Memory Latency reads ESXi page-fault waits, not a limit inside the guest; the service reached its cgroup limit.

## Notes
- Outside the knowledge base: keyed from the Linux kernel documentation and the systemd documentation.
- Linux kernel, Control Group v2: memory.max is the hard limit of a cgroup; when usage reaches it and cannot be reduced, the OOM killer runs inside the cgroup; memory.events counts max, oom and oom_kill; going over memory.high throttles and never invokes the OOM killer. https://docs.kernel.org/admin-guide/cgroup-v2.html
- systemd.resource-control(5), MemoryMax=: the absolute limit on memory usage of the unit's processes; the OOM killer acts inside the unit when it cannot be kept; written to the cgroup v2 attribute memory.max (unified hierarchy). https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html
- Linux kernel source, mm/oom_kill.c: the kill message starts with "Memory cgroup out of memory" for a cgroup OOM and "Out of memory" otherwise; total-vm prints mm->total_vm (virtual size), anon-rss the resident anonymous pages. https://github.com/torvalds/linux/blob/master/mm/oom_kill.c
- Converted from judged to multiple choice (Q199 F, 2026-11-14).

## Metadata
```yaml
id: "0272"
title: "Linux OOM kill with memory available"
product: [linux, vsphere]
technology: [memory]
task: troubleshoot
level: 400
answer_type: deterministic
answer: [B, C, D, E, F, G]
misconception: [A]
input: [text]
object: [guest-os, vm]
tool: [guest-os-tools, vcenter]
knowledge:
  - vsphere/technology/memory/concepts/guest-os-vs-vm-memory
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
knowledge_main: vsphere/technology/memory/concepts/guest-os-vs-vm-memory
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12, outside the knowledge base"
misconception_type: [layer-confusion]
status: draft
```
