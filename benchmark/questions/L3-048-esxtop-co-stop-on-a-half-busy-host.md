# esxtop Co-stop on a host at half load

## Prompt
- A database team says their 16-vCPU VM, ora-db-07, stalls for short moments and asks for 8 more vCPUs.
- Its host: ESXi 9.1, one socket of 24 cores, Hyper-Threading on (48 PCPUs). The other VMs on it: app-11 to app-16 with 4 vCPUs each; jump-01, dns-02 and ntp-03 with 1 vCPU each.
- You run esxtop on the host, open the CPU panel and expand ora-db-07 with `e`:

```text
10:42:17am up 63 days 04:11, 903 worlds, 10 VMs, 43 vCPUs; CPU load average: 0.55, 0.56, 0.56
PCPU USED(%): 59.3 33.6 39.8 29.3 33.3 27.3 43.8 49.2 46.4 50.6 31.7 43.9 50.2 51.4 67.1 28.8 57.5 46.0 48.6 40.2 47.0 61.4 34.7 40.4 59.8 31.4 51.5 40.3 41.4 42.3 37.2 52.1 53.1 49.9 52.3 56.1 40.7 62.7 43.3 51.4 49.7 45.1 40.5 36.6 60.7 48.5 44.3 54.7 NUMA: 46.0 AVG: 46.0
PCPU UTIL(%): 65.3 39.0 44.8 34.0 39.0 30.0 46.7 54.7 50.0 58.8 37.0 51.0 58.9 55.5 72.1 31.2 65.4 49.9 56.0 46.5 49.6 65.3 36.8 46.1 67.4 36.4 57.9 46.4 47.5 47.5 39.6 57.1 57.8 58.2 60.1 61.1 45.0 71.2 48.0 54.1 53.8 51.9 46.1 40.3 66.2 55.3 51.4 64.2 NUMA: 51.4 AVG: 51.4
CORE UTIL(%): 78.8     63.6     57.3     75.9     79.4     69.1     81.7     80.8     82.7     76.5     82.5     65.9     79.3     77.4     72.4     74.1     82.4     84.5     84.2     76.1     77.8     67.8     84.9     82.6     NUMA: 76.6 AVG: 76.6
         ID         GID NAME             NWLD   %USED    %RUN    %SYS   %WAIT %VMWAIT    %RDY   %IDLE  %OVRLP   %CSTP  %MLMTD  %SWPWT 
   41877211    41877211 ora-db-07          22  976.58  973.21    8.02 1165.76   10.79   14.55  555.71    4.65   46.48    0.00    0.00 
   41877212    41877211 vmx                 1    0.12    0.10    0.02   99.90       -    0.00    0.00    0.00    0.00    0.00    0.00 
   41877213    41877211 vmast.41877211      1    0.14    0.13    0.01   99.85       -    0.02    0.00    0.00    0.00    0.00    0.00 
   41877214    41877211 vmx-vthread-40      1    0.07    0.03    0.04   99.96       -    0.01    0.00    0.00    0.00    0.00    0.00 
   41877215    41877211 vmx-vthread-41      1    0.15    0.14    0.01   99.83       -    0.03    0.00    0.00    0.00    0.00    0.00 
   41877216    41877211 vmx-mks:ora-db-     1    0.14    0.11    0.03   99.86       -    0.03    0.00    0.00    0.00    0.00    0.00 
   41877217    41877211 vmx-svga:ora-db     1    0.17    0.13    0.04   99.86       -    0.01    0.00    0.00    0.00    0.00    0.00 
   41877218    41877211 vmx-vcpu-0:ora-     1   68.36   67.83    0.98   25.97    0.53    2.53   25.44    0.45    3.67    0.00    0.00 
   41877219    41877211 vmx-vcpu-1:ora-     1   56.01   56.06    0.26   39.22    1.43    1.36   37.79    0.31    3.36    0.00    0.00 
   41877220    41877211 vmx-vcpu-2:ora-     1   58.35   57.99    0.75   38.86    0.23    0.08   38.63    0.39    3.07    0.00    0.00 
   41877221    41877211 vmx-vcpu-3:ora-     1   68.63   68.32    0.40   24.52    0.74    1.54   23.78    0.09    5.62    0.00    0.00 
   41877222    41877211 vmx-vcpu-4:ora-     1   61.59   61.34    0.41   36.89    0.47    0.21   36.42    0.16    1.56    0.00    0.00 
   41877223    41877211 vmx-vcpu-5:ora-     1   64.90   64.86    0.31   33.91    0.26    0.22   33.65    0.27    1.01    0.00    0.00 
   41877224    41877211 vmx-vcpu-6:ora-     1   60.30   59.93    0.82   36.90    1.06    0.25   35.84    0.45    2.92    0.00    0.00 
   41877225    41877211 vmx-vcpu-7:ora-     1   58.96   58.82    0.60   36.63    0.53    2.79   36.10    0.46    1.76    0.00    0.00 
   41877226    41877211 vmx-vcpu-8:ora-     1   67.44   67.48    0.22   28.40    0.43    1.52   27.97    0.26    2.60    0.00    0.00 
   41877227    41877211 vmx-vcpu-9:ora-     1   56.91   56.85    0.37   38.30    0.68    0.32   37.62    0.31    4.53    0.00    0.00 
   41877228    41877211 vmx-vcpu-10:ora     1   52.86   52.42    0.63   45.44    0.38    0.39   45.06    0.19    1.75    0.00    0.00 
   41877229    41877211 vmx-vcpu-11:ora     1   52.67   52.32    0.60   45.45    0.59    0.33   44.86    0.25    1.90    0.00    0.00 
   41877230    41877211 vmx-vcpu-12:ora     1   57.91   58.07    0.20   40.52    0.34    0.12   40.18    0.36    1.29    0.00    0.00 
   41877231    41877211 vmx-vcpu-13:ora     1   66.48   66.48    0.45   26.63    1.30    1.14   25.33    0.45    5.75    0.00    0.00 
   41877232    41877211 vmx-vcpu-14:ora     1   66.38   66.07    0.40   29.19    0.69    0.11   28.50    0.09    4.63    0.00    0.00 
   41877233    41877211 vmx-vcpu-15:ora     1   58.04   57.73    0.47   39.67    1.13    1.54   38.54    0.16    1.06    0.00    0.00 
   42042986    42042986 app-11              9  226.33  226.13    0.52  673.42    0.50    0.43  172.92    0.32    0.02    0.00    0.00 
   43538739    43538739 app-16              9  219.65  218.65    1.15  680.58    1.36    0.76  179.22    0.15    0.01    0.00    0.00 
   43212445    43212445 app-15              9  212.39  211.83    0.74  687.53    1.80    0.60  185.73    0.18    0.04    0.00    0.00 
   42620682    42620682 app-13              9  210.05  209.59    0.66  689.43    1.81    0.73  187.62    0.20    0.25    0.00    0.00 
   42917684    42917684 app-14              9  209.25  208.91    0.51  689.77    1.71    1.02  188.06    0.17    0.30    0.00    0.00 
   42226025    42226025 app-12              9  206.09  205.68    0.57  693.84    2.28    0.47  191.56    0.16    0.01    0.00    0.00 
   43775864    43775864 jump-01             6   40.62   40.48    0.23  559.36    0.37    0.16   58.99    0.09    0.00    0.00    0.00 
   44242339    44242339 ntp-03              6   34.34   34.12    0.30  565.60    0.76    0.28   64.84    0.08    0.00    0.00    0.00 
   44093656    44093656 dns-02              6   29.92   29.85    0.09  569.72    0.81    0.43   68.91    0.02    0.00    0.00    0.00 
   44246113    44246113 system             95    2.60    3.05    0.00 9494.85       -    2.10    0.00    0.00    0.00    0.00    0.00 
   44310014    44310014 hostd.2098125      47    0.54    0.70    0.00 4699.17       -    0.13    0.00    0.00    0.00    0.00    0.00 
   44434206    44434206 envoy.2098611      17    0.52    0.64    0.00 1699.23       -    0.13    0.00    0.00    0.00    0.00    0.00 
   44520951    44520951 esxtop.2561833      1    0.27    0.35    0.00   99.48       -    0.17    0.00    0.00    0.00    0.00    0.00 
   44354861    44354861 vpxa.2098398       41    0.13    0.14    0.00 4099.86       -    0.01    0.00    0.00    0.00    0.00    0.00 
```

Which statements are correct?

- A. PCPU UTIL near half shows free threads existed while vcpu worlds of the large VM sat in %CSTP.
- B. The %CSTP of the large VM shows the host had no thread free for those vCPUs.
- C. %MLMTD at 0 rules out a CPU limit behind the large VM's %RDY.
- D. The large VM's group row adds up its worlds, its 16 vcpu worlds among them, so its %RDY can pass 100%.
- E. %CSTP above 2% on the large VM shows it needs the 8 extra vCPUs.
- F. The 1-vCPU VMs in the output show %CSTP above 0.
- G. A narrower VM would tend to show less %CSTP.
- H. The %RDY on some vcpu worlds has nothing to do with the %CSTP on their siblings.

## Likely wrong answer
B: Co-stop means the host had no free threads. Or E: the VM stalls, so give it more vCPUs.

## Expected key points
- Answer: A, C, D, G.
- A true: the PCPU UTIL(%) line ends with NUMA and AVG between 45 and 55 (one NUMA node, so the node the VM runs in is also about half busy), while several vcpu worlds of ora-db-07 show %CSTP above 2. Threads were free; co-stopped vCPUs are held back to stay in step with a sibling, even when a thread is free for them.
- B false: the misconception. Waiting for a thread is Ready; Co-stop holds a vCPU that ran ahead of a sibling, and half the threads were free.
- C true: %MLMTD (time held back by a limit) is counted inside %RDY; it reads 0.00 on the group row and on every vcpu world, while %RDY is above 0, so the Ready is not from a limit.
- D true: a group row adds up all its worlds (vmx, vmast, mks, svga and the 16 vcpu worlds); its %RDY is the sum of the worlds' %RDY, so a 16-vCPU VM can pass 100%.
- E false: wrong action. Co-stop tends to rise with the vCPU count; 8 more vCPUs make it worse.
- F false: reading. jump-01, dns-02 and ntp-03 show %CSTP 0.00: Co-stop needs sibling vCPUs.
- G true: fewer vCPUs keep in step more easily.
- H false: over-correction. Ready on one vCPU is the usual cause of Co-stop on its siblings; the vcpu worlds with %RDY above 0 sit next to siblings in %CSTP.

## Notes
- Paired with the theory question 0053 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C28). Counts only after author approval.
- Review 2026-11-15: options tied to the screen (A, C, D, F) and reworded away from 0053. Key changed from A, C, D, H to A, C, D, G (new options).
- Converted 2026-11-16 from a screenshot to esxtop text generated by a seeded script (project/practical-questions-as-exports-2026-11-15.md). One-socket host, so the per-NUMA-node value is the host value (A). D reworded: the expanded output shows the non-vcpu worlds, and the group row sums them too; truth unchanged. F: "on the screen" became "in the output".

## Metadata
```yaml
id: "0375"
title: "esxtop Co-stop on a host at half load"
product: [vsphere]
technology: [cpu]
task: read-metric
level: 300
answer_type: deterministic
input: [text]
object: [vm, esxi]
tool: [esxtop]
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/co-stop
  - vsphere/technology/cpu/concepts/vcpu-states
  - vsphere/tools/esxtop/cpu
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/co-stop
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C28"
answer: [A, C, D, G]
misconception: [B]
misconception_type: [provider-vs-consumer]
pair: "0053"
status: draft
```
