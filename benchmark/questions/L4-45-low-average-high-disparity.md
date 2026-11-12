# Low average, vCPU Usage Disparity above 100%

## Prompt
- An 8-vCPU Linux appliance VM from a network monitoring vendor. Its hosts have a base clock of 2.0 GHz.
- VCF Operations shows CPU Net Run at about 12.5% all day, and CPU vCPU Usage Disparity at about 132%.
- The vendor says the appliance needs 8 vCPUs. Its users say reports are slow.
- The VM owner reads 12.5% as "mostly idle" and says the VM cannot be the bottleneck.
- [The attached metric export](0101/netmon-appl-01-cpu-5-minute.csv) holds 6 hours in 5-minute points: Net Run, vCPU Usage Disparity, and the Usage of each vCPU.

How can the average be so low while the disparity is above 100%? Is the owner right, and what do you advise on the VM's size?

## Likely wrong answer
"12.5% means the VM is mostly idle, so it is not the bottleneck. A disparity above 100% is a data error: usage cannot pass 100%."

## Expected key points
- Only vCPU 0 works: it runs at about 2,640 MHz while the other 7 vCPUs are near 0. One busy vCPU of 8 gives a Net Run of 12.5%.
- vCPU Usage Disparity is the spread between the busiest and the least busy vCPU. vCPU 0 runs above the 2.0 GHz base clock (Turbo Boost), so its usage is about 132% of base, and the spread passes 100%.
- The owner is wrong: the appliance is saturated on its one working vCPU. The VM-level average hides it.
- The guest uses one CPU only: likely a kernel or service that runs on a single CPU (for example a uniprocessor kernel, or a single-threaded process). Check inside the guest: the CPU count the kernel sees and the per-CPU load.
- More vCPUs will not make it faster; a faster clock would. The 7 idle vCPUs can be removed without slowing it, unless the vendor fixes the guest to use them.

## Notes
- From the author's samples: average utilization 12.5%, Usage Disparity above 100%; plotting each vCPU showed only the first one busy (uniprocessor kernel), and Turbo above 100%. Values reproduced in the export.

## Metadata
```yaml
id: "0101"
title: "Low average, vCPU Usage Disparity above 100%"
product: [vsphere, vcf-operations, linux]
technology: [cpu]
task: troubleshoot
level: 400
answer_type: judged
input: [table]
object: [vm, guest-os]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/cpu/metrics/virtual-motherboard/usage-disparity
  - vsphere/technology/cpu/metrics/virtual-motherboard/net-run
  - vsphere/technology/cpu/concepts/cpu-frequency
knowledge_main: vsphere/technology/cpu/metrics/virtual-motherboard/usage-disparity
attachments:
  - 0101/netmon-appl-01-cpu-5-minute.csv
origin: book
source_path: "Author samples (docx, 2026-11-12) > Average utilization 12.5% yet Usage Disparity above 100%"
misconception_type: [average-hides-worst, frequency-and-hyper-threading]
status: draft
```
