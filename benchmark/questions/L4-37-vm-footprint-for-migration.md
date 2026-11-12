# VM footprint for a migration to slower CPUs

## Prompt
The attached table is an export of 150 VMs that will move from a cluster with a nominal clock of 2.5 GHz to one with 2.0 GHz. Per VM: vCPUs, the per-vCPU CPU states summed over the vCPUs (Used, Overlap, Co-stop, Ready, Other Wait, in ms per 20-second sample), System (ms), and Consumed, Overhead, Swapped, Compressed and Ballooned memory (GB).

- Row db-01: 8 vCPUs; Used 70,000, Overlap 2,000, Co-stop 4,000, Ready 16,000, Other Wait 4,000; System 4,000. Memory: Consumed 60, Overhead 0.5, Swapped 2, Compressed 1, Ballooned 4.

Work out the footprint of db-01 in the source cluster: CPU as a share of its vCPUs and in GHz, and memory in GB. How many vCPUs does it take in the destination cluster? Show the formulas.

## Input to supply
- Source: VCF Operations 9.1 or vCenter real-time export, 150 VMs, peak 20-second sample of the busiest hour, one row per VM.
- Columns: VM name, vCPUs, Used, Overlap, Co-stop, Ready, Other Wait (each summed over the vCPUs, ms), System (ms), Consumed, Overhead, Swapped, Compressed, Ballooned (GB).
- Condition for the key: row db-01 holds exactly the values in the prompt. Other rows are real data.
- Save as `benchmark/questions/83/vm-footprint-150-vms.xlsx`.

## Likely wrong answer
"Footprint = Used only: 70,000 / 160,000 = 44%, so 4 vCPUs."

## Expected key points
- VM CPU Needed = (sum over vCPUs of (Used + Overlap + Co-stop + Ready + Other Wait) + System) / (20,000 × vCPU).
- db-01: (96,000 + 4,000) / 160,000 = 0.625, so 62.5% of 8 vCPUs, the equal of 5 vCPUs at the source speed.
- In GHz: 0.625 × 8 × 2.5 GHz = 12.5 GHz.
- At 2.0 GHz: 12.5 / 2.0 = 6.25, so at least 7 vCPUs in the destination cluster.
- Memory: VM Memory Needed = Consumed + Overhead + Swapped + Compressed + Ballooned = 60 + 0.5 + 2 + 1 + 4 = 67.5 GB. Memory contention is excluded: it measures speed, not space.
- Contention (Ready, Co-stop, Other Wait) is included: runtime the VM demanded but did not get. The Guest OS queue is excluded.

## Notes
- Previous id: question-0083 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0083"
title: "VM footprint for a migration to slower CPUs"
product: [vsphere, vcf-operations]
technology: [system, cpu, memory]
task: decide-capacity
level: 400
answer_type: judged
input: [table]
knowledge:
  - sp5-framework/capacity/vm-footprint-sizing
attachments:
  - 0083/vm-footprint-150-vms.xlsx
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
status: awaiting-input
```
