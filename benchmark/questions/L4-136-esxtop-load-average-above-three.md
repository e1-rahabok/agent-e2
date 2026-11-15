# esxtop load average above 3 on a saturated host

## Prompt
- Users of several VMs on one host report slowness. A colleague says: "The host is at 100%, the maximum. Nothing more to read on this screen."
- See [the esxtop CPU panel](0377/esxtop-cpu-panel-load-average.png) of the host.

Which statements are correct?

- A. With every PCPU busy, whatever the load average shows above 1.00 is work waiting for a PCPU.
- B. A load average above 3 means the PCPUs run above 300% utilization.
- C. PCPU UTIL(%) AVG on this screen is below 90%.
- D. About two thirds or more of the runnable work on this host is waiting, not running.
- E. PCPU USED(%) reads above 100% here because it takes the clock speed into account.
- F. The VM with %MLMTD above 0 is held back by its own CPU limit: that part of its %RDY is not caused by the busy host.
- G. %MLMTD is extra wait on top of %RDY: add the two for that VM's total wait.
- H. The VM rows, not the first line, tell which VMs are held back and by how much.
- I. Migrate the VM with the highest %RDY first: the busy host is what holds it back.
- J. Every VM row should show about the same %RDY, since the load average is shared by all.

## Input to supply
- Product and version: ESXi 9.1, esxtop in an SSH session (interactive mode), CPU panel (`c`). Hyper-Threading off, or note the PCPU count shown. Turbo Boost on.
- Object: one ESXi host; on the same screen, at least five VM groups, one of them with a CPU limit (for example 2,000 MHz) on a VM that demands more.
- Screen: the CPU panel after at least 5 minutes of steady load, with the first line (load average over 1, 5 and 15 minutes), the PCPU USED(%) and PCPU UTIL(%) lines with their AVG, and the VM rows with %USED, %RUN, %RDY, %CSTP, %MLMTD (use `f` to add any missing). Save as `0377/esxtop-cpu-panel-load-average.png`.
- How to produce it in a lab: run CPU burners in VMs whose vCPUs total 3-4 times the host's PCPUs; set a CPU limit on one of them.
- Condition the key depends on: load average (1 minute) between 3.2 and 4.0; PCPU UTIL(%) AVG 98-100; PCPU USED(%) AVG above 100; VM rows with %RDY well above 0, the highest at least twice the lowest; the limited VM with the highest %RDY of all VM rows, %MLMTD making up most of it.
- Masking: mask every VM, host, datastore and cluster name.

## Likely wrong answer
B: a load average above 3 means more than 300% utilization. Or the colleague's view: UTIL is at 100%, so the screen says nothing more.

## Expected key points
- Answer: A, D, E, F, H.
- A true: the load average counts running and ready-to-run worlds against the PCPU count; running work cannot exceed the PCPUs, so the excess over 1.00 is waiting work.
- B false: the misconception. It is runnable work per PCPU, not a percentage of utilization.
- C false: reading. UTIL AVG is at 98-100%: no PCPU is idle.
- D true: with a load average L of 3.2-4.0 and at most 1.00 running, the waiting share is at least (L - 1) / L: about 69-75%.
- E true: reading. USED builds on UTIL and adds frequency; Turbo lifts it above 100% while UTIL stays at 100%.
- F true: Max Limited is time held back by a limit, not by lack of CPU.
- G false: %MLMTD is counted inside %RDY; adding them counts it twice.
- H true: Ready is a consumer counter; the first line is one host-wide number over all worlds, VM and non-VM.
- I false: wrong action. The VM with the highest %RDY is the limited one, and most of its Ready is %MLMTD: its own limit, which moves with it. Moving it does not end that wait; the host holds back the other VMs with high %RDY.
- J false: reading and mechanism. The rows differ by a factor of two or more: each VM's wait depends on its own demand, shares and limits, not on the host average.

## Reasoning path
1. UTIL at 100%: no PCPU idle; it cannot show the queue.
2. Load average above 3: most of the runnable work is waiting.
3. Per VM: %RDY, and %MLMTD inside it for the limited VM.

## Notes
- Paired with the theory question 0331 (theory and practical; design.md, section 3.9).
- Sources as in 0331: Broadcom KB 304594 and KB 382249 (load average: run and ready time of all groups against the PCPUs; 1.00 means fully used); vSphere Monitoring and Performance, CPU Panel (PCPU UTIL(%) is non-idle time).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C34). Counts only after author approval.
- Review 2026-11-15: load average range moved to 3.2-4.0 (off 0331's 2.6); options reworded away from 0331; screen readings C and J (false) and D (true) added; the %MLMTD part kept. Key changed from A, D, E, F, I to A, D, E, F, H (new options).

## Metadata
```yaml
id: "0377"
title: "esxtop load average above 3 on a saturated host"
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
answer: [A, D, E, F, H]
misconception: [B]
misconception_type: [consumption-as-contention, tool-confusion]
pair: "0331"
status: awaiting-input
```
