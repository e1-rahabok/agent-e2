# esxtop: the time a vCPU could not run

## Prompt
- An application owner asks how much of the last minutes the vCPUs of his 4-vCPU VM erp-05 spent unable to run.
- You run esxtop on its host, open the CPU panel and expand the VM with `e`:

```text
3:42:18pm up 88 days 06:12, 1104 worlds, 5 VMs, 22 vCPUs; CPU load average: 1.13, 1.11, 1.02
PCPU USED(%): 50.6 43.9 42.2 38.0 45.2 49.5 47.1 38.9 37.9 39.9 53.4 37.3 46.5 46.8 48.0 43.1 NUMA: 44.3 AVG: 44.3
PCPU UTIL(%): 91.9 79.2 82.6 73.3 85.7 88.5 87.4 70.5 70.7 72.5 96.7 70.1 89.0 89.2 96.0 75.1 NUMA: 82.4 AVG: 82.4
CORE UTIL(%): 96.7     92.5     96.4     99.5     93.6     92.2     98.0     97.0     NUMA: 95.7 AVG: 95.7
         ID         GID NAME             NWLD   %USED    %RUN    %SYS   %WAIT %VMWAIT    %RDY   %IDLE  %OVRLP   %CSTP  %MLMTD  %SWPWT 
      45875       45875 web-31              9   93.86  138.23    2.01  751.92    3.15    6.05  695.12    1.39    3.80    0.00    0.00 
      44397       44397 web-32              8   45.95   68.09    1.29  722.97    2.38    3.28  678.99    0.53    5.66    0.00    0.00 
      50341       50341 bld-agent-07        5   82.55  131.91    2.86  351.16    4.74   11.10  290.63    0.17    5.83    0.00    0.00 
      24958       24958 sql-12              5   79.58  116.07    2.66  369.60    2.43   10.44  297.74    0.59    3.89    0.00    0.00 
      52817       52817 erp-05              7  105.14  159.15    3.62  518.53   13.25   20.50  206.08    1.61    1.82    0.00    5.92 
      52818       52817 vmx                 1    0.30    0.30    0.00   99.70       -    0.00    0.00    0.00    0.00    0.00    0.00 
      52819       52817 vmx-vcpu-0:erp-05   1   23.84   35.02    0.94   58.50    3.30    6.26   55.20    0.37    0.22    0.00    1.41 
      52820       52817 vmx-vcpu-1:erp-05   1   27.46   44.62    1.10   48.01    1.76    7.07   46.25    0.43    0.30    0.00    1.24 
      52821       52817 vmx-vcpu-2:erp-05   1   28.31   41.85    0.88   54.12    4.16    3.01   49.96    0.52    1.02    0.00    1.45 
      52822       52817 vmx-vcpu-3:erp-05   1   24.77   36.90    0.70   58.70    4.03    4.12   54.67    0.29    0.28    0.00    1.82 
      52823       52817 vmx-mks:erp-05      1    0.23    0.23    0.00   99.74       -    0.03    0.00    0.00    0.00    0.00    0.00 
      52824       52817 vmx-svga:erp-05     1    0.23    0.23    0.00   99.76       -    0.01    0.00    0.00    0.00    0.00    0.00 
```

Which statements are correct?

- A. %RDY on a vcpu world is time it had work and no physical thread to run on.
- B. %CSTP on a vcpu world is time it was held back to stay in step with a sibling.
- C. %SWPWT on a vcpu world is time it stalled for a page coming back from ESXi swap.
- D. %OVRLP is time a running vCPU was interrupted for kernel work: the guest made no progress.
- E. On each vcpu world, %RUN, %RDY, %CSTP and %WAIT add up to about 100%.
- F. All of %WAIT is time the vCPUs were held back, so it adds to the VM's CPU wait.
- G. Swap wait has a memory cause, so it does not count as time the vCPU was stopped.
- H. On each vcpu world, %SWPWT is part of %VMWAIT, not added on top of it.
- I. %USED on each vcpu world shows how long that vCPU was stopped.
- J. %RDY is above 0 on every vcpu world: add vCPUs to the VM.
- K. %SWPWT reads 0 on every vcpu world, so memory plays no part in the wait here.

## Likely wrong answer
I: %USED read as the time the vCPUs stopped. Or F: all of %WAIT is time lost to the VM. Or G: swap wait is memory, not time the vCPU stopped.

## Expected key points
- Answer: A, B, C, D, E, H.
- A true: Ready is demanded run time the kernel could not give. The vcpu worlds show %RDY of 3-8.
- B true: Co-stop holds a vCPU that ran ahead of a sibling.
- C true: the vCPU stalls until the page is read back; the guest sees a freeze.
- D true: Overlap is time stolen from a running vCPU for system services; the guest is frozen during it, even though Run keeps counting.
- E true: reading. Per vcpu world, %RUN + %RDY + %CSTP + %WAIT = 100%: each `vmx-vcpu-N:erp-05` row adds to 100 (for example 35.02 + 6.26 + 0.22 + 58.50).
- F false: %WAIT = %VMWAIT + %IDLE, and %IDLE is the guest's own idle time, not a wait imposed on it; here %IDLE is most of %WAIT.
- G false: over-correction. Swap wait is a stall of the vCPU, whatever its cause; it belongs to memory contention, but the vCPU could not run.
- H true: %VMWAIT includes %SWPWT; on every vcpu world %SWPWT is below %VMWAIT, and %WAIT = %VMWAIT + %IDLE with nothing added for swap.
- I false: the misconception. %USED is consumption and moves with frequency and Hyper-Threading; it does not measure stopped time.
- J false: wrong action. More vCPUs tend to raise Ready on a busy host.
- K false: reading. %SWPWT is 0.80 or more on every vcpu world: the vCPUs stall on pages coming back from swap.

## Notes
- Paired with the theory question 0009 (theory and practical; design.md, section 3.9).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C29). Counts only after author approval.
- Review 2026-11-15: condition now requires %WAIT of 40% or more (E decidable); screen reading K (false) added. Key unchanged: A, B, C, D, E, H.
- Changed in the 2026-11-15 audit (cap of two questions per fact): E (most of %WAIT is %IDLE, tested in 0001 and 0372) replaced by the state-sum reading; H (%MLMTD inside %RDY, tested in 0103 and 0066) replaced by the %SWPWT-inside-%VMWAIT reading; I is now the listed misconception in place of F (F's fact is homed in 0001/0372); D, I and J reworded for length. Key letters unchanged.
- Export note for the generator: the vcpu worlds show %USED above %RUN (%USED = %RUN + %SYS - %OVRLP) on a busy Hyper-Threading host, where the knowledge base says %USED falls below %RUN while the sibling thread runs; no option rests on it.
- Converted to exports 2026-11-15 (project/practical-questions-as-exports-2026-11-15.md): the esxtop CPU panel as text, with %VMWAIT (E reads %WAIT = %VMWAIT + %IDLE). No option changed. E, H and K are the options only the panel decides; A-D repeat the pair's facts (open finding of the 2026-11-15 review, left to the author).

## Metadata
```yaml
id: "0376"
title: "esxtop: the time a vCPU could not run"
product: [vsphere]
technology: [cpu, memory]
task: read-metric
level: 300
answer_type: deterministic
input: [text]
object: [vm]
tool: [esxtop]
knowledge:
  - vsphere/technology/cpu/metrics/comparisons/vm-contention-metrics
  - vsphere/tools/esxtop/cpu
  - vsphere/technology/cpu/metrics/virtual-motherboard/overlap
  - vsphere/technology/cpu/metrics/virtual-motherboard/swap-wait
  - vsphere/technology/cpu/metrics/virtual-motherboard/wait
knowledge_main: vsphere/technology/cpu/metrics/comparisons/vm-contention-metrics
attachments: []
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C29"
answer: [A, B, C, D, E, H]
misconception: [I]
misconception_type: [consumption-as-contention]
pair: "0009"
status: draft
```
