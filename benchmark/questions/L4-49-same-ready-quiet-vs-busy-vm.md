# The same CPU Ready on quiet and busy VMs

## Prompt
- The team alerts when a VM's CPU Ready passes 5% (per vCPU, 20-second peak). No alert fired today.
- Between 10:00 and 11:00 the web team reported slow page loads on web-01, web-02 and web-03. The batch team reported nothing.
- [The attached VCF Operations list](0106/vms-cpu-ready-10-to-11.csv) shows each VM on the host. For each VM it takes the 20-second sample with the highest Ready in that hour, and gives CPU Ready (%) and CPU Net Run (%) in that same sample.

Which VMs lose the most to CPU Ready, and why did the alert not catch them? What would you change in how the team reads Ready?

## Likely wrong answer
"No VM passed 5%, so CPU Ready is not the cause. batch-01 at 4.6% is the worst VM."

## Expected key points
- Read Ready against the time the VM runs. The web VMs wait about 3% while they run about 6%: for every 2 ms of work they wait about 1 ms, so their work takes about 1.5 times as long.
- erp-app-01 waits 2.4% against 12% of run: its work takes about 1.2 times as long.
- batch-01 and batch-02 wait 4.2-4.6% against 94-95.5% of run: their work takes about 5% longer, and a batch job does not notice.
- A flat Ready threshold ignores how busy the VM is: it is closest to firing on the busy VMs that barely suffer, and it misses the quiet, interactive VMs that do.
- For interactive VMs, read Ready relative to Run (or alert on a lower level), keep the 20-second peak, and check whether many VMs on the host wait at the same time (a busy host).

## Notes
- Mechanism: 2% Ready on 10% Run delays about 20% of the work; the application may not notice 2% on 98% Run (knowledge base, VM CPU Ready, sections Read against Run and Guest OS sizing).

## Metadata
```yaml
id: "0106"
title: "The same CPU Ready on quiet and busy VMs"
product: [vsphere, vcf-operations]
technology: [cpu]
task: read-metric
level: 400
answer_type: judged
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
