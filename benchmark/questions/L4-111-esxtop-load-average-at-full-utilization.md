# esxtop load average on a host at 100% utilization

## Prompt
- An ESXi 9.1 host has 2 sockets of 16 cores. Hyper-Threading is off, so esxtop shows 32 PCPUs.
- The esxtop CPU panel, refreshed every 5 seconds for 10 minutes, shows PCPU UTIL(%) at 100% on the average line the whole time.
- The first line shows CPU load average: 2.60, 2.55, 2.40 (1, 5 and 15 minutes).
- A colleague says: "Utilization cannot go above 100%, so the host is full but not overloaded. A load average above 1 adds nothing."

Which statements are correct?

- A. A load average of 2.60 means the CPUs of the host run at 260% utilization, beyond what PCPU UTIL can show.
- B. Once PCPU UTIL has reached 100%, a load average above 1.00 adds no information about the host.
- C. PCPU USED(%) stops at 100% in the same way as PCPU UTIL(%), so both lines read alike.
- D. The load average sets the run and ready time of all worlds against the PCPU count; 1.00 means full use.
- E. If VMs wait, the remedy is less demand on this host or more PCPUs: DRS moves, more hosts, fewer vCPUs.
- F. Run time cannot exceed the 32 PCPUs, so at least 1.6 of the 2.6 is ready time: worlds waiting for a PCPU.
- G. To see whether VMs suffer, read CPU Ready and Co-stop per VM at the 20-second peak.
- H. PCPU UTIL(%) is the share of time a PCPU was not idle, so it cannot go above 100%.
- I. The load average counts only the vCPU worlds of VMs, so system and kernel worlds do not move it.
- J. A CPU limit on a VM shows inside its Ready in esxtop: %MLMTD is part of %RDY.
- K. The load average tells which VM is waiting for a PCPU, so it points to the VM to move.

## Likely wrong answer
- A: "A load average of 2.60 means 260% CPU utilization."
- B: "PCPU UTIL is 100%, the maximum, so the host is at capacity and that is all the CPU panel can say."

## Expected key points
- Answer: D, E, F, G, H, J.
- A is false: the load average is not a percent of utilization; it is runnable work per PCPU, run plus ready.
- B is false: the colleague's claim; UTIL saturates at 100% while the load average keeps rising with the ready time.
- C is false: PCPU USED(%) builds on UTIL and adds frequency; it can exceed 100% (example 131%, Turbo above nominal) while UTIL stops at 100%.
- D is true: the load average accounts the run time and ready time of all worlds on the host against the number of PCPUs (KB 382249); 1.00 means the PCPUs are fully used (KB 304594). 2.60 is about 2.6 PCPUs of runnable work per PCPU present.
- E is true: if VMs wait, lower the demand on this host or add PCPUs: DRS moves, more hosts or fewer vCPUs.
- F is true: run time is capped by the PCPU count, so 2.60 - 1.00 = 1.60 (about 60% of the runnable time) is ready time at least. At 100% UTIL the load average is the only first-line value that shows the size of that queue.
- G is true: Ready is a consumer metric; whether VMs suffer is read per VM (esxtop %RDY per vCPU, or the vCenter and VCF Operations counters), at the 20-second peak.
- H is true: PCPU UTIL is the percentage of real time the PCPU was not idle; it shows that no PCPU is idle, not how much runnable work waits.
- I is false: the load average counts all worlds (groups) on the host, including non-VM worlds.
- J is true: %MLMTD (Max Limited) is counted inside %RDY, so check for limits before blaming the host.
- K is false: it is a host-wide number that averages all worlds, VM and non-VM; it does not say which VM waits.

## Notes
- Converted from judged to multiple choice (Q199 F, 2026-11-14). The options avoid the word overloaded as a verdict (sources disagree on it).
- Public source: Broadcom KB 304594, "Troubleshooting ESX/ESXi virtual machine performance issues" (ESXi 7.x and 8.x): "A load average of 1.00 means that the ESXi/ESX Server machine's physical CPUs are fully utilized". Broadcom KB 382249, "Using ESXTop and Interpreting ESXTop Statistics" (ESXi 7.0 and 8.0): CPU load "accounts the run time and ready time for all the groups on the host". vSphere Monitoring and Performance 9.0, CPU Panel (last updated 2026-10-28 for the 8.0 copy, 2026-10-19 for the 9.0 index): "PCPU UTIL(%) represents the percentage of real time that the PCPU was not idle" and "100% = %RUN + %RDY + %CSTP + %WAIT". https://knowledge.broadcom.com/external/article/304594/troubleshooting-esxesxi-virtual-machine.html and https://knowledge.broadcom.com/external/article/382249/using-esxtop-and-interpreting-esxtop-sta.html . The sentence "2.00 means twice the PCPUs" is in the vSphere 6.5/6.7 documentation; the current 9.x CPU Panel page does not repeat the load-average text, so it is cited from the two KB articles.
- Why one answer: the load average adds ready time to run time and divides by the PCPU count (documented); run time cannot exceed the PCPU count; 2.60 minus 1.00 is then ready time. UTIL is capped at 100% by its definition.
- Debatable risk: sources disagree on the word "overloaded" (the Performance Best Practices say a value of 1 or more is overloaded; KB 304594 says 2.00 is overloaded). The question and key avoid that word as a verdict and rely only on the counter definitions. The 60% figure is a lower bound of the average over the window, not an exact share.

## Metadata
```yaml
id: "0331"
title: "esxtop load average on a host at 100% utilization"
product: [vsphere]
technology: [cpu]
task: read-metric
level: 400
answer_type: deterministic
answer: [D, E, F, G, H, J]
misconception: [B, A]
input: [text]
object: [esxi]
tool: [esxtop]
knowledge:
  - vsphere/object-types/esxi/esxi-health-check
  - vsphere/tools/esxtop/cpu
  - vsphere/technology/cpu/metrics/host/utilization
knowledge_main: vsphere/tools/esxtop/cpu
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
misconception_type: [consumption-as-contention, tool-confusion]
status: draft
```
