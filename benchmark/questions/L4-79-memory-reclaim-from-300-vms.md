# Which VMs to reclaim memory from

## Prompt
The attached table is a VCF Operations export of 300 VMs over 30 days: configured memory, Consumed, Active, Ballooned, Swapped, Guest OS Needed Memory, Guest OS Page-out Rate (peak), Memory Contention (peak).

- The owner of the cluster asks for 1 TB of memory back from the VMs, without hurting any application.

Pick the 5 VMs you would reclaim memory from first. For each, give the counters that support it, and say which counters you did not use, and why.

## Input to supply
- Source: VCF Operations 9.1 export (View > Export as XLSX), 300 powered-on VMs, 30 days, one row per VM.
- Columns: VM name, Guest OS (Windows or Linux), configured memory (GB), Consumed (GB, max), Active (GB, max), Ballooned (GB, max), Swapped (GB, max), Guest OS Needed Memory (GB, max), Guest OS Page-out Rate (peak, max), Memory Contention (%, peak max), VMware Tools running (yes or no).
- Condition for the key: at least 5 VMs have Guest OS Needed Memory below 50% of configured memory, Page-out Rate near 0, and Contention 0; at least 3 VMs have low Active but high Guest OS Needed Memory (database or Java caches); at least 2 VMs have no Guest OS data (Tools not running).
- Record in the Notes the 5 VM names that meet the first condition: they become the key.
- Save as `benchmark/questions/79/vm-memory-300-vms.xlsx`.

## Likely wrong answer
"Reclaim from the VMs with the lowest Active memory."

## Expected key points
- Size from the Guest OS counters (Guest OS Needed Memory, Page-out Rate): the question is what the Windows or Linux workload demands. This is Guest OS sizing, not VM footprint.
- The 5 VMs listed in the Notes of this question: Guest OS Needed Memory well below configured, page-out near 0, no contention.
- Active is not used: it is a VM-level estimate of recently touched pages, and it undercounts caches that a database or Java heap depends on. Low Active with high Guest OS Needed Memory is not a candidate.
- Consumed is not used to size down: it stays high once pages are touched, whatever the guest uses now.
- Ballooned pages are still counted in the Guest OS counters: exclude them when working out Guest OS utilization.
- VMs without Guest OS data (Tools not running) are not sized from this table: fix the data first.

## Notes
- Previous id: question-0079 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "79"
title: "Which VMs to reclaim memory from"
product: [vcf-operations, windows, linux]
technology: [memory]
task: decide-capacity
level: 400
answer_type: judged
input: [table]
knowledge:
  - operations-management/capacity/rightsizing
  - vsphere/technology/memory/concepts/guest-os-vs-vm-memory
  - vsphere/technology/memory/metrics/virtual-motherboard/active
  - vsphere/technology/memory/metrics/virtual-motherboard/ballooned
attachments:
  - 79/vm-memory-300-vms.xlsx
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
status: awaiting-input
```
