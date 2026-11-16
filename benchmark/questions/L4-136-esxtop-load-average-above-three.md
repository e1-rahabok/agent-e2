# esxtop load average above 3 on a saturated host

## Prompt
- Users of several VMs on the host esx-c4-12 report slowness. A colleague says: "The host is at 100%, the maximum. Nothing more to read in esxtop."
- The host has 16 cores in one socket, Hyper-Threading off.
- esxtop on the host, CPU panel, after 10 minutes of steady load:

```text
10:42:17am up 41 days 03:12, 1458 worlds, 9 VMs, 72 vCPUs; CPU load average: 3.60, 3.52, 3.31
PCPU USED(%):  109  108  109  109  109  109  108  108  109  108  109  110  108  108  109  108 NUMA:  109 AVG:  109
PCPU UTIL(%): 99.4 99.5 99.4 99.8 99.6 99.6 99.2 99.6 99.5 99.4 99.7 99.6  100 99.6 99.4 98.9 NUMA: 99.5 AVG: 99.5
         ID         GID NAME             NWLD   %USED    %RUN    %SYS   %WAIT %VMWAIT    %RDY   %IDLE  %OVRLP   %CSTP  %MLMTD  %SWPWT 
    2112002     2112002 app-ora-02         20  275.84  252.14    1.19  823.16   11.91  881.76   12.57    0.21   42.94    0.00    0.00 
    2108001     2108001 dw-etl-01          24  255.05  233.68    1.39  834.34   11.36 1315.17   24.66    1.03   16.81 1163.21    0.00 
    2116003     2116003 web-fe-03          16  230.95  209.85    2.56  813.34    7.63  542.99    7.11    0.48   33.82    0.00    0.00 
    2120004     2120004 web-fe-04          16  222.11  204.00    0.93  812.38    7.35  555.38    6.48    1.11   28.24    0.00    0.00 
    2128006     2128006 mq-node-06         16  212.73  194.10    1.39  811.55    6.73  567.96    6.43    0.28   26.39    0.00    0.00 
    2124005     2124005 api-gw-05          16  193.85  176.34    2.30  813.18    7.56  581.60    7.12    0.76   28.88    0.00    0.00 
    2136008     2136008 bld-08             12   98.48   88.22    2.72  805.37    3.50  300.16    3.45    0.57    6.25    0.00    0.00 
    2132007     2132007 bld-07             12   92.45   83.17    2.94  806.94    4.27  304.95    3.89    1.27    4.94    0.00    0.00 
    2140009     2140009 ci-runner-09       12   92.33   83.81    1.67  805.69    3.58  306.47    3.86    0.75    4.03    0.00    0.00 
    2140026     2140026 system            442   50.50   21.49   24.90 44174.31       -    4.20    0.00    0.05    0.00    0.00    0.00 
    2140111     2140111 esxtop.2159953      1    5.97    4.73    0.84   94.76       -    0.51    0.00    0.09    0.00    0.00    0.00 
    2140060     2140060 vpxa.2198865       41    1.99    1.47    0.37 4098.39       -    0.14    0.00    0.01    0.00    0.00    0.00 
    2140094     2140094 sensord.2197719    12    1.53    1.05    0.41 1198.75       -    0.20    0.00    0.06    0.00    0.00    0.00 
    2140043     2140043 hostd.2166502      47    0.99    0.75    0.20 4698.98       -    0.27    0.00    0.04    0.00    0.00    0.00 
    2140077     2140077 envoy.2166267      17    0.78    0.36    0.45 1698.86       -    0.78    0.00    0.09    0.00    0.00    0.00 
```

Which statements are correct?

- A. With every PCPU busy, whatever the load average shows above 1.00 is work waiting for a PCPU.
- B. A load average above 3 means the PCPUs run above 300% utilization.
- C. PCPU UTIL(%) AVG in the panel is below 90%.
- D. About two thirds or more of the runnable work on this host is waiting, not running.
- E. PCPU USED(%) reads above 100% in the panel because it takes the clock speed into account.
- F. The VM with %MLMTD above 0 is held back by its own CPU limit: that part of its %RDY is not caused by the busy host.
- G. %MLMTD is extra wait on top of %RDY: add the two for that VM's total wait.
- H. The VM rows, not the first line, tell which VMs are held back and by how much.
- I. Migrate the VM with the highest %RDY first: the busy host is what holds it back.
- J. Every VM row should show about the same %RDY, since the load average is shared by all.

## Likely wrong answer
B: a load average above 3 means more than 300% utilization. Or the colleague's view: UTIL is at 100%, so the screen says nothing more.

## Expected key points
- Answer: A, D, E, F, H.
- A true: the load average counts running and ready-to-run worlds against the PCPU count; running work cannot exceed the PCPUs, so the excess over 1.00 is waiting work. Every PCPU UTIL(%) value is 98.5-100.
- B false: the misconception. It is runnable work per PCPU, not a percentage of utilization.
- C false: the reading. PCPU UTIL(%) AVG is 99-100: no PCPU is idle.
- D true: the 1-minute load average L is 3.2-4.0; with at most 1.00 running, the waiting share is at least (L - 1) / L: about 69-75%.
- E true: the reading. USED builds on UTIL and adds frequency; Turbo lifts PCPU USED(%) AVG above 100 (about 105-112) while UTIL stays at 99-100.
- F true: Max Limited is time held back by a limit, not by lack of CPU. One VM row has %MLMTD above 0, most of its %RDY.
- G false: %MLMTD is counted inside %RDY; adding them counts it twice.
- H true: Ready is a consumer counter; the first line is one host-wide number over all worlds, VM and non-VM.
- I false: the wrong action. The VM with the highest %RDY is the limited one, and most of its Ready is %MLMTD: its own limit, which moves with it. Moving it does not end that wait; the host holds back the other VMs with high %RDY.
- J false: the reading and the mechanism. The highest VM %RDY is more than twice the lowest: each VM's wait depends on its own vCPU count, demand, shares and limits, not on the host average.

## Reasoning path
1. UTIL at 100%: no PCPU idle; it cannot show the queue.
2. Load average above 3: most of the runnable work is waiting.
3. Per VM: %RDY, and %MLMTD inside it for the limited VM.

## Notes
- Paired with the theory question 0331 (theory and practical; design.md, section 3.9).
- Sources as in 0331: Broadcom KB 304594 and KB 382249 (load average: run and ready time of all groups against the PCPUs; 1.00 means fully used); vSphere Monitoring and Performance, CPU Panel (PCPU UTIL(%) is non-idle time).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C34). Counts only after author approval.
- Converted to exports 2026-11-15 (project/practical-questions-as-exports-2026-11-15.md): the esxtop CPU panel as text in the prompt, generated by project/tools/exportgen. C and E reworded from screen to panel; the PCPU count stated as a case fact. Key unchanged: A, D, E, F, H.
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
input: [text]
object: [esxi, vm]
tool: [esxtop]
knowledge:
  - vsphere/tools/esxtop/cpu
  - vsphere/technology/cpu/metrics/host/utilization
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
knowledge_main: vsphere/tools/esxtop/cpu
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C34"
answer: [A, D, E, F, H]
misconception: [B]
misconception_type: [consumption-as-contention, tool-confusion]
pair: "0331"
status: draft
```
