# Run far above Used: add vCPUs?

## Prompt
- A 4-vCPU Ubuntu VM runs an API service. The application team says it is slow and asks for 4 more vCPUs.
- Its host runs about 30 other VMs. The host power policy is Balanced.
- [The attached VCF Operations export](0104/ubuntu-api-04-cpu-7-days.csv) holds 7 days in 2-hour points, each the average of the 5-minute values: CPU Run, Used, System and Overlap in ms per 5-minute collection cycle, summed over the 4 vCPUs (1,200,000 ms is 100%), and Ready (%) and Co-stop (%).

Do you add the vCPUs? Explain what the counters show and what you check instead.

## Likely wrong answer
"Used is less than half of Run, so the VM gets less than half the CPU it needs: add the 4 vCPUs."

## Expected key points
- No: Run is about 375,000 of 1,200,000 ms (about 31%). The 4 vCPUs are far from full.
- The VM does not wait for CPU: Ready below 1% and Co-stop near 0.
- Used is about 44% of Run, with little System and Overlap: each ms of run does less work. The likely causes are a lower clock speed (power saving under the Balanced policy) and busy sibling threads (Hyper-Threading).
- Check the host: the power policy and the actual frequency, and how busy the sibling threads are (Utilization against Core Utilization).
- More vCPUs change neither frequency nor Hyper-Threading. Before any size change, ask for the guest's view: run queue and per-process CPU.

## Notes
- From the author's samples: a 4-vCPU 64-bit Ubuntu VM with Used about 44% of Run, minimal System and Overlap; Used lowered by power saving and SMT; if Run is far from 100% and the team wants faster performance, the answer is not to add vCPUs. Values reproduced in the export.

## Metadata
```yaml
id: "0104"
title: "Run far above Used: add vCPUs?"
product: [vsphere, vcf-operations, linux]
technology: [cpu]
task: troubleshoot
level: 400
answer_type: judged
input: [table]
object: [vm, esxi]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/cpu/troubleshooting/run-vs-used-gap
  - vsphere/technology/cpu/metrics/virtual-motherboard/used
  - vsphere/technology/cpu/metrics/virtual-motherboard/run
  - vsphere/technology/cpu/concepts/power-states
knowledge_main: vsphere/technology/cpu/troubleshooting/run-vs-used-gap
attachments:
  - 0104/ubuntu-api-04-cpu-7-days.csv
origin: book
source_path: "Author samples (docx, 2026-11-12) > Why Run is higher than Used"
misconception_type: [frequency-and-hyper-threading]
status: draft
```
