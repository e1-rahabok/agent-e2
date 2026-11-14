# The same CPU Ready on quiet and busy VMs

## Prompt
- The team alerts when a VM's CPU Ready passes 5% (per vCPU, 20-second peak). No alert fired today.
- Between 10:00 and 11:00 the web team reported slow page loads on web-01, web-02 and web-03. The batch team reported nothing.
- [The attached VCF Operations list](0106/vms-cpu-ready-10-to-11.csv) shows each VM on the host. For each VM it takes the 20-second sample with the highest Ready in that hour, and gives CPU Ready (%) and CPU Net Run (%) in that same sample.

Which VMs lose the most to CPU Ready, why did the alert not catch them, and what would you change in how the team reads Ready? Which statements are correct?

- A. The web VMs lose the most: about 3% Ready against about 6% of run, so their work takes about 1.5 times as long.
- B. erp-app-01 waits 2.4% against 12% of run: its work takes about 1.2 times as long.
- C. batch-01 and batch-02 wait about 4-5% against 94-95% of run: their work takes about 5% longer, which a batch job hardly notices.
- D. A flat Ready threshold ignores how busy the VM is: it nearly fires on busy VMs that barely suffer and misses quiet ones that do.
- E. For interactive VMs, the team should read Ready relative to the time the VM runs, not on its own.
- F. The 20-second peak is the right sample to keep: Ready usually lasts seconds, not minutes.
- G. No VM passed the 5% alert level in that hour, so CPU Ready cannot be the cause of the slow pages.
- H. batch-01, at 4.6%, has the highest Ready of the host and is the VM that loses the most to it.
- I. erp-db-01 loses more than erp-app-01 to Ready, because a 16-vCPU VM is harder to schedule.
- J. The Ready of the web VMs comes from busy sibling threads on their cores (Hyper-Threading).
- K. Ready (%) is not normalized by the vCPU count, so the values of the 8-vCPU batch VMs are overstated.
- L. Adding vCPUs to the web VMs would lower their Ready, since each vCPU would carry less of the load.

## Likely wrong answer
- G: "No VM passed 5%, so CPU Ready is not the cause."
- H: "batch-01 at 4.6% is the worst VM."

## Expected key points
- Answer: A, B, C, D, E, F.
- A true: 3.1/6.2, 2.9/5.8 and 3.0/6.5: about 1 ms of wait for every 2 ms of work.
- B true: 2.4/12.0 = 20%.
- C true: 4.6/94.0 and 4.2/95.5 are about 5%.
- D true: Ready 5% on Run 95% is low; Ready 2% on Run 10% is very high. One threshold for both reads the wrong VMs.
- E true: read Ready against Run (or alert on a lower level for interactive VMs), and check whether many VMs on the host wait at once (a busy host).
- F true: a 5-minute value would dilute a wait that lasts seconds.
- G false: the web VMs, the ones whose users complained, lose about a third of their elapsed time to Ready.
- H false: batch-01 has the highest Ready in %, but only about 5% of its run; the web VMs lose ten times more relative to their work.
- I false: 1.1/55 = 2%, against 20% for erp-app-01.
- J false: a busy sibling thread does not put a vCPU into Ready; Ready means no physical thread was free to run it.
- K false: Ready (%) is normalized by the vCPU count; Ready (ms) is the summed value.
- L false: all else equal, larger VMs show more Ready; a busy host is less likely to run many vCPUs at once.

## Notes
- Mechanism: 2% Ready on 10% Run delays about 20% of the work; the application may not notice 2% on 98% Run (knowledge base, VM CPU Ready, sections Read against Run and Guest OS sizing).
- Converted from judged to multiple choice (Q199 F, 2026-11-14).

## Metadata
```yaml
id: "0106"
title: "The same CPU Ready on quiet and busy VMs"
product: [vsphere, vcf-operations]
technology: [cpu]
task: read-metric
level: 400
answer_type: deterministic
answer: [A,B,C,D,E,F]
misconception: [G,H]
input: [table]
object: [vm]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/ready
  - vsphere/technology/cpu/metrics/virtual-motherboard/net-run
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/ready
attachments:
  - 0106/vms-cpu-ready-10-to-11.csv
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
misconception_type: [threshold-transplanted]
status: draft
```
