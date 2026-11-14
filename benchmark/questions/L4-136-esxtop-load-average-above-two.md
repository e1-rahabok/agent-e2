# esxtop load average above 2 on a saturated host

## Prompt
- Users of several VMs on one host report slowness. A colleague says: "The host is at 100%, the maximum. Nothing more to read on this screen."
- See [the esxtop CPU panel](0377/esxtop-cpu-panel-load-average.png) of the host.

Which statements are correct?

- A. The load average sets the running and ready-to-run worlds against the PCPU count, so the part above 1.00 is at least that much ready time.
- B. A load average above 2 means the PCPUs run above 200% utilization.
- C. Once PCPU UTIL(%) reaches 100%, the load average adds nothing about the host.
- D. PCPU UTIL(%) is the share of time a PCPU was not idle, so it stops at 100%.
- E. PCPU USED(%) reads above 100% here because it takes the clock speed into account.
- F. The VM with %MLMTD above 0 is held back by its own CPU limit: that part of its %RDY is not caused by the busy host.
- G. %MLMTD is extra wait on top of %RDY: add the two for that VM's total wait.
- H. The load average shows which VMs wait for a PCPU, so it points to the VM to move.
- I. To see which VMs suffer, read %RDY per VM and per vCPU, not the load average.
- J. Migrate the VM with the highest %RDY first: the busy host is what holds it back.

## Input to supply
- Product and version: ESXi 9.1, esxtop in an SSH session (interactive mode), CPU panel (`c`). Hyper-Threading off, or note the PCPU count shown. Turbo Boost on.
- Object: one ESXi host; on the same screen, at least five VM groups, one of them with a CPU limit (for example 2,000 MHz) on a VM that demands more.
- Screen: the CPU panel after at least 5 minutes of steady load, with the first line (load average over 1, 5 and 15 minutes), the PCPU USED(%) and PCPU UTIL(%) lines with their AVG, and the VM rows with %USED, %RUN, %RDY, %CSTP, %MLMTD (use `f` to add any missing). Save as `0377/esxtop-cpu-panel-load-average.png`.
- How to produce it in a lab: run CPU burners in VMs whose vCPUs total 2-3 times the host's PCPUs; set a CPU limit on one of them.
- Condition the key depends on: load average (1 minute) between 2.0 and 3.0; PCPU UTIL(%) AVG 98-100; PCPU USED(%) AVG above 100; several VM rows with %RDY well above 0; the limited VM with the highest %RDY of all VM rows, %MLMTD making up most of it.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
B: a load average above 2 means more than 200% utilization. Or C: UTIL is 100%, the maximum, so the screen says nothing more.

## Expected key points
- Answer: A, D, E, F, I.
- A true: the load average accounts run and ready time of all worlds against the PCPU count; run time cannot exceed the PCPUs, so the excess over 1.00 is ready time at least.
- B false: the misconception. It is runnable work per PCPU, not a percentage of utilization.
- C false: the colleague's claim. UTIL saturates at 100% while the load average keeps rising with the queue.
- D true: UTIL is non-idle time per PCPU.
- E true: USED builds on UTIL and adds frequency; Turbo lifts it above 100% while UTIL stays at 100%.
- F true: Max Limited is time held back by a limit, not by lack of CPU.
- G false: %MLMTD is counted inside %RDY; adding them counts it twice.
- H false: the load average is one host-wide number over all worlds, VM and non-VM; it does not say which VM waits.
- I true: Ready is a consumer counter; read it per VM.
- J false: wrong action. The VM with the highest %RDY is the limited one, and most of its Ready is %MLMTD: its own limit, which moves with it. Moving it does not end that wait; the host holds back the other VMs with high %RDY.

## Reasoning path
1. UTIL at 100%: no PCPU idle; it cannot show the queue.
2. Load average above 2: at least half of the runnable time is waiting.
3. Per VM: %RDY, and %MLMTD inside it for the limited VM.

## Notes
- Paired with the theory question 0331 (theory and practical; design.md, section 3.9).
- Sources as in 0331: Broadcom KB 304594 and KB 382249 (load average: run and ready time of all groups against the PCPUs; 1.00 means fully used); vSphere Monitoring and Performance, CPU Panel (PCPU UTIL(%) is non-idle time).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C34). Counts only after author approval.

## Metadata
```yaml
id: "0377"
title: "esxtop load average above 2 on a saturated host"
product: [vsphere]
technology: [cpu]
task: troubleshoot
level: 400
answer_type: deterministic
input: [screenshot]
object: [esxi, vm]
tool: [esxtop]
knowledge:
  - vsphere/tools/esxtop/cpu
  - vsphere/technology/cpu/metrics/host/utilization
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
knowledge_main: vsphere/tools/esxtop/cpu
attachments:
  - 0377/esxtop-cpu-panel-load-average.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C34"
answer: [A, D, E, F, I]
misconception: [B, C]
misconception_type: [consumption-as-contention, tool-confusion]
pair: "0331"
status: awaiting-input
```
