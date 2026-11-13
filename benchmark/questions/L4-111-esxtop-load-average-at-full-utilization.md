# esxtop load average on a host at 100% utilization

## Prompt
- An ESXi 9.1 host has 2 sockets of 16 cores. Hyper-Threading is off, so esxtop shows 32 PCPUs.
- The esxtop CPU panel, refreshed every 5 seconds for 10 minutes, shows PCPU UTIL(%) at 100% on the average line the whole time.
- The first line shows CPU load average: 2.60, 2.55, 2.40 (1, 5 and 15 minutes).
- A colleague says: "Utilization cannot go above 100%, so the host is full but not overloaded. A load average above 1 adds nothing."

Is the colleague right? What does the load average add to PCPU UTIL here, and how do you find out whether VMs suffer?

## Likely wrong answer
"PCPU UTIL is 100%, the maximum, so the host is at capacity and that is all the CPU panel can say." Or: the load average of 2.60 read as 260% CPU utilization.

## Expected key points
- The colleague is wrong. PCPU UTIL is the share of real time a PCPU was not idle, so it stops at 100%: it shows that no PCPU is idle, not how much runnable work is waiting.
- The load average counts the run time and the ready time of all worlds on the host, against the number of PCPUs. 1.00 means the PCPUs are fully used; 2.60 means about 2.6 PCPUs of runnable work per PCPU present.
- Run time cannot exceed the 32 PCPUs. So at least 1.6 of the 2.6 (about 60%) of the runnable time is ready time: worlds that could run and wait for a PCPU. At 100% utilization the load average is the only first-line value that shows the size of that queue.
- It is not a percent of utilization, and it is a host-wide number that includes non-VM worlds and averages all of them. It does not say which VM waits.
- To find out whether VMs suffer: read CPU Ready (and Co-stop) per VM, at the 20-second peak, for the VMs on this host (esxtop %RDY per vCPU, or vCenter and VCF Operations counters). A limit counts as Ready too (%MLMTD is inside %RDY), so check for limits.
- If VMs wait, the fix is less demand on this host or more PCPUs: DRS moves, more hosts or fewer vCPUs.

## Notes
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
answer_type: judged
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
